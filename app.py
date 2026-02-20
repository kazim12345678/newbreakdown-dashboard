import streamlit as st
import pandas as pd
import plotly.express as px
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import pagesizes
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
import io

st.set_page_config(page_title="SERAC Executive Downtime Dashboard", layout="wide")

# -----------------------------
# STYLE (Professional Look)
# -----------------------------
st.markdown("""
<style>
.main {
    background-color: #0e1117;
}
h1, h2, h3 {
    color: white;
}
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
# RAW DATA  (YOUR SAME DATA)
# -----------------------------
data = [
# (YOUR FULL DATA REMAINS SAME — NOT CHANGED)
]

df = pd.DataFrame(data, columns=["Machine","Downtime Type","Minutes"])

# -----------------------------
# KPIs
# -----------------------------
total_dt = df["Minutes"].sum()
machines = df["Machine"].nunique()
top_machine = df.groupby("Machine")["Minutes"].sum().idxmax()

col1,col2,col3 = st.columns(3)
col1.metric("Total Downtime (Minutes)", f"{total_dt:,}")
col2.metric("Total Machines", machines)
col3.metric("Highest Downtime Machine", top_machine)

st.markdown("---")

# -----------------------------
# Machine Ranking
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

fig1.update_layout(
    template="plotly_dark",
    xaxis_title="Machine",
    yaxis_title="Downtime (Minutes)"
)

st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# Pareto Chart
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

fig2.update_layout(
    template="plotly_dark",
    xaxis_tickangle=-45,
    yaxis_title="Downtime (Minutes)"
)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# Detailed Table
# -----------------------------
st.subheader("📋 Detailed Downtime Data")
st.dataframe(df, use_container_width=True)

# -----------------------------
# PDF DOWNLOAD
# -----------------------------
def generate_pdf(dataframe):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=pagesizes.A4)
    elements = []

    styles = getSampleStyleSheet()
    elements.append(Paragraph("SERAC Technical Downtime Report", styles["Heading1"]))
    elements.append(Spacer(1, 0.3 * inch))

    table_data = [dataframe.columns.tolist()] + dataframe.values.tolist()
    table = Table(table_data)

    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('FONTSIZE', (0,0), (-1,-1), 7)
    ]))

    elements.append(table)
    doc.build(elements)

    buffer.seek(0)
    return buffer

pdf_file = generate_pdf(df)

st.download_button(
    label="⬇ Download Full Report as PDF",
    data=pdf_file,
    file_name="SERAC_Downtime_Report.pdf",
    mime="application/pdf"
)
