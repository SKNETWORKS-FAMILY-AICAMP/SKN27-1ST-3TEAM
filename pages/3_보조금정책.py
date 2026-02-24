import streamlit as st
from numpy.random import default_rng as rng
import pandas as pd
import plotly.graph_objects as go
from common.db import DB

## class DB에서 가져오기!
test = DB("subsidy", "local_gov_name")
table_1 = test.select_table()[:8]

test2 = DB("ev_registration", "ev_count")
table_2 = test2.select_table()[:8]
tt = table_2["ev_count"]

# 전기차 보조금 합계 : sum_ev 수소차 보조금 합계 : sum_h2   평균 : sum_ev_avg, sum_h2_avg   
sum_ev = table_1["ev_sedan_amt"]+table_1["ev_small_amt"]+table_1["ev_mid_amt"]+table_1["ev_large_amt"]
sum_h2 = table_1["h2_sedan_amt"]+table_1["h2_van_amt"]
sum_ev_avg = sum(sum_ev)//len(table_1)
sum_h2_avg = sum(sum_h2)//len(table_1)

df_1 = pd.DataFrame({
    "지역": table_1["local_gov_name"],  
    "전기차 보조금":sum_ev,
    "수소차 보조금":sum_h2,
    "전기차 평균":sum_ev_avg,
    "수소차 평균":sum_h2_avg
})

list_1 = [sum_ev_avg, sum_h2_avg]

df_2 = pd.DataFrame({
    "지역": table_1["local_gov_name"],
    "전체 보조금":sum_ev+sum_h2
})
###

container = st.container(border = True, height = 140)
container.header("💸보조금 정책 분석")
container.text("지역별 보조금 지원 현황 및 정책 효과 분석")


col1, col2, col3 = st.columns(3)
col1.metric("💵평균 전기차 보조금", list_1[0], border =True, width = 250, height = "content")
col2.metric("💵평균 수소차 보조금", list_1[1], border =True, width = 250, height = "content")
col3.metric("🌉최고 보조금 지역", df_2["지역"][df_2["전체 보조금"].idxmax()], border =True, width = 250, height = "content")


fig = go.Figure()

# 1️⃣ 전기차 (막대, 왼쪽)
fig.add_trace(go.Bar(
    x=df_1["지역"],
    y=df_1["전기차 보조금"],
    name="전기차",
    yaxis="y1",
    opacity=0.7
))

# 3️⃣ 충전기 (막대, 왼쪽)
fig.add_trace(go.Bar(
    x=df_1["지역"],
    y=df_1["수소차 보조금"],
    name="수소차",
    yaxis="y1",
    opacity=0.7
))

# 3️⃣ 전기차 수요 (선, 오른쪽 축)
fig.add_trace(go.Scatter(
    x=df_1["지역"],
    y=tt,
    name="전기차 수요",
    mode="lines+markers",
    yaxis="y2"
))

fig.update_layout(
    title="전기차와 충전기 수요량",
    xaxis=dict(title="지역"),
    yaxis=dict(
        title="보조금(만원)",
        side="left"
    ),
    yaxis2=dict(
        title="전기차(만대)",
        overlaying = 'y',
        side="right"
    ),
    barmode="group"
)
st.plotly_chart(fig, use_container_width=True)

st.dataframe(df_1[["지역","전기차 보조금","수소차 보조금"]], use_container_width=True)