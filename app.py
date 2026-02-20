df = pd.DataFrame(data, columns=["Machine","Downtime Type","Minutes"])

# ================= BASIC CALC =================

total_dt = df["Minutes"].sum()
machine_totals = df.groupby("Machine")["Minutes"].sum()
cause_totals = df.groupby("Downtime Type")["Minutes"].sum()
avg_dt = machine_totals.mean()

machine_analysis = machine_totals.reset_index()
machine_analysis.columns = ["Machine","Total_DT"]
machine_analysis["% Plant DT"] = (machine_analysis["Total_DT"] / total_dt * 100).round(2)
machine_analysis["Above Avg"] = machine_analysis["Total_DT"] > avg_dt

def classify(row):
    if row["% Plant DT"] > 10:
        return "CRITICAL"
    elif row["% Plant DT"] > 7:
        return "HIGH"
    elif row["% Plant DT"] > 4:
        return "MEDIUM"
    else:
        return "LOW"

machine_analysis["Criticality"] = machine_analysis.apply(classify, axis=1)
machine_analysis = machine_analysis.sort_values("Total_DT", ascending=False)

# ================= ROOT CAUSE GROUPING =================

def group_issue(x):
    x = x.lower()
    if "crate" in x:
        return "Crate System"
    elif "fill" in x or "level" in x or "nozzle" in x:
        return "Filling System"
    elif "conveyor" in x:
        return "Conveyor System"
    elif "cap" in x:
        return "Cap System"
    elif "prasmatic" in x or "lanfranchi" in x or "palletizer" in x:
        return "Downstream System"
    elif "motor" in x or "sensor" in x or "electrical" in x:
        return "Electrical System"
    else:
        return "Other"

df["System Group"] = df["Downtime Type"].apply(group_issue)
group_totals = df.groupby("System Group")["Minutes"].sum().sort_values(ascending=False)

# ================= TRUE PARETO =================

pareto_df = cause_totals.sort_values(ascending=False).reset_index()
pareto_df["Cumulative %"] = pareto_df["Minutes"].cumsum() / total_dt * 100

fig_pareto = go.Figure()
fig_pareto.add_bar(x=pareto_df["Downtime Type"][:10],
                   y=pareto_df["Minutes"][:10],
                   name="Minutes")

fig_pareto.add_scatter(x=pareto_df["Downtime Type"][:10],
                       y=pareto_df["Cumulative %"][:10],
                       name="Cumulative %",
                       yaxis="y2")

fig_pareto.update_layout(
    yaxis2=dict(overlaying='y', side='right'),
    xaxis_tickangle=-45
)

st.subheader("True Pareto Analysis")
st.plotly_chart(fig_pareto, use_container_width=True)

# ================= MACHINE CRITICALITY TABLE =================

st.subheader("Machine Criticality Analysis")
st.dataframe(machine_analysis)

# ================= SYSTEM CONTRIBUTION =================

st.subheader("System Level Contribution")
fig_sys = px.pie(group_totals, values=group_totals.values,
                 names=group_totals.index)
st.plotly_chart(fig_sys)

# ================= PDF WITH INSIGHTS =================

def generate_pdf():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=pagesizes.A4)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("SERAC Advanced Technical Downtime Analysis", styles["Heading1"]))
    elements.append(Spacer(1,0.3*inch))

    elements.append(Paragraph(f"Total Plant Downtime: {total_dt} Minutes", styles["Normal"]))
    elements.append(Paragraph(f"Average per Machine: {int(avg_dt)} Minutes", styles["Normal"]))
    elements.append(Spacer(1,0.3*inch))

    elements.append(Paragraph("Machine Criticality Ranking:", styles["Heading2"]))
    elements.append(Spacer(1,0.2*inch))

    table_data = [machine_analysis.columns.tolist()] + machine_analysis.values.tolist()
    table = Table(table_data, repeatRows=1)
    table.setStyle(TableStyle([
        ('GRID',(0,0),(-1,-1),0.3,colors.black),
        ('BACKGROUND',(0,0),(-1,0),colors.grey),
        ('FONTSIZE',(0,0),(-1,-1),7)
    ]))
    elements.append(table)
    elements.append(PageBreak())

    elements.append(Paragraph("System Level Downtime Contribution:", styles["Heading2"]))
    elements.append(Spacer(1,0.2*inch))

    for system, value in group_totals.items():
        percent = round(value/total_dt*100,2)
        elements.append(Paragraph(f"{system}: {value} Minutes ({percent}%)", styles["Normal"]))

    doc.build(elements)
    buffer.seek(0)
    return buffer

pdf_file = generate_pdf()

st.download_button("Download Advanced Executive Analysis PDF",
                   data=pdf_file,
                   file_name="SERAC_Advanced_Analysis.pdf",
                   mime="application/pdf")
