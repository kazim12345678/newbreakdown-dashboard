# ===============================================================
# ENTERPRISE MANAGEMENT DOWNTIME DASHBOARD
# January – February 2026
# Covers 12 KPIs + MTTR + MTBF + Availability + Advanced Graphs
# ===============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.title("📊 Executive Downtime & Reliability Dashboard")
st.markdown("### Operational Performance Review – Jan & Feb 2026")
st.markdown("---")

# ===============================================================
# LOAD DATA
# ===============================================================

df = pd.read_csv("data/cleaned_downtime_data.csv")
df["Date_Clean"] = pd.to_datetime(df["Date_Clean"])

# ===============================================================
# BASIC CALCULATIONS
# ===============================================================

TOTAL_DAYS = df["Date_Clean"].nunique()
TOTAL_MACHINES = df["Machine"].nunique()
TOTAL_DOWNTIME = df["Consumed_Hours"].sum()

DAILY_DOWNTIME = df.groupby("Date_Clean")["Consumed_Hours"].sum().reset_index()
MACHINE_DOWNTIME = df.groupby("Machine")["Consumed_Hours"].sum().reset_index()

AVERAGE_DAILY_DOWNTIME = TOTAL_DOWNTIME / TOTAL_DAYS

AVAILABLE_HOURS = TOTAL_DAYS * 24 * TOTAL_MACHINES
AVAILABILITY_PERCENT = (1 - (TOTAL_DOWNTIME / AVAILABLE_HOURS)) * 100

ZERO_DOWNTIME_DAYS = DAILY_DOWNTIME[DAILY_DOWNTIME["Consumed_Hours"] == 0].shape[0]
PEAK_DAY = DAILY_DOWNTIME.loc[DAILY_DOWNTIME["Consumed_Hours"].idxmax()]
DOWNTIME_STD = DAILY_DOWNTIME["Consumed_Hours"].std()

# ===============================================================
# MTTR & MTBF
# ===============================================================

FAILURE_COUNT = df.shape[0]
MTTR = TOTAL_DOWNTIME / FAILURE_COUNT
TOTAL_OPERATING_TIME = AVAILABLE_HOURS - TOTAL_DOWNTIME
MTBF = TOTAL_OPERATING_TIME / FAILURE_COUNT

# ===============================================================
# MACHINE CONTRIBUTION %
# ===============================================================

MACHINE_DOWNTIME["Contribution_%"] = (
    MACHINE_DOWNTIME["Consumed_Hours"] / TOTAL_DOWNTIME
) * 100

TOP5 = MACHINE_DOWNTIME.sort_values(
    by="Consumed_Hours", ascending=False
).head(5)

# ===============================================================
# EXECUTIVE KPI CARDS
# ===============================================================

st.subheader("🔎 Executive KPI Overview")

row1 = st.columns(4)
row1[0].metric("Total Downtime (hrs)", round(TOTAL_DOWNTIME, 2))
row1[1].metric("Avg Daily Downtime (hrs)", round(AVERAGE_DAILY_DOWNTIME, 2))
row1[2].metric("Availability (%)", round(AVAILABILITY_PERCENT, 2))
row1[3].metric("Zero Downtime Days", ZERO_DOWNTIME_DAYS)

row2 = st.columns(4)
row2[0].metric("Peak Downtime Day", PEAK_DAY["Date_Clean"].date())
row2[1].metric("Peak Downtime (hrs)", round(PEAK_DAY["Consumed_Hours"], 2))
row2[2].metric("MTTR (hrs)", round(MTTR, 2))
row2[3].metric("MTBF (hrs)", round(MTBF, 2))

st.markdown("---")

# ===============================================================
# KPI 1 – Daily Downtime Trend
# ===============================================================

st.subheader("📈 Daily Downtime Trend")

fig_trend = px.line(
    DAILY_DOWNTIME,
    x="Date_Clean",
    y="Consumed_Hours",
    markers=True,
    template="plotly_white"
)
fig_trend.update_traces(line=dict(width=4))
st.plotly_chart(fig_trend, use_container_width=True)

# ===============================================================
# KPI 2 – Machine-wise Downtime
# ===============================================================

st.subheader("🏭 Machine-wise Total Downtime")

fig_machine = px.bar(
    MACHINE_DOWNTIME.sort_values(by="Consumed_Hours", ascending=False),
    x="Machine",
    y="Consumed_Hours",
    template="plotly_white",
    text_auto=True
)
st.plotly_chart(fig_machine, use_container_width=True)

# ===============================================================
# KPI 3 – Contribution %
# ===============================================================

st.subheader("📊 Machine Contribution %")

fig_pie = px.pie(
    MACHINE_DOWNTIME,
    names="Machine",
    values="Consumed_Hours",
    hole=0.5
)
st.plotly_chart(fig_pie, use_container_width=True)

# ===============================================================
# KPI 4 – Top 5 Critical Machines
# ===============================================================

st.subheader("🚨 Top 5 Critical Machines")

fig_top5 = px.bar(
    TOP5,
    x="Machine",
    y="Consumed_Hours",
    color="Consumed_Hours",
    template="plotly_white",
    text_auto=True
)
st.plotly_chart(fig_top5, use_container_width=True)

# ===============================================================
# KPI 5 – Downtime Variability
# ===============================================================

st.subheader("📉 Downtime Stability Analysis")

fig_box = px.box(
    DAILY_DOWNTIME,
    y="Consumed_Hours",
    template="plotly_white"
)
st.plotly_chart(fig_box, use_container_width=True)

# ===============================================================
# KPI 6 – Heatmap (Date vs Machine)
# ===============================================================

st.subheader("🔥 Downtime Heatmap")

pivot = df.pivot_table(
    index="Date_Clean",
    columns="Machine",
    values="Consumed_Hours",
    aggfunc="sum",
    fill_value=0
)

fig_heat = px.imshow(
    pivot,
    aspect="auto",
    color_continuous_scale="Reds"
)
st.plotly_chart(fig_heat, use_container_width=True)

# ===============================================================
# KPI 7 – Availability Gauge
# ===============================================================

st.subheader("⚙ Plant Availability")

fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=AVAILABILITY_PERCENT,
    gauge={'axis': {'range': [0, 100]}}
))
st.plotly_chart(fig_gauge, use_container_width=True)

# ===============================================================
# KPI 8 – Reliability Summary Table
# ===============================================================

st.subheader("📋 Machine Downtime Table")

st.dataframe(
    MACHINE_DOWNTIME.sort_values(
        by="Consumed_Hours", ascending=False
    ),
    use_container_width=True
)

# ===============================================================
# KPI 9 – Distribution Histogram
# ===============================================================

st.subheader("📊 Downtime Distribution")

fig_hist = px.histogram(
    DAILY_DOWNTIME,
    x="Consumed_Hours",
    nbins=20,
    template="plotly_white"
)
st.plotly_chart(fig_hist, use_container_width=True)

# ===============================================================
# KPI 10 – Cumulative Downtime Curve
# ===============================================================

st.subheader("📈 Cumulative Downtime")

DAILY_DOWNTIME["Cumulative"] = DAILY_DOWNTIME["Consumed_Hours"].cumsum()

fig_cum = px.area(
    DAILY_DOWNTIME,
    x="Date_Clean",
    y="Cumulative",
    template="plotly_white"
)
st.plotly_chart(fig_cum, use_container_width=True)

# ===============================================================
# KPI 11 – Operating vs Downtime
# ===============================================================

st.subheader("⚖ Operating vs Downtime Comparison")

fig_compare = go.Figure()
fig_compare.add_bar(
    x=["Operating Time"],
    y=[TOTAL_OPERATING_TIME]
)
fig_compare.add_bar(
    x=["Downtime"],
    y=[TOTAL_DOWNTIME]
)
st.plotly_chart(fig_compare, use_container_width=True)

# ===============================================================
# KPI 12 – Executive Insights
# ===============================================================

st.subheader("🧠 Executive Insights")

st.markdown(f"""
- Total Downtime Recorded: **{round(TOTAL_DOWNTIME,2)} hrs**
- Average Daily Downtime: **{round(AVERAGE_DAILY_DOWNTIME,2)} hrs**
- Plant Availability: **{round(AVAILABILITY_PERCENT,2)}%**
- Most Critical Machine: **{TOP5.iloc[0]['Machine']}**
- MTTR: **{round(MTTR,2)} hrs**
- MTBF: **{round(MTBF,2)} hrs**
- Downtime Variability (Std Dev): **{round(DOWNTIME_STD,2)}**
""")

st.markdown("---")
st.markdown("### ✅ Dashboard Ready for Management Review & PDF Export")
