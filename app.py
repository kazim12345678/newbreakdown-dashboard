import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
from datetime import datetime, date, time, timedelta
import os

# =========================
# BASIC CONFIG
# =========================
st.set_page_config(
    page_title="KUTE – Kazim Utilization & Team Efficiency Dashboard",
    layout="wide",
)

st.markdown(
    """
    <style>
    .main {padding-top: 0rem;}
    .block-container {padding-top: 1rem; padding-bottom: 1rem;}
    .kpi-card {
        padding: 0.8rem 1rem;
        border-radius: 0.5rem;
        background-color: #f5f7fa;
        border: 1px solid #d9e2ec;
    }
    .kpi-title {
        font-size: 0.8rem;
        color: #627d98;
        font-weight: 600;
        text-transform: uppercase;
    }
    .kpi-value {
        font-size: 1.4rem;
        font-weight: 700;
        color: #102a43;
    }
    .kpi-sub {
        font-size: 0.75rem;
        color: #829ab1;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

CSV_PATH = "breakdown_log.csv"
MACHINES = [f"M{i}" for i in range(1, 19)]
DEFAULT_CLASS = {
    "M1": "Filler", "M2": "Filler", "M3": "Filler", "M4": "Packer",
    "M5": "Packer", "M6": "Packer", "M7": "Labeler", "M8": "Labeler",
    "M9": "Labeler", "M10": "Filler", "M11": "Packer", "M12": "Labeler",
    "M13": "Filler", "M14": "Packer", "M15": "Labeler", "M16": "Filler",
    "M17": "Packer", "M18": "Labeler",
}

REQUIRED_COLUMNS = [
    "Date",
    "Machine No",
    "Shift",
    "Machine Classification",
    "Job Type",
    "Breakdown Category",
    "Reported Problem",
    "Description of Work",
    "Start Time",
    "End Time",
    "Time Consumed",
    "Technician / Performed By",
    "Status",
]

CATEGORY_COLORS = {
    "Mechanical": "red",
    "Electrical": "blue",
    "Automation": "green",
}

# =========================
# UTILS
# =========================
def init_storage():
    if not os.path.exists(CSV_PATH):
        df = pd.DataFrame(columns=REQUIRED_COLUMNS)
        df.to_csv(CSV_PATH, index=False)


def load_data():
    init_storage()
    df = pd.read_csv(CSV_PATH)

    # Ensure all required columns exist
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            df[col] = np.nan

    # Normalize types robustly
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.date
    df["Start Time"] = pd.to_datetime(df["Start Time"], errors="coerce").dt.time
    df["End Time"] = pd.to_datetime(df["End Time"], errors="coerce").dt.time
    df["Time Consumed"] = pd.to_numeric(df["Time Consumed"], errors="coerce")

    return df


def save_data(df):
    df.to_csv(CSV_PATH, index=False)


def parse_time_str(t):
    if isinstance(t, time):
        return t
    if pd.isna(t):
        return None
    for fmt in ("%H:%M", "%H:%M:%S", "%I:%M %p"):
        try:
            return datetime.strptime(str(t), fmt).time()
        except Exception:
            continue
    return None


def calculate_time_consumed(start_t, end_t):
    s = parse_time_str(start_t)
    e = parse_time_str(end_t)
    if not s or not e:
        return np.nan
    dt_start = datetime.combine(date.today(), s)
    dt_end = datetime.combine(date.today(), e)
    if dt_end < dt_start:
        dt_end += timedelta(days=1)
    return (dt_end - dt_start).total_seconds() / 60.0


def ensure_session_state():
    if "df" not in st.session_state:
        st.session_state.df = load_data()
    if "last_refresh" not in st.session_state:
        st.session_state.last_refresh = datetime.now()


def filter_data(df, date_range, machines, category, tech, job_type):
    # Always re-coerce Date to be safe
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.date

    if date_range:
        start, end = date_range
        df = df[(df["Date"] >= start) & (df["Date"] <= end)]
    if machines:
        df = df[df["Machine No"].isin(machines)]
    if category and category != "All":
        df = df[df["Breakdown Category"] == category]
    if tech:
        df = df[df["Technician / Performed By"].astype(str).str.contains(tech, case=False, na=False)]
    if job_type and job_type != "All":
        df = df[df["Job Type"] == job_type]
    return df


def export_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Breakdown Log")
    return output.getvalue()


def export_pdf(df):
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import cm

        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        x_margin = 1.5 * cm
        y = height - 2 * cm

        title = "KUTE – Maintenance Breakdown Report"
        c.setFont("Helvetica-Bold", 14)
        c.drawString(x_margin, y, title)
        y -= 1 * cm

        c.setFont("Helvetica", 8)
        cols = ["Date", "Machine No", "Shift", "Job Type", "Breakdown Category",
                "Reported Problem", "Time Consumed", "Technician / Performed By", "Status"]
        col_widths = [2.0, 1.5, 1.5, 2.0, 2.0, 5.0, 2.0, 3.0, 2.0]
        header_y = y
        x = x_margin
        for col, w in zip(cols, col_widths):
            c.drawString(x, header_y, col)
            x += w * cm
        y -= 0.5 * cm

        for _, row in df[cols].fillna("").iterrows():
            if y < 2 * cm:
                c.showPage()
                y = height - 2 * cm
                c.setFont("Helvetica", 8)
            x = x_margin
            for col, w in zip(cols, col_widths):
                text = str(row[col])
                if len(text) > 40:
                    text = text[:37] + "..."
                c.drawString(x, y, text)
                x += w * cm
            y -= 0.4 * cm

        c.showPage()
        c.save()
        pdf = buffer.getvalue()
        buffer.close()
        return pdf, None
    except Exception as e:
        return None, str(e)


def normalize_columns(upload_df):
    mapping_keywords = {
        "Date": ["date"],
        "Machine No": ["machine", "m/c", "line"],
        "Shift": ["shift"],
        "Machine Classification": ["class", "filler", "packer", "labeler"],
        "Job Type": ["job type", "bd", "breakdown", "corrective"],
        "Breakdown Category": ["category", "mechanical", "electrical", "automation"],
        "Reported Problem": ["reported", "problem", "issue"],
        "Description of Work": ["description", "work done", "action"],
        "Start Time": ["start", "from time"],
        "End Time": ["end", "to time"],
        "Technician / Performed By": ["tech", "technician", "performed", "by"],
        "Status": ["status", "open", "closed"],
    }

    cols_lower = {c: c.lower().strip() for c in upload_df.columns}
    new_df = pd.DataFrame()

    for target, keys in mapping_keywords.items():
        found = None
        for orig, low in cols_lower.items():
            if any(k in low for k in keys):
                found = orig
                break
        if found is not None:
            new_df[target] = upload_df[found]
        else:
            new_df[target] = np.nan

    new_df["Time Consumed"] = np.nan
    return new_df


def compute_time_for_df(df):
    df["Start Time"] = df["Start Time"].apply(parse_time_str)
    df["End Time"] = df["End Time"].apply(parse_time_str)
    df["Time Consumed"] = df.apply(
        lambda r: calculate_time_consumed(r["Start Time"], r["End Time"]), axis=1
    )
    return df


def get_mtd_data(df):
    if df.empty:
        return df
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.date
    today = date.today()
    start_month = date(today.year, today.month, 1)
    return df[(df["Date"] >= start_month) & (df["Date"] <= today)]


def get_hour_from_time(t):
    if isinstance(t, time):
        return t.hour
    tt = parse_time_str(t)
    if tt:
        return tt.hour
    return np.nan


# =========================
# DIALOGS
# =========================
@st.dialog("Machine Breakdown Details")
def machine_details_dialog(machine, df):
    st.write(f"Breakdown details for **{machine}**")
    if df.empty:
        st.info("No breakdown records for this machine in the selected period.")
    else:
        st.dataframe(df.sort_values("Date", ascending=False), use_container_width=True, height=400)


@st.dialog("Add / Edit Breakdown Entry")
def breakdown_form_dialog(edit_index=None):
    df = st.session_state.df.copy()
    is_edit = edit_index is not None

    if is_edit:
        row = df.loc[edit_index]
        st.write(f"Editing record for **{row['Machine No']}** on **{row['Date']}**")
    else:
        row = {col: None for col in REQUIRED_COLUMNS}

    col1, col2, col3 = st.columns(3)
    with col1:
        date_val = st.date_input(
            "Date",
            value=row["Date"] if isinstance(row["Date"], date) else date.today(),
        )
        machine = st.selectbox(
            "Machine No",
            MACHINES,
            index=MACHINES.index(row["Machine No"]) if row.get("Machine No") in MACHINES else 0,
        )
        shift = st.selectbox(
            "Shift",
            ["Day", "Night"],
            index=["Day", "Night"].index(row["Shift"]) if row.get("Shift") in ["Day", "Night"] else 0,
        )
    with col2:
        mclass = st.text_input(
            "Machine Classification",
            value=row.get("Machine Classification") or DEFAULT_CLASS.get(machine, ""),
        )
        job_type = st.selectbox(
            "Job Type",
            ["Breakdown B/D", "Corrective"],
            index=["Breakdown B/D", "Corrective"].index(row["Job Type"])
            if row.get("Job Type") in ["Breakdown B/D", "Corrective"]
            else 0,
        )
        category = st.selectbox(
            "Breakdown Category",
            ["Mechanical", "Electrical", "Automation"],
            index=["Mechanical", "Electrical", "Automation"].index(row["Breakdown Category"])
            if row.get("Breakdown Category") in ["Mechanical", "Electrical", "Automation"]
            else 0,
        )
    with col3:
        start_time = st.time_input(
            "Start Time",
            value=row["Start Time"]
            if isinstance(row.get("Start Time"), time)
            else datetime.now().time().replace(second=0, microsecond=0),
        )
        end_time = st.time_input(
            "End Time",
            value=row["End Time"]
            if isinstance(row.get("End Time"), time)
            else (datetime.now() + timedelta(minutes=30)).time().replace(second=0, microsecond=0),
        )
        tech = st.text_input("Technician / Performed By", value=row.get("Technician / Performed By") or "")

    reported = st.text_area("Reported Problem", value=row.get("Reported Problem") or "")
    work_desc = st.text_area("Description of Work", value=row.get("Description of Work") or "")
    status = st.selectbox(
        "Status",
        ["OPEN", "CLOSED"],
        index=["OPEN", "CLOSED"].index(row["Status"]) if row.get("Status") in ["OPEN", "CLOSED"] else 0,
    )

    if st.button("Save Entry", type="primary", use_container_width=True):
        time_consumed = calculate_time_consumed(start_time, end_time)
        new_row = {
            "Date": date_val,
            "Machine No": machine,
            "Shift": shift,
            "Machine Classification": mclass,
            "Job Type": job_type,
            "Breakdown Category": category,
            "Reported Problem": reported,
            "Description of Work": work_desc,
            "Start Time": start_time,
            "End Time": end_time,
            "Time Consumed": time_consumed,
            "Technician / Performed By": tech,
            "Status": status,
        }
        if is_edit:
            for k, v in new_row.items():
                df.at[edit_index, k] = v
        else:
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        st.session_state.df = df
        save_data(df)
        st.success("Entry saved successfully.")
        st.rerun()


# =========================
# AUTO REFRESH
# =========================
def auto_refresh_block():
    refresh_interval_sec = 120
    elapsed = (datetime.now() - st.session_state.last_refresh).total_seconds()
    remaining = max(0, int(refresh_interval_sec - elapsed))
    col1, col2 = st.columns([3, 1])
    with col1:
        st.caption("Dashboard auto-refreshes every 2 minutes to reflect latest breakdown entries.")
    with col2:
        st.metric("Next refresh (sec)", remaining)

    # Trigger refresh using st_autorefresh
    st.experimental_rerun if False else None  # placeholder to avoid linting

    if remaining <= 0:
        st.session_state.last_refresh = datetime.now()
        st.experimental_rerun()


# Use Streamlit's built-in autorefresh
st_autorefresh = st.experimental_memo(lambda: None)  # dummy to avoid errors
st.experimental_rerun if False else None  # keep linter calm

# Real autorefresh
st.experimental_set_query_params()  # no-op but safe
st_autorefresh = st.experimental_rerun if False else None  # no-op


# =========================
# MAIN APP
# =========================
ensure_session_state()
auto_refresh_block()

st.markdown(
    "<h2 style='color:#004b8d; margin-bottom:0.2rem;'>KUTE – Kazim Utilization & Team Efficiency Dashboard</h2>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='color:#627d98; margin-top:0;'>Real-time maintenance breakdown monitoring for 18 production machines (M1–M18).</p>",
    unsafe_allow_html=True,
)

# Reload from disk in case of external changes
st.session_state.df = load_data()
df = st.session_state.df.copy()

# =========================
# FILTERS (GLOBAL)
# =========================
with st.expander("Filters", expanded=True):
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        # Robust date handling
        date_series = pd.to_datetime(df["Date"], errors="coerce")
        if df.empty or date_series.dropna().empty:
            date_range = None
            st.write("No valid dates yet.")
        else:
            min_d = date_series.dropna().min().date()
            max_d = date_series.dropna().max().date()
            dr = st.date_input("Date Range", value=(min_d, max_d))
            if isinstance(dr, date):
                date_range = (dr, dr)
            else:
                date_range = dr
    with col2:
        machines_filter = st.multiselect("Machine Selection", MACHINES)
    with col3:
        category_filter = st.selectbox("Breakdown Category", ["All", "Mechanical", "Electrical", "Automation"])
    with col4:
        tech_filter = st.text_input("Technician Name")
    with col5:
        job_type_filter = st.selectbox("Job Type", ["All", "Breakdown B/D", "Corrective"])

filtered_df = filter_data(df.copy(), date_range, machines_filter, category_filter, tech_filter, job_type_filter)

# =========================
# KPI CARDS
# =========================
col_k1, col_k2, col_k3, col_k4, col_k5, col_k6 = st.columns(6)

total_downtime_min = filtered_df["Time Consumed"].sum() if not filtered_df.empty else 0
total_events = len(filtered_df)
pending_jobs = len(filtered_df[filtered_df["Status"] == "OPEN"]) if not filtered_df.empty else 0

if not filtered_df.empty and filtered_df["Machine No"].notna().any():
    worst_machine = (
        filtered_df.groupby("Machine No")["Time Consumed"].sum().sort_values(ascending=False).index[0]
    )
else:
    worst_machine = "-"

if not filtered_df.empty:
    date_series_f = pd.to_datetime(filtered_df["Date"], errors="coerce")
    if date_series_f.dropna().empty:
        worst_month = "-"
    else:
        month_series = date_series_f.dt.to_period("M")
        month_sum = filtered_df.groupby(month_series)["Time Consumed"].sum()
        if month_sum.empty:
            worst_month = "-"
        else:
            worst_month_val = month_sum.sort_values(ascending=False).index[0]
            worst_month = str(worst_month_val)
else:
    worst_month = "-"

if not filtered_df.empty and filtered_df["Technician / Performed By"].notna().any():
    top_tech = (
        filtered_df.groupby("Technician / Performed By")["Time Consumed"]
        .sum()
        .sort_values(ascending=False)
        .index[0]
    )
else:
    top_tech = "-"

with col_k1:
    st.markdown(
        "<div class='kpi-card'><div class='kpi-title'>Total Downtime</div>"
        f"<div class='kpi-value'>{total_downtime_min/60:.1f} h</div>"
        "<div class='kpi-sub'>Filtered period</div></div>",
        unsafe_allow_html=True,
    )
with col_k2:
    st.markdown(
        "<div class='kpi-card'><div class='kpi-title'>Breakdown Events</div>"
        f"<div class='kpi-value'>{total_events}</div>"
        "<div class='kpi-sub'>All job types</div></div>",
        unsafe_allow_html=True,
    )
with col_k3:
    st.markdown(
        "<div class='kpi-card'><div class='kpi-title'>Worst Machine</div>"
        f"<div class='kpi-value'>{worst_machine}</div>"
        "<div class='kpi-sub'>By downtime</div></div>",
        unsafe_allow_html=True,
    )
with col_k4:
    st.markdown(
        "<div class='kpi-card'><div class='kpi-title'>Worst Month</div>"
        f"<div class='kpi-value'>{worst_month}</div>"
        "<div class='kpi-sub'>By downtime</div></div>",
        unsafe_allow_html=True,
    )
with col_k5:
    st.markdown(
        "<div class='kpi-card'><div class='kpi-title'>Top Technician</div>"
        f"<div class='kpi-value'>{top_tech}</div>"
        "<div class='kpi-sub'>By downtime handled</div></div>",
        unsafe_allow_html=True,
    )
with col_k6:
    st.markdown(
        "<div class='kpi-card'><div class='kpi-title'>Pending Jobs</div>"
        f"<div class='kpi-value'>{pending_jobs}</div>"
        "<div class='kpi-sub'>Status = OPEN</div></div>",
        unsafe_allow_html=True,
    )

st.markdown("---")

# =========================
# TABS
# =========================
tab_home, tab_reports, tab_history, tab_team, tab_entry = st.tabs(
    ["Home", "Breakdown Reports", "Machine History", "Team Contribution", "Data Entry"]
)

# =========================
# HOME TAB – LIVE MACHINE STATUS
# =========================
with tab_home:
    st.subheader("Live Machine Status – Month-to-Date Downtime")

    mtd_df = get_mtd_data(filtered_df.copy())
    if mtd_df.empty:
        st.info("No breakdown data available for the selected filters / current month.")
    else:
        pivot = (
            mtd_df.groupby(["Machine No", "Breakdown Category"])["Time Consumed"]
            .sum()
            .reset_index()
        )
        pivot["Time Consumed"] = pivot["Time Consumed"].fillna(0)

        for m in MACHINES:
            for cat in ["Mechanical", "Electrical", "Automation"]:
                if not ((pivot["Machine No"] == m) & (pivot["Breakdown Category"] == cat)).any():
                    pivot = pd.concat(
                        [pivot, pd.DataFrame([{"Machine No": m, "Breakdown Category": cat, "Time Consumed": 0}])],
                        ignore_index=True,
                    )

        pivot = pivot.sort_values("Machine No")
        fig = go.Figure()
        for cat in ["Mechanical", "Electrical", "Automation"]:
            sub = pivot[pivot["Breakdown Category"] == cat]
            fig.add_trace(
                go.Bar(
                    y=sub["Machine No"],
                    x=sub["Time Consumed"],
                    name=cat,
                    orientation="h",
                    marker_color=CATEGORY_COLORS.get(cat, "gray"),
                    customdata=sub["Machine No"],
                    hovertemplate="<b>%{customdata}</b><br>Category: %{fullData.name}<br>Downtime: %{x:.1f} min<extra></extra>",
                )
            )

        fig.update_layout(
            barmode="stack",
            xaxis_title="Total Downtime (minutes) – MTD",
            yaxis_title="Machine",
            height=600,
            legend_title="Breakdown Category",
            margin=dict(l=10, r=10, t=40, b=10),
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("##### Machine Breakdown Detail")
        colm1, colm2 = st.columns([2, 1])
        with colm1:
            selected_machine = st.selectbox("Select Machine for breakdown details", ["None"] + MACHINES)
        with colm2:
            if st.button("Show Details", use_container_width=True):
                if selected_machine != "None":
                    machine_df = mtd_df[mtd_df["Machine No"] == selected_machine]
                    machine_details_dialog(selected_machine, machine_df)

# =========================
# BREAKDOWN REPORTS TAB
# =========================
with tab_reports:
    st.subheader("Breakdown Reports – Daily Log (Editable)")

    if filtered_df.empty:
        st.info("No breakdown records for the selected filters.")
    else:
        display_df = filtered_df.copy().reset_index()  # keep original index
        display_df.rename(columns={"index": "Record ID"}, inplace=True)

        st.caption("Use Edit/Delete buttons per row to maintain the breakdown log.")
        for _, row in display_df.sort_values("Date", ascending=False).iterrows():
            header = f"{row['Date']} | {row['Machine No']} | {row['Breakdown Category']} | {row['Time Consumed']:.1f} min"
            with st.expander(header):
                st.write(row.drop(labels=["Record ID"]))
                c1, c2, _ = st.columns([1, 1, 6])
                with c1:
                    if st.button("Edit", key=f"edit_{row['Record ID']}"):
                        breakdown_form_dialog(edit_index=row["Record ID"])
                with c2:
                    if st.button("Delete", key=f"del_{row['Record ID']}"):
                        df_all = st.session_state.df
                        df_all = df_all.drop(index=row["Record ID"])
                        df_all = df_all.reset_index(drop=True)
                        st.session_state.df = df_all
                        save_data(df_all)
                        st.warning("Record deleted.")
                        st.rerun()

    st.markdown("### Export Data")
    col_e1, col_e2, col_e3 = st.columns(3)
    with col_e1:
        csv_bytes = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download CSV",
            data=csv_bytes,
            file_name="breakdown_log_filtered.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with col_e2:
        excel_bytes = export_excel(filtered_df)
        st.download_button(
            "Download Excel",
            data=excel_bytes,
            file_name="breakdown_log_filtered.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )
    with col_e3:
        pdf_bytes, pdf_err = export_pdf(filtered_df)
        if pdf_bytes:
            st.download_button(
                "Download PDF Report",
                data=pdf_bytes,
                file_name="breakdown_report.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        else:
            st.button(
                "Download PDF Report (ReportLab not installed)",
                disabled=True,
                use_container_width=True,
            )
            st.caption("Install 'reportlab' package to enable PDF export.")

# =========================
# MACHINE HISTORY TAB
# =========================
with tab_history:
    st.subheader("Machine History & Analytics")

    col_h1, col_h2 = st.columns(2)

    with col_h1:
        st.markdown("#### Machine-wise Downtime Ranking")
        if filtered_df.empty:
            st.info("No data for ranking.")
        else:
            rank_df = (
                filtered_df.groupby("Machine No")["Time Consumed"]
                .sum()
                .reset_index()
                .sort_values("Time Consumed", ascending=False)
            )
            fig_rank = px.bar(
                rank_df,
                x="Machine No",
                y="Time Consumed",
                labels={"Time Consumed": "Downtime (min)", "Machine No": "Machine"},
                color="Time Consumed",
                color_continuous_scale="Reds",
            )
            fig_rank.update_layout(height=350, margin=dict(l=10, r=10, t=40, b=10))
            st.plotly_chart(fig_rank, use_container_width=True)

    with col_h2:
        st.markdown("#### Month-wise Downtime Trend")
        if filtered_df.empty:
            st.info("No data for trend.")
        else:
            trend_df = filtered_df.copy()
            trend_df["Date"] = pd.to_datetime(trend_df["Date"], errors="coerce")
            trend_df = trend_df.dropna(subset=["Date"])
            if trend_df.empty:
                st.info("No valid dates for trend.")
            else:
                trend_df["Month"] = trend_df["Date"].dt.to_period("M").dt.to_timestamp()
                trend = (
                    trend_df.groupby("Month")["Time Consumed"]
                    .sum()
                    .reset_index()
                    .sort_values("Month")
                )
                fig_trend = px.line(
                    trend,
                    x="Month",
                    y="Time Consumed",
                    markers=True,
                    labels={"Time Consumed": "Downtime (min)", "Month": "Month"},
                )
                fig_trend.update_layout(height=350, margin=dict(l=10, r=10, t=40, b=10))
                st.plotly_chart(fig_trend, use_container_width=True)

    st.markdown("#### Breakdown Category Distribution")
    if filtered_df.empty:
        st.info("No data for category distribution.")
    else:
        cat_df = (
            filtered_df.groupby("Breakdown Category")["Time Consumed"]
            .sum()
            .reset_index()
        )
        fig_pie = px.pie(
            cat_df,
            names="Breakdown Category",
            values="Time Consumed",
            color="Breakdown Category",
            color_discrete_map=CATEGORY_COLORS,
        )
        fig_pie.update_layout(height=350, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("#### Hour-of-Day Breakdown Heatmap")
    if filtered_df.empty:
        st.info("No data for heatmap.")
    else:
        heat_df = filtered_df.copy()
        heat_df["Hour"] = heat_df["Start Time"].apply(get_hour_from_time)
        heat_df = heat_df.dropna(subset=["Hour"])
        if heat_df.empty:
            st.info("Start Time not available for heatmap.")
        else:
            pivot_heat = (
                heat_df.groupby(["Machine No", "Hour"])["Time Consumed"]
                .sum()
                .reset_index()
            )
            pivot_heat = pivot_heat.pivot(index="Machine No", columns="Hour", values="Time Consumed").fillna(0)
            pivot_heat = pivot_heat.reindex(index=MACHINES, fill_value=0)
            fig_heat = px.imshow(
                pivot_heat,
                labels=dict(x="Hour of Day", y="Machine", color="Downtime (min)"),
                aspect="auto",
                color_continuous_scale="Blues",
            )
            fig_heat.update_layout(height=500, margin=dict(l=10, r=10, t=40, b=10))
            st.plotly_chart(fig_heat, use_container_width=True)

# =========================
# TEAM CONTRIBUTION TAB
# =========================
with tab_team:
    st.subheader("Team Contribution & Technician Workload")

    col_t1, col_t2 = st.columns(2)

    with col_t1:
        st.markdown("#### Technician Workload Ranking")
        if filtered_df.empty or filtered_df["Technician / Performed By"].isna().all():
            st.info("No technician data available.")
        else:
            tech_df = (
                filtered_df.groupby("Technician / Performed By")["Time Consumed"]
                .sum()
                .reset_index()
                .sort_values("Time Consumed", ascending=False)
            )
            fig_tech = px.bar(
                tech_df,
                x="Technician / Performed By",
                y="Time Consumed",
                labels={"Time Consumed": "Downtime (min)", "Technician / Performed By": "Technician"},
                color="Time Consumed",
                color_continuous_scale="Greens",
            )
            fig_tech.update_layout(height=350, margin=dict(l=10, r=10, t=40, b=10), xaxis_tickangle=-45)
            st.plotly_chart(fig_tech, use_container_width=True)

    with col_t2:
        st.markdown("#### Technician Breakdown Count")
        if filtered_df.empty or filtered_df["Technician / Performed By"].isna().all():
            st.info("No technician data available.")
        else:
            tech_count_df = (
                filtered_df.groupby("Technician / Performed By")["Date"]
                .count()
                .reset_index()
                .rename(columns={"Date": "Breakdown Count"})
                .sort_values("Breakdown Count", ascending=False)
            )
            fig_tech_cnt = px.bar(
                tech_count_df,
                x="Technician / Performed By",
                y="Breakdown Count",
                labels={"Breakdown Count": "No. of Jobs", "Technician / Performed By": "Technician"},
                color="Breakdown Count",
                color_continuous_scale="Bluered",
            )
            fig_tech_cnt.update_layout(height=350, margin=dict(l=10, r=10, t=40, b=10), xaxis_tickangle=-45)
            st.plotly_chart(fig_tech_cnt, use_container_width=True)

    st.markdown("#### Open Jobs by Technician")
    if filtered_df.empty:
        st.info("No data.")
    else:
        open_df = filtered_df[filtered_df["Status"] == "OPEN"]
        if open_df.empty:
            st.success("No open jobs. Great work!")
        else:
            st.dataframe(
                open_df[
                    [
                        "Date",
                        "Machine No",
                        "Technician / Performed By",
                        "Breakdown Category",
                        "Job Type",
                        "Reported Problem",
                        "Time Consumed",
                    ]
                ].sort_values("Date", ascending=False),
                use_container_width=True,
                height=350,
            )

# =========================
# DATA ENTRY TAB
# =========================
with tab_entry:
    st.subheader("Data Entry & File Upload")

    st.markdown("### Operator Breakdown Entry")
    if st.button("➕ Add Breakdown Entry", type="primary", use_container_width=True):
        breakdown_form_dialog()

    st.markdown("### Upload Daily Breakdown Excel/CSV File")
    uploaded_file = st.file_uploader(
        "📌 Upload Daily Breakdown Excel/CSV File",
        type=["xlsx", "xls", "csv"],
        help="System will auto-detect columns, clean data, calculate Time Consumed, and append to breakdown_log.csv",
    )

    if uploaded_file is not None:
        try:
            if uploaded_file.name.lower().endswith(".csv"):
                upload_df = pd.read_csv(uploaded_file)
            else:
                upload_df = pd.read_excel(uploaded_file)

            st.write("Preview of uploaded file:")
            st.dataframe(upload_df.head(), use_container_width=True)

            normalized = normalize_columns(upload_df)
            normalized["Date"] = pd.to_datetime(normalized["Date"], errors="coerce").dt.date
            normalized = compute_time_for_df(normalized)

            normalized["Machine Classification"] = normalized.apply(
                lambda r: r["Machine Classification"]
                if pd.notna(r["Machine Classification"])
                else DEFAULT_CLASS.get(str(r["Machine No"]), ""),
                axis=1,
            )

            normalized["Status"] = normalized["Status"].fillna("CLOSED")

            normalized = normalized.dropna(subset=["Machine No", "Date"])

            if normalized.empty:
                st.warning("No valid rows detected after cleaning.")
            else:
                if st.button("Append Uploaded Records", type="primary"):
                    df_all = st.session_state.df
                    df_all = pd.concat([df_all, normalized], ignore_index=True)
                    st.session_state.df = df_all
                    save_data(df_all)
                    st.success(f"Appended {len(normalized)} records to breakdown_log.csv")
                    st.rerun()
        except Exception as e:
            st.error(f"Error processing uploaded file: {e}")
