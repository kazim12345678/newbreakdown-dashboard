# pages/2026_Drinkable_Update.py

import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="2026 Drinkable Update", layout="wide")

st.title("2026 Drinkable Maintenance Dashboard")

# =====================================================
# UPLOAD FILE
# =====================================================

uploaded_file = st.file_uploader("Upload Maintenance Excel File", type=["xlsx"])

if uploaded_file is None:
    st.warning("Please upload your Excel file.")
    st.stop()

# =====================================================
# READ FILE DIRECTLY (NO SMART DETECTION)
# =====================================================

df = pd.read_excel(uploaded_file)

# Clean column spaces
df.columns = df.columns.str.strip()

# =====================================================
# BASIC CONVERSIONS
# =====================================================

# Convert Date
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Convert Time Consumed (format 0:15:00)
df["Time Consumed"] = pd.to_timedelta(df["Time Consumed"], errors="coerce")
df["Minutes"] = df["Time Consumed"].dt.total_seconds() / 60

df["Minutes"] = df["Minutes"].fillna(0)

# =====================================================
# MACHINE BREAKDOWN
# =====================================================

st.subheader("Machine Breakdown Frequency")
st.bar_chart(df["Machine No."].value_counts())

# =====================================================
# JOB TYPE
# =====================================================

st.subheader("Job Type Analysis")
st.bar_chart(df["Type"].value_counts())

# =====================================================
# SPARE PARTS
# =====================================================

st.subheader("Spare Parts Usage")
st.bar_chart(df["Spare Part Used"].value_counts())

# =====================================================
# NOTIFICATION PER DATE
# =====================================================

st.subheader("Notification Count per Date")
st.line_chart(df.groupby("Date")["Notification No."].count())

# =====================================================
# TECHNICIAN PERFORMANCE
# =====================================================

def split_tech(value):
    if pd.isna(value):
        return []
    parts = re.split(r"/|,|&", str(value))
    return [p.strip() for p in parts if p.strip()]

tech_rows = []

for _, row in df.iterrows():
    techs = split_tech(row["Performed By"])
    for tech in techs:
        tech_rows.append({
            "Technician": tech,
            "Minutes": row["Minutes"]
        })

tech_df = pd.DataFrame(tech_rows)

if not tech_df.empty:
    st.subheader("Technician Performance (Total Minutes)")
    st.bar_chart(tech_df.groupby("Technician")["Minutes"].sum())

st.success("Dashboard Loaded Successfully")
