import streamlit as st
import pandas as pd

st.set_page_config(page_title="Master List of Equipment", layout="wide")
st.title("Master Equipment Manager")

# ==========================================================
# INITIALIZE SESSION STATE
# ==========================================================

if "machines" not in st.session_state:

    machine_data = [
        ["M1","FCS+ 6.2 CR 10","0393-0H09-W88U_ID109","1095 - R18/1080 V9 Mec GD 10kg PW20","TOR","127.0.0.1","2018-05-29",133214,67494,174085910],
        ["M2","FCS+ 6.2 CR/17","078Z-W9AZ ID1180","1180 - R18/1080 V9 Mec GD 3.3kg PW-10","TOR","127.0.0.1","2019-02-05",12172,7446,13930490],
        ["M3","FCS+ 6.2 CR 17","D784-W9AY-ID1034","1034 - R8/720 V4 Mec GD 3kg PW10","TOR","127.0.0.1","2019-02-04",126016,57500,189700750],
        ["M4","FCS+ 6.2 CR 10","D197-W87T_ID1333","1333 - R8/720 V4 Mec GD 4kg(3kg) PW10","TOOR","127.0.0.1","2018-05-29",36586,18842,58650901],
        ["M5","FCS+ 6.0 CR 8","0F18-W1ZD_ID57","057 - R18/1080 V9 Mec GD 3kg","TOR","127.0.0.1","2015-03-12",76735,36384,95461227],
        ["M6","FCS+ 6.0 CR 12","0MW2-W25L_ID613","613 - R3G/1620 V16 Mtec GD 3kg PWM10 MFAS","MULTIFLOW AS","127.0.0.1","2015-07-29",76728,37440,619740035],
        ["M7","FCS+ 6.0 CR 12","#ID436 - 0M2E","608 - R45/2700 V12 Mec GD 3kg PW10 MFAS","MULTIFLOW AS","127.0.0.1","2015-07-27",110257,57766,413015663],
        ["M8","FCS+ 6.0 CR 7","0F24-W12C_ID4","004 - R16/720 V8 Mec GD 3kg","TOR","127.0.0.1","2015-02-25",52501,28007,168139993],
        ["M9","FCS+ 6.0 CR 1","0D27HD151","151 - R16/720 V8 Mec GD 3kg PW10","TOR","127.0.0.1","2014-02-27",125648,65566,394937594],
        ["M10","FCS+ 6.0 CR 12","0M01-W25K-ID612","630 - R36/1620 V16 UCB DG 3kg PW10 MFAS","MULTIFLOW AS","127.0.0.1","2015-07-29",182730,18385,241007795],
        ["M11","FCS+ 6.0 CR 12","0M01-W25K-ID612","630 - R25/1602 V16 UCB DG 3kg PW10 MFAS","MULTIFLOW AS","127.0.0.1","2015-07-29",182652,18351,240644255],
        ["M12","FCS+ 6.0 CR 12","0M2F-W25L_ID613","613 - R36/1620 V16 Mec GD 3kg PW10 MFAS","MULTIFLOW AS","127.0.0.1","2015-07-29",76653,37421,615495135],
        ["M13","FCS+ 6.0 CR 8","0F18-W1ZD_ID57","057 - R18/1080 V9 Mec GD 3kg","TOR","127.0.0.1","2015-03-12",76641,36343,95368919],
        ["M14","FCS+ 6.2 CR 17","0784-WSAY_ID1034","1034 - R8/720 V4 Mec GD 3kg PW10","TOR","127.0.0.1","2019-02-04",125922,57452,18956152],
        ["M15","FCS+ 6.1 CR 10","0M93 - ID1008","1008 - R30/1080 V15 Mec GD 3kg(2kg) PW27 MFAS H2F","MULTIFLOW AS","127.0.0.1","2015-10-20",2390,783,12870533],
        ["M16","FCS+ 6.1 CR 10","0M92 - ID1008","1008 - R30/1080 V15 Mec GD 3kg(2kg) PW27 MFAS H2F","MULTIFLOW AS","127.0.0.1","2015-10-20",3899,1208,16516564],
        ["M17","FCS+ 6.0 CR 15","0M6XID518","518 - R30/1080 V15 Mec GD 3kg(2kg) PW27 MFAS","MULTIFLOW AS","127.0.0.1","2014-07-04",243380,205482,47208836],
        ["M18","New Machine","Not Assigned","-","-","-","2024-01-01",0,0,0],
    ]

    st.session_state.machines = pd.DataFrame(machine_data, columns=[
        "Machine No","Model Name","Machine ID","Model Code",
        "Filling Type","IP Address","In-Service Date",
        "Machine Switch-On Hours","Machine Rotation Hours","Filled Containers"
    ])

if "printers" not in st.session_state:

    printer_data = [
        ["M1","Citronix","ci5500","0723178D",1],
        ["M2","Citronix","ci5500","0723178D",1],
        ["M3","Citronix","ci5500","0723178D",1],
        ["M4","Citronix","ci5500","0723178D",1],
        ["Not Assigned","Citronix","ci5500","0725037J",1],
        ["Not Assigned","Citronix","ci5500","0725006D",1],
        ["Not Assigned","Citronix","ci5500","0724332B",1],
        ["Not Assigned","Citronix","ci5500","Serial Hidden",1],
        ["Not Assigned","Citronix","ci3500","05230C",1],
        ["Not Assigned","Citronix","CI3500 (BI)","0516230B",1],
    ]

    st.session_state.printers = pd.DataFrame(printer_data, columns=[
        "Machine No","Printer Company","Printer Model","Serial Number","Quantity"
    ])

# ==========================================================
# MACHINE BUTTONS
# ==========================================================

st.header("Select Machine")

cols = st.columns(6)
for i in range(18):
    m = f"M{i+1}"
    if cols[i % 6].button(m):
        st.session_state.selected = m

# ==========================================================
# SHOW MACHINE DETAILS
# ==========================================================

if "selected" in st.session_state:

    selected_machine = st.session_state.selected
    st.subheader(f"Machine Details: {selected_machine}")

    machine_data = st.session_state.machines[
        st.session_state.machines["Machine No"] == selected_machine
    ]

    edited_machine = st.data_editor(machine_data, num_rows="dynamic")

    if st.button("Save Machine Changes"):
        st.session_state.machines.update(edited_machine)
        st.success("Machine updated")

    if st.button("Delete Machine"):
        st.session_state.machines = st.session_state.machines[
            st.session_state.machines["Machine No"] != selected_machine
        ]
        st.success("Machine deleted")
        st.rerun()

    st.divider()

    # ======================================================
    # PRINTERS
    # ======================================================

    st.subheader("Related Printers")

    printer_data = st.session_state.printers[
        st.session_state.printers["Machine No"] == selected_machine
    ]

    edited_printers = st.data_editor(printer_data, num_rows="dynamic")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Save Printer Changes"):
            st.session_state.printers = st.session_state.printers[
                st.session_state.printers["Machine No"] != selected_machine
            ]
            st.session_state.printers = pd.concat(
                [st.session_state.printers, edited_printers],
                ignore_index=True
            )
            st.success("Printers updated")

    with col2:
        if st.button("Add New Printer"):
            new_row = pd.DataFrame(
                [[selected_machine,"","","",1]],
                columns=st.session_state.printers.columns
            )
            st.session_state.printers = pd.concat(
                [st.session_state.printers,new_row],
                ignore_index=True
            )
            st.rerun()

st.success("Master Equipment Management System Ready ✅")
