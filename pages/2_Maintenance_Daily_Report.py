import pandas as pd
import numpy as np

# ======================================================
# GET DATA (SAFE – NO FILE PATHS)
# ======================================================

# OPTION 1: Streamlit (most common)
if "data" in globals():
    df = data.copy()
elif "st" in globals() and "data" in st.session_state:
    df = st.session_state["data"].copy()

# OPTION 2: Python in Excel
elif "xl" in globals():
    df = xl("Main Data[#All]", headers=True)

else:
    raise RuntimeError("❌ No active data source found")

# ======================================================
# CLEAN COLUMN NAMES
# ======================================================
df.columns = df.columns.str.strip().str.lower()

def has(col):
    return col in df.columns

kpis = []

# ======================================================
# BASIC KPIs
# ======================================================
kpis.append(("Total Jobs", len(df)))

# ======================================================
# JOB TYPE KPIs
# ======================================================
if has("job"):
    job_col = df["job"].astype(str).str.upper()
    kpis.append(("Breakdown Jobs (B/D)", (job_col == "B/D").sum()))
    kpis.append(("Corrective Jobs", (job_col == "CORRECTIVE").sum()))

# ======================================================
# TIME / DOWNTIME KPIs
# ======================================================
time_col = None
for c in ["time consumed", "maintenance time", "time consumed (minute)"]:
    if has(c):
        time_col = c
        df[c] = pd.to_numeric(df[c], errors="coerce")
        break

if time_col:
    kpis.append(("Total Downtime (hrs)", round(df[time_col].sum(), 2)))
    kpis.append(("MTTR - Avg Repair Time (hrs)", round(df[time_col].mean(), 2)))

# ======================================================
# MACHINE KPIs
# ======================================================
if has("machine no.") and time_col:
    top_machines = (
        df.groupby("machine no.")[time_col]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

    for i, (m, t) in enumerate(top_machines.items(), 1):
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
# KPI OUTPUT TABLE
# ======================================================
kpi_df = pd.DataFrame(kpis, columns=["KPI", "Value"])

# ======================================================
# OUTPUT (SAFE FOR ALL ENVIRONMENTS)
# ======================================================
kpi_df
