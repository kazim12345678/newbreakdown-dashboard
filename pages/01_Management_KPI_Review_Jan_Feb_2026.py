import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Management KPI Review – Jan & Feb 2026", layout="wide")

# -----------------------------
# Helper: convert HH:MM to hours
# -----------------------------
def to_hours(t):
    t = str(t).strip()
    if t == "" or t.lower() == "nan":
        return 0.0
    h, m = map(int, t.split(":"))
    return h + m/60

# ============================================================
# EXECUTIVE SUMMARY SECTION
# ============================================================

st.title("📈 Management KPI Review – Jan & Feb 2026")

st.markdown("""
### 🔍 Executive Summary

This report provides a clear view of maintenance performance for January and February 2026.  
It highlights where breakdowns are happening, which machines and areas are most affected,  
and how effectively the maintenance team is responding.

### ⭐ Key Highlights
- **Mechanical and Electrical issues** caused the highest downtime.  
- **Filling & Capping, Packer Tunnel, Crates Line** remain the top contributors.  
- **Technician involvement is strong**, especially from Dante, Nashwan, Husam, and shift teams.  
- **Notification discipline is improving**, but jobs without notification still need attention.  
- **Hour‑wise analysis** shows clear peak load periods for manpower planning.

### 🎯 What This Dashboard Shows
- Daily and hourly breakdown trends  
- Machine, area, and classification breakdowns  
- Technician performance  
- Notification compliance summary  

Below are the detailed KPI visuals.
""")

# ============================================================
# 1) DAILY BREAKDOWN TREND
# ============================================================

daily_data = [
    ("1/1/2026",781),("1/2/2026",688),("1/3/2026",337),("1/4/2026",567),
    ("1/5/2026",302),("1/6/2026",540),("1/7/2026",666),("1/8/2026",650),
    ("1/9/2026",1166),("1/10/2026",796),("1/11/2026",460),("1/12/2026",858),
    ("1/13/2026",192),("1/14/2026",444),("1/15/2026",669),("1/16/2026",413),
    ("1/17/2026",472),("1/18/2026",377),("1/19/2026",854),("1/20/2026",200),
    ("1/21/2026",395),("1/22/2026",369),("1/23/2026",452),("1/24/2026",641),
    ("1/25/2026",448),("1/26/2026",429),("1/27/2026",339),("1/28/2026",656),
    ("1/29/2026",694),("1/30/2026",150),("1/31/2026",486),
    ("2/1/2026",215),("2/2/2026",608),("2/3/2026",543),("2/4/2026",377),
    ("2/5/2026",519),("2/6/2026",453),("2/7/2026",463),("2/8/2026",493),
    ("2/9/2026",442),("2/10/2026",373),("2/11/2026",980),("2/12/2026",534),
    ("2/13/2026",496),("2/14/2026",693),("2/15/2026",684),("2/16/2026",405),
    ("2/17/2026",636),("2/18/2026",570),("2/19/2026",415),("2/20/2026",693),
    ("2/21/2026",510),("2/22/2026",810),("2/23/2026",1042),("2/24/2026",435),
    ("2/25/2026",698),("2/26/2026",1320),("2/27/2026",675),("2/28/2026",395),
    ("3/1/2026",10)
]

df_daily = pd.DataFrame(daily_data, columns=["Date","Minutes"])
df_daily["Date"] = pd.to_datetime(df_daily["Date"])
df_daily["Hours"] = df_daily["Minutes"] / 60

st.subheader("📅 Daily Breakdown Trend")
fig_daily, ax_daily = plt.subplots(figsize=(12,4))
ax_daily.plot(df_daily["Date"], df_daily["Hours"], marker="o", color="#ff0066")
ax_daily.set_ylabel("Breakdown Hours")
ax_daily.grid(True, linestyle="--", alpha=0.4)
st.pyplot(fig_daily)

# ============================================================
# 2) HOUR-WISE BREAKDOWN
# ============================================================

hour_data = [
    (0,"19:59"),(1,"28:00"),(2,"21:43"),(3,"21:21"),(4,"23:21"),(5,"5:14"),
    (6,"20:42"),(7,"53:39"),(8,"21:34"),(9,"20:24"),(10,"21:31"),(11,"6:48"),
    (12,"17:25"),(13,"31:42"),(14,"26:16"),(15,"31:08"),(16,"14:31"),
    (17,"13:39"),(18,"33:21"),(19,"6:13"),(20,"29:51"),(21,"26:19"),
    (22,"30:06"),(23,"24:51")
]

df_hour = pd.DataFrame(hour_data, columns=["Hour","Time"])
df_hour["Hours"] = df_hour["Time"].apply(to_hours)
# ============================================================
# 3) MACHINE-WISE BREAKDOWN (continued)
# ============================================================

st.subheader("🛠 Machine-wise Breakdown")
fig_machine, ax_machine = plt.subplots(figsize=(12,5))
ax_machine.barh(
    df_machine["Machine"],
    df_machine["Hours"],
    color=plt.cm.plasma(df_machine["Hours"] / df_machine["Hours"].max())
)
ax_machine.set_title("Machine-wise Breakdown (Hours)")
ax_machine.invert_yaxis()
ax_machine.grid(axis="x", linestyle="--", alpha=0.4)
st.pyplot(fig_machine)

# ============================================================
# 4) AREA-WISE BREAKDOWN
# ============================================================

st.subheader("🏭 Area-wise Breakdown")
fig_area, ax_area = plt.subplots(figsize=(12,4))
ax_area.bar(
    df_area["Area"],
    df_area["Hours"],
    color=plt.cm.viridis(df_area["Hours"] / df_area["Hours"].max())
)
ax_area.set_title("Area-wise Breakdown (Hours)")
ax_area.set_xticklabels(df_area["Area"], rotation=25, ha="right")
ax_area.grid(axis="y", linestyle="--", alpha=0.4)
st.pyplot(fig_area)

# ============================================================
# 5) MACHINE CLASSIFICATION BREAKDOWN
# ============================================================

st.subheader("⚙ Machine Classification Breakdown")
fig_class, ax_class = plt.subplots(figsize=(12,8))
ax_class.barh(
    df_class["Equipment"],
    df_class["Hours"],
    color=plt.cm.cividis(df_class["Hours"] / df_class["Hours"].max())
)
ax_class.set_title("Machine Classification Breakdown (Hours)")
ax_class.invert_yaxis()
ax_class.grid(axis="x", linestyle="--", alpha=0.4)
st.pyplot(fig_class)

# ============================================================
# 6) TECHNICIAN PERFORMANCE
# ============================================================

st.subheader("👨‍🔧 Technician Performance")
fig_tech, ax_tech = plt.subplots(figsize=(12,6))
ax_tech.bar(
    df_tech["Technician"],
    df_tech["Hours"],
    color=plt.cm.magma(df_tech["Hours"] / df_tech["Hours"].max())
)
ax_tech.set_title("Technician Performance – Total Maintenance Hours")
ax_tech.set_xticklabels(df_tech["Technician"], rotation=60, ha="right")
ax_tech.grid(axis="y", linestyle="--", alpha=0.4)
st.pyplot(fig_tech)

# ============================================================
# 7) NOTIFICATION SUMMARY
# ============================================================

st.subheader("🔔 Notification Summary – Jan & Feb 2026")
fig_notif, ax_notif = plt.subplots(figsize=(12,5))
ax_notif.bar(
    notif_totals.index,
    notif_totals.values,
    color="#00b894"
)
ax_notif.set_title("Notification Summary – Jan & Feb 2026")
ax_notif.set_xticklabels(notif_totals.index, rotation=45, ha="right")
ax_notif.set_ylabel("Total Count")
ax_notif.grid(axis="y", linestyle="--", alpha=0.4)
st.pyplot(fig_notif)

# ============================================================
# END OF FILE
# ============================================================

st.success("Dashboard loaded successfully.")
