import streamlit as st
import pandas as pd
import datetime
import os

# ============================
# CONFIG
# ============================
st.set_page_config(
    page_title="NADEC CUTE Maintenance Dashboard",
    layout="wide"
)

DATA_FILE = "breakdown_log.csv"

MACHINES = [f"M{i}" for i in range(1, 19)]

# Required Columns (Fix for old CSV)
REQUIRED_COLUMNS = [
    "Date", "Machine", "Shift", "Classification",
    "JobType", "Category",
    "Problem", "WorkDone",
    "StartTime", "EndTime",
    "Downtime_Minutes",
    "Technician",
    "Status"
]

# ============================
# LOAD / SAVE FUNCTIONS
# ============================
def load_data():
    # If file exists, load it
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)

        # ✅ Auto-Fix Missing Columns
        for col in REQUIRED_COLUMNS:
            if col not in df.columns:
                df[col] = ""

        return df

    # If no file exists, create fresh structure
    else:
        return pd.DataFrame(columns=REQUIRED_COLUMNS)


def save_data(df):
    df.to_csv(DATA_FILE, index=False)


df = load_data()

# ============================
# HEADER
# ============================
st.markdown("""
<style>
.big-title {
    font-size:35px;
    font-weight:800;
    color:#003366;
}
.kpi-box {
    padding:15px;
    border-radius:15px;
    background:white;
    box-shadow:0px 3px 10px rgba(0,0,0,0.15);
    text-align:center;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='big-title'>🏭 NADEC CUTE Maintenance Breakdown Dashboard</div>", unsafe_allow_html=True)
st.write("Real-time Machine Breakdown Tracking | Operator Entry | KPI Analytics")

st.divider()

# ============================
# KPI SUMMARY
# ============================
total_events = len(df)

# Convert downtime safely
df["Downtime_Minutes"] = pd.to_numeric(df["Downtime_Minutes"], errors="coerce").fillna(0)

total_downtime = df["Downtime_Minutes"].sum()

worst_machine = "-"
if total_events > 0:
    worst_machine = df.groupby("Machine")["Downtime_Minutes"].sum().idxmax()

top_tech = "-"
if total_events > 0:
    top_tech = df.groupby("Technician")["Downtime_Minutes"].sum().idxmax()

col1, col2, col3, col4 = st.columns(4)

col1.markdown(f"<div class='kpi-box'><h4>Total Events</h4><h2>{total_events}</h2></div>", unsafe_allow_html=True)
col2.markdown(f"<div class='kpi-box'><h4>Total Downtime (min)</h4><h2>{total_downtime:.0f}</h2></div>", unsafe_allow_html=True)
col3.markdown(f"<div class='kpi-box'><h4>Worst Machine</h4><h2>{worst_machine}</h2></div>", unsafe_allow_html=True)
col4.markdown(f"<div class='kpi-box'><h4>Top Technician</h4><h2>{top_tech}</h2></div>", unsafe_allow_html=True)

st.divider()

# ============================
# CURRENT REAL-TIME BREAKDOWN BAR
# ============================
st.subheader("🚨 Current Active Breakdowns (Real-Time OPEN Jobs)")

# Fix empty status
df["Status"] = df["Status"].fillna("CLOSED")

active_df = df[df["Status"] == "OPEN"]

if len(active_df) == 0:
    st.success("✅ No Active Breakdown Right Now")
else:
    st.dataframe(active_df, use_container_width=True)

st.divider()

# ============================
# OPERATOR ENTRY FORM
# ============================
with st.expander("➕ Add New Breakdown Entry (Operator Form)", expanded=False):

    with st.form("entry_form"):

        date = st.date_input("Date", datetime.date.today())
        machine = st.selectbox("Machine", MACHINES)

        shift = st.radio("Shift", ["Day", "Night"], horizontal=True)

        classification = st.text_input("Machine Classification (Filler, Packer...)")

        jobtype = st.selectbox("Job Type", ["Breakdown (B/D)", "Corrective"])

        category = st.selectbox("Breakdown Category", ["Mechanical", "Electrical", "Automation"])

        problem = st.text_area("Reported Problem")
        workdone = st.text_area("Description of Work Done")

        start_time = st.time_input("Start Time", datetime.datetime.now().time())
        end_time = st.time_input("End Time", datetime.datetime.now().time())

        technician = st.text_input("Technician Name")

        status = st.selectbox("Status", ["OPEN", "CLOSED"])

        submitted = st.form_submit_button("💾 Save Breakdown Entry")

        if submitted:
            dt_start = datetime.datetime.combine(date, start_time)
            dt_end = datetime.datetime.combine(date, end_time)

            downtime = (dt_end - dt_start).total_seconds() / 60
            if downtime < 0:
                downtime = 0

            new_row = {
                "Date": date,
                "Machine": machine,
                "Shift": shift,
                "Classification": classification,
                "JobType": jobtype,
                "Category": category,
                "Problem": problem,
                "WorkDone": workdone,
                "StartTime": start_time,
                "EndTime": end_time,
                "Downtime_Minutes": downtime,
                "Technician": technician,
                "Status": status
            }

            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_data(df)

            st.success("✅ Breakdown Entry Saved Successfully!")
            st.rerun()

st.divider()

# ============================
# MACHINE WISE BAR CHART (M1–M18)
# ============================
st.subheader("⚙️ Machine Downtime Summary (M1–M18)")

machine_summary = df.groupby("Machine")["Downtime_Minutes"].sum().reindex(MACHINES, fill_value=0)

st.bar_chart(machine_summary)

st.divider()

# ============================
# FULL DAILY LOG TABLE
# ============================
st.subheader("📋 Full Breakdown Daily Log Sheet")

st.dataframe(df, use_container_width=True)

st.divider()

# ============================
# EXPORT OPTIONS
# ============================
st.subheader("📤 Export Reports")

st.download_button(
    "⬇️ Download CSV Report",
    df.to_csv(index=False),
    file_name="breakdown_report.csv",
    mime="text/csv"
)

st.success("✅ NADEC Dashboard Running Perfectly")
