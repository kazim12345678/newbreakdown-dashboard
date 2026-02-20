import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="SERAC Downtime Dashboard", layout="wide")

st.title("🔧 SERAC Production Line Downtime Dashboard")
st.markdown("### Technical Downtime Analysis (M1 - M9)")

# -----------------------------
# Raw Data
# -----------------------------

data = [
    # M1
    ["M1", "Crates delivery stopped-Tech", 316],
    ["M1", "Filling product valve", 112],
    ["M1", "Filling Station", 70],
    ["M1", "Product Level Low", 34],
    ["M1", "Packer", 30],
    ["M1", "Bottle line conveyor", 21],
    ["M1", "Filling Printer", 15],
    ["M1", "Possimat", 15],
    ["M1", "Crates area / conveyors", 12],
    ["M1", "Crate Stacker", 4],

    # M2
    ["M2", "Crate Stacker", 374],
    ["M2", "Crates delivery stopped-Tech", 239],
    ["M2", "Filler", 169],
    ["M2", "Filling product valve", 85],
    ["M2", "Product Level Low", 73],
    ["M2", "Packer", 52],
    ["M2", "Cap Applicator", 50],
    ["M2", "Bottle guider/Bottle holder/Bottle Screw", 44],
    ["M2", "Conveyor Breakdown", 25],
    ["M2", "Welding work", 23],
    ["M2", "Possimat", 20],
    ["M2", "Bottle line conveyor", 12],
    ["M2", "Outfeed Conveyor", 10],

    # M3
    ["M3", "Crates delivery stopped-Tech", 485],
    ["M3", "Filler", 482],
    ["M3", "Product Level Low", 127],
    ["M3", "Filling product valve", 126],
    ["M3", "Crates area / conveyors", 90],
    ["M3", "Welding work", 77],
    ["M3", "Electrical Motor", 48],
    ["M3", "Bottle guider/Bottle holder/Bottle Screw", 46],
    ["M3", "Filling Station", 41],
    ["M3", "Electrical Sensor", 36],
    ["M3", "Conveyor Breakdown", 28],
    ["M3", "Crate Stacker", 27],
    ["M3", "Possimat", 12],
    ["M3", "Packer", 11],

    # M4
    ["M4", "Crates delivery stopped-Tech", 329],
    ["M4", "Crate Stacker", 220],
    ["M4", "Product Level Low", 98],
    ["M4", "Conveyor Between Packer & Cold Store", 82],
    ["M4", "Crates area / conveyors", 81],
    ["M4", "Divider", 74],
    ["M4", "Filling product valve", 70],
    ["M4", "Packer", 65],
    ["M4", "Crate Conveyor & Pusher C-Loop", 25],
    ["M4", "Automation Fault", 16],
    ["M4", "Welding work", 12],
    ["M4", "Labeling Machine", 5],

    # M6
    ["M6", "Conveyor Breakdown", 93],
    ["M6", "Bottle line conveyor", 56],
    ["M6", "Possimat", 50],
    ["M6", "Axon Machine", 44],
    ["M6", "Filling Nozzle issue", 42],
    ["M6", "Product Level Low", 35],
    ["M6", "Outfeed Conveyor", 30],
    ["M6", "Filling Printer", 18],
    ["M6", "May pack", 17],
    ["M6", "Bottle guider/Bottle holder/Bottle Screw", 8],

    # M7
    ["M7", "Crates delivery stopped-Tech", 270],
    ["M7", "Packer", 125],
    ["M7", "Filling Printer", 104],
    ["M7", "Welding work", 73],
    ["M7", "Filling Station", 45],
    ["M7", "Product Level Low", 25],
    ["M7", "Automation Fault", 23],
    ["M7", "Crate Stacker", 14],

    # M8
    ["M8", "Crates delivery stopped-Tech", 266],
    ["M8", "Packer", 85],
    ["M8", "Crate Conveyor & Pusher C-Loop", 28],
    ["M8", "Product Level Low", 26],
    ["M8", "Filling product valve", 18],
    ["M8", "Filler", 18],
]

df = pd.DataFrame(data, columns=["Machine", "Downtime Type", "Minutes"])

# -----------------------------
# KPI Section
# -----------------------------

total_downtime = df["Minutes"].sum()
total_machines = df["Machine"].nunique()
top_machine = df.groupby("Machine")["Minutes"].sum().idxmax()

col1, col2, col3 = st.columns(3)

col1.metric("Total Downtime (Minutes)", total_downtime)
col2.metric("Total Machines Reported", total_machines)
col3.metric("Highest Downtime Machine", top_machine)

st.markdown("---")

# -----------------------------
# Machine Wise Downtime
# -----------------------------

st.subheader("📊 Machine Wise Total Downtime")

machine_summary = df.groupby("Machine")["Minutes"].sum().sort_values()

fig1, ax1 = plt.subplots()
machine_summary.plot(kind="barh", ax=ax1)
st.pyplot(fig1)

# -----------------------------
# Top 10 Downtime Causes
# -----------------------------

st.subheader("🚨 Top 10 Downtime Causes")

top_causes = df.groupby("Downtime Type")["Minutes"].sum().sort_values(ascending=False).head(10)

fig2, ax2 = plt.subplots()
top_causes.plot(kind="bar", ax=ax2)
st.pyplot(fig2)

# -----------------------------
# Detailed Data View
# -----------------------------

st.subheader("📋 Full Downtime Data Table")
st.dataframe(df)
