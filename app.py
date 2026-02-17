import streamlit as st
import pandas as pd

st.set_page_config(page_title="NADEC Breakdown Dashboard", layout="wide")

# -----------------------------------------
# HEADER
# -----------------------------------------
st.markdown("""
<div style='background:#003366; padding:15px; text-align:center; color:white; 
            font-size:22px; border-radius:6px;'>
    <b>NADEC Real-Time Maintenance Breakdown Dashboard</b>
</div>
""", unsafe_allow_html=True)

st.write("")

# -----------------------------------------
# SESSION STATE DATA
# -----------------------------------------
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(
        columns=["Date", "Machine", "Time", "Reason", "Technician"]
    )

df = st.session_state.data

# -----------------------------------------
# BUTTONS
# -----------------------------------------
colA, colB, colC = st.columns([1,1,1])

with colA:
    upload = st.file_uploader("📂 Upload CSV", type=["csv"])

    if upload:
        st.session_state.data = pd.read_csv(upload)
        st.success("CSV Loaded Successfully!")

with colB:
    add_form = st.button("➕ Add Breakdown Entry", use_container_width=True)

with colC:
    st.download_button(
        "📥 Export Updated CSV",
        df.to_csv(index=False),
        file_name="breakdown_data.csv",
        mime="text/csv",
        use_container_width=True
    )

# -----------------------------------------
# ADD ENTRY FORM
# -----------------------------------------
if add_form:
    with st.form("entry_form", clear_on_submit=True):
        st.subheader("Add Breakdown Entry")

        c1, c2 = st.columns(2)
        with c1:
            date = st.date_input("Date")
            machine = st.selectbox("Machine", [f"M{i}" for i in range(1,19)])
            time = st.number_input("Time (minutes)", min_value=1)

        with c2:
            reason = st.selectbox("Reason", ["Mechanical", "Electrical", "Automation"])
            tech = st.text_input("Technician")

        submitted = st.form_submit_button("Save Entry")

        if submitted:
            new_row = pd.DataFrame(
                [[str(date), machine, time, reason, tech]],
                columns=df.columns
            )
            st.session_state.data = pd.concat([df, new_row], ignore_index=True)
            st.success("Entry Added Successfully!")

df = st.session_state.data

# -----------------------------------------
# BREAKDOWN TABLE (WITH EDIT + DELETE)
# -----------------------------------------
st.subheader("📋 Breakdown Log")

if len(df) > 0:
    edited_df = st.data_editor(df, num_rows="dynamic")
    st.session_state.data = edited_df
else:
    st.info("No breakdown data yet.")

# -----------------------------------------
# TIMELINE VIEW (CUTE BAR STYLE)
# -----------------------------------------
st.subheader("📊 Machine Breakdown Timeline (Cute View)")

if len(df) == 0:
    st.info("Add entries to see timeline.")
else:
    machines = df["Machine"].unique()

    for m in machines:
        st.markdown(f"### {m}")

        row = df[df["Machine"] == m]

        bar_html = ""

        for _, r in row.iterrows():
            color = {
                "Mechanical": "red",
                "Electrical": "blue",
                "Automation": "green"
            }[r["Reason"]]

            width = min(int(r["Time"]) * 2, 300)  # scaling for beauty

            bar_html += f"""
            <div title="Reason: {r['Reason']} | Time: {r['Time']} min | Tech: {r['Technician']}"
                 style="
                    display:inline-block;
                    width:{width}px;
                    height:18px;
                    background:{color};
                    border-radius:6px;
                    margin-right:4px;
                    cursor:pointer;">
            </div>
            """

        st.markdown(f"<div>{bar_html}</div>", unsafe_allow_html=True)
