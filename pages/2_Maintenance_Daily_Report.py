import streamlit as st
import pandas as pd
import numpy as np

st.title("Maintenance Daily KPI Report")

# ======================================================
# LOAD EXCEL FILE (STREAMLIT SAFE)
# ======================================================
uploaded_file = st.file_uploader(
    "Upload Maintenance Log Sheet",
    type=["xlsx"]
)

if uploaded_file is None:
    st.info("⬆️ Please upload the maintenance Excel file")
    st.stop()

# Read first sheet only
df = pd.read_excel(uploaded_file)
df.columns = df.columns.str.strip().str.lower()

# ======================================================
# HELPER
# ======================================================
def has(col):
    return col in df.columns

kpis = []

# ======================================================
# BASIC KPIs
# ======================================================
kpis.append(("Total Jobs", len(df)))

# ======================================================
# JOB KPIs
# ======================================================
if has("job"):
    job = df["job"].astype(str).str.upper()
    kpis.append(("Breakdown Jobs (B/D)", (job == "B/D").sum()))
    kpis.append(("Corrective Jobs", (job == "CORRECTIVE").sum()))

# ======================================================
# TIME KPIs
# ======================================================
time_col = None
for c in ["time consumed", "maintenance time", "time consumed (minute)"]:
    if has(c):
        time_col = c
        df[c] = pd.to_numeric(df[c], errors="coerce")
        break

if time_col:
    kpis.append(("Total Downtime (hrs)", round(df[time_col].sum(), 2)))
    kpis.append(("MTTR – Avg Repair Time (hrs)", round(df[time_col].mean(), 2)))

# ======================================================
# MACHINE KPIs
# ======================================================
if has("machine no.") and time_col:
    top = (
        df.groupby("machine no.")[time_col]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

    for i, (m, t) in enumerate(top.items(), 1):
        kpis.append((f"Top {i} Machine Downtime", f"{m} ({round(t,2)} hrs)"))

# ======================================================
# SHIFT KPIs
# ======================================================
if has("shift"):
    for s, c in df["shift"].value_counts().items():
        kpis.append((f"Jobs – {s} Shift", c))

# ======================================================
# AREA KPIs
# ======================================================
if has("area"):
    for a, c in df["area"].value_counts().head(5).items():
        kpis.append((f"Jobs – {a}", c))

# ======================================================
# MAINTENANCE TYPE KPIs
# ======================================================
if has("type"):
    for t, c in df["type"].value_counts().items():
        kpis.append((f"Jobs Type – {t}", c))

# ======================================================
# KPI OUTPUT
# ======================================================
kpi_df = pd.DataFrame(kpis, columns=["KPI", "Value"])

st.subheader("✅ KPI Summary")
st.dataframe(kpi_df, use_container_width=True)
