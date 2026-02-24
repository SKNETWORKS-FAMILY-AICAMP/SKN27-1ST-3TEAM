import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

st.set_page_config(layout="wide", page_title="현대차 전기차 분석")

# 데이터베이스 연결 엔진
engine = create_engine("mysql+mysqlconnector://car_insert:car1234@127.0.0.1:3306/car_insert")

# 세션 상태 초기화 (오류 방지)
if 'selected_card' not in st.session_state:
    st.session_state['selected_card'] = "전체"

# CSS 스타일 정의 (배너 및 카드 공통)
st.markdown("""
    <style>
    /* 배너 스타일 */
    .main-banner {
        background-color: #2b57d1;
        padding: 35px 45px;
        border-radius: 15px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .banner-title {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .banner-subtitle {
        font-size: 18px;
        opacity: 0.9;
    }

    /* 지표 카드 컨테이너 스타일 */
    .metric-container {
        display: flex;
        justify-content: space-between;
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #eef0f5;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
    }
    .metric-label {
        font-size: 14px;
        color: #666;
        font-weight: 500;
    }
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #1a1a1a;
        margin: 5px 0;
    }
    .metric-unit {
        font-size: 16px;
        color: #1a1a1a; /* '만 대', '%' 등 단위도 검정색으로 */
        font-weight: 400;
    }
    .metric-delta {
        font-size: 13px;
        color: #28a745;
        display: flex;
        align-items: center;
    }
    .icon-box {
        width: 45px;
        height: 45px;
        border-radius: 10px;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 배너 출력
st.markdown("""
    <div class="main-banner">
        <div class="banner-title">친환경차 분석 대시보드</div>
        <div class="banner-subtitle">전국 자동차 등록 현황 및 환경 데이터 통합 분석</div>
    </div>
    """, unsafe_allow_html=True)

# 4개 위젯 생성
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="metric-container"><div><div style="font-size:14px;color:#666;">전국 전기차 등록</div><div style="font-size:28px;font-weight:700;">224.4 <span style="font-size:16px;">만 대</span></div><div style="color:#28a745;">📈 +12.3%</div></div><div style="font-size:30px;">🚗</div></div>', unsafe_allow_html=True)
    if st.button("전기차 상세 데이터 보기", key="ev"):
        st.session_state['selected_card'] = "전기차"

with col2:
    st.markdown('<div class="metric-container"><div><div style="font-size:14px;color:#666;">전국 수소차 등록</div><div style="font-size:28px;font-weight:700;">12.7 <span style="font-size:16px;">만 대</span></div><div style="color:#28a745;">📈 +8.7%</div></div><div style="font-size:30px;">🍃</div></div>', unsafe_allow_html=True)
    if st.button("수소차 상세 데이터 보기", key="h2"):
        st.session_state['selected_card'] = "수소차"

with col3:
    st.markdown('<div class="metric-container"><div><div style="font-size:14px;color:#666;">CO2 배출 현황</div><div style="font-size:28px;font-weight:700;">17.0 <span style="font-size:16px;">%</span></div><div style="color:#6366f1;">⏱ transport_co2</div></div><div style="font-size:30px;">🚀</div></div>', unsafe_allow_html=True)
    if st.button("탄소 배출 분석 보기", key="ratio"):
        st.session_state['selected_card'] = "CO2 배출 현황"

with col4:
    st.markdown('<div class="metric-container"><div><div style="font-size:14px;color:#666;">전체 테이블 현황</div><div style="font-size:28px;font-weight:700;">11 <span style="font-size:16px;">개</span></div><div style="color:#f97316;">🔔 실시간</div></div><div style="font-size:30px;">📈</div></div>', unsafe_allow_html=True)
    if st.button("DB 테이블 전체 보기", key="year"):
        st.session_state['selected_card'] = "전체현황"

st.divider()

# 5. 클릭 결과에 따른 하단 변화 (데이터 없이 반응 확인)
st.subheader(f"🔍 {st.session_state['selected_card']} 상세 분석 영역")


try:
    if st.session_state['selected_card'] == "전기차":
        # 1. 쿼리 실행: 연도(base_year)와 등록대수(count)를 가져와서 연도순 정렬
        query = "SELECT base_year, count FROM ev_registration ORDER BY base_year ASC"
        df = pd.read_sql(query, engine)
        
        if not df.empty:
            st.info("🚗 연도별 전기차 등록 현황 추이")
            chart_data = df.set_index('base_year')
            st.line_chart(chart_data, color="#2b57d1")

            with st.expander("상세 데이터 표 확인"):
                st.dataframe(df, use_container_width=True)
        else:
            st.warning("테이블에 데이터가 존재하지 않습니다.")
            
    elif st.session_state['selected_card'] == "수소차":
        # 수소차도 전기차와 같은 방식으로 연도별 그래프를 그린다면 아래처럼 수정 가능합니다.
        query_h2 = "SELECT base_year, count FROM hydrogen_yearly ORDER BY base_year ASC"
        df_h2 = pd.read_sql(query_h2, engine)
        
        st.success("🍃 연도별 수소차 등록 현황 (막대 그래프)")
        chart_data_h2 = df_h2.set_index('base_year')
        st.bar_chart(chart_data_h2, color="#28a745") # 수소차는 초록색 포인트

    elif st.session_state['selected_card'] == "CO2 배출 현황":
        df_co2 = pd.read_sql("SELECT * FROM transport_co2", engine)
        st.write(df_co2)

    elif st.session_state['selected_card'] == "전체현황":
        union_query = """
        SELECT 'region' as 테이블, count(*) as 행수 FROM region UNION ALL
        SELECT 'ev_registration' , count(*) FROM ev_registration UNION ALL
        SELECT 'hydrogen_yearly' , count(*) FROM hydrogen_yearly UNION ALL
        SELECT 'transport_co2' , count(*) FROM transport_co2
        """
        df_all = pd.read_sql(union_query, engine)
        st.table(df_all)

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.info("DBeaver에서 테이블명과 컬럼명이 일치하는지 다시 한번 확인해주세요.")