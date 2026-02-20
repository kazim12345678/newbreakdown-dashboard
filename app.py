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
st.title(" SERAC DRINKABLE SECTION – Technical Downtime Analysis")
st.markdown("### Mobile‑Friendly Optimized Dashboard")
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
# CALCULATIONS
# ----------------------------------------------------
total_dt = df["Minutes"].sum()
machine_totals = df.groupby("Machine")["Minutes"].sum().sort_values(ascending=False)
cause_totals = df.groupby("Downtime Type")["Minutes"].sum().sort_values(ascending=False)
avg_dt = machine_totals.mean()

machine_analysis = machine_totals.reset_index()
machine_analysis.columns = ["Machine","Total DT"]
machine_analysis["% Plant Impact"] = (machine_analysis["Total DT"]/total_dt*100).round(2)
machine_analysis["Above Average"] = machine_analysis["Total DT"] > avg_dt

# ----------------------------------------------------
# MACHINE RANKING
# ----------------------------------------------------
st.subheader("📊 Machine Criticality Ranking")

with st.expander("View Machine Ranking Table"):
    st.dataframe(machine_analysis, use_container_width=True, height=350)

fig1 = px.bar(
    machine_totals,
    x=machine_totals.index,
    y=machine_totals.values,
    text=machine_totals.values,
    title="Machine Downtime Ranking",
)
fig1.update_layout(xaxis_title="Machine", yaxis_title="Minutes", height=450)
st.plotly_chart(fig1, use_container_width=True)

# ----------------------------------------------------
# PARETO
# ----------------------------------------------------
st.subheader("📉 True Pareto Analysis (Top 10 Causes)")

pareto = cause_totals.reset_index()
pareto["Cumulative %"] = pareto["Minutes"].cumsum() / total_dt * 100

fig2 = go.Figure()
fig2.add_bar(x=pareto["Downtime Type"][:10], y=pareto["Minutes"][:10], name="Minutes")
fig2.add_scatter(
    x=pareto["Downtime Type"][:10],
    y=pareto["Cumulative %"][:10],
    yaxis="y2",
    name="Cumulative %",
    mode="lines+markers",
)

fig2.update_layout(
    yaxis2=dict(overlaying="y", side="right"),
    xaxis_tickangle=-45,
    height=450
)

st.plotly_chart(fig2, use_container_width=True)

# ----------------------------------------------------
# PDF EXPORT
# ----------------------------------------------------
@st.cache_data
def generate_pdf():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=pagesizes.A4)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("SERAC Advanced Technical Downtime Report", styles["Heading1"]))
    elements.append(Spacer(1, 0.3 * inch))
    elements.append(Paragraph(f"Total Plant Downtime: {total_dt} Minutes", styles["Normal"]))
    elements.append(Paragraph(f"Average per Machine: {int(avg_dt)} Minutes", styles["Normal"]))
    elements.append(PageBreak())

    table_data = [machine_analysis.columns.tolist()] + machine_analysis.values.tolist()
    table = Table(table_data, repeatRows=1)
    table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.3, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('FONTSIZE', (0,0), (-1,-1), 7)
    ]))
    elements.append(table)

    doc.build(elements)
    buffer.seek(0)
    return buffer

pdf_file = generate_pdf()

st.download_button(
    "📥 Download Executive PDF Report",
    data=pdf_file,
    file_name="SERAC_Advanced_Report.pdf",
    mime="application/pdf"
)
