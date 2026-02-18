import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="NADEC Breakdown Dashboard", layout="wide")

st.title("NADEC Breakdown Maintenance Dashboard 2025")

# Monthly downtime data
monthly_data = pd.DataFrame({
    "Month": ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
    "Downtime Hours": [285,241,312,222,304,260,446,277,260,327,270,257]
})

# Show table
st.subheader("📅 Monthly Downtime Summary")
st.dataframe(monthly_data)

# Plot chart
fig = px.bar(monthly_data, x="Month", y="Downtime Hours", title="Monthly Downtime Hours")
st.plotly_chart(fig, use_container_width=True)
