import streamlit as st
import sys
sys.path.append('..')
from db import query

st.title("🌍 Prologue - 지구가 뜨거워지고 있다")

# 1. 연도별 평균기온
st.subheader("📌 연도별 평균기온 (2015~2025)")
df_temp = query("""
    SELECT reg_year, avg_temp
    FROM temperature_yearly
    ORDER BY reg_year
""")
st.dataframe(df_temp)
st.line_chart(df_temp.set_index('reg_year')['avg_temp'])

# 2. 전국 수송 CO2 연도별
st.subheader("📌 전국 수송 CO2 연도별 합계 (2010~2023, VKT 기준)")
df_co2 = query("""
    SELECT reg_year, ROUND(SUM(emission), 2) AS total_emission
    FROM transport_co2
    WHERE criteria = 'VKT'
    GROUP BY reg_year
    ORDER BY reg_year
""")
st.dataframe(df_co2)
st.line_chart(df_co2.set_index('reg_year')['total_emission'])

# 3. 시도별 수송 CO2 (2023년 기준)
st.subheader("📌 시도별 수송 CO2 (2023년, VKT 기준)")
df_co2_region = query("""
    SELECT r.region_name, ROUND(t.emission, 2) AS emission
    FROM transport_co2 t
    JOIN region r ON t.region_id = r.region_id
    WHERE t.criteria = 'VKT' AND t.reg_year = 2023
    ORDER BY emission DESC
""")
st.dataframe(df_co2_region)
st.bar_chart(df_co2_region.set_index('region_name')['emission'])
