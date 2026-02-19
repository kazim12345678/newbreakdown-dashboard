import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import hashlib
import random

# =========================================
# CONFIG
# =========================================
st.set_page_config(page_title="KUTE Enterprise CMMS", layout="wide")
DB_FILE = "kute_enterprise.db"
MACHINES = [f"M{i}" for i in range(1, 19)]

# =========================================
# DATABASE
# =========================================
conn = sqlite3.connect(DB_FILE, check_same_thread=False)
c = conn.cursor()

# USERS TABLE
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    role TEXT
)
""")

# BREAKDOWNS TABLE
c.execute("""
CREATE TABLE IF NOT EXISTS breakdowns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    machine TEXT,
    category TEXT,
    problem TEXT,
    downtime INTEGER,
    technician TEXT,
    status TEXT,
    start_time TEXT,
    end_time TEXT
)
""")

# PM TABLE
c.execute("""
CREATE TABLE IF NOT EXISTS pm_schedule (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    machine TEXT,
    pm_type TEXT,
    last_done TEXT,
    next_due TEXT,
    status TEXT
)
""")

conn.commit()

# =========================================
# CREATE DEFAULT USERS
# =========================================
def hash_pwd(p):
    return hashlib.sha256(p.encode()).hexdigest()

def create_default_users():
    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] == 0:
        users = [
            ("admin", hash_pwd("1234"), "Admin"),
            ("manager", hash_pwd("1111"), "Manager"),
            ("ali", hash_pwd("0000"), "Technician"),
        ]
        c.executemany("INSERT INTO users (username,password,role) VALUES (?,?,?)", users)
        conn.commit()

create_default_users()

# =========================================
# LOGIN SYSTEM
# =========================================
if "logged" not in st.session_state:
    st.session_state.logged = False

if not st.session_state.logged:
    st.title("🔐 KUTE Enterprise Login")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        hashed = hash_pwd(pwd)
        result = c.execute(
            "SELECT role FROM users WHERE username=? AND password=?",
            (user, hashed)
        ).fetchone()

        if result:
            st.session_state.logged = True
            st.session_state.role = result[0]
            st.session_state.username = user
            st.rerun()
        else:
            st.error("Invalid Credentials")

    st.stop()

# =========================================
# LOAD DATA
# =========================================
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
st.title("KUTE Enterprise CMMS")
st.write(f"Logged in as: **{st.session_state.username} ({st.session_state.role})**")

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Breakdown", total)
k2.metric("Open Jobs", open_jobs)
k3.metric("MTTR (min)", mttr)
k4.metric("MTBF (min)", mtbf)
k5.metric("Availability %", availability)

st.divider()

# =========================================
# MACHINE STATUS TILES
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
            f"<div style='background:{color};padding:15px;border-radius:10px;color:white;text-align:center;font-weight:bold;'>{machine}<br>{downtime} min</div>",
            unsafe_allow_html=True
        )

# =========================================
# MACHINE DETAIL VIEW
# =========================================
if "selected_machine" in st.session_state:
    sm = st.session_state.selected_machine
    st.subheader(f"Breakdowns for {sm}")
    machine_df = df[df["machine"] == sm]
    st.dataframe(machine_df)

# =========================================
# ADD BREAKDOWN (Admin & Technician Only)
# =========================================
if st.session_state.role in ["Admin", "Technician"]:

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
            (date,machine,category,problem,downtime,technician,status,start_time,end_time)
            VALUES (?,?,?,?,?,?,?,?,?)
            """, (date,machine,category,problem,downtime,technician,status,"",""))
            conn.commit()
            st.success("Saved")
            st.rerun()

# =========================================
# PM MODULE
# =========================================
st.divider()
st.subheader("Preventive Maintenance (PM)")

today = datetime.today().date()

if st.session_state.role == "Admin":

    with st.form("pm_form"):
        machine = st.selectbox("Machine for PM", MACHINES)
        pm_type = st.selectbox("PM Type", ["Weekly", "Monthly"])
        last_done = st.date_input("Last Done", today)

        next_due = last_done + timedelta(days=7 if pm_type=="Weekly" else 30)

        if st.form_submit_button("Schedule PM"):
            c.execute("""
            INSERT INTO pm_schedule 
            (machine,pm_type,last_done,next_due,status)
            VALUES (?,?,?,?,?)
            """, (machine,pm_type,last_done,next_due,"Scheduled"))
            conn.commit()
            st.success("PM Scheduled")
            st.rerun()

if not pm_df.empty:
    pm_df["next_due"] = pd.to_datetime(pm_df["next_due"]).dt.date
    pm_df["status"] = pm_df["next_due"].apply(
        lambda x: "Overdue" if x < today else "Upcoming"
    )

    st.dataframe(pm_df)

# =========================================
# DELETE RECORD (Admin Only)
# =========================================
if st.session_state.role == "Admin":
    st.divider()
    st.subheader("Delete Breakdown Record")

    delete_id = st.number_input("Enter Breakdown ID", 0)

    if st.button("Delete"):
        c.execute("DELETE FROM breakdowns WHERE id=?", (delete_id,))
        conn.commit()
        st.success("Deleted")
        st.rerun()
