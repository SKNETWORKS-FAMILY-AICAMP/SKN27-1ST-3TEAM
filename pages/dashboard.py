import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import common.db as db


# ── 데이터 로드 ────────────────────────────────────────────────────────────────
def car_data():
    df_ev    = db.fetch_data(db.queries["ev_main"])
    df_h2    = db.fetch_data(db.queries["h2_main"])
    df_total = db.fetch_data(db.queries["total_main"])
    if any(d is None for d in [df_ev, df_h2, df_total]):
        return None, None, None
    return df_ev, df_h2, df_total


def graph_data():
    df_co2_vkt  = db.fetch_data(db.queries["co2_vkt"])
    df_co2_fuel = db.fetch_data(db.queries["co2_fuel"])
    df_temp     = db.fetch_data(db.queries["temp"])
    df_demand   = db.fetch_data(db.queries["demand"])
    df_ev_count = db.fetch_data(db.queries["ev_count"])
    if any(d is None for d in [df_co2_vkt, df_co2_fuel, df_temp, df_demand, df_ev_count]):
        return None

    df = (df_co2_vkt.rename(columns={"연도": "reg_year", "총_CO2_VKT": "co2_vkt"})
          .merge(df_co2_fuel.rename(columns={"연도": "reg_year", "총_CO2_연료": "co2_fuel"}), on="reg_year")
          .merge(df_temp.rename(columns={"연도": "reg_year", "평균기온": "avg_temp"}), on="reg_year")
          .merge(df_demand.rename(columns={"연도": "reg_year", "전체_등록_대수": "total_v"}), on="reg_year")
          .merge(df_ev_count.rename(columns={"sum_count": "ev_count"}), on="reg_year", how="left")
          .sort_values("reg_year").reset_index(drop=True))

    # total_v: 대 단위 → 만대 변환
    df["total_v_man"] = df["total_v"] / 10000
    # EV 비율: ev_count(대) / total_v(대) * 100
    df["ev_pct"]      = df["ev_count"] / df["total_v"] * 100
    # 1만대당 CO₂: co2(천톤) / total_v_man(만대)
    df["eff_vkt"]     = df["co2_vkt"]  / df["total_v_man"]
    df["eff_fuel"]    = df["co2_fuel"] / df["total_v_man"]
    return df


df_ev, df_h2, df_total = car_data()
df = graph_data()


# ── 헤더 ───────────────────────────────────────────────────────────────────────
container = st.container(border=True)
container.header("한국 전기차 보급 × 탄소배출 × 기온\n실데이터 통합 분석")


# ── KPI 카드 ───────────────────────────────────────────────────────────────────
if df_ev is not None and df_h2 is not None and df_total is not None:
    total_ev      = df_ev["ev_count"].sum()
    total_h2      = df_h2["h2_count"].sum()
    total_vehicle = df_total["total_vehicle"].sum()
    ratio         = (total_ev + total_h2) / total_vehicle * 100
    ev_man        = int(total_ev / 10000)
    h2_man        = int(total_h2 / 10000)
else:
    st.error("KPI 데이터를 불러오지 못했습니다. DB 연결을 확인해주세요.")

if df is None:
    st.error("그래프 데이터를 불러오지 못했습니다. DB 연결을 확인해주세요.")
    st.stop()


# ══════════════════════════════════════════════════════════════════════════════
#  차트 1 — CO₂ VKT(선, fill) / 전체차량(막대) / 평균기온(선)
#  yCO2: left, min=90000, max=106000
#  yVeh: right, min=1900,  max=2800
#  yTemp: right, min=12.4, max=14.2
# ══════════════════════════════════════════════════════════════════════════════
st.subheader("①CO₂ 전국합 / 전체 차량 등록 / 연평균 기온 중첩 시계열")

fig1 = go.Figure()

# CO₂ VKT — 선 + fill (HTML: fill: true, tension: 0.4)
fig1.add_trace(go.Scatter(
    x=df["reg_year"], y=df["co2_vkt"],
    name="CO₂ VKT (천톤)",
    mode="lines+markers",
    fill="tozeroy",
    fillcolor="rgba(56,189,248,0.07)",
    line=dict(color="#38bdf8", width=2.5, shape="spline", smoothing=0.4),
    marker=dict(
        size=8,
        color=["#f87171" if v == df["co2_vkt"].max() else "#38bdf8" for v in df["co2_vkt"]]
    ),
    yaxis="y1",
    hovertemplate="CO₂(VKT): %{y:,.0f}천톤<extra></extra>"
))

# 전체차량 — 막대 (HTML: bar, backgroundColor rgba(167,139,250,.18))
fig1.add_trace(go.Bar(
    x=df["reg_year"], y=df["total_v_man"],
    name="전체 차량 (만대)",
    marker_color="rgba(167,139,250,0.18)",
    marker_line_color="rgba(167,139,250,0.5)", marker_line_width=1.5,
    yaxis="y2",
    hovertemplate="전체차량: %{y:.1f}만대<extra></extra>"
))

# 평균기온 — 선 (HTML: borderDash [6,3], no fill)
fig1.add_trace(go.Scatter(
    x=df["reg_year"], y=df["avg_temp"],
    name="연평균 기온 (℃)",
    mode="lines+markers",
    line=dict(color="#fb923c", width=2, dash="dot", shape="spline", smoothing=0.4),
    marker=dict(
        size=7,
        color=["#f87171" if v == df["avg_temp"].max() else "#fb923c" for v in df["avg_temp"]]
    ),
    yaxis="y3",
    hovertemplate="기온: %{y}℃<extra></extra>"
))

fig1.update_layout(
    title=dict(text="CO₂ 전국합 / 전체 차량 등록 / 연평균 기온 중첩 시계열",
               font=dict(size=18), x=0.5, xanchor="center"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
    xaxis=dict(title="연도", tickmode="linear", domain=[0.0, 0.75]),
    # 좌축 CO₂: min=90000, max=106000
    yaxis=dict(
        title=dict(text="CO₂ VKT (천톤)", font=dict(color="#38bdf8")),
        tickfont=dict(color="#38bdf8"),
        side="left",
        range=[90000, 106000],
        showgrid=True, gridcolor="rgba(0,0,0,0.06)",
        tickformat=","
    ),
    # 우축1 전체차량: min=1900, max=2800
    yaxis2=dict(
        title=dict(text="전체 차량 (만대)", font=dict(color="#a78bfa")),
        tickfont=dict(color="#a78bfa"),
        overlaying="y", side="right",
        anchor="free", position=0.77,
        range=[1900, 2800],
        showgrid=False,
        ticksuffix="만"
    ),
    # 우축2 기온: min=12.4, max=14.2
    yaxis3=dict(
        title=dict(text="기온 (℃)", font=dict(color="#fb923c")),
        tickfont=dict(color="#fb923c"),
        overlaying="y", side="right",
        anchor="free", position=0.90,
        range=[12.4, 14.2],
        showgrid=False,
        ticksuffix="℃"
    ),
    margin=dict(l=60, r=180, t=80, b=50),
    plot_bgcolor="white", hovermode="x unified", height=420
)
st.plotly_chart(fig1, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
#  차트 2 — 전기차(막대) / 전체차량(선) / EV%(선, fill)
#  yEV:  left
#  yVeh: right, min=1900, max=2800
#  yPct: right, min=0,    max=2.2
# ══════════════════════════════════════════════════════════════════════════════
st.subheader("② 전기차 등록대수 급성장 vs 전체 차량 · EV 비율(%)")

fig2 = go.Figure()

# 전기차 막대 (HTML: bar, 색상 단계별)
fig2.add_trace(go.Bar(
    x=df["reg_year"], y=df["ev_count"],
    name="전기차 등록대수 (대)",
    marker_color=[
        "rgba(52,211,153,0.85)" if i == len(df)-1
        else "rgba(52,211,153,0.65)" if v > 100000
        else "rgba(52,211,153,0.45)" if v > 10000
        else "rgba(52,211,153,0.30)"
        for i, v in enumerate(df["ev_count"])
    ],
    marker_line_color="#34d399", marker_line_width=1.5,
    yaxis="y1",
    hovertemplate="전기차: %{y:,.0f}대<extra></extra>"
))

# 전체차량 선 (HTML: line, tension 0.3, no fill)
fig2.add_trace(go.Scatter(
    x=df["reg_year"], y=df["total_v_man"],
    name="전체 차량 (만대)",
    mode="lines+markers",
    line=dict(color="#a78bfa", width=2.5, shape="spline", smoothing=0.3),
    marker=dict(size=6, color="#a78bfa"),
    yaxis="y2",
    hovertemplate="전체차량: %{y:.1f}만대<extra></extra>"
))

# EV 비율 선 (HTML: line + fill, borderDash [5,3])
fig2.add_trace(go.Scatter(
    x=df["reg_year"], y=df["ev_pct"],
    name="EV 비율 (%)",
    mode="lines+markers",
    fill="tozeroy",
    fillcolor="rgba(244,114,182,0.06)",
    line=dict(color="#f472b6", width=2.5, dash="dot", shape="spline", smoothing=0.4),
    marker=dict(
        size=7,
        color=["#f87171" if v >= 1.0 else "#f472b6" for v in df["ev_pct"]]
    ),
    yaxis="y3",
    hovertemplate="EV비율: %{y:.3f}%<extra></extra>"
))

fig2.update_layout(
    title=dict(text="전국 전기차 등록대수(막대) / 전체 차량(선) / EV 비율(선)",
               font=dict(size=18), x=0.5, xanchor="center"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
    xaxis=dict(title="연도", tickmode="linear", domain=[0.0, 0.75]),
    # 좌축 전기차
    yaxis=dict(
        title=dict(text="전기차 (대)", font=dict(color="#34d399")),
        tickfont=dict(color="#34d399"),
        side="left",
        showgrid=True, gridcolor="rgba(0,0,0,0.06)",
        tickformat=","
    ),
    # 우축1 전체차량: min=1900, max=2800
    yaxis2=dict(
        title=dict(text="전체 차량 (만대)", font=dict(color="#a78bfa")),
        tickfont=dict(color="#a78bfa"),
        overlaying="y", side="right",
        anchor="free", position=0.77,
        range=[1900, 2800],
        showgrid=False,
        ticksuffix="만"
    ),
    # 우축2 EV%: min=0, max=2.2
    yaxis3=dict(
        title=dict(text="EV 비율 (%)", font=dict(color="#f472b6")),
        tickfont=dict(color="#f472b6"),
        overlaying="y", side="right",
        anchor="free", position=0.90,
        range=[0, 2.2],
        showgrid=False,
        ticksuffix="%"
    ),
    margin=dict(l=60, r=180, t=80, b=50),
    plot_bgcolor="white", hovermode="x unified", height=400
)
st.plotly_chart(fig2, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
#  차트 3 — 1만대당 CO₂ (VKT 선+fill / 연료 선점선)
#  y: min=36, max=47
# ══════════════════════════════════════════════════════════════════════════════
st.subheader("③ 차량 1만대당 CO₂ 배출 효율 변화")

fig3 = go.Figure()

# VKT 기준 — 선 + fill (HTML: fill: true)
fig3.add_trace(go.Scatter(
    x=df["reg_year"], y=df["eff_vkt"],
    name="1만대당 CO₂ (VKT 기준)",
    mode="lines+markers",
    fill="tozeroy",
    fillcolor="rgba(251,191,36,0.07)",
    line=dict(color="#fbbf24", width=3, shape="spline", smoothing=0.4),
    marker=dict(
        size=[10 if i == df["eff_vkt"].idxmax() else 6 for i in range(len(df))],
        color=[
            "#f87171" if i == df["eff_vkt"].idxmax()
            else "#34d399" if i == len(df)-1
            else "#fbbf24"
            for i in range(len(df))
        ]
    ),
    hovertemplate="VKT: %{y:.2f}톤/만대<extra></extra>"
))

# 연료 기준 — 점선, no fill (HTML: borderDash [6,3], fill: false)
fig3.add_trace(go.Scatter(
    x=df["reg_year"], y=df["eff_fuel"],
    name="1만대당 CO₂ (연료 기준)",
    mode="lines+markers",
    line=dict(color="#38bdf8", width=2, dash="dot", shape="spline", smoothing=0.4),
    marker=dict(size=6, color="#38bdf8"),
    hovertemplate="연료: %{y:.2f}톤/만대<extra></extra>"
))

fig3.update_layout(
    title=dict(text="차량 1만대당 CO₂ — VKT 기준 vs 연료 기준 (2015~)",
               font=dict(size=18), x=0.5, xanchor="center"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
    xaxis=dict(title="연도", tickmode="linear"),
    yaxis=dict(
        title="톤CO₂eq / 만대",
        range=[36, 47],
        showgrid=True, gridcolor="rgba(0,0,0,0.06)",
        ticksuffix="톤"
    ),
    margin=dict(l=60, r=40, t=80, b=50),
    plot_bgcolor="white", hovermode="x unified", height=380
)
st.plotly_chart(fig3, use_container_width=True)


# ── 원본 수치 테이블 ───────────────────────────────────────────────────────────
with st.expander("연도별 원본 수치 보기"):
    tbl = df[["reg_year", "co2_vkt", "co2_fuel", "total_v_man", "avg_temp", "ev_count", "ev_pct", "eff_vkt", "eff_fuel"]].copy()
    tbl.columns = ["연도", "CO₂ VKT(천톤)", "CO₂ 연료(천톤)", "전체차량(만대)", "평균기온(℃)", "전기차(대)", "EV비율(%)", "효율 VKT(톤/만대)", "효율 연료(톤/만대)"]
    tbl = tbl.set_index("연도")
    st.dataframe(
        tbl.style
            .format({
                "CO₂ VKT(천톤)":    "{:,.1f}",
                "CO₂ 연료(천톤)":   "{:,.1f}",
                "전체차량(만대)":    "{:.1f}",
                "평균기온(℃)":      "{:.2f}",
                "전기차(대)":        "{:,.0f}",
                "EV비율(%)":         "{:.3f}",
                "효율 VKT(톤/만대)": "{:.2f}",
                "효율 연료(톤/만대)":"{:.2f}",
            })
            .highlight_max(subset=["CO₂ VKT(천톤)", "효율 VKT(톤/만대)"], color="#ffe4e4")
            .highlight_min(subset=["CO₂ VKT(천톤)", "효율 VKT(톤/만대)"], color="#d4f7ec"),
        use_container_width=True
    )