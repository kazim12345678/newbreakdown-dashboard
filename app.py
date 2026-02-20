import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import pagesizes
from reportlab.lib.units import inch
import io
import tempfile

st.set_page_config(page_title="SERAC Executive Downtime Dashboard", layout="wide")

st.title("🏭 SERAC DRINKABLE SECTION")
st.markdown("### Technical Downtime Executive Dashboard | Machines M1 - M18")
st.markdown("---")

# =========================
# COMPLETE DATA (ALL MACHINES)
# =========================

data = [
# M1
["M1","Crates delivery stopped-Tech",316],
["M1","Filling product valve",112],
["M1","Filling Station",70],
["M1","Product Level Low_",34],
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
["M2","Product Level Low_",73],
["M2","Packer",52],
["M2","Cap Applicator",50],
["M2","Bottle guider/Bottle holder/Bottle Screw",44],
["M2","Conveyor Breakdown",25],
["M2","Welding work",23],
["M2","Possimat",20],
["M2","Bottle line conveyor",12],
["M2","Outfeed Conveyor of Filling Machine",10],

# M3
["M3","Crates delivery stopped-Tech",485],
["M3","Filler",482],
["M3","Product Level Low_",127],
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
["M4","Product Level Low_",98],
["M4","Conveyor Between Packer & Cold Store",82],
["M4","Crates area / conveyors",81],
["M4","Divider",74],
["M4","Filling product valve",70],
["M4","Packer",65],
["M4","Crate Conveyor & Pusher C-Loop",25],
["M4","Automation_Fault_",16],
["M4","Welding work",12],
["M4","Labeling Machine",5],

# M6
["M6","Conveyor Breakdown",93],
["M6","Bottle line conveyor",56],
["M6","Possimat",50],
["M6","Axon Machine",44],
["M6","Filling Nozzle issue",42],
["M6","Product Level Low_",35],
["M6","Outfeed Conveyor of Filling Machine",30],
["M6","Filling Printer",18],
["M6","May pack",17],
["M6","Bottle guider/Bottle holder/Bottle Screw",8],

# M7
["M7","Crates delivery stopped-Tech",270],
["M7","Packer",125],
["M7","Filling Printer",104],
["M7","Welding work",73],
["M7","Filling Station",45],
["M7","Product Level Low_",25],
["M7","Automation_Fault_",23],
["M7","Crate Stacker",14],

# M8
["M8","Crates delivery stopped-Tech",266],
["M8","Packer",85],
["M8","Crate Conveyor & Pusher C-Loop",28],
["M8","Product Level Low_",26],
["M8","Filling product valve",18],
["M8","Filler",18],

# M9
["M9","Possimat",25],

# M12
["M12","Crates delivery stopped-Tech",108],
["M12","Minor Stopages <10 min",60],
["M12","Lanfranchi Lines",48],
["M12","Filling Station",41],
["M12","Product Level Low_",10],
["M12","Crate Conveyor & Pusher C-Loop",10],
["M12","Crate Stacker",6],

# M13
["M13","Prasmatic Machine",197],
["M13","Product Level Low_",85],
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
["M14","Product Level Low_",127],
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
["M15","Product Level Low_",106],
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
["M16","Product Level Low_",15],

# M17
["M17","Lanfranchi Lines",53],
["M17","Product Level Low_",40],
["M17","Prasmatic Machine",40],
["M17","Cap Applicator",29],
["M17","Downline Breakdown",27],

# M18
["M18","Prasmatic Machine",117],
["M18","Cap Applicator",88],
["M18","Filling Printer",83],
["M18","Product Level Low_",72],
["M18","Lanfranchi Lines",66],
["M18","Emmiti Palletizer",14],
["M18","Bottle guider/Bottle holder/Bottle Screw",12],
]

df = pd.DataFrame(data, columns=["Machine","Downtime Type","Minutes"])

# =========================
# CALCULATIONS
# =========================

total_dt = df["Minutes"].sum()
machine_totals = df.groupby("Machine")["Minutes"].sum().sort_values(ascending=False)
cause_totals = df.groupby("Downtime Type")["Minutes"].sum().sort_values(ascending=False)
avg_dt = machine_totals.mean()

# =========================
# DISPLAY GRAPHS
# =========================

st.subheader("Machine Downtime Ranking")
fig1 = px.bar(machine_totals, x=machine_totals.index, y=machine_totals.values, text=machine_totals.values)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Top 10 Downtime Causes")
pareto = cause_totals.head(10).reset_index()
fig2 = px.bar(pareto, x="Downtime Type", y="Minutes", text="Minutes")
fig2.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig2, use_container_width=True)

# =========================
# PDF EXPORT
# =========================

def generate_pdf():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=pagesizes.A4)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("SERAC Technical Downtime Executive Report", styles["Heading1"]))
    elements.append(Spacer(1, 0.3 * inch))
    elements.append(Paragraph(f"Total Downtime: {total_dt} Minutes", styles["Normal"]))
    elements.append(Paragraph(f"Average Downtime per Machine: {int(avg_dt)} Minutes", styles["Normal"]))
    elements.append(PageBreak())

    # Machine ranking graph
    plt.figure(figsize=(8,4))
    machine_totals.plot(kind="bar")
    plt.title("Machine Downtime Ranking")
    plt.tight_layout()
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    plt.savefig(tmp.name)
    plt.close()
    elements.append(Image(tmp.name, width=6*inch, height=3*inch))
    elements.append(PageBreak())

    # Detailed full table
    elements.append(Paragraph("Complete Downtime Details (All Machines)", styles["Heading2"]))
    elements.append(Spacer(1, 0.3 * inch))

    table_data = [df.columns.tolist()] + df.values.tolist()
    table = Table(table_data, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.grey),
        ('GRID',(0,0),(-1,-1),0.3,colors.black),
        ('FONTSIZE',(0,0),(-1,-1),6)
    ]))
    elements.append(table)

    doc.build(elements)
    buffer.seek(0)
    return buffer

pdf_file = generate_pdf()

st.download_button(
    "Download Complete Executive PDF",
    data=pdf_file,
    file_name="SERAC_Complete_Executive_Report.pdf",
    mime="application/pdf"
)
