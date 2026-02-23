# pages/2026_Drinkable_Update.py

import streamlit as st
import pandas as pd
import numpy as np
import os
import re
from datetime import datetime

st.set_page_config(page_title="2026 Drinkable Update", layout="wide")

DATA_PATH = "data/maintenance_data.xlsx"

st.title("2026 Drinkable Maintenance Dashboard")

# =========================================================
# LOAD DATA
# =========================================================

def load_data():
    if os.path.exists(DATA_PATH):
        df = pd.read_excel(DATA_PATH)
        return df
    else:
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.error("No file found in data/maintenance_data.xlsx")
    st.stop()

# =========================================================
# CLEAN & STANDARDIZE COLUMN NAMES (AUTO FIX)
# =========================================================

# Remove line breaks and extra spaces
df.columns = (
    df.columns
    .str.replace("\n", " ", regex=True)
    .str.replace("\r", " ", regex=True)
    .str.strip()
)

# Auto rename known broken headers
rename_map = {
    "Machine No": "Machine No.",
    "Machine No .": "Machine No.",
    "Notification No": "Notification No.",
    "Notification No .": "Notification No.",
    "Time Consume": "Time Consumed",
    "Requested  Time": "Requested Time",
    "Waiting  Time": "Waiting Time",
    "Description Of  Work": "Description Of Work",
}

df.rename(columns=rename_map, inplace=True)

# Show detected columns (for debugging if needed)
# st.write(df.columns.tolist())

# =========================================================
# REQUIRED COLUMNS CHECK
# =========================================================

required_columns = [
    "Date",
    "Machine No.",
    "Notification No.",
    "Shift",
    "Area",
    "Machine Classification",
    "Job",
    "Type",
    "Reported Problem",
    "Requested Time",
    "Description Of Work",
    "Spare Part Used",
    "Start",
    "End",
    "Waiting Time",
    "Time Consumed",
    "Performed By",
    "Remarks"
]

missing = [col for col in required_columns if col not in df.columns]

if missing:
    st.error(f"Still missing columns: {missing}")
    st.write("Detected columns:", df.columns.tolist())
    st.stop()

# =========================================================
# DATA PREPARATION
# =========================================================

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Start"] = pd.to_datetime(df["Start"], errors="coerce")
df["End"] = pd.to_datetime(df["End"], errors="coerce")
df["Requested Time"] = pd.to_datetime(df["Requested Time"], errors="coerce")

df["Time Consumed"] = pd.to_timedelta(df["Time Consumed"], errors="coerce").dt.total_seconds().div(60)
df["Time Consumed"] = df["Time Consumed"].fillna(0)

# =========================================================
# MTD / YTD FILTER
# =========================================================

col1, col2 = st.columns(2)

today = pd.Timestamp.today()

if "period" not in st.session_state:
    st.session_state.period = "ALL"

with col1:
    if st.button("MTD"):
        st.session_state.period = "MTD"

with col2:
    if st.button("YTD"):
        st.session_state.period = "YTD"

if st.session_state.period == "MTD":
    df = df[(df["Date"].dt.month == today.month) &
            (df["Date"].dt.year == today.year)]

elif st.session_state.period == "YTD":
    df = df[df["Date"].dt.year == today.year]

# =========================================================
# TECHNICIAN PERFORMANCE
# =========================================================

def split_tech(value):
    if pd.isna(value):
        return []
    parts = re.split(r"/|and", str(value))
    return [p.strip() for p in parts if p.strip()]

tech_list = []

for _, row in df.iterrows():
    techs = split_tech(row["Performed By"])
    for tech in techs:
        tech_list.append({
            "Technician": tech,
            "Date": row["Date"],
            "Minutes": row["Time Consumed"]
        })

tech_df = pd.DataFrame(tech_list)

tech_summary = tech_df.groupby("Technician")["Minutes"].sum().reset_index()

tech_date_summary = (
    tech_df.groupby(["Technician", "Date"])["Minutes"]
    .sum()
    .reset_index()
    .sort_values("Date")
)

# =========================================================
# HOURLY BREAKDOWN
# =========================================================

df["Hour"] = df["Start"].dt.hour
hour_counts = df["Hour"].value_counts().reindex(range(24), fill_value=0)

# =========================================================
# OTHER ANALYSIS
# =========================================================

machine_breakdown = df["Machine No."].value_counts()
job_type = df["Type"].value_counts()
spare_usage = df["Spare Part Used"].value_counts()
notif_machine = df.groupby("Machine No.")["Notification No."].count()
notif_date = df.groupby("Date")["Notification No."].count()
remarks_machine = df.groupby("Machine No.")["Remarks"].count()

# =========================================================
# DASHBOARD
# =========================================================

st.markdown("## Machine Breakdown Frequency")
st.bar_chart(machine_breakdown)

st.markdown("## Technician Performance (Minutes)")
st.bar_chart(tech_summary.set_index("Technician"))

st.markdown("## Technician Performance Table")
st.dataframe(tech_date_summary, use_container_width=True)

st.markdown("## Job Type Analysis")
st.bar_chart(job_type)

st.markdown("## Spare Parts Usage")
st.bar_chart(spare_usage)

st.markdown("## Notification Count per Machine")
st.bar_chart(notif_machine)

st.markdown("## Notification Count per Date")
st.line_chart(notif_date)

st.markdown("## Remarks Summary")
st.bar_chart(remarks_machine)

st.markdown("## Hourly Breakdown (0–23)")
hour_df = pd.DataFrame({
    "Hour": range(24),
    "Breakdowns": hour_counts.values
}).set_index("Hour")

st.bar_chart(hour_df)

st.success("Dashboard Loaded Successfully")
