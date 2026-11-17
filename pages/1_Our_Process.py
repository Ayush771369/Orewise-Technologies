
import streamlit as st
import pandas as pd
from pathlib import Path

from styles import (
    load_css,
    page_header,
    section_title,
    equipment_card,
    info_card,
    status_pill,
    footer,
)

# ==========================================================
# 1. PAGE SETUP AND DATA
# ==========================================================

load_css()

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

SUMMARY_PATH = DATA_DIR / "aspen_cases_summary.csv"
STREAMS_PATH = DATA_DIR / "aspen_streams.csv"


@st.cache_data
def load_csv(path):
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()


summary_df = load_csv(SUMMARY_PATH)
streams_df = load_csv(STREAMS_PATH)

# ==========================================================
# 2. PAGE HEADER
# ==========================================================

page_header(
    title="Our Process",
    eyebrow="OREWISE | PROCESS ENGINEERING",
    description=(
        "Explore our proposed hematite beneficiation process, "
        "equipment arrangement, Aspen operating cases and "
        "material streams."
    ),
)

status_pill("ASPEN FLOWSHEET", "blue")
status_pill("GRAVITY SEPARATION CONCEPT", "amber")

st.divider()

# ==========================================================
# 3. PROCESS INTRODUCTION
# ==========================================================

section_title(
    "From Raw Ore to Valuable Product",
    "Understanding the material flow through our processing circuit.",
)

st.markdown("""
OreWise Technologies proposes a preliminary mineral-processing
plant to upgrade hematite–quartz ore.

The process begins with fresh ore feed and recycled screen
oversize. The combined material passes through crushing and
screening. Screen undersize is mixed with water to prepare a
slurry for the gravity-separation stage.

The G-SEP unit produces two outlet streams: a hematite-rich
concentrate and quartz-rich tailings.
""")

st.info(
    "The flowsheet represents the proposed process arrangement. "
    "The G-SEP block uses specified component split fractions in "
    "the current Aspen model; it is not a detailed physical "
    "particle-trajectory simulation."
)

st.divider()

# ==========================================================
# 4. PROCESS FLOW DIAGRAM
# ==========================================================

section_title(
    "Mineral Processing Flowsheet",
    "Connected equipment blocks and material streams in the Aspen model.",
)

st.graphviz_chart(
    """
    digraph OreWise {
        graph [
            rankdir=LR,
            bgcolor="transparent",
            nodesep=0.55,
            ranksep=0.65,
            pad=0.25,
            splines=ortho
        ];

        node [
            shape=box,
            style="rounded,filled",
            fillcolor="#EAF0F5",
            color="#B9CAD6",
            fontname="Arial",
            fontsize=11,
            fontcolor="#142638",
            margin="0.20,0.14",
            penwidth=1.4
        ];

        edge [
            color="#6C8598",
            penwidth=1.7,
            fontname="Arial",
            fontsize=9,
            fontcolor="#526B7B",
            arrowsize=0.8
        ];

        Feed [
            label="ORE-FEED\\nFresh Ore",
            fillcolor="#F3F5F7"
        ];

        Mixer [
            label="MIXER\\nFresh Feed + Recycle"
        ];

        Crusher [
            label="CRUSHER\\nParticle Size Reduction"
        ];

        Screen [
            label="SCREEN\\nSize Separation"
        ];

        Water [
            label="WATER\\nWater Addition",
            fillcolor="#E4EEF5"
        ];

        Mix [
            label="MIX\\nSlurry Preparation",
            fillcolor="#E4EEF5"
        ];

        GSEP [
            label="G-SEP\\nGravity Separator",
            fillcolor="#FFF1DC",
            color="#E69B45",
            penwidth=2.0
        ];

        Conc [
            label="CONC\\nHematite-rich Product",
            fillcolor="#E2F3EC",
            color="#278568"
        ];

        Tail [
            label="TAIL\\nQuartz-rich Waste",
            fillcolor="#F4EBE5",
            color="#C58C70"
        ];

        Feed -> Mixer [label="Fresh ore"];
        Screen -> Mixer [
            label="O-F: Oversize recycle",
            style=dashed,
            color="#E69B45",
            constraint=false
        ];

        Mixer -> Crusher [label="MIXED-F"];
        Crusher -> Screen;
        Screen -> Mix [label="U-F: Undersize"];
        Water -> Mix;
        Mix -> GSEP [label="MIXED"];
        GSEP -> Conc [label="Concentrate"];
        GSEP -> Tail [label="Tailings"];
    }
    """,
    use_container_width=True,
)

st.caption(
    "The flowsheet shows the proposed arrangement of MIXER, "
    "CRUSHER, SCREEN, MIX and G-SEP. The dashed line represents "
    "the screen oversize recycle."
)

st.divider()

# ==========================================================
# 5. ASPEN OPERATING CASE SELECTOR
# ==========================================================

section_title(
    "Explore Aspen Operating Cases",
    "Select one of the nine saved Aspen simulations to view its results.",
)

if summary_df.empty:
    st.error(
        "Aspen case summary not found. Please check that "
        "data/aspen_cases_summary.csv exists."
    )
    footer()
    st.stop()

required_summary = [
    "case_id",
    "feed_rate_kg_hr",
    "psd_id",
    "hematite_recovery_pct",
    "concentrate_grade_dry_pct",
    "concentrate_solids_kg_hr",
    "tailings_solids_kg_hr",
    "F80_mm",
    "P80_mm",
    "external_mass_balance_error_pct",
]

missing_summary = [
    col for col in required_summary
    if col not in summary_df.columns
]

if missing_summary:
    st.error(
        "The Aspen summary is missing columns: "
        + ", ".join(missing_summary)
    )
    footer()
    st.stop()

summary_df["case_id"] = summary_df["case_id"].astype(str)

summary_df = summary_df.sort_values(
    ["feed_rate_kg_hr", "psd_id"]
).reset_index(drop=True)

case_ids = summary_df["case_id"].tolist()

default_case = (
    "1000_1" if "1000_1" in case_ids else case_ids[0]
)

selected_case = st.selectbox(
    "Select Aspen case",
    options=case_ids,
    index=case_ids.index(default_case),
    format_func=lambda x: (
        f"{x.replace('_', ' | PSD ')} "
        f"(Feed {summary_df.loc[summary_df['case_id'] == x, 'feed_rate_kg_hr'].iloc[0]:,.0f} kg/h)"
    ),
)

case = summary_df[
    summary_df["case_id"] == selected_case
].iloc[0]

feed_rate = float(case["feed_rate_kg_hr"])
psd_id = int(case["psd_id"])

# ==========================================================
# 6. SELECTED CASE PERFORMANCE
# ==========================================================

st.markdown("### Selected Case Performance")

m1, m2, m3 = st.columns(3)

with m1:
    st.metric(
        "Fresh Feed Rate",
        f"{feed_rate:,.0f} kg/h",
    )

with m2:
    st.metric(
        "Hematite Recovery",
        f"{case['hematite_recovery_pct']:.2f}%",
    )

with m3:
    st.metric(
        "Concentrate Grade",
        f"{case['concentrate_grade_dry_pct']:.2f}%",
    )

m4, m5, m6 = st.columns(3)

with m4:
    st.metric(
        "Concentrate Solids",
        f"{case['concentrate_solids_kg_hr']:,.2f} kg/h",
    )

with m5:
    st.metric(
        "Tailings Solids",
        f"{case['tailings_solids_kg_hr']:,.2f} kg/h",
    )

with m6:
    st.metric(
        "PSD Case",
        f"PSD {psd_id}",
    )

st.caption(
    f"Selected Aspen case: {selected_case}. "
    "Values are retrieved from the saved simulation dataset."
)

st.divider()

# ==========================================================
# 7. PROCESS STREAM OVERVIEW
# ==========================================================

section_title(
    "Process Stream Overview",
    "Major incoming, circulating and outgoing material streams.",
)

flow1, flow2, flow3 = st.columns(3)

with flow1:
    info_card(
        "01 | Fresh Ore Feed",
        "Fresh hematite–quartz ore enters the plant and combines "
        "with recycled screen oversize.",
    )

with flow2:
    info_card(
        "02 | Oversize Recycle",
        "Screen oversize returns to the first mixer and passes "
        "through the crushing circuit again.",
    )

with flow3:
    info_card(
        "03 | Slurry Preparation",
        "Screen undersize combines with water before entering "
        "the G-SEP separation stage.",
    )

st.divider()

# ==========================================================
# 8. ASPEN STREAM RESULTS
# ==========================================================

section_title(
    "Aspen Material Stream Results",
    "Component flow rates for the selected operating case.",
)

if streams_df.empty:
    st.warning(
        "The file data/aspen_streams.csv was not found. "
        "Run the dataset-building script to generate it."
    )

elif "case_id" not in streams_df.columns:
    st.error("The Aspen streams dataset does not contain case_id.")

else:
    streams_df["case_id"] = streams_df["case_id"].astype(str)

    case_streams = streams_df[
        streams_df["case_id"] == selected_case
    ].copy()

    if case_streams.empty:
        st.warning(
            f"No stream records were found for {selected_case}."
        )

    else:
        preferred_columns = [
            "stream_id",
            "total_wet_flow_kg_hr",
            "dry_solids_flow_kg_hr",
            "hematite_kg_hr",
            "silica_kg_hr",
            "water_kg_hr",
        ]

        available_columns = [
            col for col in preferred_columns
            if col in case_streams.columns
        ]

        if available_columns:
            display_streams = case_streams[
                available_columns
            ].copy()

            column_names = {
                "stream_id": "Stream",
                "total_wet_flow_kg_hr": "Total Wet Flow (kg/h)",
                "dry_solids_flow_kg_hr": "Dry Solids (kg/h)",
                "hematite_kg_hr": "Hematite (kg/h)",
                "silica_kg_hr": "Silica (kg/h)",
                "water_kg_hr": "Water (kg/h)",
            }

            display_streams = display_streams.rename(
                columns=column_names
            )

            st.dataframe(
                display_streams,
                use_container_width=True,
                hide_index=True,
            )

        else:
            st.warning(
                "The stream dataset does not contain the expected "
                "flow columns. Available columns: "
                + ", ".join(case_streams.columns)
            )

        st.caption(
            "These values are from the saved Aspen stream dataset "
            "for the selected case."
        )

st.divider()

# ==========================================================
# 9. PARTICLE SIZE AND CRUSHING INDICATORS
# ==========================================================

section_title(
    "Particle Size Preparation",
    "Feed and product size indicators from the Aspen cases.",
)

p1, p2, p3 = st.columns(3)

with p1:
    st.metric(
        "Feed F80",
        f"{case['F80_mm']:.3f} mm",
    )

with p2:
    st.metric(
        "Product P80",
        f"{case['P80_mm']:.3f} mm",
    )

with p3:
    st.metric(
        "External Balance Error",
        f"{case['external_mass_balance_error_pct']:.3e}%",
    )

st.markdown("""
The F80 and P80 values describe the particle sizes at which
80% of the respective size distributions pass. They provide
an indication of the size-reduction performance represented
by the selected case.
""")

st.divider()

# ==========================================================
# 10. EQUIPMENT AND UNIT OPERATIONS
# ==========================================================

section_title(
    "Equipment and Unit Operations",
    "The purpose of each equipment block in the process flowsheet.",
)

col1, col2 = st.columns(2, gap="large")

with col1:
    equipment_card(
        "01",
        "MIXER",
        "Combines fresh ore feed with recycled screen oversize.",
    )

with col2:
    equipment_card(
        "02",
        "JAW CRUSHER",
        "Reduces the particle size of the incoming ore.",
    )

col3, col4 = st.columns(2, gap="large")

with col3:
    equipment_card(
        "03",
        "VIBRATING SCREEN",
        "Separates material by particle size and returns "
        "the oversize fraction to the crusher circuit.",
    )

with col4:
    equipment_card(
        "04",
        "WATER MIXER",
        "Combines screen undersize and water to prepare "
        "the slurry feed for separation.",
    )

col5 = st.columns(1)[0]

with col5:
    equipment_card(
        "05",
        "GRAVITY SEPARATOR | G-SEP",
        "Represents the proposed mineral-separation stage, "
        "producing a hematite-rich concentrate and "
        "quartz-rich tailings.",
    )

st.divider()

# ==========================================================
# 11. GRAVITY SEPARATION PRINCIPLES
# ==========================================================

section_title(
    "The Science Behind Gravity Separation",
    "Using differences in mineral density and particle settling behaviour.",
)

col1, col2 = st.columns(2, gap="large")

with col1:
    info_card(
        "HEMATITE | Fe₂O₃",
        """
Hematite is the valuable iron-bearing mineral.
Its approximate design-basis density is 5,250 kg/m³.

Its higher density can promote faster settling than
quartz particles of comparable size in a suitable
gravity-separation environment.
""",
    )

with col2:
    info_card(
        "QUARTZ | SiO₂",
        """
Quartz is the unwanted gangue material.
Its approximate design-basis density is 2,650 kg/m³.

Its lower density creates an opportunity to separate
it from heavier hematite using suitable gravity-based
equipment.
""",
    )

st.markdown("### Why particle size also matters")

st.markdown("""
Separation depends on both particle density and particle size.
A larger quartz particle can settle faster than a much smaller
hematite particle.

Therefore, feed-size preparation and mineral liberation are
important considerations when designing a real gravity-separation
plant.
""")

st.divider()

# ==========================================================
# 12. PROCESS OUTPUTS
# ==========================================================

section_title(
    "Final Product Streams",
    "The two outlet streams leaving the separation block.",
)

out1, out2 = st.columns(2, gap="large")

with out1:
    info_card(
        "HEMATITE-RICH CONCENTRATE",
        """
This is the valuable product stream. It contains
a greater proportion of hematite than the original
feed under the specified Aspen component split.
""",
    )

with out2:
    info_card(
        "QUARTZ-RICH TAILINGS",
        """
This is the waste stream. It contains the greater
proportion of the incoming quartz and may also
include water reporting to the tailings outlet.
""",
    )

st.divider()

# ==========================================================
# 13. ENGINEERING ASSUMPTIONS AND LIMITATIONS
# ==========================================================

section_title(
    "Engineering Assumptions and Model Limitations",
    "Understanding what the current Aspen model represents.",
)

with st.expander(
    "View process assumptions and simulation limitations",
    expanded=True,
):
    st.markdown("""
**Aspen simulation dataset**

- Nine saved Aspen operating cases are available.
- Feed rates include 750, 1,000 and 1,250 kg/h.
- Three particle-size distribution cases are represented.
- The saved cases provide stream, particle-size and
  material-balance information.

**Process arrangement**

- The flowsheet contains MIXER, CRUSHER, SCREEN, MIX and G-SEP.
- Screen oversize is recycled to the first mixer.
- Screen undersize is sent to slurry preparation.
- G-SEP produces concentrate and tailings using specified
  component split fractions.

**Important limitations**

- G-SEP is a generic separator, not a detailed physical
  spiral-concentrator or gravity-separator model.
- Its specified component split fractions determine the
  separation outputs.
- Python settling and partition calculations are estimates,
  not direct Aspen predictions.
- Actual mineral liberation and separator performance require
  ore-specific testing or validation.
""")

st.warning(
    "The Aspen recovery and grade values are based on the "
    "specified G-SEP component split fractions. They should "
    "not be interpreted as experimentally validated gravity "
    "separator performance."
)

# ==========================================================
# 14. FOOTER
# ==========================================================

footer()
