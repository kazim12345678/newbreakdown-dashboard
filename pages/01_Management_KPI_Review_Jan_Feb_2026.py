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
# EXECUTIVE SUMMARY
# ============================================================

st.title("📈 Management KPI Review – Jan & Feb 2026")

st.markdown("""
### 🔍 Executive Summary
This report highlights maintenance performance for January and February 2026.  
It shows where breakdowns occur, which machines and areas are most affected,  
and how effectively the maintenance team is responding.

### ⭐ Key Highlights
- Mechanical and Electrical issues caused the highest downtime.  
- Filling & Capping, Packer Tunnel, and Crates Line are top contributors.  
- Technician involvement is strong (Dante, Nashwan, Husam, shift teams).  
- Notification discipline improving, but jobs without notification still exist.  
- Hour‑wise analysis shows clear peak load periods.

### 🎯 Dashboard Contents
- Daily & hourly breakdown trends  
- Machine, area & classification breakdowns  
- Technician performance  
- Notification compliance summary  
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
# 3) MACHINE-WISE BREAKDOWN
# ============================================================

machine_data = [
    ("Crates Area/Line",53.918),("M1",24.367),("M12",20.066),("M13",22.748),
    ("M14",43.951),("M15",52.431),("M16",36.348),("M17",19.252),
    ("M18",30.216),("M2",35.060),("M3",31.498),("M4",31.734),
    ("M5",1.499),("M6",58.450),("M7",47.500),("M8",37.363),("M9",3.217)
]

df_machine = pd.DataFrame(machine_data, columns=["Machine","Hours"]).sort_values("Hours", ascending=False)

# ============================================================
# 4) AREA-WISE BREAKDOWN
# ============================================================

area_data = [
    ("Crates Area /Line",3250),
    ("Downline",10634),
    ("Filling & Capping",15903),
    ("Upstream",3191),
]

df_area = pd.DataFrame(area_data, columns=["Area","Minutes"])
df_area["Hours"] = df_area["Minutes"] / 60
df_area = df_area.sort_values("Hours", ascending=False)

# ============================================================
# 5) MACHINE CLASSIFICATION BREAKDOWN
# ============================================================

class_data = [
    ("Bottle Debagger, Bottle Unscrambler",1611),
    ("Bottle Inspection Machine, Bottle Invert Cleaner",263),
    ("Bottle Line Conveyor,Overhead Bottle Conveyor, Air Conveyor",1292),
    ("Cap Hooper / Elevator Unit",75),
    ("Cap Sorter / Cap Conveyor Unit",150),
    ("Cap Top Sticker Unit",15),
    ("C-loop Crates Chute / Overhead Crates Conveyor",670),
    ("Crates Destacker / Crates Washer / Crates lines",3220),
    ("Crates Stacker & Unitizer Unit",2916),
    ("Downline Conveyor Bottles, Wraps & Case Handling Line",165),
    ("Filling and Capping Machine",13876),
    ("Filling Machine Infeed Conveyor",135),
    ("Filling Machine Outfeed Conveyor",103),
    ("Ink Jet Printer Unit",926),
    ("Labelling Machine",245),
    ("Packer Machine & Heating Tunnel",5664),
    ("Pallet Wrapping Machine",67),
    ("Palletizer Machine",575),
    ("Sleeve Applicator & Heating Tunnel",362),
    ("Turret Bottle Cleaner / Rinser",648),
]

df_class = pd.DataFrame(class_data, columns=["Equipment","Minutes"])
df_class["Hours"] = df_class["Minutes"] / 60
df_class = df_class.sort_values("Hours", ascending=False)
# ============================================================
# 6) TECHNICIAN PERFORMANCE
# ============================================================

tech_data = [
    ("ali","79:17"),("amgad","49:36"),("automation","0:20"),("automation mtc","19:34"),
    ("dante","119:49"),("day","11:41"),("day shift","6:09"),("day shift maint. team","94:21"),
    ("edgar","73:13"),("gilbert","65:20"),("husam","89:33"),("husam?moneef","0:35"),
    ("hussam","1:10"),("jamal","33:47"),("lito","28:39"),("majid","1:18"),
    ("moneef","37:43"),("nahswan","0:55"),("nashwan","113:14"),("night shift","3:46"),
    ("night shift maint. team","74:04"),("nsahwan","0:19"),("operator","0:46"),
    ("rakan","1:00"),("sai","0:25"),("sameer","62:28"),("sami","54:21"),
    ("serac techn","0:20"),("workshop mtc","5:21"),("yosuefs","0:50"),
    ("yousef","10:12"),("yousef k","0:40"),("yousef s","0:40"),
    ("yousefk","13:02"),("yousefs","15:48"),
]

df_tech = pd.DataFrame(tech_data, columns=["Technician","Total"])
df_tech["Hours"] = df_tech["Total"].apply(to_hours)
df_tech["Technician"] = df_tech["Technician"].str.title()
df_tech = df_tech.sort_values("Hours", ascending=False)

# ============================================================
# 7) NOTIFICATION SUMMARY
# ============================================================

notif_data = [
    ("2026-01-01",22,9,14,8,6,3), ("2026-01-02",7,20,5,2,13,7),
    ("2026-01-03",9,12,4,5,10,2), ("2026-01-04",14,8,9,5,6,2),
    ("2026-01-05",12,4,8,4,4,0), ("2026-01-06",20,4,8,12,4,0),
    ("2026-01-07",24,13,12,12,8,5), ("2026-01-08",25,5,8,17,5,0),
    ("2026-01-09",8,11,2,6,9,2), ("2026-01-10",18,6,8,10,5,1),
    ("2026-01-11",17,3,10,7,3,0), ("2026-01-12",16,3,4,12,1,2),
    ("2026-01-13",9,5,9,0,5,0), ("2026-01-14",14,6,6,8,5,1),
    ("2026-01-15",19,5,11,8,5,0), ("2026-01-16",19,3,9,10,3,0),
    ("2026-01-17",15,5,8,7,5,0), ("2026-01-18",7,8,4,3,8,0),
    ("2026-01-19",25,2,14,11,1,1), ("2026-01-20",7,5,6,1,5,0),
    ("2026-01-21",14,8,2,12,8,0), ("2026-01-22",19,3,9,10,3,0),
    ("2026-01-23",15,2,6,9,2,0), ("2026-01-24",25,3,11,14,2,1),
    ("2026-01-25",22,1,5,17,1,0), ("2026-01-26",18,0,8,10,0,0),
    ("2026-01-27",7,5,5,2,3,2), ("2026-01-28",27,4,13,14,4,0),
    ("2026-01-29",22,3,12,10,1,2), ("2026-01-30",7,0,6,1,0,0),
    ("2026-01-31",16,4,13,3,4,0), ("2026-02-01",11,0,9,2,0,0),
    ("2026-02-02",21,4,16,5,4,0), ("2026-02-03",15,1,11,4,0,1),
    ("2026-02-04",12,3,6,6,3,0), ("2026-02-05",14,9,5,9,4,5),
    ("2026-02-06",21,1,12,9,1,0), ("2026-02-07",19,3,10,9,3,0),
    ("2026-02-08",15,2,9,6,2,0), ("2026-02-09",19,1,13,6,1,0),
    ("2026-02-10",12,4,7,5,2,2), ("2026-02-11",30,5,16,14,3,2),
    ("2026-02-12",16,4,13,3,3,1), ("2026-02-13",20,6,12,8,6,0),
    ("2026-02-14",21,6,10,11,4,2), ("2026-02-15",24,4,12,12,4,0),
    ("2026-02-16",18,3,10,8,3,0), ("2026-02-17",26,4,17,9,1,3),
    ("2026-02-18",13,9,5,8,9,0), ("2026-02-19",14,9,9,5,4,5),
    ("2026-02-20",18,13,11,7,6,7), ("2026-02-21",15,11,9,6,6,5),
    ("2026-02-22",23,7,10,13,3,4), ("2026-02-23",18,14,9,9,10,4),
    ("2026-02-24",12,8,6,6,6,2), ("2026-02-25",17,12,9,8,8,4),
    ("2026-02-26",14,17,4,10,10,7), ("2026-02-27",14,19,4,10,14,5),
    ("2026-02-28",11,13,9,2,11,2),
]

df_notif = pd.DataFrame(
    notif_data,
    columns=[
        "Date","Notifications_Received","Jobs_Without_Notification",
        "Corrective_With_Notif","BD_With_Notif",
        "Corrective_Without_Notif","BD_Without_Notif"
    ]
)

notif_totals = df_notif.iloc[:,1:].sum()

# ============================================================
# VISUALS SECTION
# ============================================================

# Hour-wise + Machine-wise
st.subheader("⏱ Hour-wise Breakdown & 🛠 Machine-wise Breakdown")
col1, col2 = st.columns(2)

with col1:
    fig2, ax2 = plt.subplots(figsize=(7,4))
    ax2.bar(df_hour["Hour"], df_hour["Hours"],
            color=plt.cm.turbo(df_hour["Hours"]/df_hour["Hours"].max()))
    ax2.set_title("Hour-wise Breakdown (0–23)")
    ax2.set_xlabel("Hour")
    ax2.set_ylabel("Hours")
    ax2.grid(axis="y", linestyle="--", alpha=0.4)
    st.pyplot(fig2)

with col2:
    fig3, ax3 = plt.subplots(figsize=(7,4))
    ax3.barh(df_machine["Machine"], df_machine["Hours"],
             color=plt.cm.plasma(df_machine["Hours"]/df_machine["Hours"].max()))
    ax3.set_title("Machine-wise Breakdown (Hours)")
    ax3.invert_yaxis()
    ax3.grid(axis="x", linestyle="--", alpha=0.4)
    st.pyplot(fig3)

# Area-wise + Classification
st.subheader("🏭 Area-wise Breakdown & ⚙ Machine Classification Breakdown")
col3, col4 = st.columns(2)

with col3:
    fig4, ax4 = plt.subplots(figsize=(7,4))
    ax4.bar(df_area["Area"], df_area["Hours"],
            color=plt.cm.viridis(df_area["Hours"]/df_area["Hours"].max()))
    ax4.set_title("Area-wise Breakdown (Hours)")
    ax4.set_xticklabels(df_area["Area"], rotation=25, ha="right")
    ax4.grid(axis="y", linestyle="--", alpha=0.4)
    st.pyplot(fig4)

with col4:
    fig5, ax5 = plt.subplots(figsize=(7,6))
    ax5.barh(df_class["Equipment"], df_class["Hours"],
             color=plt.cm.cividis(df_class["Hours"]/df_class["Hours"].max()))
    ax5.set_title("Machine Classification Breakdown (Hours)")
    ax5.invert_yaxis()
    ax5.grid(axis="x", linestyle="--", alpha=0.4)
    st.pyplot(fig5)

# Technician + Notifications
st.subheader("👨‍🔧 Technician Performance & 🔔 Notification Summary")
col5, col6 = st.columns(2)

with col5:
    fig6, ax6 = plt.subplots(figsize=(7,5))
    ax6.bar(df_tech["Technician"], df_tech["Hours"],
            color=plt.cm.magma(df_tech["Hours"]/df_tech["Hours"].max()))
    ax6.set_title("Technician Performance – Total Hours")
    ax6.set_xticklabels(df_tech["Technician"], rotation=60, ha="right")
    ax6.grid(axis="y", linestyle="--", alpha=0.4)
    st.pyplot(fig6)

with col6:
    fig7, ax7 = plt.subplots(figsize=(7,5))
    ax7.bar(notif_totals.index, notif_totals.values, color="#00b894")
    ax7.set_title("Notification Summary – Jan & Feb 2026")
    ax7.set_xticklabels(notif_totals.index, rotation=45, ha="right")
    ax7.set_ylabel("Total Count")
    ax7.grid(axis="y", linestyle="--", alpha=0.4)
    st.pyplot(fig7)

# End
st.success("Dashboard loaded successfully.")
