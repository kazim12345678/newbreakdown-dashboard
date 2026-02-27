# ============================================================
# KPI #2 – NOTIFICATION PERFORMANCE ANALYTICS
# ============================================================

st.subheader("📢 KPI #2 – Notification Compliance Dashboard")

# ------------------------------------------------------------
# PREPARE NOTIFICATION DATA
# ------------------------------------------------------------

notif_df = df.copy()

notif_summary = (
    notif_df
    .groupby(["Date_Clean", "Notification_Status"])
    .size()
    .unstack(fill_value=0)
    .reset_index()
)

# Ensure both columns exist
if "With Notification" not in notif_summary.columns:
    notif_summary["With Notification"] = 0
if "Without Notification" not in notif_summary.columns:
    notif_summary["Without Notification"] = 0

notif_summary["Total_Jobs"] = (
    notif_summary["With Notification"] +
    notif_summary["Without Notification"]
)

notif_summary["Compliance_%"] = (
    notif_summary["With Notification"] /
    notif_summary["Total_Jobs"]
) * 100

# ------------------------------------------------------------
# GLOBAL METRICS
# ------------------------------------------------------------

TOTAL_JOBS = notif_summary["Total_Jobs"].sum()
TOTAL_WITH = notif_summary["With Notification"].sum()
TOTAL_WITHOUT = notif_summary["Without Notification"].sum()

OVERALL_COMPLIANCE = (TOTAL_WITH / TOTAL_JOBS) * 100
OVERALL_NON_COMPLIANCE = (TOTAL_WITHOUT / TOTAL_JOBS) * 100

BEST_DAY = notif_summary.loc[notif_summary["Compliance_%"].idxmax()]
WORST_DAY = notif_summary.loc[notif_summary["Compliance_%"].idxmin()]

COMPLIANCE_STD = notif_summary["Compliance_%"].std()

# ------------------------------------------------------------
# EXECUTIVE METRIC CARDS
# ------------------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Jobs", int(TOTAL_JOBS))
col2.metric("With Notification %", f"{OVERALL_COMPLIANCE:.1f}%")
col3.metric("Without Notification %", f"{OVERALL_NON_COMPLIANCE:.1f}%")
col4.metric("Compliance Stability (Std Dev)", f"{COMPLIANCE_STD:.2f}")

col5, col6 = st.columns(2)

col5.metric(
    "Best Compliance Day",
    BEST_DAY["Date_Clean"].date(),
    f"{BEST_DAY['Compliance_%']:.1f}%"
)

col6.metric(
    "Worst Compliance Day",
    WORST_DAY["Date_Clean"].date(),
    f"{WORST_DAY['Compliance_%']:.1f}%"
)

st.markdown("---")

# ------------------------------------------------------------
# BEAUTIFUL STACKED BAR – DAILY BREAKDOWN
# ------------------------------------------------------------

fig1 = px.bar(
    notif_summary,
    x="Date_Clean",
    y=["With Notification", "Without Notification"],
    title="Daily Jobs – With vs Without Notification",
    barmode="stack",
    template="plotly_dark"
)

fig1.update_layout(
    xaxis_title="Date",
    yaxis_title="Number of Jobs",
    legend_title="Notification Status",
    height=500
)

st.plotly_chart(fig1, use_container_width=True)

# ------------------------------------------------------------
# COMPLIANCE TREND LINE
# ------------------------------------------------------------

fig2 = px.line(
    notif_summary,
    x="Date_Clean",
    y="Compliance_%",
    markers=True,
    title="Daily Notification Compliance %",
    template="plotly_dark"
)

fig2.update_layout(
    yaxis=dict(range=[0, 100]),
    height=450
)

st.plotly_chart(fig2, use_container_width=True)

# ------------------------------------------------------------
# 7-DAY ROLLING TREND
# ------------------------------------------------------------

notif_summary["Rolling_7Day_Compliance"] = (
    notif_summary["Compliance_%"]
    .rolling(7)
    .mean()
)

fig3 = px.line(
    notif_summary,
    x="Date_Clean",
    y="Rolling_7Day_Compliance",
    title="7-Day Rolling Compliance Trend",
    template="plotly_dark"
)

fig3.update_layout(
    yaxis=dict(range=[0, 100]),
    height=450
)

st.plotly_chart(fig3, use_container_width=True)

# ------------------------------------------------------------
# PIE CHART – OVERALL DISTRIBUTION
# ------------------------------------------------------------

fig4 = px.pie(
    values=[TOTAL_WITH, TOTAL_WITHOUT],
    names=["With Notification", "Without Notification"],
    title="Overall Notification Distribution",
    template="plotly_dark",
    hole=0.5
)

st.plotly_chart(fig4, use_container_width=True)

# ------------------------------------------------------------
# BEAUTIFUL EXECUTIVE TABLE
# ------------------------------------------------------------

styled_table = notif_summary.style \
    .background_gradient(subset=["Compliance_%"], cmap="YlGn") \
    .format({
        "Compliance_%": "{:.1f}%",
        "Rolling_7Day_Compliance": "{:.1f}%"
    })

st.markdown("### 📋 Detailed Daily Notification Table")
st.dataframe(styled_table, use_container_width=True)
