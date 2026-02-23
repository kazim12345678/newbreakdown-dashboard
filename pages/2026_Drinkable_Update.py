# pages/2026_Drinkable_Update.py

import streamlit as st
import pandas as pd
import numpy as np
import os
import re

st.set_page_config(page_title="2026 Drinkable Update", layout="wide")

DATA_PATH = "data/maintenance_data.xlsx"

st.title("2026 Drinkable Maintenance Dashboard")

# ===============================
# LOAD FILE
# ===============================

def smart_load_excel(path):
    raw = pd.read_excel(path, header=None)

    header_row_index = None
    for i in range(len(raw)):
        row_values = raw.iloc[i].astype(str).str.lower().tolist()
        if any("date" in cell for cell in row_values):
            header_row_index = i
            break

    if header_row_index is None:
        st.error("Header row not found.")
        st.stop()

    df = pd.read_excel(path, header=header_row_index)
    return df


if not os.path.exists(DATA_PATH):
    st.error("File not found in data/maintenance_data.xlsx")
    st.stop()

df = smart_load_excel(DATA_PATH)

# ===============================
# CLEAN COLUMNS
# ===============================

df.columns = (
    df.columns
    .astype(str)
    .str.replace("\n", " ", regex=True)
    .str.strip()
)

# Remove unnamed columns
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

# ===============================
# RENAME TO STANDARD
# ===============================

df.rename(columns={
    "Time Consumed (minute)": "Time Consumed",
    "Maintenance Time": "Maintenance Time"
}, inplace=True)

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
    "Time Consumed",
    "Performed By",
    "Remarks"
]

missing = [col for col in required_columns if col not in df.columns]

if missing:
    st.error(f"Still missing columns: {missing}")
    st.write("Detected columns:", df.columns.tolist())
    st.stop()

# ===============================
# DATA PREPARATION
# ===============================

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

df["Time Consumed"] = pd.to_numeric(df["Time Consumed"], errors="coerce")
df["Time Consumed"] = df["Time Consumed"].fillna(0)

# ===============================
# MTD / YTD FILTER
# ===============================

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

# ===============================
# TECHNICIAN SPLIT
# ===============================

def split_tech(value):
    if pd.isna(value):
        return []
    parts = re.split(r"/|and", str(value))
    return [p.strip() for p in parts if p.strip()]

tech_rows = []

for _, row in df.iterrows():
    techs = split_tech(row["Performed By"])
    for tech in techs:
        tech_rows.append({
            "Technician": tech,
            "Date": row["Date"],
            "Minutes": row["Time Consumed"]
        })

tech_df = pd.DataFrame(tech_rows)

tech_summary = tech_df.groupby("Technician")["Minutes"].sum()
tech_date_summary = tech_df.groupby(["Technician", "Date"])["Minutes"].sum().reset_index()

# ===============================
# DASHBOARD
# ===============================

st.markdown("## Machine Breakdown Frequency")
st.bar_chart(df["Machine No."].value_counts())

st.markdown("## Technician Performance (Total Minutes)")
st.bar_chart(tech_summary)

st.markdown("## Technician Performance Per Date")
st.dataframe(tech_date_summary, use_container_width=True)

st.markdown("## Job Type Analysis")
st.bar_chart(df["Type"].value_counts())

st.markdown("## Spare Parts Usage")
st.bar_chart(df["Spare Part Used"].value_counts())

st.markdown("## Notification Count per Machine")
st.bar_chart(df.groupby("Machine No.")["Notification No."].count())

st.markdown("## Notification Count per Date")
st.line_chart(df.groupby("Date")["Notification No."].count())

st.markdown("## Remarks Count per Machine")
st.bar_chart(df.groupby("Machine No.")["Remarks"].count())

st.success("Dashboard Loaded Successfully")
