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

# =========================
# Load Data
# =========================

@st.cache_data
def load_data():
    if os.path.exists(DATA_PATH):
        df = pd.read_excel(DATA_PATH)
        return df
    else:
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.warning("No data found in data/maintenance_data.xlsx")
    st.stop()

# =========================
# Data Preprocessing
# =========================

# Ensure date column
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Convert time columns
time_columns = ["Requested Time", "Start", "End"]
for col in time_columns:
    df[col] = pd.to_datetime(df[col], errors="coerce")

# Ensure numeric minutes
df["Time Consumed"] = pd.to_numeric(df["Time Consumed"], errors="coerce").fillna(0)
df["Waiting Time"] = pd.to_numeric(df["Waiting Time"], errors="coerce").fillna(0)

# =========================
# MTD / YTD Buttons
# =========================

col1, col2 = st.columns(2)

today = pd.Timestamp.today()

with col1:
    if st.button("MTD"):
        df = df[(df["Date"].dt.month == today.month) &
                (df["Date"].dt.year == today.year)]

with col2:
    if st.button("YTD"):
        df = df[(df["Date"].dt.year == today.year)]

# =========================
# Technician Performance
# =========================

def split_technicians(row):
    if pd.isna(row):
        return []
    parts = re.split(r"/|and", str(row))
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

# =========================
# Hourly Breakdown
# =========================

df["Hour"] = df["Start"].dt.hour
hour_counts = df["Hour"].value_counts().reindex(range(24), fill_value=0)

# =========================
# Machine Breakdown Frequency
# =========================

machine_breakdown = df["Machine No."].value_counts().reset_index()
machine_breakdown.columns = ["Machine No.", "Job Count"]

# =========================
# Job Type Analysis
# =========================

job_type_analysis = df["Type"].value_counts().reset_index()
job_type_analysis.columns = ["Type", "Count"]

# =========================
# Spare Parts Usage
# =========================

spare_parts = df["Spare Part Used"].value_counts().reset_index()
spare_parts.columns = ["Spare Part Used", "Count"]

# =========================
# Notification Analysis
# =========================

notif_machine = df.groupby("Machine No.")["Notification No."].count().reset_index()
notif_machine.columns = ["Machine No.", "Notification Count"]

notif_date = df.groupby("Date")["Notification No."].count().reset_index()
notif_date.columns = ["Date", "Notification Count"]

# =========================
# Remarks Summary
# =========================

remarks_summary = df.groupby("Machine No.")["Remarks"].count().reset_index()
remarks_summary.columns = ["Machine No.", "Remarks Count"]

# =========================
# DASHBOARD SECTIONS
# =========================

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
})
hour_df = hour_df.set_index("Hour")
st.bar_chart(hour_df)

st.success("2026 Drinkable Maintenance Dashboard Loaded Successfully")
