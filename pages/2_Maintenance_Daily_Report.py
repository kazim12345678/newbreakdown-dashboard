import streamlit as st
import pandas as pd
import numpy as np
import re

st.set_page_config(page_title="Maintenance KPI Dashboard", layout="wide")
st.title("🛠️ Maintenance KPI Dashboard")

# ---------------------------
# Helpers
# ---------------------------
def norm_col(c):
    c = str(c).strip().lower()
    c = re.sub(r"[._/()-]+", " ", c)      # punctuation -> space
    c = re.sub(r"\s+", " ", c).strip()   # collapse spaces
    return c

def fmt_num(x, decimals=2):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "-"
    if isinstance(x, (int, np.integer)):
        return f"{x:,}"
    if isinstance(x, (float, np.floating)):
        return f"{x:,.{decimals}f}"
    return str(x)

def safe_series_nonempty(s):
    if s is None:
        return pd.Series(dtype="object")
    return s.dropna()

# ---------------------------
# Upload
# ---------------------------
file = st.file_uploader("Upload Maintenance Log Sheet", type=["xlsx", "xlsm", "xls"])
if file is None:
    st.stop()

xls = pd.ExcelFile(file)
sheet_names = xls.sheet_names

# Prefer "Main Data" if exists, else use largest sheet
preferred = None
for s in sheet_names:
    if s.strip().lower() in ["main data", "maindata", "main"]:
        preferred = s
        break

if preferred:
    df = pd.read_excel(file, sheet_name=preferred)
else:
    dfs = {s: pd.read_excel(file, sheet_name=s) for s in sheet_names}
    preferred = max(dfs, key=lambda s: len(dfs[s]))
    df = dfs[preferred]

st.caption(f"✅ Using sheet: **{preferred}** | Rows: **{len(df):,}** | Columns: **{len(df.columns)}**")

# ---------------------------
# Clean columns
# ---------------------------
df.columns = [norm_col(c) for c in df.columns]

# Expected columns (after normalization)
# date, machine no, notification no, shift, area, machine classification,
# job, type, reported problem, requested time, description of work,
# spare part used, start, end, waiting time, time consumed, performed by, remarks

def has(col): return col in df.columns

# ---------------------------
# Parse types
# ---------------------------
if has("date"):
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

for c in ["requested time", "start", "end"]:
    if has(c):
        df[c] = pd.to_datetime(df[c], errors="coerce")

for c in ["waiting time", "time consumed"]:
    if has(c):
        df[c] = pd.to_numeric(df[c], errors="coerce")

if has("job"):
    df["job"] = df["job"].astype(str).str.strip().str.upper()

# ---------------------------
# Sidebar filters
# ---------------------------
st.sidebar.header("🔎 Filters")

df_f = df.copy()

# Date filter
if has("date"):
    dmin = df_f["date"].min()
    dmax = df_f["date"].max()
    if pd.notna(dmin) and pd.notna(dmax):
        start_date, end_date = st.sidebar.date_input(
            "Date range",
            value=(dmin.date(), dmax.date()),
            min_value=dmin.date(),
            max_value=dmax.date()
        )
        df_f = df_f[(df_f["date"].dt.date >= start_date) & (df_f["date"].dt.date <= end_date)]

# Dropdown filters
def sidebar_multiselect(col, label):
    global df_f
    if has(col):
        vals = sorted(safe_series_nonempty(df_f[col].astype(str).str.strip()).unique().tolist())
        if len(vals) > 0:
            sel = st.sidebar.multiselect(label, vals, default=[])
            if sel:
                df_f = df_f[df_f[col].astype(str).str.strip().isin(sel)]

sidebar_multiselect("area", "Area")
sidebar_multiselect("shift", "Shift")
sidebar_multiselect("type", "Type")
sidebar_multiselect("machine classification", "Machine Classification")
sidebar_multiselect("machine no", "Machine No")
sidebar_multiselect("performed by", "Performed By")

st.sidebar.caption(f"Filtered rows: **{len(df_f):,}**")

# ---------------------------
# KPI Calculations
# ---------------------------
total_jobs = len(df_f)

unique_notifications = df_f["notification no"].nunique(dropna=True) if has("notification no") else np.nan
unique_machines = df_f["machine no"].nunique(dropna=True) if has("machine no") else np.nan
unique_techs = df_f["performed by"].nunique(dropna=True) if has("performed by") else np.nan
unique_areas = df_f["area"].nunique(dropna=True) if has("area") else np.nan

total_down = df_f["time consumed"].sum() if has("time consumed") else np.nan
avg_down = df_f["time consumed"].mean() if has("time consumed") else np.nan
p95_down = df_f["time consumed"].quantile(0.95) if has("time consumed") else np.nan
max_down = df_f["time consumed"].max() if has("time consumed") else np.nan

total_wait = df_f["waiting time"].sum() if has("waiting time") else np.nan
avg_wait = df_f["waiting time"].mean() if has("waiting time") else np.nan

wait_share = np.nan
if has("waiting time") and has("time consumed"):
    denom = (df_f["waiting time"].sum() + df_f["time consumed"].sum())
    wait_share = (df_f["waiting time"].sum() / denom) if denom and denom > 0 else np.nan

# Duration from start-end (if available)
valid_duration_count = np.nan
avg_duration = np.nan
if has("start") and has("end"):
    dur_min = (df_f["end"] - df_f["start"]).dt.total_seconds() / 60
    dur_min = dur_min.where(dur_min >= 0)
    valid_duration_count = dur_min.notna().sum()
    avg_duration = dur_min.mean()

# Data completeness
def fill_rate(col):
    if not has(col): return np.nan
    s = df_f[col].astype(str).str.strip()
    return ((s.notna()) & (s != "") & (s.str.lower() != "nan")).mean()

reported_problem_rate = fill_rate("reported problem")
desc_work_rate = fill_rate("description of work")
remarks_rate = fill_rate("remarks")
spare_rate = fill_rate("spare part used")

# ---------------------------
# KPI Display (Cards)
# ---------------------------
st.subheader("✅ Key KPI Cards")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Jobs", fmt_num(total_jobs, 0))
c2.metric("Unique Notifications", fmt_num(unique_notifications, 0))
c3.metric("Unique Machines", fmt_num(unique_machines, 0))
c4.metric("Unique Technicians", fmt_num(unique_techs, 0))

c5, c6, c7, c8 = st.columns(4)
c5.metric("Total Downtime (Time Consumed)", fmt_num(total_down))
c6.metric("MTTR (Avg Time Consumed)", fmt_num(avg_down))
c7.metric("P95 Repair Time", fmt_num(p95_down))
c8.metric("Max Repair Time", fmt_num(max_down))

c9, c10, c11, c12 = st.columns(4)
c9.metric("Total Waiting Time", fmt_num(total_wait))
c10.metric("Avg Waiting Time", fmt_num(avg_wait))
c11.metric("Waiting Share", f"{fmt_num(wait_share*100)}%" if pd.notna(wait_share) else "-")
c12.metric("Avg Start→End Duration (min)", fmt_num(avg_duration) if pd.notna(avg_duration) else "-")

st.divider()

# ---------------------------
# Breakdown tables (Top-N)
# ---------------------------
st.subheader("🏆 Top Drivers (Where the time is going)")

left, right = st.columns(2)

with left:
    if has("machine no") and has("time consumed"):
        top_m = (df_f.groupby("machine no")["time consumed"]
                 .sum().sort_values(ascending=False).head(10).reset_index())
        top_m.columns = ["Machine No", "Total Time Consumed"]
        st.markdown("**Top 10 Machines by Downtime**")
        st.dataframe(top_m, use_container_width=True)
    else:
        st.info("Machine downtime table needs: machine no + time consumed")

with right:
    if has("type") and has("time consumed"):
        top_t = (df_f.groupby("type")["time consumed"]
                 .sum().sort_values(ascending=False).head(10).reset_index())
        top_t.columns = ["Type", "Total Time Consumed"]
        st.markdown("**Top 10 Types by Downtime**")
        st.dataframe(top_t, use_container_width=True)
    else:
        st.info("Type downtime table needs: type + time consumed")

st.divider()

# ---------------------------
# Trend charts (Date)
# ---------------------------
st.subheader("📈 Trends Over Time")

if has("date"):
    trend = df_f.copy()
    trend["day"] = trend["date"].dt.date

    cols = st.columns(2)

    with cols[0]:
        jobs_day = trend.groupby("day").size().reset_index(name="jobs")
        st.markdown("**Jobs per Day**")
        st.line_chart(jobs_day.set_index("day")["jobs"])

    with cols[1]:
        if has("time consumed"):
            down_day = trend.groupby("day")["time consumed"].sum().reset_index(name="downtime")
            st.markdown("**Downtime per Day (Time Consumed)**")
            st.line_chart(down_day.set_index("day")["downtime"])
        else:
            st.info("Downtime trend needs: time consumed")
else:
    st.info("Trends need: date column")

st.divider()

# ---------------------------
# Data Quality
# ---------------------------
st.subheader("🧾 Data Quality (How complete is the log?)")
q1, q2, q3, q4 = st.columns(4)
q1.metric("% Reported Problem filled", f"{fmt_num(reported_problem_rate*100)}%" if pd.notna(reported_problem_rate) else "-")
q2.metric("% Description of Work filled", f"{fmt_num(desc_work_rate*100)}%" if pd.notna(desc_work_rate) else "-")
q3.metric("% Remarks filled", f"{fmt_num(remarks_rate*100)}%" if pd.notna(remarks_rate) else "-")
q4.metric("% Spare Part Used filled", f"{fmt_num(spare_rate*100)}%" if pd.notna(spare_rate) else "-")

st.divider()

# ---------------------------
# Show filtered data (optional)
# ---------------------------
with st.expander("📄 View filtered data"):
    st.dataframe(df_f, use_container_width=True)
