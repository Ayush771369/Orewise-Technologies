
import streamlit as st

from styles import (
    load_css,
    brand_header,
    hero_section,
    section_title,
    metric_card,
    info_card,
    status_pill,
    footer,
)


# ==========================================================
# 1. PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="OreWise Technologies | Mineral Processing",
    page_icon="⛏️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# 2. GLOBAL DESIGN
# ==========================================================

load_css()


# ==========================================================
# 3. SIDEBAR BRANDING
# ==========================================================

with st.sidebar:

    st.markdown(
        """
        <div style="padding: 15px 5px 25px 5px;">

            <div style="
                display:flex;
                align-items:center;
                gap:12px;
            ">

                <div style="
                    width:44px;
                    height:44px;
                    background:#E69B45;
                    color:#142638;
                    border-radius:10px;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    font-size:23px;
                    font-weight:900;
                ">
                    O
                </div>

                <div>
                    <div style="
                        color:white;
                        font-size:21px;
                        font-weight:900;
                        letter-spacing:1px;
                    ">
                        OREWISE
                    </div>

                    <div style="
                        color:#ADBCC9;
                        font-size:8px;
                        letter-spacing:2px;
                        font-weight:700;
                    ">
                        MINERAL TECHNOLOGIES
                    </div>
                </div>

            </div>

        </div>

        <hr style="border-color:#354B5E;">
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="
            color:#E69B45;
            font-size:10px;
            letter-spacing:2px;
            font-weight:800;
            margin-bottom:8px;
        ">
            PROJECT NAVIGATION
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption("Explore the OreWise engineering platform.")

    st.divider()

    st.markdown(
        """
        <div style="
            color:#AEBCC8;
            font-size:11px;
            line-height:1.8;
        ">
            PROJECT<br>
            <span style="color:white;font-weight:700;">
                Low-Cost Mineral Processing
            </span>
            <br><br>
            DESIGN CAPACITY<br>
            <span style="color:#E69B45;font-weight:700;">
                1 Tonne / Hour
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# 4. HOMEPAGE BRAND HEADER
# ==========================================================

brand_header()


# ==========================================================
# 5. HERO SECTION
# ==========================================================

hero_section(
    title="Turning Raw Ore Into Valuable Resources.",
    description=(
        "Engineering compact mineral-processing solutions "
        "that transform hematite–quartz ore into a more "
        "valuable mineral product through particle-size "
        "preparation and gravity-separation principles."
    ),
    label="OREWISE TECHNOLOGIES | ENGINEERING THE FUTURE"
)


# ==========================================================
# 6. HERO SUPPORTING INFORMATION
# ==========================================================

col1, col2, col3 = st.columns(3)

with col1:
    status_pill("DESIGN BASIS", "amber")

    st.markdown("### 1 TPH")

    st.caption(
        "Proposed fresh ore processing capacity"
    )

with col2:
    status_pill("MINERAL SYSTEM", "blue")

    st.markdown("### Hematite + Quartz")

    st.caption(
        "Valuable mineral and unwanted gangue"
    )

with col3:
    status_pill("SEPARATION CONCEPT", "green")

    st.markdown("### Gravity Separation")

    st.caption(
        "Density-dependent particle behaviour"
    )


st.divider()


# ==========================================================
# 7. COMPANY AND PROBLEM STATEMENT
# ==========================================================

section_title(
    "The Challenge We Address",
    "Understanding the problem behind mineral beneficiation."
)

st.markdown("""
Mining produces large quantities of ore containing valuable
minerals mixed with unwanted gangue.

In our selected mineral system, hematite (Fe₂O₃) is the
valuable iron-bearing mineral, while quartz (SiO₂) is the
unwanted material.

The presence of quartz reduces the quality of the raw ore.
Our objective is to improve the proportion of hematite in
the final product through a connected mineral-processing route.
""")

c1, c2 = st.columns(2, gap="large")

with c1:

    info_card(
        "THE PROBLEM",
        """
        Low-grade hematite ore contains unwanted quartz.
        Processing the raw ore without beneficiation carries
        this gangue into downstream operations and reduces
        product quality.
        """
    )

with c2:

    info_card(
        "OUR PROPOSED SOLUTION",
        """
        A modular process concept combining crushing,
        screening, water addition and gravity-separation
        principles to produce a hematite-rich concentrate
        and quartz-rich tailings.
        """
    )


st.divider()


# ==========================================================
# 8. PROJECT DESIGN BASIS
# ==========================================================

section_title(
    "Engineering Design Basis",
    "The preliminary operating basis used in our project."
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    metric_card(
        "FRESH FEED",
        "1,000",
        "kg/h"
    )

with col2:
    metric_card(
        "HEMATITE",
        "40%",
        "Feed composition"
    )

with col3:
    metric_card(
        "QUARTZ",
        "60%",
        "Feed composition"
    )

with col4:
    metric_card(
        "WATER ADDITION",
        "1,200",
        "kg/h in saved Aspen case"
    )


st.divider()


# ==========================================================
# 9. CURRENT ASPEN CASE PERFORMANCE
# ==========================================================

section_title(
    "Current Simulation Highlights",
    "Performance indicators calculated from the saved Aspen simulation case."
)

col1, col2, col3 = st.columns(3)

with col1:
    metric_card(
        "HEMATITE RECOVERY",
        "85%",
        "Based on specified separator split"
        ,
        accent="green"
    )

with col2:
    metric_card(
        "CONCENTRATE GRADE",
        "73.91%",
        "Dry-solids basis",
        accent="amber"
    )

with col3:
    metric_card(
        "CONCENTRATE FLOW",
        "520 kg/h",
        "Saved Aspen case",
        accent="blue"
    )

st.info(
    "These are calculated results from the saved Aspen case. "
    "The G-SEP component split fractions are specified model "
    "inputs, not predictions from a detailed physical gravity-separator model."
)


st.divider()


# ==========================================================
# 10. PROCESS OVERVIEW
# ==========================================================

section_title(
    "Our Mineral Processing Route",
    "A connected preliminary flowsheet developed in Aspen Plus."
)

st.markdown("""
The process prepares the incoming ore through crushing and
screening. Screen oversize is recycled for further crushing,
while undersize is combined with water before entering the
separator.
""")

st.graphviz_chart(
    """
    digraph OreWise {

        graph [
            rankdir=LR,
            bgcolor="transparent",
            nodesep=0.45,
            ranksep=0.65,
            pad=0.2
        ];

        node [
            shape=box,
            style="rounded,filled",
            fillcolor="#EAF0F5",
            color="#BCCAD5",
            fontname="Arial",
            fontsize=11,
            fontcolor="#142638",
            margin="0.18,0.12"
        ];

        edge [
            color="#718DA1",
            penwidth=1.7,
            fontname="Arial",
            fontsize=9,
            fontcolor="#526B7B",
            arrowsize=0.8
        ];

        Feed [label="RAW ORE\\nFEED"];
        Mixer [label="MIXER"];
        Crusher [label="JAW\\nCRUSHER"];
        Screen [label="VIBRATING\\nSCREEN"];
        Water [label="WATER\\nADDITION"];
        Mix [label="SLURRY\\nMIXER", fillcolor="#FFF1DC", color="#E69B45"];
        Gravity [label="GRAVITY\\nSEPARATOR", fillcolor="#FFF1DC", color="#E69B45"];

        Conc [
            label="HEMATITE-RICH\\nCONCENTRATE",
            fillcolor="#E2F3EC",
            color="#278568"
        ];

        Tail [
            label="QUARTZ-RICH\\nTAILINGS",
            fillcolor="#F4EBE5",
            color="#C58C70"
        ];

        Feed -> Mixer;
        Mixer -> Crusher;
        Crusher -> Screen;

        Screen -> Mixer [
            label="Oversize recycle",
            style=dashed,
            constraint=false,
            color="#E69B45"
        ];

        Screen -> Mix [
            label="Undersize"
        ];

        Water -> Mix;

        Mix -> Gravity;

        Gravity -> Conc;
        Gravity -> Tail;
    }
    """,
    use_container_width=True
)


st.caption(
    "Process diagram follows the uploaded Aspen model's "
    "MIXER, CRUSHER, SCREEN, MIX and G-SEP structure. "
    "Oversize recycle returns to the first mixer."
)


# ==========================================================
# 11. PROCESS EQUIPMENT OVERVIEW
# ==========================================================

section_title(
    "Key Process Equipment",
    "The main equipment blocks represented in the current Aspen flowsheet."
)

e1, e2, e3 = st.columns(3)

with e1:

    info_card(
        "01 | Jaw Crusher",
        """
        Reduces the particle size of the incoming ore
        before screening.
        """
    )

with e2:

    info_card(
        "02 | Vibrating Screen",
        """
        Separates material according to particle size.
        Oversize is returned through the recycle circuit.
        """
    )

with e3:

    info_card(
        "03 | Gravity Separator",
        """
        Represents the proposed separation stage that
        produces a hematite-rich concentrate and
        quartz-rich tailings.
        """
    )


st.divider()


# ==========================================================
# 12. ENGINEERING TECHNOLOGY
# ==========================================================

section_title(
    "Our Engineering Approach",
    "Combining process simulation with particle-level calculations."
)

c1, c2, c3 = st.columns(3)

with c1:

    info_card(
        "ASPEN PLUS",
        """
        A connected process model is used to represent
        the equipment arrangement and calculate stream
        flow rates for the saved simulation case.
        """
    )

with c2:

    info_card(
        "PYTHON CALCULATIONS",
        """
        Particle terminal settling velocity and Reynolds
        number are calculated to demonstrate the influence
        of particle density and diameter.
        """
    )

with c3:

    info_card(
        "DIGITAL PLATFORM",
        """
        The website brings together process information,
        stored Aspen outputs and Python calculations
        in one interactive interface.
        """
    )


# ==========================================================
# 13. MODEL TRANSPARENCY
# ==========================================================

st.divider()

section_title(
    "Simulation Scope and Model Transparency",
    "Understanding what the current model represents."
)

st.warning(
    """
    The saved Aspen model contains MIXER, CRUSHER, SCREEN,
    MIX and G-SEP, including the screen oversize recycle.

    The G-SEP block is configured using specified component
    split fractions. It is described on this website as the
    gravity separator for the proposed process concept, but
    it is not a detailed physical model of a spiral or other
    commercial gravity concentrator.

    Additional Aspen operating cases are needed to demonstrate
    performance trends across operating conditions.
    """
)


# ==========================================================
# 14. FOOTER
# ==========================================================

footer()
