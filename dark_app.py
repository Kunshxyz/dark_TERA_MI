import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# TERA 2.0 - MIDNIGHT INTELLIGENCE EDITION
# Same six-tab dashboard; live charts are driven by the sliders.
# ============================================================

st.set_page_config(
    page_title="TERA 2.0 | Midnight Intelligence",
    page_icon="🌍",
    layout="wide",
)

BG, PANEL, ALT = "#07111F", "#0D1B2A", "#102338"
CYAN, MINT, TEXT, MUTED, BORDER = "#38D6E8", "#63F2C2", "#E7F1FA", "#9CB0C5", "#1D3850"
COLORS = {
    "CRITICAL": "#FF5C70",
    "HIGH": "#FFB454",
    "MODERATE": "#F5D76E",
    "LOWER": "#63D9A5",
}
FACTORS = ["Hazard", "Vulnerability", "Population", "Exposure", "Urgency"]
DEFAULT_WEIGHTS = {
    "Hazard": 30,
    "Vulnerability": 25,
    "Population": 20,
    "Exposure": 15,
    "Urgency": 10,
}
DEFAULT_ZONES = {
    "Forest": [72, 65, 35, 95, 75],
    "Residential Area": [80, 85, 95, 45, 90],
    "Hospital": [75, 90, 90, 30, 95],
    "Smart Farm": [60, 65, 45, 75, 60],
    "River & Dam": [85, 75, 70, 85, 85],
    "Industrial Zone": [82, 70, 75, 65, 80],
}
FACTOR_COLORS = ["#38D6E8", "#63F2C2", "#8A9CFF", "#FFB454", "#E78BFF"]
PRIORITY_ORDER = ["CRITICAL", "HIGH", "MODERATE", "LOWER"]

# Plotly's editable mode lets users adjust chart text/annotations in the chart UI.
# The underlying values remain controlled by the sliders, so every rerun stays
# consistent with the model data.
PLOT_CONFIG = {
    "displayModeBar": True,
    "displaylogo": False,
    "editable": True,
    "toImageButtonOptions": {"format": "png", "filename": "TERA_chart", "scale": 2},
}

# -------------------- DARK THEME + TABLE FIX --------------------
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: Manrope, sans-serif;
        color: {TEXT};
    }}
    .stApp {{
        background: radial-gradient(circle at 15% 0%, #10283A 0%, {BG} 42%);
        color: {TEXT};
    }}
    [data-testid="stHeader"] {{
        background: rgba(7,17,31,.92);
    }}
    [data-testid="stSidebar"] {{
        background: #091725;
        border-right: 1px solid {BORDER};
    }}
    [data-testid="stSidebar"] * {{
        color: {TEXT};
    }}
    h1, h2, h3, h4, p, label, .stMarkdown, [data-testid="stCaptionContainer"] {{
        color: {TEXT};
    }}
    [data-testid="stMetric"] {{
        background: linear-gradient(145deg, {ALT}, {PANEL});
        border: 1px solid {BORDER};
        padding: 15px 18px;
        border-radius: 16px;
    }}
    [data-testid="stMetricLabel"] {{
        color: {MUTED} !important;
    }}
    [data-testid="stMetricValue"] {{
        color: {TEXT} !important;
    }}
    div[data-testid="stTabs"] button {{
        color: {MUTED};
        font-weight: 700;
    }}
