import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import hashlib
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import os
import smtplib
from email.mime.text import MIMEText

# =========================================
# CONFIG
# =========================================
st.set_page_config(page_title="KUTE Enterprise CMMS+", layout="wide")

DB_FILE = "kute_enterprise.db"
MACHINES = [f"M{i}" for i in range(1, 19)]

# =========================================
# DARK MODE TOGGLE
# =========================================
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

dark_toggle = st.sidebar.toggle("🌙 Dark Mode")

if dark_toggle:
    st.markdown("""
        <style>
        body { background-color: #111 !important; color: white !important; }
        </style>
    """, unsafe_allow_html=True)

# =========================================
# DATABASE
# =========================================
conn = sqlite3.connect(DB_FILE, check_same_thread=False)
df = pd.read_sql("SELECT * FROM breakdowns", conn)
pm_df = pd.read_sql("SELECT * FROM pm_schedule", conn)

# =========================================
# KPI CALCULATIONS
# =========================================
total = len(df)
open_jobs = len(df[df["status"] == "Open"])
solved = len(df[df["status"] == "Solved"])
total_downtime = df["downtime"].sum()

mttr = round(total_downtime / solved, 2) if solved else 0
mtbf = round((30*24*60) / total, 2) if total else 0
availability = round((mtbf / (mtbf + mttr)) * 100, 2) if mtbf+mttr > 0 else 0

# =========================================
# HEADER
# =========================================
st.title("KUTE Enterprise CMMS+")
st.subheader("Executive Maintenance Intelligence System")

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Breakdown", total)
k2.metric("Open Jobs", open_jobs)
k3.metric("MTTR (min)", mttr)
k4.metric("MTBF (min)", mtbf)
k5.metric("Availability %", availability)

# =========================================
# ALERT SYSTEM
# =========================================
if open_jobs > 10:
    st.error("⚠ High number of open jobs!")

today = datetime.today().date()

if not pm_df.empty:
    pm_df["next_due"] = pd.to_datetime(pm_df["next_due"]).dt.date
    overdue = pm_df[pm_df["next_due"] < today]

    if not overdue.empty:
        st.warning("⚠ Some PM tasks are overdue!")

# =========================================
# MACHINE STATUS TILES
# =========================================
st.divider()
st.subheader("Machine Status Overview")

cols = st.columns(6)

for i, machine in enumerate(MACHINES):
    machine_data = df[df["machine"] == machine]
    downtime = machine_data["downtime"].sum()

    if downtime > 300:
        color = "red"
    elif downtime > 120:
        color = "orange"
    else:
        color = "green"

    with cols[i % 6]:
        st.markdown(
            f"<div style='background:{color};padding:15px;border-radius:10px;color:white;text-align:center;font-weight:bold;'>{machine}<br>{downtime} min</div>",
            unsafe_allow_html=True
        )

# =========================================
# PDF EXPORT FUNCTION
# =========================================
def generate_pdf():
    file_path = "KUTE_Report.pdf"
    doc = SimpleDocTemplate(file_path)
    elements = []

    styles = getSampleStyleSheet()
    elements.append(Paragraph("KUTE Maintenance Report", styles["Title"]))
    elements.append(Spacer(1, 0.5 * inch))

    data = [
        ["Total Breakdown", total],
        ["Open Jobs", open_jobs],
        ["MTTR", mttr],
        ["MTBF", mtbf],
        ["Availability %", availability]
    ]

    table = Table(data)
    elements.append(table)

    doc.build(elements)
    return file_path

if st.button("📄 Generate PDF Report"):
    pdf_path = generate_pdf()
    with open(pdf_path, "rb") as f:
        st.download_button("Download Report", f, file_name="KUTE_Report.pdf")

# =========================================
# EMAIL ALERT FUNCTION (SMTP READY)
# =========================================
def send_email_alert():
    sender = "your_email@gmail.com"
    password = "your_app_password"
    receiver = "manager_email@gmail.com"

    msg = MIMEText("KUTE Alert: High open jobs or PM overdue.")
    msg["Subject"] = "KUTE Maintenance Alert"
    msg["From"] = sender
    msg["To"] = receiver

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, password)
    server.send_message(msg)
    server.quit()

if st.button("📧 Send Alert Email"):
    st.info("Configure SMTP credentials in code to enable real email sending.")
    # Uncomment below after adding real credentials
    # send_email_alert()

st.success("Enterprise+ System Running Successfully")
