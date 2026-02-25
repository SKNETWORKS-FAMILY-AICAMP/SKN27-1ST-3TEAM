import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import common.db as db

# 차량 데이터
def car_data():
    df_ev = db.fetch_data(db.queries["ev_main"])       # 전기차 등록대수 (최신연도)
    df_h2 = db.fetch_data(db.queries["h2_main"])       # 수소차 등록대수 (최신연도)
    df_total = db.fetch_data(db.queries["total_main"]) # 전체 차량 등록대수 (최신연도)
    
    if any(df is None for df in [df_ev, df_h2, df_total]):
        return None, None, None
        
    return df_ev, df_h2, df_total

#그래프 데이터
def graph_data():
    df_co2 = db.fetch_data(db.queries["co2"])       #연도별 총 CO2 배출량
    df_temp = db.fetch_data(db.queries["temp"])     #연도별 평균기온
    df_demand = db.fetch_data(db.queries["demand"]) #연도별 전체 차량 등록대수
    
    # 데이터 검증
    if any(df is None for df in [df_co2, df_temp, df_demand]):
        return None, None, None
        
    return df_co2, df_temp, df_demand

# 실행
df_ev, df_h2, df_total = car_data()
df_co2, df_temp, df_demand = graph_data()



### 화면 부분 ####
container = st.container(border = True, height = 140)
container.header("🚗친환경차 분석 대시보드")
container.text("전국 자동차 등록 현황 및 데이터 종합 분석")

if df_ev is not None and df_h2 is not None:
    # 데이터프레임에서 합계 추출
    total_ev = df_ev['ev_count'].sum()                # 전국 전기차 등록대수
    total_h2 = df_h2['h2_count'].sum()                # 전국 수소차 등록대수
    total_vehicle = df_total['total_vehicle'].sum()   # 전체 차량 등록대수
    ratio = (total_ev + total_h2) / total_vehicle * 100 # 친환경차 비율
    
    #'만 대' 단위로 변환
    ev_man = int(total_ev / 10000)
    h2_man = int(total_h2 / 10000)
    
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("전국 전기차 등록", f"{ev_man:}만 대", border=True, height ="content" )
    col2.metric("전국 수소차 등록", f"{h2_man:}만 대", border=True, height ="content" )
    col3.metric("친환경차 비율",  f"{ratio:.2f}%", border =True, height ="content" )
    col4.metric("최신데이터 연도", "2024년", border =True, height ="content" )


# 데이터 검증
if df_co2 is not None and df_temp is not None and df_demand is not None:
    df_merged = pd.merge(df_co2, df_temp, on="연도")
    df_merged = pd.merge(df_merged, df_demand, on="연도").sort_values("연도")

    fig = go.Figure()

    # CO2 배출량
    fig.add_trace(go.Bar(
        x=df_merged["연도"],
        y=df_merged["총_CO2_배출량"],
        name="CO2 배출량",
        marker_color="#A2C8EC",
        yaxis="y1"
    ))

    # 기후 변화
    fig.add_trace(go.Scatter(
        x=df_merged["연도"],
        y=df_merged["평균기온"],
        name="기후 변화",
        mode="lines+markers",
        line=dict(color="#8ECAE6", width=2),
        marker=dict(size=8),
        yaxis="y1"
    ))

    # 차량 수요량
    fig.add_trace(go.Scatter(
        x=df_merged["연도"],
        y=df_merged["전체_등록_대수"],
        name="차량 수요량",
        mode="lines+markers",
        line=dict(color="#FF3B30", width=3),
        marker=dict(size=10),
        yaxis="y2"
    ))

    # 그래프 레이아웃 설정
    fig.update_layout(
        title=dict(text="기후 변화 / 차량 수요 / CO2 배출량", font=dict(size=18)),
        xaxis=dict(title="연도", showgrid=False, tickmode='linear'),
        
        # 왼쪽 축 (기후변화/CO2)
        yaxis=dict(
            title="기후 변화 / CO2",
            side="left",
            showgrid=True,
            gridcolor='rgba(200, 200, 200, 0.3)'
        ),
        
        # 오른쪽 축 (차량 수요량)
        yaxis2=dict(
            title="차량 수요량",
            overlaying="y",
            side="right",
            showgrid=False
        ),
        
        #직관적으로 co2배출량, 차량수요량, 기후변화의 관계를 파악하기 위해 y축을 공유
        plot_bgcolor="white",
        paper_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=50, r=50, t=100, b=50),
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)
