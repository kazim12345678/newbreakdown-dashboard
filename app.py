import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="NADEC Maintenance KPIs", layout="wide")

st.markdown("""
<div style='background:#003366; padding:15px; text-align:center; color:white; 
            font-size:22px; border-radius:6px;'>
    <b>NADEC Real-Time Maintenance Breakdown Dashboard</b>
</div>
""", unsafe_allow_html=True)

st.write("")

# ---------------- Session data ----------------
if "bd" not in st.session_state:
    st.session_state.bd = pd.DataFrame(
        columns=["DateTime", "Machine", "Minutes", "Reason", "Technician", "Notes"]
    )

df = st.session_state.bd

# ---------------- Entry form ----------------
with st.expander("➕ Add Breakdown Event", expanded=False):
    c1, c2, c3 = st.columns(3)
    with c1:
        machine = st.selectbox("Machine", [f"M{i}" for i in range(1,19)])
        minutes = st.number_input("Downtime (minutes)", min_value=1)
    with c2:
        reason = st.selectbox("Reason", ["Mechanical", "Electrical", "Automation", "Other"])
        tech = st.text_input("Technician")
    with c3:
        notes = st.text_area("Notes / Root Cause / Action", height=80)
        if st.button("Save Breakdown"):
            new = pd.DataFrame(
                [[datetime.now(), machine, minutes, reason, tech, notes]],
                columns=df.columns
            )
            st.session_state.bd = pd.concat([df, new], ignore_index=True)
            st.success("Breakdown saved.")

df = st.session_state.bd

# ---------------- KPIs ----------------
st.subheader("📊 High-Level KPIs (Today)")

if len(df) == 0:
    st.info("No breakdowns recorded yet.")
else:
    total_minutes = df["Minutes"].sum()
    worst_machine = df.groupby("Machine")["Minutes"].sum().idxmax()
    common_reason = df["Reason"].value_counts().idxmax()

    k1, k2, k3 = st.columns(3)
    k1.metric("Total Breakdown Minutes", total_minutes)
    k2.metric("Worst Machine", worst_machine)
    k3.metric("Most Common Reason", common_reason)

# ---------------- Machine table ----------------
st.subheader("🧾 Machine Breakdown Summary")

if len(df) > 0:
    summary = df.groupby("Machine")["Minutes"].sum().reset_index()
    summary = summary.sort_values("Minutes", ascending=False)
    st.dataframe(summary, use_container_width=True)
else:
    st.info("No data to summarize yet.")

# ---------------- Timeline-style bars ----------------
st.subheader("📍 Breakdown Bars by Machine")

if len(df) > 0:
    machines = df["Machine"].unique()
    for m in machines:
        st.markdown(f"### {m}")
        row = df[df["Machine"] == m]

        bar_html = ""
        for _, r in row.iterrows():
            color = {
                "Mechanical": "red",
                "Electrical": "blue",
                "Automation": "green",
                "Other": "gray"
            }[r["Reason"]]
            width = min(int(r["Minutes"]) * 2, 300)

            bar_html += f"""
            <div style="
                display:inline-block;
                width:{width}px;
                height:18px;
                background:{color};
                border-radius:6px;
                margin-right:4px;
                cursor:pointer;"
                title="Reason: {r['Reason']} | {r['Minutes']} min | Tech: {r['Technician']} | {r['Notes']}">
            </div>
            """

        st.markdown(bar_html, unsafe_allow_html=True)

# ---------------- Export ----------------
st.subheader("📤 Export Data")

st.download_button(
    "Download CSV",
    df.to_csv(index=False),
    file_name="maintenance_breakdowns.csv",
    mime="text/csv"
)
