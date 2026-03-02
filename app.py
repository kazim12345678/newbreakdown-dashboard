import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")

# -----------------------------
# HELPER FUNCTION
# -----------------------------
def time_to_hours(t):
    h, m, s = map(int, t.split(":"))
    return h + m/60 + s/3600

# -----------------------------
# RAW DATA
# -----------------------------

total_downtime = time_to_hours("549:38:00")

# Machine Data
machine_data = {
    "M1":"24:22:00","M2":"35:04:00","M3":"31:30:00","M4":"31:44:00",
    "M5":"1:30:00","M6":"58:27:00","M7":"47:30:00","M8":"37:22:00",
    "M9":"3:13:00","M12":"20:04:00","M13":"22:45:00","M14":"43:57:00",
    "M15":"52:26:00","M16":"36:21:00","M17":"19:15:00","M18":"30:13:00",
    "Crates Area Line":"53:55:00"
}

machine_df = pd.DataFrame([
    {"Machine":k,"Hours":time_to_hours(v)} for k,v in machine_data.items()
]).sort_values(by="Hours",ascending=False)

machine_df["% Contribution"] = (machine_df["Hours"]/total_downtime)*100
machine_df["Cumulative %"] = machine_df["% Contribution"].cumsum()

top5_contribution = machine_df.head(5)["% Contribution"].sum()

# Equipment Data
equipment_data = {
"Filling & Capping Machine":"231:16:00",
"Packer Machine & Heating Tunnel":"94:24:00",
"Crates Destacker/Washer":"53:40:00",
"Crates Stacker & Unitizer":"48:36:00",
"Bottle Debagger/Unscrambler":"26:51:00"
}

equipment_df = pd.DataFrame([
    {"Equipment":k,"Hours":time_to_hours(v)} for k,v in equipment_data.items()
]).sort_values(by="Hours",ascending=False)

equipment_df["% Contribution"] = (equipment_df["Hours"]/total_downtime)*100

# Area Data
area_data = {
"Filling & Capping":"265:03:00",
"Downline":"177:14:00",
"Crates Area":"54:10:00",
"Upstream":"53:11:00"
}

area_df = pd.DataFrame([
    {"Area":k,"Hours":time_to_hours(v)} for k,v in area_data.items()
])

area_df["% Contribution"] = (area_df["Hours"]/total_downtime)*100

# Department Data
dept_data = {
"Mechanical":"377:47:00",
"Electrical":"148:47:00",
"Automation":"17:09:00"
}

dept_df = pd.DataFrame([
    {"Department":k,"Hours":time_to_hours(v)} for k,v in dept_data.items()
])

dept_df["% Contribution"] = (dept_df["Hours"]/total_downtime)*100

# Job Type
job_data = {
"Breakdown":"309:21:00",
"Corrective":"240:17:00"
}

job_df = pd.DataFrame([
    {"Type":k,"Hours":time_to_hours(v)} for k,v in job_data.items()
])

job_df["% Contribution"] = (job_df["Hours"]/total_downtime)*100

# Monthly
jan = 247
feb = 301

# -----------------------------
# DASHBOARD
# -----------------------------

st.title("EXECUTIVE MAINTENANCE KPI REVIEW – JAN & FEB 2026")

# -----------------------------
# CORE KPI SECTION
# -----------------------------

st.subheader("CORE KPIs (Top Management View)")

col1,col2,col3,col4 = st.columns(4)

col1.metric("Total Downtime (hrs)","549.6")
col2.metric("Breakdown %","56%")
col3.metric("Mechanical %","69%")
col4.metric("Top 5 Machines %","46.5%")

col5,col6,col7 = st.columns(3)

col5.metric("Filling Area Loss %","48%")
col6.metric("Worst Day","22 hrs (26-Feb)")
col7.metric("Top Equipment","Filling & Capping (42%)")

st.markdown("---")

# -----------------------------
# MACHINE PARETO
# -----------------------------
st.subheader("Machine Wise Downtime – Pareto")

fig = go.Figure()
fig.add_trace(go.Bar(
    x=machine_df["Machine"],
    y=machine_df["Hours"],
    name="Hours",
))
fig.add_trace(go.Scatter(
    x=machine_df["Machine"],
    y=machine_df["Cumulative %"],
    name="Cumulative %",
    yaxis="y2"
))

fig.update_layout(
    yaxis=dict(title="Hours"),
    yaxis2=dict(title="Cumulative %",overlaying="y",side="right"),
    height=500
)

st.plotly_chart(fig,use_container_width=True)

# -----------------------------
# EQUIPMENT
# -----------------------------
st.subheader("Equipment Contribution")

fig2 = px.bar(equipment_df,x="Equipment",y="% Contribution",text="% Contribution")
st.plotly_chart(fig2,use_container_width=True)

# -----------------------------
# AREA DISTRIBUTION
# -----------------------------
st.subheader("Area Wise Distribution")

fig3 = px.pie(area_df,values="Hours",names="Area",hole=0.5)
st.plotly_chart(fig3,use_container_width=True)

# -----------------------------
# DEPARTMENT DISTRIBUTION
# -----------------------------
st.subheader("Department Contribution")

fig4 = px.pie(dept_df,values="Hours",names="Department",hole=0.5)
st.plotly_chart(fig4,use_container_width=True)

# -----------------------------
# JOB TYPE
# -----------------------------
st.subheader("Breakdown vs Corrective")

fig5 = px.pie(job_df,values="Hours",names="Type",hole=0.5)
st.plotly_chart(fig5,use_container_width=True)

# -----------------------------
# MONTHLY TREND
# -----------------------------
st.subheader("Monthly Comparison")

month_df = pd.DataFrame({
    "Month":["January","February"],
    "Hours":[jan,feb]
})

fig6 = px.bar(month_df,x="Month",y="Hours",text="Hours")
st.plotly_chart(fig6,use_container_width=True)

# -----------------------------
# EXECUTIVE SUMMARY
# -----------------------------
st.markdown("### Executive Insights")

st.markdown("""
- 549.6 total downtime hours recorded.
- 56% of maintenance is reactive breakdown.
- Mechanical failures dominate at 69%.
- Top 5 machines contribute 46.5% of losses.
- Filling & Capping area accounts for 48% of downtime.
- Filling & Capping Machine alone contributes 42%.
- February downtime higher than January.
- 26-Feb recorded highest single day downtime (22 hrs).
""")
