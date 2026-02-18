import streamlit as st
import pandas as pd
import datetime
import plotly.express as px

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="NADEC Breakdown Dashboard",
    layout="wide"
)

st.title("🛠️ NADEC Real-Time Breakdown Dashboard (18 Machines)")
st.markdown("Interactive Bar Chart + Operator Entry + Download Reports")

# -----------------------------
# MACHINE LIST
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
# CSV UPLOAD
# -----------------------------
st.subheader("📂 Upload Breakdown CSV (Optional)")

uploaded = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded:
    df_uploaded = pd.read_csv(uploaded)
    st.session_state.log = df_uploaded
    st.success("✅ CSV Loaded Successfully!")

# -----------------------------
# TOP KPI BAR CHART
# -----------------------------
st.subheader("📊 Machine Breakdown Overview (Click Any Bar)")

if len(st.session_state.log) > 0:
    summary = (
        st.session_state.log.groupby("Machine")["Breakdown Time (min)"]
        .sum()
        .reindex(machines)
        .fillna(0)
        .reset_index()
    )
else:
    summary = pd.DataFrame({
        "Machine": machines,
        "Breakdown Time (min)": [0]*18
    })

# Interactive Bar Chart
fig = px.bar(
    summary,
    x="Machine",
    y="Breakdown Time (min)",
    title="Total Breakdown Minutes per Machine",
    text="Breakdown Time (min)"
)

fig.update_layout(
    height=450,
    xaxis_title="Machines",
    yaxis_title="Breakdown Minutes",
)

selected = st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# CLICK MACHINE DROPDOWN (SIMULATES BAR CLICK)
# -----------------------------
st.markdown("### 🔍 Select Machine to View Breakdown Details")

selected_machine = st.selectbox(
    "Choose Machine",
    ["All"] + machines
)

# -----------------------------
# HIDDEN DATA ENTRY FORM
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
st.subheader("📋 Breakdown Log Details")

filtered = st.session_state.log.copy()

if selected_machine != "All":
    filtered = filtered[filtered["Machine"] == selected_machine]

# Show Breakdown Table
st.dataframe(filtered, use_container_width=True)

# -----------------------------
# DOWNLOAD SECTION
# -----------------------------
st.divider()
st.subheader("⬇️ Download Report")

csv_data = st.session_state.log.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Full Breakdown Report CSV",
    data=csv_data,
    file_name="breakdown_report.csv",
    mime="text/csv"
)

# -----------------------------
# MINI AI INSIGHTS
# -----------------------------
st.divider()
st.subheader("🤖 Quick Maintenance Insight")

if len(st.session_state.log) > 0:
    worst_machine = summary.loc[
        summary["Breakdown Time (min)"].idxmax(), "Machine"
    ]
    worst_time = summary["Breakdown Time (min)"].max()

    st.info(f"""
    ✅ Highest Breakdown Machine: **{worst_machine}**  
    ⏱ Total Breakdown Time: **{worst_time} minutes**

    Suggestion: Focus preventive maintenance on this line.
    """)
else:
    st.warning("No breakdown data yet. Upload CSV or add entry.")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("NADEC Dashboard Prototype | Streamlit Real-Time Breakdown KPI System")
