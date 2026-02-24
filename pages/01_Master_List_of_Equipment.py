# pages/01_Master_List_of_Equipment.py

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Master List of Equipment", layout="wide")

st.title("Master List of Equipment")

st.markdown("Upload your Machine / Equipment CSV file to generate Master Equipment List")

uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is None:
    st.info("Please upload a CSV file to continue.")
    st.stop()

# =========================
# READ FILE SAFELY
# =========================

try:
    df = pd.read_csv(uploaded_file)
except:
    st.error("Error reading file. Please upload valid CSV.")
    st.stop()

# Clean column names
df.columns = (
    df.columns
    .astype(str)
    .str.strip()
    .str.replace("\n", "")
)

# Remove duplicated header rows if exist
df = df[df["Machine No"] != "Machine No"] if "Machine No" in df.columns else df

# =========================
# STANDARD MASTER LIST FORMAT
# =========================

expected_columns = [
    "Machine No",
    "Model Name",
    "Machine ID",
    "Model Code",
    "Filling Type",
    "IP Address",
    "In-Service Date",
    "Machine Switch-On Hours",
    "Machine Rotation Hours",
    "Filled Containers"
]

# Keep only available columns safely
available_columns = [col for col in expected_columns if col in df.columns]

master_df = df[available_columns].copy()

# Convert date safely
if "In-Service Date" in master_df.columns:
    master_df["In-Service Date"] = pd.to_datetime(
        master_df["In-Service Date"],
        errors="coerce"
    )

# Convert numeric columns safely
numeric_cols = [
    "Machine Switch-On Hours",
    "Machine Rotation Hours",
    "Filled Containers"
]

for col in numeric_cols:
    if col in master_df.columns:
        master_df[col] = pd.to_numeric(master_df[col], errors="coerce")

# =========================
# ADD CALCULATED FIELDS
# =========================

if "Machine Switch-On Hours" in master_df.columns and \
   "Machine Rotation Hours" in master_df.columns:

    master_df["Utilization %"] = (
        master_df["Machine Rotation Hours"] /
        master_df["Machine Switch-On Hours"]
    ) * 100

# =========================
# DISPLAY SECTION
# =========================

st.subheader("Equipment Master List")

st.dataframe(master_df, use_container_width=True)

st.subheader("Summary Statistics")

col1, col2, col3 = st.columns(3)

if "Machine No" in master_df.columns:
    col1.metric("Total Machines", master_df["Machine No"].nunique())

if "Machine Switch-On Hours" in master_df.columns:
    col2.metric(
        "Total Switch-On Hours",
        int(master_df["Machine Switch-On Hours"].sum())
    )

if "Filled Containers" in master_df.columns:
    col3.metric(
        "Total Filled Containers",
        int(master_df["Filled Containers"].sum())
    )

# =========================
# DOWNLOAD OPTION
# =========================

csv_download = master_df.to_csv(index=False)

st.download_button(
    label="Download Clean Master List",
    data=csv_download,
    file_name="Master_List_of_Equipment.csv",
    mime="text/csv"
)

st.success("Master Equipment List Generated Successfully")
