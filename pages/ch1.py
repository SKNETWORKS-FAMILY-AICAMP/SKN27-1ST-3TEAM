import streamlit as st
import sys
sys.path.append('..')
from db import query

st.title("📊 Ch.1 - 대한민국 도로의 현실")

# 1. 전체 자동차 연도별
st.subheader("📌 전체 자동차 등록대수 (2015~2025) 누적합계")
df_total = query("""
    SELECT reg_year, total_vehicle 
    FROM total_vehicle_yearly
    ORDER BY reg_year
""")
st.dataframe(df_total)
st.line_chart(df_total.set_index('reg_year')['total_vehicle'])

# 2. 전기차 연도별 전국 합계
st.subheader("📌 전기차 등록대수 연도별 전국 합계")
df_ev = query("""
    SELECT reg_year, SUM(ev_count) AS ev_total
    FROM ev_registration
    GROUP BY reg_year
    ORDER BY reg_year
""")
st.dataframe(df_ev)
st.line_chart(df_ev.set_index('reg_year')['ev_total'])

# 3. 수소차 연도별
st.subheader("📌 수소차 누적 등록대수 (2018~2025)")
df_h2 = query("""
    SELECT reg_year, h2_count
    FROM hydrogen_yearly
    ORDER BY reg_year
""")
st.dataframe(df_h2)
st.line_chart(df_h2.set_index('reg_year')['h2_count'])

# 4. 전체 대비 친환경차 비율
st.subheader("📌 전체 자동차 대비 전기차 비율 (%)")
df_ratio = query("""
    SELECT t.reg_year,
           t.total_vehicle,
           SUM(e.ev_count) AS ev_total,
           ROUND(SUM(e.ev_count) / t.total_vehicle * 100, 2) AS ev_ratio
    FROM total_vehicle_yearly t
    JOIN ev_registration e ON t.reg_year = e.reg_year
    GROUP BY t.reg_year, t.total_vehicle
    ORDER BY t.reg_year
""")
st.dataframe(df_ratio)
st.line_chart(df_ratio.set_index('reg_year')['ev_ratio'])
