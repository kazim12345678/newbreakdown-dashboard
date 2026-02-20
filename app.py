import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="SERAC Executive Dashboard", layout="wide")

st.title("🏭 SERAC DRINKABLE SECTION")
st.subheader("Technical Downtime Executive Dashboard")

# -----------------------------
# SAMPLE DATA (Replace with your full data list)
# -----------------------------
data = [
    ("M1", "Electrical", 120),
    ("M2", "Mechanical", 90),
    ("M3", "Sensor Fault", 150),
    ("M1", "Mechanical", 60),
    ("M4", "Electrical", 200),
]

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

# Prevent empty selection crash
if len(machine_filter) == 0:
    st.warning("Please select at least one machine.")
    st.stop()

df_filtered = df[df["Machine"].isin(machine_filter)]

# -----------------------------
# KPI SECTION (SAFE)
# -----------------------------
if df_filtered.empty:
    total_dt = 0
    avg_dt = 0
    top_machine = "No Data"
else:
    total_dt = df_filtered["Minutes"].sum()
    avg_dt = round(df_filtered.groupby("Machine")["Minutes"].sum().mean(), 1)
    machine_totals = df_filtered.groupby("Machine")["Minutes"].sum()
    top_machine = machine_totals.idxmax() if not machine_totals.empty else "No Data"

col1, col2, col3 = st.columns(3)

col1.metric("Total Downtime (Min)", total_dt)
col2.metric("Avg Downtime / Machine", avg_dt)
col3.metric("Worst Machine", top_machine)

st.markdown("---")

# -----------------------------
# MACHINE RANKING
# -----------------------------
st.subheader("🔴 Machine Downtime Ranking")

machine_sum = df_filtered.groupby("Machine")["Minutes"].sum().sort_values(ascending=False)

if not machine_sum.empty:
    fig1 = px.bar(
        x=machine_sum.index,
        y=machine_sum.values,
        color=machine_sum.values,
        color_continuous_scale="Reds",
        labels={'x':'Machine','y':'Minutes'}
    )
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.info("No data available for selected machines.")

# -----------------------------
# PARETO ANALYSIS
# -----------------------------
st.subheader("📊 Pareto Analysis")

cause_sum = df_filtered.groupby("Downtime Type")["Minutes"].sum().sort_values(ascending=False)

if not cause_sum.empty:
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
else:
    st.info("No downtime causes available.")

# -----------------------------
# DOWNLOAD BUTTON
# -----------------------------
st.download_button(
    label="⬇ Download Filtered Data as CSV",
    data=df_filtered.to_csv(index=False),
    file_name="serac_filtered_downtime.csv",
    mime="text/csv"
)
