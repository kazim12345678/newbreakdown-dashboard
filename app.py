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

CATEGORIES = {
    "Mechanical": "🔴 Mechanical",
    "Electrical": "🔵 Electrical",
    "Automation": "🟢 Automation"
}

# ============================
# LOAD / SAVE FUNCTIONS
# ============================
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=[
            "Date", "Machine", "Shift", "Classification",
            "JobType", "Category",
            "Problem", "WorkDone",
            "StartTime", "EndTime",
            "Downtime_Minutes",
            "Technician",
            "Status"
        ])

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

# ============================
# KPI SUMMARY
# ============================
total_events = len(df)
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
st.subheader("🚨 Current Active Breakdowns (Real-Time)")

active_df = df[df["Status"] == "OPEN"]

if len(active_df) == 0:
    st.success("✅ No Active Breakdown Right Now")
else:
    st.dataframe(active_df, use_container_width=True)

st.divider()

# ============================
# OPERATOR ENTRY FORM (HIDDEN)
# ============================
with st.expander("➕ Add New Breakdown Entry (Operator Form)", expanded=False):

    with st.form("entry_form"):

        date = st.date_input("Date", datetime.date.today())
        machine = st.selectbox("Machine", MACHINES)

        shift = st.radio("Shift", ["Day", "Night"], horizontal=True)

        classification = st.text_input("Machine Classification (Filler, Packer...)")

        jobtype = st.selectbox("Job Type", ["Breakdown (B/D)", "Corrective"])

        category = st.selectbox("Breakdown Category", list(CATEGORIES.keys()))

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
# CSV PASTE IMPORT
# ============================
st.subheader("📌 Paste Daily CSV Breakdown Log Here")

csv_text = st.text_area("Paste CSV Text (Date,Machine,Shift,...)", height=150)

if st.button("⬇️ Import CSV Data"):
    try:
        from io import StringIO
        imported = pd.read_csv(StringIO(csv_text))

        df = pd.concat([df, imported], ignore_index=True)
        save_data(df)

        st.success("✅ CSV Imported Successfully!")
        st.rerun()

    except Exception as e:
        st.error(f"Error importing CSV: {e}")

st.divider()

# ============================
# MACHINE WISE BAR CHART (M1–M18)
# ============================
st.subheader("⚙️ Machine Downtime Summary (M1–M18)")

machine_summary = df.groupby("Machine")["Downtime_Minutes"].sum().reindex(MACHINES, fill_value=0)

st.bar_chart(machine_summary)

st.divider()

# ============================
# DAILY LOG TABLE WITH DELETE OPTION
# ============================
st.subheader("📋 Full Breakdown Daily Log Sheet")

st.dataframe(df, use_container_width=True)

st.write("### ❌ Delete a Record")

if total_events > 0:
    delete_index = st.number_input("Enter Row Index to Delete", min_value=0, max_value=len(df)-1)

    if st.button("Delete Selected Row"):
        df = df.drop(delete_index).reset_index(drop=True)
        save_data(df)
        st.success("Row Deleted Successfully!")
        st.rerun()

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

st.download_button(
    "⬇️ Download Excel Report",
    df.to_excel("report.xlsx", index=False),
    file_name="breakdown_report.xlsx"
)

st.success("✅ Dashboard Ready for NADEC Real-Time Use")
