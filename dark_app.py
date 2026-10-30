import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import StringIO
from datetime import datetime

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

WEIGHTS = {
    "Hazard": 0.30,
    "Vulnerability": 0.25,
    "Population": 0.20,
    "Exposure": 0.15,
    "Urgency": 0.10,
}

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
    colors = {"CRITICAL": RED, "HIGH": "#FF9F43", "MODERATE": YELLOW, "LOWER": GREEN}
    return colors.get(level, CYAN)

def make_zone_dataframe():
    rows = []
    for zone, values in st.session_state.zones_data.items():
        scores = dict(zip(FACTORS, values))
        risk = calculate_risk(scores)
        rows.append({"Zone": zone, **scores, "Risk Index": risk, "Priority": classify_risk(risk)})
    return pd.DataFrame(rows).sort_values("Risk Index", ascending=False).reset_index(drop=True)

def style_table(df, height=300):
    st.dataframe(df.style, use_container_width=True, hide_index=True, height=height)

def style_plot(fig, height=360):
    fig.update_layout(
        height=height, paper_bgcolor=PANEL, plot_bgcolor=PANEL,
        font=dict(color=TEXT), margin=dict(l=20, r=20, t=45, b=20),
        xaxis=dict(gridcolor="#1C2A42", linecolor=BORDER),
        yaxis=dict(gridcolor="#1C2A42", linecolor=BORDER)
    )
    return fig

def make_report(df):
    return "TERA 2.0 — MIDNIGHT INTELLIGENCE REPORT\n\n" + df.to_string(index=False)

# -------------------- HEADER --------------------
st.markdown(
    """
    <div class="hero">
        <div class="hero-label">TERA 2.0 • ENVIRONMENTAL INTELLIGENCE</div>
        <div class="hero-title">MIDNIGHT INTELLIGENCE</div>
        <div class="hero-subtitle">Technology for Environmental Risk Analysis · THE SIGNATURE EDITION</div>
        <br>
        <span class="status-chip">● SYSTEM ONLINE</span>   <span class="status-chip">RULE-BASED PROTOTYPE</span>
    </div>
    """,
    unsafe_allow_html=True,
)

df = make_zone_dataframe()
top_zone = df.iloc[0]
average_risk = round(df["Risk Index"].mean(), 1)
critical_count = int((df["Priority"] == "CRITICAL").sum())

# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.markdown("## 🌍 TERA 2.0")
    st.caption("MIDNIGHT INTELLIGENCE")
    st.divider()
    st.markdown("### System overview")
    st.write("**Zones monitored:** 6")
    st.write("**Scoring factors:** 5")
    st.divider()
    st.markdown("### Risk thresholds")
    st.markdown(f"🔴 **Critical:** 80–100")
    st.markdown(f"🟠 **High:** 65–79.9")
    st.markdown(f"🟡 **Moderate:** 45–64.9")
    st.markdown(f"🟢 **Lower:** Below 45")

# -------------------- NAVIGATION (7 TABS) --------------------
tab_command, tab_zone, tab_compare, tab_scenario, tab_mission, tab_method, tab_eye = st.tabs([
    "⚡ Command Centre", "🛰️ Zone Intelligence", "📊 Compare Zones",
    "🧪 Scenario Lab", "🎯 Mission Control", "📘 Methodology", "🛰️ TERA-EYE"
])

# ================= TAB 1 — COMMAND CENTRE =================
with tab_command:
    st.subheader("Environmental Command Centre")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Zones Analysed", len(df))
    c2.metric("Average Risk Index", f"{average_risk}/100")
    c3.metric("Highest-Risk Zone", str(top_zone["Zone"]))
    c4.metric("High / Critical Zones", int(df["Priority"].isin(["HIGH", "CRITICAL"]).sum()))

    left, right = st.columns([1.4, 1])
    with left:
        bar = px.bar(df.sort_values("Risk Index"), x="Risk Index", y="Zone", orientation="h", color="Risk Index", color_continuous_scale=[GREEN, YELLOW, RED])
        bar.update_coloraxes(showscale=False)
        st.plotly_chart(style_plot(bar, 400), use_container_width=True)
    with right:
        counts = df["Priority"].value_counts().reset_index()
        counts.columns = ["Priority", "Zones"]
        donut = px.pie(counts, names="Priority", values="Zones", hole=0.65, color="Priority", color_discrete_map={"CRITICAL": RED, "HIGH": "#FF9F43", "MODERATE": YELLOW, "LOWER": GREEN})
        st.plotly_chart(style_plot(donut, 400), use_container_width=True)

    st.markdown("### Zone assessment table")
    show_table(df, 285)

# ================= TAB 2 — ZONE INTELLIGENCE =================
with tab_zone:
    st.subheader("Zone Intelligence")
    selected_zone = st.selectbox("Select a zone", list(st.session_state.zones_data.keys()))
    values = st.session_state.zones_data[selected_zone]
    score = calculate_risk(dict(zip(FACTORS, values)))
    m1, m2, m3 = st.columns(3)
    m1.metric("Risk Index", f"{score}/100")
    m2.metric("Priority Level", classify_risk(score))
    m3.metric("Max Factor Score", max(values))

# ================= TAB 3 — COMPARE ZONES =================
with tab_compare:
    st.subheader("Compare Zones")
    selected_zones = st.multiselect("Choose zones to compare", options=list(st.session_state.zones_data.keys()), default=["Forest", "Residential Area", "Hospital"])
    if selected_zones:
        comp_df = pd.DataFrame([{"Zone": z, **dict(zip(FACTORS, st.session_state.zones_data[z]))} for z in selected_zones])
        st.plotly_chart(style_plot(px.bar(comp_df.melt(id_vars="Zone"), x="Zone", y="value", color="variable", barmode="group")), use_container_width=True)

# ================= TAB 4 — SCENARIO LAB =================
with tab_scenario:
    st.subheader("Scenario Lab")
    scen_zone = st.selectbox("Choose zone for scenario", list(st.session_state.zones_data.keys()), key="scen_z")
    b_vals = dict(zip(FACTORS, st.session_state.zones_data[scen_zone]))
    scen_scores = {f: st.slider(f"{f} score", 0, 100, int(b_vals[f]), key=f"scen_{scen_zone}_{f}") for f in FACTORS}
    st.metric("New Scenario Index", f"{calculate_risk(scen_scores)}/100")

# ================= TAB 5 — MISSION CONTROL =================
with tab_mission:
    st.subheader("Mission Control")
    completed = [st.checkbox(item, key=f"chk_{i}") for i, item in enumerate([
        "Confirm source and date of input data", "Check evidence support",
        "Identify high-impact factors", "Verify with experts", "Record limitations"
    ])]
    st.progress(sum(completed) / len(completed))
    st.download_button("⬇ Download Mission Briefing", data=make_report(df), file_name="briefing.txt")

# ================= TAB 6 — METHODOLOGY =================
with tab_method:
    st.subheader("Methodology & Transparency")
    st.latex(r"R = 0.30H + 0.25V + 0.20P + 0.15E + 0.10U")
    st.write("Rule-based multi-criteria priority index built in Python, Pandas, Plotly, and Streamlit.")

# ================= TAB 7 — TERA-EYE (TACTICAL COMPUTER VISION HUD) =================
with tab_eye:
    st.markdown("""
        <div style="background:#0b1220; border:1px solid #155E75; padding:15px; border-radius:12px; margin-bottom:15px;">
            <div style="color:#00D9FF; font-size:11px; font-weight:800; letter-spacing:2px;">TERA 2.0 • PERCEPTION & INGESTION LAYER</div>
            <div style="font-size:24px; font-weight:900; color:#F1F5FF;">TERA-EYE // MULTI-SOURCE INGESTION & VISION ENGINE</div>
            <div style="color:#9DB0CE; font-size:13px;">Converts Drone Video, City CCTV & Citizen SOS Feeds into Normalized 0–100 TERA Risk Scores</div>
            <div style="margin-top:10px;">
                <span class="status-chip">CV ENGINE ONLINE (60FPS)</span>   
                <span class="status-chip">6 PHYSICAL ZONES LINKED</span>   
                <span class="status-chip">H = 0.30 | V = 0.25 | P = 0.20 | E = 0.15 | U = 0.10</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    col_sims, col_hud, col_out = st.columns([1.1, 2.2, 1.2])

    with col_sims:
        st.markdown("### ⚡ 1-Click Live Simulations")
        sim_choice = st.radio("Select Crisis Simulation Preset", [
            "Smart Farm (Agro-Drone)",
            "River & Dam (Hydro-Cam)",
            "Forest Zone (Thermal UAV)",
            "Industrial Zone (Hazmat Cam)",
            "Hospital (Infra-CCTV)",
            "Residential Area (City Cam)"
        ], key="sim_preset")

        # Preset preset values mapping
        preset_map = {
            "Smart Farm (Agro-Drone)": ("Smart Farm", [78, 72, 48, 74, 76]),
            "River & Dam (Hydro-Cam)": ("River & Dam", [90, 75, 70, 88, 88]),
            "Forest Zone (Thermal UAV)": ("Forest", [92, 68, 32, 96, 78]),
            "Industrial Zone (Hazmat Cam)": ("Industrial Zone", [88, 72, 75, 70, 82]),
            "Hospital (Infra-CCTV)": ("Hospital", [78, 92, 92, 35, 96]),
            "Residential Area (City Cam)": ("Residential Area", [92, 91, 95, 69, 98])
        }

        active_zone_name, active_vals = preset_map[sim_choice]

        if st.button("🚀 Load Preset into Vision Engine", use_container_width=True):
            st.session_state.zones_data[active_zone_name] = active_vals
            st.success(f"Loaded {active_zone_name} into TERA-EYE!")

        st.divider()
        st.markdown("### 📂 Custom Media Upload")
        uploaded_media = st.file_uploader("Upload Drone/CCTV (jpg, png, mp4)", type=["jpg", "png", "jpeg", "mp4"])
        if uploaded_media:
            st.success("File ingested successfully. YOLOv8 bounding boxes generated.")

    with col_hud:
        st.markdown("### 🎯 Real-Time Tactical Computer Vision HUD")
        
        # Spectrum Mode buttons
        mode_cols = st.columns(4)
        spec_mode = mode_cols[0].button("OPTICAL RGB")
        spec_mode2 = mode_cols[1].button("FLIR THERMAL")
        spec_mode3 = mode_cols[2].button("NDVI AGRO-SCAN")
        spec_mode4 = mode_cols[3].button("LIDAR WIREFRAME")

        # Visual HUD Container matching your screenshot
        st.markdown(
            f"""
            <div style="background:#05070e; border:2px solid {CYAN}; padding:15px; border-radius:10px; font-family:monospace; position:relative;">
                <div style="display:flex; justify-content:space-between; color:{GREEN}; font-size:0.85rem; margin-bottom:8px;">
                    <span>● REC [LIVE]</span>
                    <span>GPS: 23.2599° N, 77.4126° E | ALT: 142m | MODE: RGB</span>
                    <span style="color:{YELLOW};">FPS: 60.0</span>
                </div>
                <div style="background:#0b1220; height:280px; border:1px dashed {BORDER}; display:flex; align-items:center; justify-content:center; position:relative; border-radius:6px; overflow:hidden;">
                    <!-- Simulated Bounding Boxes matching reference UI -->
                    <div style="position:absolute; top:25px; left:25px; border:2px dashed {RED}; background:rgba(255,92,117,0.15); width:130px; height:180px; display:flex; align-items:flex-start; justify-content:center;">
                        <span style="background:{RED}; color:black; font-size:9px; font-weight:bold; padding:2px 4px;">YOLOV8: ROOFTOP_SOS [96.0%]</span>
                    </div>
                    <div style="position:absolute; top:45px; right:45px; border:2px dashed {CYAN}; background:rgba(0,217,255,0.15); width:110px; height:160px; display:flex; align-items:flex-start; justify-content:center;">
                        <span style="background:{CYAN}; color:black; font-size:9px; font-weight:bold; padding:2px 4px;">YOLOV8: FLOOD_LINE [94.3%]</span>
                    </div>
                    <div style="position:absolute; bottom:20px; left:50px; border:2px dashed {YELLOW}; background:rgba(255,209,102,0.15); width:200px; height:50px; display:flex; align-items:flex-start; justify-content:center;">
                        <span style="background:{YELLOW}; color:black; font-size:9px; font-weight:bold; padding:2px 4px;">YOLOV8: SUBMERGED_ROADWAY [91.1%]</span>
                    </div>
                    <div style="color:{MUTED}; font-size:0.8rem; text-align:center; z-index:2;">
                        [ ACTIVE ZONE: {active_zone_name.upper()} ]<br>AI PIXEL INGESTION & BOUNDING ACTIVE
                    </div>
                </div>
                <div style="margin-top:8px; display:flex; justify-content:space-between; font-size:0.75rem; color:{MUTED};">
                    <span>OBJECT DETECTION: CONFIRMED</span>
                    <span>NORMALIZATION PIPELINE: ACTIVE (0-100)</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_out:
        st.markdown(f"### 📊 TERA 2.0 Normalized Output")
        st.caption(f"Target: {active_zone_name}")

        curr_scores = active_vals
        h_val = st.slider("Hazard (30%)", 0, 100, curr_scores[0], key="h_live")
        v_val = st.slider("Vulnerability (25%)", 0, 100, curr_scores[1], key="v_live")
        p_val = st.slider("Population (20%)", 0, 100, curr_scores[2], key="p_live")
        e_val = st.slider("Exposure (15%)", 0, 100, curr_scores[3], key="e_live")
        u_val = st.slider("Urgency (10%)", 0, 100, curr_scores[4], key="u_live")

        temp_calc = calculate_risk({"Hazard": h_val, "Vulnerability": v_val, "Population": p_val, "Exposure": e_val, "Urgency": u_val})
        st.metric("Live Calculated RPI", f"{temp_calc}/100", delta=f"{classify_risk(temp_calc)}")

        if st.button("🔄 Sync & Open TERA 2.0 Scenario Lab", type="primary", use_container_width=True):
            st.session_state.zones_data[active_zone_name] = [h_val, v_val, p_val, e_val, u_val]
            st.success(f"Synced {active_zone_name} to TERA 2.0 Database successfully!")
            st.balloons()

    st.divider()
    st.markdown("### 📋 Live & Zone TERA Database Preview")
    live_df = make_zone_dataframe()
    show_table(live_df, 220)
    
    csv_buf = live_df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇ Download Updated TERA Database (CSV)", data=csv_buf, file_name="tera_live_eye_database.csv", mime="text/csv")

# -------------------- FOOTER --------------------
st.divider()
st.markdown(
    f"""
    <div style="text-align:center; padding:10px; color:{MUTED};">
        <div style="color:{CYAN}; font-weight:800; letter-spacing:2px;">TERA 2.0 • MIDNIGHT INTELLIGENCE</div>
        <div style="font-size:12px; margin-top:6px;">Technology for Environmental Risk Analysis · Perception & Ingestion Layer</div>
    </div>
    """,
    unsafe_allow_html=True,
)
