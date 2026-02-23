import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# ----------------- PAGE CONFIG -----------------
st.set_page_config(page_title="2026 – Drinkable Section Current Update", layout="wide")
st.title("2026 – Drinkable Section Current Update")

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "maintenance_data.xlsx")


# ----------------- DETECT REAL HEADER -----------------

def load_real_data(path):
    df_raw = pd.read_excel(path, header=None)

    # Find the row where the REAL header starts
    header_keywords = [
        "Date", "Machine No.", "Notification No.", "Shift",
        "Area", "Machine Classification", "Job", "Type",
        "Reported Problem", "Requested Time", "Description Of Work",
        "Spare Part Used", "Start", "End", "Waiting Time",
        "Time Consumed", "Performed By", "Remarks"
    ]

    header_row = None
    for i in range(len(df_raw)):
        row_values = df_raw.iloc[i].astype(str).str.strip().tolist()
        match_count = sum(1 for h in header_keywords if h in row_values)
        if match_count >= 8:  # enough columns match
            header_row = i
            break

    if header_row is None:
        st.error("Could not detect header row in Excel file.")
        st.stop()

    df = pd.read_excel(path, header=header_row)
    return df


# ----------------- SAFE HELPERS -----------------

def safe_col(df, col, default=""):
    return df[col] if col in df.columns else pd.Series([default] * len(df))

def safe_time(series):
    if series.dtype in ["float64", "int64"]:
        return pd.to_datetime(series, unit="D", origin="1899-12-30", errors="coerce")
    return pd.to_datetime(series, errors="coerce")

def safe_timedelta(series):
    if series.dtype in ["float64", "int64"]:
        return pd.to_timedelta(series, unit="D", errors="coerce").fillna(pd.Timedelta(0))
    return pd.to_timedelta(series, errors="coerce").fillna(pd.Timedelta(0))


# ----------------- CLEANING -----------------

def clean_data(df):
    df.columns = [c.strip() for c in df.columns]

    df["Date"] = safe_time(safe_col(df, "Date"))
    df["Requested Time"] = safe_time(safe_col(df, "Requested Time"))
    df["Start"] = safe_time(safe_col(df, "Start"))
    df["End"] = safe_time(safe_col(df, "End"))
    df["Time Consumed"] = safe_timedelta(safe_col(df, "Time Consumed"))

    df["Minutes"] = df["Time Consumed"].dt.total_seconds() / 60

    df["Hour"] = df["Requested Time"].dt.hour
    df["Hour"] = df["Hour"].fillna(df["Start"].dt.hour)
    df["Hour"] = df["Hour"].fillna(0).astype(int)

    # Skip incomplete rows
    df = df[df["Date"].notna()]
    df = df[df["Minutes"] >= 0]

    return df


# ----------------- TECHNICIAN SPLIT -----------------

def explode_tech(df):
    perf = safe_col(df, "Performed By").fillna("").astype(str)
    perf = (
        perf.str.replace(" and ", "/", case=False)
        .str.replace("&", "/", case=False)
        .str.replace(",", "/", case=False)
    )
    df["Tech_List"] = perf.str.split("/")
    df2 = df.explode("Tech_List")
    df2["Tech_List"] = df2["Tech_List"].astype(str).str.strip()
    df2 = df2[df2["Tech_List"] != ""]
    return df2


# ----------------- LOAD DATA -----------------

uploaded = st.file_uploader("Upload updated Excel", type=["xlsx", "xls"])

if uploaded:
    uploaded_df = load_real_data(uploaded)
    uploaded_df.to_excel(DATA_PATH, index=False)
    st.success("File saved permanently.")

if not os.path.exists(DATA_PATH):
    st.warning("No saved data found.")
    st.stop()

df = load_real_data(DATA_PATH)
df = clean_data(df)
df_tech = explode_tech(df.copy())


# ----------------- MTD / YTD -----------------

col1, col2, col3 = st.columns(3)
mode = "ALL"

if col1.button("MTD"):
    mode = "MTD"
if col2.button("YTD"):
    mode = "YTD"
if col3.button("ALL"):
    mode = "ALL"

today = datetime.today()

if mode == "MTD":
    df = df[df["Date"].dt.month == today.month]
    df_tech = df_tech[df_tech["Date"].dt.month == today.month]

if mode == "YTD":
    df = df[df["Date"].dt.year == today.year]
    df_tech = df_tech[df_tech["Date"].dt.year == today.year]


# ----------------- FILTERS -----------------

st.sidebar.header("Filters")

machine_list = sorted(safe_col(df, "Machine No.").dropna().astype(str).unique())
shift_list = sorted(safe_col(df, "Shift").dropna().astype(str).unique())
job_list = sorted(safe_col(df, "Job").dropna().astype(str).unique())
area_list = sorted(safe_col(df, "Machine Classification").dropna().astype(str).unique())
tech_list = sorted(df_tech["Tech_List"].dropna().astype(str).unique())

machine_filter = st.sidebar.multiselect("Machine", machine_list)
shift_filter = st.sidebar.multiselect("Shift", shift_list)
job_filter = st.sidebar.multiselect("Job", job_list)
area_filter = st.sidebar.multiselect("Area", area_list)
tech_filter = st.sidebar.multiselect("Technician", tech_list)

df_view = df.copy()

if machine_filter:
    df_view = df_view[df_view["Machine No."].astype(str).isin(machine_filter)]
if shift_filter:
    df_view = df_view[df_view["Shift"].astype(str).isin(shift_filter)]
if job_filter:
    df_view = df_view[df_view["Job"].astype(str).isin(job_filter)]
if area_filter:
    df_view = df_view[df_view["Machine Classification"].astype(str).isin(area_filter)]

df_tech_view = df_tech.copy()
if tech_filter:
    df_tech_view = df_tech_view[df_tech_view["Tech_List"].astype(str).isin(tech_filter)]


# ----------------- DASHBOARDS -----------------

tabs = st.tabs([
    "Machine Breakdown",
    "Technician Performance",
    "Job Type",
    "Spare Parts",
    "Notifications",
    "Remarks",
    "Hourly Breakdown",
    "Raw Data"
])

# ---------- Machine Breakdown ----------
with tabs[0]:
    col = safe_col(df_view, "Machine No.")
    if col.empty:
        st.info("No Machine No. data available.")
    else:
        freq = col.astype(str).value_counts().reset_index()
        freq.columns = ["Machine No.", "Jobs"]
        st.plotly_chart(px.bar(freq, x="Machine No.", y="Jobs"), use_container_width=True)

# ---------- Technician Performance ----------
with tabs[1]:
    if df_tech_view.empty:
        st.info("No technician data.")
    else:
        tech = df_tech_view.groupby("Tech_List")["Minutes"].sum().reset_index()
        st.plotly_chart(px.bar(tech, x="Tech_List", y="Minutes"), use_container_width=True)

        tech_date = df_tech_view.groupby(["Tech_List", "Date"])["Minutes"].sum().reset_index()
        st.dataframe(tech_date, use_container_width=True)

# ---------- Job Type ----------
with tabs[2]:
    col = safe_col(df_view, "Job")
    if col.empty:
        st.info("No Job data.")
    else:
        job_counts = col.value_counts().reset_index()
        job_counts.columns = ["Job", "Count"]
        st.plotly_chart(px.bar(job_counts, x="Job", y="Count"), use_container_width=True)

# ---------- Spare Parts ----------
with tabs[3]:
    spare = safe_col(df_view, "Spare Part Used").fillna("").astype(str)
    spare = spare[spare.str.strip() != ""]
    if spare.empty:
        st.info("No spare parts used.")
    else:
        spare_counts = spare.value_counts().reset_index()
        spare_counts.columns = ["Spare Part", "Count"]
        st.plotly_chart(px.bar(spare_counts, x="Spare Part", y="Count"), use_container_width=True)
        st.dataframe(spare_counts)

# ---------- Notifications ----------
with tabs[4]:
    if ("Machine No." in df_view.columns) and ("Notification No." in df_view.columns):
        notif_mach = df_view.groupby("Machine No.")["Notification No."].nunique().reset_index()
        notif_mach.columns = ["Machine No.", "Unique Notifications"]
        st.plotly_chart(px.bar(notif_mach, x="Machine No.", y="Unique Notifications"), use_container_width=True)
    else:
        st.info("Notification or Machine No. missing.")

# ---------- Remarks ----------
with tabs[5]:
    remarks = safe_col(df_view, "Remarks").astype(str)
    remarks = remarks[remarks.str.strip() != ""]
    if remarks.empty:
        st.info("No remarks.")
    else:
        remarks_mach = df_view[df_view["Remarks"].astype(str).str.strip() != ""]["Machine No."].value_counts().reset_index()
        remarks_mach.columns = ["Machine No.", "Remarks Count"]
        st.plotly_chart(px.bar(remarks_mach, x="Machine No.", y="Remarks Count"), use_container_width=True)

# ---------- Hourly Breakdown ----------
with tabs[6]:
    if ("Hour" in df_view.columns) and ("Machine No." in df_view.columns):
        hour_jobs = df_view.groupby("Hour")["Machine No."].count().reset_index()
        hour_jobs.columns = ["Hour", "Jobs"]
        st.plotly_chart(px.bar(hour_jobs, x="Hour", y="Jobs"), use_container_width=True)
    else:
        st.info("Hour or Machine No. missing.")

# ---------- Raw Data ----------
with tabs[7]:
    st.dataframe(df_view, use_container_width=True)
