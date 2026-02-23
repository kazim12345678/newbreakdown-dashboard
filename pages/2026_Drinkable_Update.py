# pages/2026_Drinkable_Update.py

import streamlit as st
import pandas as pd
import numpy as np
import os
import re

st.set_page_config(page_title="2026 Drinkable Update", layout="wide")

st.title("2026 Drinkable Maintenance Dashboard")

DATA_PATH = "data/maintenance_data.xlsx"

# =====================================================
# SAFE EXCEL LOADER (AUTO HEADER DETECTION)
# =====================================================

def smart_load_excel(path):
    try:
        raw = pd.read_excel(path, header=None)

        header_row = None
        for i in range(len(raw)):
            row_values = raw.iloc[i].astype(str).str.lower().tolist()
            if any("date" in cell for cell in row_values):
                header_row = i
                break

        if header_row is None:
            return pd.DataFrame()

        df = pd.read_excel(path, header=header_row)
        return df

    except:
        return pd.DataFrame()


if not os.path.exists(DATA_PATH):
    st.warning("Excel file not found.")
    st.stop()

df = smart_load_excel(DATA_PATH)

if df.empty:
    st.warning("File loaded but no readable data found.")
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
# STANDARDIZE KNOWN COLUMN VARIATIONS
# =====================================================

rename_map = {
    "Time Consumed (minute)": "Time Consumed",
    "Maintenance Time": "Maintenance Time",
}

df.rename(columns=rename_map, inplace=True)

# =====================================================
# SAFE DATE CONVERSION
# =====================================================

if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

if "Time Consumed" in df.columns:
    df["Time Consumed"] = pd.to_numeric(df["Time Consumed"], errors="coerce").fillna(0)
else:
    df["Time Consumed"] = 0

# =====================================================
# PERIOD FILTER
# =====================================================

today = pd.Timestamp.today()

col1, col2 = st.columns(2)

if "period" not in st.session_state:
    st.session_state.period = "ALL"

with col1:
    if st.button("MTD"):
        st.session_state.period = "MTD"

with col2:
    if st.button("YTD"):
        st.session_state.period = "YTD"

if "Date" in df.columns:
    if st.session_state.period == "MTD":
        df = df[(df["Date"].dt.month == today.month) &
                (df["Date"].dt.year == today.year)]

    elif st.session_state.period == "YTD":
        df = df[df["Date"].dt.year == today.year]

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
# NOTIFICATION PER MACHINE
# =====================================================

if "Machine No." in df.columns and "Notification No." in df.columns:
    st.markdown("## Notification Count per Machine")
    st.bar_chart(df.groupby("Machine No.")["Notification No."].count())

# =====================================================
# NOTIFICATION PER DATE
# =====================================================

if "Date" in df.columns and "Notification No." in df.columns:
    st.markdown("## Notification Count per Date")
    st.line_chart(df.groupby("Date")["Notification No."].count())

# =====================================================
# TECHNICIAN PERFORMANCE (SAFE)
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
                "Date": row["Date"] if "Date" in df.columns else None,
                "Minutes": row["Time Consumed"]
            })

    if len(tech_rows) > 0:
        tech_df = pd.DataFrame(tech_rows)

        st.markdown("## Technician Performance (Total Minutes)")
        st.bar_chart(tech_df.groupby("Technician")["Minutes"].sum())

# =====================================================
# REMARKS COUNT
# =====================================================

if "Machine No." in df.columns and "Remarks" in df.columns:
    st.markdown("## Remarks Count per Machine")
    st.bar_chart(df.groupby("Machine No.")["Remarks"].count())

st.success("Dashboard Loaded Successfully")
