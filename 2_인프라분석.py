import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from db import get_connection

conn = get_connection()

# 차량 데이터
def get_data():
    if conn is None: 
        return None, None, None
    try:
        with conn.cursor() as cursor:
            # 전기차 등록대수 (최신 연도)
            query_ev = """
                SELECT ev_count FROM ev_registration 
                WHERE reg_year = (SELECT MAX(reg_year) FROM ev_registration)
            """
            # 수소차 등록대수 (최신 연도)
            query_h2 = """
                SELECT h2_count FROM hydrogen_regional 
                WHERE base_ym = (SELECT MAX(base_ym) FROM hydrogen_regional)
            """
            # 총 충전기 수 (최신 연도)
            query_total = """
                SELECT total_cnt FROM charger_yearly 
                WHERE reg_year = (SELECT MAX(reg_year) FROM charger_yearly)
            """
            
            df_evcount = pd.read_sql(query_ev, conn)
            df_h2count = pd.read_sql(query_h2, conn)
            df_totalcount = pd.read_sql(query_total, conn)
            
            return df_evcount, df_h2count, df_totalcount
    except Exception as e:
        st.error(f"데이터 로드 중 오류: {e}")
        return None, None, None

df_evcount, df_h2count, df_totalcount = get_data()

# 그래프 데이터 함수
def graph_data():
    if conn is None: return None
    try:
        with conn.cursor() as cursor:
            # 시도별 전기차 데이터
            query_ev = """  
                SELECT r.region_id, r.region_name as '지역', e.ev_count as '전기차' 
                FROM region r
                JOIN ev_registration e ON r.region_id = e.region_id
                WHERE e.reg_year = 2024
                ORDER BY r.region_id
            """
            df_ev = pd.read_sql(query_ev, conn)

            # 충전기 데이터
            query_charger = "SELECT * FROM charger_yearly WHERE reg_year = 2024 LIMIT 1"
            df_charger_raw = pd.read_sql(query_charger, conn)
            
            if df_charger_raw.empty: return None
            row = df_charger_raw.iloc[0]

            # 시도별 딕셔너리에 담아서 매핑
            mapping_data = {
                '서울': row['seoul_cnt'], '경기': row['gyeonggi_cnt'], '인천': row['incheon_cnt'],
                '강원': row['gangwon_cnt'], '제주': row['jeju_cnt'],
                '대전': row['chungcheong_cnt'], '세종': row['chungcheong_cnt'], 
                '충북': row['chungcheong_cnt'], '충남': row['chungcheong_cnt'],
                '광주': row['jeolla_cnt'], '전북': row['jeolla_cnt'], '전남': row['jeolla_cnt'],
                '부산': row['gyeongsang_cnt'], '대구': row['gyeongsang_cnt'], 
                '울산': row['gyeongsang_cnt'], '경북': row['gyeongsang_cnt'], '경남': row['gyeongsang_cnt']
            }
            
            df_ev['충전기'] = df_ev['지역'].map(mapping_data).fillna(0) # 데이터 없는 지역은 0으로 수치 표시
            df_ev['전기차당 충전기'] = (df_ev['충전기'] / df_ev['전기차']).round(2)
            
            return df_ev.head(10) # 10개 지역만 추출

    except Exception as e:
        st.error(f"그래프 데이터 로드 중 오류: {e}")
        return None

df = graph_data()


## 화면 부분
container = st.container(border=True, height=140)
container.header("📊 인프라 격차 분석")
container.text("지역별 충전 인프라 및 친환경차 현황 비교")

if all(df is not None for df in [df_evcount, df_h2count, df_totalcount]):
    total_ev = df_evcount['ev_count'].sum()          # 전기차 총 대수
    total_h2 = df_h2count['h2_count'].sum()          # 수소차 총 대수
    total_charger = df_totalcount['total_cnt'].sum() # 충전기 총 대수
    
    # '만 대' 단위로 변환
    ev_man = int(total_ev / 10000) 
    h2_man = int(total_h2 / 10000)

    charger_man = int(total_charger / 10000) # 총 충전기 수
    ev_charger = round(total_charger / total_ev, 2) if total_ev > 0 else 0 # 전기 차량별 충전기
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("전국 전기차 등록", f"{ev_man}만 대", border=True)
    col2.metric("수소차 등록 대수", f"{h2_man}만 대", border=True)
    col3.metric("총 충전기 수", f"{charger_man}만 대", border=True)
    col4.metric("전기차량 충전기", f"{ev_charger}기/대", border=True)


# 그래프와 표
if df is not None:
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df["지역"], y=df["전기차"], name="전기차", 
        yaxis="y1", marker_color='skyblue', offsetgroup=1
    ))

    fig.add_trace(go.Bar(
        x=df["지역"], y=df["충전기"], name="충전기", 
        yaxis="y2", marker_color='orange', offsetgroup=2
    ))

    fig.update_layout(
        title="전기차와 충전기 수요량 (지역별 비교)",
        xaxis=dict(title="지역"),
        yaxis=dict(title="전기차 수 (대)", side="left", showgrid=True),
        yaxis2=dict(title="충전기 수 (대)", side="right", overlaying="y", anchor="x", showgrid=False),
        barmode="group",
        legend=dict(x=1.1, y=1),
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df[['지역', '전기차', '충전기', '전기차당 충전기']], use_container_width=True)




