import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
import os
from datetime import datetime

# ----------------- PAGE CONFIG -----------------

st.set_page_config(page_title="2026 – Drinkable Section Current Update", layout="wide")

st.title("2026 – Drinkable Section Current Update")
st.write("MTD / YTD view, technician performance, and breakdown analysis based on the current maintenance sheet.")

# Permanent saved data path
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "maintenance_data.xlsx")


# ----------------- HELPER FUNCTIONS -----------------

def safe_get(df, col):
    """Return column if exists, else return a column of NaT."""
    if col in df.columns:
        return df[col]
    return pd.Series([pd.NaT] * len(df))


def parse_time_column(series):
    """Universal time parser."""
    return pd.to_datetime(series, errors="coerce")


def clean_time_and_date(df):
    """Clean Date and time columns safely."""
    df.columns = [c.strip() for c in df.columns]

    # Parse Date
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce", dayfirst=True)
    else:
        df["Date"] = pd.NaT

    # Parse Requested Time, Start, End safely
    df["Requested Time"] = parse_time_column(safe_get(df, "Requested Time"))
    df["Start"] = parse_time_column(safe_get(df, "Start"))
    df["End"] = parse_time_column(safe_get(df, "End"))

    # Parse Time Consumed safely
    if "Time Consumed" in df.columns:
        df["Time Consumed"] = pd.to_timedelta(df["Time Consumed"], errors="coerce")
        df["Time Consumed"] = df["Time Consumed"].fillna(
            pd.to_timedelta(df["Time Consumed"].astype(str), errors="coerce")
        )
        df["Time Consumed"] = df["Time Consumed"].fillna(pd.Timedelta(seconds=0))
    else:
        df["Time Consumed"] = pd.Timedelta(seconds=0)

    # Minutes
    df["Minutes"] = df["Time Consumed"].dt.total_seconds() / 60

    # Hour extraction (fallback logic)
    df["Hour"] = df["Requested Time"].dt.hour
    df.loc[df["Hour"].isna(), "Hour"] = df["Start"].dt.hour

    df["Hour"] = df["Hour"].fillna(0).astype(int)

    return df


def explode_technicians(df):
    """Split technicians by '/', 'and', '&'."""
    if "Performed By" not in df.columns:
        df["Performed By"] = ""

    df["Performed By"] = df["Performed By"].fillna("").astype(str)

    df["Performed_By_Normalized"] = (
        df["Performed By"]
        .str.replace(" and ", "/", case=False)
        .str.replace("&", "/", case=False)
    )

    df["Tech_List"] = df["Performed_By_Normalized"].str.split("/")

    df_exploded = df.explode("Tech_List")
    df_exploded["Tech_List"] = df_exploded["Tech_List"].astype(str).str.strip()
    df_exploded = df_exploded[df_exploded["Tech_List"] != ""]
    return df_exploded


def load_saved_data():
    if os.path.exists(DATA_PATH):
        return pd.read_excel(DATA_PATH)
    return None


def save_data(df):
    df.to_excel(DATA_PATH, index=False)


def filter_mtd_ytd(df, mode):
    if "Date" not in df.columns:
        return df

    today = datetime.today()

    if mode == "MTD":
        return df[df["Date"].dt.month == today.month]

    if mode == "YTD":
        return df[df["Date"].dt.year == today.year]

    return df


# ----------------- LOAD BASE DATA -----------------

saved_df = load_saved_data()

uploaded_file = st.file_uploader(
    "Upload updated maintenance Excel (to replace current data for 2026 view)",
    type=["xlsx", "xls"]
)

if uploaded_file is not None:
    base_df = pd.read_excel(uploaded_file)
    save_data(base_df)
    st.success("New file uploaded and saved permanently for 2026 view.")
    saved_df = base_df

if saved_df is None:
    st.info("No saved data found yet. Please upload the first Excel file.")
    st.stop()

# Clean data
df = clean_time_and_date(saved_df.copy())
df_tech = explode_technicians(df.copy())


# ----------------- MTD / YTD FILTER CONTROLS -----------------

st.markdown("---")
col_mtd, col_ytd, col_all = st.columns([1, 1, 1])

filter_mode = "ALL"

with col_mtd:
    if st.button("MTD (Month-to-Date)"):
        filter_mode = "MTD"
with col_ytd:
    if st.button("YTD (Year-to-Date)"):
        filter_mode = "YTD"
with col_all:
    if st.button("Show All"):
        filter_mode = "ALL"

df = filter_mtd_ytd(df, filter_mode)
df_tech = filter_mtd_ytd(df_tech, filter_mode)


# ----------------- SIDEBAR FILTERS -----------------

st.sidebar.header("Filters")

machine_list = sorted(df["Machine No."].dropna().astype(str).unique()) if "Machine No." in df.columns else []
shift_list = sorted(df["Shift"].dropna().astype(str).unique()) if "Shift" in df.columns else []
job_list = sorted(df["Job"].dropna().astype(str).unique()) if "Job" in df.columns else []
area_list = sorted(df["Machine Classification"].dropna().astype(str).unique()) if "Machine Classification" in df.columns else []
tech_list = sorted(df_tech["Tech_List"].dropna().astype(str).unique()) if not df_tech.empty else []

machine_filter = st.sidebar.multiselect("Machine", machine_list)
shift_filter = st.sidebar.multiselect("Shift", shift_list)
job_filter = st.sidebar.multiselect("Job", job_list)
area_filter = st.sidebar.multiselect("Machine Classification", area_list)
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

st.markdown("---")
st.subheader("Dashboards – 2026 Drinkable Section")

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "Machine Breakdown Frequency",
    "Technician Performance",
    "Job Type Analysis",
    "Spare Parts Usage",
    "Notification Analysis",
    "Remarks Summary",
    "Hourly Breakdown",
    "Raw Data",
])

# ---------- Tab 1 ----------
with tab1:
    freq = df_view["Machine No."].astype(str).value_counts().reset_index()
    freq.columns = ["Machine No.", "Jobs"]
    st.plotly_chart(px.bar(freq, x="Machine No.", y="Jobs", title="Jobs per Machine"), use_container_width=True)

# ---------- Tab 2 ----------
with tab2:
    if not df_tech_view.empty:
        tech = df_tech_view.groupby("Tech_List")["Minutes"].sum().reset_index()
        tech.columns = ["Technician", "Total Minutes"]
        st.plotly_chart(px.bar(tech, x="Technician", y="Total Minutes", title="Technician Performance"), use_container_width=True)

        tech_date = (
            df_tech_view.groupby(["Tech_List", "Date"])["Minutes"]
            .sum()
            .reset_index()
            .sort_values(["Tech_List", "Date"])
        )
        tech_date.columns = ["Technician", "Date", "Total Minutes"]

        st.subheader("Technician Performance – Date-wise")
        st.dataframe(tech_date, use_container_width=True)

# ---------- Tab 3 ----------
with tab3:
    job_counts = df_view["Job"].value_counts().reset_index()
    job_counts.columns = ["Job", "Jobs"]
    st.plotly_chart(px.bar(job_counts, x="Job", y="Jobs", title="Jobs by Job Type"), use_container_width=True)

    type_counts = df_view["Type"].value_counts().reset_index()
    type_counts.columns = ["Type", "Jobs"]
    st.plotly_chart(px.bar(type_counts, x="Type", y="Jobs", title="Jobs by Type (Mech/Elect)"), use_container_width=True)

# ---------- Tab 4 ----------
with tab4:
    spare = df_view["Spare Part Used"].fillna("").astype(str)
    spare = spare[spare.str.strip() != ""]
    if not spare.empty:
        spare_counts = spare.value_counts().reset_index()
        spare_counts.columns = ["Spare Part", "Usage Count"]
        st.plotly_chart(px.bar(spare_counts, x="Spare Part", y="Usage Count", title="Spare Parts Usage"), use_container_width=True)
        st.dataframe(spare_counts, use_container_width=True)
    else:
        st.info("No spare parts usage recorded.")

# ---------- Tab 5 ----------
with tab5:
    notif_machine = (
        df_view.groupby("Machine No.")["Notification No."]
        .nunique()
        .reset_index()
    )
    notif_machine.columns = ["Machine No.", "Unique Notifications"]
    st.plotly_chart(px.bar(notif_machine, x="Machine No.", y="Unique Notifications", title="Notifications per Machine"), use_container_width=True)

    if "Date" in df_view.columns:
        notif_date = (
            df_view.groupby("Date")["Notification No."]
            .nunique()
            .reset_index()
            .sort_values("Date")
        )
        notif_date.columns = ["Date", "Unique Notifications"]
        st.plotly_chart(px.line(notif_date, x="Date", y="Unique Notifications", title="Notifications per Date"), use_container_width=True)

# ---------- Tab 6 ----------
with tab6:
    remarks_nonempty = df_view[df_view["Remarks"].astype(str).str.strip() != ""]
    if not remarks_nonempty.empty:
        remarks_mach = remarks_nonempty["Machine No."].astype(str).value_counts().reset_index()
        remarks_mach.columns = ["Machine No.", "Remarks Count"]
        st.plotly_chart(px.bar(remarks_mach, x="Machine No.", y="Remarks Count", title="Remarks per Machine"), use_container_width=True)
        st.dataframe(remarks_mach, use_container_width=True)
    else:
        st.info("No remarks recorded.")

# ---------- Tab 7 ----------
with tab7:
    all_hours = pd.DataFrame({"Hour": range(24)})
    hour_jobs = df_view.groupby("Hour")["Machine No."].count().reset_index()
    hour_jobs.columns = ["Hour", "Jobs"]
    hour_jobs = all_hours.merge(hour_jobs, on="Hour", how="left").fillna(0)

    st.plotly_chart(px.bar(hour_jobs, x="Hour", y="Jobs", title="Breakdowns by Hour (0–23)"), use_container_width=True)

    max_row = hour_jobs.loc[hour_jobs["Jobs"].idxmax()]
    st.info(f"Highest breakdowns at hour **{int(max_row['Hour'])}:00** with **{int(max_row['Jobs'])}** jobs.")

# ---------- Tab 8 ----------
with tab8:
    st.dataframe(df_view, use_container_width=True)
