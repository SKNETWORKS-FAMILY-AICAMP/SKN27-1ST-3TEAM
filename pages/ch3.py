import streamlit as st
import sys
sys.path.append('..')
from db import query

st.title("🗺️ Ch.3 - 지금 어디까지 왔나")

# 1. 시도별 전기차 현황 (2024년)
st.subheader("📌 시도별 전기차 등록대수 (2024년)")
df_ev_region = query("""
    SELECT r.region_name, e.ev_count
    FROM ev_registration e
    JOIN region r ON e.region_id = r.region_id
    WHERE e.reg_year = 2024
    ORDER BY e.ev_count DESC
""")
st.dataframe(df_ev_region)
st.bar_chart(df_ev_region.set_index('region_name')['ev_count'])

# 2. 시도별 수소차 현황
st.subheader("📌 시도별 수소차 등록대수 (2025-12)")
df_h2_region = query("""
    SELECT r.region_name, h.h2_count
    FROM hydrogen_regional h
    JOIN region r ON h.region_id = r.region_id
    ORDER BY h.h2_count DESC
""")
st.dataframe(df_h2_region)
st.bar_chart(df_h2_region.set_index('region_name')['h2_count'])

# 3. 인구 대비 전기차 비율
st.subheader("📌 인구 대비 전기차 비율 (2024년, 인구 1만명당)")
df_per_pop = query("""
    SELECT r.region_name,
           e.ev_count,
           p.population,
           ROUND(e.ev_count / p.population * 10000, 1) AS ev_per_10k
    FROM ev_registration e
    JOIN region r ON e.region_id = r.region_id
    JOIN population p ON e.region_id = p.region_id
    WHERE e.reg_year = 2024
    ORDER BY ev_per_10k DESC
""")
st.dataframe(df_per_pop)
st.bar_chart(df_per_pop.set_index('region_name')['ev_per_10k'])

# 4. 지자체별 전기차 보조금 (승용 기준 상위 10개)
st.subheader("📌 지자체별 전기차 승용 보조금 상위 10개 (만원)")
df_subsidy = query("""
    SELECT r.region_name, s.local_gov_name, s.ev_sedan_amt
    FROM subsidy s
    JOIN region r ON s.region_id = r.region_id
    ORDER BY s.ev_sedan_amt DESC
    LIMIT 10
""")
st.dataframe(df_subsidy)
