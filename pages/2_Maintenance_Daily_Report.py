import pandas as pd
import numpy as np

# Load Excel file
file_path = "log sheet for copilot.xlsx"
df = pd.read_excel(file_path)

# Normalize column names
df.columns = [c.strip().lower() for c in df.columns]

kpi_results = []

def col_exists(name):
    return name.lower() in df.columns

# -------------------------------
# BASIC KPIs
# -------------------------------
kpi_results.append(("Total Jobs", len(df)))

# Job Type KPIs
if col_exists("job"):
    kpi_results.append(("Breakdown Jobs (B/D)", (df["job"].astype(str).str.upper() == "B/D").sum()))
    kpi_results.append(("Corrective Jobs", (df["job"].astype(str).str.upper() == "CORRECTIVE").sum()))

# -------------------------------
# TIME KPIs
# -------------------------------
time_col = None
for c in ["time consumed", "maintenance time", "time consumed (minute)"]:
    if col_exists(c):
        time_col = c
        break

if time_col:
    df[time_col] = pd.to_numeric(df[time_col], errors="coerce")
    total_hours = df[time_col].sum()
    avg_time = df[time_col].mean()
    kpi_results.append(("Total Maintenance Time (Hours)", round(total_hours, 2)))
    kpi_results.append(("Average Repair Time - MTTR (Hours)", round(avg_time, 2)))

# -------------------------------
# MACHINE KPIs
# -------------------------------
if col_exists("machine no.") and time_col:
    machine_downtime = (
        df.groupby("machine no.")[time_col]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

    for i, (machine, hours) in enumerate(machine_downtime.items(), start=1):
        kpi_results.append((f"Top {i} Machine by Downtime", f"{machine} ({round(hours,2)} hrs)"))

# -------------------------------
# SHIFT KPIs
# -------------------------------
if col_exists("shift"):
    shift_counts = df["shift"].value_counts()
    for shift, count in shift_counts.items():
        kpi_results.append((f"Jobs in {shift} Shift", count))

# -------------------------------
# AREA KPIs
# -------------------------------
if col_exists("area"):
    area_counts = df["area"].value_counts().head(5)
    for area, count in area_counts.items():
        kpi_results.append((f"Jobs in Area: {area}", count))

# -------------------------------
# JOB TYPE KPIs (Mech / Elect / etc.)
# -------------------------------
if col_exists("type"):
    type_counts = df["type"].value_counts()
    for t, count in type_counts.items():
        kpi_results.append((f"Jobs Type: {t}", count))

# -------------------------------
# CREATE KPI TABLE
# -------------------------------
kpi_df = pd.DataFrame(kpi_results, columns=["KPI", "Value"])

# Write KPIs back into the SAME sheet (right side)
with pd.ExcelWriter(file_path, engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
    df.to_excel(writer, index=False, sheet_name="Main Data")
    kpi_df.to_excel(writer, index=False, sheet_name="Main Data", startcol=len(df.columns) + 2)

print("✅ KPI generation completed successfully")
