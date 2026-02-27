# =========================================================
# Page: Drinkable KPIs — Jan & Feb 2026
# File: pages/01_Drinkable_KPIs_Jan_Feb_2026.py
#
# IMPORTANT ASSUMPTION (as requested):
RUN_HOURS_PER_DAY = 600   # Used for MTBF calculation
PLANNED_AVAILABLE_HOURS_PER_DAY = 24  # Used for Availability %
# =========================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import date

st.set_page_config(layout="wide")

# ---------------------------------------------------------
# Page Title
# ---------------------------------------------------------
st.title("🥤 Drinkable Section KPIs — Jan & Feb 2026")
st.caption(
    "Period: 01 Jan 2026 → 26 Feb 2026 | "
    f"MTBF assumption = {RUN_HOURS_PER_DAY} hrs/day"
)

# ---------------------------------------------------------
# Load data from main.py
# ---------------------------------------------------------
df = None

if "df_main" in st.session_state:
    df = st.session_state["df_main"]
elif "df" in globals():
    df = globals()["df"]

if df is None:
    st.error(
        "No data found. "
        "Please load and clean data in main.py and store it as "
        "`st.session_state['df_main']`."
    )
    st.stop()

# ---------------------------------------------------------
# Filter period: Jan–Feb 2026
# ---------------------------------------------------------
START_DATE = date(2026, 1, 1)
END_DATE   = date(2026, 2, 26)

df = df[
    (df["Date_Clean"] >= START_DATE) &
    (df["Date_Clean"] <= END_DATE)
].copy()

# ---------------------------------------------------------
# Executive KPIs
# ---------------------------------------------------------
total_downtime = df["Consumed_Hours"].sum()
distinct_days = df["Date_Clean"].nunique()

# Breakdown only
df_bd = df[df["Job_Category"] == "Breakdown"]
bd_events = len(df_bd)
bd_downtime = df_bd["Consumed_Hours"].sum()

total_running_hours = distinct_days * RUN_HOURS_PER_DAY

mttr = bd_downtime / bd_events if bd_events else 0
mtbf = total_running_hours / bd_events if bd_events else 0

planned_hours_total = distinct_days * PLANNED_AVAILABLE_HOURS_PER_DAY
availability = (
    1 - (total_downtime / planned_hours_total)
) * 100 if planned_hours_total else 0

# ---------------------------------------------------------
# KPI Cards
# ---------------------------------------------------------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Downtime (hrs)", f"{total_downtime:,.2f}")
c2.metric("Availability %", f"{availability:,.2f}%")
c3.metric("MTTR (hrs)", f"{mttr:,.2f}")
c4.metric("MTBF (hrs)", f"{mtbf:,.2f}")

st.divider()

# ---------------------------------------------------------
# KPI 1 — Date × Machine Downtime
# ---------------------------------------------------------
st.header("1️⃣ Date-wise Machine Downtime")

kpi1 = pd.pivot_table(
    df,
    index="Date_Clean",
    columns="Machine No.",
    values="Consumed_Hours",
    aggfunc="sum",
    fill_value=0
).sort_index()

kpi1["Grand Total"] = kpi1.sum(axis=1)

fig, ax = plt.subplots(figsize=(10, 3.5))
ax.plot(kpi1.index, kpi1["Grand Total"], linewidth=2)
ax.set_title("Daily Total Downtime (hrs)")
ax.set_xlabel("Date")
ax.set_ylabel("Downtime (hrs)")
ax.tick_params(axis="x", rotation=45)
st.pyplot(fig)

st.dataframe(kpi1, use_container_width=True)

st.divider()

# ---------------------------------------------------------
# KPI 2 — Top Machines + Pareto
# ---------------------------------------------------------
st.header("2️⃣ Top Machines & Pareto Analysis")

pareto = (
    df.groupby("Machine No.")["Consumed_Hours"]
    .sum()
    .sort_values(ascending=False)
    .to_frame("Downtime_Hours")
)

pareto["% of Total"] = pareto["Downtime_Hours"] / pareto["Downtime_Hours"].sum() * 100
pareto["Cumulative %"] = pareto["% of Total"].cumsum()

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    ax.bar(pareto.head(13).index, pareto.head(13)["Downtime_Hours"])
    ax.set_title("Top 13 Machines by Downtime (hrs)")
    ax.tick_params(axis="x", rotation=45)
    st.pyplot(fig)

with col2:
    fig, ax1 = plt.subplots(figsize=(6.5, 3.8))
    ax1.bar(pareto.index, pareto["Downtime_Hours"])
    ax1.set_ylabel("Downtime (hrs)")
    ax1.tick_params(axis="x", rotation=45)

    ax2 = ax1.twinx()
    ax2.plot(pareto.index, pareto["Cumulative %"], color="red", marker="o")
    ax2.set_ylabel("Cumulative %")
    ax2.set_ylim(0, 110)

    ax1.set_title("Pareto — Downtime Contribution")
    st.pyplot(fig)

st.dataframe(pareto, use_container_width=True)

st.divider()

# ---------------------------------------------------------
# KPI 3 — Shift & Job Type
# ---------------------------------------------------------
st.header("3️⃣ Shift & Job Category Performance")

kpi_shift = df.groupby("Shift")["Consumed_Hours"].sum().sort_values(ascending=False)
kpi_job = df.groupby("Job_Category")["Consumed_Hours"].sum()

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(5.5, 3.5))
    ax.bar(kpi_shift.index, kpi_shift.values)
    ax.set_title("Downtime by Shift (hrs)")
    st.pyplot(fig)
    st.dataframe(kpi_shift.to_frame("Downtime_Hours"))

with col2:
    fig, ax = plt.subplots(figsize=(5.5, 3.5))
    ax.bar(kpi_job.index, kpi_job.values)
    ax.set_title("Downtime by Job Category (hrs)")
    st.pyplot(fig)
    st.dataframe(kpi_job.to_frame("Downtime_Hours"))

st.divider()

# ---------------------------------------------------------
# KPI 4 — Technician Workload (FULL CREDIT)
# ---------------------------------------------------------
st.header("4️⃣ Technician Workload (FULL Credit Rule)")

st.caption(
    "If two technicians worked on the same job, "
    "each technician receives FULL job minutes (not divided)."
)

tech = (
    df.groupby(["Technician", "Job_Category"])["Consumed_Hours"]
    .sum()
    .unstack(fill_value=0)
)

tech["Total_Hours"] = tech.sum(axis=1)
tech = tech.sort_values("Total_Hours", ascending=False)

fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(tech.head(10).index, tech.head(10)["Total_Hours"])
ax.set_title("Top 10 Technicians by Workload (hrs)")
ax.tick_params(axis="x", rotation=45)
st.pyplot(fig)

st.dataframe(tech, use_container_width=True)

st.divider()

# ---------------------------------------------------------
# KPI 5 — Breakdown Reasons
# ---------------------------------------------------------
st.header("5️⃣ Top Breakdown Reasons")

reasons = (
    df_bd.groupby("Reason_Clean")["Consumed_Hours"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig, ax = plt.subplots(figsize=(8, 3.8))
ax.barh(reasons.index[::-1], reasons.values[::-1])
ax.set_title("Top 10 Breakdown Reasons (hrs)")
st.pyplot(fig)

st.dataframe(reasons.to_frame("Downtime_Hours"))

st.info(
    "✅ MTTR & MTBF calculated using Breakdown (B/D) jobs only.\n\n"
    f"✅ MTBF uses fixed assumption: {RUN_HOURS_PER_DAY} hrs/day."
)
