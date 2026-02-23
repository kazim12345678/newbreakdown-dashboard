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

def parse_time_column(series: pd.Series) -> pd.Series:
    """Universal time parser for all formats."""
    return pd.to_datetime(series, errors="coerce")


def clean_time_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Clean time columns and extract hour + minutes based on your sheet format."""
    df.columns = [c.strip() for c in df.columns]

    # Parse time-related columns
    for col in ["Requested Time", "Start", "End"]:
        if col in df.columns:
            df[col] = parse_time_column(df[col])

    # Time Consumed
    if "Time Consumed" in df.columns:
        df["Time Consumed"] = pd.to_timedelta(df["Time Consumed"], errors="coerce")
    else:
        df["Time Consumed"] = pd.NaT

    # Auto-calc Time Consumed if missing but Start/End exist
    if {"Start", "End"}.issubset(df.columns):
        mask = df["Time Consumed"].isna() & df["Start"].notna() & df["End"].notna()
        df.loc[mask, "Time Consumed"] = df.loc[mask, "End"] - df.loc[mask, "Start"]

    # Minutes
    df["Minutes"] = df["Time Consumed"].dt.total_seconds() / 60

    # Hour from Requested Time (fallback to Start)
    if "Requested Time" in df.columns:
        df["Hour"] = pd.to_datetime(df["Requested Time"], errors="coerce").dt.hour
    else:
        df["Hour"] = pd.to_datetime(df["Start"], errors="coerce").dt.hour

    return df


def explode_technicians(df: pd.DataFrame) -> pd.DataFrame:
    """Split 'Performed By' into multiple rows so each technician is counted."""
    if "Performed By" not in df.columns:
        df["Performed By"] = ""

    df["Performed By"] = df["Performed By"].fillna("")
    df["Tech_List"] = df["Performed By"].astype(str).str.split("/")

    df_exploded = df.explode("Tech_List")
    df_exploded["Tech_List"] = df_exploded["Tech_List"].astype(str).str.strip()
    df_exploded = df_exploded[df_exploded["Tech_List"] != ""]
    return df_exploded


def download_excel(df: pd.DataFrame) -> bytes:
    """Return Excel bytes for download."""
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Data")
    return output.getvalue()


def load_saved_data() -> pd.DataFrame | None:
    """Load saved Excel if exists."""
    if os.path.exists(DATA_PATH):
        return pd.read_excel(DATA_PATH)
    return None


def save_data(df: pd.DataFrame):
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

# Clean data according to your sheet format
df = clean_time_columns(saved_df.copy())
df_tech = explode_technicians(df.copy())

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
if machine_filter and "Machine No." in df_tech_view.columns:
    df_tech_view = df_tech_view[df_tech_view["Machine No."].astype(str).isin(machine_filter)]
if shift_filter and "Shift" in df_tech_view.columns:
    df_tech_view = df_tech_view[df_tech_view["Shift"].astype(str).isin(shift_filter)]


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

# ---------- Tab 1: Machine Breakdown Frequency ----------
with tab1:
    if "Machine No." in df_view.columns:
        freq = df_view["Machine No."].astype(str).value_counts().reset_index()
        freq.columns = ["Machine No.", "Jobs"]
        fig_mach = px.bar(
            freq,
            x="Machine No.",
            y="Jobs",
            title="Jobs per Machine",
        )
        st.plotly_chart(fig_mach, use_container_width=True)
    else:
        st.warning("Column 'Machine No.' not found in data.")

# ---------- Tab 2: Technician Performance ----------
with tab2:
    if not df_tech_view.empty:
        tech = df_tech_view.groupby("Tech_List")["Minutes"].sum().reset_index()
        tech.columns = ["Technician", "Total Minutes"]
        fig_tech = px.bar(
            tech,
            x="Technician",
            y="Total Minutes",
            title="Technician Performance (Minutes)",
        )
        st.plotly_chart(fig_tech, use_container_width=True)
    else:
        st.warning("No technician data available (Performed By column may be empty).")

# ---------- Tab 3: Shift Analysis ----------
with tab3:
    if "Shift" in df_view.columns:
        shift_jobs = df_view["Shift"].value_counts().reset_index()
        shift_jobs.columns = ["Shift", "Jobs"]

        if "Minutes" in df_view.columns:
            shift_minutes = df_view.groupby("Shift")["Minutes"].sum().reset_index()
            shift_minutes.columns = ["Shift", "Total Minutes"]
        else:
            shift_minutes = pd.DataFrame(columns=["Shift", "Total Minutes"])

        col_s1, col_s2 = st.columns(2)
        with col_s1:
            fig_shift_jobs = px.bar(
                shift_jobs,
                x="Shift",
                y="Jobs",
                title="Jobs per Shift",
            )
            st.plotly_chart(fig_shift_jobs, use_container_width=True)
        with col_s2:
            if not shift_minutes.empty:
                fig_shift_min = px.bar(
                    shift_minutes,
                    x="Shift",
                    y="Total Minutes",
                    title="Total Minutes per Shift",
                )
                st.plotly_chart(fig_shift_min, use_container_width=True)
            else:
                st.info("No minutes data available for shift analysis.")
    else:
        st.warning("Column 'Shift' not found in data.")

# ---------- Tab 4: Job Type Analysis ----------
with tab4:
    col_j1, col_j2 = st.columns(2)

    if "Job" in df_view.columns:
        job_counts = df_view["Job"].value_counts().reset_index()
        job_counts.columns = ["Job", "Jobs"]
        with col_j1:
            fig_job = px.bar(
                job_counts,
                x="Job",
                y="Jobs",
                title="Jobs by Job",
            )
            st.plotly_chart(fig_job, use_container_width=True)
    else:
        st.warning("Column 'Job' not found in data.")

    if "Type" in df_view.columns:
        type_counts = df_view["Type"].value_counts().reset_index()
        type_counts.columns = ["Type", "Jobs"]
        with col_j2:
            fig_type = px.bar(
                type_counts,
                x="Type",
                y="Jobs",
                title="Jobs by Type (Mech/Elect)",
            )
            st.plotly_chart(fig_type, use_container_width=True)
    else:
        st.info("Column 'Type' (Mech/Elect) not found in data.")

# ---------- Tab 5: Hourly Breakdown ----------
with tab5:
    all_hours = pd.DataFrame({"Hour": range(24)})

    if "Hour" in df_view.columns and "Machine No." in df_view.columns:
        hour_jobs = df_view.groupby("Hour")["Machine No."].count().reset_index()
        hour_jobs.columns = ["Hour", "Jobs"]
        hour_jobs = all_hours.merge(hour_jobs, on="Hour", how="left").fillna(0)

        fig_hour_jobs = px.bar(
            hour_jobs,
            x="Hour",
            y="Jobs",
            title="Jobs by Hour of Day (0–23)",
        )
        st.plotly_chart(fig_hour_jobs, use_container_width=True)
    else:
        st.warning("Hour or Machine No. column not available. Check time parsing and column names.")

# ---------- Tab 6: Area / Classification ----------
with tab6:
    if "Machine Classification" in df_view.columns:
        area_jobs = df_view["Machine Classification"].value_counts().reset_index()
        area_jobs.columns = ["Area", "Jobs"]

        if "Minutes" in df_view.columns:
            area_minutes = df_view.groupby("Machine Classification")["Minutes"].sum().reset_index()
            area_minutes.columns = ["Area", "Minutes"]
        else:
            area_minutes = pd.DataFrame(columns=["Area", "Minutes"])

        col_a1, col_a2 = st.columns(2)
        with col_a1:
            fig_area_jobs = px.bar(
                area_jobs,
                x="Area",
                y="Jobs",
                title="Jobs by Area",
            )
            st.plotly_chart(fig_area_jobs, use_container_width=True)
        with col_a2:
            if not area_minutes.empty:
                fig_area_min = px.bar(
                    area_minutes,
                    x="Area",
                    y="Minutes",
                    title="Minutes by Area",
                )
                st.plotly_chart(fig_area_min, use_container_width=True)
            else:
                st.info("No minutes data available for area analysis.")
    else:
        st.warning("Column 'Machine Classification' not found in data.")

# ---------- Tab 7: Raw Data ----------
with tab7:
    st.write("Cleaned raw data (after time processing):")
    st.dataframe(df_view, use_container_width=True)
