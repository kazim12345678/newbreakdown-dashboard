import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
import os

# ----------------- PAGE CONFIG -----------------

st.set_page_config(page_title="Maintenance Daily Report Dashboard", layout="wide")

st.title("Maintenance Daily Report Dashboard")
st.write("Upload or edit the daily maintenance data. The latest saved data will be reused automatically.")

# Permanent saved data path (Option 1)
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "maintenance_data.xlsx")


# ----------------- HELPER FUNCTIONS -----------------

def parse_time_column(series):
    """Universal time parser for all formats."""
    return pd.to_datetime(series, errors="coerce")


def clean_time_columns(df):
    """Clean time columns and extract hour + minutes."""
    df.columns = [c.strip() for c in df.columns]

    # Parse time columns
    for col in ["Requested Time", "Start", "End"]:
        if col in df.columns:
            df[col] = parse_time_column(df[col])

    # Time Consumed
    if "Time Consumed" in df.columns:
        df["Time Consumed"] = pd.to_timedelta(df["Time Consumed"], errors="coerce")
    else:
        df["Time Consumed"] = pd.NaT

    # Auto-calc Time Consumed
    if {"Start", "End"}.issubset(df.columns):
        mask = df["Time Consumed"].isna() & df["Start"].notna() & df["End"].notna()
        df.loc[mask, "Time Consumed"] = df.loc[mask, "End"] - df.loc[mask, "Start"]

    # Minutes
    df["Minutes"] = df["Time Consumed"].dt.total_seconds() / 60

    # Hour extraction
    if "Requested Time" in df.columns:
        df["Hour"] = pd.to_datetime(df["Requested Time"], errors="coerce").dt.hour
    else:
        df["Hour"] = pd.to_datetime(df["Start"], errors="coerce").dt.hour

    return df


def explode_technicians(df):
    """Split 'Performed By' into multiple rows."""
    if "Performed By" not in df.columns:
        df["Performed By"] = ""

    df["Performed By"] = df["Performed By"].fillna("")
    df["Tech_List"] = df["Performed By"].astype(str).str.split("/")
    df_exploded = df.explode("Tech_List")
    df_exploded["Tech_List"] = df_exploded["Tech_List"].astype(str).strip()
    df_exploded = df_exploded[df_exploded["Tech_List"] != ""]
    return df_exploded


def download_excel(df):
    """Return Excel bytes for download."""
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Data")
    return output.getvalue()


def load_saved_data():
    """Load saved Excel if exists."""
    if os.path.exists(DATA_PATH):
        return pd.read_excel(DATA_PATH)
    return None


def save_data(df):
    """Save dataframe permanently."""
    df.to_excel(DATA_PATH, index=False)


# ----------------- LOAD BASE DATA -----------------

saved_df = load_saved_data()

uploaded_file = st.file_uploader(
    "Upload daily maintenance Excel (to replace current data)",
    type=["xlsx", "xls"]
)

if uploaded_file is not None:
    base_df = pd.read_excel(uploaded_file)
    save_data(base_df)
    st.success("New file uploaded and saved permanently.")
    saved_df = base_df

if saved_df is None:
    st.info("No saved data found yet. Please upload the first Excel file.")
    st.stop()

# Clean data
df = clean_time_columns(saved_df.copy())
df_tech = explode_technicians(df.copy())

# ----------------- SESSION STATE -----------------

if "editable_df" not in st.session_state:
    st.session_state["editable_df"] = df.copy()


# ----------------- SIDEBAR FILTERS -----------------

st.sidebar.header("Filters")

machine_list = sorted(df["Machine No."].dropna().astype(str).unique()) if "Machine No." in df.columns else []
shift_list = sorted(df["ARIA"].dropna().astype(str).unique()) if "ARIA" in df.columns else []
jobtype_list = sorted(df["Job TYPE"].dropna().astype(str).unique()) if "Job TYPE" in df.columns else []
area_list = sorted(df["Machine Classification"].dropna().astype(str).unique()) if "Machine Classification" in df.columns else []
tech_list = sorted(df_tech["Tech_List"].dropna().astype(str).unique()) if not df_tech.empty else []

machine_filter = st.sidebar.multiselect("Machine", machine_list)
shift_filter = st.sidebar.multiselect("Shift (ARIA)", shift_list)
jobtype_filter = st.sidebar.multiselect("Job TYPE", jobtype_list)
area_filter = st.sidebar.multiselect("Area / Machine Classification", area_list)
tech_filter = st.sidebar.multiselect("Technician", tech_list)

df_view = df.copy()
if machine_filter:
    df_view = df_view[df_view["Machine No."].astype(str).isin(machine_filter)]
if shift_filter:
    df_view = df_view[df_view["ARIA"].astype(str).isin(shift_filter)]
if jobtype_filter:
    df_view = df_view[df_view["Job TYPE"].astype(str).isin(jobtype_filter)]
if area_filter:
    df_view = df_view[df_view["Machine Classification"].astype(str).isin(area_filter)]

df_tech_view = df_tech.copy()
if tech_filter:
    df_tech_view = df_tech_view[df_tech_view["Tech_List"].astype(str).isin(tech_filter)]


# ----------------- DASHBOARDS -----------------

st.subheader("Dashboards")

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Machine Breakdown Frequency",
    "Technician Performance",
    "Shift Analysis",
    "Job Type Analysis",
    "Hourly Breakdown",
    "Area / Classification",
    "Raw Data",
])

# ---------- Tab 1 ----------
with tab1:
    freq = df_view["Machine No."].astype(str).value_counts().reset_index()
    freq.columns = ["Machine No.", "Jobs"]
    st.plotly_chart(px.bar(freq, x="Machine No.", y="Jobs", title="Jobs per Machine"), use_container_width=True)

# ---------- Tab 2 ----------
with tab2:
    tech = df_tech_view.groupby("Tech_List")["Minutes"].sum().reset_index()
    tech.columns = ["Technician", "Total Minutes"]
    st.plotly_chart(px.bar(tech, x="Technician", y="Total Minutes", title="Technician Performance"), use_container_width=True)

# ---------- Tab 3 ----------
with tab3:
    shift_jobs = df_view["ARIA"].value_counts().reset_index()
    shift_jobs.columns = ["Shift", "Jobs"]

    shift_minutes = df_view.groupby("ARIA")["Minutes"].sum().reset_index()
    shift_minutes.columns = ["Shift", "Total Minutes"]

    col1, col2 = st.columns(2)
    col1.plotly_chart(px.bar(shift_jobs, x="Shift", y="Jobs", title="Jobs per Shift"), use_container_width=True)
    col2.plotly_chart(px.bar(shift_minutes, x="Shift", y="Total Minutes", title="Minutes per Shift"), use_container_width=True)

# ---------- Tab 4 ----------
with tab4:
    col1, col2 = st.columns(2)

    job_counts = df_view["Job TYPE"].value_counts().reset_index()
    job_counts.columns = ["Job TYPE", "Jobs"]
    col1.plotly_chart(px.bar(job_counts, x="Job TYPE", y="Jobs", title="Jobs by Job TYPE"), use_container_width=True)

    type_counts = df_view["Type"].value_counts().reset_index()
    type_counts.columns = ["Type", "Jobs"]
    col2.plotly_chart(px.bar(type_counts, x="Type", y="Jobs", title="Jobs by Type"), use_container_width=True)

# ---------- Tab 5 ----------
with tab5:
    all_hours = pd.DataFrame({"Hour": range(24)})
    hour_jobs = df_view.groupby("Hour")["Machine No."].count().reset_index()
    hour_jobs = all_hours.merge(hour_jobs, on="Hour", how="left").fillna(0)
    st.plotly_chart(px.bar(hour_jobs, x="Hour", y="Jobs", title="Jobs by Hour (0–23)"), use_container_width=True)

# ---------- Tab 6 ----------
with tab6:
    area_jobs = df_view["Machine Classification"].value_counts().reset_index()
    area_jobs.columns = ["Area", "Jobs"]

    area_minutes = df_view.groupby("Machine Classification")["Minutes"].sum().reset_index()
    area_minutes.columns = ["Area", "Minutes"]

    col1, col2 = st.columns(2)
    col1.plotly_chart(px.bar(area_jobs, x="Area", y="Jobs", title="Jobs by Area"), use_container_width=True)
    col2.plotly_chart(px.bar(area_minutes, x="Area", y="Minutes", title="Minutes by Area"), use_container_width=True)

# ---------- Tab 7 ----------
with tab7:
    st.dataframe(df_view, use_container_width=True)
