import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Dairy Plant Equipment Manager", layout="wide")

st.title("🏭 Dairy Plant Master Equipment Manager")

MACHINE_FILE = "master_machine_list.csv"
PRINTER_FILE = "master_printer_list.csv"
LINE_FILE = "line_equipment_list.csv"


# ==========================================================
# LOAD MACHINE DATA
# ==========================================================

if "machines" not in st.session_state:

    if os.path.exists(MACHINE_FILE):
        st.session_state.machines = pd.read_csv(MACHINE_FILE)

    else:

        machine_data = [
            ["M1","FCS+ 6.2 CR 10","0393-0H09-W88U_ID109","TOR","127.0.0.1"],
            ["M2","FCS+ 6.2 CR 17","078Z-W9AZ_ID1180","TOR","127.0.0.1"],
            ["M3","FCS+ 6.2 CR 17","D784-W9AY_ID1034","TOR","127.0.0.1"],
            ["M4","FCS+ 6.2 CR 10","D197-W87T_ID1333","TOR","127.0.0.1"],
            ["M5","FCS+ 6.0 CR 8","0F18-W1ZD_ID57","TOR","127.0.0.1"],
            ["M6","FCS+ 6.0 CR 12","0MW2-W25L_ID613","MULTIFLOW AS","127.0.0.1"],
            ["M7","FCS+ 6.0 CR 12","0M2E_ID436","MULTIFLOW AS","127.0.0.1"],
            ["M8","FCS+ 6.0 CR 7","0F24-W12C_ID4","TOR","127.0.0.1"],
            ["M9","FCS+ 6.0 CR 1","0D27HD151","TOR","127.0.0.1"],
            ["M10","FCS+ 6.0 CR 12","0M01-W25K_ID612","MULTIFLOW AS","127.0.0.1"],
            ["M11","FCS+ 6.0 CR 12","0M01-W25K_ID612","MULTIFLOW AS","127.0.0.1"],
            ["M12","FCS+ 6.0 CR 12","0M2F-W25L_ID613","MULTIFLOW AS","127.0.0.1"],
            ["M13","FCS+ 6.0 CR 8","0F18-W1ZD_ID57","TOR","127.0.0.1"],
            ["M14","FCS+ 6.2 CR 17","0784-WSAY_ID1034","TOR","127.0.0.1"],
            ["M15","FCS+ 6.1 CR 10","0M93_ID1008","MULTIFLOW AS","127.0.0.1"],
            ["M16","FCS+ 6.1 CR 10","0M92_ID1008","MULTIFLOW AS","127.0.0.1"],
            ["M17","FCS+ 6.0 CR 15","0M6XID518","MULTIFLOW AS","127.0.0.1"],
            ["M18","New Machine","Not Assigned","-","-"]
        ]

        st.session_state.machines = pd.DataFrame(machine_data, columns=[
            "Machine No","Model Name","Machine ID","Manufacturer","IP Address"
        ])


# ==========================================================
# LOAD PRINTER DATA
# ==========================================================

if "printers" not in st.session_state:

    if os.path.exists(PRINTER_FILE):
        st.session_state.printers = pd.read_csv(PRINTER_FILE)

    else:

        printer_data = [
            ["M1","Citronix","ci5500","0723178D",1],
            ["M2","Citronix","ci5500","0723178D",1],
            ["M3","Citronix","ci5500","0723178D",1],
            ["M4","Citronix","ci5500","0723178D",1],
        ]

        st.session_state.printers = pd.DataFrame(printer_data, columns=[
            "Machine No","Printer Company","Printer Model","Serial Number","Quantity"
        ])


# ==========================================================
# LOAD LINE EQUIPMENT DATA
# ==========================================================

if "line_equipment" not in st.session_state:

    if os.path.exists(LINE_FILE):

        st.session_state.line_equipment = pd.read_csv(LINE_FILE)

    else:

        line_data = [

            ["M16","Packer","TCS310 PRASMATIC"],
            ["M17","Packer","TCS310 PRASMATIC"],
            ["M18","Packer","TCS310 PRASMATIC"],

            ["M13","Packer","AMBRA"],

            ["M16","Palletizer","EMMTI"],
            ["M17","Palletizer","EMMTI"],
            ["M18","Palletizer","EMMTI"],

            ["M13","Palletizer","TMG Automated"],

            ["M16","Stretch Wrapper","ATLANTA"],
            ["M17","Stretch Wrapper","ATLANTA"],
            ["M18","Stretch Wrapper","ATLANTA"],

            ["M16","Bottle Conveyor","SIPAC"],
            ["M17","Bottle Conveyor","SIPAC"],
            ["M18","Bottle Conveyor","SIPAC"],

            ["M13","Bottle Conveyor","MEMCO"],

            ["M16","Empty Bottle Feeder","Lanfranchi"],

            ["Plant","Ozonizer System","WS"]

        ]

        st.session_state.line_equipment = pd.DataFrame(line_data, columns=[
            "Machine No","Equipment Type","Equipment Name"
        ])


# ==========================================================
# MACHINE SELECTION
# ==========================================================

st.header("Select Machine")

machine_list = st.session_state.machines["Machine No"].tolist()

cols = st.columns(6)

for i,m in enumerate(machine_list):

    if cols[i%6].button(m):

        st.session_state.selected = m


# ==========================================================
# MACHINE DETAILS
# ==========================================================

if "selected" in st.session_state:

    selected = st.session_state.selected

    st.subheader(f"Machine Details : {selected}")

    machine_data = st.session_state.machines[
        st.session_state.machines["Machine No"]==selected
    ]

    edited_machine = st.data_editor(machine_data)

    if st.button("💾 Save Machine Changes"):

        st.session_state.machines.update(edited_machine)

        st.session_state.machines.to_csv(MACHINE_FILE,index=False)

        st.success("Machine Updated")


# ==========================================================
# PRINTER SECTION
# ==========================================================

    st.divider()

    st.subheader("Printers")

    printer_data = st.session_state.printers[
        st.session_state.printers["Machine No"]==selected
    ]

    edited_printers = st.data_editor(printer_data, num_rows="dynamic")

    col1,col2 = st.columns(2)

    with col1:

        if st.button("Save Printer Changes"):

            st.session_state.printers = st.session_state.printers[
                st.session_state.printers["Machine No"]!=selected
            ]

            st.session_state.printers = pd.concat(
                [st.session_state.printers,edited_printers],
                ignore_index=True
            )

            st.session_state.printers.to_csv(PRINTER_FILE,index=False)

            st.success("Printer Updated")

    with col2:

        if st.button("Add New Printer"):

            new_row = pd.DataFrame(
                [[selected,"","","",1]],
                columns=st.session_state.printers.columns
            )

            st.session_state.printers = pd.concat(
                [st.session_state.printers,new_row],
                ignore_index=True
            )

            st.session_state.printers.to_csv(PRINTER_FILE,index=False)

            st.rerun()


# ==========================================================
# LINE EQUIPMENT SECTION
# ==========================================================

    st.divider()

    st.subheader("Line Equipment")

    equip_data = st.session_state.line_equipment[
        st.session_state.line_equipment["Machine No"]==selected
    ]

    edited_equipment = st.data_editor(equip_data, num_rows="dynamic")

    col3,col4 = st.columns(2)

    with col3:

        if st.button("Save Equipment"):

            st.session_state.line_equipment = st.session_state.line_equipment[
                st.session_state.line_equipment["Machine No"]!=selected
            ]

            st.session_state.line_equipment = pd.concat(
                [st.session_state.line_equipment,edited_equipment],
                ignore_index=True
            )

            st.session_state.line_equipment.to_csv(LINE_FILE,index=False)

            st.success("Equipment Updated")

    with col4:

        if st.button("Add Equipment"):

            new_row = pd.DataFrame(
                [[selected,"",""]],
                columns=st.session_state.line_equipment.columns
            )

            st.session_state.line_equipment = pd.concat(
                [st.session_state.line_equipment,new_row],
                ignore_index=True
            )

            st.session_state.line_equipment.to_csv(LINE_FILE,index=False)

            st.rerun()


st.success("System Ready ✅")
