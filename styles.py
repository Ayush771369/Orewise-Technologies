
import html
import textwrap
import streamlit as st


# ==========================================================
# OREWISE DESIGN SYSTEM
# ==========================================================

COLORS = {
    "navy": "#142638",
    "navy_light": "#203B50",
    "amber": "#E69B45",
    "background": "#F3F5F7",
    "white": "#FFFFFF",
    "text": "#182D3D",
    "muted": "#718096",
    "green": "#278568",
    "border": "#DCE3E8",
}


# ==========================================================
# SAFE HTML RENDERING HELPER
# ==========================================================

def render_html(markup):
    """Remove indentation and render HTML instead of code."""

    clean_markup = textwrap.dedent(markup).strip()

    st.markdown(
        clean_markup,
        unsafe_allow_html=True
    )


# ==========================================================
# GLOBAL CSS
# ==========================================================

def load_css():

    render_html("""
    <style>

    .stApp {
        background-color: #F3F5F7;
        color: #182D3D;
    }

    .block-container {
        max-width: 1440px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    #MainMenu, footer {
        visibility: hidden;
    }

    header[data-testid="stHeader"] {
        background: rgba(243,245,247,0.95);
    }

    /* SIDEBAR */

    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #142638,
            #0D1B29
        );
    }

    section[data-testid="stSidebar"] * {
        color: #F3F5F7;
    }

    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #C5D1DB;
    }

    section[data-testid="stSidebar"] hr {
        border-color: #354B5E;
    }

    /* TYPOGRAPHY */

    h1, h2, h3, h4 {
        color: #142638;
        font-weight: 750;
        letter-spacing: -0.5px;
    }

    p {
        line-height: 1.7;
    }

    /* BUTTONS */

    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease;
    }

    .stButton > button[kind="primary"] {
        background: #E69B45;
        color: #142638;
        border: none;
    }

    .stButton > button[kind="primary"]:hover {
        background: #F4C078;
        transform: translateY(-2px);
    }

    /* INPUTS */

    .stTextInput input,
    .stNumberInput input {
        border-radius: 8px;
    }

    /* TABLES */

    [data-testid="stDataFrame"] {
        border: 1px solid #DCE3E8;
        border-radius: 10px;
        overflow: hidden;
    }

    /* CHARTS */

    [data-testid="stPlotlyChart"],
    [data-testid="stVegaLiteChart"] {
        background: white;
        border: 1px solid #E5EAF0;
        border-radius: 12px;
        padding: 8px;
    }

    /* EXPANDERS */

    [data-testid="stExpander"] {
        background: white;
        border: 1px solid #DCE3E8;
        border-radius: 10px;
    }

    /* HERO */

    .ow-hero {
        background:
            radial-gradient(
                circle at 85% 20%,
                rgba(230,155,69,0.17),
                transparent 36%
            ),
            linear-gradient(
                120deg,
                #142638,
                #203B50
            );
        padding: 3.2rem;
        border-radius: 18px;
        margin-bottom: 2rem;
        overflow: hidden;
    }

    .ow-hero-label {
        color: #E69B45;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 2.5px;
        margin-bottom: 18px;
    }

    .ow-hero-title {
        color: white !important;
        font-size: clamp(32px, 4vw, 52px);
        font-weight: 850;
        line-height: 1.15;
        letter-spacing: -1.5px;
        max-width: 850px;
        margin-bottom: 18px;
    }

    .ow-hero-description {
        color: #D1DCE5;
        font-size: 16px;
        line-height: 1.8;
        max-width: 700px;
    }

    /* BRAND */

    .ow-brand {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 1.8rem;
    }

    .ow-brand-symbol {
        width: 46px;
        height: 46px;
        background: #E69B45;
        color: #142638;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 23px;
        font-weight: 900;
    }

    .ow-brand-name {
        color: #142638;
        font-size: 22px;
        font-weight: 900;
        letter-spacing: 1px;
    }

    .ow-brand-tagline {
        color: #718096;
        font-size: 9px;
        letter-spacing: 2px;
        font-weight: 700;
    }

    /* PAGE HEADER */

    .ow-page-eyebrow {
        color: #C27C29;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 2px;
        margin-bottom: 8px;
    }

    .ow-page-title {
        color: #142638;
        font-size: clamp(28px, 3vw, 38px);
        font-weight: 850;
        margin-bottom: 8px;
    }

    .ow-page-description {
        color: #718096;
        font-size: 15px;
        line-height: 1.7;
        margin-bottom: 25px;
    }

    /* SECTION TITLES */

    .ow-section-title {
        color: #142638;
        font-size: 21px;
        font-weight: 800;
        margin-top: 24px;
        margin-bottom: 5px;
    }

    .ow-section-caption {
        color: #718096;
        font-size: 13px;
        margin-bottom: 17px;
    }

    /* KPI CARDS */

    .ow-kpi-card {
        background: white;
        border: 1px solid #E2E8ED;
        border-radius: 12px;
        padding: 20px;
        min-height: 145px;
        box-shadow: 0 3px 12px rgba(20,38,56,0.04);
        transition: all 0.2s ease;
    }

    .ow-kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 22px rgba(20,38,56,0.09);
    }

    .ow-kpi-accent {
        width: 35px;
        height: 4px;
        border-radius: 10px;
        margin-bottom: 15px;
    }

    .ow-kpi-label {
        color: #718096;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1px;
        margin-bottom: 12px;
    }

    .ow-kpi-value {
        color: #142638;
        font-size: 30px;
        font-weight: 850;
        letter-spacing: -1px;
    }

    .ow-kpi-detail {
        color: #8795A4;
        font-size: 11px;
        margin-top: 7px;
    }

    /* INFO CARDS */

    .ow-info-card {
        background: white;
        border: 1px solid #E2E8ED;
        border-radius: 12px;
        padding: 22px;
        min-height: 150px;
        height: 100%;
    }

    .ow-info-card-title {
        font-weight: 850;
        color: #142638;
        font-size: 17px;
        margin-bottom: 12px;
    }

    .ow-info-card-body {
        color: #718096;
        font-size: 13px;
        line-height: 1.75;
    }

    /* STATUS PILLS */

    .ow-pill {
        display: inline-block;
        border-radius: 30px;
        padding: 5px 11px;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 0.7px;
    }

    .ow-pill-amber {
        background: #FFF1DC;
        color: #986020;
    }

    .ow-pill-green {
        background: #E2F3EC;
        color: #247457;
    }

    .ow-pill-blue {
        background: #E4EEF5;
        color: #294B63;
    }

    /* EQUIPMENT CARDS */

    .ow-equipment-card {
        background: white;
        border: 1px solid #DCE3E8;
        border-radius: 12px;
        padding: 19px;
        text-align: center;
        height: 100%;
    }

    .ow-equipment-number {
        color: #C27C29;
        font-weight: 900;
        font-size: 11px;
        letter-spacing: 1.5px;
    }

    .ow-equipment-name {
        color: #142638;
        font-weight: 850;
        font-size: 15px;
        margin-top: 8px;
    }

    .ow-equipment-description {
        color: #718096;
        font-size: 12px;
        line-height: 1.5;
        margin-top: 7px;
    }

    /* FOOTER */

    .ow-footer {
        background: #142638;
        color: white;
        border-radius: 12px;
        padding: 25px;
        margin-top: 40px;
        text-align: center;
    }

    .ow-footer-title {
        color: #E69B45;
        font-size: 17px;
        font-weight: 850;
        letter-spacing: 1.5px;
    }

    .ow-footer-text {
        color: #C1CED8;
        font-size: 11px;
        margin-top: 7px;
    }

    /* RESPONSIVE */

    @media (max-width: 768px) {
        .block-container {
            padding: 1rem;
        }

        .ow-hero {
            padding: 1.7rem;
        }

        .ow-hero-title {
            font-size: 30px;
        }

        .ow-kpi-value {
            font-size: 24px;
        }
    }

    </style>
    """)


# ==========================================================
# BRAND HEADER
# ==========================================================

def brand_header():

    render_html("""
    <div class="ow-brand">

        <div class="ow-brand-symbol">O</div>

        <div>
            <div class="ow-brand-name">OREWISE</div>

            <div class="ow-brand-tagline">
                MINERAL PROCESSING TECHNOLOGIES
            </div>
        </div>

    </div>
    """)


# ==========================================================
# HERO SECTION
# ==========================================================

def hero_section(
    title,
    description,
    label="MINERAL PROCESSING TECHNOLOGIES"
):

    render_html(f"""
    <div class="ow-hero">

        <div class="ow-hero-label">
            {html.escape(str(label))}
        </div>

        <div class="ow-hero-title">
            {html.escape(str(title))}
        </div>

        <div class="ow-hero-description">
            {html.escape(str(description))}
        </div>

    </div>
    """)


# ==========================================================
# PAGE HEADER
# ==========================================================

def page_header(
    title,
    description="",
    eyebrow="OREWISE TECHNOLOGIES"
):

    render_html(f"""
    <div class="ow-page-eyebrow">
        {html.escape(str(eyebrow))}
    </div>

    <div class="ow-page-title">
        {html.escape(str(title))}
    </div>

    <div class="ow-page-description">
        {html.escape(str(description))}
    </div>
    """)


# ==========================================================
# SECTION TITLE
# ==========================================================

def section_title(title, caption=""):

    render_html(f"""
    <div class="ow-section-title">
        {html.escape(str(title))}
    </div>

    <div class="ow-section-caption">
        {html.escape(str(caption))}
    </div>
    """)


# ==========================================================
# KPI CARD
# ==========================================================

def metric_card(
    label,
    value,
    detail="",
    accent="amber"
):

    accent_colors = {
        "amber": "#E69B45",
        "green": "#278568",
        "blue": "#426A85",
        "red": "#C95757"
    }

    accent_color = accent_colors.get(
        accent,
        "#E69B45"
    )

    render_html(f"""
    <div class="ow-kpi-card">

        <div
            class="ow-kpi-accent"
            style="background-color:{accent_color};">
        </div>

        <div class="ow-kpi-label">
            {html.escape(str(label))}
        </div>

        <div class="ow-kpi-value">
            {html.escape(str(value))}
        </div>

        <div class="ow-kpi-detail">
            {html.escape(str(detail))}
        </div>

    </div>
    """)


# ==========================================================
# INFORMATION CARD
# ==========================================================

def info_card(title, description):

    render_html(f"""
    <div class="ow-info-card">

        <div class="ow-info-card-title">
            {html.escape(str(title))}
        </div>

        <div class="ow-info-card-body">
            {html.escape(str(description))}
        </div>

    </div>
    """)


# ==========================================================
# STATUS PILL
# ==========================================================

def status_pill(label, color="amber"):

    allowed_colors = ["amber", "green", "blue"]

    if color not in allowed_colors:
        color = "amber"

    render_html(f"""
    <span class="ow-pill ow-pill-{color}">
        {html.escape(str(label))}
    </span>
    """)


# ==========================================================
# EQUIPMENT CARD
# ==========================================================

def equipment_card(number, name, description):

    render_html(f"""
    <div class="ow-equipment-card">

        <div class="ow-equipment-number">
            UNIT {html.escape(str(number))}
        </div>

        <div class="ow-equipment-name">
            {html.escape(str(name))}
        </div>

        <div class="ow-equipment-description">
            {html.escape(str(description))}
        </div>

    </div>
    """)


# ==========================================================
# FOOTER
# ==========================================================

def footer():

    render_html("""
    <div class="ow-footer">

        <div class="ow-footer-title">
            OREWISE TECHNOLOGIES
        </div>

        <div class="ow-footer-text">
            Engineering smarter mineral processing solutions.
        </div>

        <div class="ow-footer-text">
            ChE 303 | Fluid Particle Systems Project
        </div>

    </div>
    """)
