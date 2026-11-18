"""
Nebula AI Analytics — Streamlit Clean Light Glassmorphism Theme Template
=====================================================================

A production-style dashboard template featuring:
- Clean light-mode glassmorphism design system (CSS injected via st.markdown)
- Frosted white glass cards, soft shadows, and clean typography
- Sidebar navigation, tabbed analytics panels, and an AI insight feed
- Plotly charts restyled to match the light theme
- Synthetic demo data so the app runs with zero external dependencies

Run with:
    pip install streamlit plotly numpy pandas
    streamlit run app.py
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Nebula AI Analytics",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# 2. THEME TOKENS (Clean Light Theme)
# ---------------------------------------------------------------------------
THEME = {
    "bg_primary": "#F4F6FB",
    "bg_secondary": "#FFFFFF",
    "glass_fill": "rgba(255, 255, 255, 0.78)",
    "glass_border": "rgba(15, 23, 42, 0.08)",
    "text_primary": "#0F172A",
    "text_muted": "#64748B",
    "accent_1": "#6366F1",   # Indigo
    "accent_2": "#0EA5E9",   # Sky Blue
    "accent_3": "#EC4899",   # Pink
    "success": "#10B981",    # Emerald
    "danger": "#F43F5E",     # Rose
}


# ---------------------------------------------------------------------------
# 3. CUSTOM CSS (Light glassmorphism)
# ---------------------------------------------------------------------------
def inject_custom_css() -> None:
    """Inject the full light theme stylesheet into the Streamlit page."""
    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* ---------- Global base ---------- */
    html, body, [class*="css"], .stApp {{
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
        color: {THEME['text_primary']};
    }}

    /* Light animated gradient background */
    .stApp {{
        background:
            radial-gradient(circle at 12% 18%, rgba(99, 102, 241, 0.12) 0%, transparent 40%),
            radial-gradient(circle at 88% 12%, rgba(14, 165, 233, 0.12) 0%, transparent 38%),
            radial-gradient(circle at 60% 92%, rgba(236, 72, 153, 0.08) 0%, transparent 42%),
            linear-gradient(160deg, {THEME['bg_primary']} 0%, {THEME['bg_secondary']} 100%);
        background-attachment: fixed;
    }}

    /* Hide Streamlit chrome */
    #MainMenu, footer, header {{ visibility: hidden; }}
    .block-container {{
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }}

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {{
        background: rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: blur(20px) saturate(160%);
        -webkit-backdrop-filter: blur(20px) saturate(160%);
        border-right: 1px solid {THEME['glass_border']};
    }}
    section[data-testid="stSidebar"] * {{ color: {THEME['text_primary']}; }}

    /* ---------- Typography ---------- */
    .hero-title {{
        font-size: 2.6rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(90deg, {THEME['accent_1']}, {THEME['accent_2']}, {THEME['accent_3']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }}
    .hero-sub {{
        color: {THEME['text_muted']};
        font-size: 1.02rem;
        margin-bottom: 1.8rem;
    }}
    .section-title {{
        font-size: 1.15rem;
        font-weight: 700;
        margin: 1.6rem 0 0.8rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: {THEME['text_primary']};
    }}
    .section-title::before {{
        content: "";
        width: 6px;
        height: 18px;
        border-radius: 4px;
        background: linear-gradient(180deg, {THEME['accent_1']}, {THEME['accent_2']});
        box-shadow: 0 0 10px rgba(99, 102, 241, 0.3);
    }}

    /* ---------- Glass card (reusable) ---------- */
    .glass-card {{
        background: {THEME['glass_fill']};
        border: 1px solid {THEME['glass_border']};
        border-radius: 20px;
        padding: 1.4rem 1.5rem;
        backdrop-filter: blur(16px) saturate(160%);
        -webkit-backdrop-filter: blur(16px) saturate(160%);
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.05), inset 0 1px 0 rgba(255, 255, 255, 0.9);
        transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
    }}
    .glass-card:hover {{
        transform: translateY(-3px);
        border-color: rgba(99, 102, 241, 0.35);
        box-shadow: 0 16px 36px rgba(99, 102, 241, 0.12), inset 0 1px 0 rgba(255, 255, 255, 1);
    }}

    /* ---------- Styled KPI metric cards ---------- */
    .kpi-card {{
        position: relative;
        overflow: hidden;
    }}
    .kpi-card::after {{
        content: "";
        position: absolute;
        top: -40%;
        right: -20%;
        width: 140px;
        height: 140px;
        border-radius: 50%;
        background: radial-gradient(circle, var(--glow, {THEME['accent_1']}) 0%, transparent 70%);
        opacity: 0.15;
        pointer-events: none;
    }}
    .kpi-label {{
        color: {THEME['text_muted']};
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 600;
    }}
    .kpi-value {{
        font-size: 2.1rem;
        font-weight: 800;
        margin: 0.35rem 0 0.25rem 0;
        letter-spacing: -0.02em;
        color: {THEME['text_primary']};
    }}
    .kpi-delta {{
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        padding: 0.18rem 0.6rem;
        border-radius: 999px;
    }}
    .kpi-delta.up {{
        color: #047857;
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.25);
    }}
    .kpi-delta.down {{
        color: #BE123C;
        background: rgba(244, 63, 94, 0.12);
        border: 1px solid rgba(244, 63, 94, 0.25);
    }}

    /* Native st.metric restyled */
    div[data-testid="stMetric"] {{
        background: {THEME['glass_fill']};
        border: 1px solid {THEME['glass_border']};
        border-radius: 18px;
        padding: 1rem 1.2rem;
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        box-shadow: 0 4px 20px rgba(15, 23, 42, 0.03);
    }}
    div[data-testid="stMetricValue"] {{
        font-weight: 800;
        color: {THEME['text_primary']};
    }}
    div[data-testid="stMetricLabel"] p {{
        color: {THEME['text_muted']} !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-size: 0.75rem !important;
    }}

    /* ---------- Glowing buttons ---------- */
    div.stButton > button,
    div.stDownloadButton > button {{
        background: linear-gradient(135deg, {THEME['accent_1']}, {THEME['accent_2']});
        color: #ffffff;
        border: none;
        border-radius: 14px;
        padding: 0.65rem 1.4rem;
        font-weight: 700;
        letter-spacing: 0.02em;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35);
        transition: all 0.25s ease;
    }}
    div.stButton > button:hover,
    div.stDownloadButton > button:hover {{
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5);
        color: #ffffff;
    }}
    div.stButton > button:active {{ transform: scale(0.98); }}

    /* ---------- Tabs ---------- */
    div[data-baseweb="tab-list"] {{
        gap: 0.5rem;
        background: rgba(255, 255, 255, 0.6);
        border: 1px solid {THEME['glass_border']};
        border-radius: 14px;
        padding: 0.35rem;
        width: fit-content;
    }}
    button[data-baseweb="tab"] {{
        background: transparent !important;
        border-radius: 10px !important;
        color: {THEME['text_muted']} !important;
        font-weight: 600;
        padding: 0.45rem 1rem !important;
    }}
    button[data-baseweb="tab"][aria-selected="true"] {{
        color: {THEME['text_primary']} !important;
        background: #ffffff !important;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.08);
    }}
    div[data-baseweb="tab-highlight"], div[data-baseweb="tab-border"] {{ display: none; }}

    /* ---------- Inputs ---------- */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    .stTextInput input, .stTextArea textarea {{
        background: rgba(255, 255, 255, 0.8) !important;
        border: 1px solid {THEME['glass_border']} !important;
        border-radius: 12px !important;
        color: {THEME['text_primary']} !important;
    }}

    /* ---------- AI insight feed ---------- */
    .insight {{
        display: flex;
        gap: 0.9rem;
        align-items: flex-start;
        padding: 0.95rem 1rem;
        border-radius: 14px;
        background: rgba(255, 255, 255, 0.5);
        border: 1px solid {THEME['glass_border']};
        margin-bottom: 0.7rem;
        transition: background 0.2s ease;
    }}
    .insight:hover {{ background: rgba(255, 255, 255, 0.9); }}
    .insight-dot {{
        width: 10px; height: 10px; margin-top: 0.4rem; border-radius: 50%;
        flex-shrink: 0;
        box-shadow: 0 0 8px currentColor;
    }}
    .insight-title {{ font-weight: 700; font-size: 0.95rem; color: {THEME['text_primary']}; }}
    .insight-body {{ color: {THEME['text_muted']}; font-size: 0.88rem; margin-top: 0.15rem; }}

    /* ---------- Badges ---------- */
    .badge {{
        display: inline-block;
        padding: 0.2rem 0.65rem;
        border-radius: 999px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        background: rgba(99, 102, 241, 0.1);
        color: {THEME['accent_1']};
        border: 1px solid rgba(99, 102, 241, 0.2);
    }}

    /* ---------- Scrollbar ---------- */
    ::-webkit-scrollbar {{ width: 8px; height: 8px; }}
    ::-webkit-scrollbar-thumb {{
        background: rgba(99, 102, 241, 0.25);
        border-radius: 10px;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# 4. REUSABLE UI COMPONENTS
# ---------------------------------------------------------------------------
def kpi_card(label: str, value: str, delta: str, positive: bool, glow: str) -> str:
    arrow = "▲" if positive else "▼"
    direction = "up" if positive else "down"
    return f"""
    <div class="glass-card kpi-card" style="--glow:{glow};">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <span class="kpi-delta {direction}">{arrow} {delta}</span>
    </div>
    """


def section_title(text: str) -> None:
    st.markdown(f'<div class="section-title">{text}</div>', unsafe_allow_html=True)


def insight_item(title: str, body: str, color: str) -> str:
    return f"""
    <div class="insight">
        <div class="insight-dot" style="background:{color}; color:{color};"></div>
        <div>
            <div class="insight-title">{title}</div>
            <div class="insight-body">{body}</div>
        </div>
    </div>
    """


def styled_plotly(fig: go.Figure, height: int = 360) -> go.Figure:
    fig.update_layout(
        height=height,
        margin=dict(l=10, r=10, t=30, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, system-ui", color=THEME["text_muted"]),
        legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", y=1.08, x=0),
        hoverlabel=dict(
            bgcolor="rgba(255,255,255,0.95)",
            bordercolor=THEME["glass_border"],
            font=dict(color=THEME["text_primary"]),
        ),
    )
    fig.update_xaxes(showgrid=False, zeroline=False, linecolor=THEME["glass_border"])
    fig.update_yaxes(gridcolor="rgba(15,23,42,0.06)", zeroline=False)
    return fig


# ---------------------------------------------------------------------------
# 5. DEMO DATA
# ---------------------------------------------------------------------------
@st.cache_data
def generate_demo_data(days: int = 90, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.date_range(end=pd.Timestamp.today().normalize(), periods=days, freq="D")
    trend = np.linspace(0, 1, days)
    requests = (1200 + 900 * trend + rng.normal(0, 120, days)).clip(min=200)
    latency = (320 - 40 * trend + rng.normal(0, 25, days)).clip(min=80)
    accuracy = (0.91 + 0.05 * trend + rng.normal(0, 0.008, days)).clip(0.8, 0.99)
    cost = requests * rng.uniform(0.0018, 0.0022, days)
    return pd.DataFrame({
        "date": dates,
        "requests": requests.round(0).astype(int),
        "latency_ms": latency.round(1),
        "accuracy": accuracy.round(4),
        "cost_usd": cost.round(2),
    })


@st.cache_data
def generate_model_breakdown() -> pd.DataFrame:
    return pd.DataFrame({
        "model": ["Nova-Large", "Nova-Mini", "Vision-Pro", "Embed-v3", "Audio-Lite"],
        "share": [38, 27, 18, 11, 6],
    })


# ---------------------------------------------------------------------------
# 6. SIDEBAR
# ---------------------------------------------------------------------------
def render_sidebar() -> dict:
    with st.sidebar:
        st.markdown(
            '<div class="hero-title" style="font-size:1.6rem;">✨ Nebula</div>'
            '<div class="hero-sub" style="margin-bottom:1rem;">AI Analytics Suite</div>',
            unsafe_allow_html=True,
        )
        st.markdown('<span class="badge">Live Demo</span>', unsafe_allow_html=True)
        st.markdown("---")

        page = st.radio(
            "Navigate",
            ["Overview", "Models", "Insights", "Settings"],
            label_visibility="collapsed",
        )
        st.markdown("---")

        date_range = st.select_slider(
            "Lookback window (days)",
            options=[7, 14, 30, 60, 90],
            value=90,
        )
        model_filter = st.multiselect(
            "Models",
            ["Nova-Large", "Nova-Mini", "Vision-Pro", "Embed-v3", "Audio-Lite"],
            default=["Nova-Large", "Nova-Mini", "Vision-Pro"],
        )

        st.markdown("---")
        st.markdown("**Refresh data**")
        if st.button("⚡ Run analysis", use_container_width=True):
            st.toast("Analysis queued — insights updated!", icon="✨")

    return {"page": page, "days": date_range, "models": model_filter}


# ---------------------------------------------------------------------------
# 7. PAGES
# ---------------------------------------------------------------------------
def render_overview(df: pd.DataFrame) -> None:
    st.markdown('<div class="hero-title">AI Performance Overview</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-sub">Real-time health of your AI inference fleet.</div>',
        unsafe_allow_html=True,
    )

    total_requests = int(df["requests"].sum())
    avg_latency = df["latency_ms"].mean()
    avg_accuracy = df["accuracy"].mean() * 100
    total_cost = df["cost_usd"].sum()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(kpi_card("Total requests", f"{total_requests:,}", "+12.4%", True, THEME["accent_1"]),
                    unsafe_allow_html=True)
    with c2:
        st.markdown(kpi_card("Avg latency", f"{avg_latency:.0f} ms", "-8.1%", True, THEME["accent_2"]),
                    unsafe_allow_html=True)
    with c3:
        st.markdown(kpi_card("Accuracy", f"{avg_accuracy:.1f}%", "+1.3%", True, THEME["accent_3"]),
                    unsafe_allow_html=True)
    with c4:
        st.markdown(kpi_card("Spend", f"${total_cost:,.0f}", "+5.6%", False, THEME["success"]),
                    unsafe_allow_html=True)

    st.write("")

    left, right = st.columns([2.3, 1])
    with left:
        section_title("Request volume")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["date"], y=df["requests"], mode="lines",
            line=dict(color=THEME["accent_2"], width=3, shape="spline"),
            fill="tozeroy", fillcolor="rgba(14,165,233,0.08)", name="Requests",
            hovertemplate="%{y:,} requests<extra></extra>",
        ))
        fig.add_trace(go.Scatter(
            x=df["date"], y=df["requests"].rolling(7, min_periods=1).mean(),
            mode="lines", line=dict(color=THEME["accent_1"], width=2, dash="dot"),
            name="7-day avg", hoverinfo="skip",
        ))
        st.plotly_chart(styled_plotly(fig), use_container_width=True, config={"displayModeBar": False})

    with right:
        section_title("Health")
        st.metric("Uptime", "99.98%", "+0.02%")
        st.metric("Error rate", "0.12%", "-0.04%", delta_color="inverse")
        st.metric("p95 latency", "412 ms", "-18 ms", delta_color="inverse")

    section_title("Latency & accuracy trend")
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=df["date"], y=df["latency_ms"], name="Latency (ms)",
        marker=dict(color="rgba(99,102,241,0.55)", line=dict(width=0)),
    ))
    fig2.add_trace(go.Scatter(
        x=df["date"], y=df["accuracy"] * 100, name="Accuracy (%)", yaxis="y2",
        mode="lines", line=dict(color=THEME["accent_3"], width=3),
    ))
    fig2.update_layout(yaxis2=dict(overlaying="y", side="right", showgrid=False))
    st.plotly_chart(styled_plotly(fig2, 320), use_container_width=True, config={"displayModeBar": False})


def render_models(df: pd.DataFrame, breakdown: pd.DataFrame, selected: list) -> None:
    st.markdown('<div class="hero-title">Model Portfolio</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Traffic share and routing across deployed models.</div>',
                unsafe_allow_html=True)

    filtered = breakdown[breakdown["model"].isin(selected)] if selected else breakdown

    left, right = st.columns([1, 1.2])
    with left:
        section_title("Traffic share")
        fig = go.Figure(go.Pie(
            labels=filtered["model"], values=filtered["share"], hole=0.68,
            marker=dict(colors=[THEME["accent_1"], THEME["accent_2"], THEME["accent_3"],
                                THEME["success"], "#F59E0B"],
                        line=dict(color=THEME["bg_primary"], width=3)),
            textinfo="none",
        ))
        fig.add_annotation(text=f"<b>{filtered['share'].sum()}%</b><br>routed",
                           showarrow=False, font=dict(size=20, color=THEME["text_primary"]))
        st.plotly_chart(styled_plotly(fig, 380), use_container_width=True, config={"displayModeBar": False})

    with right:
        section_title("Model cards")
        for _, row in filtered.iterrows():
            st.markdown(f"""
            <div class="glass-card" style="margin-bottom:0.9rem; padding:1rem 1.2rem;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div class="insight-title">{row['model']}</div>
                        <div class="insight-body">{row['share']}% of traffic</div>
                    </div>
                    <span class="badge">Healthy</span>
                </div>
                <div style="margin-top:0.7rem; height:6px; border-radius:6px;
                            background:rgba(15,23,42,0.06); overflow:hidden;">
                    <div style="width:{row['share']}%; height:100%;
                                background:linear-gradient(90deg,{THEME['accent_1']},{THEME['accent_2']});
                                box-shadow:0 0 8px rgba(99,102,241,0.3);"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")
    section_title("Actions")
    b1, b2, _ = st.columns([1, 1, 3])
    with b1:
        if st.button("🚀 Deploy model", use_container_width=True):
            st.success("Deployment pipeline started.")
    with b2:
        st.download_button(
            "⬇ Export CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="nebula_usage.csv",
            mime="text/csv",
            use_container_width=True,
        )


def render_insights() -> None:
    st.markdown('<div class="hero-title">AI Insights</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Automatically surfaced anomalies and recommendations.</div>',
                unsafe_allow_html=True)

    insights = [
        ("Latency improved after cache warm-up", "p95 dropped 18% since the Tuesday deploy.", THEME["success"]),
        ("Vision-Pro usage spiking on weekends", "Consider autoscaling rules for Sat–Sun traffic.", THEME["accent_3"]),
        ("Embed-v3 cost efficiency opportunity", "Batching requests could reduce spend by ~9%.", THEME["accent_2"]),
        ("Accuracy drift detected in Audio-Lite", "Retraining candidate flagged for review.", THEME["danger"]),
    ]

    left, right = st.columns(2)
    for i, (title, body, color) in enumerate(insights):
        target = left if i % 2 == 0 else right
        with target:
            st.markdown(f'<div class="glass-card">{insight_item(title, body, color)}</div>',
                        unsafe_allow_html=True)


def render_settings() -> None:
    st.markdown('<div class="hero-title">Settings</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Configure your workspace and API preferences.</div>',
                unsafe_allow_html=True)

    with st.container(border=True):
        st.text_input("Workspace name", value="Nebula Labs")
        st.text_input("API endpoint", value="https://api.example.com/v1")
        st.slider("Alert threshold (latency ms)", 100, 1000, 450)
        st.toggle("Enable anomaly detection", value=True)
        st.toggle("Send weekly digest", value=False)
        st.button("Save changes")


# ---------------------------------------------------------------------------
# 8. MAIN ENTRY POINT
# ---------------------------------------------------------------------------
def main() -> None:
    inject_custom_css()
    controls = render_sidebar()

    df = generate_demo_data(days=controls["days"])
    breakdown = generate_model_breakdown()

    if controls["page"] == "Overview":
        render_overview(df)
    elif controls["page"] == "Models":
        render_models(df, breakdown, controls["models"])
    elif controls["page"] == "Insights":
        render_insights()
    else:
        render_settings()


if __name__ == "__main__":
    main()
