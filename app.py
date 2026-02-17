import streamlit as st
import pandas as pd

st.set_page_config(page_title="Breakdown Dashboard", layout="wide")

st.title("🛠 Maintenance Breakdown Dashboard (18 Machines)")

uploaded_file = st.file_uploader("Upload Breakdown CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📋 Breakdown Log Table")
    edited_df = st.data_editor(df, num_rows="dynamic")

    st.subheader("📊 Breakdown Time by Machine")
    summary = edited_df.groupby("Machine")["Time"].sum()
    st.bar_chart(summary)

    st.download_button(
        "📥 Download Updated CSV",
        edited_df.to_csv(index=False),
        file_name="updated_breakdown.csv",
        mime="text/csv"
    )
else:
    st.info("Please upload a CSV file to start.")
