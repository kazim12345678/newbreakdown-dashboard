import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import plotly.express as px

# ============================================
# CONFIG
# ============================================
st.set_page_config(
    page_title="KUTE - Maintenance Dashboard",
    layout="wide"
)

DATA_FILE = "breakdown_log.csv"
MACHINES = [f"M{i}" for i in range(1, 19)]

# ============================================
# AUTO REFRESH TIMER
# ============================================
st.markdown("""
<script>
setTimeout(function(){
    window.location.reload();
}, 120000);
</script>
""", unsafe_allow_html=True)

# ============================================
# HELPERS
# ============================================
def time_to_minutes(t):
    try:
        if pd.isna(t) or str(t).strip() == "":
            return 0
        parts = str(t).split(":")
        if len(parts) == 3:
            h, m, s = parts
            return int(h) * 60 + int(m)
        return 0
    except:
        return 0


def standardize_columns(df):
    df.columns = [c.strip() for c in df.columns]

    mapping = {
        "Machine": "Machine No",
        "Technician": "Performed By",
        "Duration": "Time Consumed",
        "Downtime": "Time Consumed",
        "Category": "Breakdown Category",
        "Problem": "Reported Problem",
    }

    df.rename(columns=mapping, inplace=True)

    required = [
        "Date", "Machine No", "Shift",
        "Machine Classification", "Job Type",
        "Breakdown Category", "Reported Problem",
        "Description of Work", "Start Time",
        "End Time", "Time Consumed", "Performed By"
    ]

    for col in required:
        if col not in df.columns:
            df[col] = ""

    return df


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


def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# ============================================
# LOAD DATA
# ============================================
df = load_data()

# ============================================
# HEADER UI
# ============================================
st.markdown("""
<style>
.kute-title {
    font-size:40px;
    font-weight:bold;
    color:#003366;
    text-align:center;
}
.navbox {
    background:#f8f9fa;
    padding:15px;
    border-radius:15px;
    text-align:center;
    font-size:18px;
    font-weight:bold;
    box-shadow:0px 2px 6px rgba(0,0,0,0.2);
}
.machinebox {
    background:white;
    padding:10px;
    border-radius:12px;
    text-align:center;
    border:2px solid #ddd;
    margin:5px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='kute-title'>KUTE Dashboard</div>", unsafe_allow_html=True)
st.markdown(
    "<h4 style='text-align:center;'>Kazim Utilization Team Efficiency (NADEC Style)</h4>",
    unsafe_allow_html=True
)

# ============================================
# NAVIGATION TABS
# ============================================
tabs = st.tabs([
    "🏠 Home",
    "📉 Breakdown Analytics",
    "📌 Machine History",
    "👷 Team Contribution",
    "➕ Data Entry"
])

# ============================================
# HOME TAB
# ============================================
with tabs[0]:

    st.subheader("🚦 Live Machine Breakdown Status (M1–M18)")

    # Machine downtime summary
    machine_summary = (
        df.groupby("Machine No")["Time Consumed"]
        .apply(lambda x: x.apply(time_to_minutes).sum())
        .reindex(MACHINES, fill_value=0)
    )

    # KPI Cards
    total_events = len(df)
    total_minutes = machine_summary.sum()
    total_hours = round(total_minutes / 60, 2)

    worst_machine = machine_summary.idxmax()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Events", total_events)
    col2.metric("Total Downtime (Hours)", total_hours)
    col3.metric("Worst Machine", worst_machine)
    col4.metric("Auto Refresh", "Every 2 min")

    st.divider()

    # Horizontal Bar Chart
    fig = px.bar(
        machine_summary.reset_index(),
        x="Time Consumed",
        y="Machine No",
        orientation="h",
        title="Machine Downtime Minutes (MTD)",
        labels={"Time Consumed": "Downtime (Minutes)"}
    )
    st.plotly_chart(fig, use_container_width=True)

    st.info("Click any machine tab in Machine History for details.")

# ============================================
# BREAKDOWN ANALYTICS TAB
# ============================================
with tabs[1]:
    st.subheader("📉 Breakdown Analytics")

    # Month wise downtime
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Month"] = df["Date"].dt.strftime("%b")

    month_summary = (
        df.groupby("Month")["Time Consumed"]
        .apply(lambda x: x.apply(time_to_minutes).sum())
    )

    fig2 = px.line(
        month_summary.reset_index(),
        x="Month",
        y="Time Consumed",
        markers=True,
        title="Month Wise Downtime Trend"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Category Pie
    cat_summary = df["Breakdown Category"].value_counts()

    fig3 = px.pie(
        cat_summary.reset_index(),
        names="index",
        values="Breakdown Category",
        title="Breakdown Category Contribution"
    )
    st.plotly_chart(fig3, use_container_width=True)

# ============================================
# MACHINE HISTORY TAB
# ============================================
with tabs[2]:
    st.subheader("📌 Machine Breakdown History")

    selected_machine = st.selectbox("Select Machine", MACHINES)

    machine_df = df[df["Machine No"] == selected_machine]

    st.write(f"### Breakdown Records for {selected_machine}")
    st.dataframe(machine_df, use_container_width=True)

# ============================================
# TEAM CONTRIBUTION TAB
# ============================================
with tabs[3]:
    st.subheader("👷 Technician Contribution")

    tech_summary = df["Performed By"].value_counts().head(10)

    fig4 = px.bar(
        tech_summary.reset_index(),
        x="Performed By",
        y="count",
        title="Top Technician Workload"
    )
    st.plotly_chart(fig4, use_container_width=True)

# ============================================
# DATA ENTRY TAB
# ============================================
with tabs[4]:
    st.subheader("➕ Operator Breakdown Entry Form")

    with st.form("entry_form"):

        date = st.date_input("Date", datetime.today())
        machine = st.selectbox("Machine", MACHINES)
        shift = st.selectbox("Shift", ["Day", "Night"])
        category = st.selectbox("Category", ["Mechanical", "Electrical", "Automation"])

        problem = st.text_area("Reported Problem")
        work = st.text_area("Work Done")
        time_consumed = st.text_input("Time Consumed (HH:MM:SS)", "00:10:00")
        technician = st.text_input("Technician Name")

        submitted = st.form_submit_button("✅ Save Breakdown")

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

            st.success("✅ Entry Saved Successfully!")
            st.rerun()

# ============================================
# EXPORT SECTION
# ============================================
st.sidebar.header("📥 Export Data")

st.sidebar.download_button(
    "Download CSV Report",
    df.to_csv(index=False),
    "breakdown_export.csv",
    "text/csv"
)

st.sidebar.success("KUTE Dashboard Running ✅")
