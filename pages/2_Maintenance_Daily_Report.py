import streamlit as st
import pandas as pd
import numpy as np
import re

st.set_page_config(page_title="Maintenance KPI Dashboard", layout="wide")
st.title("🛠 Maintenance KPI Dashboard")

# ======================================================
# Helpers
# ======================================================
def norm_col(c):
    c = str(c).strip().lower()
    c = re.sub(r"[._/()-]+", " ", c)
    c = re.sub(r"\s+", " ", c).strip()
    return c

def excel_time_to_minutes(x):
    """
    Convert Excel time or datetime to minutes.
    Excel stores time as fraction of a day.
    """
    if pd.isna(x):
        return np.nan

    # datetime -> seconds
    if isinstance(x, pd.Timestamp):
        return x.hour * 60 + x.minute + x.second / 60

    # numeric fraction of day
    if isinstance(x, (int, float)):
        return x * 24 * 60

    return np.nan

def has(col):
    return col in df.columns

def fmt(x, d=2):
    if pd.isna(x):
        return "-"
    return f"{x:,.{d}f}"

# ======================================================
# Upload
# ======================================================
file = st.file_uploader("Upload Maintenance Log Sheet", type=["xlsx", "xlsm", "xls"])
if file is None:
    st.stop()

xls = pd.ExcelFile(file)

# Pick Main Data or largest sheet
sheet = next((s for s in xls.sheet_names if s.lower().strip() in ["main data", "maindata"]), None)
if sheet is None:
    sheet = max(xls.sheet_names, key=lambda s: pd.read_excel(file, sheet_name=s).shape[0])

df = pd.read_excel(file, sheet_name=sheet)
st.caption(f"Using sheet: **{sheet}** | Rows: **{len(df)}**")

# ======================================================
# Clean columns
# ======================================================
df.columns = [norm_col(c) for c in df.columns]

# ======================================================
# Parse & FIX time columns
# ======================================================
# Datetime columns
for c in ["date", "start", "end"]:
    if has(c):
        df[c] = pd.to_datetime(df[c], errors="coerce")

# Convert Excel time → minutes
for c in ["time consumed", "waiting time"]:
    if has(c):
        df[c] = df[c].apply(excel_time_to_minutes)

# Job normalization
if has("job"):
    df["job"] = df["job"].astype(str).str.strip().str.upper()

# ======================================================
# Filters
# ======================================================
st.sidebar.header("Filters")
df_f = df.copy()

if has("date"):
    dmin, dmax = df_f["date"].min(), df_f["date"].max()
    if pd.notna(dmin) and pd.notna(dmax):
        dr = st.sidebar.date_input(
            "Date range",
            (dmin.date(), dmax.date()),
            min_value=dmin.date(),
            max_value=dmax.date()
        )
        df_f = df_f[(df_f["date"].dt.date >= dr[0]) & (df_f["date"].dt.date <= dr[1])]

def mfilter(col, label):
    global df_f
    if has(col):
        opts = sorted(df_f[col].dropna().astype(str).unique())
        sel = st.sidebar.multiselect(label, opts)
        if sel:
            df_f = df_f[df_f[col].astype(str).isin(sel)]

mfilter("area", "Area")
mfilter("shift", "Shift")
mfilter("type", "Type")
mfilter("machine no", "Machine No")
mfilter("performed by", "Technician")

st.sidebar.caption(f"Filtered rows: {len(df_f)}")

# ======================================================
# KPI CALCULATION (CORRECT)
# ======================================================
total_jobs = len(df_f)

total_down = df_f["time consumed"].sum() if has("time consumed") else np.nan
avg_down = df_f["time consumed"].mean() if has("time consumed") else np.nan
p95_down = df_f["time consumed"].quantile(0.95) if has("time consumed") else np.nan
max_down = df_f["time consumed"].max() if has("time consumed") else np.nan

total_wait = df_f["waiting time"].sum() if has("waiting time") else np.nan
avg_wait = df_f["waiting time"].mean() if has("waiting time") else np.nan

wait_share = (total_wait / (total_wait + total_down)) if (total_wait + total_down) > 0 else np.nan

# Start-End duration
avg_duration = np.nan
if has("start") and has("end"):
    dur = (df_f["end"] - df_f["start"]).dt.total_seconds() / 60
    dur = dur.where(dur >= 0)
    avg_duration = dur.mean()

# ======================================================
# KPI DISPLAY
# ======================================================
st.subheader("✅ Key KPIs (Minutes)")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Jobs", total_jobs)
c2.metric("Total Downtime (min)", fmt(total_down))
c3.metric("MTTR (Avg min)", fmt(avg_down))
c4.metric("Max Repair Time (min)", fmt(max_down))

c5, c6, c7, c8 = st.columns(4)
c5.metric("P95 Repair Time (min)", fmt(p95_down))
c6.metric("Total Waiting Time (min)", fmt(total_wait))
c7.metric("Avg Waiting Time (min)", fmt(avg_wait))
c8.metric("Waiting Share", f"{fmt(wait_share*100)}%")

c9, _, _, _ = st.columns(4)
c9.metric("Avg Start → End Duration (min)", fmt(avg_duration))

# ======================================================
# TOP DRIVERS
# ======================================================
st.subheader("🏆 Top Drivers")

if has("machine no") and has("time consumed"):
    top_m = (
        df_f.groupby("machine no")["time consumed"]
        .sum().sort_values(ascending=False).head(10)
        .reset_index()
    )
    st.markdown("**Top Machines by Downtime (min)**")
    st.dataframe(top_m, use_container_width=True)

if has("type") and has("time consumed"):
    top_t = (
        df_f.groupby("type")["time consumed"]
        .sum().sort_values(ascending=False).head(10)
        .reset_index()
    )
    st.markdown("**Top Types by Downtime (min)**")
    st.dataframe(top_t, use_container_width=True)
