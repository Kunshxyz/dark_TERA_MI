import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ============================================================
# TERA 2.0 - MIDNIGHT INTELLIGENCE EDITION
# Educational environmental risk-priority prototype
# ============================================================

st.set_page_config(
    page_title="TERA 2.0 | Midnight Intelligence",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------- COLOUR PALETTE --------------------
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
ORANGE = "#FF9F43"
RED = "#FF5C75"

# -------------------- THEME CSS --------------------
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {BG};
        color: {TEXT};
    }}
    [data-testid="stSidebar"] {{
        background-color: #090F1C;
        border-right: 1px solid {BORDER};
    }}
    [data-testid="stHeader"] {{
        background: rgba(7, 11, 20, 0.95);
    }}
    h1, h2, h3, h4 {{
        color: {TEXT} !important;
    }}
    p, label, li, [data-testid="stMarkdownContainer"] {{
        color: {TEXT};
    }}
    [data-testid="stMetric"] {{
        background-color: {PANEL};
        border: 1px solid {BORDER};
        border-radius: 14px;
        padding: 14px;
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
    div.stButton > button, div.stDownloadButton > button {{
        background: linear-gradient(90deg, #12345A, #155E75);
        color: white;
        border: 1px solid {CYAN};
        border-radius: 9px;
        font-weight: 600;
    }}
    div.stButton > button:hover, div.stDownloadButton > button:hover {{
        background: #164E63;
        color: white;
        border-color: white;
    }}
    [data-testid="stDataFrame"], [data-testid="stTable"] {{
        background-color: {PANEL};
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
    [data-testid="stTable"] table {{
        background-color: {PANEL} !important;
        color: {TEXT} !important;
        border-collapse: collapse !important;
    }}
    [data-testid="stTable"] thead th {{
        background-color: {HEADER} !important;
        color: {CYAN} !important;
        border-bottom: 1px solid {BORDER} !important;
    }}
    [data-testid="stTable"] tbody td {{
        background-color: {PANEL} !important;
        color: {TEXT} !important;
        border-bottom: 1px solid {BORDER} !important;
    }}
    .tera-hero {{
        padding: 26px;
        border-radius: 18px;
        border: 1px solid #155E75;
        background: linear-gradient(120deg, #0B1220 0%, #10243D 60%, #10102A 100%);
        margin-bottom: 18px;
    }}
    .tera-eyebrow {{
        color: {CYAN};
        font-size: 12px;
        letter-spacing: 3px;
        font-weight: 800;
    }}
    .tera-title {{
        color: {TEXT};
        font-size: clamp(28px, 4vw, 44px);
        font-weight: 900;
        line-height: 1.1;
        margin: 8px 0;
    }}
    .tera-subtitle {{
        color: {MUTED};
        font-size: 15px;
    }}
    .tera-chip {{
        display: inline-block;
        color: {CYAN};
        border: 1px solid #155E75;
        background: #0A2533;
        border-radius: 20px;
        padding: 5px 10px;
        font-size: 12px;
        font-weight: 700;
    }}
    .tera-note {{
        color: {MUTED};
        font-size: 12px;
    }}
    div[data-testid="stAlert"] {{
        background-color: #111C33;
        border: 1px solid {BORDER};
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------- MODEL DATA --------------------
FACTORS = ["Hazard", "Vulnerability", "Population", "Exposure", "Urgency"]

WEIGHTS = {
    "Hazard": 0.30,
    "Vulnerability": 0.25,
    "Population": 0.20,
    "Exposure": 0.15,
    "Urgency": 0.10,
}

ZONES = {
    "Forest": [72, 65, 35, 95, 75],
    "Residential Area": [80, 85, 95, 45, 90],
    "Hospital": [75, 90, 90, 30, 95],
    "Smart Farm": [60, 65, 45, 75, 60],
    "River & Dam": [85, 75, 70, 85, 85],
    "Industrial Zone": [82, 70, 75, 65, 80],
}


def calculate_risk(scores):
    """Return the weighted illustrative priority index, from 0 to 100."""
    return round(sum(float(scores[f]) * WEIGHTS[f] for f in FACTORS), 1)


def classify_risk(score):
    if score >= 80:
        return "CRITICAL"
    if score >= 65:
        return "HIGH"
    if score >= 45:
        return "MODERATE"
    return "LOWER"


def priority_colour(priority):
    return {
        "CRITICAL": RED,
        "HIGH": ORANGE,
        "MODERATE": YELLOW,
        "LOWER": GREEN,
    }.get(priority, CYAN)


def make_zone_dataframe():
    rows = []
    for zone, values in ZONES.items():
        scores = dict(zip(FACTORS, values))
        risk = calculate_risk(scores)
        rows.append({
            "Zone": zone,
            **scores,
            "Risk Index": risk,
            "Priority": classify_risk(risk),
        })
    return pd.DataFrame(rows).sort_values(
        "Risk Index", ascending=False
    ).reset_index(drop=True)


def show_table(dataframe, height=300):
    """Display a dataframe; CSS above styles the Streamlit table surface."""
    st.dataframe(
        dataframe,
        use_container_width=True,
        hide_index=True,
        height=height,
    )


def style_plot(fig, height=360):
    fig.update_layout(
        height=height,
        paper_bgcolor=PANEL,
        plot_bgcolor=PANEL,
        font=dict(color=TEXT, family="Arial"),
        margin=dict(l=20, r=20, t=50, b=20),
        title_font=dict(color=TEXT, size=17),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color=TEXT),
        ),
        xaxis=dict(
            gridcolor="#1C2A42",
            linecolor=BORDER,
            tickfont=dict(color=MUTED),
            title_font=dict(color=MUTED),
        ),
        yaxis=dict(
            gridcolor="#1C2A42",
            linecolor=BORDER,
            tickfont=dict(color=MUTED),
            title_font=dict(color=MUTED),
        ),
    )
    return fig


def make_report(dataframe, notes="", checklist_percent=None):
    lines = [
        "TERA 2.0 - MIDNIGHT INTELLIGENCE EDITION",
        "Technology for Environmental Risk Analysis",
        "Report generated: " + datetime.now().strftime("%d %b %Y, %H:%M"),
        "",
        "SCIENTIFIC NOTE:",
        "Scores are illustrative weighted priority indices, not probabilities,",
        "validated forecasts, live sensor readings, or official warnings.",
        "",
        "FORMULA:",
        "R = 0.30H + 0.25V + 0.20P + 0.15E + 0.10U",
        "",
        "ZONE RESULTS:",
        dataframe.to_string(index=False),
        "",
        "LIMITATIONS:",
        "- Uses illustrative example scores.",
        "- No live sensor, satellite, or weather feeds are connected.",
        "- This version is rule-based and does not use a trained ML model.",
        "- Real-world use would require validated data and expert review.",
    ]
    if notes.strip():
        lines.extend(["", "TEAM NOTES:", notes.strip()])
    if checklist_percent is not None:
        lines.extend(["", f"CHECKLIST COMPLETION: {checklist_percent}%"])
    return "\n".join(lines)


# -------------------- HEADER --------------------
st.markdown(
    """
    <div class="tera-hero">
        <div class="tera-eyebrow">TERA 2.0 • ENVIRONMENTAL INTELLIGENCE</div>
        <div class="tera-title">MIDNIGHT INTELLIGENCE</div>
        <div class="tera-subtitle">
            Technology for Environmental Risk Analysis · THE SIGNATURE EDITION
        </div>
        <br>
        <span class="tera-chip">● SYSTEM ONLINE</span>
        &nbsp;
        <span class="tera-chip">RULE-BASED PROTOTYPE</span>
    </div>
    """,
    unsafe_allow_html=True,
)

zone_df = make_zone_dataframe()
top_zone = zone_df.iloc[0]
average_risk = round(zone_df["Risk Index"].mean(), 1)
high_critical_count = int(zone_df["Priority"].isin(["HIGH", "CRITICAL"]).sum())

# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.markdown("## 🌍 TERA 2.0")
    st.caption("MIDNIGHT INTELLIGENCE")
    st.divider()
    st.markdown("### System overview")
    st.write("**Zones analysed:** 6")
    st.write("**Scoring factors:** 5")
    st.write("**Scoring model:** Weighted index")
    st.divider()
    st.markdown("### Priority thresholds")
    st.markdown("🔴 **Critical:** 80–100")
    st.markdown("🟠 **High:** 65–79.9")
    st.markdown("🟡 **Moderate:** 45–64.9")
    st.markdown("🟢 **Lower:** Below 45")
    st.divider()
    st.markdown("### Data integrity")
    st.caption(
        "Demonstration values only. No live environmental sensor data is connected."
    )

# -------------------- TABS --------------------
tab_command, tab_zone, tab_compare, tab_scenario, tab_mission, tab_method = st.tabs([
    "⚡ Command Centre",
    "🛰️ Zone Intelligence",
    "📊 Compare Zones",
    "🧪 Scenario Lab",
    "🎯 Mission Control",
    "📘 Methodology",
])

# ============================================================
# TAB 1: COMMAND CENTRE
# ============================================================
with tab_command:
    st.subheader("Environmental Command Centre")
    st.caption("A consolidated view of illustrative environmental-risk priorities.")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Zones Analysed", len(zone_df))
    col2.metric("Average Risk Index", f"{average_risk}/100")
    col3.metric("Highest-Risk Zone", str(top_zone["Zone"]))
    col4.metric("High / Critical Zones", high_critical_count)

    left, right = st.columns([1.4, 1])

    with left:
        ranked = zone_df.sort_values("Risk Index", ascending=True)
        bar = px.bar(
            ranked,
            x="Risk Index",
            y="Zone",
            orientation="h",
            color="Priority",
            color_discrete_map={
                "CRITICAL": RED,
                "HIGH": ORANGE,
                "MODERATE": YELLOW,
                "LOWER": GREEN,
            },
            text="Risk Index",
            title="Zone priority ranking",
            category_orders={
                "Priority": ["CRITICAL", "HIGH", "MODERATE", "LOWER"]
            },
        )
        bar.update_traces(textposition="outside", cliponaxis=False)
        bar.update_xaxes(range=[0, 112], title="Illustrative index")
        st.plotly_chart(style_plot(bar, 400), use_container_width=True)

    with right:
        counts = (
            zone_df["Priority"]
            .value_counts()
            .reindex(["CRITICAL", "HIGH", "MODERATE", "LOWER"])
            .fillna(0)
            .reset_index()
        )
        counts.columns = ["Priority", "Zones"]
        donut = px.pie(
            counts,
            names="Priority",
            values="Zones",
            hole=0.62,
            title="Priority distribution",
            color="Priority",
            color_discrete_map={
                "CRITICAL": RED,
                "HIGH": ORANGE,
                "MODERATE": YELLOW,
                "LOWER": GREEN,
            },
        )
        donut.update_traces(textposition="inside", textinfo="label+value")
        st.plotly_chart(style_plot(donut, 400), use_container_width=True)

    st.markdown("### Zone assessment table")
    show_table(zone_df, 285)

    st.info(
        "A higher index indicates higher relative priority within this illustrative model. "
        "It is not a percentage probability of a disaster."
    )

    st.download_button(
        "⬇ Download zone results (CSV)",
        data=zone_df.to_csv(index=False).encode("utf-8"),
        file_name="tera_zone_results.csv",
        mime="text/csv",
        key="command_csv",
    )

# ============================================================
# TAB 2: ZONE INTELLIGENCE
# ============================================================
with tab_zone:
    st.subheader("Zone Intelligence")
    st.caption("Inspect one zone's factor profile and weighted contributions.")

    selected_zone = st.selectbox("Select a zone", list(ZONES.keys()), key="zone_select")
    selected_values = ZONES[selected_zone]
    selected_scores = dict(zip(FACTORS, selected_values))
    selected_risk = calculate_risk(selected_scores)
    selected_priority = classify_risk(selected_risk)

    m1, m2, m3 = st.columns(3)
    m1.metric("Risk Index", f"{selected_risk}/100")
    m2.metric("Priority Level", selected_priority)
    m3.metric("Largest Raw Factor", max(selected_values))

    left, right = st.columns(2)

    with left:
        radar = go.Figure()
        radar.add_trace(go.Scatterpolar(
            r=selected_values + [selected_values[0]],
            theta=FACTORS + [FACTORS[0]],
            fill="toself",
            name=selected_zone,
            line=dict(color=CYAN, width=3),
            fillcolor="rgba(0,217,255,0.18)",
        ))
        radar.update_layout(
            title="Factor profile",
            polar=dict(
                bgcolor=PANEL,
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    gridcolor=BORDER,
                    tickfont=dict(color=MUTED),
                ),
                angularaxis=dict(gridcolor=BORDER, tickfont=dict(color=TEXT)),
            ),
        )
        st.plotly_chart(style_plot(radar, 420), use_container_width=True)

    with right:
        contributions = pd.DataFrame({
            "Factor": FACTORS,
            "Raw Score": selected_values,
            "Weight (%)": [WEIGHTS[f] * 100 for f in FACTORS],
            "Weighted Contribution": [
                round(selected_scores[f] * WEIGHTS[f], 2) for f in FACTORS
            ],
        })
        contribution_chart = px.bar(
            contributions,
            x="Factor",
            y="Weighted Contribution",
            color="Factor",
            title="Contribution to total index",
            text="Weighted Contribution",
            color_discrete_sequence=[CYAN, BLUE, PURPLE, GREEN, YELLOW],
        )
        contribution_chart.update_traces(textposition="outside")
        st.plotly_chart(
            style_plot(contribution_chart, 420),
            use_container_width=True,
        )

    st.markdown("### Factor breakdown")
    show_table(contributions, 260)

    st.markdown("### Suggested review focus")
    if selected_priority == "CRITICAL":
        st.warning(
            "Priority review: verify input assumptions, inspect the largest contributing "
            "factors, and consider whether expert assessment is needed."
        )
    elif selected_priority == "HIGH":
        st.warning(
            "Elevated review priority: check the most influential factors and identify "
            "practical prevention measures."
        )
    elif selected_priority == "MODERATE":
        st.info(
            "Moderate review priority: review the assumptions and consider measures "
            "that reduce exposure or vulnerability."
        )
    else:
        st.success(
            "Lower relative priority in this demonstration model. This is not a guarantee of safety."
        )

# ============================================================
# TAB 3: COMPARE ZONES
# ============================================================
with tab_compare:
    st.subheader("Compare Zones")
    st.caption("Compare factor scores across selected zones.")

    selected_zones = st.multiselect(
        "Choose zones to compare",
        options=list(ZONES.keys()),
        default=["Forest", "Residential Area", "Hospital"],
        key="compare_zones",
    )

    if selected_zones:
        compare_rows = []
        for zone in selected_zones:
            values = ZONES[zone]
            row = {"Zone": zone}
            row.update(dict(zip(FACTORS, values)))
            row["Risk Index"] = calculate_risk(dict(zip(FACTORS, values)))
            row["Priority"] = classify_risk(row["Risk Index"])
            compare_rows.append(row)

        compare_df = pd.DataFrame(compare_rows)
        melted = compare_df.melt(
            id_vars="Zone",
            value_vars=FACTORS,
            var_name="Factor",
            value_name="Score",
        )

        grouped = px.bar(
            melted,
            x="Zone",
            y="Score",
            color="Factor",
            barmode="group",
            title="Factor-by-factor comparison",
            color_discrete_sequence=[CYAN, BLUE, PURPLE, GREEN, YELLOW],
        )
        st.plotly_chart(style_plot(grouped, 420), use_container_width=True)

        st.markdown("### Comparison results")
        show_table(compare_df, 260)

        compare_radar = go.Figure()
        for zone in selected_zones:
            values = ZONES[zone]
            compare_radar.add_trace(go.Scatterpolar(
                r=values + [values[0]],
                theta=FACTORS + [FACTORS[0]],
                name=zone,
                fill="none",
            ))
        compare_radar.update_layout(
            title="Environmental factor profiles",
            polar=dict(
                bgcolor=PANEL,
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    gridcolor=BORDER,
                    tickfont=dict(color=MUTED),
                ),
                angularaxis=dict(gridcolor=BORDER, tickfont=dict(color=TEXT)),
            ),
        )
        st.plotly_chart(style_plot(compare_radar, 440), use_container_width=True)
    else:
        st.info("Select at least one zone to display comparisons.")

# ============================================================
# TAB 4: SCENARIO LAB
# ============================================================
with tab_scenario:
    st.subheader("Scenario Lab")
    st.caption(
        "Change illustrative factor values and observe how the weighted index responds. "
        "This is a hypothetical scenario tool, not a real-world prediction."
    )

    scenario_zone = st.selectbox(
        "Choose a zone for your scenario",
        list(ZONES.keys()),
        key="scenario_zone",
    )
    base_values = dict(zip(FACTORS, ZONES[scenario_zone]))

    st.markdown("### Adjust factor assumptions")
    slider_columns = st.columns(2)
    scenario_scores = {}

    for index, factor in enumerate(FACTORS):
        with slider_columns[index % 2]:
            scenario_scores[factor] = st.slider(
                f"{factor} score",
                min_value=0,
                max_value=100,
                value=int(base_values[factor]),
                step=1,
                key=f"scenario_{scenario_zone}_{factor}",
                help="Illustrative input from 0 to 100.",
            )

    baseline_score = calculate_risk(base_values)
    scenario_score = calculate_risk(scenario_scores)
    difference = round(scenario_score - baseline_score, 1)
    scenario_priority = classify_risk(scenario_score)

    st.markdown("### Scenario outcome")
    s1, s2, s3 = st.columns(3)
    s1.metric("Original Index", f"{baseline_score}/100")
    s2.metric("Scenario Index", f"{scenario_score}/100")
    s3.metric("Change", f"{difference:+.1f}", delta=f"{difference:+.1f}")

    st.markdown(
        f"**Scenario priority:** <span style='color:{priority_colour(scenario_priority)};"
        f"font-weight:bold'>{scenario_priority}</span>",
        unsafe_allow_html=True,
    )

    scenario_table = pd.DataFrame([
        {
            "Factor": factor,
            "Original Score": base_values[factor],
            "Scenario Score": scenario_scores[factor],
            "Weight (%)": WEIGHTS[factor] * 100,
            "New Contribution": round(scenario_scores[factor] * WEIGHTS[factor], 2),
        }
        for factor in FACTORS
    ])
    show_table(scenario_table, 260)

    scenario_chart = go.Figure()
    scenario_chart.add_trace(go.Bar(
        name="Original",
        x=FACTORS,
        y=[base_values[f] for f in FACTORS],
        marker_color=BLUE,
    ))
    scenario_chart.add_trace(go.Bar(
        name="Scenario",
        x=FACTORS,
        y=[scenario_scores[f] for f in FACTORS],
        marker_color=CYAN,
    ))
    scenario_chart.update_layout(
        title="Original vs scenario factor scores",
        barmode="group",
        yaxis=dict(range=[0, 100]),
    )
    st.plotly_chart(style_plot(scenario_chart, 390), use_container_width=True)

    st.caption(
        "A change in the index reflects the chosen inputs and fixed weights. It does not "
        "prove that actual environmental risk has changed."
    )

# ============================================================
# TAB 5: MISSION CONTROL
# ============================================================
with tab_mission:
    st.subheader("Mission Control")
    st.caption(
        "Use this checklist to structure a responsible environmental-risk review. "
        "It does not issue real emergency alerts."
    )

    checklist_items = [
        "Confirm the source and date of the input data",
        "Check whether scores are supported by evidence",
        "Identify the factors contributing most to the index",
        "Verify the assessment with relevant experts",
        "Identify feasible prevention or preparedness actions",
        "Record assumptions, uncertainty, and limitations",
    ]

    st.markdown("### Assessment checklist")
    checklist_columns = st.columns(2)
    completed = []

    for index, item in enumerate(checklist_items):
        with checklist_columns[index % 2]:
            completed.append(st.checkbox(item, key=f"mission_check_{index}"))

    completion_percent = int(sum(completed) / len(checklist_items) * 100)
    st.progress(completion_percent)
    st.write(f"Checklist progress: **{completion_percent}%**")

    st.markdown("### Current illustrative priorities")
    show_table(zone_df[["Zone", "Risk Index", "Priority"]], 260)

    st.markdown("### Generate a briefing")
    briefing_notes = st.text_area(
        "Add notes for your team",
        placeholder=(
            "Example: verify the assumptions for the highest-ranked zone and identify "
            "what additional data would be needed."
        ),
        height=120,
    )

    st.download_button(
        "⬇ Download mission briefing (TXT)",
        data=make_report(zone_df, briefing_notes, completion_percent),
        file_name="tera_mission_briefing.txt",
        mime="text/plain",
        key="mission_report",
    )

    st.warning(
        "TERA is an educational prototype. Do not use it as a substitute for official "
        "warnings, emergency services, professional environmental assessment, or validated forecasts."
    )

# ============================================================
# TAB 6: METHODOLOGY
# ============================================================
with tab_method:
    st.subheader("Methodology & Transparency")
    st.caption("How the index is calculated and what it means.")

    st.markdown("### Weighted risk-index formula")
    st.latex(r"R = 0.30H + 0.25V + 0.20P + 0.15E + 0.10U")
    st.write(
        "Each factor is scored from 0 to 100. The weighted contributions are added "
        "to produce an illustrative index from 0 to 100."
    )

    weights_df = pd.DataFrame({
        "Factor": FACTORS,
        "Weight": [WEIGHTS[f] for f in FACTORS],
        "Weight (%)": [WEIGHTS[f] * 100 for f in FACTORS],
        "Meaning": [
            "Illustrative hazard score",
            "Illustrative vulnerability score",
            "Illustrative population score",
            "Illustrative exposure score",
            "Illustrative urgency score",
        ],
    })
    show_table(weights_df, 260)

    st.markdown("### Classification thresholds")
    thresholds_df = pd.DataFrame([
        {"Priority": "CRITICAL", "Index Range": "80–100"},
        {"Priority": "HIGH", "Index Range": "65–79.9"},
        {"Priority": "MODERATE", "Index Range": "45–64.9"},
        {"Priority": "LOWER", "Index Range": "Below 45"},
    ])
    show_table(thresholds_df, 220)

    st.markdown("### What this prototype does")
    st.markdown(
        """
        - Stores illustrative scores for six example environmental zones.
        - Calculates a weighted priority index using fixed factor weights.
        - Classifies zones using predefined thresholds.
        - Displays interactive charts and comparisons.
        - Allows users to explore hypothetical scenarios.
        - Exports tables and a text briefing.
        """
    )

    st.markdown("### What this prototype does not do")
    st.markdown(
        """
        - It does not use live sensor, satellite, or weather feeds.
        - It does not provide a scientifically validated disaster forecast.
        - It does not calculate the probability of a disaster.
        - It does not contain a trained machine-learning model in this version.
        - It does not replace expert assessment or official emergency alerts.
        """
    )

    st.markdown("### Technology stack")
    technology_df = pd.DataFrame([
        {"Technology": "Python", "Purpose": "Calculations and application logic"},
        {"Technology": "Streamlit", "Purpose": "Interactive dashboard interface"},
        {"Technology": "Pandas", "Purpose": "Organising tabular data"},
        {"Technology": "Plotly", "Purpose": "Interactive visualisations"},
        {"Technology": "GitHub", "Purpose": "Source-code version control"},
    ])
    show_table(technology_df, 250)

    st.markdown("### Download complete results")
    st.download_button(
        "⬇ Download complete results (CSV)",
        data=zone_df.to_csv(index=False).encode("utf-8"),
        file_name="tera_2_complete_results.csv",
        mime="text/csv",
        key="method_csv",
    )
    st.download_button(
        "⬇ Download methodology report (TXT)",
        data=make_report(zone_df),
        file_name="tera_2_methodology_report.txt",
        mime="text/plain",
        key="method_txt",
    )

# -------------------- FOOTER --------------------
st.divider()
st.markdown(
    f"""
    <div style="text-align:center; padding:10px; color:{MUTED};">
        <div style="color:{CYAN}; font-weight:800; letter-spacing:2px;">
            TERA 2.0 • MIDNIGHT INTELLIGENCE
        </div>
        <div style="font-size:12px; margin-top:6px;">
            Technology for Environmental Risk Analysis
        </div>
        <div style="font-size:11px; margin-top:5px;">
            Educational prototype · Illustrative inputs · Not an operational early-warning system
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
