import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ============================================
# CONFIG
# ============================================
st.set_page_config(
    page_title="KUTE Maintenance Dashboard",
    layout="wide"
)

DATA_FILE = "breakdown_log.csv"
MACHINES = [f"M{i}" for i in range(1, 19)]

# ============================================
# AUTO REFRESH EVERY 2 MINUTES
# ============================================
st.markdown("""
<script>
setTimeout(function(){
    window.location.reload();
}, 120000);
</script>
""", unsafe_allow_html=True)

# ============================================
# HELPER FUNCTIONS
# ============================================

def time_to_minutes(t):
    try:
        if pd.isna(t) or str(t).strip() == "":
            return 0
        parts = str(t).split(":")
        if len(parts) == 3:
            h, m, s = parts
            return int(h) * 60 + int(m)
        elif len(parts) == 2:
            h, m = parts
            return int(h) * 60 + int(m)
        return 0
    except:
        return 0


def standardize_columns(df):
    df.columns = [c.strip() for c in df.columns]

    mapping = {
        "Machine": "Machine No",
        "MachineNo": "Machine No",
        "Line": "Machine No",
        "Technician": "Performed By",
        "Duration": "Time Consumed",
        "Downtime": "Time Consumed",
        "Category": "Breakdown Category",
        "Problem": "Reported Problem",
    }

    df.rename(columns=mapping, inplace=True)

    required_cols = [
        "Date", "Machine No", "Shift",
        "Machine Classification", "Job Type",
        "Breakdown Category", "Reported Problem",
        "Description of Work", "Start Time",
        "End Time", "Time Consumed", "Performed By"
    ]

    for col in required_cols:
        if col not in df.columns:
            df[col] = ""

    return df


def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        return standardize_columns(df)
    else:
        return pd.DataFrame(columns=[
            "Date", "Machine No", "Shift",
            "Machine Classification", "Job Type",
            "Breakdown Category", "Reported Problem",
            "Description of Work", "Start Time",
            "End Time", "Time Consumed", "Performed By"
        ])


def save_data(df):
    df.to_csv(DATA_FILE, index=False)


# ============================================
# LOAD DATA
# ============================================
df = load_data()

# ============================================
# HEADER STYLE
# ============================================
st.markdown("""
<style>
.big-title {
    font-size:40px;
    font-weight:bold;
    color:#003366;
    text-align:center;
}
.sub-title {
    text-align:center;
    font-size:18px;
    color:#555;
}
.kpi-box {
    background-color:#f8f9fa;
    padding:20px;
    border-radius:15px;
    text-align:center;
    box-shadow: 0px 3px 6px rgba(0,0,0,0.2);
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='big-title'>KUTE Dashboard</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Kazim Utilization & Team Efficiency</div>", unsafe_allow_html=True)

st.divider()

# ============================================
# TABS
# ============================================
tabs = st.tabs([
    "🏠 Home",
    "📊 Analytics",
    "📌 Machine History",
    "👷 Team Contribution",
    "➕ Data Entry"
])

# ============================================
# HOME TAB
# ============================================
with tabs[0]:

    st.subheader("Live Machine Breakdown Status")

    total_events = len(df)
    total_minutes = df["Time Consumed"].apply(time_to_minutes).sum()
    total_hours = round(total_minutes / 60, 2)

    if total_events > 0:
        machine_summary = (
            df.groupby("Machine No")["Time Consumed"]
            .apply(lambda x: x.apply(time_to_minutes).sum())
            .reindex(MACHINES, fill_value=0)
        )
        worst_machine = machine_summary.idxmax()
    else:
        machine_summary = pd.Series(0, index=MACHINES)
        worst_machine = "N/A"

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Events", total_events)
    col2.metric("Total Downtime (Hours)", total_hours)
    col3.metric("Worst Machine", worst_machine)

    st.divider()

    st.bar_chart(machine_summary)

# ============================================
# ANALYTICS TAB
# ============================================
with tabs[1]:

    st.subheader("Monthly Breakdown Trend")

    if not df.empty:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df["Month"] = df["Date"].dt.strftime("%b")

        month_summary = (
            df.groupby("Month")["Time Consumed"]
            .apply(lambda x: x.apply(time_to_minutes).sum())
        )

        st.line_chart(month_summary)
    else:
        st.info("No data available.")

    st.divider()

    st.subheader("Breakdown Category Distribution")

    if "Breakdown Category" in df.columns:
        cat_df = df[df["Breakdown Category"].astype(str).str.strip() != ""]
        cat_summary = cat_df["Breakdown Category"].value_counts()

        if not cat_summary.empty:
            st.bar_chart(cat_summary)
        else:
            st.info("No category data available.")

# ============================================
# MACHINE HISTORY TAB
# ============================================
with tabs[2]:

    selected_machine = st.selectbox("Select Machine", MACHINES)

    machine_df = df[df["Machine No"] == selected_machine]

    st.dataframe(machine_df, use_container_width=True)

# ============================================
# TEAM CONTRIBUTION TAB
# ============================================
with tabs[3]:

    if "Performed By" in df.columns:
        tech_summary = df["Performed By"].value_counts()
        if not tech_summary.empty:
            st.bar_chart(tech_summary)
        else:
            st.info("No technician data available.")

# ============================================
# DATA ENTRY TAB
# ============================================
with tabs[4]:

    with st.form("entry_form"):

        date = st.date_input("Date", datetime.today())
        machine = st.selectbox("Machine", MACHINES)
        shift = st.selectbox("Shift", ["Day", "Night"])
        category = st.selectbox("Category", ["Mechanical", "Electrical", "Automation"])

        problem = st.text_area("Reported Problem")
        work = st.text_area("Work Done")
        time_consumed = st.text_input("Time Consumed (HH:MM:SS)", "00:10:00")
        technician = st.text_input("Technician")

        submitted = st.form_submit_button("Save Breakdown")

        if submitted:

            new_row = {
                "Date": date,
                "Machine No": machine,
                "Shift": shift,
                "Machine Classification": "",
                "Job Type": "B/D",
                "Breakdown Category": category,
                "Reported Problem": problem,
                "Description of Work": work,
                "Start Time": "",
                "End Time": "",
                "Time Consumed": time_consumed,
                "Performed By": technician
            }

            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_data(df)

            st.success("Breakdown Saved Successfully")
            st.rerun()

    st.divider()

    st.subheader("Delete Record")

    if len(df) > 0:
        delete_index = st.number_input(
            "Row Number",
            min_value=0,
            max_value=len(df)-1,
            step=1
        )

        if st.button("Delete Selected Row"):
            df = df.drop(delete_index).reset_index(drop=True)
            save_data(df)
            st.success("Record Deleted")
            st.rerun()

# ============================================
# SIDEBAR EXPORT
# ============================================
st.sidebar.header("Export")

st.sidebar.download_button(
    "Download CSV",
    df.to_csv(index=False),
    "breakdown_export.csv",
    "text/csv"
)

st.sidebar.success("System Running Successfully")
