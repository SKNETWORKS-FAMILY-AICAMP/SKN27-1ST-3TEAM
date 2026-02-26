import streamlit as st
#from common.crawl import crawl_faq
from common.db2 import DB



pages = {
    "현대 친환경차 등록 현황 및 FAQ 조회": [
        st.Page("pages/dashboard.py", title="친환경 차 분석 대시보드"),
        st.Page("pages/infra_subsidy.py", title="인프라 격차 & 보조금 정책 분석"),
        st.Page("pages/4_FAQ.py", title="FAQ")
    ]
}

pg = st.navigation(pages)
pg.run()