import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(layout="wide", page_title="현대차 전기차 분석")

# 데이터베이스 연결 엔진
engine = create_engine("mysql+mysqlconnector://car_insert:car1234@127.0.0.1:3306/car_insert")

# CSS 스타일 정의 (배너 및 카드 공통)
st.markdown("""
    <style>
    /* 전체 배경 및 텍스트 색상 */
    .main { background-color: #0e1117; }
    
    /* 메인 배너 스타일 */
    .main-banner { background-color: #2b57d1; padding: 35px 45px; border-radius: 15px; color: white; margin-bottom: 25px; }
    .banner-title { font-size: 36px; font-weight: 700; margin-bottom: 8px; }
    .banner-subtitle { font-size: 22px; opacity: 0.9; }

    /* 대시보드 메트릭 카드 스타일 */
    .metric-container {
        display: flex; justify-content: space-between; background-color: #1a1c24; padding: 20px; 
        border-radius: 15px; border: 1px solid #2d2e3a; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
        color: white; align-items: center;
    }
    .metric-label { font-size: 14px; color: #a0a0a0; margin-bottom: 10px; }
    .metric-value { font-size: 24px; font-weight: 700; color: #ffffff; }
    .metric-unit { font-size: 16px; font-weight: 400; color: #888; }
    .icon-style { font-size: 30px; margin-top: 10px; }

    /* FAQ 섹션 스타일 */
    .stExpander {
        background-color: #FFFFFF !important;
        border: 1px solid #2d2e3a !important;
        border-radius: 8px !important;
        margin-bottom: 10px !important;
    }

    # FAQ 질문 & 답변 폰트 조절
    .stExpander summary p {
        font-size: 50px !important; 
        font-weight: 600 !important;
        color: #333333 !important; 
    }

    .stExpander div[data-testid="stExpanderDetails"] p {
        font-size: 18px !important;  /* 답변 크기: 18px */
        color: #333333 !important;   /* 진한 회색 */
        line-height: 1.6 !important; /* 줄간격 확보 */
    }

    /* 버튼 스타일 조정 */
    div.stButton > button p {
        font-size: 20px !important;
        font-weight: 600 !important;
    }

    div.stButton > button {
        background-color: #ffffff; 
        color: #000000; 
        border: 1px solid #3e404b;
        width: 100%; 
        border-radius: 5px;
        padding: 10px 0px;        
        height: auto;             
        transition: all 0.2s;
    }

    div.stButton > button:hover {
        background-color: #f1f3f5;
        border-color: #002c5f;
        color: #002c5f;
    }

    </style>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 페이지 2: 자주 묻는 질문 (FAQ) 화면 구현
# ---------------------------------------------------------

# st.markdown('<div class="main-banner" style="background-color: #3f3da1;"><div class="banner-title">자주 묻는 질문 (FAQ)</div><div>현대차 전기차 관련 궁금증을 해결해드립니다</div></div>', unsafe_allow_html=True)
# 상단 배너 (글자 크기 클래스 적용)
st.markdown("""
        <div class="main-banner">
            <div class="banner-title">자주 묻는 질문 (FAQ)</div>
            <div class="banner-subtitle">현대차 전기차 관련 궁금증을 해결해드립니다</div>
        </div>
        """, unsafe_allow_html=True)


# 검색바
st.text_input("검색어", placeholder="🔍검색어를 입력하세요...", label_visibility="collapsed")
    
# 카테고리 버튼
btn_cols = st.columns(6)
categories = ["전체", "충전", "구매/보조금", "유지보수", "성능/사양", "기타"]
for i, cat in enumerate(categories):
    btn_cols[i].button(cat, use_container_width=True)

st.write("")

# FAQ 리스트 구현
faq_items = [
    {"cat": "충전", "q": "전기차 충전 시간은 얼마나 걸리나요?"},
    {"cat": "충전", "q": "집에서 충전이 가능한가요?"},
    {"cat": "구매/보조금", "q": "전기차 구매 시 보조금은 얼마나 받을 수 있나요?"},
    {"cat": "구매/보조금", "q": "보조금 신청은 어떻게 하나요?"},
    {"cat": "유지보수", "q": "전기차 유지비용은 어느 정도인가요?"},
    {"cat": "유지보수", "q": "배터리 수명은 얼마나 되나요?"},
]

for item in faq_items:
    with st.expander(f"[{item['cat']}] {item['q']}"):
        # 답변 내용 출력
        st.markdown(f"상세 답변 내용이 여기에 표시됩니다. {item['q']}\n 에 대한 현시점 기준 가장 정확한 정보를 안내드립니다.")