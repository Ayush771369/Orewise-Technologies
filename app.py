
import streamlit as st
import pandas as pd
from pathlib import Path

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
    initial_sidebar_state="expanded",
)

load_css()

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"

SUMMARY_PATH = DATA_DIR / "aspen_cases_summary.csv"
STREAMS_PATH = DATA_DIR / "aspen_streams.csv"


# ==========================================================
# 2. LOAD ASPEN DATA
# ==========================================================

@st.cache_data
def load_csv(path, modified_time):
    return pd.read_csv(path)


def load_dataset(path):
    if not path.exists():
        return pd.DataFrame()

    try:
        return load_csv(str(path), path.stat().st_mtime)
    except Exception as error:
        st.warning(f"Could not load {path.name}: {error}")
        return pd.DataFrame()


summary_df = load_dataset(SUMMARY_PATH)
streams_df = load_dataset(STREAMS_PATH)

if not summary_df.empty:
    summary_df["case_id"] = summary_df["case_id"].astype(str)

if not streams_df.empty:
    streams_df["case_id"] = streams_df["case_id"].astype(str)
    streams_df["stream_id"] = streams_df["stream_id"].astype(str)


# ==========================================================
# 3. SIDEBAR BRANDING
# ==========================================================

with st.sidebar:
    st.markdown("## ⛏️ OREWISE")
    st.caption("MINERAL PROCESSING TECHNOLOGIES")

    st.divider()

    st.caption("PROJECT NAVIGATION")
    st.write("Explore the OreWise engineering platform.")

    st.divider()

    st.caption("PROJECT")
    st.markdown("**Low-Cost Mineral Processing**")

    st.caption("DESIGN CAPACITY")
    st.markdown(
        "<span style='color:#E69B45;font-weight:800;'>"
        "1 Tonne / Hour"
        "</span>",
        unsafe_allow_html=True,
    )

    st.divider()
    st.caption("ChE 303 | Fluid Particle Systems")


# ==========================================================
# 4. BRAND HEADER AND HERO
# ==========================================================

brand_header()

hero_section(
    title="Turning Raw Ore Into Valuable Resources.",
    description=(
        "Engineering compact mineral-processing solutions "
        "that transform hematite–quartz ore into a more "
        "valuable mineral product through particle-size "
        "preparation and gravity-separation principles."
    ),
    label="OREWISE TECHNOLOGIES | ENGINEERING THE FUTURE",
)


# ==========================================================
# 5. PROJECT OVERVIEW
# ==========================================================

col1, col2, col3 = st.columns(3)

with col1:
    status_pill("DESIGN BASIS", "amber")
    st.markdown("### 1 TPH")
    st.caption("Proposed nominal processing capacity")

with col2:
    status_pill("MINERAL SYSTEM", "blue")
    st.markdown("### Hematite + Quartz")
    st.caption("Valuable mineral and unwanted gangue")

with col3:
    status_pill("SEPARATION CONCEPT", "green")
    st.markdown("### Gravity Separation")
    st.caption("Density-dependent particle behaviour")

st.divider()


# ==========================================================
# 6. COMPANY AND PROBLEM STATEMENT
# ==========================================================

section_title(
    "The Challenge We Address",
    "Understanding the problem behind mineral beneficiation.",
)

st.markdown("""
Mining produces ore containing valuable minerals mixed with
unwanted gangue.

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
""",
    )

with c2:
    info_card(
        "OUR PROPOSED SOLUTION",
        """
A modular process concept combining crushing,
screening, water addition and gravity-separation
principles to produce a hematite-rich concentrate
and quartz-rich tailings.
""",
    )

st.divider()


# ==========================================================
# 7. ENGINEERING DESIGN BASIS
# ==========================================================

section_title(
    "Engineering Design Basis",
    "The preliminary material assumptions used in the project.",
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    metric_card(
        "NOMINAL FEED",
        "1,000",
        "kg/h design basis",
    )

with col2:
    metric_card(
        "HEMATITE",
        "40%",
        "Assumed feed composition",
    )

with col3:
    metric_card(
        "QUARTZ",
        "60%",
        "Assumed feed composition",
    )

with col4:
    metric_card(
        "WATER ADDITION",
        "1,200",
        "kg/h reference case",
    )

st.caption(
    "These are project design-basis assumptions and reference "
    "conditions, not values that apply to every operating case."
)

st.divider()


# ==========================================================
# 8. LIVE ASPEN CASE HIGHLIGHTS
# ==========================================================

section_title(
    "Aspen Simulation Highlights",
    "Explore the performance of the saved Aspen operating cases.",
)

if summary_df.empty:
    st.warning(
        "The Aspen case summary is unavailable. Check that "
        "data/aspen_cases_summary.csv exists."
    )

else:
    required = [
        "case_id",
        "feed_rate_kg_hr",
        "psd_id",
        "hematite_recovery_pct",
        "concentrate_grade_dry_pct",
        "concentrate_solids_kg_hr",
    ]

    missing = [col for col in required if col not in summary_df.columns]

    if missing:
        st.error(
            "The Aspen summary is missing: " + ", ".join(missing)
        )

    else:
        case_options = summary_df.sort_values(
            ["feed_rate_kg_hr", "psd_id"]
        )["case_id"].tolist()

        default_case = (
            "1000_1" if "1000_1" in case_options
            else case_options[0]
        )

        selected_case_id = st.selectbox(
            "Explore Aspen operating case",
            case_options,
            index=case_options.index(default_case),
            format_func=lambda x: (
                f"{x} | "
                f"{summary_df.loc[summary_df['case_id'] == x, 'feed_rate_kg_hr'].iloc[0]:,.0f} kg/h"
            ),
        )

        selected_rows = summary_df[
            summary_df["case_id"] == selected_case_id
        ]

        case = selected_rows.iloc[0]

        feed_rate = float(case["feed_rate_kg_hr"])

        case_streams = (
            streams_df[
                streams_df["case_id"] == selected_case_id
            ].copy()
            if not streams_df.empty
            else pd.DataFrame()
        )

        water_flow = None

        if not case_streams.empty:
            water_rows = case_streams[
                case_streams["stream_id"] == "WATER"
            ]

            if (
                not water_rows.empty
                and "total_wet_flow_kg_hr" in water_rows.columns
            ):
                water_flow = float(
                    water_rows.iloc[0]["total_wet_flow_kg_hr"]
                )

        st.caption(
            f"Selected case: {selected_case_id} | "
            f"Feed: {feed_rate:,.0f} kg/h | "
            f"PSD {int(case['psd_id'])}"
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            metric_card(
                "HEMATITE RECOVERY",
                f"{case['hematite_recovery_pct']:.2f}%",
                "Aspen specified separator split",
                accent="green",
            )

        with col2:
            metric_card(
                "CONCENTRATE GRADE",
                f"{case['concentrate_grade_dry_pct']:.2f}%",
                "Dry-solids basis",
                accent="amber",
            )

        with col3:
            metric_card(
                "CONCENTRATE SOLIDS",
                f"{case['concentrate_solids_kg_hr']:,.2f}",
                "kg/h dry solids",
                accent="blue",
            )

        a, b = st.columns(2)

        with a:
            info_card(
                "FRESH ORE FEED",
                f"{feed_rate:,.0f} kg/h entering the selected Aspen case.",
            )

        with b:
            info_card(
                "WATER ADDITION",
                (
                    f"{water_flow:,.2f} kg/h from the Aspen WATER stream."
                    if water_flow is not None
                    else "Water stream data unavailable for this case."
                ),
            )

        st.info(
            "These performance indicators are retrieved from the "
            "saved Aspen dataset. G-SEP uses specified component "
            "split fractions rather than a detailed physical "
            "gravity-separator model."
        )


st.divider()


# ==========================================================
# 9. PROCESS OVERVIEW
# ==========================================================

section_title(
    "Our Mineral Processing Route",
    "A connected preliminary flowsheet developed in Aspen Plus.",
)

st.markdown("""
The process prepares incoming ore through crushing and
screening. Screen oversize is recycled for further crushing,
while undersize is combined with water before entering
the separation stage.
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

        Screen -> Mix [label="Undersize"];
        Water -> Mix;
        Mix -> Gravity;
        Gravity -> Conc;
        Gravity -> Tail;
    }
    """,
    use_container_width=True,
)

st.caption(
    "Process diagram follows the Aspen model's MIXER, CRUSHER, "
    "SCREEN, MIX and G-SEP structure. Oversize recycle returns "
    "to the first mixer."
)


# ==========================================================
# 10. PROCESS EQUIPMENT
# ==========================================================

st.divider()

section_title(
    "Key Process Equipment",
    "The main equipment blocks represented in the current flowsheet.",
)

e1, e2, e3 = st.columns(3)

with e1:
    info_card(
        "01 | Jaw Crusher",
        "Reduces the particle size of incoming ore before screening.",
    )

with e2:
    info_card(
        "02 | Vibrating Screen",
        "Separates material by particle size and returns oversize "
        "through the recycle circuit.",
    )

with e3:
    info_card(
        "03 | Gravity Separator",
        "Represents the proposed separation stage producing "
        "hematite-rich concentrate and quartz-rich tailings.",
    )


# ==========================================================
# 11. ENGINEERING TECHNOLOGY
# ==========================================================

st.divider()

section_title(
    "Our Engineering Approach",
    "Combining process simulation with particle-level calculations.",
)

c1, c2, c3 = st.columns(3)

with c1:
    info_card(
        "ASPEN PLUS",
        """
A connected process model represents the equipment
arrangement and calculates stream flow rates for
the saved simulation cases.
""",
    )

with c2:
    info_card(
        "PYTHON CALCULATIONS",
        """
Particle terminal settling velocity, Reynolds number,
gravity partition estimates and crusher power
sensitivity are calculated using Python.
""",
    )

with c3:
    info_card(
        "DIGITAL PLATFORM",
        """
The website combines process information,
stored Aspen outputs and Python calculations
in one interactive interface.
""",
    )


# ==========================================================
# 12. MODEL TRANSPARENCY
# ==========================================================

st.divider()

section_title(
    "Simulation Scope and Model Transparency",
    "Understanding what the current model represents.",
)

st.warning("""
The saved Aspen model contains MIXER, CRUSHER, SCREEN,
MIX and G-SEP, including the screen oversize recycle.

The G-SEP block uses specified component split fractions.
It is described as the gravity separator in the proposed
process concept, but it is not a detailed physical model
of a spiral or other commercial gravity concentrator.

Python settling, partition and grade–recovery calculations
are estimates and should not be presented as validated
separator performance.
""")

with st.expander("View project modelling scope"):
    st.markdown("""
**Aspen Plus**
- Nine saved operating cases.
- Three feed rates: 750, 1,000 and 1,250 kg/h.
- Three particle-size distribution cases.
- Exported stream and material-balance results.

**Python**
- Particle settling velocity and Reynolds number.
- Hindered settling estimates.
- Idealised gravity partition and grade–recovery calculations.
- Bond crusher power sensitivity calculations.

**Limitations**
- G-SEP uses specified component split fractions.
- Bond Work Index values are sensitivity assumptions.
- Actual separator performance requires experimental validation.
""")


# ==========================================================
# 13. FOOTER
# ==========================================================

footer()
