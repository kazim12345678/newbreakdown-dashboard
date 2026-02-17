import streamlit as st
import pandas as pd

st.set_page_config(page_title="Breakdown Dashboard", layout="wide")

st.title("🛠 Live Breakdown Entry + Machine Tracker (M1–M18)")

# -----------------------------------------
# Load or initialize data
# -----------------------------------------
if "breakdowns" not in st.session_state:
    st.session_state.breakdowns = pd.DataFrame(
        columns=["Date", "Machine", "Minutes", "Reason"]
    )

df = st.session_state.breakdowns

# -----------------------------------------
# Breakdown Entry Form
# -----------------------------------------
with st.expander("➕ Add Breakdown Entry", expanded=False):
    col1, col2 = st.columns(2)

    with col1:
        date = st.date_input("Date")
        machine = st.selectbox("Machine", [f"M{i}" for i in range(1, 18+1)])

    with col2:
        minutes = st.number_input("Downtime Minutes", min_value=1, step=1)
        reason = st.selectbox(
            "Reason",
            ["Mechanical", "Electrical", "Automation", "Operator Error"]
        )

    if st.button("✅ Save Breakdown Entry"):
        new_row = pd.DataFrame(
            [[str(date), machine, minutes, reason]],
            columns=df.columns
        )
        st.session_state.breakdowns = pd.concat([df, new_row], ignore_index=True)
        st.success("Breakdown entry saved!")

df = st.session_state.breakdowns

# -----------------------------------------
# Machine Tiles (M1–M18)
# -----------------------------------------
st.subheader("📊 Machine Downtime Tiles (Click Any Machine)")

tile_cols = st.columns(6)

for i in range(1, 19):
    m = f"M{i}"
    total = df[df["Machine"] == m]["Minutes"].sum()

    with tile_cols[(i-1) % 6]:
        if st.button(f"{m}\n{total} min", key=f"tile_{m}"):
            st.session_state.selected_machine = m

# -----------------------------------------
# Machine Popup (Streamlit Modal)
# -----------------------------------------
if "selected_machine" in st.session_state:
    m = st.session_state.selected_machine
    total = df[df["Machine"] == m]["Minutes"].sum()

    with st.modal(f"Machine {m} Summary"):
        st.write(f"### Total Downtime: **{total} minutes**")
        st.write("#### Breakdown Details")
        st.dataframe(df[df["Machine"] == m])

        if st.button("Close"):
            del st.session_state.selected_machine

# -----------------------------------------
# Breakdown Table (Editable)
# -----------------------------------------
st.subheader("📋 Breakdown Log Table (Editable)")

edited_df = st.data_editor(df, num_rows="dynamic")

# Save edits
st.session_state.breakdowns = edited_df

# -----------------------------------------
# Export CSV
# -----------------------------------------
st.download_button(
    "⬇ Download CSV Report",
    edited_df.to_csv(index=False),
    file_name="NADEC_Breakdown_Report.csv",
    mime="text/csv"
)
