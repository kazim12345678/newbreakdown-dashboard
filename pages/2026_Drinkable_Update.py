# pages/2026_Drinkable_Update.py

import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="2026 Drinkable Update", layout="wide")
st.title("2026 Drinkable Maintenance Dashboard")

uploaded_file = st.file_uploader("Upload Maintenance Excel File", type=["xlsx"])

if uploaded_file is None:
    st.stop()

# ===============================
# READ FILE SAFELY
# ===============================

df = pd.read_excel(uploaded_file)

# Clean all column names safely
df.columns = (
    df.columns
    .astype(str)
    .str.strip()
    .str.replace("\n", "")
)

# Make lowercase copy for searching
lower_cols = {col.lower(): col for col in df.columns}

# ===============================
# SAFE COLUMN FINDER
# ===============================

def find_column(keyword):
    for col in df.columns:
        if keyword.lower() in col.lower():
            return col
    return None

date_col = find_column("date")
machine_col = find_column("machine")
type_col = find_column("type")
spare_col = find_column("spare")
notif_col = find_column("notification")
tech_col = find_column("performed")
time_col = find_column("time consumed")

# ===============================
# DATE CONVERSION (SAFE)
# ===============================

if date_col:
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

if time_col:
    df[time_col] = pd.to_timedelta(df[time_col], errors="coerce")
    df["Minutes"] = df[time_col].dt.total_seconds() / 60
    df["Minutes"] = df["Minutes"].fillna(0)
else:
    df["Minutes"] = 0

# ===============================
# MACHINE BREAKDOWN
# ===============================

if machine_col:
    st.subheader("Machine Breakdown Frequency")
    st.bar_chart(df[machine_col].value_counts())

# ===============================
# JOB TYPE
# ===============================

if type_col:
    st.subheader("Job Type Analysis")
    st.bar_chart(df[type_col].value_counts())

# ===============================
# SPARE PARTS
# ===============================

if spare_col:
    st.subheader("Spare Parts Usage")
    st.bar_chart(df[spare_col].value_counts())

# ===============================
# NOTIFICATION PER DATE
# ===============================

if date_col and notif_col:
    st.subheader("Notification Count per Date")
    st.line_chart(df.groupby(date_col)[notif_col].count())

# ===============================
# TECHNICIAN PERFORMANCE
# ===============================

if tech_col:

    def split_tech(value):
        if pd.isna(value):
            return []
        parts = re.split(r"/|,|&", str(value))
        return [p.strip() for p in parts if p.strip()]

    tech_rows = []

    for _, row in df.iterrows():
        techs = split_tech(row[tech_col])
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
