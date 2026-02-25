import streamlit as st
import plotly.graph_objects as go
import db

# 차량 데이터
def get_data():
    df_ev = db.fetch_data(db.queries["ev_latest"])           #전기차 최신연도
    df_h2 = db.fetch_data(db.queries["h2_latest"])           #수소차 최신연도
    df_total = db.fetch_data(db.queries["charger_latest"])   #충전기 최신연도
    
    # 데이터 검증
    if any(df is None for df in [df_ev, df_h2, df_total]):
        return None, None, None
        
    return df_ev, df_h2, df_total

# 데이터 가져오기 실행
df_evcount, df_h2count, df_totalcount = get_data()


# 그래프 데이터 함수
def graph_data():
    # 데이터 추출
    df_ev = db.fetch_data(db.queries["ev_regional"])          #시도별 전기차
    df_charger_raw = db.fetch_data(db.queries["charger_raw"]) #충전기

    # 데이터 검증
    if df_ev is None or df_charger_raw is None or df_charger_raw.empty:
        return None

    try:
        row = df_charger_raw.iloc[0]
        
        # 시도별 매핑
        mapping_data = {
            '서울': row['seoul_cnt'], '경기': row['gyeonggi_cnt'], '인천': row['incheon_cnt'],
            '강원': row['gangwon_cnt'], '제주': row['jeju_cnt'],
            '대전': row['chungcheong_cnt'], '세종': row['chungcheong_cnt'], 
            '충북': row['chungcheong_cnt'], '충남': row['chungcheong_cnt'],
            '광주': row['jeolla_cnt'], '전북': row['jeolla_cnt'], '전남': row['jeolla_cnt'],
            '부산': row['gyeongsang_cnt'], '대구': row['gyeongsang_cnt'], 
            '울산': row['gyeongsang_cnt'], '경북': row['gyeongsang_cnt'], '경남': row['gyeongsang_cnt']
        }
        
        # 컬럼
        df_ev['충전기'] = df_ev['지역'].map(mapping_data).fillna(0)
        # 0으로 나누기 방지 처리
        df_ev['전기차당 충전기'] = (df_ev['충전기'] / df_ev['전기차']).replace([float('inf'), -float('inf')], 0).round(2)
        
        return df_ev.head(10) # 10개 지역만 추출

    except Exception as e:
        st.error(f"그래프 가공 중 오류: {e}")
        return None

# 그래프 데이터
df = graph_data()



### 화면 부분 ####
container = st.container(border=True, height=140)
container.header("📊 인프라 격차 분석")
container.text("지역별 충전 인프라 및 친환경차 현황 비교")

if all(df is not None for df in [df_evcount, df_h2count, df_totalcount]):
    total_ev = df_evcount['ev_count'].sum()          # 전기차 총 대수
    total_h2 = df_h2count['h2_count'].sum()          # 수소차 총 대수
    total_charger = df_totalcount['total_cnt'].sum() # 충전기 총 대수
    
    # '만 대' 단위로 변환
    ev_man = int(total_ev / 10000) 
    h2_man = int(total_h2 / 10000)

    charger_man = int(total_charger / 10000) # 총 충전기 수
    ev_charger = round(total_charger / total_ev, 2) if total_ev > 0 else 0 # 전기 차량별 충전기
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("전국 전기차 등록", f"{ev_man}만 대", border=True)
    col2.metric("수소차 등록 대수", f"{h2_man}만 대", border=True)
    col3.metric("총 충전기 수", f"{charger_man}만 대", border=True)
    col4.metric("전기차량 충전기", f"{ev_charger}기/대", border=True)


# 그래프와 표
if df is not None:
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df["지역"], y=df["전기차"], name="전기차", 
        yaxis="y1", marker_color='skyblue', offsetgroup=1
    ))

    fig.add_trace(go.Bar(
        x=df["지역"], y=df["충전기"], name="충전기", 
        yaxis="y2", marker_color='orange', offsetgroup=2
    ))

    fig.update_layout(
        title="전기차와 충전기 수요량 (지역별 비교)",
        xaxis=dict(title="지역"),
        yaxis=dict(title="전기차 수 (대)", side="left", showgrid=True),
        yaxis2=dict(title="충전기 수 (대)", side="right", overlaying="y", anchor="x", showgrid=False),
        barmode="group",
        legend=dict(x=1.1, y=1),
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df[['지역', '전기차', '충전기', '전기차당 충전기']], use_container_width=True)




