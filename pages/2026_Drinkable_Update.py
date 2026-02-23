import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# ----------------- PAGE CONFIG -----------------
st.set_page_config(page_title="2026 – Drinkable Section Current Update", layout="wide")
st.title("2026 – Drinkable Section Current Update")

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "maintenance_data.xlsx")


# ----------------- SAFE HELPERS -----------------

def safe_col(df, col, default=""):
    """Return a column safely. If missing, return empty column."""
    if col in df.columns:
        return df[col]
    return pd.Series([default] * len(df))


def safe_time(series):
    """Convert Excel float time or text to datetime safely."""
    # Excel float time → convert to datetime
    if series.dtype in ["float64", "int64"]:
        return pd.to_datetime(series, unit="D", origin="1899-12-30", errors="coerce")
    return pd.to_datetime(series, errors="coerce")


def safe_timedelta(series):
    """Convert Excel float time or text to timedelta safely."""
    if series.dtype in ["float64", "int64"]:
        return pd.to_timedelta(series, unit="D", errors="coerce").fillna(pd.Timedelta(0))
    td = pd.to_timedelta(series, errors="coerce")
    return td.fillna(pd.Timedelta(0))


# ----------------- CLEANING -----------------

def clean_data(df):
    df.columns = [c.strip() for c in df.columns]

    # Date (Excel float → real date)
    df["Date"] = safe_time(safe_col(df, "Date"))

    # Time fields (Excel float → real time)
    df["Requested Time"] = safe_time(safe_col(df, "Requested Time"))
    df["Start"] = safe_time(safe_col(df, "Start"))
    df["End"] = safe_time(safe_col(df, "End"))

    # Time Consumed
