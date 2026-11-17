
"""
OREWISE TECHNOLOGIES
Shared Industrial Design System

Provides:
- Global CSS styling
- Brand header
- Page headings
- Section headings
- KPI cards
- Information cards
- Status labels
- Footer
"""

import html
import streamlit as st


# ==========================================================
# 1. BRAND COLOURS
# ==========================================================

COLORS = {
    "navy": "#142638",
    "navy_light": "#203B50",
    "navy_deep": "#0D1B29",
    "amber": "#E69B45",
    "amber_light": "#F4C078",
    "background": "#F3F5F7",
    "white": "#FFFFFF",
    "text": "#182D3D",
    "muted": "#718096",
    "border": "#DCE3E8",
    "green": "#278568",
    "red": "#C95757",
}


# ==========================================================
# 2. GLOBAL CSS
# ==========================================================

def load_css():
    """
    Apply the shared OreWise website styling.
    Call once near the beginning of each Streamlit page.
    """

    st.markdown(
        """
        <style>

        /* --------------------------------------------------
           GLOBAL APPLICATION
        -------------------------------------------------- */

        .stApp {
            background-color: #F3F5F7;
            color: #182D3D;
            font-family: 'Inter', sans-serif;
        }

        .block-container {
            max-width: 1440px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        /* Hide default Streamlit decorations */

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        header[data-testid="stHeader"] {
            background-color: rgba(243, 245, 247, 0.95);
        }


        /* --------------------------------------------------
           SIDEBAR
        -------------------------------------------------- */

        section[data-testid="stSidebar"] {
            background: linear-gradient(
                180deg,
                #142638 0%,
                #0D1B29 100%
            );
            border-right: 1px solid #203B50;
        }

        section[data-testid="stSidebar"] * {
            color: #F3F5F7;
        }

        section[data-testid="stSidebar"] a:hover {
            color: #E69B45 !important;
        }

        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
            color: #C5D1DB;
        }

        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3 {
            color: #FFFFFF;
        }

        section[data-testid="stSidebar"] hr {
            border-color: #354B5E;
        }


        /* --------------------------------------------------
           TYPOGRAPHY
        -------------------------------------------------- */

        h1, h2, h3, h4 {
            color: #142638 !important;
            font-weight: 700 !important;
            letter-spacing: -0.6px;
        }

        p {
            line-height: 1.7;
        }

        [data-testid="stCaptionContainer"] {
            color: #718096;
        }


        /* --------------------------------------------------
           BUTTONS
        -------------------------------------------------- */

        .stButton > button {
            border-radius: 8px;
            border: 1px solid #DCE3E8;
            font-weight: 600;
            padding: 0.55rem 1.2rem;
            transition: all 0.2s ease;
        }

        .stButton > button[kind="primary"] {
            background-color: #E69B45;
            color: #142638;
            border: none;
        }

        .stButton > button[kind="primary"]:hover {
            background-color: #F4C078;
            color: #142638;
            transform: translateY(-2px);
        }


        /* --------------------------------------------------
           INPUT WIDGETS
        -------------------------------------------------- */

        .stTextInput input,
        .stNumberInput input,
        .stSelectbox div[data-baseweb="select"] {
            border-radius: 8px;
        }

        div[data-baseweb="slider"] {
            padding-top: 0.5rem;
        }


        /* --------------------------------------------------
           DATAFRAMES AND TABLES
        -------------------------------------------------- */

        [data-testid="stDataFrame"] {
            border: 1px solid #DCE3E8;
            border-radius: 10px;
            overflow: hidden;
        }


        /* --------------------------------------------------
           CHARTS
        -------------------------------------------------- */

        [data-testid="stVegaLiteChart"],
        [data-testid="stPlotlyChart"] {
            background: #FFFFFF;
            border: 1px solid #E5EAF0;
            border-radius: 12px;
            padding: 0.5rem;
        }


        /* --------------------------------------------------
           EXPANDERS
        -------------------------------------------------- */

        [data-testid="stExpander"] {
            background-color: #FFFFFF;
            border: 1px solid #DCE3E8;
            border-radius: 10px;
        }


        /* --------------------------------------------------
           DIVIDERS
        -------------------------------------------------- */

        hr {
            border-color: #DCE3E8;
            margin-top: 1.5rem;
            margin-bottom: 1.5rem;
        }


        /* --------------------------------------------------
           OREWISE BRAND HEADER
        -------------------------------------------------- */

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
            font-size: 9px;
            color: #718096;
            letter-spacing: 2px;
            font-weight: 700;
        }


        /* --------------------------------------------------
           HERO SECTION
        -------------------------------------------------- */

        .ow-hero {
            background:
                radial-gradient(
                    circle at 85% 20%,
                    rgba(230,155,69,0.16),
                    transparent 35%
                ),
                linear-gradient(
                    120deg,
                    #142638 0%,
                    #203B50 100%
                );

            padding: 3rem;
            border-radius: 18px;
            color: #FFFFFF;
            margin-bottom: 2rem;
            position: relative;
            overflow: hidden;
        }

        .ow-hero-label {
            color: #E69B45;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 2.5px;
            text-transform: uppercase;
            margin-bottom: 15px;
        }

        .ow-hero-title {
            color: #FFFFFF !important;
            font-size: clamp(30px, 4vw, 52px);
            line-height: 1.12;
            font-weight: 800;
            letter-spacing: -1.8px;
            margin: 0 0 18px 0;
            max-width: 800px;
        }

        .ow-hero-description {
            color: #D1DCE5;
            font-size: 16px;
            line-height: 1.8;
            max-width: 690px;
        }


        /* --------------------------------------------------
           PAGE HEADERS
        -------------------------------------------------- */

        .ow-page-eyebrow {
            color: #C27C29;
            font-weight: 800;
            font-size: 11px;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 8px;
        }

        .ow-page-title {
            font-size: clamp(28px, 3vw, 38px);
            color: #142638;
            font-weight: 800;
            letter-spacing: -1.2px;
            margin-bottom: 8px;
        }

        .ow-page-description {
            color: #718096;
            font-size: 15px;
            max-width: 850px;
            line-height: 1.7;
            margin-bottom: 25px;
        }


        /* --------------------------------------------------
           SECTION HEADERS
        -------------------------------------------------- */

        .ow-section-title {
            color: #142638;
            font-size: 21px;
            font-weight: 750;
            margin-top: 24px;
            margin-bottom: 5px;
        }

        .ow-section-caption {
            color: #718096;
            font-size: 13px;
            margin-bottom: 17px;
        }


        /* --------------------------------------------------
           KPI CARDS
        -------------------------------------------------- */

        .ow-kpi-card {
            background: #FFFFFF;
            border: 1px solid #E2E8ED;
            border-radius: 12px;
            padding: 20px;
            height: 100%;
            box-shadow: 0 3px 12px rgba(20, 38, 56, 0.035);
            transition: all 0.2s ease;
        }

        .ow-kpi-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 22px rgba(20, 38, 56, 0.09);
        }

        .ow-kpi-label {
            color: #718096;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 1.1px;
            text-transform: uppercase;
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

        .ow-kpi-accent {
            width: 35px;
            height: 4px;
            background: #E69B45;
            border-radius: 10px;
            margin-bottom: 15px;
        }


        /* --------------------------------------------------
           INFORMATION CARDS
        -------------------------------------------------- */

        .ow-info-card {
            background: #FFFFFF;
            border: 1px solid #E2E8ED;
            border-radius: 12px;
            padding: 22px;
            height: 100%;
        }

        .ow-info-card-title {
            font-weight: 800;
            color: #142638;
            font-size: 17px;
            margin-bottom: 9px;
        }

        .ow-info-card-body {
            color: #718096;
            font-size: 13px;
            line-height: 1.75;
        }


        /* --------------------------------------------------
           STATUS PILLS
        -------------------------------------------------- */

        .ow-pill {
            display: inline-block;
            border-radius: 30px;
            padding: 5px 11px;
            font-size: 10px;
            letter-spacing: 0.7px;
            font-weight: 800;
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


        /* --------------------------------------------------
           PROCESS EQUIPMENT CARDS
        -------------------------------------------------- */

        .ow-equipment-card {
            background: #FFFFFF;
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
            font-weight: 800;
            font-size: 15px;
            margin-top: 8px;
        }

        .ow-equipment-description {
            color: #718096;
            font-size: 12px;
            line-height: 1.5;
            margin-top: 7px;
        }


        /* --------------------------------------------------
           FOOTER
        -------------------------------------------------- */

        .ow-footer {
            background: #142638;
            color: #FFFFFF;
            border-radius: 12px;
            padding: 23px;
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


        /* --------------------------------------------------
           MOBILE RESPONSIVENESS
        -------------------------------------------------- */

        @media (max-width: 768px) {

            .block-container {
                padding-top: 1rem;
                padding-left: 1rem;
                padding-right: 1rem;
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
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# 3. BRAND HEADER
# ==========================================================

def brand_header():
    """Display the OreWise wordmark."""

    st.markdown(
        """
        <div class="ow-brand">

            <div class="ow-brand-symbol">O</div>

            <div>
                <div class="ow-brand-name">OREWISE</div>
                <div class="ow-brand-tagline">
                    MINERAL PROCESSING TECHNOLOGIES
                </div>
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# 4. HERO SECTION
# ==========================================================

def hero_section(
    title,
    description,
    label="MINERAL PROCESSING TECHNOLOGIES"
):
    """Display the large homepage hero section."""

    title = html.escape(str(title))
    description = html.escape(str(description))
    label = html.escape(str(label))

    st.markdown(
        f"""
        <div class="ow-hero">

            <div class="ow-hero-label">
                {label}
            </div>

            <div class="ow-hero-title">
                {title}
            </div>

            <div class="ow-hero-description">
                {description}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# 5. PAGE HEADER
# ==========================================================

def page_header(
    title,
    description="",
    eyebrow="OREWISE TECHNOLOGIES"
):
    """Standard header for internal website pages."""

    title = html.escape(str(title))
    description = html.escape(str(description))
    eyebrow = html.escape(str(eyebrow))

    st.markdown(
        f"""
        <div class="ow-page-eyebrow">
            {eyebrow}
        </div>

        <div class="ow-page-title">
            {title}
        </div>

        <div class="ow-page-description">
            {description}
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# 6. SECTION TITLE
# ==========================================================

def section_title(title, caption=""):
    """Consistent section heading."""

    title = html.escape(str(title))
    caption = html.escape(str(caption))

    st.markdown(
        f"""
        <div class="ow-section-title">
            {title}
        </div>

        <div class="ow-section-caption">
            {caption}
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# 7. KPI CARD
# ==========================================================

def metric_card(
    label,
    value,
    detail="",
    accent="amber"
):
    """Display a premium KPI card."""

    label = html.escape(str(label))
    value = html.escape(str(value))
    detail = html.escape(str(detail))

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

    st.markdown(
        f"""
        <div class="ow-kpi-card">

            <div
                class="ow-kpi-accent"
                style="background-color:{accent_color};">
            </div>

            <div class="ow-kpi-label">
                {label}
            </div>

            <div class="ow-kpi-value">
                {value}
            </div>

            <div class="ow-kpi-detail">
                {detail}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# 8. INFORMATION CARD
# ==========================================================

def info_card(title, description):
    """Display a reusable information card."""

    title = html.escape(str(title))
    description = html.escape(str(description))

    st.markdown(
        f"""
        <div class="ow-info-card">

            <div class="ow-info-card-title">
                {title}
            </div>

            <div class="ow-info-card-body">
                {description}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# 9. STATUS PILL
# ==========================================================

def status_pill(label, color="amber"):
    """Display a small status indicator."""

    label = html.escape(str(label))

    allowed_colors = [
        "amber",
        "green",
        "blue"
    ]

    if color not in allowed_colors:
        color = "amber"

    st.markdown(
        f"""
        <span class="ow-pill ow-pill-{color}">
            {label}
        </span>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# 10. EQUIPMENT CARD
# ==========================================================

def equipment_card(number, name, description):
    """Display a process equipment card."""

    number = html.escape(str(number))
    name = html.escape(str(name))
    description = html.escape(str(description))

    st.markdown(
        f"""
        <div class="ow-equipment-card">

            <div class="ow-equipment-number">
                UNIT {number}
            </div>

            <div class="ow-equipment-name">
                {name}
            </div>

            <div class="ow-equipment-description">
                {description}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# 11. WEBSITE FOOTER
# ==========================================================

def footer():
    """Display the standard OreWise footer."""

    st.markdown(
        """
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
        """,
        unsafe_allow_html=True
    )
