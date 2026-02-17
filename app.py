import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

st.set_page_config(page_title="NADEC Maintenance Dashboard", layout="wide")

# ---------------- GOOGLE SHEET CONNECTION ----------------
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
client = gspread.authorize(creds)

sheet = client.open("NADEC_Maintenance_DB").sheet1

# Load data
data = sheet.get_all_records()
df = pd.DataFrame(data)

# ---------------- HEADER ----------------
st.markdown("""
<div style='background:#003366; padding:15px; text-align:center; color:white; 
            font-size:22px; border-radius:6px;'>
    <b>NADEC Real-Time Maintenance Breakdown Dashboard</b>
</div>
""", unsafe_allow_html=True)

st.write("")

# ---------------- OPERATOR ENTRY FORM ----------------
with st.expander("➕ Add Breakdown Entry", expanded=False):
    c1, c2, c3 = st.columns(3)

    with c1:
        machine = st.selectbox("Machine", [f"M{i}" for i in range(1,19)])
        duration = st.number_input("Downtime (minutes)", min_value=1)

    with c2:
        reason = st.selectbox("Reason", ["Mechanical", "Electrical", "Automation", "Operator Error"])
        tech = st.text_input("Technician")

    with c3:
        notes = st.text_area("Notes", height=80)
        if st.button("Save Breakdown"):
            new_row = [str(datetime.now()), machine, duration, reason, tech, notes]
            sheet.append_row(new_row)
            st.success("Breakdown saved! Refresh page to update.")

# Reload after entry
data = sheet.get_all_records()
df = pd.DataFrame(data)

# ---------------- KPIs ----------------
st.subheader("📊 Maintenance KPIs")

if len(df) > 0:
    total_minutes = df["Duration"].sum()
    worst_machine = df.groupby("Machine")["Duration"].sum().idxmax()
    common_reason = df["Reason"].value_counts().idxmax()

    k1, k2, k3 = st.columns(3)
    k1.metric("Total Breakdown Minutes", total_minutes)
    k2.metric("Worst Machine", worst_machine)
    k3.metric("Most Common Reason", common_reason)
else:
    st.info("No breakdowns recorded yet.")

# ---------------- MACHINE TIMELINE ----------------
st.subheader("📍 Breakdown Timeline (CUTE Style)")

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
                "Operator Error": "yellow"
            }[r["Reason"]]

            width = min(int(r["Duration"]) * 2, 300)

            bar_html += f"""
            <div style="
                display:inline-block;
                width:{width}px;
                height:18px;
                background:{color};
                border-radius:6px;
                margin-right:4px;
                cursor:pointer;"
                title="Reason: {r['Reason']} | {r['Duration']} min | Tech: {r['Technician']} | {r['Notes']}">
            </div>
            """

        st.markdown(bar_html, unsafe_allow_html=True)

# ---------------- EXPORT ----------------
st.subheader("📤 Export Data")

st.download_button(
    "Download CSV",
    df.to_csv(index=False),
    file_name="maintenance_breakdowns.csv",
    mime="text/csv"
)
