import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from io import StringIO

# =========================
# BASIC CONFIG
# =========================
st.set_page_config(
    page_title="KUTE: Kazim Utilization Team Efficiency",
    layout="wide",
)

# =========================
# CSS STYLING
# =========================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }
    .kute-header {
        background: #0f172a;
        padding: 0.6rem 1rem;
        border-radius: 0.5rem;
        color: #e5e7eb;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .kute-header-left {
        display: flex;
        flex-direction: column;
    }
    .kute-title {
        font-size: 1.1rem;
        font-weight: 700;
        letter-spacing: 0.04em;
    }
    .kute-subtitle {
        font-size: 0.75rem;
        color: #9ca3af;
    }
    .kute-header-right {
        display: flex;
        gap: 1rem;
        align-items: center;
        font-size: 0.8rem;
    }
    .kute-clock {
        font-weight: 600;
        color: #e5e7eb;
    }
    .kute-timer {
        font-weight: 600;
        color: #facc15;
    }
    .ticker-container {
        margin-top: 0.4rem;
        background: #020617;
        border-radius: 0.4rem;
        padding: 0.25rem 0.6rem;
        overflow: hidden;
        border: 1px solid #1f2937;
    }
    .ticker-text {
        display: inline-block;
        white-space: nowrap;
        animation: ticker 25s linear infinite;
        font-size: 0.78rem;
        color: #e5e7eb;
    }
    @keyframes ticker {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
    .ticker-highlight {
        color: #f97316;
        font-weight: 600;
    }
    .ticker-metric {
        color: #22c55e;
        font-weight: 600;
    }
    .kute-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 0.6rem;
        font-size: 0.78rem;
    }
    .kute-table thead {
        background: #020617;
        position: sticky;
        top: 0;
        z-index: 1;
    }
    .kute-table th {
        padding: 0.4rem 0.35rem;
        text-align: center;
        color: #e5e7eb;
        border-bottom: 1px solid #1f2937;
        border-right: 1px solid #111827;
        font-weight: 600;
        white-space: nowrap;
    }
    .kute-table td {
        padding: 0.35rem 0.35rem;
        border-bottom: 1px solid #111827;
        border-right: 1px solid #020617;
        color: #e5e7eb;
        text-align: center;
    }
    .kute-row {
        background: #020617;
    }
    .kute-row:hover {
        background: #111827;
    }
    .kute-identity {
        text-align: left;
    }
    .kute-machine-name {
        font-weight: 600;
        color: #e5e7eb;
    }
    .kute-machine-code {
        font-size: 0.7rem;
        color: #9ca3af;
    }
    .kute-shift {
        font-size: 0.7rem;
        color: #38bdf8;
    }
    .kute-segment-bar {
        display: flex;
        width: 100%;
        height: 12px;
        border-radius: 999px;
        overflow: hidden;
        background: #020617;
        border: 1px solid #1f2937;
    }
    .seg-prod { background: #059669; }
    .seg-bd { background: #e11d48; }
    .seg-rep { background: #f97316; }
    .seg-rem { background: #eab308; }
    .kute-eff {
        font-weight: 700;
    }
    .kute-complaints {
        font-size: 0.7rem;
    }
    .kute-complaints-bar {
        width: 100%;
        height: 6px;
        border-radius: 999px;
        overflow: hidden;
        background: #020617;
        border: 1px solid #1f2937;
        margin-top: 2px;
    }
    .kute-complaints-fill {
        height: 100%;
        background: #22c55e;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================
# MOCK DATA GENERATOR
# =========================
def generate_mock_data():
    np.random.seed(42)
    machines = [f"M{i:02d}" for i in range(1, 13)]
    rows = []
    now = datetime.now()
    for m in machines:
        code = f"KUTE-{int(m[1:]):02d}"
        shift_start = now.replace(hour=6, minute=0, second=0, microsecond=0)
        shift_end = now.replace(hour=18, minute=0, second=0, microsecond=0)
        prod = np.random.randint(60, 85)
        bd = np.random.randint(5, 20)
        rep = np.random.randint(5, 15)
        rem = max(0, 100 - (prod + bd + rep))
        pe = np.random.uniform(80, 98)
        oe = np.random.uniform(75, 95)
        ou = np.random.uniform(70, 98)
        pr_pcs = np.random.randint(18000, 42000)
        ta_mins = 720
        failures = np.random.randint(1, 6)
        total_bd_mins = int(ta_mins * (bd / 100))
        mttr = total_bd_mins / failures
        mtbf = (ta_mins - total_bd_mins) / failures
        solved = np.random.randint(3, 10)
        total_comp = solved + np.random.randint(0, 5)
        rows.append(
            {
                "Machine": m,
                "Code": code,
                "ShiftStart": shift_start.strftime("%H:%M"),
                "ShiftEnd": shift_end.strftime("%H:%M"),
                "ProdPct": prod,
                "BdPct": bd,
                "RepPct": rep,
                "RemPct": rem,
                "PE": round(pe, 1),
                "OE": round(oe, 1),
                "OU": round(ou, 1),
                "PR_Pcs": pr_pcs,
                "TA_Mins": ta_mins,
                "MTTR": round(mttr, 1),
                "MTBF": round(mtbf, 1),
                "ComplSolved": solved,
                "ComplTotal": total_comp,
            }
        )
    return pd.DataFrame(rows)

# =========================
# SESSION & AUTO REFRESH
# =========================
def ensure_session_state():
    if "df" not in st.session_state:
        st.session_state.df = generate_mock_data()
    if "last_refresh" not in st.session
