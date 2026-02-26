import streamlit as st
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt

st.set_page_config(page_title="Maintenance KPI Dashboard", layout="wide")
st.title("🛠 Maintenance KPI Dashboard")

# -----------------------------
# Upload
# -----------------------------
file = st.file_uploader("Upload Maintenance Log Sheet", type=["xlsx", "xlsm", "xls"])
if file is None:
    st.stop()

xls = pd.ExcelFile(file)
sheet = next((s for s in xls.sheet_names if s.strip().lower() in ["main data", "maindata", "main"]), xls.sheet_names[0])
df = pd.read_excel(file, sheet_name=sheet)

st.caption(f"✅ Loaded sheet: **{sheet}** | Rows: **{len(df):,}** | Cols: **{len(df.columns)}**")

# -----------------------------
# Column normalization (keep your original names but make matching easier)
# -----------------------------
df.columns = [str(c).strip() for c in df.columns]

# -----------------------------
# Keep only REAL rows (avoid template/blank rows)
# -----------------------------
required_any = ["Notification No.", "Machine No.", "Type", "Reported Problem"]
present = [c for c in required_any if c in df.columns]

if present:
    mask = False
    for c in present:
        mask = mask | df[c].notna()
    real = df[mask].copy()
else:
    real = df.copy()

st.sidebar.header("Filters")
st.sidebar.write(f"Real rows detected: **{len(real):,}** (from {len(df):,})")

# -----------------------------
# Parse Date + time columns
# -----------------------------
if "Date" in real.columns:
    real["Date"] = pd.to_datetime(real["Date"], errors="coerce")

# Time Consumed: in your file it is a timedelta (duration). Convert to hours properly.
def to_hours(series):
    # timedelta -> hours
    if pd.api.types.is_timedelta64_dtype(series):
        return series.dt.total_seconds() / 3600

    # object -> could be time, datetime, number, string
    import datetime as dt
    def conv(x):
        if pd.isna(x):
            return np.nan
        if isinstance(x, pd.Timedelta):
            return x.total_seconds() / 3600
        if isinstance(x, pd.Timestamp):
            return x.hour + x.minute/60 + x.second/3600
        if isinstance(x, dt.time):
            return x.hour + x.minute/60 + x.second/3600
        if isinstance(x, dt.datetime):
            return x.hour + x.minute/60 + x.second/3600
        if isinstance(x, (int, float, np.integer, np.floating)):
            # Excel fraction-of-day (0–1) -> hours
            if x <= 1.5:
                return x * 24
            return float(x)
        if isinstance(x, str):
            t = x.strip()
            m = re.match(r"^(\d{1,2}):(\d{1,2})(?::(\d{1,2}))?$", t)
            if m:
                hh = int(m.group(1)); mm = int(m.group(2)); ss = int(m.group(3) or 0)
                return hh + mm/60 + ss/3600
        return np.nan

    return series.apply(conv)

if "Time Consumed" in real.columns:
    real["time_h"] = to_hours(real["Time Consumed"])
else:
    real["time_h"] = np.nan

if "Waiting Time" in real.columns:
    real["wait_h"] = to_hours(real["Waiting Time"])
else:
    real["wait_h"] = np.nan

# Hour-of-day from Start else Requested Time
import datetime as dt
def get_hour(x):
    if pd.isna(x): return np.nan
    if isinstance(x, pd.Timestamp): return x.hour
    if isinstance(x, dt.time): return x.hour
    if isinstance(x, dt.datetime): return x.hour
    if isinstance(x, str):
        m = re.match(r"^(\d{1,2}):", x.strip())
        if m: return int(m.group(1))
    return np.nan

real["hour"] = np.nan
if "Start" in real.columns:
    real["hour"] = real["Start"].apply(get_hour)
if "Requested Time" in real.columns:
    real.loc[real["hour"].isna(), "hour"] = real.loc[real["hour"].isna(), "Requested Time"].apply(get_hour)

# -----------------------------
# Date filter (optional)
# -----------------------------
df_f = real.copy()
if "Date" in df_f.columns:
    dmin, dmax = df_f["Date"].min(), df_f["Date"].max()
    if pd.notna(dmin) and pd.notna(dmax):
        start_date, end_date = st.sidebar.date_input(
            "Date range",
            value=(dmin.date(), dmax.date()),
            min_value=dmin.date(),
            max_value=dmax.date()
        )
        df_f = df_f[(df_f["Date"].dt.date >= start_date) & (df_f["Date"].dt.date <= end_date)]

st.sidebar.caption(f"Filtered rows: **{len(df_f):,}**")

# -----------------------------
# KPIs
# -----------------------------
total_jobs = len(df_f)
unique_complaints = df_f["Notification No."].nunique(dropna=True) if "Notification No." in df_f.columns else np.nan
total_hours = df_f["time_h"].sum(skipna=True)
avg_hours = df_f["time_h"].mean(skipna=True)

st.subheader("✅ KPI Summary")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Jobs (real rows)", f"{total_jobs:,}")
c2.metric("Complaints (unique notifications)", f"{int(unique_complaints):,}" if pd.notna(unique_complaints) else "-")
c3.metric("Total Time Consumed (hours)", f"{total_hours:,.2f}")
c4.metric("Avg Time per Job (hours)", f"{avg_hours:,.2f}" if pd.notna(avg_hours) else "-")

st.divider()

# -----------------------------
# Chart 1: Top machines by downtime hours
# -----------------------------
st.subheader("🏭 Machine-wise Breakdown (Top 10 by hours)")
if "Machine No." in df_f.columns:
    top_m = df_f.groupby("Machine No.")["time_h"].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10,4))
    ax.bar(top_m.index.astype(str), top_m.values)
    ax.set_ylabel("Hours")
    ax.set_xlabel("Machine")
    ax.set_title("Top 10 Machines by Total Time Consumed (hours)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    st.pyplot(fig)
else:
    st.info("Machine No. column not found.")

# -----------------------------
# Chart 2: Technician hours (split + equal allocation)
# -----------------------------
st.subheader("👷 Technician Worked Hours (Top 10)")
if "Performed By" in df_f.columns:
    def split_names(s):
        parts = re.split(r"[/,&]|\band\b", str(s), flags=re.IGNORECASE)
        parts = [p.strip() for p in parts if p.strip() and p.strip().lower() != "nan"]
        return parts if parts else ["Unknown"]

    rows = []
    for who, h in zip(df_f["Performed By"].fillna("Unknown"), df_f["time_h"]):
        if pd.isna(h): 
            continue
        names = split_names(who)
        share = h / len(names)
        for n in names:
            rows.append((n, share))

    tech_df = pd.DataFrame(rows, columns=["Technician", "hours"])
    top_t = tech_df.groupby("Technician")["hours"].sum().sort_values(ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(10,4))
    ax.bar(top_t.index.astype(str), top_t.values)
    ax.set_ylabel("Hours (allocated)")
    ax.set_xlabel("Technician")
    ax.set_title("Top 10 Technicians by Allocated Worked Hours")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    st.pyplot(fig)
else:
    st.info("Performed By column not found.")

st.divider()

# -----------------------------
# Chart 3: Complaints trend by date
# -----------------------------
st.subheader("📩 Complaints Received Trend (Date-wise)")
if "Date" in df_f.columns:
    dated = df_f.dropna(subset=["Date"]).copy()
    dated["day"] = dated["Date"].dt.date
    if "Notification No." in dated.columns:
        comp = dated.dropna(subset=["Notification No."]).groupby("day")["Notification No."].nunique()
    else:
        comp = dated.groupby("day").size()

    fig, ax = plt.subplots(figsize=(10,4))
    ax.plot(comp.index, comp.values)
    ax.set_ylabel("Complaints (unique)")
    ax.set_xlabel("Date")
    ax.set_title("Complaints Received per Day")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    st.pyplot(fig)
else:
    st.info("Date column not found.")

# -----------------------------
# Chart 4: Hourly pattern 0–23
# -----------------------------
st.subheader("🕐 0–23 Hour Pattern (Total Time Consumed)")
hourly = df_f.dropna(subset=["hour"]).groupby("hour")["time_h"].sum().reindex(range(24), fill_value=0)

fig, ax = plt.subplots(figsize=(10,4))
ax.bar(hourly.index, hourly.values)
ax.set_xlabel("Hour (0–23)")
ax.set_ylabel("Hours")
ax.set_title("Total Time Consumed by Hour of Day")
ax.set_xticks(range(24))
plt.tight_layout()
st.pyplot(fig)

# -----------------------------
# Chart 5: Date × Hour Heatmap
# -----------------------------
st.subheader("🗓️ Date × Hour Heatmap (Time Consumed)")
heat = df_f.dropna(subset=["Date", "hour"]).copy()
heat["day"] = heat["Date"].dt.date

pivot = heat.pivot_table(index="day", columns="hour", values="time_h", aggfunc="sum").reindex(columns=range(24)).fillna(0)
pivot_recent = pivot.tail(30)  # last 30 days for readability

fig, ax = plt.subplots(figsize=(12,5))
im = ax.imshow(pivot_recent.values, aspect="auto", interpolation="nearest")
ax.set_title("Date × Hour Heatmap (last 30 days in filtered data)")
ax.set_xlabel("Hour of day")
ax.set_ylabel("Date")
ax.set_xticks(range(24))
ax.set_xticklabels(range(24))
ax.set_yticks(range(len(pivot_recent.index)))
ax.set_yticklabels([str(d) for d in pivot_recent.index])
fig.colorbar(im, ax=ax, label="Hours")
plt.tight_layout()
st.pyplot(fig)

st.divider()

# -----------------------------
# Chart 6: Top 10 breakdown reasons
# -----------------------------
st.subheader("🧾 Top 10 Breakdown Reasons")
if "Reported Problem" in df_f.columns:
    reason = df_f["Reported Problem"].fillna("").astype(str).str.strip()
    reason_clean = (reason.str.lower()
                    .str.replace(r"[^a-z0-9\s]", "", regex=True)
                    .str.replace(r"\s+", " ", regex=True)
                    .str.strip())
    reason_short = reason_clean.apply(lambda s: " ".join(s.split()[:6]) if s else "")

    fallback = df_f["Type"].fillna("unknown").astype(str).str.strip().str.lower() if "Type" in df_f.columns else "unknown"
    reason_final = reason_short.where(reason_short != "", fallback)
    df_f["reason"] = reason_final

    top_r = df_f.groupby("reason")["time_h"].sum().sort_values(ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(10,4))
    ax.barh(top_r.index[::-1], top_r.values[::-1])
    ax.set_xlabel("Hours")
    ax.set_title("Top 10 Reasons by Total Time Consumed")
    plt.tight_layout()
    st.pyplot(fig)
else:
    st.info("Reported Problem column not found.")

with st.expander("📄 View filtered data"):
    st.dataframe(df_f, use_container_width=True)
