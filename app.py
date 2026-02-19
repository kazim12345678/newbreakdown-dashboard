import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ================================
# CONFIG
# ================================
st.set_page_config(
    page_title="NADEC Maintenance Breakdown Dashboard",
    layout="wide"
)

DATA_FILE = "breakdown_log.csv"

MACHINES = [f"M{i}" for i in range(1, 19)]

# ================================
# AUTO COLUMN FIX FUNCTION
# ================================
def standardize_columns(df):
    """
    Fix wrong/missing column names automatically
    """

    df.columns = [c.strip() for c in df.columns]

    mapping = {
        "Machine": "Machine No",
        "MachineNo": "Machine No",
        "Line": "Machine No",

        "Technician": "Performed By",
        "Technician Name": "Performed By",
        "Engineer": "Performed By",

        "Duration": "Time Consumed",
        "TimeTaken": "Time Consumed",
        "Downtime": "Time Consumed",

        "Category": "Breakdown Category",
        "Type": "Job Type",

        "Problem": "Reported Problem",
        "Work Done": "Description of Work",
    }

    df.rename(columns=mapping, inplace=True)

    required_cols = [
        "Date",
        "Machine No",
        "Shift",
        "Machine Classification",
        "Job Type",
        "Breakdown Category",
        "Reported Problem",
        "Description of Work",
        "Start Time",
        "End Time",
        "Time Consumed",
        "Performed By"
    ]

    # Add missing columns
    for col in required_cols:
        if col not in df.columns:
            df[col] = ""

    return df


# ================================
# TIME CONVERSION
# ================================
def time_to_minutes(t):
    try:
        if pd.isna(t) or str(t).strip() == "":
            return 0
        parts = str(t).split(":")
        if len(parts) == 3:
            h, m, s = parts
            return int(h) * 60 + int(m)
        elif len(parts) == 2:
            m, s = parts
            return int(m)
        return 0
    except:
        return 0


# ================================
# LOAD DATA
# ================================
def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df = standardize_columns(df)
        return df
    else:
        return pd.DataFrame(columns=[
            "Date", "Machine No", "Shift",
            "Machine Classification", "Job Type",
            "Breakdown Category", "Reported Problem",
            "Description of Work", "Start Time",
            "End Time", "Time Consumed", "Performed By"
        ])


# ================================
# SAVE DATA
# ================================
def save_data(df):
    df.to_csv(DATA_FILE, index=False)


# ================================
# APP TITLE
# ================================
st.markdown(
    """
    <h1 style='text-align:center;color:#003366;'>
    KUTE Dashboard (Kazim Utilization Team Efficiency)
    </h1>
    """,
    unsafe_allow_html=True
)

st.write("### NADEC Style Maintenance Breakdown Monitoring System")

# ================================
# LOAD EXISTING DATA
# ================================
df = load_data()

# ================================
# SIDEBAR UPLOAD EXCEL
# ================================
st.sidebar.header("📤 Upload Daily Excel File")

uploaded = st.sidebar.file_uploader(
    "Upload Breakdown Excel",
    type=["xlsx", "csv"]
)

if uploaded:
    try:
        if uploaded.name.endswith(".csv"):
            new_df = pd.read_csv(uploaded)
        else:
            new_df = pd.read_excel(uploaded)

        new_df = standardize_columns(new_df)

        df = pd.concat([df, new_df], ignore_index=True)
        save_data(df)

        st.sidebar.success("✅ File Uploaded & Saved Successfully!")

    except Exception as e:
        st.sidebar.error("Upload Failed")
        st.sidebar.write(e)

# ================================
# KPI SUMMARY
# ================================
st.markdown("## 📊 KPI Summary")

total_events = len(df)

total_minutes = df["Time Consumed"].apply(time_to_minutes).sum()
total_hours = round(total_minutes / 60, 2)

worst_machine = "N/A"
if total_events > 0:
    worst_machine = (
        df.groupby("Machine No")["Time Consumed"]
        .apply(lambda x: x.apply(time_to_minutes).sum())
        .idxmax()
    )

col1, col2, col3 = st.columns(3)

col1.metric("Total Breakdown Events", total_events)
col2.metric("Total Downtime Hours", total_hours)
col3.metric("Worst Machine", worst_machine)

# ================================
# MACHINE WISE BAR CHART
# ================================
st.markdown("## 🚦 Machine Breakdown Status (M1–M18)")

machine_summary = (
    df.groupby("Machine No")["Time Consumed"]
    .apply(lambda x: x.apply(time_to_minutes).sum())
    .reindex(MACHINES, fill_value=0)
)

st.bar_chart(machine_summary)

# ================================
# ADD NEW ENTRY FORM
# ================================
st.markdown("## ➕ Add Breakdown Entry")

with st.expander("Click Here to Add Entry"):

    with st.form("entry_form"):

        date = st.date_input("Date", datetime.today())

        machine = st.selectbox("Machine No", MACHINES)

        shift = st.selectbox("Shift", ["Day", "Night"])

        classification = st.text_input("Machine Classification")

        job_type = st.selectbox("Job Type", ["B/D", "Corrective"])

        category = st.selectbox(
            "Breakdown Category",
            ["Mechanical", "Electrical", "Automation"]
        )

        problem = st.text_area("Reported Problem")

        work = st.text_area("Description of Work")

        start = st.text_input("Start Time (HH:MM)")
        end = st.text_input("End Time (HH:MM)")

        time_consumed = st.text_input("Time Consumed (HH:MM:SS)", "00:10:00")

        technician = st.text_input("Performed By")

        submitted = st.form_submit_button("✅ Save Entry")

        if submitted:
            new_row = {
                "Date": date,
                "Machine No": machine,
                "Shift": shift,
                "Machine Classification": classification,
                "Job Type": job_type,
                "Breakdown Category": category,
                "Reported Problem": problem,
                "Description of Work": work,
                "Start Time": start,
                "End Time": end,
                "Time Consumed": time_consumed,
                "Performed By": technician
            }

            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_data(df)

            st.success("✅ Breakdown Entry Saved!")

# ================================
# DAILY LOG TABLE + DELETE
# ================================
st.markdown("## 📋 Breakdown Daily Log Table")

st.dataframe(df, use_container_width=True)

st.markdown("### 🗑 Delete Record")

if len(df) > 0:
    delete_index = st.number_input(
        "Enter Row Number to Delete",
        min_value=0,
        max_value=len(df) - 1,
        step=1
    )

    if st.button("Delete Selected Row"):
        df = df.drop(delete_index).reset_index(drop=True)
        save_data(df)
        st.success("✅ Record Deleted Successfully!")
        st.rerun()

# ================================
# EXPORT OPTIONS
# ================================
st.markdown("## 📥 Export Data")

st.download_button(
    "Download CSV",
    df.to_csv(index=False),
    "breakdown_export.csv",
    "text/csv"
)

st.success("Dashboard Running Successfully ✅")
