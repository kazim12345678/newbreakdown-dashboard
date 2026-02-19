import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ============================
# CONFIG
# ============================

st.set_page_config(
    page_title="KUTE Dashboard",
    layout="wide"
)

DATA_FILE = "breakdown_log.csv"

# ============================
# CREATE FILE IF NOT EXISTS
# ============================

def create_file():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=[
            "Date", "Machine No", "Shift",
            "Machine Classification", "Job Type",
            "Breakdown Category", "Reported Problem",
            "Description of Work", "Start Time",
            "End Time", "Time Consumed",
            "Performed By", "Status"
        ])
        df.to_csv(DATA_FILE, index=False)

create_file()

# ============================
# LOAD DATA
# ============================

df = pd.read_csv(DATA_FILE)

# ============================
# TITLE HEADER
# ============================

st.title("KUTE - Kazim Utilization & Team Efficiency Dashboard")
st.write("Real-time NADEC Style Maintenance Breakdown System")

st.divider()

# ============================
# KPI CARDS
# ============================

total_events = len(df)

if total_events > 0:
    total_minutes = df["Time Consumed"].fillna("00:00").apply(
        lambda x: int(x.split(":")[0]) * 60 + int(x.split(":")[1])
        if ":" in str(x) else 0
    ).sum()
else:
    total_minutes = 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Breakdown Events", total_events)
col2.metric("Total Downtime (Minutes)", total_minutes)

if total_events > 0:
    worst_machine = df["Machine No"].value_counts().idxmax()
else:
    worst_machine = "None"

col3.metric("Worst Machine", worst_machine)

open_jobs = len(df[df["Status"] == "OPEN"]) if "Status" in df.columns else 0
col4.metric("Pending Jobs", open_jobs)

st.divider()

# ============================
# ADD BREAKDOWN FORM
# ============================

st.subheader("Add New Breakdown Entry")

with st.form("breakdown_form"):
    date = st.date_input("Date", datetime.today())
    machine = st.selectbox("Machine No", [f"M{i}" for i in range(1, 19)])
    shift = st.selectbox("Shift", ["Day", "Night"])
    classification = st.text_input("Machine Classification")
    job_type = st.selectbox("Job Type", ["B/D", "Corrective"])
    category = st.selectbox("Breakdown Category", ["Mechanical", "Electrical", "Automation"])
    problem = st.text_input("Reported Problem")
    work = st.text_area("Description of Work")
    start = st.time_input("Start Time")
    end = st.time_input("End Time")
    technician = st.text_input("Performed By")
    status = st.selectbox("Status", ["OPEN", "CLOSED"])

    submitted = st.form_submit_button("Save Breakdown")

    if submitted:
        start_dt = datetime.combine(date, start)
        end_dt = datetime.combine(date, end)
        duration = end_dt - start_dt
        minutes = int(duration.total_seconds() / 60)

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
            "Time Consumed": minutes,
            "Performed By": technician,
            "Status": status
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)

        st.success("Breakdown saved successfully!")
        st.rerun()

st.divider()

# ============================
# SHOW TABLE
# ============================

st.subheader("Full Breakdown Log")

st.dataframe(df, use_container_width=True)
