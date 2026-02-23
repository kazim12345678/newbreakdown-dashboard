# pages/2026_Drinkable_Update.py

import streamlit as st
import pandas as pd
import numpy as np
import re

st.set_page_config(page_title="2026 Drinkable Update", layout="wide")

st.title("2026 Drinkable Maintenance Dashboard")

# =====================================================
# FILE UPLOAD
# =====================================================

uploaded_file = st.file_uploader("Upload Maintenance Excel File", type=["xlsx"])

if uploaded_file is None:
    st.warning("Please upload your Excel file to continue.")
    st.stop()

# =====================================================
# SMART HEADER DETECTION
# =====================================================

def smart_load_excel(file):
    raw = pd.read_excel(file, header=None)

    header_row = None
    for i in range(len(raw)):
        row_values = raw.iloc[i].astype(str).str.lower().tolist()
        if any("date" in cell for cell in row_values):
            header_row = i
            break

    if header_row is None:
        return pd.DataFrame()

    df = pd.read_excel(file, header=header_row)
    return df


df = smart_load_excel(uploaded_file)

if df.empty:
    st.error("Could not detect header row (Date column not found).")
    st.stop()

# =====================================================
# CLEAN COLUMNS
# =====================================================

df.columns = (
    df.columns
    .astype(str)
    .str.replace("\n", " ", regex=True)
    .str.strip()
)

df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

# =====================================================
# STANDARDIZE COLUMN NAMES
# =====================================================

df.rename(columns={
    "Time Consumed (minute)": "Time Consumed",
}, inplace=True)

# =====================================================
# SAFE CONVERSIONS
# =====================================================

if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

if "Time Consumed" in df.columns:
    df["Time Consumed"] = pd.to_numeric(df["Time Consumed"], errors="coerce").fillna(0)
else:
    df["Time Consumed"] = 0

# =====================================================
# MACHINE BREAKDOWN
# =====================================================

if "Machine No." in df.columns:
    st.markdown("## Machine Breakdown Frequency")
    st.bar_chart(df["Machine No."].value_counts())

# =====================================================
# JOB TYPE
# =====================================================

if "Type" in df.columns:
    st.markdown("## Job Type Analysis")
    st.bar_chart(df["Type"].value_counts())

# =====================================================
# SPARE PARTS
# =====================================================

if "Spare Part Used" in df.columns:
    st.markdown("## Spare Parts Usage")
    st.bar_chart(df["Spare Part Used"].value_counts())

# =====================================================
# NOTIFICATION PER DATE
# =====================================================

if "Date" in df.columns and "Notification No." in df.columns:
    st.markdown("## Notification Count per Date")
    st.line_chart(df.groupby("Date")["Notification No."].count())

# =====================================================
# TECHNICIAN PERFORMANCE
# =====================================================

if "Performed By" in df.columns:

    def split_tech(value):
        if pd.isna(value) or str(value).strip() == "":
            return []
        parts = re.split(r"/|and|,", str(value))
        return [p.strip() for p in parts if p.strip()]

    tech_rows = []

    for _, row in df.iterrows():
        techs = split_tech(row["Performed By"])
        for tech in techs:
            tech_rows.append({
                "Technician": tech,
                "Minutes": row["Time Consumed"]
            })

    if len(tech_rows) > 0:
        tech_df = pd.DataFrame(tech_rows)

        st.markdown("## Technician Performance (Total Minutes)")
        st.bar_chart(tech_df.groupby("Technician")["Minutes"].sum())

st.success("Dashboard Loaded Successfully")
