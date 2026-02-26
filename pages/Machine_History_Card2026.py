# pages/02_Machine_History.py
# ---------------------------------------------------------
# Machine History page (M1..M18 buttons)
# - Reads history from:
#   1) Uploaded DOCX/TXT
#   2) Repo file path (e.g., data/report.docx)
#   3) Optional: your own dict in st.session_state["machine_history_dict"]
# - Shows formatted + raw (word-by-word) view
# ---------------------------------------------------------

import re
from io import BytesIO
from pathlib import Path

import streamlit as st

# Optional DOCX support
try:
    from docx import Document
except Exception:
    Document = None


st.set_page_config(page_title="Machine History", layout="wide")

MACHINES = [f"M{i}" for i in range(1, 19)]
SPECIAL = ["CRATES AREA / LINE"]
ALL_KEYS = SPECIAL + MACHINES

# --------- Heading detection (matches your report style) ----------
HEADER_PATTERNS = [
    re.compile(r"^CRATES\s+AREA\s*/\s*LINE\s*[–-]\s*MACHINE\s+HISTORY", re.IGNORECASE),
    re.compile(r"^(M\d{1,2})\s*[–-]\s*MACHINE\s+HISTORY", re.IGNORECASE),
    re.compile(r"^(M\d{1,2})\s*[–-]\s*MACHINE\s+HISTORY\s*\(Technical\s+Summary\)", re.IGNORECASE),
]

BULLET_PREFIXES = ("•", "-", "–")


def _is_header(line: str):
    s = line.strip()
    if not s:
        return False, None

    # CRATES
    if HEADER_PATTERNS[0].match(s) or (s.upper().startswith("CRATES AREA / LINE") and "MACHINE HISTORY" in s.upper()):
        return True, "CRATES AREA / LINE"

    # M1..M18
    m = HEADER_PATTERNS[1].match(s)
    if m:
        return True, m.group(1).upper()

    # Mx .. (Technical Summary)
    m = HEADER_PATTERNS[2].match(s)
    if m:
        return True, m.group(1).upper()

    return False, None


def parse_lines_to_sections(lines):
    """
    Returns dict: { 'M1': [lines...], 'M2': [...], ... }
    Keeps wording as-is (word-by-word). Only strips empty lines.
    """
    sections = {k: [] for k in ALL_KEYS}
    current = None

    for raw in lines:
        line = raw.rstrip("\n")
        is_h, key = _is_header(line)

        if is_h:
            current = key
            sections[current].append(line.strip())  # keep header line
            continue

        if current is None:
            # ignore preamble until first machine header appears
            continue

        if not line.strip():
            continue

        sections[current].append(line)

    # remove empty
    sections = {k: v for k, v in sections.items() if v}
    return sections


def parse_docx(file_bytes: bytes):
    if Document is None:
        raise RuntimeError("python-docx is not installed. Add python-docx to your requirements.")
    doc = Document(BytesIO(file_bytes))
    lines = []
    for p in doc.paragraphs:
        t = (p.text or "").strip()
        if t:
            lines.append(t)
    return parse_lines_to_sections(lines)


def parse_text(text: str):
    lines = [ln for ln in text.splitlines() if ln.strip()]
    return parse_lines_to_sections(lines)


def format_for_display(lines):
    """
    Converts '• blah' into markdown bullets, keeps other lines as text.
    """
    formatted = []
    for ln in lines:
        s = ln.strip()
        if s.startswith("•"):
            formatted.append(("bullet", s.lstrip("•").strip()))
        elif s.startswith("-") or s.startswith("–"):
            formatted.append(("bullet", s.lstrip("-–").strip()))
        else:
            formatted.append(("text", ln))
    return formatted


# ---------------- UI ----------------
st.title("Machine History (M1–M18)")
st.caption("Click a machine button to view its history. Wording is preserved; only display formatting changes.")

left, right = st.columns([1, 3], gap="large")

with left:
    st.subheader("Load Data")

    # Option A: If your main app already loads data into session_state, use it
    use_session = st.checkbox("Use st.session_state['machine_history_dict'] (if available)", value=True)

    uploaded = st.file_uploader("Upload DOCX/TXT (optional)", type=["docx", "txt", "md"])

    repo_path = st.text_input("Or load from repo path", value="data/report.docx")
    load_repo = st.button("Load from repo")

    st.divider()
    st.subheader("Machines")

    if "selected_machine" not in st.session_state:
        st.session_state.selected_machine = "M1"

    # CRATES button
    if st.button("CRATES AREA / LINE", use_container_width=True):
        st.session_state.selected_machine = "CRATES AREA / LINE"

    # Buttons grid for M1..M18
    cols = st.columns(3)
    for idx, m in enumerate(MACHINES):
        with cols[idx % 3]:
            if st.button(m, use_container_width=True):
                st.session_state.selected_machine = m

    st.info(f"Selected: **{st.session_state.selected_machine}**")


with right:
    st.subheader("History Viewer")

    sections = None
    err = None

    # 1) Session dict
    if use_session and isinstance(st.session_state.get("machine_history_dict"), dict):
        # expected format: { "M1": ["line1","line2"...], ... }
        sections = st.session_state["machine_history_dict"]

    # 2) Uploaded file
    elif uploaded is not None:
        try:
            if uploaded.name.lower().endswith(".docx"):
                sections = parse_docx(uploaded.getvalue())
            else:
                sections = parse_text(uploaded.getvalue().decode("utf-8", errors="replace"))
        except Exception as e:
            err = str(e)

    # 3) Repo file path
    elif load_repo:
        try:
            p = Path(repo_path)
            if not p.exists():
                raise FileNotFoundError(f"File not found: {p}")
            if p.suffix.lower() == ".docx":
                sections = parse_docx(p.read_bytes())
            else:
                sections = parse_text(p.read_text(encoding="utf-8", errors="replace"))
        except Exception as e:
            err = str(e)

    if err:
        st.error(err)
        st.stop()

    if sections is None:
        st.warning("Load data first (session_state dict, upload file, or repo path).")
        st.stop()

    key = st.session_state.selected_machine

    if key not in sections:
        st.warning(f"No section found for {key}.")
        st.write("Detected keys:", list(sections.keys()))
        st.stop()

    lines = sections[key]
    formatted = format_for_display(lines)

    st.markdown("### Formatted view")
    for kind, val in formatted:
        if kind == "bullet":
            st.markdown(f"- {val}")
        else:
            st.write(val)

    st.divider()
    st.markdown("### Raw view (word-by-word)")
    st.code("\n".join(lines), language="text")

    st.download_button(
        label=f"Download {key} as TXT",
        data="\n".join(lines).encode("utf-8"),
        file_name=f"{key.replace(' / ', '_').replace(' ', '_')}_history.txt",
        mime="text/plain",
    )
