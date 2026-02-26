import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Maintenance KPI Dashboard", layout="wide")
st.title("Maintenance KPI Dashboard")

# ---------- FILE UPLOAD ----------
uploaded_file = st.file_uploader("Upload Maintenance Excel File", type=["xlsx"])

if not uploaded_file:
    st.stop()

# ---------- LOAD CORRECT SHEET ----------
df = pd.read_excel(uploaded_file, sheet_name=0)
df.columns = df.columns.str.strip()

# ---------- SAFE TIME CONVERSION ----------
def excel_time_to_minutes(x):
    if pd.isna(x):
        return 0
    if isinstance(x, (int, float)):
        return x * 24 * 60   # Excel day fraction → minutes
    try:
        return pd.to_timedelta(x).total_seconds() / 60
    except:
        return 0

if "Time Consumed" in df.columns:
    df["Minutes"] = df["Time Consumed"].apply(excel_time_to_minutes)
else:
    df["Minutes"] = 0

# ---------- BASIC CLEAN ----------
df["Job"] = df.get("Job", "")
df["Shift"] = df.get("Shift", "")
df["Machine No."] = df.get("Machine No.", "")

# ---------- KPI CALCULATIONS ----------
total_jobs = len(df)
breakdown_jobs = (df["Job"] == "B/D").sum()
corrective_jobs = (df["Job"] == "Corrective").sum()
total_downtime = df["Minutes"].sum()
avg_mttr = df["Minutes"].mean()

# ---------- KPI DISPLAY ----------
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Jobs", total_jobs)
c2.metric("Breakdowns", breakdown_jobs)
c3.metric("Corrective", corrective_jobs)
c4.metric("Total Downtime (min)", int(total_downtime))
c5.metric("Avg MTTR (min)", round(avg_mttr, 1))

st.divider()

# ---------- MACHINE ANALYSIS ----------
st.subheader("Machine Analysis")

mach_jobs = df["Machine No."].value_counts().reset_index()
mach_jobs.columns = ["Machine", "Jobs"]

mach_time = df.groupby("Machine No.")["Minutes"].sum().reset_index()
mach_time.columns = ["Machine", "Downtime"]

fig1 = px.bar(mach_jobs, x="Machine", y="Jobs", title="Jobs per Machine")
fig2 = px.bar(mach_time, x="Machine", y="Downtime", title="Downtime per Machine")

st.plotly_chart(fig1, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)

# ---------- SHIFT ANALYSIS ----------
st.subheader("Shift Analysis")

shift_jobs = df["Shift"].value_counts().reset_index()
shift_jobs.columns = ["Shift", "Jobs"]

shift_time = df.groupby("Shift")["Minutes"].sum().reset_index()
shift_time.columns = ["Shift", "Downtime"]

fig3 = px.bar(shift_jobs, x="Shift", y="Jobs", title="Jobs per Shift")
fig4 = px.bar(shift_time, x="Shift", y="Downtime", title="Downtime per Shift")

st.plotly_chart(fig3, use_container_width=True)
st.plotly_chart(fig4, use_container_width=True)

# ---------- TECHNICIAN ANALYSIS ----------
if "Performed By" in df.columns:
    tech_df = df.copy()
    tech_df["Tech"] = tech_df["Performed By"].fillna("").str.split("/")
    tech_df = tech_df.explode("Tech")
    tech_df["Tech"] = tech_df["Tech"].str.strip()
    tech_df = tech_df[tech_df["Tech"] != ""]

    tech_time = tech_df.groupby("Tech")["Minutes"].sum().reset_index()

    fig5 = px.bar(
        tech_time,
        x="Tech",
        y="Minutes",
        title="Downtime per Technician"
    )
    st.plotly_chart(fig5, use_container_width=True)

# ---------- RAW DATA ----------
st.subheader("Raw Data")
st.dataframe(df, use_container_width=True)
