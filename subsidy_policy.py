import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import common.db as db 

# 데이터 가져오기
def get_subsidy_data():
    df_subsidy = db.fetch_data(db.queries["subsidy_all"])
    df_ev_reg = db.fetch_data(db.queries["ev_reg_all"])
    
    if df_subsidy is None or df_ev_reg is None:
        return None, None
    
    # 상위 8개 지역만 사용
    return df_subsidy.head(8), df_ev_reg.head(8)

df_sub_raw, df_ev_raw = get_subsidy_data()

if df_sub_raw is not None:    
    # 전기차 보조금 합계
    sum_ev = (df_sub_raw["ev_sedan_amt"] + df_sub_raw["ev_small_amt"] + 
              df_sub_raw["ev_mid_amt"] + df_sub_raw["ev_large_amt"])
    
    # 수소차 보조금 합계
    sum_h2 = df_sub_raw["h2_sedan_amt"] + df_sub_raw["h2_van_amt"]
    
    # 평균 계산
    sum_ev_avg = int(sum_ev.mean())
    sum_h2_avg = int(sum_h2.mean())

    df_1 = pd.DataFrame({
        "지역": df_sub_raw["local_gov_name"],  
        "전기차 보조금": sum_ev,
        "수소차 보조금": sum_h2,
        "전기차 평균": sum_ev_avg,
        "수소차 평균": sum_h2_avg
    })

    df_2 = pd.DataFrame({
        "지역": df_sub_raw["local_gov_name"],
        "전체 보조금": sum_ev + sum_h2
    })

    tt = df_ev_raw["ev_count"] # 그래프용 전기차 등록수

    # UI 부분
    container = st.container(border=True, height=140)
    container.header("💸 보조금 정책 분석")
    container.text("지역별 보조금 지원 현황 및 정책 효과 분석")

    col1, col2, col3 = st.columns(3)
    col1.metric("💵 평균 전기차 보조금", f"{sum_ev_avg} 만원", border=True)
    col2.metric("💵 평균 수소차 보조금", f"{sum_h2_avg} 만원", border=True)
    col3.metric("🌉 최고 보조금 지역", df_2.loc[df_2["전체 보조금"].idxmax(), "지역"], border=True)

    # Plotly 그래프
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_1["지역"], y=df_1["전기차 보조금"], name="전기차 보조금", yaxis="y1", opacity=0.7))
    fig.add_trace(go.Bar(x=df_1["지역"], y=df_1["수소차 보조금"], name="수소차 보조금", yaxis="y1", opacity=0.7))
    fig.add_trace(go.Scatter(x=df_1["지역"], y=tt, name="전기차 수요(등록수)", mode="lines+markers", yaxis="y2"))

    fig.update_layout(
        title="지역별 보조금 및 전기차 등록 현황",
        xaxis=dict(title="지역"),
        yaxis=dict(title="보조금(만원)", side="left"),
        yaxis2=dict(title="전기차 등록수", overlaying='y', side="right"),
        barmode="group"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df_1[["지역","전기차 보조금","수소차 보조금"]], use_container_width=True)
else:
    st.error("데이터를 불러오는 데 실패했습니다.")