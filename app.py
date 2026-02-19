import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import random

# =========================================
# CONFIG
# =========================================
st.set_page_config(page_title="KUTE CMMS", layout="wide")

DB_FILE = "kute.db"
MACHINES = [f"M{i}" for i in range(1, 19)]

# =========================================
# DATABASE INIT
# =========================================
conn = sqlite3.connect(DB_FILE, check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS breakdowns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    machine TEXT,
    category TEXT,
    problem TEXT,
    downtime INTEGER,
    technician TEXT,
    status TEXT
)
""")
conn.commit()

# =========================================
# FAKE DATA GENERATOR (First Run Only)
# =========================================
def generate_fake_data():
    c.execute("SELECT COUNT(*) FROM breakdowns")
    if c.fetchone()[0] == 0:
        techs = ["Ali", "Ahmed", "John", "Khalid", "Rashid"]
        categories = ["Mechanical", "Electrical", "Automation"]
        statuses = ["Open", "Solved"]

        for _ in range(50):
            c.execute("""
            INSERT INTO breakdowns 
            (date, machine, category, problem, downtime, technician, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                (datetime.today() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d"),
                random.choice(MACHINES),
                random.choice(categories),
                "Sample Issue",
                random.randint(10, 180),
                random.choice(techs),
                random.choice(statuses)
            ))
        conn.commit()

generate_fake_data()

# =========================================
# LOGIN SYSTEM
# =========================================
if "logged" not in st.session_state:
    st.session_state.logged = False

if not st.session_state.logged:
    st.title("🔐 KUTE Login")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == "admin" and pwd == "1234":
            st.session_state.logged = True
            st.rerun()
        else:
            st.error("Wrong Credentials")
    st.stop()

# =========================================
# LOAD DATA
# =========================================
df = pd.read_sql("SELECT * FROM breakdowns", conn)

# =========================================
# HEADER STYLE
# =========================================
st.markdown("""
<style>
.tile {
    padding:20px;
    border-radius:15px;
    text-align:center;
    font-weight:bold;
    font-size:18px;
    color:white;
}
</style>
""", unsafe_allow_html=True)

st.title("KUTE CMMS Dashboard")

# =========================================
# KPI SECTION
# =========================================
total = len(df)
open_jobs = len(df[df["status"] == "Open"])
solved = len(df[df["status"] == "Solved"])

total_downtime = df["downtime"].sum()
mttr = round(total_downtime / solved, 2) if solved > 0 else 0
mtbf = round((30*24*60) / total, 2) if total > 0 else 0

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Breakdown", total)
k2.metric("Open Jobs", open_jobs)
k3.metric("MTTR (min)", mttr)
k4.metric("MTBF (min)", mtbf)

st.divider()

# =========================================
# MACHINE COLOR TILES
# =========================================
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
        if st.button(machine):
            st.session_state.selected_machine = machine

        st.markdown(
            f"<div class='tile' style='background:{color};'>{machine}<br>{downtime} min</div>",
            unsafe_allow_html=True
        )

# =========================================
# CLICKABLE MACHINE POPUP
# =========================================
if "selected_machine" in st.session_state:
    sm = st.session_state.selected_machine
    st.subheader(f"Breakdowns for {sm}")

    machine_df = df[df["machine"] == sm]
    st.dataframe(machine_df)

# =========================================
# ADD NEW BREAKDOWN
# =========================================
st.divider()
st.subheader("Add Breakdown")

with st.form("add_form"):
    date = st.date_input("Date", datetime.today())
    machine = st.selectbox("Machine", MACHINES)
    category = st.selectbox("Category", ["Mechanical", "Electrical", "Automation"])
    problem = st.text_input("Problem")
    downtime = st.number_input("Downtime (minutes)", 0)
    technician = st.text_input("Technician")
    status = st.selectbox("Status", ["Open", "Solved"])

    submit = st.form_submit_button("Save")

    if submit:
        c.execute("""
        INSERT INTO breakdowns 
        (date, machine, category, problem, downtime, technician, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (date, machine, category, problem, downtime, technician, status))
        conn.commit()
        st.success("Saved")
        st.rerun()

# =========================================
# EDIT / DELETE
# =========================================
st.divider()
st.subheader("Edit / Delete Records")

st.dataframe(df)

delete_id = st.number_input("Enter ID to Delete", 0)

if st.button("Delete Record"):
    c.execute("DELETE FROM breakdowns WHERE id = ?", (delete_id,))
    conn.commit()
    st.success("Deleted")
    st.rerun()
