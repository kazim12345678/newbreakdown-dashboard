import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Drinkable KPIs 2025", layout="wide")

st.title("🥤 Drinkable KPIs Dashboard – 2025")
st.markdown("### Breakdown Downtime | Machine Failures | Technician Workload")

# -----------------------------
# KPI CARDS
# -----------------------------
kpi_data = {
    "Total Downtime Hours": 3466,
    "Total Breakdown Events": 8903,
    "Worst Downtime Month": "July",
    "Highest Breakdown Machine": "M15",
    "Top Technician Contributor": "Dante"
}

cols = st.columns(5)
for i, (k, v) in enumerate(kpi_data.items()):
    with cols[i]:
        st.metric(k, v)

# -----------------------------
# MONTHLY DOWNTIME CHART
# -----------------------------
months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
monthly_hours = [285,241,312,222,304,260,446,277,260,327,270,257]

fig1 = px.bar(
    x=months, y=monthly_hours,
    labels={"x":"Month", "y":"Downtime Hours"},
    title="Monthly Downtime Hours"
)
st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# TOP MACHINES BREAKDOWN
# -----------------------------
machines = ["M15","M7","M1","M14","M2"]
machine_counts = [963,825,822,805,621]

fig2 = px.bar(
    x=machine_counts, y=machines,
    orientation="h",
    labels={"x":"Breakdown Count", "y":"Machine"},
    title="Top Machines Breakdown Count"
)
st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# TECHNICIAN CONTRIBUTION PIE
# -----------------------------
tech_labels = ["Dante","Sameer","Gilbert","Lito","Husam","Ali"]
tech_values = [1541,1479,1395,1236,1214,753]

fig3 = px.pie(
    names=tech_labels, values=tech_values,
    title="Technician Contribution Share",
    hole=0.4
)
st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# TECHNICIAN WORKLOAD BAR
# -----------------------------
tech_rank_labels = ["Dante","Sameer","Gilbert","Lito","Husam","Amgad","Ali"]
tech_rank_values = [1541,1479,1395,1236,1214,1112,753]

fig4 = px.bar(
    x=tech_rank_values, y=tech_rank_labels,
    orientation="h",
    labels={"x":"Total Contribution", "y":"Technician"},
    title="Top Technician Workload Ranking"
)
st.plotly_chart(fig4, use_container_width=True)

# -----------------------------
# TECHNICIAN MONTHLY TABLE
# -----------------------------
tech_table = {
    "Technician": ["Ali","Amgad","Dante","Sameer","Gilbert","Lito","Husam","Nashwan","Moneef","Yousef"],
    "Jan":[50,117,129,216,132,143,88,71,61,16],
    "Feb":[54,97,110,98,128,130,92,85,99,11],
    "Mar":[65,102,160,91,115,140,72,100,110,14],
    "Apr":[65,None,40,129,113,125,None,105,143,20],
    "May":[70,105,86,81,152,134,100,71,111,53],
    "Jun":[68,126,105,None,128,83,127,None,97,66],
    "Jul":[78,110,120,163,125,101,126,132,107,74],
    "Aug":[90,121,142,166,126,139,145,147,138,47],
    "Sep":[None,84,134,145,118,126,130,161,6,46],
    "Oct":[43,99,189,176,147,72,107,112,80,30],
    "Nov":[88,101,163,140,111,11,98,108,102,33],
    "Dec":[82,50,163,74,None,32,129,108,57,14],
    "Total":[753,1112,1541,1479,1395,1236,1214,1200,1111,424]
}

df_tech = pd.DataFrame(tech_table)
st.subheader("👷 Technician Monthly Breakdown Workload (Jan–Dec)")
st.dataframe(df_tech.style.highlight_max(axis=0), use_container_width=True)

# -----------------------------
# MONTH-WISE DOWNTIME TABLE
# -----------------------------
month_dt = {
    "Month": months,
    "Total Downtime (HH:MM:SS)": [
        "285:51:00","241:58:00","312:16:00","222:32:00","304:34:00","260:13:00",
        "446:58:00","277:00:00","260:12:00","327:08:00","270:41:00","257:24:00"
    ]
}

df_month_dt = pd.DataFrame(month_dt)
st.subheader("📅 Month-wise Breakdown Downtime Summary")
st.dataframe(df_month_dt.style.highlight_max(subset=["Total Downtime (HH:MM:SS)"]), use_container_width=True)

# -----------------------------
# MACHINE BREAKDOWN FREQUENCY
# -----------------------------
machine_freq = {
    "Machine": ["Crates Area/Line","M1","M2","M3","M4","M5","M6","M7","M8","M9","M10","M12","M13","M14","M15","M16","M17","M18"],
    "Count": [635,822,621,538,590,1,574,825,614,59,1,366,317,805,963,214,511,447]
}

df_machine_freq = pd.DataFrame(machine_freq)
st.subheader("⚙️ Machine-wise Breakdown Frequency Report")
st.dataframe(df_machine_freq.style.highlight_max(subset=["Count"]), use_container_width=True)

# -----------------------------
# MACHINE AREA REPEATED ISSUE TABLE
# -----------------------------
area_data = {
    "Machine": ["M1","M1","M1","M2","M2","M2","M3","M3","M3","M3","M4","M4","M4","M4","M5","M6","M6","M6","M7","M7","M7","M8","M8","M8","M9","M9","M9","M10","M12","M12","M12","M13","M13","M13","M14","M14","M14","M15","M15","M15","M15","M16","M16","M16","M17","M17","M17","M18","M18","M18","Crates Area/Line","Crates Area/Line"],
    "Area": ["Filling & Capping","Downline","Crates Area /Line","Filling & Capping","Downline","Upstream","Filling & Capping","Upstream","Downline","Crates Area /Line","Filling & Capping","Downline","Upstream","Crates Area /Line","Filling & Capping","Filling & Capping","Upstream","Downline","Filling & Capping","Upstream","Downline","Upstream","Downline","Filling & Capping","Upstream","Filling & Capping","Downline","Downline","Filling & Capping","Downline","Upstream","Upstream","Downline","Filling & Capping","Filling & Capping","Downline","Upstream","Downline","Crates Area /Line","Downline"],
    "Count": [543,231,12,434,169,18,250,50,237,1,283,289,16,1,1,396,115,63,324,88,413,56,329,229,6,35,18,1,115,223,28,65,94,158,546,226,33,378,178,405,2,123,9,82,314,50,147,259,24,164,633,2]
}

df_area = pd.DataFrame(area_data)
st.subheader("🏭 Machine Area Wise Repeated Issues")
st.dataframe(df_area.style.highlight_max(subset=["Count"]), use_container_width=True)

# -----------------------------
# HOURLY BREAKDOWN HEATMAP
# -----------------------------
import numpy as np

breakdown_matrix = np.array([
 [14.4,13.4,11.0,10.9,18.8,9.3,13.3,16.9,10.3,11.6,9.2,10.0],
 [11.0,11.2,17.3,9.9,10.1,13.2,11.8,11.7,11.5,19.5,12.3,15.7],
 [7.9,15.4,10.9,6.7,10.9,7.8,22.4,9.3,10.0,7.0,9.4,11.8],
 [5.9,11.0,8.8,8.8,9.5,8.0,8.9,10.9,5.8,4.4,7.0,9.5],
 [6.6,10.7,10.0,8.0,7.0,5.0,123.1,9.3,8.1,9.5,9.4,8.2],
 [1.5,1.7,18.0,5.8,2.5,0.9,4.1,3.3,1.4,0.7,1.3,2.6],
 [21.0,14.7,19.3,16.7,18.4,22.5,34.0,16.0,14.2,27.1,11.3,11.9],
 [14.6,14.7,14.0,8.0,20.0,19.3,15.0,21.5,22.5,22.0,24.4,17.3],
 [18.0,11.3,8.4,9.8,23.8,10.5,17.6,15.5,13.5,32.6,27.6,16.1],
 [10.0,11.3,15.5,9.6,15.2,16.9,16.6,14.3,10.8,28.5,9.4,9.0],
 [6.1,4.3,6.0,8.4,12.0,18.5,13.1,11.5,12.6,7.8,15.5,6.7],
 [3.8,3.9,12.4,1.7,3.2,5.6,0.8,6.0,1.8,2.4,4.5,3.3],
 [7.5,10.5,14.8,11.1,5.6,7.8,18.3,10.1,12.0,10.8,8.5,8.2],
 [12.3,9.9,13.5,8.7,20.3,13.7,17.1,21.7,11.5,17.1,17.7,14.0],
 [15.5,11.2,11.9,8.7,12.4,13.6,20.9,13.1,10.5,15.7,14.6,21.2],
 [8.4,12.0,7.0,13.5,10.7,8.2,12.6,9.0,17.8,15.3,11.0,10.4],
 [26.6,8.5,2.8,5.5,11.8,10.7,9.7,7.4,12.8,14.8,10.7,8.1],
 [17.8,4.3,18.2,1.9,4.4,5.6,8.3,3.0,2.6,3.1,3.6,3.7],
 [24.4,12.2,19.1,11.1,24.5,14.1,15.9,18.0,13.6,17.3,13.4,12.0],
 [4.7,4.4,18.2,13.4,12.8,1.4,4.5,3.8,1.4,4.4,6.9,1.0],
 [14.8,6.0,11.8,9.5,9.5,16.1,6.4,11.3,11.2,12.1,10.9,16.7],
 [14.8,14.8,14.2,8.5,12.9,12.1,12.1,14.0,11.9,13.4,9.8,15.1],
 [9.0,13.9,10.3,9.4,13.0,9.7,20.0,9.7,14.4,20.7,16.0,14.6],
 [9.3,10.4,19.1,16.7,15.0,9.8,20.6,9.8,18.0,9.5,6.0,10.0]
])

fig_heat = px.imshow(
    breakdown_matrix,
    labels=dict(x="Month", y="Hour", color="Hours"),
    x=months,
    aspect="auto",
    color_continuous_scale="Reds"
)
st.subheader("🔥 Hourly Breakdown Heatmap (Hour vs Month)")
st.plotly_chart(fig_heat, use_container_width=True)

# -----------------------------
# MONTHLY TREND LINE
# -----------------------------
monthly_totals = breakdown_matrix.sum(axis=0)

fig_trend = px.line(
    x=months, y=monthly_totals,
    labels={"x":"Month", "y":"Total Breakdown Hours"},
    title="📈 Monthly Breakdown Trend"
)
st.plotly_chart(fig_trend, use_container_width=True)

# -----------------------------
# HOURLY TOTAL BAR
# -----------------------------
hourly_totals = breakdown_matrix.sum(axis=1)

fig_hour = px.bar(
    x=list(range(24)), y=hourly_totals,
    labels={"x":"Hour", "y":"Total Breakdown Hours"},
    title="📊 Total Breakdown by Hour (0–23)"
)
st.plotly_chart(fig_hour, use_container_width=True)
