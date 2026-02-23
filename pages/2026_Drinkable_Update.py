import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# ----------------- PAGE CONFIG -----------------
st.set_page_config(page_title="2026 – Drinkable Section Current Update", layout="wide")
st.title("2026 – Drinkable Section Current Update")

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "maintenance_data.xlsx")


# ----------------- SAFE HELPERS -----------------

def safe_col(df, col, default=""):
    """Return a column safely. If missing, return empty column."""
    if col in df.columns:
        return df[col]
    return pd.Series([default] * len(df))


def safe_time(series):
    """Convert to datetime safely."""
    return pd.to_datetime(series, errors="coerce")


def safe_timedelta(series):
    """Convert to timedelta safely."""
    td = pd.to_timedelta(series, errors="coerce")
    td = td.fillna(pd.Timedelta(seconds=0))
    return td


# ----------------- CLEANING -----------------

def clean_data(df):
    df.columns = [c.strip() for c in df.columns]

    # Date
    df["Date"] = safe_time(safe_col(df, "Date"))

    # Time fields
    df["Requested Time"] = safe_time(safe_col(df, "Requested Time"))
    df["Start"] = safe_time(safe_col(df, "Start"))
    df["End"] = safe_time(safe_col(df, "End"))

    # Time Consumed
    df["Time Consumed"] = safe_timedelta(safe_col(df, "Time Consumed"))

    # Minutes
    df["Minutes"] = df["Time Consumed"].dt.total_seconds() / 60

    # Hour
    df["Hour"] = df["Requested Time"].dt.hour
    df["Hour"] = df["Hour"].fillna(df["Start"].dt.hour)
    df["Hour"] = df["Hour"].fillna(0).astype(int)

    return df


# ----------------- TECHNICIAN SPLIT -----------------

def explode_tech(df):
    perf = safe_col(df, "Performed By").fillna("").astype(str)

    perf = (
        perf.str.replace(" and ", "/", case=False)
        .str.replace("&", "/", case=False)
    )

    df["Tech_List"] = perf.str.split("/")
    df2 = df.explode("Tech_List")
    df2["Tech_List"] = df2["Tech_List"].astype(str).str.strip()
    df2 = df2[df2["Tech_List"] != ""]
    return df2


# ----------------- LOAD DATA -----------------

def load_data():
    if os.path.exists(DATA_PATH):
        return pd.read_excel(DATA_PATH)
    return None


uploaded = st.file_uploader("Upload updated Excel", type=["xlsx", "xls"])
saved_df = load_data()

if uploaded:
    saved_df = pd.read_excel(uploaded)
    saved_df.to_excel(DATA_PATH, index=False)
    st.success("File saved permanently.")

if saved_df is None:
    st.warning("No saved data found.")
    st.stop()

df = clean_data(saved_df.copy())
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
tech_list = sorted(df_tech["Tech_List"].dropna().astype(str).unique()) if not df_tech.empty else []

machine_filter = st.sidebar.multiselect("Machine", machine_list)
shift_filter = st.sidebar.multiselect("Shift", shift_list)
job_filter = st.sidebar.multiselect("Job", job_list)
area_filter = st.sidebar.multiselect("Area", area_list)
tech_filter = st.sidebar.multiselect("Technician", tech_list)

df_view = df.copy()

if machine_filter and "Machine No." in df_view.columns:
    df_view = df_view[df_view["Machine No."].astype(str).isin(machine_filter)]
if shift_filter and "Shift" in df_view.columns:
    df_view = df_view[df_view["Shift"].astype(str).isin(shift_filter)]
if job_filter and "Job" in df_view.columns:
    df_view = df_view[df_view["Job"].astype(str).isin(job_filter)]
if area_filter and "Machine Classification" in df_view.columns:
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
        st.plotly_chart(px.bar(freq, x="Machine No.", y="Jobs", title="Jobs per Machine"), use_container_width=True)

# ---------- Technician Performance ----------
with tabs[1]:
    if df_tech_view.empty:
        st.info("No technician data.")
    else:
        tech = df_tech_view.groupby("Tech_List")["Minutes"].sum().reset_index()
        tech.columns = ["Technician", "Total Minutes"]
        st.plotly_chart(px.bar(tech, x="Technician", y="Total Minutes", title="Technician Performance"), use_container_width=True)

        tech_date = df_tech_view.groupby(["Tech_List", "Date"])["Minutes"].sum().reset_index()
        tech_date.columns = ["Technician", "Date", "Total Minutes"]
        st.subheader("Technician Performance – Date-wise")
        st.dataframe(tech_date, use_container_width=True)

# ---------- Job Type ----------
with tabs[2]:
    col = safe_col(df_view, "Job")
    if col.empty:
        st.info("No Job data.")
    else:
        job_counts = col.value_counts().reset_index()
        job_counts.columns = ["Job", "Count"]
        st.plotly_chart(px.bar(job_counts, x="Job", y="Count", title="Jobs by Job Type"), use_container_width=True)

# ---------- Spare Parts ----------
with tabs[3]:
    spare = safe_col(df_view, "Spare Part Used").fillna("").astype(str)
    spare = spare[spare.str.strip() != ""]
    if spare.empty:
        st.info("No spare parts used.")
    else:
        spare_counts = spare.value_counts().reset_index()
        spare_counts.columns = ["Spare Part", "Count"]
        st.plotly_chart(px.bar(spare_counts, x="Spare Part", y="Count", title="Spare Parts Usage"), use_container_width=True)
        st.dataframe(spare_counts, use_container_width=True)

# ---------- Notifications ----------
with tabs[4]:
    notif = safe_col(df_view, "Notification No.")
    mach = safe_col(df_view, "Machine No.")
    if notif.empty or mach.empty:
        st.info("No notifications data.")
    else:
        notif_mach = df_view.groupby("Machine No.")["Notification No."].nunique().reset_index()
        notif_mach.columns = ["Machine No.", "Unique Notifications"]
        st.plotly_chart(px.bar(notif_mach, x="Machine No.", y="Unique Notifications", title="Notifications per Machine"), use_container_width=True)

# ---------- Remarks ----------
with tabs[5]:
    remarks = safe_col(df_view, "Remarks").astype(str)
    remarks = remarks[remarks.str.strip() != ""]
    if remarks.empty:
        st.info("No remarks.")
    else:
        if "Machine No." in df_view.columns:
            remarks_mach = df_view[df_view["Remarks"].astype(str).str.strip() != ""]["Machine No."].value_counts().reset_index()
            remarks_mach.columns = ["Machine No.", "Remarks Count"]
            st.plotly_chart(px.bar(remarks_mach, x="Machine No.", y="Remarks Count", title="Remarks per Machine"), use_container_width=True)
            st.dataframe(remarks_mach, use_container_width=True)
        else:
            st.info("Machine No. column not available for remarks summary.")

# ---------- Hourly Breakdown ----------
with tabs[6]:
    if "Hour" in df_view.columns and "Machine No." in df_view.columns:
        hour_jobs = df_view.groupby("Hour")["Machine No."].count().reset_index()
        hour_jobs.columns = ["Hour", "Jobs"]
        st.plotly_chart(px.bar(hour_jobs, x="Hour", y="Jobs", title="Breakdowns by Hour"), use_container_width=True)
    else:
        st.info("Hour or Machine No. data not available for hourly breakdown.")

# ---------- Raw Data ----------
with tabs[7]:
    st.dataframe(df_view, use_container_width=True)
