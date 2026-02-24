# pages/01_Master_List_of_Equipment.py

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Master List of Equipment", layout="wide")

st.title("Master List of Equipment")

# =====================================================
# SECTION 1 — MACHINE MASTER LIST (UPLOAD)
# =====================================================

st.header("Primary Filling Machines")

uploaded_file = st.file_uploader("Upload Machine CSV File", type=["csv"])

if uploaded_file is not None:

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

    # Remove duplicated header rows
    if "Machine No" in df.columns:
        df = df[df["Machine No"] != "Machine No"]

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

    available_columns = [col for col in expected_columns if col in df.columns]

    master_df = df[available_columns].copy()

    # Safe conversions
    if "In-Service Date" in master_df.columns:
        master_df["In-Service Date"] = pd.to_datetime(
            master_df["In-Service Date"], errors="coerce"
        )

    numeric_cols = [
        "Machine Switch-On Hours",
        "Machine Rotation Hours",
        "Filled Containers"
    ]

    for col in numeric_cols:
        if col in master_df.columns:
            master_df[col] = pd.to_numeric(master_df[col], errors="coerce")

    if (
        "Machine Switch-On Hours" in master_df.columns
        and "Machine Rotation Hours" in master_df.columns
    ):
        master_df["Utilization %"] = (
            master_df["Machine Rotation Hours"]
            / master_df["Machine Switch-On Hours"]
        ) * 100

    st.subheader("Machine Master List")
    st.dataframe(master_df, use_container_width=True)

    # Summary
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

else:
    st.info("Upload machine CSV to display master list.")


# =====================================================
# SECTION 2 — PRINTER MASTER LIST (STATIC CHILD ASSETS)
# =====================================================

st.header("Printer Equipment (Child Assets)")

printer_data = [
    ["M1", "Inkjet Printer", "Citronix", "ci5500", "0723178D", 1],
    ["M2", "Inkjet Printer", "Citronix", "ci5500", "0723178D", 1],
    ["M3", "Inkjet Printer", "Citronix", "ci5500", "0723178D", 1],
    ["M4", "Inkjet Printer", "Citronix", "ci5500", "0723178D", 1],
    ["Unassigned", "Inkjet Printer", "Citronix", "ci5500", "0725037J", 1],
    ["Unassigned", "Inkjet Printer", "Citronix", "ci5500", "0725006D", 1],
    ["Unassigned", "Inkjet Printer", "Citronix", "ci5500", "0724332B", 1],
    ["Unassigned", "Inkjet Printer", "Citronix", "ci5500", "Serial Hidden", 1],
    ["Unassigned", "Inkjet Printer", "Citronix", "ci3500", "05230C", 1],
    ["Unassigned", "Inkjet Printer", "Citronix", "CI3500 (BI)", "0516230B", 1],
]

printer_df = pd.DataFrame(
    printer_data,
    columns=[
        "Parent Machine",
        "Equipment Type",
        "Company",
        "Model",
        "Serial Number",
        "Quantity"
    ]
)

st.subheader("Printer Master List")
st.dataframe(printer_df, use_container_width=True)


# =====================================================
# DOWNLOAD COMBINED MASTER LIST
# =====================================================

st.header("Download Complete Master List")

if uploaded_file is not None:
    combined_df = pd.concat(
        [master_df.assign(Asset_Type="Primary Machine"),
         printer_df.assign(Asset_Type="Child Equipment")],
        ignore_index=True,
        sort=False
    )

    csv_download = combined_df.to_csv(index=False)

    st.download_button(
        label="Download Complete Master Equipment List",
        data=csv_download,
        file_name="Complete_Master_List.csv",
        mime="text/csv"
    )

st.success("Master Equipment Page Loaded Successfully")
