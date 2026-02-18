import streamlit as st
import pandas as pd
import os
import plotly.express as px
from datetime import datetime

# ============================================
# CONFIG
# ============================================
st.set_page_config(
    page_title="NADEC Live Breakdown Dashboard",
    layout="wide"
)

DATA_FILE = "breakdown_log.csv"

# ============================================
# LOAD OR CREATE DATA
# ============================================
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=[
        "Date", "Machine", "Reason", "Downtime_Minutes",
        "Technician", "Remarks"
    ])
    df.to_csv(DATA_FILE, index=False)

# Convert Date column
if not df.empty:
    df["Date"] = pd.to_datetime(df["Date"])

# ============================================
# MACHINE LIST (18 Machines)
# ============================================
machines = [f"M{i}" for i in range(1, 19)]

# ============================================
# REASON COLORS
# ============================================
reason_color = {
    "Mechanical": "red",
    "Electrical": "blue",
    "Automation": "orange",
    "Utility": "green",
    "Other": "gray"
}

# ============================================
# HEADER
# ============================================
st.markdown(
    """
    <h1 style='text-align:center; color:#003366;'>
    🖥 NADEC Live Maintenance Breakdown System (CUTE Style)
    </h1>
    <p style='text-align:center; font-size:16px;'>
    Real-Time Breakdown Tracking • 18 Machines • Operator Entry + KPI Monitoring
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# ============================================
# KPI SUMMARY
# ============================================
total_events = len(df)
total_minutes = df["Downtime_Minutes"].sum() if not df.empty else 0
total_hours = total_minutes / 60

worst_machine = "-"
if not df.empty:
    worst_machine = df.groupby("Machine")["Downtime_Minutes"].sum().idxmax()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Breakdown Events", total_events)
col2.metric("Total Downtime Hours", f"{total_hours:.1f} hrs")
col3.metric("Worst Machine", worst_machine)
col4.metric("System Status", "LIVE ✅")

st.divider()

# ============================================
# TOP MACHINE BARS (CUTE STYLE)
# ============================================
st.subheader("⚙️ Live Machine Breakdown Status (18 Lines)")

machine_summary = []
for m in machines:
    m_data = df[df["Machine"] == m]
    downtime = m_data["Downtime_Minutes"].sum() if not m_data.empty else 0
    last_reason = m_data["Reason"].iloc[-1] if not m_data.empty else "Other"
    machine_summary.append({
        "Machine": m,
        "Downtime_Minutes": downtime,
        "Reason": last_reason
    })

summary_df = pd.DataFrame(machine_summary)

# Plot Bar Chart
fig = px.bar(
    summary_df,
    x="Machine",
    y="Downtime_Minutes",
    color="Reason",
    color_discrete_map=reason_color,
    title="Breakdown Downtime per Machine (Minutes)",
)

fig.update_layout(
    height=400,
    xaxis_title="Machines",
    yaxis_title="Total Downtime (Minutes)",
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ============================================
# DATA ENTRY BUTTON (HIDDEN FORM)
# ============================================
st.subheader("➕ Operator Breakdown Entry")

if "show_form" not in st.session_state:
    st.session_state.show_form = False

# Button toggle
if st.button("📝 Add New Breakdown Entry"):
    st.session_state.show_form = not st.session_state.show_form

# Show Form Downside
if st.session_state.show_form:

    with st.form("breakdown_form"):

        entry_date = st.date_input("Breakdown Date", datetime.today())

        machine = st.selectbox("Select Machine", machines)

        reason = st.selectbox(
            "Breakdown Type",
            ["Mechanical", "Electrical", "Automation", "Utility", "Other"]
        )

        downtime = st.number_input(
            "Downtime Duration (Minutes)",
            min_value=1,
            step=5
        )

        technician = st.text_input("Technician Name")

        remarks = st.text_area("Remarks / Root Cause")

        submitted = st.form_submit_button("✅ Save Breakdown")

        if submitted:
            new_row = {
                "Date": entry_date,
                "Machine": machine,
                "Reason": reason,
                "Downtime_Minutes": downtime,
                "Technician": technician,
                "Remarks": remarks
            }

            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

            df.to_csv(DATA_FILE, index=False)

            st.success("Breakdown Entry Saved Successfully ✅")
            st.experimental_rerun()

st.divider()

# ============================================
# BREAKDOWN LOG TABLE (BOTTOM)
# ============================================
st.subheader("📋 Breakdown Event Log (Live Data Table)")

if df.empty:
    st.info("No breakdown records entered yet.")
else:
    st.dataframe(df.sort_values("Date", ascending=False), use_container_width=True)

# ============================================
# DOWNLOAD REPORT BUTTONS
# ============================================
st.subheader("⬇ Export Reports")

c1, c2 = st.columns(2)

with c1:
    st.download_button(
        "⬇ Download CSV Report",
        df.to_csv(index=False),
        file_name="NADEC_breakdown_report.csv"
    )

with c2:
    st.download_button(
        "⬇ Download Excel Report",
        df.to_excel("report.xlsx", index=False),
        file_name="NADEC_breakdown_report.xlsx"
    )

st.markdown(
    "<p style='text-align:center; font-size:13px; color:gray;'>"
    "NADEC Live Maintenance KPI Dashboard • Streamlit Real-Time Prototype"
    "</p>",
    unsafe_allow_html=True
)
