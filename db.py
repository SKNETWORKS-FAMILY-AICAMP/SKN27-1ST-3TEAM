import pymysql
import pandas as pd
import streamlit as st

@st.cache_resource
def get_connection():
    try:
        return pymysql.connect(
            host="localhost", 
            user="root", 
            password="root1234",
            port=3307,              #로컬 테스트용 임시포트 (나중에 변경)
            charset="utf8mb4", 
            database="car_insert" 
        )
    except Exception as e:
        st.error(f"DB 연결 실패: {e}")
        return None

# 공통 쿼리 실행 함수
def fetch_data(query):
    conn = get_connection()
    if conn is None: return None
    try:
        return pd.read_sql(query, conn)
    except Exception as e:
        st.error(f"데이터 쿼리 오류: {e}")
        return None

# 딕셔너리에 쿼리 모음
queries = {   
    ### 대시보드 페이지 쿼리 ###
    #최신연도 전국 전기차 등록대수
    "ev_main": """SELECT ev_count FROM ev_registration 
                    WHERE reg_year = (SELECT MAX(reg_year) FROM ev_registration)""", 
    #최신연도 전국 수소차 등록대수
    "h2_main": """SELECT h2_count FROM hydrogen_regional 
                    WHERE base_ym = (SELECT MAX(base_ym) FROM hydrogen_regional)""", 
    #최신연도 전체 차량 등록대수
    "total_main": """SELECT total_vehicle FROM total_vehicle_yearly 
                    WHERE reg_year = (SELECT MAX(reg_year) FROM total_vehicle_yearly)""", 
    #연도별 총 CO2 배출량
    "co2": """
        SELECT reg_year AS 연도, SUM(emission) AS 총_CO2_배출량 
        FROM transport_co2 
        GROUP BY reg_year 
        ORDER BY reg_year DESC
    """,
    #연도별 평균기온
    "temp": """
        SELECT reg_year AS 연도, avg_temp AS 평균기온 
        FROM temperature_yearly 
        ORDER BY reg_year DESC
    """,
    #연도별 전체 차량 등록대수
    "demand": """
        SELECT reg_year AS 연도, total_vehicle AS 전체_등록_대수 
        FROM total_vehicle_yearly 
        ORDER BY reg_year DESC
    """,
    # 전기차 등록대수 (최신 연도)
    "ev_latest": """
        SELECT ev_count FROM ev_registration 
        WHERE reg_year = (SELECT MAX(reg_year) FROM ev_registration)
    """,
    # 수소차 등록대수 (최신 연도)
    "h2_latest": """
        SELECT h2_count FROM hydrogen_regional 
        WHERE base_ym = (SELECT MAX(base_ym) FROM hydrogen_regional)
    """,
    # 충전기 설치 대수 (최신 연도)
    "charger_latest": """
        SELECT total_cnt FROM charger_yearly 
        WHERE reg_year = (SELECT MAX(reg_year) FROM charger_yearly)
    """,



    ### 인프라 분석 페이지 쿼리 ###
    # 시도별 전기차 데이터
    "ev_regional": """
        SELECT r.region_id, r.region_name as '지역', e.ev_count as '전기차' 
        FROM region r
        JOIN ev_registration e ON r.region_id = e.region_id
        WHERE e.reg_year = 2024
        ORDER BY r.region_id
    """,
    # 충전기 데이터 (매핑)
    "charger_raw": "SELECT * FROM charger_yearly WHERE reg_year = 2024 LIMIT 1"
    
}