# ============================================================
# MANAGEMENT KPI DASHBOARD – SAFE COMPLETE VERSION
# Downtime + MTTR + MTBF + Notification Analytics
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------
st.set_page_config(page_title="Management KPI Review", layout="wide")

st.title("📊 Management Operational KPI Dashboard")
st.markdown("### January – February 2026 Performance Review")
st.markdown("---")

# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------
try:
    df = pd.read_csv("data/cleaned_downtime_data.csv")
except:
    st.error("Data file not found. Please check path.")
    st.stop()

# Ensure required columns exist
required_columns = ["Date_Clean", "Machine", "Consumed_Hours"]

for col in required_columns:
    if col not in df.columns:
        st.error(f"Missing required column: {col}")
        st.stop()

df["Date_Clean"] = pd.to_datetime(df["Date_Clean"], errors="coerce")
df["Consumed_Hours"] = pd.to_numeric(df["Consumed_Hours"], errors="coerce").fillna(0)

# ------------------------------------------------------------
# ================= DOWNTIME KPI SECTION =====================
# ------------------------------------------------------------
st.header("⚙️ Downtime Performance Analytics")

TOTAL_DAYS = df["Date_Clean"].nunique()
TOTAL_MACHINES = df["Machine"].nunique()
TOTAL_DOWNTIME = df["Consumed_Hours"].sum()

DAILY_DOWNTIME = df.groupby("Date_Clean")["Consumed_Hours"].sum().reset_index()
MACHINE_DOWNTIME = df.groupby("Machine")["Consumed_Hours"].sum().reset_index()

AVERAGE_DAILY_DOWNTIME = TOTAL_DOWNTIME / TOTAL_DAYS if TOTAL_DAYS else 0

AVAILABLE_HOURS = TOTAL_DAYS * 24 * TOTAL_MACHINES
AVAILABILITY_PERCENT = (
    (1 - (TOTAL_DOWNTIME / AVAILABLE_HOURS)) * 100
    if AVAILABLE_HOURS else 0
)

ZERO_DOWNTIME_DAYS = DAILY_DOWNTIME[
    DAILY_DOWNTIME["Consumed_Hours"] == 0
].shape[0]

PEAK_DOWNTIME_DAY = DAILY_DOWNTIME.loc[
    DAILY_DOWNTIME["Consumed_Hours"].idxmax()
] if not DAILY_DOWNTIME.empty else None

DOWNTIME_STD = DAILY_DOWNTIME["Consumed_Hours"].std()

FAILURE_COUNT = df.shape[0]

MTTR = TOTAL_DOWNTIME / FAILURE_COUNT if FAILURE_COUNT else 0
TOTAL_OPERATING_TIME = AVAILABLE_HOURS - TOTAL_DOWNTIME
MTBF = TOTAL_OPERATING_TIME / FAILURE_COUNT if FAILURE_COUNT else 0

# ---------------- EXECUTIVE CARDS ----------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Downtime (hrs)", round(TOTAL_DOWNTIME, 2))
col2.metric("Avg Daily Downtime (hrs)", round(AVERAGE_DAILY_DOWNTIME, 2))
col3.metric("Availability (%)", round(AVAILABILITY_PERCENT, 2))
col4.metric("Zero Downtime Days", ZERO_DOWNTIME_DAYS)

col5, col6, col7, col8 = st.columns(4)

col5.metric("Peak Downtime Day",
            PEAK_DOWNTIME_DAY["Date_Clean"].date()
            if PEAK_DOWNTIME_DAY is not None else "N/A")

col6.metric("Peak Downtime (hrs)",
            round(PEAK_DOWNTIME_DAY["Consumed_Hours"], 2)
            if PEAK_DOWNTIME_DAY is not None else 0)

col7.metric("MTTR (hrs)", round(MTTR, 2))
col8.metric("MTBF (hrs)", round(MTBF, 2))

st.markdown("---")

# ---------------- DAILY TREND ----------------
if not DAILY_DOWNTIME.empty:
    fig1 = px.line(
        DAILY_DOWNTIME,
        x="Date_Clean",
        y="Consumed_Hours",
        markers=True,
        title="Daily Downtime Trend",
        template="plotly_dark"
    )
    st.plotly_chart(fig1, use_container_width=True)

# ---------------- MACHINE PARETO ----------------
if not MACHINE_DOWNTIME.empty:
    MACHINE_DOWNTIME = MACHINE_DOWNTIME.sort_values(
        by="Consumed_Hours",
        ascending=False
    )

    MACHINE_DOWNTIME["Cumulative_%"] = (
        MACHINE_DOWNTIME["Consumed_Hours"].cumsum() /
        MACHINE_DOWNTIME["Consumed_Hours"].sum()
    ) * 100

    fig2 = go.Figure()

    fig2.add_bar(
        x=MACHINE_DOWNTIME["Machine"],
        y=MACHINE_DOWNTIME["Consumed_Hours"],
        name="Downtime"
    )

    fig2.add_scatter(
        x=MACHINE_DOWNTIME["Machine"],
        y=MACHINE_DOWNTIME["Cumulative_%"],
        name="Cumulative %",
        yaxis="y2"
    )

    fig2.update_layout(
        title="Machine Downtime Pareto (80/20)",
        template="plotly_dark",
        yaxis2=dict(overlaying="y", side="right", range=[0, 100]),
        height=500
    )

    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ------------------------------------------------------------
# ================= NOTIFICATION KPI SECTION =================
# ------------------------------------------------------------
st.header("📢 Notification Compliance Analytics")

if "Notification_Status" in df.columns:

    notif_summary = (
        df.groupby(["Date_Clean", "Notification_Status"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )

    notif_summary["With Notification"] = notif_summary.get("With Notification", 0)
    notif_summary["Without Notification"] = notif_summary.get("Without Notification", 0)

    notif_summary["Total_Jobs"] = (
        notif_summary["With Notification"] +
        notif_summary["Without Notification"]
    )

    notif_summary["Compliance_%"] = (
        notif_summary["With Notification"] /
        notif_summary["Total_Jobs"].replace(0, np.nan)
    ) * 100

    TOTAL_JOBS = notif_summary["Total_Jobs"].sum()
    TOTAL_WITH = notif_summary["With Notification"].sum()
    TOTAL_WITHOUT = notif_summary["Without Notification"].sum()

    OVERALL_COMPLIANCE = (TOTAL_WITH / TOTAL_JOBS * 100) if TOTAL_JOBS else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Jobs", int(TOTAL_JOBS))
    col2.metric("Overall Compliance %", f"{OVERALL_COMPLIANCE:.1f}%")
    col3.metric("Without Notification", int(TOTAL_WITHOUT))

    fig3 = px.bar(
        notif_summary,
        x="Date_Clean",
        y=["With Notification", "Without Notification"],
        barmode="stack",
        title="Daily Jobs – Notification Status",
        template="plotly_dark"
    )

    st.plotly_chart(fig3, use_container_width=True)

    fig4 = px.line(
        notif_summary,
        x="Date_Clean",
        y="Compliance_%",
        markers=True,
        title="Daily Compliance %",
        template="plotly_dark"
    )

    fig4.update_layout(yaxis=dict(range=[0, 100]))
    st.plotly_chart(fig4, use_container_width=True)

else:
    st.warning("Notification_Status column not found in dataset.")
