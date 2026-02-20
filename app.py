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

# -----------------------------
# TITLE
# -----------------------------
st.title("🏭 SERAC DRINKABLE SECTION")
st.markdown("### Technical Downtime Executive Dashboard | Machines M1 - M18")
st.markdown("---")

# -----------------------------
# YOUR FULL ORIGINAL DATA
# -----------------------------
data = [
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
# 🔴 PASTE THE REST OF YOUR ORIGINAL DATA HERE (UNCHANGED)
]

df = pd.DataFrame(data, columns=["Machine","Downtime Type","Minutes"])

# -----------------------------
# KPI CALCULATIONS
# -----------------------------
total_dt = df["Minutes"].sum()
machines = df["Machine"].nunique()
machine_totals = df.groupby("Machine")["Minutes"].sum().sort_values(ascending=False)
avg_dt = machine_totals.mean()

top_machine = machine_totals.idxmax()
top_machine_value = machine_totals.max()

cause_totals = df.groupby("Downtime Type")["Minutes"].sum().sort_values(ascending=False)
top_causes = cause_totals.head(5)

# -----------------------------
# KPIs DISPLAY
# -----------------------------
col1,col2,col3,col4 = st.columns(4)
col1.metric("Total Downtime (Min)", f"{total_dt:,}")
col2.metric("Total Machines", machines)
col3.metric("Highest DT Machine", top_machine)
col4.metric("Average DT / Machine", f"{int(avg_dt)}")

st.markdown("---")

# -----------------------------
# MACHINE RANKING GRAPH
# -----------------------------
st.subheader("🔴 Machine Downtime Ranking")

fig1 = px.bar(machine_totals,
              x=machine_totals.index,
              y=machine_totals.values,
              color=machine_totals.values,
              color_continuous_scale="Reds",
              text=machine_totals.values)

fig1.update_layout(template="plotly_dark")
st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# PARETO GRAPH
# -----------------------------
st.subheader("📊 Pareto Analysis – Top Downtime Causes")

pareto_df = cause_totals.reset_index().head(10)

fig2 = px.bar(pareto_df,
              x="Downtime Type",
              y="Minutes",
              color="Minutes",
              color_continuous_scale="Blues",
              text="Minutes")

fig2.update_layout(template="plotly_dark", xaxis_tickangle=-45)
st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# MACHINE SUMMARY TABLE
# -----------------------------
st.subheader("📋 Machine-wise Top 3 Issues")

machine_summary = []

for m in df["Machine"].unique():
    temp = df[df["Machine"] == m]
    total_m = temp["Minutes"].sum()
    top3 = temp.sort_values("Minutes", ascending=False).head(3)
    for _, row in top3.iterrows():
        percent = round((row["Minutes"] / total_m) * 100,1)
        machine_summary.append([m, total_m, row["Downtime Type"], row["Minutes"], f"{percent}%"])

summary_df = pd.DataFrame(machine_summary,
                          columns=["Machine","Total DT","Top Issue","Minutes","% of Machine DT"])

st.dataframe(summary_df, use_container_width=True)

# -----------------------------
# PDF GENERATION
# -----------------------------
def generate_pdf():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=pagesizes.A4)
    elements = []
    styles = getSampleStyleSheet()

    # PAGE 1 – EXECUTIVE SUMMARY
    elements.append(Paragraph("SERAC Technical Downtime Executive Report", styles["Heading1"]))
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph(f"Total Downtime: {total_dt} Minutes", styles["Normal"]))
    elements.append(Paragraph(f"Total Machines: {machines}", styles["Normal"]))
    elements.append(Paragraph(f"Highest Downtime Machine: {top_machine} ({top_machine_value} Minutes)", styles["Normal"]))
    elements.append(Paragraph(f"Average Downtime per Machine: {int(avg_dt)} Minutes", styles["Normal"]))
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph("Top 5 Downtime Contributors:", styles["Heading3"]))
    for cause, val in top_causes.items():
        elements.append(Paragraph(f"- {cause} : {val} Minutes", styles["Normal"]))

    elements.append(PageBreak())

    # PAGE 2 – MACHINE RANKING GRAPH
    plt.figure(figsize=(8,4))
    machine_totals.plot(kind="bar")
    plt.title("Machine Downtime Ranking")
    plt.ylabel("Minutes")
    plt.tight_layout()

    tmp1 = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    plt.savefig(tmp1.name)
    plt.close()

    elements.append(Paragraph("Machine Downtime Ranking", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Image(tmp1.name, width=6*inch, height=3*inch))

    elements.append(PageBreak())

    # PAGE 3 – PARETO GRAPH
    plt.figure(figsize=(8,4))
    pareto_df.set_index("Downtime Type")["Minutes"].plot(kind="bar")
    plt.title("Top Downtime Causes")
    plt.ylabel("Minutes")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    tmp2 = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    plt.savefig(tmp2.name)
    plt.close()

    elements.append(Paragraph("Pareto – Top Downtime Causes", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Image(tmp2.name, width=6*inch, height=3*inch))

    elements.append(PageBreak())

    # PAGE 4 – MACHINE SUMMARY TABLE
    elements.append(Paragraph("Machine-wise Top 3 Issues", styles["Heading2"]))
    elements.append(Spacer(1, 0.3 * inch))

    table_data = [summary_df.columns.tolist()] + summary_df.values.tolist()
    table = Table(table_data, repeatRows=1)

    table.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.grey),
        ('GRID',(0,0),(-1,-1),0.5,colors.black),
        ('FONTSIZE',(0,0),(-1,-1),8)
    ]))

    elements.append(table)

    doc.build(elements)
    buffer.seek(0)
    return buffer

pdf_file = generate_pdf()

st.download_button(
    label="⬇ Download Executive PDF Report",
    data=pdf_file,
    file_name="SERAC_Executive_Downtime_Report.pdf",
    mime="application/pdf"
)
