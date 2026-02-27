# ==========================================
# Drinks Section KPI Report (Downloadable HTML)
# Period: 01 Jan 2026 to 26 Feb 2026
#
# IMPORTANT ASSUMPTION (as requested):
RUN_HOURS_PER_DAY = 600  # Used in MTBF = (RUN_HOURS_PER_DAY * number_of_days) / breakdown_events
PLANNED_AVAILABLE_HOURS_PER_DAY = 24  # Used in Availability% (change if your plan is different)
# ==========================================

import pandas as pd
import numpy as np
import re, base64, io
from datetime import datetime, date, time

import matplotlib.pyplot as plt
import seaborn as sns

from google.colab import files

# ---------------------------
# 1) Upload Excel file
# ---------------------------
uploaded = files.upload()
fname = list(uploaded.keys())[0]
print("Uploaded:", fname)

# ---------------------------
# 2) Read Excel (prefer 'Main Data')
# ---------------------------
xls = pd.ExcelFile(fname, engine="openpyxl")
sheet = None
for s in xls.sheet_names:
    if s.strip().lower() in ["main data", "maindata", "main"]:
        sheet = s
        break
if sheet is None:
    sheet = xls.sheet_names[0]

df = pd.read_excel(fname, sheet_name=sheet, engine="openpyxl")
df.columns = [str(c).strip() for c in df.columns]
print("Using sheet:", sheet, "| rows:", len(df), "| cols:", len(df.columns))

# ---------------------------
# 3) Helpers
# ---------------------------
def is_blank(x):
    if pd.isna(x): return True
    s = str(x).strip().lower()
    return s == "" or s == "nan"

def time_to_minutes(x, default=np.nan):
    """Convert time/duration to minutes.
       Handles: Timedelta, Timestamp, datetime, time, numeric Excel fraction, string hh:mm[:ss]
    """
    if pd.isna(x): return default

    if isinstance(x, pd.Timedelta):
        return x.total_seconds() / 60

    if isinstance(x, pd.Timestamp):
        return x.hour*60 + x.minute + x.second/60

    if isinstance(x, datetime):
        return x.hour*60 + x.minute + x.second/60

    if isinstance(x, time):
        return x.hour*60 + x.minute + x.second/60

    if isinstance(x, (int, float, np.integer, np.floating)):
        v = float(x)
        # Excel time is fraction of day (0..1)
        if 0 <= v <= 1.5:
            return v * 24 * 60
        # else: guess hours vs minutes
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
    """Hour 0-23 from Start, else Requested Time."""
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
    """Split technician names by /, &, comma, 'and' etc. Full credit rule later."""
    if pd.isna(performed_by):
        return ["Unknown"]
    s = str(performed_by).strip()
    if s == "" or s.lower() == "nan":
        return ["Unknown"]
    s = s.replace("&", "/").replace(",", "/").replace(";", "/")
    s = re.sub(r"\band\b", "/", s, flags=re.IGNORECASE)
    parts = [p.strip() for p in s.split("/") if p.strip()]
    return parts if parts else ["Unknown"]

# ---------------------------
# 4) Keep only REAL rows (ignore templates)
# Real row if any of: Notification No., Machine No., Type, Reported Problem exists
# ---------------------------
key_cols = ["Notification No.", "Machine No.", "Type", "Reported Problem"]
present_keys = [c for c in key_cols if c in df.columns]
if present_keys:
    mask = False
    for c in present_keys:
        mask = mask | df[c].notna()
    df_real = df[mask].copy()
else:
    df_real = df.copy()

print("Real rows kept:", len(df_real), "out of", len(df))

# ---------------------------
# 5) Parse + compute columns
# ---------------------------
# Date
if "Date" in df_real.columns:
    df_real["Date_Clean"] = pd.to_datetime(df_real["Date"], errors="coerce").dt.date
else:
    df_real["Date_Clean"] = pd.NaT

# Waiting time -> minutes/hours (blank => 0)
df_real["Waiting_Minutes"] = 0.0
if "Waiting Time" in df_real.columns:
    df_real["Waiting_Minutes"] = df_real["Waiting Time"].apply(lambda x: 0.0 if is_blank(x) else time_to_minutes(x, default=0.0))
df_real["Waiting_Hours"] = df_real["Waiting_Minutes"] / 60.0

# Consumed time -> minutes/hours (prefer Start/End; fallback Time Consumed)
df_real["Consumed_Minutes"] = np.nan

cons_col = "Time Consumed" if "Time Consumed" in df_real.columns else None
start_col = "Start" if "Start" in df_real.columns else None
end_col = "End" if "End" in df_real.columns else None
req_col = "Requested Time" if "Requested Time" in df_real.columns else None

# If Time Consumed is timedelta, convert directly (correct)
if cons_col and pd.api.types.is_timedelta64_dtype(df_real[cons_col]):
    df_real["Consumed_Minutes"] = df_real[cons_col].dt.total_seconds() / 60.0

def calc_consumed_minutes(row):
    # prefer Start/End
    if start_col and end_col:
        s_min = time_to_minutes(row[start_col], default=np.nan)
        e_min = time_to_minutes(row[end_col], default=np.nan)
        if not np.isnan(s_min) and not np.isnan(e_min):
            dur = e_min - s_min
            if dur < 0:
                dur += 24*60  # crossed midnight
            return dur
    # fallback Time Consumed
    if cons_col:
        return time_to_minutes(row[cons_col], default=np.nan)
    return np.nan

need_calc = df_real["Consumed_Minutes"].isna()
df_real.loc[need_calc, "Consumed_Minutes"] = df_real.loc[need_calc].apply(calc_consumed_minutes, axis=1)
df_real["Consumed_Minutes"] = df_real["Consumed_Minutes"].fillna(0.0)
df_real["Consumed_Hours"] = df_real["Consumed_Minutes"] / 60.0

# Hour of day (0..23)
df_real["HourOfDay"] = df_real.apply(lambda r: get_hour_of_day(r.get(start_col, np.nan), r.get(req_col, np.nan)), axis=1)

# Job category
if "Job" in df_real.columns:
    df_real["Job_Category"] = df_real["Job"].apply(normalize_job)
else:
    df_real["Job_Category"] = "Other"

# Notification status
if "Notification No." in df_real.columns:
    df_real["Notification_Status"] = df_real["Notification No."].apply(lambda x: "Without Notification" if is_blank(x) else "With Notification")
else:
    df_real["Notification_Status"] = "Unknown"

# Reason clean
prob_col = "Reported Problem" if "Reported Problem" in df_real.columns else None
type_col = "Type" if "Type" in df_real.columns else None
fallback_series = df_real[type_col].fillna("unknown") if type_col else "unknown"
if prob_col:
    df_real["Reason_Clean"] = [
        clean_reason(p, fallback=clean_reason(f, fallback="unknown"))
        for p, f in zip(df_real[prob_col].fillna(""), fallback_series)
    ]
else:
    df_real["Reason_Clean"] = fallback_series.astype(str).apply(lambda s: clean_reason(s, fallback="unknown"))

# Machine column must exist
if "Machine No." not in df_real.columns:
    raise ValueError("Machine No. column not found. Cannot build report.")

# ---------------------------
# 6) Filter report period
# ---------------------------
START_DATE = date(2026, 1, 1)
END_DATE   = date(2026, 2, 26)

df_period = df_real[(df_real["Date_Clean"] >= START_DATE) & (df_real["Date_Clean"] <= END_DATE)].copy()
print("Rows in report period:", len(df_period), "| Days:", df_period["Date_Clean"].nunique())

# ---------------------------
# 7) Technician log (FULL credit rule, NOT divided)
# ---------------------------
tech_log = []
if "Performed By" in df_period.columns:
    for _, row in df_period.iterrows():
        for t in split_techs(row["Performed By"]):
            tech_log.append({
                "Date_Clean": row["Date_Clean"],
                "Technician": t,
                "Machine No.": row["Machine No."],
                "Shift": row.get("Shift", np.nan),
                "Job_Category": row["Job_Category"],
                "Notification_Status": row["Notification_Status"],
                "Consumed_Minutes": row["Consumed_Minutes"],   # FULL credit
                "Consumed_Hours": row["Consumed_Hours"]
            })
tech_log = pd.DataFrame(tech_log)

# ---------------------------
# 8) KPIs (1–11 + extra manager KPIs)
# ---------------------------
# KPI 1: Date x Machine downtime
kpi1 = pd.pivot_table(df_period, index="Date_Clean", columns="Machine No.", values="Consumed_Hours", aggfunc="sum", fill_value=0).sort_index()
kpi1["Grand Total"] = kpi1.sum(axis=1)

# KPI 2: Notifications vs no notifications
kpi2 = df_period.groupby(["Date_Clean","Notification_Status"]).size().unstack(fill_value=0).sort_index()
kpi2["Total Jobs"] = kpi2.sum(axis=1)
kpi2["% Without Notification"] = (kpi2.get("Without Notification", 0) / kpi2["Total Jobs"] * 100).round(2)

# KPI 3: Shift downtime
kpi3 = df_period.groupby(df_period.get("Shift","Unknown"))["Consumed_Hours"].sum().sort_values(ascending=False).to_frame("Downtime_Hours")
kpi3["% Share"] = (kpi3["Downtime_Hours"] / kpi3["Downtime_Hours"].sum() * 100).round(2)

# KPI 4: Job category (count + downtime)
kpi4_count = df_period.groupby("Job_Category").size().to_frame("Jobs_Count").sort_values("Jobs_Count", ascending=False)
kpi4_time  = df_period.groupby("Job_Category")["Consumed_Hours"].sum().to_frame("Downtime_Hours").sort_values("Downtime_Hours", ascending=False)

# KPI 5: Waiting time by date
kpi5 = df_period.groupby("Date_Clean")["Waiting_Hours"].sum().to_frame("Waiting_Hours").sort_index()

# KPI 6: MTTR & MTBF (Breakdown = B/D)
df_bd = df_period[df_period["Job_Category"]=="Breakdown"].copy()
bd_events = len(df_bd)
bd_downtime = df_bd["Consumed_Hours"].sum()
distinct_days = df_period["Date_Clean"].nunique()

total_running_hours = distinct_days * RUN_HOURS_PER_DAY  # ASSUMPTION used here
overall_mttr = (bd_downtime / bd_events) if bd_events else 0.0
overall_mtbf = (total_running_hours / bd_events) if bd_events else 0.0

kpi6_overall = pd.DataFrame({
    "Metric": ["Distinct Days", "RUN_HOURS_PER_DAY (assumption)", "Total Running Hours", "Breakdown Events (B/D)", "Breakdown Downtime (hrs)", "MTTR (hrs)", "MTBF (hrs)"],
    "Value":  [distinct_days, RUN_HOURS_PER_DAY, total_running_hours, bd_events, round(bd_downtime,2), round(overall_mttr,2), round(overall_mtbf,2)]
})

kpi6_machine = df_bd.groupby("Machine No.").agg(
    Breakdown_Events=("Consumed_Hours","size"),
    Breakdown_Downtime_Hours=("Consumed_Hours","sum")
).sort_values("Breakdown_Downtime_Hours", ascending=False)
kpi6_machine["MTTR_Hrs"] = (kpi6_machine["Breakdown_Downtime_Hours"] / kpi6_machine["Breakdown_Events"]).round(2)
kpi6_machine["MTBF_Hrs"] = (total_running_hours / kpi6_machine["Breakdown_Events"]).replace([np.inf], 0).round(2)

# KPI 7: Hourly pattern 0–23
kpi7 = df_period.dropna(subset=["HourOfDay"]).groupby("HourOfDay")["Consumed_Hours"].sum().reindex(range(24), fill_value=0).to_frame("Downtime_Hours")

# KPI 8: Date x hour heatmap table
kpi8 = df_period.dropna(subset=["HourOfDay"]).pivot_table(index="Date_Clean", columns="HourOfDay", values="Consumed_Hours", aggfunc="sum", fill_value=0).reindex(columns=range(24), fill_value=0).sort_index()

# KPI 9: Technician workload (FULL credit, not divided)
kpi9 = tech_log.pivot_table(index="Technician", columns="Job_Category", values="Consumed_Hours", aggfunc="sum", fill_value=0)
kpi9["Total_Hours"] = kpi9.sum(axis=1)
kpi9 = kpi9.sort_values("Total_Hours", ascending=False)

# KPI 10: Top 10 breakdown reasons
kpi10 = df_bd.groupby("Reason_Clean").agg(
    Downtime_Hours=("Consumed_Hours","sum"),
    Incidents=("Reason_Clean","size")
).sort_values("Downtime_Hours", ascending=False).head(10)

# KPI 11: Top 13 machines (Breakdown)
kpi11 = df_bd.groupby("Machine No.").agg(
    Downtime_Hours=("Consumed_Hours","sum"),
    Incidents=("Machine No.","size")
).sort_values("Downtime_Hours", ascending=False).head(13)

# Extra: Availability + Pareto + concentration
planned_hours_total = distinct_days * PLANNED_AVAILABLE_HOURS_PER_DAY
total_downtime_all = df_period["Consumed_Hours"].sum()
overall_availability = (1 - (total_downtime_all / planned_hours_total)) * 100 if planned_hours_total else 0.0

pareto = df_period.groupby("Machine No.")["Consumed_Hours"].sum().sort_values(ascending=False).to_frame("Downtime_Hours")
pareto["% of Total"] = (pareto["Downtime_Hours"] / pareto["Downtime_Hours"].sum() * 100).round(2)
pareto["Cumulative %"] = pareto["% of Total"].cumsum().round(2)

def share_top(n):
    total = pareto["Downtime_Hours"].sum()
    return round(pareto.head(n)["Downtime_Hours"].sum()/total*100, 2) if total else 0.0

concentration = pd.DataFrame({
    "Metric": ["Top 3 share %", "Top 5 share %", "Top 10 share %"],
    "Value": [share_top(3), share_top(5), share_top(10)]
})

# ---------------------------
# 9) Charts (PDF-friendly style)
# ---------------------------
sns.set_theme(style="whitegrid")
COLOR_MAIN = "#1f77b4"
images = {}

def fig_to_b64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")

# Daily downtime trend
fig, ax = plt.subplots(figsize=(10,4))
ax.plot(kpi1.index, kpi1["Grand Total"], color=COLOR_MAIN, linewidth=2)
ax.set_title("Daily Total Downtime (hrs) — Drinks Section")
ax.set_xlabel("Date"); ax.set_ylabel("Downtime (hrs)")
ax.tick_params(axis="x", rotation=45)
images["trend"] = fig_to_b64(fig)

# Top 13 machines downtime (overall)
fig, ax = plt.subplots(figsize=(10,4))
ax.bar(pareto.head(13).index.astype(str), pareto.head(13)["Downtime_Hours"], color=COLOR_MAIN)
ax.set_title("Top 13 Machines by Total Downtime (hrs)")
ax.set_xlabel("Machine"); ax.set_ylabel("Downtime (hrs)")
ax.tick_params(axis="x", rotation=45)
images["top13"] = fig_to_b64(fig)

# Pareto chart
fig, ax1 = plt.subplots(figsize=(10,4))
ax1.bar(pareto.index.astype(str), pareto["Downtime_Hours"], color=COLOR_MAIN, alpha=0.85)
ax1.set_ylabel("Downtime (hrs)"); ax1.set_xlabel("Machine")
ax1.tick_params(axis="x", rotation=45)
ax2 = ax1.twinx()
ax2.plot(pareto.index.astype(str), pareto["Cumulative %"], color="#d62728", marker="o", linewidth=2)
ax2.set_ylabel("Cumulative %"); ax2.set_ylim(0,110)
ax1.set_title("Pareto: Machine Downtime (hrs) + Cumulative %")
images["pareto"] = fig_to_b64(fig)

# Heatmap Date x Machine (top 13 for readability)
top_cols = [c for c in pareto.head(13).index if c in kpi1.columns]
heat_dm = kpi1[top_cols].copy()
fig, ax = plt.subplots(figsize=(12,6))
sns.heatmap(heat_dm, cmap="Blues", ax=ax)
ax.set_title("Heatmap: Date × Machine Downtime (Top machines)")
ax.set_xlabel("Machine"); ax.set_ylabel("Date")
images["heat_date_machine"] = fig_to_b64(fig)

# Shift downtime
fig, ax = plt.subplots(figsize=(8,4))
ax.bar(kpi3.index.astype(str), kpi3["Downtime_Hours"], color=COLOR_MAIN)
ax.set_title("Downtime by Shift (hrs)")
ax.set_xlabel("Shift"); ax.set_ylabel("Downtime (hrs)")
images["shift"] = fig_to_b64(fig)

# Waiting trend
fig, ax = plt.subplots(figsize=(10,4))
ax.plot(kpi5.index, kpi5["Waiting_Hours"], color="#2ca02c", linewidth=2)
ax.set_title("Daily Total Waiting Time (hrs)")
ax.set_xlabel("Date"); ax.set_ylabel("Waiting (hrs)")
ax.tick_params(axis="x", rotation=45)
images["waiting"] = fig_to_b64(fig)

# Hourly pattern 0-23
fig, ax = plt.subplots(figsize=(10,4))
ax.bar(kpi7.index, kpi7["Downtime_Hours"], color=COLOR_MAIN)
ax.set_title("Downtime Pattern by Hour (0–23)")
ax.set_xlabel("Hour of Day"); ax.set_ylabel("Downtime (hrs)")
ax.set_xticks(range(24))
images["hourly"] = fig_to_b64(fig)

# Date x hour heatmap (last 30 days)
heat_dh = kpi8.tail(30)
fig, ax = plt.subplots(figsize=(12,6))
sns.heatmap(heat_dh, cmap="Blues", ax=ax)
ax.set_title("Heatmap: Date × Hour Downtime (Last 30 days)")
ax.set_xlabel("Hour of Day"); ax.set_ylabel("Date")
images["heat_date_hour"] = fig_to_b64(fig)

# Technician Top 10
toptech = kpi9.head(10)["Total_Hours"] if len(kpi9) else pd.Series(dtype=float)
fig, ax = plt.subplots(figsize=(10,4))
if len(toptech):
    ax.bar(toptech.index.astype(str), toptech.values, color=COLOR_MAIN)
ax.set_title("Top 10 Technicians by Workload (hrs) — FULL credit (not divided)")
ax.set_xlabel("Technician"); ax.set_ylabel("Hours")
ax.tick_params(axis="x", rotation=45)
images["tech"] = fig_to_b64(fig)

# Top 10 reasons
fig, ax = plt.subplots(figsize=(10,4))
if len(kpi10):
    ax.barh(kpi10.index.astype(str)[::-1], kpi10["Downtime_Hours"].values[::-1], color=COLOR_MAIN)
ax.set_title("Top 10 Breakdown Reasons by Downtime (hrs)")
ax.set_xlabel("Downtime (hrs)")
images["reasons"] = fig_to_b64(fig)

# ---------------------------
# 10) Build HTML (self-contained)
# ---------------------------
def df_to_html(df, title, max_rows=30):
    df2 = df.copy()
    if len(df2) > max_rows:
        df2 = df2.head(max_rows)
    # format floats
    for c in df2.columns:
        if pd.api.types.is_float_dtype(df2[c]):
            df2[c] = df2[c].map(lambda x: f"{x:,.2f}")
    return f"<h3>{title}</h3>" + df2.to_html(border=0, classes="table")

def img(key):
    return f"data:image/png;base64,{images[key]}"

REPORT_TITLE = "Drinks Section KPIs Report — 01 Jan 2026 to 26 Feb 2026"

html = f"""
<!doctype html>
<html><head><meta charset="utf-8"/>
<title>{REPORT_TITLE}</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 24px; color: #111; }}
h1 {{ margin-bottom: 0; }}
.sub {{ color: #555; margin-top: 6px; }}
.note {{ font-size: 12px; color: #444; }}
.cards {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin: 16px 0; }}
.card {{ border: 1px solid #e5e5e5; border-radius: 10px; padding: 12px 14px; background: #fff; }}
.k {{ font-size: 12px; color: #666; }}
.v {{ font-size: 22px; font-weight: 700; margin-top: 6px; }}
img.chart {{ width: 100%; max-width: 1100px; border: 1px solid #eee; border-radius: 10px; padding: 6px; background: #fff; }}
table.table {{ border-collapse: collapse; width: 100%; margin: 10px 0 18px 0; }}
table.table th, table.table td {{ border: 1px solid #e6e6e6; padding: 6px 8px; font-size: 12px; }}
table.table th {{ background: #f6f8fa; text-align: left; }}
.two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }}
.section {{ page-break-inside: avoid; margin-top: 22px; }}
</style>
</head><body>

<h1>{REPORT_TITLE}</h1>
<div class="sub">Manager-ready maintenance & downtime report (PDF-friendly)</div>

<div class="section">
<h2>1) Executive Summary</h2>
<div class="cards">
  <div class="card"><div class="k">Total Downtime (hrs)</div><div class="v">{total_downtime_all:,.2f}</div></div>
  <div class="card"><div class="k">Availability %</div><div class="v">{overall_availability:,.2f}%</div></div>
  <div class="card"><div class="k">MTTR (hrs) — Breakdown</div><div class="v">{overall_mttr:,.2f}</div></div>
  <div class="card"><div class="k">MTBF (hrs) — Breakdown</div><div class="v">{overall_mtbf:,.2f}</div></div>
</div>
<p class="note">
<b>MTBF assumption:</b> RUN_HOURS_PER_DAY = {RUN_HOURS_PER_DAY} hours/day.<br>
<b>Availability assumption:</b> PLANNED_AVAILABLE_HOURS_PER_DAY = {PLANNED_AVAILABLE_HOURS_PER_DAY} hours/day.
</p>
{img('trend')}
</div>

<div class="section">
<h2>2) Machine Downtime (KPI 1 + KPI 11)</h2>
<div class="two-col">
  {img('top13')}
  {img('pareto')}
</div>
{img('heat_date_machine')}
{df_to_html(pareto, "Pareto table (machines)", max_rows=30)}
{df_to_html(concentration, "Downtime concentration (Top shares)", max_rows=10)}
</div>

<div class="section">
<h2>3) Notifications (KPI 2)</h2>
{df_to_html(kpi2, "Jobs with Notification vs Without Notification (by date)", max_rows=31)}
</div>

<div class="section">
<h2>4) Shifts & Job Types (KPI 3 + KPI 4)</h2>
{img('shift')}
{df_to_html(kpi3, "Downtime by Shift", max_rows=10)}
<div class="two-col">
  <div>{df_to_html(kpi4_count, "Job Count by Category", max_rows=10)}</div>
  <div>{df_to_html(kpi4_time, "Downtime Hours by Category", max_rows=10)}</div>
</div>
</div>

<div class="section">
<h2>5) Waiting Time (KPI 5)</h2>
{img('waiting')}
{df_to_html(kpi5, "Waiting Hours by Date", max_rows=31)}
</div>

<div class="section">
<h2>6) Reliability (KPI 6: MTTR + MTBF)</h2>
{df_to_html(kpi6_overall, "Overall MTTR / MTBF Summary", max_rows=20)}
{df_to_html(kpi6_machine, "Per-machine MTTR/MTBF (sorted by downtime)", max_rows=30)}
</div>

<div class="section">
<h2>7) Time Pattern (KPI 7 + KPI 8)</h2>
{img('hourly')}
{img('heat_date_hour')}
</div>

<div class="section">
<h2>8) Technician Performance (KPI 9)</h2>
<p class="note"><b>Workload rule:</b> Each technician receives FULL job minutes (not divided).</p>
{img('tech')}
{df_to_html(kpi9, "Technician workload (hours) by job category (Top 30)", max_rows=30)}
</div>

<div class="section">
<h2>9) Breakdown Reasons (KPI 10)</h2>
{img('reasons')}
{df_to_html(kpi10, "Top 10 Breakdown Reasons (by downtime hours)", max_rows=10)}
</div>

<div class="section">
<h2>Appendix: KPI 1 (Date × Machine downtime)</h2>
<p class="note">Shown for transparency/audit. Can be large.</p>
{kpi1.round(2).to_html(border=0, classes="table")}
</div>

</body></html>
"""

out_name = "Drinks_Section_KPIs_Report_2026-01-01_to_2026-02-26.html"
with open(out_name, "w", encoding="utf-8") as f:
    f.write(html)

print("Report saved:", out_name)

# ---------------------------
# 11) Download the report
# ---------------------------
files.download(out_name)
