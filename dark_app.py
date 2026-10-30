import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="TERA 2.0 — Midnight Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- THEME COLORS ---
BG = "#0B1220"
CARD_BG = "#111C33"
TEXT = "#F1F5F9"
CYAN = "#00D9FF"
MINT = "#38D996"
AMBER = "#FFB454"
RED = "#FF5C70"
BORDER = "#1E293B"
MUTED = "#94A3B8"

# --- GLOBAL STYLING ---
st.markdown(f"""
<style>
    .stApp {{ background-color: {BG}; color: {TEXT}; }}
    [data-testid="stSidebar"] {{ background-color: {CARD_BG}; border-right: 1px solid {BORDER}; }}
    .stMetric {{ background-color: {CARD_BG}; padding: 15px; border-radius: 10px; border: 1px solid {BORDER}; }}
</style>
""", unsafe_allow_html=True)

# --- DATA MODEL ---
FACTORS = ["Hazard", "Vulnerability", "Population", "Exposure", "Urgency"]
FACTOR_COLORS = [RED, AMBER, MINT, CYAN, "#A78BFA"]

if "zone_values" not in st.session_state:
    st.session_state.zone_values = {
        "Smart Farm": [60, 45, 50, 70, 50],
        "River & Dam": [85, 75, 70, 80, 80],
        "Industrial Zone": [80, 70, 60, 75, 70],
        "Hospital": [50, 90, 85, 30, 95],
        "Residential Area": [70, 80, 95, 70, 85],
        "Forest": [90, 40, 30, 95, 50]
    }

if "factor_weights" not in st.session_state:
    st.session_state.factor_weights = {
        "Hazard": 30, "Vulnerability": 25, "Population": 20, "Exposure": 15, "Urgency": 10
    }

def weights():
    tot = sum(st.session_state.factor_weights.values())
    if tot == 0:
        return {f: 20 for f in FACTORS}
    return {f: (v / tot) * 100 for f, v in st.session_state.factor_weights.items()}

def rpi(vals):
    w = weights()
    return sum(vals[i] * w[f] / 100 for i, f in enumerate(FACTORS))

def classify(score):
    if score >= 80: return "CRITICAL", RED
    if score >= 65: return "HIGH", AMBER
    if score >= 45: return "MODERATE", MINT
    return "LOWER", CYAN

def style_fig(fig, height=350):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=30, b=30, l=30, r=30),
        height=height,
        font=dict(color=TEXT)
    )
    return fig

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### ⚡ TERA 2.0")
    st.caption("Midnight Intelligence Engine")
    st.divider()
    st.markdown("### Global Factor Weights")
    for f in FACTORS:
        st.session_state.factor_weights[f] = st.slider(f, 0, 50, st.session_state.factor_weights[f], key=f"weight_{f}")
    st.divider()
    if st.button("Reset Default Weights"):
        st.session_state.factor_weights = {"Hazard": 30, "Vulnerability": 25, "Population": 20, "Exposure": 15, "Urgency": 10}
        st.rerun()

# --- MAIN TABS ---
tabs = st.tabs([
    "⚡ Command Centre", 
    "🛰️ Zone Intelligence", 
    "📊 Compare Zones", 
    "🧪 Scenario Lab", 
    "🎯 Mission Control", 
    "📘 Methodology",
    "🛰️ TERA-EYE Ingestion"
])

# TAB 0: COMMAND CENTRE
with tabs[0]:
    st.markdown("## Command Centre — City Overview")
    rows = []
    for name, vals in st.session_state.zone_values.items():
        score = rpi(vals)
        label, col = classify(score)
        rows.append({"Zone": name, "RPI": round(score, 1), "Classification": label, **{f: vals[i] for i, f in enumerate(FACTORS)}})
    
    df = pd.DataFrame(rows).sort_values("RPI", ascending=False)
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Zones Monitored", len(df))
    c2.metric("City Average RPI", f"{df['RPI'].mean():.1f}/100")
    c3.metric("Critical Zones", len(df[df["Classification"] == "CRITICAL"]))
    c4.metric("High Priority Zones", len(df[df["Classification"] == "HIGH"]))
    
    st.divider()
    
    left, right = st.columns([1.5, 1])
    with left:
        fig = px.bar(df.sort_values("RPI"), x="RPI", y="Zone", orientation="h", color="RPI", color_continuous_scale=[MINT, AMBER, RED], text="RPI")
        fig.update_xaxes(range=[0, 110], gridcolor=BORDER)
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(style_fig(fig, 320), use_container_width=True)
    with right:
        donut = px.pie(df, names="Classification", hole=0.6, color="Classification", color_discrete_map={"CRITICAL": RED, "HIGH": AMBER, "MODERATE": MINT, "LOWER": CYAN})
        st.plotly_chart(style_fig(donut, 320), use_container_width=True)
        
    st.markdown("### Zone Assessment Table")
    st.dataframe(df, use_container_width=True, hide_index=True)

# TAB 1: ZONE INTELLIGENCE
with tabs[1]:
    st.markdown("## Zone Intelligence & Factor Breakdown")
    selected_zone = st.selectbox("Select zone to inspect", list(st.session_state.zone_values.keys()), key="intel_zone")
    vals = st.session_state.zone_values[selected_zone]
    score = rpi(vals)
    label, col = classify(score)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Risk Priority Index (RPI)", f"{score:.1f}/100")
    c2.metric("Priority Classification", label)
    c3.metric("Max Factor Score", f"{max(vals)}/100")
    
    left, right = st.columns(2)
    with left:
        radar = go.Figure(data=go.Scatterpolar(r=vals + [vals[0]], theta=FACTORS + [FACTORS[0]], fill='toself', line_color=CYAN))
        radar.update_polar(radialaxis=dict(range=[0, 100], gridcolor=BORDER), angularaxis=dict(gridcolor=BORDER))
        st.plotly_chart(style_fig(radar, 350), use_container_width=True)
    with right:
        w = weights()
        contributions = [vals[i] * w[f] / 100 for i, f in enumerate(FACTORS)]
        cp = px.pie(names=FACTORS, values=contributions, hole=0.58, color_discrete_sequence=FACTOR_COLORS)
        st.plotly_chart(style_fig(cp, 350), use_container_width=True)

# TAB 2: COMPARE ZONES
with tabs[2]:
    st.markdown("## Compare Zones")
    c1, c2 = st.columns(2)
    za = c1.selectbox("First zone", list(st.session_state.zone_values), key="compare_a")
    zb = c2.selectbox("Second zone", list(st.session_state.zone_values), index=1, key="compare_b")
    if za != zb:
        comp = pd.DataFrame({"Factor": FACTORS, za: st.session_state.zone_values[za], zb: st.session_state.zone_values[zb]}).melt("Factor", var_name="Zone", value_name="Score")
        fig = px.bar(comp, x="Factor", y="Score", color="Zone", barmode="group", color_discrete_sequence=[CYAN, MINT], text="Score")
        st.plotly_chart(style_fig(fig, 400), use_container_width=True)

# TAB 3: SCENARIO LAB
with tabs[3]:
    st.markdown("## Scenario Lab")
    scenario = st.selectbox("Choose scenario", ["Baseline — current model", "Heavy rainfall / flood pressure", "Industrial air-pollution incident", "Extreme heat / medical strain"])
    adjustments = {
        "Baseline — current model": {},
        "Heavy rainfall / flood pressure": {"River & Dam": [15, 5, 0, 10, 15], "Smart Farm": [20, 10, 0, 15, 10]},
        "Industrial air-pollution incident": {"Industrial Zone": [15, 5, 0, 10, 10]},
        "Extreme heat / medical strain": {"Hospital": [5, 10, 5, 0, 15]}
    }
    rows = []
    for name, base in st.session_state.zone_values.items():
        adj = adjustments[scenario].get(name, [0]*5)
        changed = [max(0, min(100, base[i] + adj[i])) for i in range(5)]
        rows.append({"Zone": name, "Scenario RPI": round(rpi(changed), 1)})
    sdf = pd.DataFrame(rows).sort_values("Scenario RPI", ascending=False)
    st.metric("Top scenario priority", sdf.iloc[0].Zone, f"RPI {sdf.iloc[0]['Scenario RPI']:.1f}")
    st.dataframe(sdf, use_container_width=True, hide_index=True)

# TAB 4: MISSION CONTROL
with tabs[4]:
    st.markdown("## Mission Control")
    mission = st.selectbox("Mission type", ["Flood readiness", "Air-quality incident", "Extreme-heat support"])
    cols = st.columns(3)
    allocations = [cols[i].number_input(act, 0, 10, 3, 1, key=f"m_{i}") for i, act in enumerate(["Task Force 1", "Task Force 2", "Task Force 3"])]
    if sum(allocations) == 10:
        st.success("Allocation complete — all 10 response units assigned.")
    else:
        st.warning(f"Total units assigned: {sum(allocations)}/10")

# TAB 5: METHODOLOGY
with tabs[5]:
    st.markdown("## Methodology & AI")
    st.latex(r"RPI = 0.30H + 0.25V + 0.20P + 0.15E + 0.10U")
    st.write("Rule-based multi-criteria priority index built in Python, Pandas, Plotly, and Streamlit.")

# TAB 6: TERA-EYE INGESTION
with tabs[6]:
    st.markdown("## 🛰️ TERA-EYE: Live Ingestion & Vision Engine")
    st.caption("Multimodal sensor and drone feed ingestion module for TERA 2.0.")
    
    col_cam1, col_cam2 = st.columns([2, 1])
    with col_cam1:
        st.markdown("### Live Tactical Drone Feed (Simulated HUD)")
        st.markdown(
            f"""
            <div style="background:#05070e; border:2px solid {CYAN}; padding:20px; border-radius:12px; text-align:center; font-family:monospace;">
                <div style="color:{MINT}; font-size:0.9rem; margin-bottom:10px;">● RECORDING [FLIR_THERMAL_MODE // ACTIVE FEED]</div>
                <div style="background:#0b1220; height:240px; border:1px dashed {MINT}; display:flex; align-items:center; justify-content:center; color:{CYAN}; font-size:1.1rem; border-radius:8px; position:relative;">
                    <div style="position:absolute; top:12px; left:12px; color:{RED}; font-size:0.75rem;">TARGET LOCKED: ANOMALY_DETECTED [98.4%]</div>
                    <div style="position:absolute; bottom:12px; right:12px; color:{AMBER}; font-size:0.75rem;">GPS: 23.2599° N, 77.4126° E</div>
                    <div>📡 INGESTING DRONE STREAM PIXELS & CCTV FRAMES...</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        selected_feed = st.selectbox("Select Feed Source", list(st.session_state.zone_values.keys()))

    with col_cam2:
        st.markdown("### Vision AI Extractor")
        st.write("Extracts unstructured video pixels and normalizes them to TERA's 0–100 scale.")
        
        cv_h = st.slider("Extracted Hazard (H)", 0, 100, 75, key="cv_h")
        cv_v = st.slider("Extracted Vulnerability (V)", 0, 100, 60, key="cv_v")
        cv_p = st.slider("Extrored Population (P)", 0, 100, 50, key="cv_p")
        cv_e = st.slider("Extracted Exposure (E)", 0, 100, 85, key="cv_e")
        cv_urg = st.slider("Extracted Urgency (U)", 0, 100, 70, key="cv_u")
        
        if st.button("🚀 Push TERA-EYE Data to Scoring Model", type="primary"):
            st.session_state.zone_values[selected_feed] = [cv_h, cv_v, cv_p, cv_e, cv_urg]
            st.success(f"Successfully injected live feed from **{selected_feed}** into TERA 2.0 database!")
            st.balloons()
