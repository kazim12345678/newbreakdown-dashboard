# pages/01_Master_List_of_Equipment.py

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Master List of Equipment", layout="wide")
st.title("Master List of Equipment")

# ==========================================================
# INITIAL DATA (RUN ONLY FIRST TIME)
# ==========================================================

if "machine_df" not in st.session_state:
    machine_data = [
        ["M1","FCS+ 6.2 CR 10","0393-0H09-W88U_ID109"],
        ["M2","FCS+ 6.2 CR/17","078Z-W9AZ ID1180"],
        ["M3","FCS+ 6.2 CR 17","D784-W9AY-ID1034"],
        ["M4","FCS+ 6.2 CR 10","D197-W87T_ID1333"],
        ["M5","FCS+ 6.0 CR 8","0F18-W1ZD_ID57"],
        ["M6","FCS+ 6.0 CR 12","0MW2-W25L_ID613"],
        ["M7","FCS+ 6.0 CR 12","#ID436 - 0M2E"],
        ["M8","FCS+ 6.0 CR 7","0F24-W12C_ID4"],
        ["M9","FCS+ 6.0 CR 1","0D27HD151"],
        ["M10","FCS+ 6.0 CR 12","0M01-W25K-ID612"],
        ["M11","FCS+ 6.0 CR 12","0M01-W25K-ID612"],
        ["M12","FCS+ 6.0 CR 12","0M2F-W25L_ID613"],
        ["M13","FCS+ 6.0 CR 8","0F18-W1ZD_ID57"],
        ["M14","FCS+ 6.2 CR 17","0784-WSAY_ID1034"],
        ["M15","FCS+ 6.1 CR 10","0M93 - ID1008"],
        ["M16","FCS+ 6.1 CR 10","0M92 - ID1008"],
        ["M17","FCS+ 6.0 CR 15","0M6XID518"],
        ["M18","NEW MACHINE","Not Assigned"]
    ]

    st.session_state.machine_df = pd.DataFrame(
        machine_data,
        columns=["Machine No","Model Name","Machine ID"]
    )

if "printer_df" not in st.session_state:
    printer_data = [
        ["M1","Citronix","ci5500","0723178D",1],
        ["M2","Citronix","ci5500","0723178D",1],
        ["M3","Citronix","ci5500","0723178D",1],
        ["M4","Citronix","ci5500","0723178D",1],
        ["M5","Citronix","ci5500","0725006D",1],
    ]

    st.session_state.printer_df = pd.DataFrame(
        printer_data,
        columns=[
            "Machine No",
            "Printer Company",
            "Printer Model",
            "Serial Number",
            "Quantity"
        ]
    )

# ==========================================================
# MACHINE BUTTONS (M1–M18)
# ==========================================================

st.header("Select Machine")

cols = st.columns(6)
selected_machine = None

for i in range(18):
    machine_name = f"M{i+1}"
    if cols[i % 6].button(machine_name):
        st.session_state.selected_machine = machine_name

if "selected_machine" in st.session_state:
    selected_machine = st.session_state.selected_machine

# ==========================================================
# SHOW SELECTED MACHINE DETAILS
# ==========================================================

if selected_machine:

    st.subheader(f"Details for {selected_machine}")

    machine_info = st.session_state.machine_df[
        st.session_state.machine_df["Machine No"] == selected_machine
    ]

    if not machine_info.empty:
        st.write("### Machine Information")
        edited_machine = st.data_editor(
            machine_info,
            num_rows="dynamic",
            key="machine_editor"
        )

        if st.button("Save Machine Changes"):
            st.session_state.machine_df.update(edited_machine)
            st.success("Machine updated successfully")

        if st.button("Delete Machine"):
            st.session_state.machine_df = st.session_state.machine_df[
                st.session_state.machine_df["Machine No"] != selected_machine
            ]
            st.success("Machine deleted")
            st.session_state.selected_machine = None
            st.rerun()

    # ======================================================
    # CHILD EQUIPMENT (PRINTERS)
    # ======================================================

    st.write("### Related Equipment")

    related_equipment = st.session_state.printer_df[
        st.session_state.printer_df["Machine No"] == selected_machine
    ]

    edited_equipment = st.data_editor(
        related_equipment,
        num_rows="dynamic",
        key="equipment_editor"
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Save Equipment Changes"):
            # Remove old records
            st.session_state.printer_df = st.session_state.printer_df[
                st.session_state.printer_df["Machine No"] != selected_machine
            ]
            # Add updated
            st.session_state.printer_df = pd.concat(
                [st.session_state.printer_df, edited_equipment],
                ignore_index=True
            )
            st.success("Equipment saved successfully")

    with col2:
        if st.button("Add New Equipment Row"):
            new_row = pd.DataFrame(
                [[selected_machine,"","","",1]],
                columns=st.session_state.printer_df.columns
            )
            st.session_state.printer_df = pd.concat(
                [st.session_state.printer_df,new_row],
                ignore_index=True
            )
            st.success("New row added")
            st.rerun()

st.divider()

st.success("Interactive Master Equipment Manager Ready ✅")
