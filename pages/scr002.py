import streamlit as st
import pandas as pd
from db import query
import numpy as np

st.title("인프라 격차 분석")

data = {
    "region" : ["서울","부산","대구","인천","광주","대전","울산","세종","경기","강원","충북","충남","전북","전남","경북","경남","제주"],
    "ev_count" : [15000, 8200, 6300, 7400, 4100, 5200, 3900,1800, 21000, 3200, 2800, 3500,2900, 3300, 4700, 5600, 2600],
    "h2_count" : [15000, 8200, 6300, 7400, 4100, 5200, 3900,1800, 21000, 3200, 2800, 3500,2900, 3300, 4700, 5600, 2600],
    "charger_yearly" : [15000, 8200, 6300, 7400, 4100, 5200, 3900,1800, 21000, 3200, 2800, 3500,2900, 3300, 4700, 5600, 2600]
}
df = pd.DataFrame(data)
#지역 셀렉트 박스
selected_region = st.selectbox("지역 선택", df["region"])

# 선택값에 맞는 데이터 찾기
selected_ev_value = df[df["region"] == selected_region]["ev_count"]
selected_h2_value = df[df["region"] == selected_region]["h2_count"]
selected_charger_value = df[df["region"] == selected_region]["charger_yearly"]
# metric 출력
col1, col2, col3 ,col4 = st.columns(4)

col1.metric("전기차 등록 대수", selected_ev_value)
col2.metric("수소차 등록 대수", selected_h2_value)
col3.metric("총 충전기 수", selected_charger_value)
col4.metric("전기차 1대당 충전기 수", selected_ev_value/selected_charger_value)



#지역별 전기차 그래프
st.header("지역별 전기차 등록 현황")
query_sql = """
SELECT r.region_name, e.ev_count
FROM ev_registration e
JOIN region r ON e.region_id = r.region_id
"""


df = query(query_sql)

#df = df.sort_values(by="ev_count", ascending= False).reset_index(drop= True)#왜 내림차순 정렬이 안되는지 모르겠음
st.bar_chart(df, x="region_name", y="ev_count")

#지역별 충전기 현황
st.header("지역별 충전기 현황")

df2 = query(
    """
 SELECT *
 FROM charger_yearly
 WHERE charger_id =12
 """
 )
df2 = df2.rename(columns = {
    "seoul_cnt": "서울",
    "gyeonggi_cnt" : "경기",
    "incheon_cnt" : "인천",
    "gangwon_cnt" : "강원",
    "chungcheong_cnt" : "충청",
    "jeolla_cnt"    : "전라",
    "gyeongsang_cnt"    : "경상",
    "jeju_cnt"  : "제주"
})

#df2 = query(query_sql2)
df_chart = df2.T
df_chart.columns = ["count"]


st.bar_chart(df_chart[2:9])

#지역, 전기차대수  , 충전기수, 전기차1대당 충전기수,

st.header("지역별 상세 현황")

def regiondata():
    return pd.DataFrame(
            np.random.randint(100, 1000, size=(8, 4)),
            index=[0,1,2,3,4,5,6,7],
            columns=['지역','전기차','충전기','전기차당 충전기']  
    )

rg = regiondata()
st.dataframe(rg,)