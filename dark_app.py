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

PLOT_CONFIG = {
    "displayModeBar": True,
    "displaylogo": False,
    "editable": True,
    "toImageButtonOptions": {
        "format": "png",
        "filename": "TERA_chart",
        "scale": 2,
    },
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
    div[data-testid="stTabs"] button[aria-selected="true"] {{
        color: {CYAN} !important;
        border-bottom-color: {CYAN} !important;
    }}
    .stButton button, .stDownloadButton button {{
        border-radius: 10px;
        border: 1px solid #28758A;
        background: linear-gradient(90deg, #0E5268, #087C83);
        color: #FFFFFF !important;
        font-weight: 800;
    }}
    .stButton button:hover, .stDownloadButton button:hover {{
        border-color: {MINT};
        color: #FFFFFF !important;
    }}

    /* Streamlit dataframe dark palette */
    [data-testid="stDataFrame"] {{
        background: {PANEL} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        color-scheme: dark !important;
    }}
    [data-testid="stDataFrame"] > div,
    [data-testid="stDataFrame"] [data-testid="glideDataEditor"],
    [data-testid="stDataFrame"] canvas {{
        background-color: {PANEL} !important;
        color-scheme: dark !important;
    }}
    [data-testid="stDataFrame"] [data-testid="glideDataEditor"] {{
        --gdg-bg-cell: {PANEL};
        --gdg-bg-cell-medium: {ALT};
        --gdg-bg-header: {ALT};
        --gdg-bg-header-has-focus: {ALT};
        --gdg-bg-header-hovered: {ALT};
        --gdg-text-dark: {TEXT};
        --gdg-text-medium: {MUTED};
        --gdg-text-light: {MUTED};
        --gdg-text-header: {CYAN};
        --gdg-border-color: {BORDER};
        --gdg-accent-color: {CYAN};
        --gdg-link-color: {CYAN};
    }}
    [data-testid="stTable"] {{
        background: {PANEL} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }}
    [data-testid="stTable"] table,
    [data-testid="stTable"] tbody,
    [data-testid="stTable"] tr,
    [data-testid="stTable"] td {{
        background: {PANEL} !important;
        color: {TEXT} !important;
        border-color: {BORDER} !important;
    }}
    [data-testid="stTable"] thead th {{
        background: {ALT} !important;
        color: {CYAN} !important;
        border-color: {BORDER} !important;
    }}
    [data-testid="stAlert"] {{
        background: {ALT};
        border: 1px solid {BORDER};
    }}
    .eyebrow {{
        color: {CYAN};
        font-size: .75rem;
        font-weight: 800;
        letter-spacing: 2px;
    }}
    .hero {{
        font-size: 2.1rem;
        font-weight: 800;
        line-height: 1.2;
        color: {TEXT};
    }}
    .pill {{
        display: inline-block;
        padding: 5px 10px;
        border-radius: 999px;
        border: 1px solid {BORDER};
        color: {MINT};
        font-size: .75rem;
        font-weight: 800;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------- SESSION STATE --------------------
if "zone_values" not in st.session_state:
    st.session_state.zone_values = {
        k: v.copy() for k, v in DEFAULT_ZONES.items()
    }

if "factor_weights" not in st.session_state:
    st.session_state.factor_weights = DEFAULT_WEIGHTS.copy()


def effective_weights():
    """Normalise entered slider weights so effective total is 100%."""
    raw = st.session_state.factor_weights
    total = sum(raw.values())

    if total == 0:
        return {factor: 20.0 for factor in FACTORS}

    return {
        factor: raw[factor] / total * 100
        for factor in FACTORS
    }


def rpi(values):
    w = effective_weights()
    return sum(
        float(values[i]) * w[factor] / 100
        for i, factor in enumerate(FACTORS)
    )


def level(score):
    if score >= 80:
        return "CRITICAL"
    if score >= 65:
        return "HIGH"
    if score >= 45:
        return "MODERATE"
    return "LOWER"


def dataframe():
    rows = []

    for zone_name, vals in st.session_state.zone_values.items():
        score = rpi(vals)

        rows.append({
            "Zone": zone_name,
            **dict(zip(FACTORS, vals)),
            "RPI": round(score, 1),
            "Classification": level(score),
        })

    return (
        pd.DataFrame(rows)
        .sort_values("RPI", ascending=False)
        .reset_index(drop=True)
    )


def style_fig(fig, height=340, chart_id="tera-chart"):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=TEXT, family="Manrope"),
        margin=dict(l=10, r=10, t=48, b=12),
        legend=dict(font=dict(color=TEXT)),
        uirevision=chart_id,
    )
    return fig


def show_chart(fig, key, height=340):
    st.plotly_chart(
        style_fig(fig, height, key),
        use_container_width=True,
        config=PLOT_CONFIG,
        key=key,
    )


def reset_weights_callback():
    st.session_state.factor_weights = DEFAULT_WEIGHTS.copy()

    for factor, value in DEFAULT_WEIGHTS.items():
        st.session_state[f"weight_{factor}"] = value


def reset_selected_zone_callback():
    selected = st.session_state.get(
        "edit_zone_select",
        list(DEFAULT_ZONES)[0],
    )

    st.session_state.zone_values[selected] = (
        DEFAULT_ZONES[selected].copy()
    )

    for factor, value in zip(
        FACTORS,
        DEFAULT_ZONES[selected],
    ):
        st.session_state[f"score_{selected}_{factor}"] = value


def reset_all_callback():
    st.session_state.zone_values = {
        name: values.copy()
        for name, values in DEFAULT_ZONES.items()
    }

    st.session_state.factor_weights = DEFAULT_WEIGHTS.copy()

    for factor, value in DEFAULT_WEIGHTS.items():
        st.session_state[f"weight_{factor}"] = value

    for zone_name, zone_values in DEFAULT_ZONES.items():
        for factor, value in zip(FACTORS, zone_values):
            st.session_state[f"score_{zone_name}_{factor}"] = value


# -------------------- HEADER --------------------
st.markdown(
    '<div class="eyebrow">ENVIRONMENTAL INTELLIGENCE PLATFORM</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="hero">TERA 2.0 <span style="color:#38D6E8">/</span> MIDNIGHT INTELLIGENCE</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<span class="pill">LIVE SIMULATION</span> &nbsp; Technology for Environmental Risk Analysis',
    unsafe_allow_html=True,
)

# -------------------- SIDEBAR SLIDERS --------------------
with st.sidebar:
    st.markdown("## 🌍 TERA CONTROL")
    st.caption("MIDNIGHT INTELLIGENCE EDITION")
    st.divider()

    st.markdown("### Editable factor weights")
    st.caption(
        "Change these sliders; effective weights are automatically normalised to 100%."
    )

    for factor in FACTORS:
        new_weight = st.slider(
            f"{factor} weight",
            min_value=0,
            max_value=100,
            value=int(st.session_state.factor_weights[factor]),
            step=1,
            key=f"weight_{factor}",
        )

        st.session_state.factor_weights[factor] = new_weight

    st.metric(
        "Entered weight total",
        f"{sum(st.session_state.factor_weights.values())}%",
    )

    st.button(
        "Reset weights",
        key="reset_weights",
        on_click=reset_weights_callback,
    )

    st.divider()
    st.markdown("### Editable zone scores")

    edit_zone = st.selectbox(
        "Select zone to edit",
        list(st.session_state.zone_values),
        key="edit_zone_select",
    )

    for i, factor in enumerate(FACTORS):
        new_value = st.slider(
            f"{edit_zone} · {factor}",
            min_value=0,
            max_value=100,
            value=int(st.session_state.zone_values[edit_zone][i]),
            step=1,
            key=f"score_{edit_zone}_{factor}",
        )

        st.session_state.zone_values[edit_zone][i] = new_value

    st.button(
        "Reset selected zone",
        key="reset_selected_zone",
        on_click=reset_selected_zone_callback,
    )

    st.button(
        "Reset all model data",
        key="reset_all_model_data",
        on_click=reset_all_callback,
    )

# Recalculate all data AFTER reading the slider state.
df = dataframe()
top = df.iloc[0]

tabs = st.tabs([
    "⌂ Command Centre",
    "◈ Zone Intelligence",
    "⇄ Compare Zones",
    "⌁ Scenario Lab",
    "✚ Mission Control",
    "ⓘ Methodology",
])

# ============================================================
# TAB 1: COMMAND CENTRE
# ============================================================
with tabs[0]:
    st.markdown("## Command Centre")

    a, b, c, d = st.columns(4)

    a.metric("Average RPI", f"{df.RPI.mean():.1f}/100")
    b.metric("Highest priority", top.Zone)
    c.metric(
        "Critical zones",
        int((df.Classification == "CRITICAL").sum()),
    )
    d.metric(
        "High-priority zones",
        int((df.Classification == "HIGH").sum()),
    )

    left, right = st.columns([1.2, 1])

    with left:
        st.markdown("### Zone risk ranking")

        ranking = df.sort_values("RPI")

        fig = px.bar(
            ranking,
            x="RPI",
            y="Zone",
            orientation="h",
            color="Classification",
            color_discrete_map=COLORS,
            text="RPI",
        )

        fig.update_traces(
            texttemplate="%{text:.1f}",
            textposition="outside",
            cliponaxis=False,
        )

        fig.update_xaxes(
            range=[0, 110],
            gridcolor=BORDER,
            title="Risk Priority Index",
        )
        fig.update_yaxes(title="")

        show_chart(fig, "command_risk_ranking", 370)

    with right:
        st.markdown("### Risk classification mix")

        counts = (
            df["Classification"]
            .value_counts()
            .reindex(PRIORITY_ORDER, fill_value=0)
        )

        pie_df = pd.DataFrame({
            "Classification": counts.index,
            "Zones": counts.values,
        })

        pie_df = pie_df[pie_df["Zones"] > 0]

        if pie_df.empty:
            st.info("No classification data is available yet.")
        else:
            pie = px.pie(
                pie_df,
                names="Classification",
                values="Zones",
                hole=0.68,
                color="Classification",
                color_discrete_map=COLORS,
            )

            pie.update_traces(
                textposition="outside",
                textinfo="label+value+percent",
            )

            pie.add_annotation(
                text=f"<b>{len(df)}</b><br><span style='font-size:11px'>ZONES</span>",
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(color=TEXT, size=20),
            )

            show_chart(pie, "command_classification_pie", 370)

        st.caption(
            "Live classification counts: changes whenever a zone score or factor weight changes."
        )

    st.markdown("### Live zone intelligence")

    shown = df.copy()
    shown["RPI"] = shown["RPI"].map(
        lambda value: f"{value:.1f}"
    )

    st.dataframe(
        shown,
        use_container_width=True,
        hide_index=True,
    )

# ============================================================
# TAB 2: ZONE INTELLIGENCE
# ============================================================
with tabs[1]:
    st.markdown("## Zone Intelligence")

    zone = st.selectbox(
        "Inspect a zone",
        list(st.session_state.zone_values),
        key="inspect_zone",
    )

    vals = st.session_state.zone_values[zone]
    score = rpi(vals)

    x, y, z = st.columns(3)

    x.metric("Risk Priority Index", f"{score:.1f}/100")
    y.metric("Classification", level(score))
    z.metric(
        "Highest factor",
        FACTORS[vals.index(max(vals))],
    )

    left, right = st.columns(2)

    with left:
        st.markdown("### Factor profile")

        radar = go.Figure(
            go.Scatterpolar(
                r=vals + [vals[0]],
                theta=FACTORS + [FACTORS[0]],
                fill="toself",
                line=dict(color=CYAN, width=3),
                fillcolor="rgba(56,214,232,.2)",
                name=zone,
            )
        )

        radar.update_layout(
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    gridcolor=BORDER,
                    color=MUTED,
                ),
                angularaxis=dict(
                    gridcolor=BORDER,
                    color=TEXT,
                ),
            ),
            showlegend=False,
        )

        show_chart(radar, "zone_factor_radar", 360)

    with right:
        st.markdown("### Editable factor contribution mix")

        w = effective_weights()

        contributions = [
            vals[i] * w[factor] / 100
            for i, factor in enumerate(FACTORS)
        ]

        contribution_df = pd.DataFrame({
            "Factor": FACTORS,
            "Contribution": contributions,
        })

        visible_contributions = contribution_df[
            contribution_df["Contribution"] > 0
        ]

        if visible_contributions.empty:
            st.info(
                "All factor contributions are currently zero. Increase a factor score or weight."
            )
        else:
            contribution_pie = px.pie(
                visible_contributions,
                names="Factor",
                values="Contribution",
                hole=0.58,
                color="Factor",
                color_discrete_map=dict(
                    zip(FACTORS, FACTOR_COLORS)
                ),
            )

            contribution_pie.update_traces(
                textposition="outside",
                textinfo="label+percent",
            )

            show_chart(
                contribution_pie,
                "zone_factor_contribution_pie",
                360,
            )

        st.caption(
            "This pie recalculates from the inspected zone's five factor scores and the live weight sliders."
        )

    st.markdown("### Factor values")

    metric_cols = st.columns(5)

    for i, factor in enumerate(FACTORS):
        metric_cols[i].metric(factor, f"{vals[i]}/100")

# ============================================================
# TAB 3: COMPARE ZONES
# ============================================================
with tabs[2]:
    st.markdown("## Compare Zones")

    c1, c2 = st.columns(2)
    zone_names = list(st.session_state.zone_values)

    za = c1.selectbox(
        "First zone",
        zone_names,
        key="compare_a",
    )

    zb = c2.selectbox(
        "Second zone",
        zone_names,
        index=1,
        key="compare_b",
    )

    if za == zb:
        st.info("Choose two different zones.")
    else:
        comp = pd.DataFrame({
            "Factor": FACTORS,
            za: st.session_state.zone_values[za],
            zb: st.session_state.zone_values[zb],
        }).melt(
            "Factor",
            var_name="Zone",
            value_name="Score",
        )

        fig = px.bar(
            comp,
            x="Factor",
            y="Score",
            color="Zone",
            barmode="group",
            color_discrete_sequence=[CYAN, MINT],
            text="Score",
        )

        fig.update_yaxes(
            range=[0, 110],
            gridcolor=BORDER,
            title="Factor score",
        )
        fig.update_xaxes(title="")
        fig.update_traces(textposition="outside")

        show_chart(fig, "compare_zone_factor_bars", 400)

        ca, cb = st.columns(2)

        ca.metric(
            f"{za} RPI",
            f"{rpi(st.session_state.zone_values[za]):.1f}",
        )
        cb.metric(
            f"{zb} RPI",
            f"{rpi(st.session_state.zone_values[zb]):.1f}",
        )

# ============================================================
# TAB 4: SCENARIO LAB
# ============================================================
with tabs[3]:
    st.markdown("## Scenario Lab")
    st.caption(
        "Hypothetical scenario adjustments only; not a forecast."
    )

    scenario = st.selectbox(
        "Choose scenario",
        [
            "Baseline — current model",
            "Heavy rainfall / flood pressure",
            "Industrial air-pollution incident",
            "Extreme heat / medical strain",
        ],
    )

    adjustments = {
        "Baseline — current model": {},
        "Heavy rainfall / flood pressure": {
            "River & Dam": [15, 5, 0, 10, 15],
            "Residential Area": [5, 5, 0, 0, 5],
        },
        "Industrial air-pollution incident": {
            "Industrial Zone": [15, 5, 0, 10, 10],
            "Residential Area": [5, 5, 0, 5, 5],
        },
        "Extreme heat / medical strain": {
            "Hospital": [5, 10, 5, 0, 15],
            "Residential Area": [10, 10, 5, 0, 10],
        },
    }

    rows = []

    for zone_name, base in st.session_state.zone_values.items():
        adj = adjustments[scenario].get(
            zone_name,
            [0] * 5,
        )

        changed = [
            max(0, min(100, base[i] + adj[i]))
            for i in range(5)
        ]

        rows.append({
            "Zone": zone_name,
            "Scenario RPI": round(rpi(changed), 1),
        })

    scenario_df = (
        pd.DataFrame(rows)
        .sort_values("Scenario RPI", ascending=False)
    )

    st.metric(
        "Top scenario priority",
        scenario_df.iloc[0].Zone,
        f"RPI {scenario_df.iloc[0]['Scenario RPI']:.1f}",
    )

    fig = px.bar(
        scenario_df.sort_values("Scenario RPI"),
        x="Scenario RPI",
        y="Zone",
        orientation="h",
        color="Scenario RPI",
        color_continuous_scale=[
            "#63D9A5",
            "#FFB454",
            "#FF5C70",
        ],
        text="Scenario RPI",
    )

    fig.update_xaxes(
        range=[0, 110],
        gridcolor=BORDER,
    )
    fig.update_yaxes(title="")
    fig.update_layout(coloraxis_showscale=False)

    show_chart(fig, "scenario_priority_bars", 350)

    st.dataframe(
        scenario_df,
        use_container_width=True,
        hide_index=True,
    )

# ============================================================
# TAB 5: MISSION CONTROL
# ============================================================
with tabs[4]:
    st.markdown("## Mission Control")

    st.caption(
        "Simplified educational planning exercise — not real emergency-response guidance."
    )

    mission = st.selectbox(
        "Mission type",
        [
            "Flood readiness",
            "Air-quality incident",
            "Extreme-heat support",
        ],
    )

    action_map = {
        "Flood readiness": [
            "Drainage and water-flow checks",
            "Community alerts",
            "Shelter readiness",
        ],
        "Air-quality incident": [
            "Air-quality monitoring",
            "Public information",
            "Protective indoor spaces",
        ],
        "Extreme-heat support": [
            "Cooling access",
            "Health advisories",
            "Water availability",
        ],
    }

    actions = action_map[mission]

    st.write("Allocate **10 illustrative response units**.")

    cols = st.columns(3)
    allocations = []

    for i, action in enumerate(actions):
        with cols[i]:
            allocations.append(
                st.number_input(
                    action,
                    min_value=0,
                    max_value=10,
                    value=[4, 3, 3][i],
                    step=1,
                    key=f"mission_{mission}_{i}",
                )
            )

    total = sum(allocations)

    st.metric("Units allocated", f"{total}/10")

    if total == 10:
        st.success("Allocation complete — all 10 units used.")
    elif total < 10:
        st.info(f"{10 - total} units remaining.")
    else:
        st.warning(f"Reduce allocation by {total - 10} units.")

    if st.button("Evaluate mission allocation"):
        if total == 10:
            st.success(
                f"Plan recorded across {sum(value > 0 for value in allocations)} action areas."
            )
        else:
            st.error(
                "Allocate exactly 10 units before evaluating."
            )

# ============================================================
# TAB 6: METHODOLOGY & AI
# ============================================================
with tabs[5]:
    st.markdown("## Methodology & AI")
    st.markdown("### Risk Priority Index")

    st.latex(
        r"RPI = 0.30H + 0.25V + 0.20P + 0.15E + 0.10U"
    )

    st.write(
        "The RPI is a weighted priority index based on five illustrative factor scores, "
        "each from 0 to 100. The effective weights shown below are normalised from the sliders."
    )

    w = effective_weights()

    weights_df = pd.DataFrame({
        "Factor": FACTORS,
        "Entered weight": [
            st.session_state.factor_weights[factor]
            for factor in FACTORS
        ],
        "Effective weight (%)": [
            round(w[factor], 1)
            for factor in FACTORS
        ],
    })

    st.dataframe(
        weights_df,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("### Classification thresholds")

    st.dataframe(
        pd.DataFrame({
            "Classification": PRIORITY_ORDER,
            "RPI range": [
                "80–100",
                "65–79.9",
                "45–64.9",
                "Below 45",
            ],
        }),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("### What TERA does")
    st.write("- Combines factor scores using visible, editable weights.")
    st.write("- Calculates and ranks each zone's Risk Priority Index.")
    st.write("- Updates charts and classifications when sliders change.")

    st.markdown("### What TERA does not do")
    st.write("- It is not a trained machine-learning model.")
    st.write("- It does not read live sensors or verified real-time environmental conditions.")
    st.write("- Scores are not probabilities or validated disaster predictions.")
    st.write("- Real-world use requires verified data, expert review and validation.")

# -------------------- FOOTER --------------------
st.divider()

st.markdown(
    f"""
    <div style="text-align:center;color:{MUTED};font-size:.78rem;">
        TERA 2.0 · MIDNIGHT INTELLIGENCE · Educational decision-support simulation<br>
        Illustrative inputs only · Not a real emergency forecast or operational response system
    </div>
    """,
    unsafe_allow_html=True,
)
