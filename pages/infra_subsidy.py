import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import common.db as db


# ── 데이터 로드 (한번에) ───────────────────────────────────────────────────────
def load_data():
    df_ev_cnt    = db.fetch_data(db.queries["ev_latest"])
    df_h2_cnt    = db.fetch_data(db.queries["h2_latest"])
    df_charger   = db.fetch_data(db.queries["charger_latest"])
    df_ev_region = db.fetch_data(db.queries["ev_regional"])
    df_charger_r = db.fetch_data(db.queries["charger_raw"])
    df_subsidy   = db.fetch_data(db.queries["subsidy_all"])
    df_ev_reg    = db.fetch_data(db.queries["ev_reg_all"])
    return df_ev_cnt, df_h2_cnt, df_charger, df_ev_region, df_charger_r, df_subsidy, df_ev_reg

df_ev_cnt, df_h2_cnt, df_charger, df_ev_region, df_charger_r, df_subsidy, df_ev_reg = load_data()


# ── 인프라 차트 데이터 가공 ────────────────────────────────────────────────────
def build_infra_df():
    if df_ev_region is None or df_charger_r is None or df_charger_r.empty:
        return None
    try:
        row = df_charger_r.iloc[0]
        mapping = {
            '서울': row['seoul_cnt'],    '경기': row['gyeonggi_cnt'], '인천': row['incheon_cnt'],
            '강원': row['gangwon_cnt'],  '제주': row['jeju_cnt'],
            '대전': row['chungcheong_cnt'], '세종': row['chungcheong_cnt'],
            '충북': row['chungcheong_cnt'], '충남': row['chungcheong_cnt'],
            '광주': row['jeolla_cnt'],   '전북': row['jeolla_cnt'],   '전남': row['jeolla_cnt'],
            '부산': row['gyeongsang_cnt'], '대구': row['gyeongsang_cnt'],
            '울산': row['gyeongsang_cnt'], '경북': row['gyeongsang_cnt'], '경남': row['gyeongsang_cnt']
        }
        df = df_ev_region.copy()
        df['충전기'] = df['지역'].map(mapping).fillna(0)
        df['전기차당 충전기'] = (df['충전기'] / df['전기차']).replace([float('inf'), -float('inf')], 0).round(2)
        return df.head(10)
    except Exception as e:
        st.error(f"인프라 데이터 가공 오류: {e}")
        return None


# ── 보조금 데이터 가공 ─────────────────────────────────────────────────────────
def build_subsidy_df():
    if df_subsidy is None or df_ev_reg is None:
        return None, None, None
    sub  = df_subsidy.head(8)
    evreg = df_ev_reg.head(8)
    sum_ev = (sub["ev_sedan_amt"] + sub["ev_small_amt"] + sub["ev_mid_amt"] + sub["ev_large_amt"])
    sum_h2 = sub["h2_sedan_amt"] + sub["h2_van_amt"]
    df_1 = pd.DataFrame({
        "지역":       sub["local_gov_name"],
        "전기차 보조금": sum_ev,
        "수소차 보조금": sum_h2,
    })
    df_2 = pd.DataFrame({
        "지역":       sub["local_gov_name"],
        "전체 보조금": sum_ev + sum_h2
    })
    return df_1, df_2, evreg["ev_count"]


df_infra   = build_infra_df()
df_sub1, df_sub2, ev_reg_count = build_subsidy_df()


# ══════════════════════════════════════════════════════════════════════════════
#  인프라 격차 분석
# ══════════════════════════════════════════════════════════════════════════════
container = st.container(border=True, height=140)
container.header("📊 인프라 격차 분석")
container.text("지역별 충전 인프라 및 친환경차 현황 비교")

if all(d is not None for d in [df_ev_cnt, df_h2_cnt, df_charger]):
    total_ev      = df_ev_cnt['ev_count'].sum()
    total_h2      = df_h2_cnt['h2_count'].sum()
    total_charger = df_charger['total_cnt'].sum()
    ev_man        = int(total_ev / 10000)
    h2_man        = int(total_h2 / 10000)
    charger_man   = int(total_charger / 10000)
    ev_charger    = round(total_charger / total_ev, 2) if total_ev > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("전국 전기차 등록",  f"{ev_man}만 대",      border=True)
    col2.metric("수소차 등록 대수",  f"{h2_man}만 대",      border=True)
    col3.metric("총 충전기 수",      f"{charger_man}만 대", border=True)
    col4.metric("전기차량 충전기",   f"{ev_charger}기/대",  border=True)

if df_infra is not None:
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(
        x=df_infra["지역"], y=df_infra["전기차"],
        name="전기차", yaxis="y1", marker_color='skyblue', offsetgroup=1
    ))
    fig1.add_trace(go.Bar(
        x=df_infra["지역"], y=df_infra["충전기"],
        name="충전기", yaxis="y2", marker_color='orange', offsetgroup=2
    ))
    fig1.update_layout(
        title="전기차와 충전기 수요량 (지역별 비교)",
        xaxis=dict(title="지역"),
        yaxis=dict(title="전기차 수 (대)", side="left", showgrid=True),
        yaxis2=dict(title="충전기 수 (대)", side="right", overlaying="y", anchor="x", showgrid=False),
        barmode="group",
        legend=dict(x=1.1, y=1),
        hovermode="x unified"
    )
    st.plotly_chart(fig1, use_container_width=True)
    st.dataframe(df_infra[['지역', '전기차', '충전기', '전기차당 충전기']], use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
#  보조금 정책 분석
# ══════════════════════════════════════════════════════════════════════════════
container2 = st.container(border=True, height=140)
container2.header("💸 보조금 정책 분석")
container2.text("지역별 보조금 지원 현황 및 정책 효과 분석")

if df_sub1 is not None:
    sum_ev_avg = int(df_sub1["전기차 보조금"].mean())
    sum_h2_avg = int(df_sub1["수소차 보조금"].mean())

    col1, col2, col3 = st.columns(3)
    col1.metric("💵 평균 전기차 보조금", f"{sum_ev_avg} 만원", border=True)
    col2.metric("💵 평균 수소차 보조금", f"{sum_h2_avg} 만원", border=True)
    col3.metric("🌉 최고 보조금 지역", df_sub2.loc[df_sub2["전체 보조금"].idxmax(), "지역"], border=True)

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=df_sub1["지역"], y=df_sub1["전기차 보조금"], name="전기차 보조금", yaxis="y1", opacity=0.7))
    fig2.add_trace(go.Bar(x=df_sub1["지역"], y=df_sub1["수소차 보조금"], name="수소차 보조금", yaxis="y1", opacity=0.7))
    fig2.add_trace(go.Scatter(x=df_sub1["지역"], y=ev_reg_count, name="전기차 수요(등록수)", mode="lines+markers", yaxis="y2"))
    fig2.update_layout(
        title="지역별 보조금 및 전기차 등록 현황",
        xaxis=dict(title="지역"),
        yaxis=dict(title="보조금(만원)", side="left"),
        yaxis2=dict(title="전기차 등록수", overlaying='y', side="right"),
        barmode="group"
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.dataframe(df_sub1[["지역", "전기차 보조금", "수소차 보조금"]], use_container_width=True)
else:
    st.error("데이터를 불러오는 데 실패했습니다.")