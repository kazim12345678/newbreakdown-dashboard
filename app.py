import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="SERAC Executive Downtime Dashboard", layout="wide")

st.title("🏭 SERAC DRINKABLE SECTION - Technical Downtime Dashboard")
st.markdown("### Executive Overview | Machines M1 - M18")

# -----------------------------
# RAW DATA
# -----------------------------

data = [

# M1
["M1","Crates delivery stopped-Tech",316],
["M1","Filling product valve",112],
["M1","Filling Station",70],
["M1","Product Level Low",34],
["M1","Packer",30],
["M1","Bottle line conveyor",21],
["M1","Filling Printer",15],
["M1","Possimat",15],
["M1","Crates area / conveyors",12],
["M1","Crate Stacker",4],

# M2
["M2","Crate Stacker",374],
["M2","Crates delivery stopped-Tech",239],
["M2","Filler",169],
["M2","Filling product valve",85],
["M2","Product Level Low",73],
["M2","Packer",52],
["M2","Cap Applicator",50],
["M2","Bottle guider/Bottle holder/Bottle Screw",44],
["M2","Conveyor Breakdown",25],
["M2","Welding work",23],
["M2","Possimat",20],
["M2","Bottle line conveyor",12],
["M2","Outfeed Conveyor",10],

# M3
["M3","Crates delivery stopped-Tech",485],
["M3","Filler",482],
["M3","Product Level Low",127],
["M3","Filling product valve",126],
["M3","Crates area / conveyors",90],
["M3","Welding work",77],
["M3","Electrical Motor",48],
["M3","Bottle guider/Bottle holder/Bottle Screw",46],
["M3","Filling Station",41],
["M3","Electrical Sensor",36],
["M3","Conveyor Breakdown",28],
["M3","Crate Stacker",27],
["M3","Possimat",12],
["M3","Packer",11],

# M4
["M4","Crates delivery stopped-Tech",329],
["M4","Crate Stacker",220],
["M4","Product Level Low",98],
["M4","Conveyor Between Packer & Cold Store",82],
["M4","Crates area / conveyors",81],
["M4","Divider",74],
["M4","Filling product valve",70],
["M4","Packer",65],
["M4","Crate Conveyor & Pusher C-Loop",25],
["M4","Automation Fault",16],
["M4","Welding work",12],
["M4","Labeling Machine",5],

# M6
["M6","Conveyor Breakdown",93],
["M6","Bottle line conveyor",56],
["M6","Possimat",50],
["M6","Axon Machine",44],
["M6","Filling Nozzle issue",42],
["M6","Product Level Low",35],
["M6","Outfeed Conveyor",30],
["M6","Filling Printer",18],
["M6","May pack",17],
["M6","Bottle guider/Bottle holder/Bottle Screw",8],

# M7
["M7","Crates delivery stopped-Tech",270],
["M7","Packer",125],
["M7","Filling Printer",104],
["M7","Welding work",73],
["M7","Filling Station",45],
["M7","Product Level Low",25],
["M7","Automation Fault",23],
["M7","Crate Stacker",14],

# M8
["M8","Crates delivery stopped-Tech",266],
["M8","Packer",85],
["M8","Crate Conveyor & Pusher C-Loop",28],
["M8","Product Level Low",26],
["M8","Filling product valve",18],
["M8","Filler",18],

# M9
["M9","Possimat",25],

# M12
["M12","Crates delivery stopped-Tech",108],
["M12","Minor Stopages <10 min",60],
["M12","Lanfranchi Lines",48],
["M12","Filling Station",41],
["M12","Product Level Low",10],
["M12","Crate Conveyor & Pusher C-Loop",10],
["M12","Crate Stacker",6],

# M13
["M13","Prasmatic Machine",197],
["M13","Product Level Low",85],
["M13","Lanfranchi Lines",85],
["M13","Cap Dispensor",33],
["M13","Filling Printer",32],
["M13","Filling product valve",20],
["M13","Bottle guider/Bottle holder/Bottle Screw",18],
["M13","Cap Applicator",15],
["M13","Filling Station",15],

# M14
["M14","Temperature of Heater",293],
["M14","Prasmatic Machine",238],
["M14","Bottle guider/Bottle holder/Bottle Screw",195],
["M14","Product Level Low",127],
["M14","Cap Sealing",55],
["M14","Lanfranchi Lines",50],
["M14","Emmiti Palletizer",40],
["M14","Bottom plate spring",30],
["M14","Bottom Film Cutter",25],
["M14","Filler",14],
["M14","Filling Printer",10],
["M14","Bottle line conveyor",5],

# M15
["M15","Sipack Packer / Crates Packer",367],
["M15","Crates delivery stopped-Tech",257],
["M15","Possimat",240],
["M15","Product Level Low",106],
["M15","Bottle guider/Bottle holder/Bottle Screw",72],
["M15","Filling Station",52],
["M15","Conveyor Between Packer & Cold Store",47],
["M15","Electrical Dosing Pump",32],
["M15","Crates area / conveyors",21],
["M15","Filling Printer",18],
["M15","Bottle line conveyor",15],
["M15","Lanfranchi Lines",15],
["M15","conveyor overload",14],
["M15","Conveyor Breakdown",12],
["M15","Crate Stacker",12],
["M15","Cap Applicator",10],

# M16
["M16","Cap Applicator",271],
["M16","Prasmatic Machine",216],
["M16","Cap Dispensor",80],
["M16","Lanfranchi Lines",55],
["M16","Glue Applying Machine",20],
["M16","Bottle guider/Bottle holder/Bottle Screw",19],
["M16","Product Level Low",15],

# M17
["M17","Lanfranchi Lines",53],
["M17","Product Level Low",40],
["M17","Prasmatic Machine",40],
["M17","Cap Applicator",29],
["M17","Downline Breakdown",27],

# M18
["M18","Prasmatic Machine",117],
["M18","Cap Applicator",88],
["M18","Filling Printer",83],
["M18","Product Level Low",72],
["M18","Lanfranchi Lines",66],
["M18","Emmiti Palletizer",14],
["M18","Bottle guider/Bottle holder/Bottle Screw",12],

]

df = pd.DataFrame(data, columns=["Machine","Downtime Type","Minutes"])

# -----------------------------
# KPIs
# -----------------------------
total_dt = df["Minutes"].sum()
machines = df["Machine"].nunique()
top_machine = df.groupby("Machine")["Minutes"].sum().idxmax()

col1,col2,col3 = st.columns(3)
col1.metric("Total Downtime (Min)", total_dt)
col2.metric("Total Machines", machines)
col3.metric("Highest Downtime Machine", top_machine)

st.markdown("---")

# -----------------------------
# Machine Ranking
# -----------------------------
st.subheader("🔴 Machine Downtime Ranking")

machine_sum = df.groupby("Machine")["Minutes"].sum().sort_values(ascending=False)
fig1 = px.bar(machine_sum,
              x=machine_sum.index,
              y=machine_sum.values,
              color=machine_sum.values,
              color_continuous_scale="Reds")

st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# Pareto Chart
# -----------------------------
st.subheader("📊 Pareto Analysis - Top Downtime Causes")

cause_sum = df.groupby("Downtime Type")["Minutes"].sum().sort_values(ascending=False)
pareto_df = cause_sum.reset_index()

fig2 = px.bar(pareto_df.head(10),
              x="Downtime Type",
              y="Minutes",
              color="Minutes",
              color_continuous_scale="Blues")

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# Detailed Table
# -----------------------------
st.subheader("📋 Detailed Data")
st.dataframe(df)
