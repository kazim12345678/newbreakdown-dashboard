import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Helper functions
# -----------------------------
def to_timedelta(s):
    return pd.to_timedelta(s)

def add_hours_column(df, time_col="Time"):
    df["Duration"] = df[time_col].apply(to_timedelta)
    df["Hours"] = df["Duration"].dt.total_seconds() / 3600
    return df

# -----------------------------
# Raw data (from your message)
# -----------------------------

# 1) Machine-wise (M1..M9 + Crates Area/Line)
machines_data = [
    ("Crates Area/Line", "53:55:00"),
    ("M1", "24:22:00"),
    ("M12", "20:04:00"),
    ("M13", "22:45:00"),
    ("M14", "43:57:00"),
    ("M15", "52:26:00"),
    ("M16", "36:21:00"),
    ("M17", "19:15:00"),
    ("M18", "30:13:00"),
    ("M2", "35:04:00"),
    ("M3", "31:30:00"),
    ("M4", "31:44:00"),
    ("M5", "1:30:00"),
    ("M6", "58:27:00"),
    ("M7", "47:30:00"),
    ("M8", "37:22:00"),
    ("M9", "3:13:00"),
]
machines_df = pd.DataFrame(machines_data, columns=["Machine", "Time"])
machines_df = add_hours_column(machines_df, "Time")

# 2) Area-wise
area_data = [
    ("Crates Area /Line", "54:10:00"),
    ("Downline", "177:14:00"),
    ("Filling & Capping", "265:03:00"),
    ("Upstream", "53:11:00"),
]
area_df = pd.DataFrame(area_data, columns=["Area", "Time"])
area_df = add_hours_column(area_df, "Time")

# 3) Breakdown vs Corrective
bd_corr_data = [
    ("B/D", "309:21:00"),
    ("Corrective", "240:17:00"),
]
bd_corr_df = pd.DataFrame(bd_corr_data, columns=["Type", "Time"])
bd_corr_df = add_hours_column(bd_corr_df, "Time")

# 4) Category-wise (Mech/Elect/Automation/etc.)
category_data = [
    ("Automation", "17:09:00"),
    ("Elect", "148:47:00"),
    ("Material", "1:31:00"),
    ("Mech", "377:47:00"),
    ("Operation", "0:46:00"),
    ("Others", "0:32:00"),
    ("Utility", "1:15:00"),
    ("Workshop", "1:51:00"),
]
category_df = pd.DataFrame(category_data, columns=["Category", "Time"])
category_df = add_hours_column(category_df, "Time")

# 5) Equipment-wise
equipment_data = [
    ("Bottle Debagger, Bottle Unscrambler", "26:51:00"),
    ("Bottle Inspection Machine, Bottle Invert Cleaner", "4:23:00"),
    ("Bottle Line Conveyor,Overhead Bottle Conveyor, Air Conveyor", "21:32:00"),
    ("Cap Hooper / Elevator Unit", "1:15:00"),
    ("Cap Sorter / Cap Conveyor Unit", "2:30:00"),
    ("Cap Top Sticker Unit", "0:15:00"),
    ("C-loop Crates Chute / Overhead Crates Conveyor", "11:10:00"),
    ("Crates Destacker / Crates Washer / Crates lines", "53:40:00"),
    ("Crates Stacker & Unitizer Unit", "48:36:00"),
    ("Downline Conveyor Bottles, Wraps & Case Handling Line", "2:45:00"),
    ("Filling and Capping Machine", "231:16:00"),
    ("Filling Machine Infeed Conveyor", "2:15:00"),
    ("Filling Machine Outfeed Conveyor", "1:43:00"),
    ("Ink Jet Printer Unit", "15:26:00"),
    ("Labelling Machine", "4:05:00"),
    ("Packer Machine & Heating Tunnel", "94:24:00"),
    ("Pallet Wrapping Machine", "1:07:00"),
    ("Palletizer Machine", "9:35:00"),
    ("Sleeve Applicator & Heating Tunnel", "6:02:00"),
    ("Turret Bottle Cleaner / Rinser", "10:48:00"),
]
equipment_df = pd.DataFrame(equipment_data, columns=["Equipment", "Time"])
equipment_df = add_hours_column(equipment_df, "Time")

# 6) Daily data (Jan–Feb–1 Mar)
daily_data = [
    ("1-Jan", "13:01:00"),
    ("2-Jan", "11:28:00"),
    ("3-Jan", "5:37:00"),
    ("4-Jan", "9:27:00"),
    ("5-Jan", "5:02:00"),
    ("6-Jan", "9:00:00"),
    ("7-Jan", "11:06:00"),
    ("8-Jan", "10:50:00"),
    ("9-Jan", "19:26:00"),
    ("10-Jan", "13:16:00"),
    ("11-Jan", "7:40:00"),
    ("12-Jan", "14:18:00"),
    ("13-Jan", "3:12:00"),
    ("14-Jan", "7:24:00"),
    ("15-Jan", "11:09:00"),
    ("16-Jan", "6:53:00"),
    ("17-Jan", "7:52:00"),
    ("18-Jan", "6:17:00"),
    ("19-Jan", "14:14:00"),
    ("20-Jan", "3:20:00"),
    ("21-Jan", "6:35:00"),
    ("22-Jan", "6:09:00"),
    ("23-Jan", "7:32:00"),
    ("24-Jan", "10:41:00"),
    ("25-Jan", "7:28:00"),
    ("26-Jan", "7:09:00"),
    ("27-Jan", "5:39:00"),
    ("28-Jan", "10:56:00"),
    ("29-Jan", "11:34:00"),
    ("30-Jan", "2:30:00"),
    ("31-Jan", "8:06:00"),
    ("1-Feb", "3:35:00"),
    ("2-Feb", "10:08:00"),
    ("3-Feb", "9:03:00"),
    ("4-Feb", "6:17:00"),
    ("5-Feb", "8:39:00"),
    ("6-Feb", "7:33:00"),
    ("7-Feb", "7:43:00"),
    ("8-Feb", "8:13:00"),
    ("9-Feb", "7:22:00"),
    ("10-Feb", "6:13:00"),
    ("11-Feb", "16:20:00"),
    ("12-Feb", "8:54:00"),
    ("13-Feb", "8:16:00"),
    ("14-Feb", "11:33:00"),
    ("15-Feb", "11:24:00"),
    ("16-Feb", "6:45:00"),
    ("17-Feb", "10:36:00"),
    ("18-Feb", "9:30:00"),
    ("19-Feb", "6:55:00"),
    ("20-Feb", "11:33:00"),
    ("21-Feb", "8:30:00"),
    ("22-Feb", "13:30:00"),
    ("23-Feb", "17:22:00"),
    ("24-Feb", "7:15:00"),
    ("25-Feb", "11:38:00"),
    ("26-Feb", "22:00:00"),
    ("27-Feb", "11:15:00"),
    ("28-Feb", "6:35:00"),
    ("1-Mar", "0:10:00"),
]
daily_df = pd.DataFrame(daily_data, columns=["Date", "Time"])
daily_df = add_hours_column(daily_df, "Time")

# -----------------------------
# Global totals & KPIs
# -----------------------------
total_duration = equipment_df["Duration"].sum()
total_hours = total_duration.total_seconds() / 3600

# Mechanical vs Electrical
mech_hours = category_df.loc[category_df["Category"] == "Mech", "Hours"].sum()
elect_hours = category_df.loc[category_df["Category"] == "Elect", "Hours"].sum()
mech_pct = mech_hours / total_hours * 100
elect_pct = elect_hours / total_hours * 100

# Breakdown vs Corrective
bd_hours = bd_corr_df.loc[bd_corr_df["Type"] == "B/D", "Hours"].sum()
corr_hours = bd_corr_df.loc[bd_corr_df["Type"] == "Corrective", "Hours"].sum()
bd_pct = bd_hours / total_hours * 100
corr_pct = corr_hours / total_hours * 100

# Top contributors
top_machine = machines_df.sort_values("Hours", ascending=False).iloc[0]
top_equipment = equipment_df.sort_values("Hours", ascending=False).iloc[0]
top_area = area_df.sort_values("Hours", ascending=False).iloc[0]

# -----------------------------
# Streamlit layout
# -----------------------------
st.set_page_config(
    page_title="Management KPI Review - Breakdown Analysis",
    layout="wide",
)

# Optional logo if present
try:
    st.sidebar.image("company_logo.png", use_column_width=True)
except Exception:
    pass

st.title("Mr. Omer KPI Review – Lines Breakdown Executive Dashboard")
st.caption("Period: Jan–Feb–2026 | All figures based on maintenance LogSheet downtime (HH:MM:SS).")

# -----------------------------
# Top KPI row
# -----------------------------
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        "Total Downtime",
        f"{int(total_hours):,} h",
        help=str(total_duration),
    )

with kpi2:
    st.metric(
        "Mechanical vs Electrical",
        f"{mech_pct:0.1f}% Mech / {elect_pct:0.1f}% Elect",
        help=f"Mech: {mech_hours:0.1f} h | Elect: {elect_hours:0.1f} h",
    )

with kpi3:
    st.metric(
        "Breakdown vs Corrective",
        f"{bd_pct:0.1f}% B/D / {corr_pct:0.1f}% Corr",
        help=f"B/D: {bd_hours:0.1f} h | Corr: {corr_hours:0.1f} h",
    )

with kpi4:
    st.metric(
        "Top Area by Downtime",
        f"{top_area['Area']}",
        help=f"{top_area['Hours']:0.1f} h",
    )

st.markdown("---")

# -----------------------------
# Area & Category view
# -----------------------------
c1, c2, c3 = st.columns([1.2, 1.2, 1])

with c1:
    st.subheader("Downtime by Area")
    fig_area = px.pie(
        area_df,
        names="Area",
        values="Hours",
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.Blues_r,
    )
    fig_area.update_layout(showlegend=True)
    st.plotly_chart(fig_area, use_container_width=True)
    st.dataframe(area_df[["Area", "Time", "Hours"]].sort_values("Hours", ascending=False))

with c2:
    st.subheader("Downtime by Category")
    fig_cat = px.bar(
        category_df.sort_values("Hours", ascending=False),
        x="Category",
        y="Hours",
        color="Category",
        color_discrete_sequence=px.colors.sequential.Viridis,
    )
    fig_cat.update_layout(xaxis_title="", yaxis_title="Hours")
    st.plotly_chart(fig_cat, use_container_width=True)
    st.dataframe(category_df[["Category", "Time", "Hours"]].sort_values("Hours", ascending=False))

with c3:
    st.subheader("Breakdown vs Corrective")
    fig_bd = px.pie(
        bd_corr_df,
        names="Type",
        values="Hours",
        color="Type",
        color_discrete_map={"B/D": "#d62728", "Corrective": "#1f77b4"},
        hole=0.5,
    )
    st.plotly_chart(fig_bd, use_container_width=True)
    st.dataframe(bd_corr_df[["Type", "Time", "Hours"]])

st.markdown("---")

# -----------------------------
# Machine-wise view
# -----------------------------
st.subheader("Machine-wise Downtime (Pareto View)")
machines_sorted = machines_df.sort_values("Hours", ascending=False)
fig_machines = px.bar(
    machines_sorted,
    x="Machine",
    y="Hours",
    color="Hours",
    color_continuous_scale="Reds",
)
fig_machines.update_layout(
    xaxis_title="Machine",
    yaxis_title="Hours",
)
st.plotly_chart(fig_machines, use_container_width=True)
st.dataframe(machines_sorted[["Machine", "Time", "Hours"]])

st.markdown("---")

# -----------------------------
# Equipment-wise view (Executive Pareto)
# -----------------------------
st.subheader("Equipment-wise Downtime – Executive Pareto")

equipment_sorted = equipment_df.sort_values("Hours", ascending=False)
equipment_sorted["Cumulative %"] = equipment_sorted["Hours"].cumsum() / equipment_sorted["Hours"].sum() * 100

c_eq1, c_eq2 = st.columns([2, 1])

with c_eq1:
    fig_eq = px.bar(
        equipment_sorted,
        x="Equipment",
        y="Hours",
        color="Hours",
        color_continuous_scale="Purples",
    )
    fig_eq.update_layout(
        xaxis_title="Equipment",
        yaxis_title="Hours",
        xaxis_tickangle=-45,
    )
    st.plotly_chart(fig_eq, use_container_width=True)

with c_eq2:
    st.write("Top Equipment Contributors")
    st.dataframe(
        equipment_sorted[["Equipment", "Time", "Hours", "Cumulative %"]].head(10)
    )

st.markdown("---")

# -----------------------------
# Daily trend view
# -----------------------------
st.subheader("Daily Downtime Trend (Jan–Feb–1 Mar 2026)")

# Try to parse dates for nicer x-axis
daily_df["Date_parsed"] = pd.to_datetime(daily_df["Date"], format="%d-%b", errors="ignore")
fig_daily = px.line(
    daily_df,
    x="Date",
    y="Hours",
    markers=True,
)
fig_daily.update_layout(
    xaxis_title="Date",
    yaxis_title="Hours",
)
st.plotly_chart(fig_daily, use_container_width=True)
st.dataframe(daily_df[["Date", "Time", "Hours"]])

st.markdown("---")

# -----------------------------
# Executive summary text (short, focused)
# -----------------------------
st.subheader("Executive Insight – Key Loss Drivers")

st.markdown(
    f"""
- **Total downtime:** **{int(total_hours)} hours** ({total_duration})  
- **Primary loss area:** **{top_area['Area']}** with **{top_area['Hours']:.1f} h**.  
- **Top equipment:** **{top_equipment['Equipment']}** with **{top_equipment['Hours']:.1f} h**.  
- **Top machine tag:** **{top_machine['Machine']}** with **{top_machine['Hours']:.1f} h**.  
- **Mechanical share:** **{mech_pct:0.1f}%** vs **Electrical:** **{elect_pct:0.1f}%** of total downtime.  
- **Breakdown vs Corrective:** **{bd_pct:0.1f}% B/D** and **{corr_pct:0.1f}% Corrective**.  
- **Peak days:** visible around **26-Feb**, **23-Feb**, and **11-Feb** on the trend chart.
"""
)
