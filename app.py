import streamlit as st
import pandas as pd
import plotly.express as px
import os

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="NADEC Breakdown Dashboard 2025",
    layout="wide"
)

st.title("🏭 NADEC Breakdown Maintenance Dashboard 2025")
st.markdown("Real-time KPI Monitoring | Machine Downtime | Technician Contribution")

# -----------------------------
# MACHINE LIST (18 Machines)
# -----------------------------
machines = [
    "M1","M2","M3","M4","M5","M6","M7","M8","M9",
    "M10","M11","M12","M13","M14","M15","M16","M17","M18"
]

# -----------------------------
# FILE STORAGE
# -----------------------------
DATA_FILE = "breakdown_data.csv"

# -----------------------------
# CREATE FILE IF NOT EXISTS
# -----------------------------
if not os.path.exists(DATA_FILE):
    df_init = pd.DataFrame(columns=[
        "Date", "Machine", "Downtime Hours", "Reason", "Technician"
    ])
    df_init.to_csv(DATA_FILE, index=False)

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv(DATA_FILE)

# -----------------------------
# SIDEBAR MENU
# -----------------------------
st.sidebar.header("⚙ Dashboard Controls")

menu = st.sidebar.radio(
    "Select View",
    ["📊 Dashboard Overview", "➕ Add Breakdown Entry", "📂 Upload CSV Data", "📝 Edit/Delete Records"]
)

# ======================================================
# 1. DASHBOARD OVERVIEW
# ======================================================
if menu == "📊 Dashboard Overview":

    st.subheader("📌 KPI Summary")

    # Convert downtime column safely
    if not df.empty:
        df["Downtime Hours"] = pd.to_numeric(df["Downtime Hours"], errors="coerce")

    total_downtime = df["Downtime Hours"].sum() if not df.empty else 0
    total_events = len(df)

    worst_machine = df.groupby("Machine")["Downtime Hours"].sum().idxmax() if total_events > 0 else "N/A"
    worst_month = pd.to_datetime(df["Date"]).dt.month_name().mode()[0] if total_events > 0 else "N/A"

    # KPI Cards Layout
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("⏱ Total Downtime Hours", f"{total_downtime:.1f} hrs")
    col2.metric("🚨 Total Breakdown Events", total_events)
    col3.metric("⚙ Worst Machine", worst_machine)
    col4.metric("📅 Most Frequent Month", worst_month)

    st.divider()

    # -----------------------------
    # FILTERS
    # -----------------------------
    st.subheader("🔍 Filters")

    fcol1, fcol2 = st.columns(2)

    selected_machine = fcol1.selectbox("Select Machine", ["All"] + machines)

    if not df.empty:
        df["Month"] = pd.to_datetime(df["Date"]).dt.month_name()

    selected_month = fcol2.selectbox(
        "Select Month",
        ["All"] + (df["Month"].unique().tolist() if not df.empty else [])
    )

    filtered_df = df.copy()

    if selected_machine != "All":
        filtered_df = filtered_df[filtered_df["Machine"] == selected_machine]

    if selected_month != "All":
        filtered_df = filtered_df[filtered_df["Month"] == selected_month]

    # -----------------------------
    # CHARTS
    # -----------------------------
    st.subheader("📊 Breakdown Analytics")

    c1, c2 = st.columns(2)

    # Chart 1: Machine Downtime
    if not filtered_df.empty:
        machine_summary = filtered_df.groupby("Machine")["Downtime Hours"].sum().reset_index()
        fig1 = px.bar(
            machine_summary,
            x="Machine",
            y="Downtime Hours",
            title="Machine-wise Downtime Hours"
        )
        c1.plotly_chart(fig1, use_container_width=True)

    # Chart 2: Reason Pie
    if not filtered_df.empty:
        reason_summary = filtered_df["Reason"].value_counts().reset_index()
        reason_summary.columns = ["Reason", "Count"]

        fig2 = px.pie(
            reason_summary,
            names="Reason",
            values="Count",
            title="Breakdown Reason Contribution"
        )
        c2.plotly_chart(fig2, use_container_width=True)

    # -----------------------------
    # DATA TABLE
    # -----------------------------
    st.subheader("📋 Breakdown Records Table")
    st.dataframe(filtered_df, use_container_width=True)

    # Download Button
    st.download_button(
        "⬇ Download Filtered Data as CSV",
        filtered_df.to_csv(index=False),
        file_name="filtered_breakdown_data.csv"
    )

# ======================================================
# 2. ADD BREAKDOWN ENTRY
# ======================================================
elif menu == "➕ Add Breakdown Entry":

    st.subheader("➕ Add New Breakdown Record")

    with st.form("entry_form"):
        date = st.date_input("Breakdown Date")
        machine = st.selectbox("Machine", machines)
        downtime = st.number_input("Downtime Hours", min_value=0.0, step=0.5)
        reason = st.selectbox("Reason", ["Mechanical", "Electrical", "Automation", "Utility", "Other"])
        technician = st.text_input("Technician Name")

        submitted = st.form_submit_button("✅ Save Entry")

        if submitted:
            new_row = {
                "Date": date,
                "Machine": machine,
                "Downtime Hours": downtime,
                "Reason": reason,
                "Technician": technician
            }

            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)

            st.success("Breakdown Entry Saved Successfully!")

# ======================================================
# 3. UPLOAD CSV
# ======================================================
elif menu == "📂 Upload CSV Data":

    st.subheader("📂 Upload Breakdown CSV File")

    uploaded = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded:
        uploaded_df = pd.read_csv(uploaded)
        st.dataframe(uploaded_df)

        if st.button("✅ Replace Existing Data"):
            uploaded_df.to_csv(DATA_FILE, index=False)
            st.success("Data Updated Successfully! Restart dashboard.")

# ======================================================
# 4. EDIT / DELETE RECORDS
# ======================================================
elif menu == "📝 Edit/Delete Records":

    st.subheader("📝 Edit or Delete Breakdown Records")

    if df.empty:
        st.warning("No records available yet.")
    else:
        st.dataframe(df)

        row_to_delete = st.number_input(
            "Enter Row Number to Delete",
            min_value=0,
            max_value=len(df)-1,
            step=1
        )

        if st.button("🗑 Delete Selected Row"):
            df = df.drop(index=row_to_delete).reset_index(drop=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("Row Deleted Successfully!")
