import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Master Equipment Manager", layout="wide")

st.title("🏭 Dairy Plant Master Equipment Manager")

MACHINE_FILE = "master_machine_list.csv"
PRINTER_FILE = "master_printer_list.csv"

# ==========================================================
# LOAD MACHINE DATA
# ==========================================================

if "machines" not in st.session_state:

    if os.path.exists(MACHINE_FILE):
        st.session_state.machines = pd.read_csv(MACHINE_FILE)

    else:

        data = [
            ["M13","Packer","TCS310 PRASMATIC","PRASMATIC","Line 13","2015"],
            ["M16","Packer","TCS310 PRASMATIC","PRASMATIC","Line 16","2015"],
            ["M17","Packer","TCS310 PRASMATIC","PRASMATIC","Line 17","2015"],
            ["M18","Packer","TCS310 PRASMATIC","PRASMATIC","Line 18","2015"],

            ["M13","Palletizer","TMG Automated","TMG","Line 13","2015"],
            ["M16","Palletizer","EMMTI","EMMTI","Line 16","2015"],
            ["M17","Palletizer","EMMTI","EMMTI","Line 17","2015"],
            ["M18","Palletizer","EMMTI","EMMTI","Line 18","2015"],

            ["M16","Stretch Wrapper","ATLANTA","ATLANTA","Line 16","2015"],
            ["M17","Stretch Wrapper","ATLANTA","ATLANTA","Line 17","2015"],
            ["M18","Stretch Wrapper","ATLANTA","ATLANTA","Line 18","2015"],

            ["M16","Bottle Conveyor","SIPAC","SIPAC","Line 16","2015"],
            ["M17","Bottle Conveyor","SIPAC","SIPAC","Line 17","2015"],
            ["M18","Bottle Conveyor","SIPAC","SIPAC","Line 18","2015"],

            ["M16","Empty Bottle Feeder","Lanfranchi","Lanfranchi","Line 16","2015"],

            ["M13","Bottle Conveyor","MEMCO","MEMCO","Line 13","2015"],

            ["Plant","Ozonizer System","WS","WS","Water Treatment","2015"]
        ]

        st.session_state.machines = pd.DataFrame(data, columns=[
            "Machine No",
            "Equipment Type",
            "Equipment Name",
            "Manufacturer",
            "Location",
            "Year"
        ])

# ==========================================================
# SEARCH BAR
# ==========================================================

st.subheader("🔍 Search Equipment")

search = st.text_input("Type equipment name or machine number")

filtered_data = st.session_state.machines

if search:
    filtered_data = filtered_data[
        filtered_data.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)
    ]

# ==========================================================
# MACHINE TABLE
# ==========================================================

st.subheader("📋 Equipment List")

edited_data = st.data_editor(filtered_data, num_rows="dynamic", use_container_width=True)

col1, col2, col3 = st.columns(3)

# SAVE
with col1:

    if st.button("💾 Save Changes"):

        st.session_state.machines.update(edited_data)

        st.session_state.machines.to_csv(MACHINE_FILE, index=False)

        st.success("Saved successfully")

# ADD NEW MACHINE
with col2:

    if st.button("➕ Add New Equipment"):

        new_row = pd.DataFrame(
            [["","","","","",""]],
            columns=st.session_state.machines.columns
        )

        st.session_state.machines = pd.concat(
            [st.session_state.machines,new_row],
            ignore_index=True
        )

        st.session_state.machines.to_csv(MACHINE_FILE,index=False)

        st.rerun()

# DELETE MACHINE
with col3:

    delete_name = st.text_input("Enter Machine No to Delete")

    if st.button("🗑 Delete Equipment"):

        st.session_state.machines = st.session_state.machines[
            st.session_state.machines["Machine No"] != delete_name
        ]

        st.session_state.machines.to_csv(MACHINE_FILE,index=False)

        st.success("Equipment Deleted")

        st.rerun()

# ==========================================================
# SUMMARY DASHBOARD
# ==========================================================

st.divider()

st.subheader("📊 Equipment Summary")

colA,colB,colC = st.columns(3)

with colA:
    st.metric("Total Equipment", len(st.session_state.machines))

with colB:
    st.metric("Total Lines", st.session_state.machines["Machine No"].nunique())

with colC:
    st.metric("Manufacturers", st.session_state.machines["Manufacturer"].nunique())

# ==========================================================
# DOWNLOAD BACKUP
# ==========================================================

st.divider()

st.download_button(
    label="⬇ Download Equipment List CSV",
    data=st.session_state.machines.to_csv(index=False),
    file_name="equipment_master_list.csv",
    mime="text/csv"
)

st.success("System Ready ✅")
