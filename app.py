import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="SERAC Executive Dashboard V2", layout="wide")

# --------- DARK THEME STYLE ----------
st.markdown("""
<style>
body {background-color: #0e1117;}
h1, h2, h3 {color: white;}
</style>
""", unsafe_allow_html=True)

st.title("🏭 SERAC DRINKABLE SECTION")
st.subheader("Technical Downtime Executive Dashboard - Version 2")

# -----------------------------
# RAW DATA
# -----------------------------
data = [
# (DATA SHORTENED HERE FOR READABILITY — KEEP YOUR FULL DATA FROM PREVIOUS VERSION)
]

# IMPORTANT:
# Paste the FULL data list from Version 1 here (same as before)

df = pd.DataFrame(data, columns=["Machine","Downtime Type","Minutes"])

# -----------------------------
# SIDEBAR FILTER
# -----------------------------
st.sidebar.header("🔍 Filter Options")

machine_filter = st.sidebar.multiselect(
    "Select Machine(s)",
    options=sorted(df["Machine"].unique()),
    default=sorted(df["Machine"].unique())
)

df_filtered = df[df["Machine"].isin(machine_filter)]

# -----------------------------
# KPI SECTION
# -----------------------------
total_dt = df_filtered["Minutes"].sum()
avg_dt = round(df_filtered.groupby("Machine")["Minutes"].sum().mean(),1)
top_machine = df_filtered.groupby("Machine")["Minutes"].sum().idxmax()

col1,col2,col3 = st.columns(3)

col1.metric("Total Downtime (Min)", total_dt)
col2.metric("Avg Downtime / Machine", avg_dt)
col3.metric("Worst Machine", top_machine)

st.markdown("---")

# -----------------------------
# MACHINE RANKING
# -----------------------------
st.subheader("🔴 Machine Downtime Ranking")

machine_sum = df_filtered.groupby("Machine")["Minutes"].sum().sort_values(ascending=False)

fig1 = px.bar(
    x=machine_sum.index,
    y=machine_sum.values,
    color=machine_sum.values,
    color_continuous_scale="Reds",
    labels={'x':'Machine','y':'Minutes'}
)

st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# PARETO ANALYSIS (80/20)
# -----------------------------
st.subheader("📊 Pareto Analysis - Top Downtime Causes")

cause_sum = df_filtered.groupby("Downtime Type")["Minutes"].sum().sort_values(ascending=False)

pareto_df = cause_sum.reset_index()
pareto_df["Cumulative %"] = pareto_df["Minutes"].cumsum() / pareto_df["Minutes"].sum() * 100

fig2 = go.Figure()

fig2.add_trace(go.Bar(
    x=pareto_df["Downtime Type"],
    y=pareto_df["Minutes"],
    name="Downtime Minutes"
))

fig2.add_trace(go.Scatter(
    x=pareto_df["Downtime Type"],
    y=pareto_df["Cumulative %"],
    name="Cumulative %",
    yaxis="y2"
))

fig2.update_layout(
    yaxis2=dict(
        overlaying='y',
        side='right',
        title='Cumulative %'
    )
)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# TOP 5 CRITICAL MACHINES
# -----------------------------
st.subheader("⚠ Top 5 Critical Machines")

top5 = machine_sum.head(5)
st.table(top5)

# -----------------------------
# TOP 10 CRITICAL CAUSES
# -----------------------------
st.subheader("🚨 Top 10 Downtime Causes")

top10 = cause_sum.head(10)
st.table(top10)

# -----------------------------
# OEM ACTION SECTION
# -----------------------------
st.subheader("📌 Recommended OEM Focus Areas")

critical_causes = cause_sum.head(3).index.tolist()

for cause in critical_causes:
    st.write(f"• Immediate root cause analysis required for: **{cause}**")

# -----------------------------
# DOWNLOAD BUTTON
# -----------------------------
st.download_button(
    label="⬇ Download Filtered Data as CSV",
    data=df_filtered.to_csv(index=False),
    file_name="serac_filtered_downtime.csv",
    mime="text/csv"
)
