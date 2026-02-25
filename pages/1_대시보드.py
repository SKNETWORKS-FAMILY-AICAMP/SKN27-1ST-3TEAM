import streamlit as st
from numpy.random import default_rng as rng
import pandas as pd
import plotly.graph_objects as go
import pandas as pd
from common.db import DB

#### DB
# 전국 자동차 등록대수
test = DB("total_vehicle_yearly", "total_vehicle")
table_1 = test.select_table()
ev_total = sum(table_1["total_vehicle"])
st.text(table_1)


# 전국 전기차 등록대수
test2 = DB("ev_registration", "ev_count")
table_2 = test2.select_table()
tt = table_2["ev_count"]

# 전국 수소차 등록대수
test3 = DB("hydrogen_yearly", "h2_count")
table_3 = test3.select_table()
tt = table_3["h2_count"]

# 전국 CO2 배출량
test4 = DB("transport_co2", "emission")
table_4 = test4.select_table()
tt = table_4["emission"]


####
container = st.container(border = True, height = 140)
container.header("🚗친환경차 분석 대시보드")
container.text("전국 자동차 등록 현황 및 데이터 종합 분석")

col1, col2, col3, col4 = st.columns(4)
col1.metric("전국 전기차 등록", ev_total, "compare", border =True, height ="content" )
col2.metric("전국 수소차 등록", "9 mph", "-8%", border =True, height ="content" )
col3.metric("친환경차 비율", "86%", border =True, height ="content" )
col4.metric("최신데이터 연도", "2024", border =True, height ="content" )


# 예시 데이터
df = pd.DataFrame({
    "year": [2015,2016,2017,2018,2019,2020],
    "climate_change": [0.9,1.0,1.1,1.3,1.4,1.6],   # 기온 상승
    "vehicle_demand": [100,120,150,170,200,180], # 차량 수요
    "co2": [400,420,450,480,500,470]             # CO2 배출량
})

fig = go.Figure()

# 1️⃣ CO2 (막대)
fig.add_trace(go.Bar(
    x=df["year"],
    y=df["co2"],
    name="CO2 배출량",
    yaxis="y1",
    opacity=0.4
))

# 2️⃣ 기후 변화 (선) >> 안보임.. 기후 변화에 대한 그래프는 제거해야 할 듯

# 3️⃣ 차량 수요량 (선, 오른쪽 축)
fig.add_trace(go.Scatter(
    x=df["year"],
    y=df["vehicle_demand"],
    name="차량 수요량",
    mode="lines+markers",
    yaxis="y2"
))

fig.update_layout(
    title="기후 변화 / 차량 수요 / CO2 배출량",
    xaxis=dict(title="연도"),

    yaxis=dict(
        title="CO2",
        side="left"
    ),

    yaxis2=dict(
        title="차량 수요량",
        overlaying="y",
        side="right"
    ),

    barmode="overlay"
)

st.plotly_chart(fig, use_container_width=True)