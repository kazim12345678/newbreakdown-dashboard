import streamlit as st
import pandas as pd
import plotly.express as px
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import pagesizes
from reportlab.lib.units import inch
import io
import tempfile

st.set_page_config(page_title="SERAC Executive Downtime Dashboard", layout="wide")

# -----------------------------
# STYLE
# -----------------------------
st.markdown("""
<style>
.main {background-color: #0e1117;}
h1, h2, h3 {color: white;}
div[data-testid="metric-container"] {
    background-color: #1f2937;
    padding: 20px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("🏭 SERAC DRINKABLE SECTION")
st.markdown("### Technical Downtime Executive Dashboard | Machines M1 - M18")
st.markdown("---")

# -----------------------------
# RAW DATA (YOUR FULL DATA HERE — KEEP SAME)
# -----------------------------
data = [
# ⬇⬇⬇ KEEP YOUR COMPLETE MACHINE DATA HERE EXACTLY SAME ⬇⬇⬇
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
# ---- KEEP REST OF YOUR DATA UNCHANGED ----
]

df = pd.DataFrame(data, columns=["Machine","Downtime Type","Minutes"])

# -----------------------------
# KPIs (SAFE FIX)
# -----------------------------
total_dt = df["Minutes"].sum()
machines = df["Machine"].nunique()

machine_totals = df.groupby("Machine")["Minutes"].sum()
top_machine = machine_totals.idxmax() if not machine_totals.empty else "No Data"

col1,col2,col3 = st.columns(3)
col1.metric("Total Downtime (Minutes)", f"{total_dt:,}")
col2.metric("Total Machines", machines)
col3.metric("Highest Downtime Machine", top_machine)

st.markdown("---")

# -----------------------------
# MACHINE RANKING
# -----------------------------
st.subheader("🔴 Machine Downtime Ranking")

machine_sum = df.groupby("Machine")["Minutes"].sum().sort_values(ascending=False)

fig1 = px.bar(
    machine_sum,
    x=machine_sum.index,
    y=machine_sum.values,
    color=machine_sum.values,
    color_continuous_scale="Reds",
    text=machine_sum.values
)
fig1.update_layout(template="plotly_dark")

st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# PARETO CHART
# -----------------------------
st.subheader("📊 Pareto Analysis - Top 10 Downtime Causes")

cause_sum = df.groupby("Downtime Type")["Minutes"].sum().sort_values(ascending=False)
pareto_df = cause_sum.reset_index()

fig2 = px.bar(
    pareto_df.head(10),
    x="Downtime Type",
    y="Minutes",
    color="Minutes",
    color_continuous_scale="Blues",
    text="Minutes"
)
fig2.update_layout(template="plotly_dark", xaxis_tickangle=-45)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# TABLE
# -----------------------------
st.subheader("📋 Detailed Downtime Data")
st.dataframe(df, use_container_width=True)

# -----------------------------
# PDF GENERATION (WITH CHARTS + KPIs)
# -----------------------------
def generate_pdf():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=pagesizes.A4)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("SERAC Technical Downtime Executive Report", styles["Heading1"]))
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph(f"Total Downtime: {total_dt} Minutes", styles["Normal"]))
    elements.append(Paragraph(f"Total Machines: {machines}", styles["Normal"]))
    elements.append(Paragraph(f"Highest Downtime Machine: {top_machine}", styles["Normal"]))
    elements.append(Spacer(1, 0.3 * inch))

    # Save charts as images
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp1:
        fig1.write_image(tmp1.name)
        elements.append(Image(tmp1.name, width=6*inch, height=3*inch))
        elements.append(Spacer(1, 0.3 * inch))

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp2:
        fig2.write_image(tmp2.name)
        elements.append(Image(tmp2.name, width=6*inch, height=3*inch))
        elements.append(Spacer(1, 0.3 * inch))

    # Add table
    table_data = [df.columns.tolist()] + df.values.tolist()
    table = Table(table_data, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('FONTSIZE', (0,0), (-1,-1), 6)
    ]))

    elements.append(table)
    doc.build(elements)

    buffer.seek(0)
    return buffer

pdf_file = generate_pdf()

st.download_button(
    label="⬇ Download Complete Executive PDF Report",
    data=pdf_file,
    file_name="SERAC_Executive_Downtime_Report.pdf",
    mime="application/pdf"
)
