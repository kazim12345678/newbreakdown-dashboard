import streamlit as st
import pandas as pd
import numpy as np

st.title("Maintenance Daily KPI Report")

# ======================================================
# FILE UPLOAD
# ======================================================
file = st.file_uploader("Upload Maintenance Log Sheet", type=["xlsx"])

if file is None:
    st.stop()

df = pd.read_excel(file)

# ======================================================
# CLEAN COLUMNS
# ======================================================
df.columns = df.columns.str.strip().str.lower()

def has(col):
    return col in df.columns

# Force numeric conversion
if has("time consumed"):
    df["time consumed"] = pd.to_numeric(df["time consumed"], errors="coerce")

# ======================================================
# KPI CALCULATION
# ======================================================
kpis = []

# ---- BASIC ----
kpis.append(("Total Jobs", len(df)))

# ---- JOB TYPE ----
if has("job"):
    job = df["job"].astype(str).str.upper()
    kpis.append(("Breakdown Jobs (B/D)", (job == "B/D").sum()))
    kpis.append(("Corrective Jobs", (job == "CORRECTIVE").sum()))
    kpis.append(("PM Jobs", (job == "PM").sum()))

# ---- TIME ----
if has("time consumed"):
    kpis.append(("Total Downtime (hrs)", round(df["time consumed"].sum(), 2)))
    kpis.append(("MTTR (Avg hrs)", round(df["time consumed"].mean(), 2)))
    kpis.append(("Max Repair Time (hrs)", round(df["time consumed"].max(), 2)))
    kpis.append(("Min Repair Time (hrs)", round(df["time consumed"].min(), 2)))

# ---- MACHINE ----
if has("machine no.") and has("time consumed"):
    top_machine = (
        df.groupby("machine no.")["time consumed"]
        .sum()
        .sort_values(ascending=False)
        .head(3)
    )
    for i, (m, t) in enumerate(top_machine.items(), 1):
        kpis.append((f"Top {i} Machine Downtime", f"{m} ({round(t,2)} hrs)"))

# ---- SHIFT ----
if has("shift"):
    for s, c in df["shift"].value_counts().items():
        kpis.append((f"Jobs – {s} Shift", c))

# ---- AREA ----
if has("area"):
    for a, c in df["area"].value_counts().items():
        kpis.append((f"Jobs – {a}", c))

# ---- TECHNICIAN ----
if has("performed by"):
    top_tech = df["performed by"].value_counts().head(3)
    for i, (t, c) in enumerate(top_tech.items(), 1):
        kpis.append((f"Top {i} Technician", f"{t} ({c} jobs)"))

# ======================================================
# OUTPUT
# ======================================================
kpi_df = pd.DataFrame(kpis, columns=["KPI", "Value"])
st.subheader("✅ KPI Summary")
st.dataframe(kpi_df, use_container_width=True)
