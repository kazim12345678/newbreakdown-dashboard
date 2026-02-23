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

# =====================================================
# DATA LOADING (Persistent + Optional Upload Replace)
# =====================================================

def load_data():
    if os.path.exists(DATA_PATH):
        df = pd.read_excel(DATA_PATH)
        return df
    else:
        return pd.DataFrame()

def save_data(df):
    os.makedirs("data", exist_ok=True)
    df.to_excel(DATA_PATH, index=False)

df = load_data()

# Optional file replacement (NOT required)
st.sidebar.markdown("### Optional: Replace Data File")
uploaded_file = st.sidebar.file_uploader("Upload new Excel file", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    save_data(df)
    st.sidebar.success("File replaced successfully!")

if df.empty:
    st.warning("No data found. Please upload maintenance_data.xlsx in data folder.")
    st.stop()

# =====================================================
# CLEAN COLUMN NAMES (PREVENT KEYERROR)
# =====================================================

df.columns = df.columns.str.strip()

required_columns = [
    "Date", "Machine No.", "Notification No.", "Shift", "Area",
    "Machine Classification", "Job", "Type", "Reported Problem",
    "Requested Time", "Description Of Work", "Spare Part Used",
    "Start", "End", "Waiting Time", "Time Consumed",
    "Performed By", "Remarks"
]

missing_cols = [col for col in required_columns if col not in df.columns]

if missing_cols:
    st.error(f"Missing columns in Excel file: {missing_cols}")
    st.stop()

# =====================================================
# DATA PREPROCESSING
# =====================================================

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Start"] = pd.to_datetime(df["Start"], errors="coerce")
df["Requested Time"] = pd.to_datetime(df["Requested Time"], errors="coerce")
df["End"] = pd.to_datetime(df["End"], errors="coerce")

df["Time Consumed"] = pd.to_numeric(df["Time Consumed"], errors="coerce").fillna(0)
df["Waiting Time"] = pd.to_numeric(df["Waiting Time"], errors="coerce").fillna(0)

# =====================================================
# MTD / YTD FILTER
# =====================================================

col1, col2 = st.columns(2)
today = pd.Timestamp.today()

if "period_filter" not in st.session_state:
    st.session_state.period_filter = "ALL"

with col1:
    if st.button("MTD"):
        st.session_state.period_filter = "MTD"

with col2:
    if st.button("YTD"):
        st.session_state.period_filter = "YTD"

if st.session_state.period_filter == "MTD":
    df = df[(df["Date"].dt.month == today.month) &
            (df["Date"].dt.year == today.year)]

elif st.session_state.period_filter == "YTD":
    df = df[df["Date"].dt.year == today.year]

# =====================================================
# TECHNICIAN PERFORMANCE
# =====================================================

def split_technicians(value):
    if pd.isna(value):
        return []
    parts = re.split(r"/|and", str(value))
    return [p.strip() for p in parts if p.strip()]

tech_rows = []

for _, row in df.iterrows():
    techs = split_technicians(row["Performed By"])
    for tech in techs:
        tech_rows.append({
            "Technician": tech,
            "Date": row["Date"],
            "Minutes": row["Time Consumed"]
        })

tech_df = pd.DataFrame(tech_rows)

tech_summary = tech_df.groupby("Technician")["Minutes"].sum().reset_index()

tech_date_summary = (
    tech_df.groupby(["Technician", "Date"])["Minutes"]
    .sum()
    .reset_index()
    .sort_values("Date")
)

# =====================================================
# HOURLY BREAKDOWN (0–23 Always Visible)
# =====================================================

df["Hour"] = df["Start"].dt.hour
hour_counts = df["Hour"].value_counts().reindex(range(24), fill_value=0)

# =====================================================
# MACHINE BREAKDOWN FREQUENCY
# =====================================================

machine_breakdown = df["Machine No."].value_counts().reset_index()
machine_breakdown.columns = ["Machine No.", "Job Count"]

# =====================================================
# JOB TYPE ANALYSIS
# =====================================================

job_type_analysis = df["Type"].value_counts().reset_index()
job_type_analysis.columns = ["Type", "Count"]

# =====================================================
# SPARE PART USAGE
# =====================================================

spare_parts = df["Spare Part Used"].value_counts().reset_index()
spare_parts.columns = ["Spare Part Used", "Count"]

# =====================================================
# NOTIFICATION ANALYSIS
# =====================================================

notif_machine = df.groupby("Machine No.")["Notification No."].count().reset_index()
notif_machine.columns = ["Machine No.", "Notification Count"]

notif_date = df.groupby("Date")["Notification No."].count().reset_index()
notif_date.columns = ["Date", "Notification Count"]

# =====================================================
# REMARKS SUMMARY
# =====================================================

remarks_summary = df.groupby("Machine No.")["Remarks"].count().reset_index()
remarks_summary.columns = ["Machine No.", "Remarks Count"]

# =====================================================
# DASHBOARD
# =====================================================

st.markdown("## Machine Breakdown Frequency")
st.bar_chart(machine_breakdown.set_index("Machine No."))

st.markdown("## Technician Performance (Total Minutes)")
st.bar_chart(tech_summary.set_index("Technician"))

st.markdown("## Technician Performance Table (Date-wise)")
st.dataframe(tech_date_summary, use_container_width=True)

st.markdown("## Job Type Analysis")
st.bar_chart(job_type_analysis.set_index("Type"))

st.markdown("## Spare Parts Usage Summary")
st.bar_chart(spare_parts.set_index("Spare Part Used"))

st.markdown("## Notification Count per Machine")
st.bar_chart(notif_machine.set_index("Machine No."))

st.markdown("## Notification Count per Date")
st.line_chart(notif_date.set_index("Date"))

st.markdown("## Remarks Summary")
st.bar_chart(remarks_summary.set_index("Machine No."))

st.markdown("## Hourly Breakdown (0–23)")
hour_df = pd.DataFrame({
    "Hour": range(24),
    "Breakdowns": hour_counts.values
}).set_index("Hour")

st.bar_chart(hour_df)

st.success("2026 Drinkable Maintenance Dashboard Loaded Successfully")
