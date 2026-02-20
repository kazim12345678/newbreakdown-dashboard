import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import pagesizes
from reportlab.lib.units import inch
import io

# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------
st.set_page_config(page_title="SERAC DT Analysis", layout="wide")

st.markdown("""
<style>
.block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
    padding-left: 0.8rem;
    padding-right: 0.8rem;
}
.metric-label { font-size: 0.8rem !important; }
.metric-value { font-size: 1.2rem !important; font-weight: 700 !important; }
</style>
""", unsafe_allow_html=True)

st.title("🏭 SERAC DRINKABLE SECTION – Advanced Technical Downtime Analysis")
st.markdown("#### Mobile‑friendly, drill‑down, and KPI‑driven view")
st.markdown("---")

# ----------------------------------------------------
# RAW DATA
# ----------------------------------------------------
data = [
["M1","Crates delivery stopped-Tech",316],["M1","Filling product valve",112],["M1","Filling Station",70],
["M1","Product Level Low_",34],["M1","Packer",30],["M1","Bottle line conveyor",21],
["M1","Filling Printer",15],["M1","Possimat",15],["M1","Crates area / conveyors",12],["M1","Crate Stacker",4],

["M2","Crate Stacker",374],["M2","Crates delivery stopped-Tech",239],["M2","Filler",169],
["M2","Filling product valve",85],["M2","Product Level Low_",73],["M2","Packer",52],
["M2","Cap Applicator",50],["M2","Bottle guider/Bottle holder/Bottle Screw",44],
["M2","Conveyor Breakdown",25],["M2","Welding work",23],["M2","Possimat",20],
["M2","Bottle line conveyor",12],["M2","Outfeed Conveyor of Filling Machine",10],

["M3","Crates delivery stopped-Tech",485],["M3","Filler",482],["M3","Product Level Low_",127],
["M3","Filling product valve",126],["M3","Crates area / conveyors",90],["M3","Welding work",77],
["M3","Electrical Motor",48],["M3","Bottle guider/Bottle holder/Bottle Screw",46],
["M3","Filling Station",41],["M3","Electrical Sensor",36],["M3","Conveyor Breakdown",28],
["M3","Crate Stacker",27],["M3","Possimat",12],["M3","Packer",11],

["M4","Crates delivery stopped-Tech",329],["M4","Crate Stacker",220],["M4","Product Level Low_",98],
["M4","Conveyor Between Packer & Cold Store",82],["M4","Crates area / conveyors",81],
["M4","Divider",74],["M4","Filling product valve",70],["M4","Packer",65],
["M4","Crate Conveyor & Pusher C-Loop",25],["M4","Automation_Fault_",16],
["M4","Welding work",12],["M4","Labeling Machine",5],

["M6","Conveyor Breakdown",93],["M6","Bottle line conveyor",56],["M6","Possimat",50],
["M6","Axon Machine",44],["M6","Filling Nozzle issue",42],["M6","Product Level Low_",35],
["M6","Outfeed Conveyor of Filling Machine",30],["M6","Filling Printer",18],
["M6","May pack",17],["M6","Bottle guider/Bottle holder/Bottle Screw",8],

["M7","Crates delivery stopped-Tech",270],["M7","Packer",125],["M7","Filling Printer",104],
["M7","Welding work",73],["M7","Filling Station",45],["M7","Product Level Low_",25],
["M7","Automation_Fault_",23],["M7","Crate Stacker",14],

["M8","Crates delivery stopped-Tech",266],["M8","Packer",85],["M8","Crate Conveyor & Pusher C-Loop",28],
["M8","Product Level Low_",26],["M8","Filling product valve",18],["M8","Filler",18],

["M9","Possimat",25],

["M12","Crates delivery stopped-Tech",108],["M12","Minor Stopages <10 min",60],
["M12","Lanfranchi Lines",48],["M12","Filling Station",41],["M12","Product Level Low_",10],
["M12","Crate Conveyor & Pusher C-Loop",10],["M12","Crate Stacker",6],

["M13","Prasmatic Machine",197],["M13","Product Level Low_",85],["M13","Lanfranchi Lines",85],
["M13","Cap Dispensor",33],["M13","Filling Printer",32],["M13","Filling product valve",20],
["M13","Bottle guider/Bottle holder/Bottle Screw",18],["M13","Cap Applicator",15],
["M13","Filling Station",15],

["M14","Temperature of Heater",293],["M14","Prasmatic Machine",238],
["M14","Bottle guider/Bottle holder/Bottle Screw",195],["M14","Product Level Low_",127],
["M14","Cap Sealing",55],["M14","Lanfranchi Lines",50],["M14","Emmiti Palletizer",40],
["M14","Bottom plate spring",30],["M14","Bottom Film Cutter",25],["M14","Filler",14],
["M14","Filling Printer",10],["M14","Bottle line conveyor",5],

["M15","Sipack Packer / Crates Packer",367],["M15","Crates delivery stopped-Tech",257],
["M15","Possimat",240],["M15","Product Level Low_",106],["M15","Bottle guider/Bottle holder/Bottle Screw",72],
["M15","Filling Station",52],["M15","Conveyor Between Packer & Cold Store",47],
["M15","Electrical Dosing Pump",32],["M15","Crates area / conveyors",21],
["M15","Filling Printer",18],["M15","Bottle line conveyor",15],["M15","Lanfranchi Lines",15],
["M15","conveyor overload",14],["M15","Conveyor Breakdown",12],["M15","Crate Stacker",12],
["M15","Cap Applicator",10],

["M16","Cap Applicator",271],["M16","Prasmatic Machine",216],["M16","Cap Dispensor",80],
["M16","Lanfranchi Lines",55],["M16","Glue Applying Machine",20],
["M16","Bottle guider/Bottle holder/Bottle Screw",19],["M16","Product Level Low_",15],

["M17","Lanfranchi Lines",53],["M17","Product Level Low_",40],["M17","Prasmatic Machine",40],
["M17","Cap Applicator",29],["M17","Downline Breakdown",27],

["M18","Prasmatic Machine",117],["M18","Cap Applicator",88],["M18","Filling Printer",83],
["M18","Product Level Low_",72],["M18","Lanfranchi Lines",66],
["M18","Emmiti Palletizer",14],["M18","Bottle guider/Bottle holder/Bottle Screw",12],
]

df = pd.DataFrame(data, columns=["Machine","Downtime Type","Minutes"])

# ----------------------------------------------------
# CORE CALCULATIONS
# ----------------------------------------------------
total_dt = df["Minutes"].sum()
machine_totals = df.groupby("Machine")["Minutes"].sum().sort_values(ascending=False)
cause_totals = df.groupby("Downtime Type")["Minutes"].sum().sort_values(ascending=False)
avg_dt = machine_totals.mean()

machine_analysis = machine_totals.reset_index()
machine_analysis.columns = ["Machine","Total DT"]
machine_analysis["% Plant Impact"] = (machine_analysis["Total DT"]/total_dt*100).round(2)
machine_analysis["Above Average"] = machine_analysis["Total DT"] > avg_dt

failure_counts = df.groupby("Machine")["Downtime Type"].count().rename("Failures")
machine_kpi = machine_analysis.merge(failure_counts, on="Machine", how="left")

# ----------------------------------------------------
# OPERATION TIME INPUT
# ----------------------------------------------------
st.subheader("⚙️ Operation Time & Reliability Basis")

col_op1, col_op2 = st.columns(2)
with col_op1:
    op_hours_per_machine = st.number_input(
        "Operating Hours per Machine (period under analysis)",
        min_value=1.0,
        value=600.0,
        step=1.0
    )
with col_op2:
    st.write("Assumptions:")
    st.write("- Failures = number of downtime events per machine")
    st.write("- MTTR uses downtime minutes / failures")
    st.write("- Availability uses operating hours vs downtime")

machine_kpi["DT Hours"] = (machine_kpi["Total DT"] / 60).round(2)
machine_kpi["MTBF (Hours)"] = (op_hours_per_machine / machine_kpi["Failures"]).round(2)
machine_kpi["MTTR (Hours)"] = (machine_kpi["DT Hours"] / machine_kpi["Failures"]).round(2)
machine_kpi["Availability %"] = (
    (op_hours_per_machine - machine_kpi["DT Hours"]) / op_hours_per_machine * 100
).round(2)

# ----------------------------------------------------
# KPI TILES
# ----------------------------------------------------
st.markdown("---")
st.subheader("📌 Plant‑Level KPIs")

plant_failures = failure_counts.sum()
plant_dt_hours = (total_dt / 60)
plant_mtbf = (op_hours_per_machine * len(machine_totals) / plant_failures)
plant_mttr = (plant_dt_hours / plant_failures)
plant_avail = ((op_hours_per_machine * len(machine_totals) - plant_dt_hours) /
               (op_hours_per_machine * len(machine_totals)) * 100)

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total DT (Minutes)", f"{int(total_dt)}")
k2.metric("Plant MTBF (Hours)", f"{plant_mtbf:.1f}")
k3.metric("Plant MTTR (Hours)", f"{plant_mttr:.2f}")
k4.metric("Availability (%)", f"{plant_avail:.1f}")

# ----------------------------------------------------
# MACHINE CRITICALITY
# ----------------------------------------------------
st.markdown("---")
st.subheader("📊 Machine Criticality & Ranking")

fig_rank = px.bar(
    machine_kpi,
    x="Machine",
    y="Total DT",
    color="Total DT",
    color_continuous_scale="Reds",
    text="Total DT",
    title="Machine Downtime Ranking (Higher = More Critical)"
)
fig_rank.update_layout(xaxis_title="Machine", yaxis_title="Downtime (Minutes)", height=420)
st.plotly_chart(fig_rank, use_container_width=True)

with st.expander("View Detailed Machine Table"):
    st.dataframe(machine_kpi, use_container_width=True, height=350)

# ----------------------------------------------------
# MACHINE‑WISE DRILL‑DOWN
# ----------------------------------------------------
st.markdown("---")
st.subheader("🔍 Machine‑wise Drill‑down")

selected_machine = st.selectbox("Select Machine", sorted(df["Machine"].unique()))

df_m = df[df["Machine"] == selected_machine].copy()
df_m = df_m.sort_values("Minutes", ascending=False)

c1, c2 = st.columns(2)
with c1:
    st.write(f"Top Downtime Causes – {selected_machine}")
    fig_m1 = px.bar(
        df_m,
        x="Downtime Type",
        y="Minutes",
        text="Minutes",
        title=f"{selected_machine} – Downtime by Cause"
    )
    fig_m1.update_layout(xaxis_tickangle=-45, height=420)
    st.plotly_chart(fig_m1, use_container_width=True)

with c2:
    st.write(f"KPI Snapshot – {selected_machine}")
    row = machine_kpi[machine_kpi["Machine"] == selected_machine].iloc[0]
    st.metric("Total DT (Minutes)", int(row["Total DT"]))
    st.metric("Failures (Events)", int(row["Failures"]))
    st.metric("MTBF (Hours)", row["MTBF (Hours)"])
    st.metric("MTTR (Hours)", row["MTTR (Hours)"])
    st.metric("Availability (%)", row["Availability %"])

# ----------------------------------------------------
# ENHANCED TREND‑STYLE VIEW
# ----------------------------------------------------
st.markdown("---")
st.subheader("📈 Trend‑style View by Machine (Enhanced)")

section_map = {
    "M1": "Section A", "M2": "Section A", "M3": "Section A", "M4": "Section A",
    "M6": "Section B", "M7": "Section B", "M8": "Section B", "M9": "Section B",
    "M12": "Section C", "M13": "Section C", "M14": "Section C",
    "M15": "Section D", "M16": "Section D", "M17": "Section D", "M18": "Section D"
}

trend_df = machine_kpi.sort_values("Machine").reset_index(drop=True)
trend_df["Section"] = trend_df["Machine"].map(section_map)

fig_trend = go.Figure()

fig_trend.add_trace(go.Scatter(
    x=trend_df["Machine"],
    y=trend_df["Total DT"],
    mode="lines+markers+text",
    text=[f"#{i+1}" for i in range(len(trend_df))],
    textposition="top center",
    marker=dict(
        size=12,
        color=trend_df["Total DT"],
        colorscale="YlOrRd",
        showscale=True,
        colorbar=dict(title="DT (min)")
    ),
    line=dict(width=3, color="gray"),
    hovertemplate=
        "<b>Machine:</b> %{x}<br>" +
        "<b>Total DT:</b> %{y} min<br>" +
        "<b>Failures:</b> %{customdata[0]}<br>" +
        "<b>MTBF:</b> %{customdata[1]} hr<br>" +
        "<b>MTTR:</b> %{customdata[2]} hr<br>" +
        "<b>Availability:</b> %{customdata[3]}%<br>" +
        "<b>Section:</b> %{customdata[4]}<extra></extra>",
    customdata=trend_df[["Failures", "MTBF (Hours)", "MTTR (Hours)", "Availability %", "Section"]]
))

fig_trend.update_layout(
    xaxis_title="Machine",
    yaxis_title="Downtime (Minutes)",
    height=450,
    title="Enhanced Trend View (Color‑coded + Tooltips + Ranking + Sections)"
)

st.plotly_chart(fig_trend, use_container_width=True)

# ----------------------------------------------------
# HEATMAP
# ----------------------------------------------------
st.markdown("---")
st.subheader("🔥 Heatmap – Machine vs Downtime Type")

pivot = df.pivot_table(
    index="Machine",
    columns="Downtime Type",
    values="Minutes",
    aggfunc="sum",
    fill_value=0
)

fig_heat = px.imshow(
    pivot,
    aspect="auto",
    color_continuous_scale="Reds",
    labels=dict(color="Minutes"),
)
fig_heat.update_layout(height=500)
st.plotly_chart(fig_heat, use_container_width=True)

# ----------------------------------------------------
# TRUE PARETO
# ----------------------------------------------------
st.markdown("---")
st.subheader("📉 True Pareto Analysis – Top 10 Downtime Causes")

pareto = cause_totals.reset_index()
pareto["Cumulative %"] = pareto["Minutes"].cumsum() / total_dt * 100

fig_pareto = go.Figure()
fig_pareto.add_bar(
    x=pareto["Downtime Type"][:10],
    y=pareto["Minutes"][:10],
    name="Minutes"
)
fig_pareto.add_scatter(
    x=pareto["Downtime Type"][:10],
    y=pareto["Cumulative %"][:10],
    yaxis="y2",
    name="Cumulative %",
    mode="lines+markers"
)
fig_pareto.update_layout(
    yaxis2=dict(overlaying="y", side="right"),
    xaxis_tickangle=-45,
    height=450
)
st.plotly_chart(fig_pareto, use_container_width=True)

# ----------------------------------------------------
# MTBF QUICK CALCULATOR
# ----------------------------------------------------
st.markdown("---")
st.subheader("🧮 MTBF Quick Calculator")

method = st.radio(
    "Select MTBF Calculation Method",
    [
        "Use current assumptions (events as failures)",
        "Manual: Enter Operating Time & Failures"
    ]
)

if method == "Use current assumptions (events as failures)":
    if st.button("Show MTBF Table (Current Settings)"):
        st.dataframe(
            machine_kpi[["Machine", "Failures", "MTBF (Hours)", "MTTR (Hours)", "Availability %"]],
            use_container_width=True
        )
else:
    op_hours_manual = st
    import streamlit as st

st.set_page_config(page_title="NADEC Breakdown Dashboard", layout="wide")

st.sidebar.title("Navigation")
st.sidebar.page_link("app.py", label="Main Dashboard")
st.sidebar.page_link("pages/1_Drinkable_KPIs_2025.py", label="Drinkable KPIs of 2025")

st.title("NADEC Breakdown Dashboard")
st.write("This is your main dashboard page. Use the sidebar to navigate to the 2025 KPIs dashboard.")
