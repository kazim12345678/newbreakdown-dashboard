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
    if "last_refresh" not in st.session_state:
        st.session_state.last_refresh = datetime.now()
    if "view_mode" not in st.session_state:
        st.session_state.view_mode = "MTD"

def auto_refresh_block():
    refresh_interval = 60  # seconds
    elapsed = (datetime.now() - st.session_state.last_refresh).total_seconds()
    remaining = max(0, refresh_interval - int(elapsed))
    if elapsed >= refresh_interval:
        st.session_state.last_refresh = datetime.now()
        st.experimental_rerun()
    return remaining

# =========================
# TICKER TEXT BUILDER
# =========================
def build_ticker_text(df):
    if df.empty:
        return "KUTE ONLINE – Awaiting breakdown data..."
    avg_mttr = df["MTTR"].mean()
    avg_mtbf = df["MTBF"].mean()
    worst = df.sort_values("MTTR", ascending=False).iloc[0]
    solved = df["ComplSolved"].sum()
    total = df["ComplTotal"].sum()
    return (
        f"<span class='ticker-highlight'>{worst['Code']}</span>: Mechanical Failure – "
        f"MTTR <span class='ticker-metric'>{worst['MTTR']:.1f}m</span> | "
        f"Avg MTBF: <span class='ticker-metric'>{avg_mtbf:.1f}m</span> | "
        f"Complaints Resolved: <span class='ticker-metric'>{solved}/{total}</span> | "
        f"KUTE Live Monitoring – PE/OE/OU updating every 60s."
    )

# =========================
# SEGMENT BAR HTML
# =========================
def render_segment_bar(row):
    prod = max(row["ProdPct"], 0)
    bd = max(row["BdPct"], 0)
    rep = max(row["RepPct"], 0)
    rem = max(row["RemPct"], 0)
    total = prod + bd + rep + rem
    if total == 0:
        prod = 100
        bd = rep = rem = 0
        total = 100
    prod_w = prod / total * 100
    bd_w = bd / total * 100
    rep_w = rep / total * 100
    rem_w = rem / total * 100
    html = f"""
    <div class="kute-segment-bar">
        <div class="seg-prod" style="width:{prod_w}%;"></div>
        <div class="seg-bd" style="width:{bd_w}%;"></div>
        <div class="seg-rep" style="width:{rep_w}%;"></div>
        <div class="seg-rem" style="width:{rem_w}%;"></div>
    </div>
    """
    return html

def render_complaints_bar(row):
    solved = row["ComplSolved"]
    total = max(row["ComplTotal"], 1)
    pct = solved / total * 100
    html = f"""
    <div class="kute-complaints">
        {solved}/{total}
        <div class="kute-complaints-bar">
            <div class="kute-complaints-fill" style="width:{pct}%;"></div>
        </div>
    </div>
    """
    return html

# =========================
# MAIN APP
# =========================
ensure_session_state()
remaining = auto_refresh_block()
now = datetime.now()
df = st.session_state.df

# HEADER
col_header = st.container()
with col_header:
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown(
            f"""
            <div class="kute-header">
                <div class="kute-header-left">
                    <div class="kute-title">KUTE: Kazim Utilization Team Efficiency</div>
                    <div class="kute-subtitle">Real-time industrial monitoring – PE / OE / OU / MTTR / MTBF</div>
                </div>
                <div class="kute-header-right">
                    <div class="kute-clock">🕒 {now.strftime("%Y-%m-%d %H:%M:%S")}</div>
                    <div class="kute-timer">⏱ Refresh in: {remaining:02d}s</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        c1, c2, c3, c4 = st.columns([1.2, 1, 1, 1.2])
        with c1:
            upload_clicked = st.button("UPLOAD DATA", use_container_width=True)
        with c2:
            save_clicked = st.button("SAVE", use_container_width=True)
        with c3:
            history_clicked = st.button("HISTORY CARD", use_container_width=True)
        with c4:
            mode = st.toggle("MTD / DTM", value=(st.session_state.view_mode == "MTD"))
            st.session_state.view_mode = "MTD" if mode else "DTM"

# UPLOAD HANDLER
if upload_clicked:
    uploaded = st.file_uploader("Upload CSV data for KUTE", type=["csv"], key="kute_uploader")
    if uploaded is not None:
        try:
            data = uploaded.read().decode("utf-8")
            df_new = pd.read_csv(StringIO(data))
            st.session_state.df = df_new
            df = df_new
            st.success("Data uploaded and loaded into KUTE.")
        except Exception as e:
            st.error(f"Error reading uploaded file: {e}")

# SAVE HANDLER (mock)
if save_clicked:
    st.success("SAVE triggered – in real deployment, persist to database or storage.")

# HISTORY CARD
if history_clicked:
    avg_pe = df["PE"].mean()
    avg_oe = df["OE"].mean()
    avg_ou = df["OU"].mean()
    avg_mttr = df["MTTR"].mean()
    avg_mtbf = df["MTBF"].mean()
    st.info(
        f"History Snapshot – Avg PE: {avg_pe:.1f}%, OE: {avg_oe:.1f}%, OU: {avg_ou:.1f}%, "
        f"MTTR: {avg_mttr:.1f}m, MTBF: {avg_mtbf:.1f}m"
    )

# TICKER
ticker_html = build_ticker_text(df)
st.markdown(
    f"""
    <div class="ticker-container">
        <div class="ticker-text">{ticker_html}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("")

# EDITABLE DATA
edit_mode = st.checkbox("Edit KUTE Data (st.data_editor)", value=False)
if edit_mode:
    edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")
    st.session_state.df = edited_df
    df = edited_df

# MAIN TABLE
st.markdown("### Line Monitoring Overview")

table_html = """
<table class="kute-table">
    <thead>
        <tr>
            <th>Machine / Code / Shift</th>
            <th>Live Progress</th>
            <th>PE %</th>
            <th>OE %</th>
            <th>OU %</th>
            <th>PR-Pcs</th>
            <th>TA-Mins</th>
            <th>MTTR</th>
            <th>MTBF</th>
            <th>Complaints</th>
        </tr>
    </thead>
    <tbody>
"""

for _, row in df.iterrows():
    identity_html = f"""
    <div class="kute-machine-name">{row['Machine']}</div>
    <div class="kute-machine-code">{row['Code']}</div>
    <div class="kute-shift">{row['ShiftStart']} - {row['ShiftEnd']}</div>
    """
    seg_html = render_segment_bar(row)
    compl_html = render_complaints_bar(row)
    table_html += f"""
    <tr class="kute-row">
        <td class="kute-identity">{identity_html}</td>
        <td>{seg_html}</td>
        <td class="kute-eff">{row['PE']:.1f}</td>
        <td class="kute-eff">{row['OE']:.1f}</td>
        <td class="kute-eff">{row['OU']:.1f}</td>
        <td>{int(row['PR_Pcs'])}</td>
        <td>{int(row['TA_Mins'])}</td>
        <td>{row['MTTR']:.1f}</td>
        <td>{row['MTBF']:.1f}</td>
        <td>{compl_html}</td>
    </tr>
    """

table_html += "</tbody></table>"

st.markdown(table_html, unsafe_allow_html=True)

st.markdown(
    """
    <div style="margin-top:0.4rem; font-size:0.7rem; color:#9ca3af;">
        <b>Legend:</b>
        <span style="color:#059669; font-weight:600;">■ Production</span> |
        <span style="color:#e11d48; font-weight:600;">■ Breakdown</span> |
        <span style="color:#f97316; font-weight:600;">■ Repair</span> |
        <span style="color:#eab308; font-weight:600;">■ Remaining</span>
    </div>
    """,
    unsafe_allow_html=True,
)
