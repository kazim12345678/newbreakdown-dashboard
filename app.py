import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_plotly_events import plotly_events

st.set_page_config(layout="wide", page_title="Machine Breakdown Dashboard")

# --- Helper functions -------------------------------------------------------
def load_data(uploaded_file):
    if uploaded_file is None:
        return None
    # try excel first, then csv
    try:
        df = pd.read_excel(uploaded_file, engine="openpyxl")
    except Exception:
        uploaded_file.seek(0)
        df = pd.read_csv(uploaded_file)
    return df

def normalize_columns(df):
    # Normalize column names to simple keys used in code
    cols = {c.strip().lower(): c for c in df.columns}
    # common names mapping (adjust if your sheet uses different names)
    mapping = {}
    if 'machine' in cols:
        mapping[cols['machine']] = 'Machine'
    if 'type' in cols:
        mapping[cols['type']] = 'Type'
    if 'time consumed' in cols:
        mapping[cols['time consumed']] = 'TimeConsumed'
    if 'date' in cols:
        mapping[cols['date']] = 'Date'
    # rename
    df = df.rename(columns=mapping)
    return df

def parse_time_consumed(df):
    # Accept formats like "0:25:00" or Excel time floats
    if 'TimeConsumed' not in df.columns:
        df['TimeConsumed_min'] = 0
        return df
    s = df['TimeConsumed']
    # If already timedelta-like strings
    def to_minutes(x):
        if pd.isna(x):
            return 0
        # if Excel float (fraction of day)
        if isinstance(x, (int, float)):
            return float(x) * 24 * 60
        # if string like "0:25:00" or "0:25"
        try:
            td = pd.to_timedelta(x)
            return td.total_seconds() / 60.0
        except Exception:
            # fallback: try parse HH:MM or MM:SS
            try:
                parts = str(x).split(':')
                parts = [float(p) for p in parts]
                if len(parts) == 3:
                    return parts[0]*60 + parts[1] + parts[2]/60.0
                if len(parts) == 2:
                    return parts[0]*60 + parts[1]
            except Exception:
                return 0
    df['TimeConsumed_min'] = df['TimeConsumed'].apply(to_minutes)
    return df

def ensure_machines(df, machines):
    # ensure all machines M1..M18 exist in the index for plotting
    agg = df.groupby(['Machine','Type'], dropna=False)['TimeConsumed_min'].sum().reset_index()
    # create full index
    full = []
    for m in machines:
        for t in agg['Type'].unique():
            full.append({'Machine': m, 'Type': t, 'TimeConsumed_min': 0})
    full_df = pd.DataFrame(full)
    merged = pd.merge(full_df, agg, on=['Machine','Type'], how='left', suffixes=('_fill',''))
    merged['TimeConsumed_min'] = merged['TimeConsumed_min'].fillna(0)
    return merged

# --- UI: file upload and options --------------------------------------------
st.title("Machine Real‑time Breakdown — M1 to M18")

col1, col2 = st.columns([1, 3])
with col1:
    st.markdown("**Upload maintenance log (Excel or CSV)**")
    uploaded = st.file_uploader("Choose file", type=['xlsx','xls','csv'])
    st.markdown("**Or** use sample data below to test.")
    use_sample = st.checkbox("Use sample data (no upload)", value=False)

with col2:
    st.markdown("**Chart controls**")
    chart_height = st.slider("Chart height (px)", 300, 1200, 420)
    show_legend = st.checkbox("Show legend", value=True)

# --- Sample data (for testing) ------------------------------------------------
if use_sample and uploaded is None:
    sample = {
        'Date': ['2025-02-06','2025-02-06','2025-02-06','2025-02-07'],
        'Machine': ['M6','M4','M4','M1'],
        'Type': ['Mech','Mech','Mech','Elec'],
        'TimeConsumed': ['0:25:00','0:25:00','0:25:00','0:45:00'],
        'Reported Problem': ['Reduced steam','Clapper issue','Clapper replaced','Power trip'],
        'Notification': [101077474,101077728,101077729,101077800]
    }
    df = pd.DataFrame(sample)
else:
    df = load_data(uploaded)

if df is None:
    st.info("Upload a file or enable sample data to see the dashboard.")
    st.stop()

# --- Normalize and parse -----------------------------------------------------
df = normalize_columns(df)
df = parse_time_consumed(df)

# ensure Machine column is string and trimmed
df['Machine'] = df['Machine'].astype(str).str.strip().str.upper()

# define machines M1..M18 in order
machines = [f"M{i}" for i in range(1,19)]

# aggregate
agg = df.groupby(['Machine','Type'], dropna=False)['TimeConsumed_min'].sum().reset_index()

# ensure all machines present (so chart shows M1..M18 even if zero)
# but keep only types present in data
types_present = agg['Type'].dropna().unique().tolist()
full = ensure_machines(df, machines)

# pivot for plotting
pivot = full.pivot(index='Machine', columns='Type', values='TimeConsumed_min').reindex(machines).fillna(0)
pivot = pivot.reset_index().melt(id_vars='Machine', var_name='Type', value_name='Minutes')

# color mapping (adjust names to match your Type values)
color_map = {}
# common type names mapping
color_map.update({'Elec':'#e74c3c', 'Electrical':'#e74c3c', 'ELEC':'#e74c3c'})
color_map.update({'Mech':'#2b7bd3', 'Mechanical':'#2b7bd3', 'MECH':'#2b7bd3'})
color_map.update({'Auto':'#27ae60', 'Automation':'#27ae60', 'AUTO':'#27ae60'})

# fallback color palette
default_colors = px.colors.qualitative.Plotly

# assign color per Type in the pivot
unique_types = pivot['Type'].unique().tolist()
type_colors = []
for t in unique_types:
    c = color_map.get(t, None)
    if c is None:
        # pick from default palette
        idx = abs(hash(str(t))) % len(default_colors)
        c = default_colors[idx]
    type_colors.append(c)

# --- Plotly stacked horizontal bar -------------------------------------------
fig = px.bar(
    pivot,
    x='Minutes',
    y='Machine',
    color='Type',
    orientation='h',
    color_discrete_map={t: color_map.get(t, default_colors[i % len(default_colors)]) for i,t in enumerate(unique_types)},
    category_orders={'Machine': machines},
    labels={'Minutes':'Minutes', 'Machine':'Machine'}
)
fig.update_layout(barmode='stack', height=chart_height, legend=dict(orientation="h" if show_legend else "v"))
fig.update_yaxes(autorange="reversed")  # keep M1 at top if desired

# remove margins for compact look
fig.update_layout(margin=dict(l=60, r=20, t=30, b=30))

# --- Render chart and capture clicks ----------------------------------------
st.markdown("### Breakdown bar (click a bar segment to select a machine)")
# Use plotly_events to capture clicks
selected_points = plotly_events(fig, click_event=True, hover_event=False, key="plot1")

selected_machine = None
if selected_points:
    # plotly_events returns list of dicts; 'y' is machine name for horizontal bars
    pt = selected_points[0]
    # some versions return 'y' or 'label' depending on event; handle both
    selected_machine = pt.get('y') or pt.get('label') or pt.get('x')
    # normalize
    if isinstance(selected_machine, str):
        selected_machine = selected_machine.strip().upper()

# fallback: allow selection via selectbox
st.sidebar.markdown("**Select machine (fallback)**")
machine_choice = st.sidebar.selectbox("Machine", options=["-- none --"] + machines, index=0)
if selected_machine is None and machine_choice != "-- none --":
    selected_machine = machine_choice

# --- Summary area ------------------------------------------------------------
st.markdown("---")
st.markdown("### Selected machine summary")
if selected_machine is None:
    st.info("Click a machine bar segment or choose a machine from the sidebar to see details.")
else:
    st.markdown(f"**Selected Machine:** {selected_machine}")

    # totals by type for the selected machine
    totals = df[df['Machine'] == selected_machine].groupby('Type', dropna=False)['TimeConsumed_min'].sum().reset_index()
    # ensure all types shown
    for t in unique_types:
        if t not in totals['Type'].values:
            totals = totals.append({'Type': t, 'TimeConsumed_min': 0}, ignore_index=True)

    # show small metric cards
    cols = st.columns(len(totals))
    for i, row in totals.iterrows():
        typ = str(row['Type'])
        mins = float(row['TimeConsumed_min'])
        hrs = mins / 60.0
        color = color_map.get(typ, default_colors[i % len(default_colors)])
        with cols[i]:
            st.markdown(f"**{typ}**")
            st.metric(label="Minutes", value=f"{mins:.1f}")
            st.markdown(f"<div style='width:100%;height:8px;background:{color};border-radius:4px'></div>", unsafe_allow_html=True)

    # show filtered rows (full details)
    st.markdown("#### Matching log entries")
    filtered = df[df['Machine'] == selected_machine].copy()
    if filtered.empty:
        st.write("No log entries for this machine.")
    else:
        # show relevant columns and nice formatting
        display_cols = [c for c in ['Date','Notification','Area','Machine','Type','Reported Problem','TimeConsumed','TimeConsumed_min'] if c in filtered.columns]
        st.dataframe(filtered[display_cols].sort_values(by='Date', ascending=False), use_container_width=True)

# --- Footer / tips -----------------------------------------------------------
st.markdown("---")
st.caption("Tip: If clicks don't register in your environment, use the sidebar machine selector as a fallback.")
