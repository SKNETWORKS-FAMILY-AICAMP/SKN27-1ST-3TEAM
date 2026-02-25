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
    .main { background-color: #1a1c2405; }
    
    /* 메인 배너 스타일 */
    .main-banner { background-color: #2b57d1; padding: 35px 45px; border-radius: 15px; color: white; margin-bottom: 25px; }
    .banner-title { font-size: 36px; font-weight: 700; margin-bottom: 8px; }
    .banner-subtitle { font-size: 22px; opacity: 0.9; }

    /* 대시보드 메트릭 카드 스타일 */
    .metric-container {
        display: flex; justify-content: space-between; background-color: #1a1c2400; padding: 20px; 
        border-radius: 15px; border: 1px solid #2d2e3a; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
        color: white; align-items: center;
    }

    .metric-label { font-size: 28px; color: #a0a0a0; margin-bottom: 10px; }
    .metric-value { font-size: 40px; font-weight: 700; color: #000000; }
    .metric-unit { font-size: 30px; font-weight: 400; color: #888; }
    .icon-style { font-size: 30px; margin-top: 10px; }

    /* FAQ 섹션 스타일 */
    .stExpander {
        background-color: #1a1c24;
        border: 1px solid #2d2e3a;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    
    /* 버튼 스타일 조정 */
    div.stButton > button {
        background-color: #1a1c24; color: white; border: 1px solid #3e404b;
        width: 100%; border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 페이지 1: 친환경차 분석 대시보드 화면 구현
# ---------------------------------------------------------
    # 상단 배너 (글자 크기 클래스 적용)
st.markdown("""
        <div class="main-banner">
            <div class="banner-title">친환경차 분석 대시보드</div>
            <div class="banner-subtitle">전국 자동차 등록 현황 및 환경 데이터 통합 분석</div>
        </div>
        """, unsafe_allow_html=True)

# 4개 위젯 생성
col1, col2, col3, col4 = st.columns(4)

with col1:
        st.markdown("""
            <div class="metric-container">
                <div>
                    <div class="metric-label">전국 전기차 등록</div>
                    <div class="metric-value">224.4 <span class="metric-unit">만 대</span></div>
                </div>
                <div style="font-size:30px;">🪫</div>
            </div>
        """, unsafe_allow_html=True)

with col2:
        st.markdown("""
            <div class="metric-container">
                <div>
                    <div class="metric-label">전국 수소차 등록</div>
                    <div class="metric-value">12.7 <span class="metric-unit">만 대</span></div>
                </div>
                <div style="font-size:30px;">🍃</div>
            </div>
        """, unsafe_allow_html=True)

with col3:
        st.markdown("""
            <div class="metric-container">
                <div>
                    <div class="metric-label">친환경차 비율</div>
                    <div class="metric-value">17.0 <span class="metric-unit">%</span></div>
                </div>
                <div style="font-size:30px;">🚙</div>
            </div>
        """, unsafe_allow_html=True)

with col4:
        # 2024년 고정 위젯
        st.markdown("""
            <div class="metric-container">
                <div>
                    <div class="metric-label">최신 데이터 연도</div>
                    <div class="metric-value">2,024 <span class="metric-unit">년</span></div>
                </div>
                <div style="font-size:30px;">📅</div>
            </div>
        """, unsafe_allow_html=True)

with st.container():
    st.markdown('<div style="background-color:white; padding:30px; border-radius:20px; solid #edf2f7;">', unsafe_allow_html=True)
    st.subheader("환경 지표 통합 분석")
    st.caption("평균기온, 친환경차 증가, CO2 배출량 추이")

    # 그래프
    try:
        # 데이터 불러오기
        df_ev = pd.read_sql("SELECT reg_year, ev_count FROM ev_registration", engine)
        df_h2 = pd.read_sql("SELECT reg_year, h2_count FROM hydrogen_yearly", engine)
        df_co2 = pd.read_sql("SELECT reg_year, emission FROM transport_co2", engine)

        # 데이터 타입 정수형으로 통일 및 병합
        for df in [df_ev, df_h2, df_co2]:
            df['reg_year'] = df['reg_year'].astype(int)

        df_final = pd.merge(df_ev, df_h2, on='reg_year', how='outer')
        df_final = pd.merge(df_final, df_co2, on='reg_year', how='outer').sort_values('reg_year')

        # Plotly 이중 Y축 그래프
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # 좌측 Y축: 차량 등록 수 (실선)
        fig.add_trace(
            go.Scatter(x=df_final['reg_year'], y=df_final['ev_count'], name="전기차(만 대)", 
                        line=dict(color='#2b57d1', width=3), mode='lines+markers'), 
            secondary_y=False
        )
        fig.add_trace(
            go.Scatter(x=df_final['reg_year'], y=df_final['h2_count'], name="수소차(만 대)", 
                        line=dict(color='#28a745', width=3), mode='lines+markers'), 
            secondary_y=False
        )

        # 우측 Y축: CO2 배출량
        fig.add_trace(
            go.Scatter(x=df_final['reg_year'], y=df_final['emission'], name="CO2 배출량", 
                        line=dict(color='#f97316', dash='dash'), mode='lines+markers'), 
            secondary_y=True
        )

        # 레이아웃 설정 (X축을 연도별로 또렷하게 표시)
        fig.update_layout(
            hovermode="x unified",
            template="plotly_dark",
            height=500,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(tickmode='linear', dtick=1, gridcolor='#2d2e3a'),
            yaxis=dict(gridcolor='#2d2e3a'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"그래프 생성 중 오류가 발생했습니다: {e}")

    st.markdown('</div>', unsafe_allow_html=True)
