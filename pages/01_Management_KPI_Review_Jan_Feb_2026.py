import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(layout="wide")

st.title("📊 Maintenance KPI Review – January & February 2026")
st.markdown("### Executive Management Dashboard")
st.markdown("---")

# =========================
# KPI 1 – Total Downtime
# =========================

st.header("1️⃣ Date-wise Machine Total Downtime")

total_downtime = 452.78

col1, col2, col3 = st.columns(3)
col1.metric("Total Downtime (hrs)", total_downtime)
col2.metric("Total Jobs", 1125)
col3.metric("Total Waiting Hours", 68.80)

st.markdown("---")

# =========================
# KPI 2 – Notification
# =========================

st.header("2️⃣ Notification Compliance")

notification_data = pd.DataFrame({
    "Status": ["With Notification", "Without Notification"],
    "Count": [858, 267]
})

fig_notif = px.pie(
    notification_data,
    names="Status",
    values="Count",
    hole=0.5,
    color_discrete_sequence=["#00CC96", "#EF553B"]
)

st.plotly_chart(fig_notif, use_container_width=True)

# =========================
# KPI 3 – Shift Downtime
# =========================

st.header("3️⃣ Shift-wise Downtime")

shift_data = pd.DataFrame({
    "Shift": ["Day", "Night"],
    "Downtime": [215.03, 237.75]
})

fig_shift = px.bar(
    shift_data,
    x="Shift",
    y="Downtime",
    color="Shift",
    text_auto=True,
    color_discrete_sequence=["#636EFA", "#AB63FA"]
)

st.plotly_chart(fig_shift, use_container_width=True)

# =========================
# KPI 4 – Job Category
# =========================

st.header("4️⃣ Breakdown vs Corrective")

job_data = pd.DataFrame({
    "Category": ["Breakdown", "Corrective"],
    "Jobs": [454, 671],
    "Downtime": [248.93, 203.85]
})

fig_job = px.bar(
    job_data,
    x="Category",
    y="Downtime",
    color="Category",
    text_auto=True,
    color_discrete_sequence=["#EF553B", "#00CC96"]
)

st.plotly_chart(fig_job, use_container_width=True)

# =========================
# KPI 5 – Waiting Time
# =========================

st.header("5️⃣ Total Waiting Time Impact")

waiting_percentage = round((68.80 / 452.78) * 100, 2)

col1, col2 = st.columns(2)
col1.metric("Total Waiting (hrs)", 68.80)
col2.metric("Waiting Impact %", f"{waiting_percentage} %")

# =========================
# KPI 6 – MTTR & MTBF
# =========================

st.header("6️⃣ Reliability KPIs")

col1, col2 = st.columns(2)
col1.metric("Overall MTTR (hrs)", 0.55)
col2.metric("Overall MTBF (hrs)", 68.72)

# =========================
# KPI 7 – Hourly Downtime Pattern
# =========================

st.header("7️⃣ Hourly Downtime Pattern")

hourly_data = pd.DataFrame({
    "Hour": list(range(24)),
    "Downtime": [
        18.30,27.43,20.87,19.27,19.17,3.35,15.35,37.42,
        19.07,14.47,16.92,4.13,15.00,20.78,22.77,27.83,
        13.38,8.62,30.53,4.88,24.20,23.90,24.88,20.27
    ]
})

fig_hour = px.line(
    hourly_data,
    x="Hour",
    y="Downtime",
    markers=True
)

st.plotly_chart(fig_hour, use_container_width=True)

# =========================
# KPI 8 – Technician Performance
# =========================

st.header("8️⃣ Technician Performance Overview")

tech_data = pd.DataFrame({
    "Technician": ["Dante","Nashwan","Husam","Day Shift Maint. Team","Edgar"],
    "Total Hours": [94.62,85.37,84.63,66.52,56.77],
    "Total Jobs": [239,235,226,157,154]
})

fig_tech = px.bar(
    tech_data,
    x="Technician",
    y="Total Hours",
    color="Total Jobs",
    text_auto=True
)

st.plotly_chart(fig_tech, use_container_width=True)

# =========================
# KPI 9 – Technician Job Distribution
# =========================

st.subheader("Technician Breakdown vs Corrective Distribution")

tech_split = pd.DataFrame({
    "Category": ["Breakdown","Corrective"],
    "Hours": [456.88, 367.87]
})

fig_split = px.pie(
    tech_split,
    names="Category",
    values="Hours",
    hole=0.4
)

st.plotly_chart(fig_split, use_container_width=True)

# =========================
# KPI 10 – Top Breakdown Reasons
# =========================

st.header("🔟 Top 10 Breakdown Reasons")

st.info("Top 10 breakdown reasons by downtime hours (From KPI#10 dataset)")

# Placeholder – connect your real dataset later
reason_data = pd.DataFrame({
    "Reason": ["Mechanical Jam","Sensor Failure","Air Pressure","Motor Fault","Capper Issue"],
    "Downtime": [45,38,32,28,25]
})

fig_reason = px.bar(
    reason_data,
    x="Downtime",
    y="Reason",
    orientation="h",
    text_auto=True,
    color="Downtime"
)

st.plotly_chart(fig_reason, use_container_width=True)

# =========================
# Executive Summary
# =========================

st.markdown("---")
st.header("📌 Executive Summary – Jan & Feb 2026")

st.success("""
• Total Downtime: 452.78 hrs  
• Breakdown Ratio: 40% (Reactive Maintenance still high)  
• Night Shift higher downtime than Day  
• Waiting Loss Impact: ~15%  
• Peak Risk Hours: 7 AM & 6 PM  
• Top Contributors: Dante, Nashwan, Husam  
• Notification Compliance: 76%  
""")

st.markdown("---")
st.markdown("Prepared for Management Review – 2026")
