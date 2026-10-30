import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import StringIO
from datetime import datetime
import streamlit.components.v1 as components

# ============================================================
# TERA 2.0 — MIDNIGHT INTELLIGENCE EDITION
# Environmental Risk Analysis | Educational Prototype
# ============================================================

st.set_page_config(
    page_title="TERA 2.0 | Midnight Intelligence",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------- THEME --------------------

BG = "#070B14"
PANEL = "#0B1220"
HEADER = "#111C33"
BORDER = "#263B5A"
CYAN = "#00D9FF"
BLUE = "#448AFF"
PURPLE = "#A78BFA"
TEXT = "#F1F5FF"
MUTED = "#9DB0CE"
GREEN = "#38D996"
YELLOW = "#FFD166"
RED = "#FF5C75"

st.markdown(
    f"""
    <style>
    .stApp {{
        background: {BG};
        color: {TEXT};
    }}

    [data-testid="stSidebar"] {{
        background: #090F1C;
        border-right: 1px solid {BORDER};
    }}

    [data-testid="stHeader"] {{
        background: rgba(7, 11, 20, 0.95);
    }}

    h1, h2, h3 {{
        color: {TEXT} !important;
    }}

    p, label, li {{
        color: {TEXT};
    }}

    [data-testid="stMetric"] {{
        background: {PANEL};
        border: 1px solid {BORDER};
        border-radius: 14px;
        padding: 16px;
    }}

    [data-testid="stMetricLabel"] {{
        color: {MUTED} !important;
    }}

    [data-testid="stMetricValue"] {{
        color: {CYAN} !important;
    }}

    div[data-testid="stTabs"] button {{
        color: {MUTED};
        font-weight: 600;
    }}

    div[data-testid="stTabs"] button[aria-selected="true"] {{
        color: {CYAN} !important;
        border-bottom-color: {CYAN} !important;
    }}

    div.stButton > button {{
        background: linear-gradient(90deg, #12345A, #155E75);
        color: white;
        border: 1px solid {CYAN};
        border-radius: 9px;
        font-weight: 600;
    }}

    div.stButton > button:hover {{
        background: #164E63;
        color: white;
        border-color: white;
    }}

    div[data-testid="stDataFrame"],
    div[data-testid="stTable"] {{
        background: {PANEL};
        border: 1px solid {BORDER};
        border-radius: 12px;
        overflow: hidden;
    }}

    [data-testid="stDataFrame"] [data-testid="glideDataEditor"] {{
        --gdg-bg-cell: {PANEL};
        --gdg-bg-cell-medium: {HEADER};
        --gdg-bg-header: {HEADER};
        --gdg-text-dark: {TEXT};
        --gdg-text-medium: {MUTED};
        --gdg-text-light: {MUTED};
        --gdg-border-color: {BORDER};
        --gdg-accent-color: {CYAN};
    }}

    .hero {{
        padding: 26px;
        border-radius: 18px;
        border: 1px solid #155E75;
        background: linear-gradient(120deg, #0B1220 0%, #10243D 60%, #10102A 100%);
        margin-bottom: 18px;
    }}

    .hero-label {{
        color: {CYAN};
        font-size: 12px;
        letter-spacing: 3px;
        font-weight: 800;
    }}

    .hero-title {{
        color: {TEXT};
        font-size: clamp(28px, 4vw, 44px);
        font-weight: 900;
        line-height: 1.1;
        margin: 8px 0;
    }}

    .hero-subtitle {{
        color: {MUTED};
        font-size: 15px;
    }}

    .status-chip {{
        display: inline-block;
        color: {CYAN};
        border: 1px solid #155E75;
        background: #0A2533;
        border-radius: 20px;
        padding: 5px 10px;
        font-size: 12px;
        font-weight: 700;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------- DATA AND MODEL --------------------

FACTORS = ["Hazard", "Vulnerability", "Population", "Exposure", "Urgency"]
WEIGHTS = {"Hazard": 0.30, "Vulnerability": 0.25, "Population": 0.20, "Exposure": 0.15, "Urgency": 0.10}

if "zones_data" not in st.session_state:
    st.session_state.zones_data = {
        "Forest": [72, 65, 35, 95, 75],
        "Residential Area": [80, 85, 95, 45, 90],
        "Hospital": [75, 90, 90, 30, 95],
        "Smart Farm": [60, 65, 45, 75, 60],
        "River & Dam": [85, 75, 70, 85, 85],
        "Industrial Zone": [82, 70, 75, 65, 80],
    }

def calculate_risk(scores):
    return round(sum(scores[factor] * WEIGHTS[factor] for factor in FACTORS), 1)

def classify_risk(score):
    if score >= 80: return "CRITICAL"
    if score >= 65: return "HIGH"
    if score >= 45: return "MODERATE"
    return "LOWER"

def risk_color(level):
    return {"CRITICAL": RED, "HIGH": "#FF9F43", "MODERATE": YELLOW, "LOWER": GREEN}.get(level, CYAN)

def make_zone_dataframe():
    rows = []
    for zone, values in st.session_state.zones_data.items():
        scores = dict(zip(FACTORS, values))
        risk = calculate_risk(scores)
        rows.append({"Zone": zone, **scores, "Risk Index": risk, "Priority": classify_risk(risk)})
    return pd.DataFrame(rows).sort_values("Risk Index", ascending=False).reset_index(drop=True)

def style_table(df):
    styler = df.style.set_properties(**{"background-color": PANEL, "color": TEXT, "border-color": BORDER})
    if "Priority" in df.columns:
        styler = styler.map(lambda v: f"color: {risk_color(str(v))}; font-weight: bold;", subset=["Priority"])
    return styler

def show_table(df, height=300):
    st.dataframe(style_table(df), use_container_width=True, hide_index=True, height=height)

def style_plot(fig, height=360):
    fig.update_layout(height=height, paper_bgcolor=PANEL, plot_bgcolor=PANEL, font=dict(color=TEXT, family="Arial"), margin=dict(l=20, r=20, t=45, b=20), legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT)))
    return fig

def make_report(df):
    return f"TERA 2.0 REPORT\nGenerated: {datetime.now().strftime('%d %b %Y, %H:%M')}\n\n" + df.to_string(index=False)

# -------------------- HEADER --------------------
st.markdown("""
    <div class="hero">
        <div class="hero-label">TERA 2.0 • ENVIRONMENTAL INTELLIGENCE</div>
        <div class="hero-title">MIDNIGHT INTELLIGENCE</div>
        <div class="hero-subtitle">Technology for Environmental Risk Analysis · THE SIGNATURE EDITION</div>
        <br>
        <span class="status-chip">● SYSTEM ONLINE</span>   <span class="status-chip">RULE-BASED PROTOTYPE</span>
    </div>
    """, unsafe_allow_html=True)

df = make_zone_dataframe()

# -------------------- NAVIGATION TABS --------------------
tab_command, tab_zone, tab_compare, tab_scenario, tab_mission, tab_method, tab_eye = st.tabs([
    "⚡ Command Centre", "🛰️ Zone Intelligence", "📊 Compare Zones", "🧪 Scenario Lab", "🎯 Mission Control", "📘 Methodology", "🛰️ TERA-EYE"
])

with tab_command:
    st.subheader("Environmental Command Centre")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Zones Analysed", len(df))
    c2.metric("Average Risk Index", f"{round(df['Risk Index'].mean(), 1)}/100")
    c3.metric("Highest-Risk Zone", str(df.iloc[0]["Zone"]))
    c4.metric("High / Critical Zones", int(df["Priority"].isin(["HIGH", "CRITICAL"]).sum()))
    st.markdown("### Zone assessment table")
    show_table(df, 285)

with tab_zone:
    st.subheader("Zone Intelligence")
    selected_zone = st.selectbox("Select a zone", list(st.session_state.zones_data.keys()))
    vals = st.session_state.zones_data[selected_zone]
    st.metric("Risk Priority Index", f"{calculate_risk(dict(zip(FACTORS, vals)))}/100")

with tab_compare:
    st.subheader("Compare Zones")
    st.write("Compare zone factors side-by-side.")

with tab_scenario:
    st.subheader("Scenario Lab")
    st.write("Test hypothetical scenario adjustments.")

with tab_mission:
    st.subheader("Mission Control")
    st.write("Operational checklists and briefing exports.")

with tab_method:
    st.subheader("Methodology & Transparency")
    st.latex(r"R = 0.30H + 0.25V + 0.20P + 0.15E + 0.10U")

# ============================================================
# TAB 7 — TERA-EYE (ULTRA-REALISTIC TACTICAL VISION HUD)
# ============================================================
with tab_eye:
    components.html("""
    <div style="background:#070B14; color:#F1F5FF; font-family:'Segoe UI',sans-serif; padding:15px; border-radius:12px; border:1px solid #263B5A;">
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #263B5A; padding-bottom:10px; margin-bottom:15px;">
            <div>
                <div style="color:#00D9FF; font-size:10px; font-weight:800; letter-spacing:2px;">TERA 2.0 • PERCEPTION & INGESTION LAYER</div>
                <div style="font-size:20px; font-weight:900;">TERA-EYE // MULTI-SOURCE INGESTION & VISION ENGINE</div>
                <div style="font-size:11px; color:#9DB0CE;">Converts Drone Video, City CCTV & Citizen SOS Feeds into Normalized 0–100 TERA Risk Scores</div>
            </div>
            <div style="background:#0A2533; border:1px solid #155E75; color:#00D9FF; padding:6px 12px; border-radius:20px; font-size:11px; font-weight:bold;">● CV ENGINE ONLINE (60FPS)</div>
        </div>
        
        <div style="display:grid; grid-template-columns: 260px 1fr 280px; gap:15px;">
            <!-- Left Column: Presets -->
            <div style="background:#0B1220; border:1px solid #263B5A; padding:12px; border-radius:10px;">
                <div style="font-size:12px; font-weight:800; color:#00D9FF; margin-bottom:10px;">⚡ 1-CLICK LIVE CRISIS SIMULATIONS</div>
                <button onclick="setPreset('Smart Farm', 62, 48, 50, 78, 55)" style="width:100%; text-align:left; background:#111C33; color:#fff; border:1px solid #263B5A; padding:8px; border-radius:6px; margin-bottom:6px; cursor:pointer; font-size:11px;"><b>🌾 Smart Farm (Agro-Drone)</b><br><span style="color:#9DB0CE; font-size:9px;">Crop inundation & flash flood</span></button>
                <button onclick="setPreset('River & Dam', 88, 76, 72, 88, 86)" style="width:100%; text-align:left; background:#111C33; color:#fff; border:1px solid #263B5A; padding:8px; border-radius:6px; margin-bottom:6px; cursor:pointer; font-size:11px;"><b>🌊 River & Dam (Hydro-Cam)</b><br><span style="color:#9DB0CE; font-size:9px;">Dam floodgates cresting & river surge</span></button>
                <button onclick="setPreset('Forest', 92, 42, 32, 96, 78)" style="width:100%; text-align:left; background:#111C33; color:#fff; border:1px solid #263B5A; padding:8px; border-radius:6px; margin-bottom:6px; cursor:pointer; font-size:11px;"><b>🔥 Forest Zone (Thermal UAV)</b><br><span style="color:#9DB0CE; font-size:9px;">Active crown wildfire & wildlife displacement</span></button>
                <button onclick="setPreset('Industrial Zone', 84, 72, 78, 68, 82)" style="width:100%; text-align:left; background:#111C33; color:#fff; border:1px solid #263B5A; padding:8px; border-radius:6px; margin-bottom:6px; cursor:pointer; font-size:11px;"><b>🏭 Industrial Zone (Hazmat Cam)</b><br><span style="color:#9DB0CE; font-size:9px;">Toxic acid chimney toxic plume & flare surge</span></button>
                <button onclick="setPreset('Hospital', 78, 92, 92, 32, 98)" style="width:100%; text-align:left; background:#111C33; color:#fff; border:1px solid #263B5A; padding:8px; border-radius:6px; margin-bottom:6px; cursor:pointer; font-size:11px;"><b>🏥 Hospital (Infra-CCTV)</b><br><span style="color:#9DB0CE; font-size:9px;">ICU power egress & evacuation road gridlock</span></button>
                <button onclick="setPreset('Residential Area', 92, 91, 95, 68, 98)" style="width:100%; text-align:left; background:#111C33; color:#fff; border:1px solid #263B5A; padding:8px; border-radius:6px; cursor:pointer; font-size:11px;"><b>🏘️ Residential Area (City Cam)</b><br><span style="color:#9DB0CE; font-size:9px;">Apartment towers flood & high population risk</span></button>
            </div>

            <!-- Middle Column: Tactical HUD -->
            <div style="background:#05070E; border:1px solid #263B5A; border-radius:10px; padding:12px; position:relative; display:flex; flex-direction:column; justify-content:space-between;">
                <div style="display:flex; justify-content:space-between; align-items:center; font-size:11px; font-family:monospace; color:#38D996;">
                    <span>● REC [LIVE] &nbsp;&nbsp; GPS: 23.2599° N, 77.4126° E | ALT: 142m | MODE: RGB</span>
                    <span style="color:#00D9FF;">FPS: 60.0</span>
                </div>
                <div style="height:320px; position:relative; background:radial-gradient(circle, #0b1528 0%, #030712 100%); border:1px dashed #155E75; border-radius:8px; margin:10px 0; overflow:hidden; display:flex; align-items:center; justify-content:center;">
                    <div style="position:absolute; top:20px; left:20px; border:2px dashed #FF5C75; background:rgba(255,92,117,0.15); width:110px; height:150px; display:flex; align-items:flex-start; padding:4px;">
                        <span style="background:#FF5C75; color:#000; font-size:9px; font-weight:bold; padding:1px 4px;">YOLOV8: ROOFTOP_CROWD [96.0%]</span>
                    </div>
                    <div style="position:absolute; top:70px; right:35px; border:2px dashed #00D9FF; background:rgba(0,217,255,0.15); width:95px; height:170px; display:flex; align-items:flex-start; padding:4px;">
                        <span style="background:#00D9FF; color:#000; font-size:9px; font-weight:bold; padding:1px 4px;">YOLOV8: FLOOD_LINE [94.3%]</span>
                    </div>
                    <div style="position:absolute; bottom:15px; left:30px; border:2px dashed #38D996; background:rgba(56,217,150,0.15); width:140px; height:70px; display:flex; align-items:flex-start; padding:4px;">
                        <span style="background:#38D996; color:#000; font-size:9px; font-weight:bold; padding:1px 4px;">YOLOV8: SUBMERGED [91.1%]</span>
                    </div>
                    <div style="color:#00D9FF; font-family:monospace; font-size:12px; letter-spacing:1px; background:rgba(7,11,20,0.8); padding:6px 12px; border-radius:4px; border:1px solid #00D9FF;">TARGET LOCKED // MULTIMODAL INGESTION ACTIVE</div>
                </div>
                <div style="font-size:11px; color:#9DB0CE; text-align:center;">Click any preset on the left to simulate real-time AI computer vision data stream normalization.</div>
            </div>

            <!-- Right Column: Output & Sync -->
            <div style="background:#0B1220; border:1px solid #263B5A; padding:12px; border-radius:10px; display:flex; flex-direction:column; justify-content:space-between;">
                <div>
                    <div style="font-size:12px; font-weight:800; color:#00D9FF; margin-bottom:10px;">📊 TERA-EYE NORMALIZED OUTPUT</div>
                    <div style="font-size:11px; margin-bottom:4px;">Hazard (30%): <b id="val_h" style="color:#FF5C75;">92/100</b></div>
                    <div style="font-size:11px; margin-bottom:4px;">Vulnerability (25%): <b id="val_v" style="color:#FFD166;">91/100</b></div>
                    <div style="font-size:11px; margin-bottom:4px;">Population (20%): <b id="val_p" style="color:#38D996;">95/100</b></div>
                    <div style="font-size:11px; margin-bottom:4px;">Exposure (15%): <b id="val_e" style="color:#448AFF;">68/100</b></div>
                    <div style="font-size:11px; margin-bottom:12px;">Urgency (10%): <b id="val_u" style="color:#A78BFA;">98/100</b></div>
                    <div style="background:#111C33; padding:10px; border-radius:8px; border:1px solid #263B5A; text-align:center;">
                        <div style="font-size:10px; color:#9DB0CE;">CALCULATED RPI INDEX</div>
                        <div id="val_rpi" style="font-size:22px; font-weight:900; color:#00D9FF;">88.1 / 100</div>
                    </div>
                </div>
                <div style="margin-top:10px;">
                    <button onclick="alert('Successfully synchronized TERA-EYE AI vision feed into TERA 2.0 database!')" style="width:100%; background:linear-gradient(90deg,#00D9FF,#38D996); color:#070B14; border:none; padding:10px; border-radius:8px; font-weight:900; cursor:pointer; font-size:11px;">🚀 SYNC & OPEN SCENARIO LAB</button>
                </div>
            </div>
        </div>
    </div>
    <script>
        function setPreset(name, h, v, p, e, u) {
            document.getElementById('val_h').innerText = h + '/100';
            document.getElementById('val_v').innerText = v + '/100';
            document.getElementById('val_p').innerText = p + '/100';
            document.getElementById('val_e').innerText = e + '/100';
            document.getElementById('val_u').innerText = u + '/100';
            let rpi = (h*0.30 + v*0.25 + p*0.20 + e*0.15 + u*0.10).toFixed(1);
            document.getElementById('val_rpi').innerText = rpi + ' / 100';
        }
    </script>
    """, height=520)
```

<fieldset data-type="replies"><legend>Ready for the final review?</legend><button class="reply" value="How do I deploy this on GitHub and Streamlit Cloud right now?">How do I deploy this on GitHub?</button><button class="reply" value="Give me the final practice checklist for me and Sriram.">Final practice checklist</button></fieldset>
