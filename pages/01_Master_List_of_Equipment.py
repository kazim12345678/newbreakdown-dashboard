# pages/01_Master_List_of_Equipment.py

import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Master List of Equipment", layout="wide")

st.title("Master List of Equipment")

# =========================================================
# FILE PATHS (Permanent Storage)
# =========================================================

PRINTER_FILE = "master_printer_list.csv"
MACHINE_FILE = "master_machine_list.csv"

# =========================================================
# LOAD EXISTING DATA IF AVAILABLE
# =========================================================

if os.path.exists(PRINTER_FILE):
    printer_df = pd.read_csv(PRINTER_FILE)
else:
    printer_df = pd.DataFrame(columns=[
        "Machine No",
        "Printer Company",
        "Printer Model",
        "Serial Number",
        "Quantity"
    ])

if os.path.exists(MACHINE_FILE):
    machine_df = pd.read_csv(MACHINE_FILE)
else:
    machine_df = pd.DataFrame(columns=[
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
    ])

# =========================================================
# PRINTER MASTER SECTION
# =========================================================

st.header("Printer Master List")

with st.form("printer_form"):
    col1, col2, col3, col4, col5 = st.columns(5)

    machine_no = col1.text_input("Machine No")
    company = col2.text_input("Printer Company")
    model = col3.text_input("Printer Model")
    serial = col4.text_input("Serial Number")
    quantity = col5.number_input("Quantity", min_value=1, step=1)

    printer_submit = st.form_submit_button("Add Printer")

    if printer_submit:
        new_row = pd.DataFrame([{
            "Machine No": machine_no,
            "Printer Company": company,
            "Printer Model": model,
            "Serial Number": serial,
            "Quantity": quantity
        }])

        printer_df = pd.concat([printer_df, new_row], ignore_index=True)
        st.success("Printer Added Successfully")

# Save Button for Printer
if st.button("Save Printer List Permanently"):
    printer_df.to_csv(PRINTER_FILE, index=False)
    st.success("Printer Master List Saved Permanently")

st.dataframe(printer_df, use_container_width=True)

st.download_button(
    "Download Printer Master List",
    printer_df.to_csv(index=False),
    "Printer_Master_List.csv",
    "text/csv"
)

st.divider()

# =========================================================
# MACHINE MASTER SECTION
# =========================================================

st.header("Machine Master List")

with st.form("machine_form"):

    col1, col2, col3 = st.columns(3)
    m_no = col1.text_input("Machine No")
    model_name = col2.text_input("Model Name")
    machine_id = col3.text_input("Machine ID")

    col4, col5, col6 = st.columns(3)
    model_code = col4.text_input("Model Code")
    filling_type = col5.text_input("Filling Type")
    ip_address = col6.text_input("IP Address")

    col7, col8, col9 = st.columns(3)
    in_service = col7.date_input("In-Service Date")
    switch_on = col8.number_input("Machine Switch-On Hours", min_value=0)
    rotation = col9.number_input("Machine Rotation Hours", min_value=0)

    filled_containers = st.number_input("Filled Containers", min_value=0)

    machine_submit = st.form_submit_button("Add Machine")

    if machine_submit:
        new_machine = pd.DataFrame([{
            "Machine No": m_no,
            "Model Name": model_name,
            "Machine ID": machine_id,
            "Model Code": model_code,
            "Filling Type": filling_type,
            "IP Address": ip_address,
            "In-Service Date": in_service,
            "Machine Switch-On Hours": switch_on,
            "Machine Rotation Hours": rotation,
            "Filled Containers": filled_containers
        }])

        machine_df = pd.concat([machine_df, new_machine], ignore_index=True)
        st.success("Machine Added Successfully")

# Save Button for Machine
if st.button("Save Machine List Permanently"):
    machine_df.to_csv(MACHINE_FILE, index=False)
    st.success("Machine Master List Saved Permanently")

st.dataframe(machine_df, use_container_width=True)

st.download_button(
    "Download Machine Master List",
    machine_df.to_csv(index=False),
    "Machine_Master_List.csv",
    "text/csv"
)

st.divider()

# =========================================================
# SUMMARY SECTION
# =========================================================

st.header("Summary")

colA, colB, colC = st.columns(3)

colA.metric("Total Printers", len(printer_df))
colB.metric("Total Machines", len(machine_df))

if "Filled Containers" in machine_df.columns:
    colC.metric(
        "Total Filled Containers",
        int(machine_df["Filled Containers"].sum())
    )

st.success("Master Equipment Page Ready and Fully Functional")
