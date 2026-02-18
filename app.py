import streamlit as st
import pandas as pd
import datetime

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="NADEC Maintenance Breakdown Dashboard",
    layout="wide"
)

st.title("🛠️ NADEC Real-Time Breakdown Dashboard (18 Machines)")
st.markdown("Operator Entry + Live KPI Bars + Download + CSV Upload")

# -----------------------------
# MACHINE LIST (18 Machines)
# -----------------------------
machines = [
    "M1", "M2", "M3", "M4", "M5", "M6",
    "M7", "M8", "M9", "M10", "M11", "M12",
    "M13", "M14", "M15", "M16", "M17", "M18"
]

# -----------------------------
# SESSION STORAGE
# -----------------------------
if "log" not in st.session_state:
    st.session_state.log = pd.DataFrame(
        columns=["Date", "Machine", "Breakdown Time (min)", "Reason", "Technician"]
    )

# -----------------------------
# CSV UPLOAD SECTION
# -----------------------------
st.subheader("📂 Upload Breakdown CSV (Optional)")

uploaded = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded:
    df_uploaded = pd.read_csv(uploaded)
    st.session_state.log = df_uploaded
    st.success("✅ CSV Loaded Successfully!")

# -----------------------------
# KPI BAR SECTION
# -----------------------------
st.subheader("📊 Machine Breakdown Status (Top View)")

if len(st.session_state.log) > 0:
    summary = (
        st.session_state.log.groupby("Machine")["Breakdown Time (min)"]
        .sum()
        .reindex(machines)
        .fillna(0)
    )
else:
    summary = pd.Series([0]*18, index=machines)

# Display bars
cols = st.columns(6)

for i, m in enumerate(machines):
    with cols[i % 6]:
        minutes = int(summary[m])
        st.metric(label=m, value=f"{minutes} min")

        # Progress bar (max 500 min scale)
        st.progress(min(minutes / 500, 1.0))

# -----------------------------
# DATA ENTRY FORM (HIDDEN BUTTON)
# -----------------------------
st.divider()
st.subheader("➕ Operator Breakdown Entry")

with st.expander("📝 Click Here to Add New Breakdown Entry", expanded=False):

    col1, col2, col3 = st.columns(3)

    with col1:
        date = st.date_input("Select Date", datetime.date.today())

    with col2:
        machine = st.selectbox("Select Machine", machines)

    with col3:
        time_min = st.number_input(
            "Breakdown Time (Minutes)",
            min_value=1,
            step=1
        )

    col4, col5 = st.columns(2)

    with col4:
        reason = st.selectbox(
            "Breakdown Reason",
            ["Mechanical", "Electrical", "Automation", "Utility", "Other"]
        )

    with col5:
        technician = st.text_input("Technician Name")

    if st.button("✅ Save Breakdown Entry"):
        new_row = pd.DataFrame([{
            "Date": str(date),
            "Machine": machine,
            "Breakdown Time (min)": time_min,
            "Reason": reason,
            "Technician": technician
        }])

        st.session_state.log = pd.concat(
            [st.session_state.log, new_row],
            ignore_index=True
        )

        st.success("Saved Successfully ✅ Dashboard Updated!")

# -----------------------------
# FILTER SECTION
# -----------------------------
st.divider()
st.subheader("🔍 Filter Breakdown Report")

colA, colB = st.columns(2)

with colA:
    filter_machine = st.selectbox(
        "Filter by Machine",
        ["All"] + machines
    )

with colB:
    filter_date = st.selectbox(
        "Filter by Date",
        ["All"] + sorted(st.session_state.log["Date"].unique().tolist())
        if len(st.session_state.log) > 0 else ["All"]
    )

filtered = st.session_state.log.copy()

if filter_machine != "All":
    filtered = filtered[filtered["Machine"] == filter_machine]

if filter_date != "All":
    filtered = filtered[filtered["Date"] == filter_date]

# -----------------------------
# BREAKDOWN LOG TABLE
# -----------------------------
st.divider()
st.subheader("📋 Breakdown Log Table (Live Data)")

st.dataframe(filtered, use_container_width=True)

# -----------------------------
# DOWNLOAD SECTION
# -----------------------------
st.divider()
st.subheader("⬇️ Download Reports")

csv_data = st.session_state.log.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Full Breakdown Report CSV",
    data=csv_data,
    file_name="breakdown_report.csv",
    mime="text/csv"
)

# -----------------------------
# AI SUPPORT BOX (Simple Analyzer)
# -----------------------------
st.divider()
st.subheader("🤖 Mini AI Assistant (Quick Insights)")

if len(st.session_state.log) > 0:
    worst_machine = summary.idxmax()
    worst_time = summary.max()

    st.info(f"""
    ✅ Highest Breakdown Machine: **{worst_machine}**  
    ⏱ Total Breakdown Time: **{worst_time} minutes**

    Suggestion: Focus preventive maintenance on this machine.
    """)
else:
    st.warning("No breakdown data yet. Upload CSV or add entry.")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("NADEC Maintenance Dashboard Prototype | Streamlit + GitHub + Real-Time KPI System")
