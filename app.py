import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
from datetime import datetime, date, time, timedelta
from streamlit_autorefresh import st_autorefresh
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
    "Date","Machine No","Shift","Machine Classification","Job Type",
    "Breakdown Category","Reported Problem","Description of Work",
    "Start Time","End Time","Time Consumed","Technician / Performed By","Status"
]

CATEGORY_COLORS = {
    "Mechanical": "red",
    "Electrical": "blue",
    "Automation": "green",
}

# =========================
# STORAGE
# =========================
def init_storage():
    if not os.path.exists(CSV_PATH):
        df = pd.DataFrame(columns=REQUIRED_COLUMNS)
        df.to_csv(CSV_PATH, index=False)

def load_data():
    init_storage()
    df = pd.read_csv(CSV_PATH)

    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            df[col] = np.nan

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.date
    df["Start Time"] = pd.to_datetime(df["Start Time"], errors="coerce").dt.time
    df["End Time"] = pd.to_datetime(df["End Time"], errors="coerce").dt.time
    df["Time Consumed"] = pd.to_numeric(df["Time Consumed"], errors="coerce")

    return df

def save_data(df):
    df.to_csv(CSV_PATH, index=False)

def ensure_session_state():
    if "df" not in st.session_state:
        st.session_state.df = load_data()
    if "last_refresh" not in st.session_state:
        st.session_state.last_refresh = datetime.now()

# =========================
# TIME UTILS
# =========================
def parse_time_str(t):
    if isinstance(t, time):
        return t
    if pd.isna(t):
        return None
    for fmt in ("%H:%M", "%H:%M:%S", "%I:%M %p"):
        try:
            return datetime.strptime(str(t), fmt).time()
        except:
            pass
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
    return (dt_end - dt_start).total_seconds() / 60

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
    return tt.hour if tt else np.nan

# =========================
# FILTER UTILS
# =========================
def filter_data(df, date_range, machines, category, tech, job_type):
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.date

    if date_range:
        start, end = date_range
        df = df[(df["Date"] >= start) & (df["Date"] <= end)]
    if machines:
        df = df[df["Machine No"].isin(machines)]
    if category != "All":
        df = df[df["Breakdown Category"] == category]
    if tech:
        df = df[df["Technician / Performed By"].astype(str).str.contains(tech, case=False, na=False)]
    if job_type != "All":
        df = df[df["Job Type"] == job_type]

    return df

# =========================
# EXPORT UTILS
# =========================
def export_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False)
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

        c.setFont("Helvetica-Bold", 14)
        c.drawString(x_margin, y, "KUTE – Maintenance Breakdown Report")
        y -= 1 * cm

        c.setFont("Helvetica", 8)
        cols = ["Date","Machine No","Shift","Job Type","Breakdown Category",
                "Reported Problem","Time Consumed","Technician / Performed By","Status"]
        col_widths = [2,1.5,1.5,2,2,5,2,3,2]

        x = x_margin
        for col, w in zip(cols, col_widths):
            c.drawString(x, y, col)
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

        c.save()
        pdf = buffer.getvalue()
        buffer.close()
        return pdf, None
    except Exception as e:
        return None, str(e)

# =========================
# AUTO REFRESH
# =========================
def auto_refresh_block():
    refresh_interval = 120
    elapsed = (datetime.now() - st.session_state.last_refresh).total_seconds()
    remaining = max(0, refresh_interval - int(elapsed))

    col1, col2 = st.columns([3,1])
    with col1:
        st.caption("Dashboard auto-refreshes every 2 minutes.")
    with col2:
        st.metric("Next refresh (sec)", remaining)

    if elapsed >= refresh_interval:
        st.session_state.last_refresh = datetime.now()

st_autorefresh(interval=120000, key="kute_refresh")
