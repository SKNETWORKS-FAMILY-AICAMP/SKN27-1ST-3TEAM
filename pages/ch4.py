import streamlit as st
import sys
sys.path.append('..')
from db import query
import pandas as pd

st.title("🔮 Ch.4 - 앞으로의 10년")

# 1. 전기차 성장 추이 (CAGR)
st.subheader("📌 전기차 연도별 성장 추이")
df_ev = query("""
    SELECT reg_year, SUM(ev_count) AS ev_total
    FROM ev_registration
    GROUP BY reg_year
    ORDER BY reg_year
""")
st.dataframe(df_ev)
st.line_chart(df_ev.set_index('reg_year')['ev_total'])

# CAGR 계산
first = df_ev['ev_total'].iloc[0]
last = df_ev['ev_total'].iloc[-1]
n = len(df_ev) - 1
cagr = ((last / first) ** (1/n) - 1) * 100
st.metric("연평균 성장률 (CAGR)", f"{cagr:.1f}%")

# 2. 수송 CO2 감소 추이
st.subheader("📌 전국 수송 CO2 감소 추이 (VKT 기준)")
df_co2 = query("""
    SELECT reg_year, ROUND(SUM(emission), 2) AS total_emission
    FROM transport_co2
    WHERE criteria = 'VKT'
    GROUP BY reg_year
    ORDER BY reg_year
""")
st.dataframe(df_co2)
st.line_chart(df_co2.set_index('reg_year')['total_emission'])

# 3. 수소차 성장 추이
st.subheader("📌 수소차 연도별 성장 추이")
df_h2 = query("""
    SELECT reg_year, h2_count
    FROM hydrogen_yearly
    ORDER BY reg_year
""")
st.dataframe(df_h2)
st.line_chart(df_h2.set_index('reg_year')['h2_count'])
