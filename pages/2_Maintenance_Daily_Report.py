import streamlit as st
import pandas as pd
import numpy as np
import re

st.set_page_config(page_title="Maintenance KPI", layout="wide")
st.title("Maintenance Daily KPI Report")

# ======================================================
# FILE UPLOAD
# ======================================================
file = st.file_uploader("Upload Maintenance Log Sheet", type=["xlsx", "xlsm", "xls"])
if file is None:
    st.stop()

# ======================================================
# READ EXCEL (pick correct sheet)
# ======================================================
xls = pd.ExcelFile(file)

# Prefer a sheet named like "Main Data" (case-insensitive), else pick largest sheet
preferred = None
for s in xls.sheet_names:
    if s.strip().lower() in ["main data", "maindata", "main"]:
        preferred = s
        break

if preferred:
    df = pd.read_excel(file, sheet_name=preferred)
else:
    # choose sheet with most rows
    dfs = {s: pd.read_excel(file, sheet_name=s) for s in xls.sheet_names}
    preferred = max(dfs, key=lambda s: len(dfs[s]))
    df = dfs[preferred]

st.caption(f"✅ Using sheet: **{preferred}** | Rows: **{len(df)}** | Cols: **{len(df.columns)}**")

# ======================================================
# NORMALIZE COLUMN NAMES
# ======================================================
def norm_col(c):
    c = str(c).strip().lower()
    c = re.sub(r"[._/()-]+", " ", c)      # remove punctuation into spaces
    c = re.sub(r"\s+", " ", c).strip()   # collapse spaces
    return c

df.columns = [norm_col(c) for c in df.columns]

# Optional: show columns so you can verify matches
with st.expander("🔎 Detected columns (after cleaning)"):
    st.write(df.columns.tolist())

def has(col): 
    return col in df.columns

# ======================================================
# TYPE FIXES
# ======================================================
# Numeric conversions
for c in ["time consumed", "waiting time"]:
    if has(c):
        df[c] = pd.to_numeric(df[c], errors="coerce")

# Standardize Job values
if has("job"):
    df["job"] = df["job"].astype(str).str.strip().str.upper()

# ======================================================
# KPI CALCULATION
# ======================================================
kpis = []
kpis.append(("Total Jobs", len(df)))

# Notifications / Machines
if has("notification no"):
    kpis.append(("Unique Notifications", df["notification no"].nunique(dropna=True)))
if has("machine no"):
    kpis.append(("Unique Machines", df["machine no"].nunique(dropna=True)))

# Job breakdown (only if those categories exist)
if has("job"):
    kpis.append(("Breakdown Jobs (B/D)", (df["job"] == "B/D").sum()))
    kpis.append(("Corrective Jobs", (df["job"] == "CORRECTIVE").sum()))
    kpis.append(("PM Jobs", (df["job"] == "PM").sum()))

# Time KPIs
if has("time consumed"):
    kpis.append(("Total Downtime", round(df["time consumed"].sum(), 2)))
    kpis.append(("MTTR (Avg)", round(df["time consumed"].mean(), 2)))
    kpis.append(("Max Repair Time", round(df["time consumed"].max(), 2)))
    kpis.append(("Min Repair Time", round(df["time consumed"].min(), 2)))

if has("waiting time"):
    kpis.append(("Total Waiting Time", round(df["waiting time"].sum(), 2)))
    kpis.append(("Avg Waiting Time", round(df["waiting time"].mean(), 2)))

# Top machine downtime
if has("machine no") and has("time consumed"):
    top_machine = (
        df.groupby("machine no")["time consumed"]
        .sum()
        .sort_values(ascending=False)
        .head(3)
    )
    for i, (m, t) in enumerate(top_machine.items(), 1):
        kpis.append((f"Top {i} Machine Downtime", f"{m} ({round(t,2)})"))

# Shift/Area counts
if has("shift"):
    for s, c in df["shift"].value_counts(dropna=True).items():
        kpis.append((f"Jobs – {s} Shift", int(c)))

if has("area"):
    for a, c in df["area"].value_counts(dropna=True).head(6).items():
        kpis.append((f"Jobs – Area {a}", int(c)))

# Top techs
if has("performed by"):
    top_tech = df["performed by"].astype(str).str.strip().value_counts().head(3)
    for i, (t, c) in enumerate(top_tech.items(), 1):
        kpis.append((f"Top {i} Technician", f"{t} ({int(c)} jobs)"))

# ======================================================
# OUTPUT KPI CARDS + TABLE
# ======================================================
st.subheader("✅ KPI Summary")

# KPI cards (first 12 as cards)
cards = kpis[:12]
cols = st.columns(4)
for i, (k, v) in enumerate(cards):
    cols[i % 4].metric(k, v)

st.divider()
kpi_df = pd.DataFrame(kpis, columns=["KPI", "Value"])
st.dataframe(kpi_df, use_container_width=True)
