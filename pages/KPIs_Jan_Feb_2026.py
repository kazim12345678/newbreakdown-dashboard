# ==========================================================
# Drinkable Section KPIs — Jan & Feb 2026 (Standalone Page)
# File: pages/01_Drinkable_KPIs_Jan_Feb_2026.py
#
# This page is SELF-CONTAINED:
# - Uploads Excel here
# - Cleans data here
# - Generates all tables + charts here
#
# IMPORTANT ASSUMPTION (requested):
RUN_HOURS_PER_DAY = 600  # MTBF uses: total_running_hours = RUN_HOURS_PER_DAY * distinct_days
PLANNED_AVAILABLE_HOURS_PER_DAY = 24  # Availability% uses planned hours/day (edit if needed)
# ==========================================================

import streamlit as st
import pandas as pd
import numpy as np
import re
import io
from datetime import datetime, date, time

import matplotlib.pyplot as plt
import seaborn as sns

# ---------- Page setup ----------
st.set_page_config(page_title="Drinkable KPIs Jan–Feb 2026", layout="wide")
sns.set_theme(style="whitegrid")

REPORT_START = date(2026, 1, 1)
REPORT_END   = date(2026, 2, 26)

COLOR_MAIN = "#1f77b4"
COLOR_ALERT = "#d62728"
COLOR_GOOD = "#2ca02c"

st.title("🥤 Drinkable Section KPIs — Jan & Feb 2026")
st.caption(
    f"Period: {REPORT_START} → {REPORT_END} | "
    f"MTBF assumption: RUN_HOURS_PER_DAY = {RUN_HOURS_PER_DAY} hrs/day | "
    f"Availability planned hours/day = {PLANNED_AVAILABLE_HOURS_PER_DAY}"
)

# ---------- Upload ----------
uploaded = st.file_uploader(
    "Upload maintenance log file (.xlsm / .xlsx / .xls)",
    type=["xlsm", "xlsx", "xls"],
    key="drinkable_upload"
)
if uploaded is None:
    st.info("Upload the maintenance log to generate the report.")
    st.stop()

# ---------- Utilities ----------
def is_blank(x):
    if pd.isna(x): return True
    s = str(x).strip().lower()
    return s == "" or s == "nan"

def time_to_minutes(x, default=np.nan):
    """Convert Excel/Python time/duration to minutes safely."""
    if pd.isna(x):
        return default

    if isinstance(x, pd.Timedelta):
        return x.total_seconds() / 60.0

    if isinstance(x, pd.Timestamp):
        return x.hour*60 + x.minute + x.second/60

    if isinstance(x, datetime):
        return x.hour*60 + x.minute + x.second/60

    if isinstance(x, time):
        return x.hour*60 + x.minute + x.second/60

    if isinstance(x, (int, float, np.integer, np.floating)):
        v = float(x)
        # Excel time is fraction-of-day
        if 0 <= v <= 1.5:
            return v * 24 * 60
        # heuristics (hours vs minutes)
        if v <= 48:
            return v * 60
        return v

    if isinstance(x, str):
        s = x.strip()
        m = re.match(r"^(\d{1,2}):(\d{1,2})(?::(\d{1,2}))?$", s)
        if m:
            hh = int(m.group(1)); mm = int(m.group(2)); ss = int(m.group(3) or 0)
            return hh*60 + mm + ss/60
        try:
            return time_to_minutes(float(s), default=default)
        except:
            return default

    return default

def get_hour_of_day(start_val, req_val):
    """Hour 0–23 from Start, else Requested Time."""
    def extract_hour(v):
        if pd.isna(v): return np.nan
        if isinstance(v, time): return v.hour
        if isinstance(v, pd.Timestamp): return v.hour
        if isinstance(v, datetime): return v.hour
        if isinstance(v, str):
            m = re.match(r"^(\d{1,2}):", v.strip())
            if m: return int(m.group(1))
        return np.nan

    h = extract_hour(start_val)
    if not np.isnan(h): return h
    return extract_hour(req_val)

def normalize_job(job):
    s = str(job).strip().upper().replace(" ", "")
    if s in ["B/D", "BD", "BREAKDOWN"]:
        return "Breakdown"
    if s in ["CORRECTIVE"]:
        return "Corrective"
    return "Other"

def clean_reason(txt, fallback="unknown"):
    s = "" if pd.isna(txt) else str(txt).strip().lower()
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    if not s:
        return fallback
    return " ".join(s.split()[:6])

def split_techs(performed_by):
    """Split technician names by /, &, comma, 'and' etc."""
    if pd.isna(performed_by):
        return ["Unknown"]
    s = str(performed_by).strip()
    if s == "" or s.lower() == "nan":
        return ["Unknown"]
    s = s.replace("&", "/").replace(",", "/").replace(";", "/")
    s = re.sub(r"\band\b", "/", s, flags=re.IGNORECASE)
    parts = [p.strip() for p in s.split("/") if p.strip()]
    return parts if parts else ["Unknown"]

def download_csv(df, filename):
    st.download_button(
        "⬇️ Download CSV",
        df.to_csv(index=True).encode("utf-8"),
        file_name=filename,
        mime="text/csv"
    )

# ---------- Load + Clean (cached) ----------
@st.cache_data(show_spinner=True)
def load_and_clean(file_bytes: bytes):
    xls = pd.ExcelFile(io.BytesIO(file_bytes), engine="openpyxl")
    sheet = next((s for s in xls.sheet_names if s.strip().lower() in ["main data", "maindata", "main"]), xls.sheet_names[0])
    df = pd.read_excel(io.BytesIO(file_bytes), sheet_name=sheet, engine="openpyxl")
    df.columns = [str(c).strip() for c in df.columns]

    # Remove template rows: keep row if any key fields exist
    key_cols = ["Notification No.", "Machine No.", "Type", "Reported Problem"]
    present = [c for c in key_cols if c in df.columns]
    if present:
        mask = False
        for c in present:
            mask = mask | df[c].notna()
        df = df[mask].copy()
    else:
        df = df.copy()

    # Date
    if "Date" in df.columns:
        df["Date_Clean"] = pd.to_datetime(df["Date"], errors="coerce").dt.date
    else:
        df["Date_Clean"] = pd.NaT

    # Waiting time
    df["Waiting_Minutes"] = 0.0
    if "Waiting Time" in df.columns:
        df["Waiting_Minutes"] = df["Waiting Time"].apply(lambda x: 0.0 if is_blank(x) else time_to_minutes(x, default=0.0))
    df["Waiting_Hours"] = df["Waiting_Minutes"] / 60.0

    # Consumed time
    cons_col = "Time Consumed" if "Time Consumed" in df.columns else None
    start_col = "Start" if "Start" in df.columns else None
    end_col   = "End" if "End" in df.columns else None
    req_col   = "Requested Time" if "Requested Time" in df.columns else None

    df["Consumed_Minutes"] = np.nan

    if cons_col and pd.api.types.is_timedelta64_dtype(df[cons_col]):
        df["Consumed_Minutes"] = df[cons_col].dt.total_seconds() / 60.0

    def calc_consumed(row):
        # prefer Start/End
        if start_col and end_col:
            s_min = time_to_minutes(row[start_col], default=np.nan)
            e_min = time_to_minutes(row[end_col], default=np.nan)
            if not np.isnan(s_min) and not np.isnan(e_min):
                dur = e_min - s_min
                if dur < 0:
                    dur += 24*60
                return dur
        # fallback Time Consumed
        if cons_col:
            return time_to_minutes(row[cons_col], default=np.nan)
        return np.nan

    need_calc = df["Consumed_Minutes"].isna()
    df.loc[need_calc, "Consumed_Minutes"] = df.loc[need_calc].apply(calc_consumed, axis=1)
    df["Consumed_Minutes"] = df["Consumed_Minutes"].fillna(0.0)
    df["Consumed_Hours"] = df["Consumed_Minutes"] / 60.0

    # Hour of day
    df["HourOfDay"] = df.apply(lambda r: get_hour_of_day(r.get(start_col, np.nan), r.get(req_col, np.nan)), axis=1)

    # Job Category
    if "Job" in df.columns:
        df["Job_Category"] = df["Job"].apply(normalize_job)
    else:
        df["Job_Category"] = "Other"

    # Notification status
    if "Notification No." in df.columns:
        df["Notification_Status"] = df["Notification No."].apply(lambda x: "Without Notification" if is_blank(x) else "With Notification")
    else:
        df["Notification_Status"] = "Unknown"

    # Reason clean
    prob_col = "Reported Problem" if "Reported Problem" in df.columns else None
    type_col = "Type" if "Type" in df.columns else None
    fallback_series = df[type_col].fillna("unknown") if type_col else "unknown"
    if prob_col:
        df["Reason_Clean"] = [
            clean_reason(p, fallback=clean_reason(f, fallback="unknown"))
            for p, f in zip(df[prob_col].fillna(""), fallback_series)
        ]
    else:
        df["Reason_Clean"] = fallback_series.astype(str).apply(lambda s: clean_reason(s, fallback="unknown"))

    return df, sheet

file_bytes = uploaded.getvalue()
df_all, used_sheet = load_and_clean(file_bytes)

st.caption(f"Loaded & cleaned from sheet: **{used_sheet}** | Clean rows: **{len(df_all):,}**")

# ---------- Filter period ----------
df = df_all[(df_all["Date_Clean"] >= REPORT_START) & (df_all["Date_Clean"] <= REPORT_END)].copy()
if df.empty:
    st.warning("No rows found in the report period (01 Jan 2026 to 26 Feb 2026).")
    st.stop()

# ---------- Optional filters (keep PDF friendly) ----------
st.sidebar.header("Filters")
min_d, max_d = df["Date_Clean"].min(), df["Date_Clean"].max()
dr = st.sidebar.date_input("Date range", (min_d, max_d), min_value=min_d, max_value=max_d)
df = df[(df["Date_Clean"] >= dr[0]) & (df["Date_Clean"] <= dr[1])]

if "Shift" in df.columns:
    shifts = sorted(df["Shift"].dropna().astype(str).unique())
    sel_shift = st.sidebar.multiselect("Shift", shifts)
    if sel_shift:
        df = df[df["Shift"].astype(str).isin(sel_shift)]

machines = sorted(df["Machine No."].dropna().astype(str).unique())
sel_mach = st.sidebar.multiselect("Machine No.", machines)
if sel_mach:
    df = df[df["Machine No."].astype(str).isin(sel_mach)]

# ---------- Tech log (FULL credit, NOT divided) ----------
tech_log = []
if "Performed By" in df.columns:
    for _, row in df.iterrows():
        for t in split_techs(row["Performed By"]):
            tech_log.append({
                "Date_Clean": row["Date_Clean"],
                "Technician": t,
                "Machine No.": row["Machine No."],
                "Shift": row.get("Shift", np.nan),
                "Job_Category": row["Job_Category"],
                "Notification_Status": row["Notification_Status"],
                "Consumed_Minutes": row["Consumed_Minutes"],  # FULL credit
                "Consumed_Hours": row["Consumed_Hours"]
            })
tech_log = pd.DataFrame(tech_log)

# ==========================================================
# Executive Summary
# ==========================================================
st.header("1) Executive Summary")

total_downtime = df["Consumed_Hours"].sum()
distinct_days = df["Date_Clean"].nunique()

df_bd = df[df["Job_Category"] == "Breakdown"].copy()
bd_events = len(df_bd)
bd_downtime = df_bd["Consumed_Hours"].sum()

total_running_hours = distinct_days * RUN_HOURS_PER_DAY  # MTBF assumption here

mttr = bd_downtime / bd_events if bd_events else 0.0
mtbf = total_running_hours / bd_events if bd_events else 0.0

planned_hours_total = distinct_days * PLANNED_AVAILABLE_HOURS_PER_DAY
availability = (1 - (total_downtime / planned_hours_total)) * 100 if planned_hours_total else 0.0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Downtime (hrs)", f"{total_downtime:,.2f}")
c2.metric("Availability %", f"{availability:,.2f}%")
c3.metric("MTTR (hrs) — Breakdown", f"{mttr:,.2f}")
c4.metric("MTBF (hrs) — Breakdown", f"{mtbf:,.2f}")

# Trend: daily downtime
kpi1 = pd.pivot_table(df, index="Date_Clean", columns="Machine No.", values="Consumed_Hours", aggfunc="sum", fill_value=0).sort_index()
kpi1["Grand Total"] = kpi1.sum(axis=1)

fig, ax = plt.subplots(figsize=(10, 3.6))
ax.plot(kpi1.index, kpi1["Grand Total"], color=COLOR_MAIN, linewidth=2)
ax.set_title("Daily Total Downtime (hrs)")
ax.set_xlabel("Date"); ax.set_ylabel("Hours")
ax.tick_params(axis="x", rotation=45)
st.pyplot(fig)

st.divider()

# ==========================================================
# KPI 1 + Pareto + Heatmap + Top Machines
# ==========================================================
st.header("2) Machine Downtime (KPI 1 + Pareto + Top Machines)")

pareto = df.groupby("Machine No.")["Consumed_Hours"].sum().sort_values(ascending=False).to_frame("Downtime_Hours")
pareto["% of Total"] = (pareto["Downtime_Hours"] / pareto["Downtime_Hours"].sum() * 100).round(2)
pareto["Cumulative %"] = pareto["% of Total"].cumsum().round(2)

def share_top(n):
    total = pareto["Downtime_Hours"].sum()
    return round(pareto.head(n)["Downtime_Hours"].sum() / total * 100, 2) if total else 0.0

concentration = pd.DataFrame({
    "Metric": ["Top 3 share %", "Top 5 share %", "Top 10 share %"],
    "Value": [share_top(3), share_top(5), share_top(10)]
})

colL, colR = st.columns(2)

with colL:
    st.subheader("Top 13 Machines by Downtime (hrs)")
    fig, ax = plt.subplots(figsize=(7, 4))
    top13 = pareto.head(13)
    ax.bar(top13.index.astype(str), top13["Downtime_Hours"], color=COLOR_MAIN)
    ax.set_xlabel("Machine"); ax.set_ylabel("Hours")
    ax.tick_params(axis="x", rotation=45)
    st.pyplot(fig)

with colR:
    st.subheader("Pareto: Downtime + Cumulative %")
    fig, ax1 = plt.subplots(figsize=(7, 4))
    ax1.bar(pareto.index.astype(str), pareto["Downtime_Hours"], color=COLOR_MAIN, alpha=0.85)
    ax1.set_ylabel("Hours"); ax1.tick_params(axis="x", rotation=45)
    ax2 = ax1.twinx()
    ax2.plot(pareto.index.astype(str), pareto["Cumulative %"], color=COLOR_ALERT, marker="o", linewidth=2)
    ax2.set_ylabel("Cumulative %"); ax2.set_ylim(0, 110)
    st.pyplot(fig)

st.subheader("Heatmap: Date × Machine (Top machines)")
heat_cols = [c for c in top13.index if c in kpi1.columns]
heat_dm = kpi1[heat_cols].copy()
fig, ax = plt.subplots(figsize=(12, 5))
sns.heatmap(heat_dm, cmap="Blues", ax=ax)
ax.set_xlabel("Machine"); ax.set_ylabel("Date")
st.pyplot(fig)

st.subheader("KPI 1 Table (Date × Machine downtime hours)")
st.dataframe(kpi1, use_container_width=True)
download_csv(kpi1, "kpi1_date_machine_downtime.csv")

st.subheader("Pareto Table + Concentration")
st.dataframe(pareto, use_container_width=True)
download_csv(pareto, "pareto_machine_downtime.csv")
st.dataframe(concentration, use_container_width=True)
download_csv(concentration, "downtime_concentration.csv")

st.divider()

# ==========================================================
# KPI 2: Notifications
# ==========================================================
st.header("3) Notifications (KPI 2)")

kpi2 = df.groupby(["Date_Clean", "Notification_Status"]).size().unstack(fill_value=0).sort_index()
kpi2["Total Jobs"] = kpi2.sum(axis=1)
kpi2["% Without Notification"] = (kpi2.get("Without Notification", 0) / kpi2["Total Jobs"] * 100).round(2)

st.dataframe(kpi2, use_container_width=True)
download_csv(kpi2, "kpi2_notifications_by_date.csv")

st.divider()

# ==========================================================
# KPI 3 + KPI 4: Shift + Job Category
# ==========================================================
st.header("4) Shifts & Job Categories (KPI 3 + KPI 4)")

kpi3 = df.groupby(df.get("Shift", "Unknown"))["Consumed_Hours"].sum().sort_values(ascending=False).to_frame("Downtime_Hours")
kpi3["% Share"] = (kpi3["Downtime_Hours"] / kpi3["Downtime_Hours"].sum() * 100).round(2)

kpi4_count = df.groupby("Job_Category").size().to_frame("Jobs_Count").sort_values("Jobs_Count", ascending=False)
kpi4_time = df.groupby("Job_Category")["Consumed_Hours"].sum().to_frame("Downtime_Hours").sort_values("Downtime_Hours", ascending=False)

cA, cB = st.columns(2)

with cA:
    st.subheader("Downtime by Shift")
    st.dataframe(kpi3, use_container_width=True)
    download_csv(kpi3, "kpi3_downtime_by_shift.csv")

    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    ax.bar(kpi3.index.astype(str), kpi3["Downtime_Hours"], color=COLOR_MAIN)
    ax.set_xlabel("Shift"); ax.set_ylabel("Hours")
    st.pyplot(fig)

with cB:
    st.subheader("Jobs by Category")
    st.dataframe(kpi4_count, use_container_width=True)
    download_csv(kpi4_count, "kpi4_job_counts.csv")

    st.subheader("Downtime by Category")
    st.dataframe(kpi4_time, use_container_width=True)
    download_csv(kpi4_time, "kpi4_job_downtime.csv")

st.divider()

# ==========================================================
# KPI 5: Waiting Time
# ==========================================================
st.header("5) Waiting Time (KPI 5)")

kpi5 = df.groupby("Date_Clean")["Waiting_Hours"].sum().to_frame("Waiting_Hours").sort_index()
st.dataframe(kpi5, use_container_width=True)
download_csv(kpi5, "kpi5_waiting_by_date.csv")

fig, ax = plt.subplots(figsize=(10, 3.6))
ax.plot(kpi5.index, kpi5["Waiting_Hours"], color=COLOR_GOOD, linewidth=2)
ax.set_title("Daily Total Waiting Time (hrs)")
ax.set_xlabel("Date"); ax.set_ylabel("Hours")
ax.tick_params(axis="x", rotation=45)
st.pyplot(fig)

st.divider()

# ==========================================================
# KPI 6: MTTR & MTBF (Breakdown only)
# ==========================================================
st.header("6) Reliability (KPI 6: MTTR & MTBF)")

kpi6_overall = pd.DataFrame({
    "Metric": [
        "Distinct Days",
        "RUN_HOURS_PER_DAY (assumption)",
        "Total Running Hours",
        "Breakdown Events (B/D)",
        "Breakdown Downtime (hrs)",
        "MTTR (hrs)",
        "MTBF (hrs)"
    ],
    "Value": [
        distinct_days,
        RUN_HOURS_PER_DAY,
        total_running_hours,
        bd_events,
        round(bd_downtime, 2),
        round(mttr, 2),
        round(mtbf, 2)
    ]
})

kpi6_machine = df_bd.groupby("Machine No.").agg(
    Breakdown_Events=("Consumed_Hours", "size"),
    Breakdown_Downtime_Hours=("Consumed_Hours", "sum")
).sort_values("Breakdown_Downtime_Hours", ascending=False)
kpi6_machine["MTTR_Hrs"] = (kpi6_machine["Breakdown_Downtime_Hours"] / kpi6_machine["Breakdown_Events"]).round(2)
kpi6_machine["MTBF_Hrs"] = (total_running_hours / kpi6_machine["Breakdown_Events"]).replace([np.inf], 0).round(2)

st.dataframe(kpi6_overall, use_container_width=True)
download_csv(kpi6_overall, "kpi6_overall_mttr_mtbf.csv")

st.subheader("Per-machine MTTR/MTBF (sorted by breakdown downtime)")
st.dataframe(kpi6_machine, use_container_width=True)
download_csv(kpi6_machine, "kpi6_machine_mttr_mtbf.csv")

st.divider()

# ==========================================================
# KPI 7 + KPI 8: Hour patterns
# ==========================================================
st.header("7) Time Pattern (KPI 7 + KPI 8)")

kpi7 = df.dropna(subset=["HourOfDay"]).groupby("HourOfDay")["Consumed_Hours"].sum().reindex(range(24), fill_value=0).to_frame("Downtime_Hours")
fig, ax = plt.subplots(figsize=(10, 3.6))
ax.bar(kpi7.index, kpi7["Downtime_Hours"], color=COLOR_MAIN)
ax.set_title("Downtime by Hour (0–23)")
ax.set_xlabel("Hour"); ax.set_ylabel("Hours")
ax.set_xticks(range(24))
st.pyplot(fig)

kpi8 = df.dropna(subset=["HourOfDay"]).pivot_table(index="Date_Clean", columns="HourOfDay", values="Consumed_Hours", aggfunc="sum", fill_value=0).reindex(columns=range(24), fill_value=0).sort_index()
heat_dh = kpi8.tail(30)

st.subheader("Heatmap: Date × Hour (last 30 days in selection)")
fig, ax = plt.subplots(figsize=(12, 5))
sns.heatmap(heat_dh, cmap="Blues", ax=ax)
ax.set_xlabel("Hour"); ax.set_ylabel("Date")
st.pyplot(fig)

st.divider()

# ==========================================================
# KPI 9: Technician workload (FULL CREDIT, not divided)
# ==========================================================
st.header("8) Technician Performance (KPI 9)")
st.caption("Workload rule: If A and B did the same job for 10 minutes, A gets 10 minutes and B gets 10 minutes (NOT divided).")

if not tech_log.empty:
    kpi9 = tech_log.pivot_table(index="Technician", columns="Job_Category", values="Consumed_Hours", aggfunc="sum", fill_value=0)
    kpi9["Total_Hours"] = kpi9.sum(axis=1)
    kpi9 = kpi9.sort_values("Total_Hours", ascending=False)

    toptech = kpi9.head(10)["Total_Hours"]
    fig, ax = plt.subplots(figsize=(10, 3.8))
    ax.bar(toptech.index.astype(str), toptech.values, color=COLOR_MAIN)
    ax.set_title("Top 10 Technicians by Workload (hrs) — FULL credit")
    ax.set_xlabel("Technician"); ax.set_ylabel("Hours")
    ax.tick_params(axis="x", rotation=45)
    st.pyplot(fig)

    st.dataframe(kpi9.head(50), use_container_width=True)
    download_csv(kpi9, "kpi9_technician_workload.csv")
else:
    st.info("No technician data found (Performed By column missing or empty).")

st.divider()

# ==========================================================
# KPI 10 + KPI 11: Reasons + Top Machines (Breakdown)
# ==========================================================
st.header("9) Breakdown Reasons & Top Machines (KPI 10 + KPI 11)")

kpi10 = df_bd.groupby("Reason_Clean").agg(
    Downtime_Hours=("Consumed_Hours", "sum"),
    Incidents=("Reason_Clean", "size")
).sort_values("Downtime_Hours", ascending=False).head(10)

kpi11 = df_bd.groupby("Machine No.").agg(
    Downtime_Hours=("Consumed_Hours", "sum"),
    Incidents=("Machine No.", "size")
).sort_values("Downtime_Hours", ascending=False).head(13)

c1, c2 = st.columns(2)

with c1:
    st.subheader("Top 10 Breakdown Reasons (by downtime hours)")
    fig, ax = plt.subplots(figsize=(8, 3.8))
    if len(kpi10):
        ax.barh(kpi10.index.astype(str)[::-1], kpi10["Downtime_Hours"].values[::-1], color=COLOR_MAIN)
    ax.set_xlabel("Hours")
    st.pyplot(fig)
    st.dataframe(kpi10, use_container_width=True)
    download_csv(kpi10, "kpi10_top10_breakdown_reasons.csv")

with c2:
    st.subheader("Top 13 Machines (Breakdown downtime)")
    st.dataframe(kpi11, use_container_width=True)
    download_csv(kpi11, "kpi11_top13_breakdown_machines.csv")

st.success("✅ This page is standalone and does not require main.py session_state.")
