import streamlit as st
import sys
sys.path.append('..')
from db import query

st.title("📈 Ch.2 - 그래도 변하고 있다")

# 1. 전기차 연도별 성장
st.subheader("📌 전기차 연도별 전국 등록대수")
df_ev = query("""
    SELECT reg_year, SUM(ev_count) AS ev_total
    FROM ev_registration
    GROUP BY reg_year
    ORDER BY reg_year
""")
st.dataframe(df_ev)
st.line_chart(df_ev.set_index('reg_year')['ev_total'])

# 2. 수소차 연도별 성장
st.subheader("📌 수소차 연도별 누적 등록대수")
df_h2 = query("""
    SELECT reg_year, h2_count
    FROM hydrogen_yearly
    ORDER BY reg_year
""")
st.dataframe(df_h2)
st.line_chart(df_h2.set_index('reg_year')['h2_count'])

# 3. 충전소 연도별 성장
st.subheader("📌 전기차 충전소 연도별 총계")
df_charger = query("""
    SELECT reg_year, total_cnt
    FROM charger_yearly
    ORDER BY reg_year
""")
st.dataframe(df_charger)
st.line_chart(df_charger.set_index('reg_year')['total_cnt'])

# 4. 충전소 권역별 현황 (2025년)
st.subheader("📌 충전소 권역별 현황 (2025년)")
df_charger_region = query("""
    SELECT seoul_cnt, gyeonggi_cnt, incheon_cnt, gangwon_cnt,
        chungcheong_cnt, jeolla_cnt, gyeongsang_cnt, jeju_cnt
    FROM charger_yearly
    WHERE reg_year = 2025
""")
st.dataframe(df_charger_region)
