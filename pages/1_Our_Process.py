
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
# 1. PAGE SETUP
# ==========================================================

load_css()

ROOT = Path(__file__).resolve().parents[1]

CSV_PATH = ROOT / "data" / "aspen_stream_results.csv"


# ==========================================================
# 2. PAGE HEADER
# ==========================================================

page_header(
    title="Our Process",
    eyebrow="OREWISE | PROCESS ENGINEERING",
    description=(
        "Explore the preliminary mineral-beneficiation process, "
        "equipment arrangement, material streams and separation "
        "principles behind the OreWise plant concept."
    )
)

status_pill("ASPEN FLOWSHEET", "blue")
status_pill("GRAVITY SEPARATION CONCEPT", "amber")

st.divider()


# ==========================================================
# 3. PROCESS INTRODUCTION
# ==========================================================

section_title(
    "From Raw Ore to Valuable Product",
    "Understanding the material flow through our processing circuit."
)

st.markdown("""
Our proposed process is designed to upgrade hematite–quartz ore.
The incoming material undergoes crushing and screening before
being mixed with water and sent to the separation stage.

The screen oversize is recycled to the first mixer and passes
through the crushing circuit again. The undersize moves forward
to slurry preparation and separation.
""")

st.divider()


# ==========================================================
# 4. PROCESS FLOW DIAGRAM
# ==========================================================

section_title(
    "Mineral Processing Flowsheet",
    "Connected equipment blocks and streams from the saved Aspen model."
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

        Feed -> Mixer [
            label="Fresh ore"
        ];

        Screen -> Mixer [
            label="O-F: Oversize recycle",
            style=dashed,
            color="#E69B45",
            constraint=false
        ];

        Mixer -> Crusher [
            label="MIXED-F"
        ];

        Crusher -> Screen;

        Screen -> Mix [
            label="U-F: Undersize"
        ];

        Water -> Mix;

        Mix -> GSEP [
            label="MIXED"
        ];

        GSEP -> Conc [
            label="Concentrate"
        ];

        GSEP -> Tail [
            label="Tailings"
        ];
    }
    """,
    use_container_width=True
)

st.caption(
    "Flowsheet follows the uploaded Aspen model: MIXER, CRUSHER, "
    "SCREEN, MIX and G-SEP. The dashed connection represents "
    "the screen oversize recycle."
)

st.divider()


# ==========================================================
# 5. MATERIAL FLOW OVERVIEW
# ==========================================================

section_title(
    "Process Stream Overview",
    "The major incoming, circulating and outgoing material streams."
)

flow1, flow2, flow3 = st.columns(3)

with flow1:
    info_card(
        "01 | Fresh Ore Feed",
        "1,000 kg/h of hematite–quartz ore enters the process. "
        "The assumed dry composition is 40 wt% hematite and "
        "60 wt% quartz."
    )

with flow2:
    info_card(
        "02 | Oversize Recycle",
        "The screen oversize returns to the first mixer and "
        "passes through the crusher circuit again."
    )

with flow3:
    info_card(
        "03 | Slurry Feed",
        "Screen undersize combines with 1,200 kg/h of water "
        "before entering the G-SEP separator."
    )

st.divider()


# ==========================================================
# 6. EQUIPMENT CARDS
# ==========================================================

section_title(
    "Equipment and Unit Operations",
    "The purpose of each equipment block in the saved Aspen flowsheet."
)

col1, col2 = st.columns(2, gap="large")

with col1:
    equipment_card(
        "01",
        "MIXER",
        "Combines fresh ore feed with recycled screen oversize."
    )

with col2:
    equipment_card(
        "02",
        "JAW CRUSHER",
        "Reduces the particle size of the incoming ore."
    )

col3, col4 = st.columns(2, gap="large")

with col3:
    equipment_card(
        "03",
        "VIBRATING SCREEN",
        "Separates material by particle size and returns "
        "the oversize fraction to the crusher circuit."
    )

with col4:
    equipment_card(
        "04",
        "WATER MIXER",
        "Combines screen undersize and water to prepare "
        "the slurry feed for separation."
    )

col5 = st.columns(1)[0]

with col5:
    equipment_card(
        "05",
        "GRAVITY SEPARATOR | G-SEP",
        "Represents the proposed mineral-separation stage, "
        "producing a hematite-rich concentrate and "
        "quartz-rich tailings."
    )

st.divider()


# ==========================================================
# 7. HOW GRAVITY SEPARATION WORKS
# ==========================================================

section_title(
    "The Science Behind Gravity Separation",
    "Using differences in particle density and settling behaviour."
)

col1, col2 = st.columns(2, gap="large")

with col1:

    info_card(
        "HEMATITE | Fe₂O₃",
        """
        Hematite is the valuable iron-bearing mineral.
        Its approximate design-basis density is 5,250 kg/m³.

        In a suitable gravity-separation environment,
        its higher density can promote different settling
        behaviour compared with quartz particles of
        comparable size.
        """
    )

with col2:

    info_card(
        "QUARTZ | SiO₂",
        """
        Quartz is the unwanted gangue material.
        Its approximate design-basis density is 2,650 kg/m³.

        Its lower density creates an opportunity to
        separate it from the heavier hematite fraction
        using suitable gravity-based equipment.
        """
    )

st.markdown("### Why particle size also matters")

st.markdown("""
The separation depends on both particle density and particle size.
A larger quartz particle can settle faster than a much smaller
hematite particle.

Therefore, feed-size preparation and mineral liberation are
important considerations when designing a real gravity-separation
plant.
""")

st.divider()


# ==========================================================
# 8. ASPEN STREAM RESULTS
# ==========================================================

section_title(
    "Aspen Stream Data",
    "Component flow rates recovered from the saved simulation case."
)

if CSV_PATH.exists():

    try:

        df = pd.read_csv(CSV_PATH)

        required_columns = [
            "stream_id",
            "description",
            "hematite_kg_hr",
            "quartz_kg_hr",
            "water_kg_hr",
            "total_kg_hr"
        ]

        missing = [
            col for col in required_columns
            if col not in df.columns
        ]

        if missing:

            st.error(
                "The Aspen CSV is missing the following columns: "
                + ", ".join(missing)
            )

        else:

            selected_streams = [
                "ORE-FEED",
                "O-F",
                "U-F",
                "MIXED",
                "CONC",
                "TAIL"
            ]

            display_df = df[
                df["stream_id"].isin(selected_streams)
            ].copy()

            display_df = display_df[
                required_columns
            ]

            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "stream_id": st.column_config.TextColumn(
                        "Stream ID"
                    ),
                    "description": st.column_config.TextColumn(
                        "Description"
                    ),
                    "hematite_kg_hr": st.column_config.NumberColumn(
                        "Hematite (kg/h)",
                        format="%.2f"
                    ),
                    "quartz_kg_hr": st.column_config.NumberColumn(
                        "Quartz (kg/h)",
                        format="%.2f"
                    ),
                    "water_kg_hr": st.column_config.NumberColumn(
                        "Water (kg/h)",
                        format="%.2f"
                    ),
                    "total_kg_hr": st.column_config.NumberColumn(
                        "Total (kg/h)",
                        format="%.2f"
                    )
                }
            )

            st.caption(
                "Values represent the saved Aspen operating case. "
                "They are not a multi-condition performance dataset."
            )

    except Exception as error:

        st.error(
            f"Unable to read the Aspen CSV: {error}"
        )

else:

    st.warning(
        "The file data/aspen_stream_results.csv was not found. "
        "Add the Aspen stream-results CSV to the data folder "
        "to display the stream table."
    )


st.divider()


# ==========================================================
# 9. PROCESS OUTPUTS
# ==========================================================

section_title(
    "Final Product Streams",
    "The two outlet streams leaving the separation block."
)

out1, out2 = st.columns(2, gap="large")

with out1:

    info_card(
        "HEMATITE-RICH CONCENTRATE",
        """
        This is the valuable product stream. It contains
        a greater proportion of hematite than the original
        feed under the specified Aspen component split.
        """
    )

with out2:

    info_card(
        "QUARTZ-RICH TAILINGS",
        """
        This is the waste stream. It contains the greater
        proportion of the incoming quartz and also includes
        the water reporting to the tailings outlet.
        """
    )

st.divider()


# ==========================================================
# 10. ENGINEERING ASSUMPTIONS AND LIMITATIONS
# ==========================================================

section_title(
    "Engineering Assumptions and Model Limitations",
    "Understanding what the current Aspen model actually represents."
)

with st.expander(
    "View process assumptions and simulation limitations",
    expanded=True
):

    st.markdown("""
    **Design basis**

    - Fresh ore feed: 1,000 kg/h.
    - Hematite composition: 40 wt%.
    - Quartz composition: 60 wt%.
    - Water addition: 1,200 kg/h.
    - Hematite density: approximately 5,250 kg/m³.
    - Quartz density: approximately 2,650 kg/m³.

    **Aspen model scope**

    - The saved model contains MIXER, CRUSHER, SCREEN, MIX and G-SEP.
    - The screen oversize stream is recycled to the first mixer.
    - The screen undersize is sent to the water mixer.
    - G-SEP produces concentrate and tailings using specified
      component split fractions.

    **Important limitations**

    - G-SEP is a generic separator, not a detailed physical
      spiral-concentrator or gravity-separator model.
    - The specified component split fractions determine the
      separation outputs.
    - The current backup contains one saved operating case.
    - Additional operating cases are required to demonstrate
      genuine process-performance trends.
    - Actual mineral liberation and separator performance
      require ore-specific testing or validation.
    """)

st.warning(
    "The website describes G-SEP as the gravity separator in "
    "the proposed process concept. Its current Aspen configuration "
    "does not independently simulate particle trajectories or "
    "density-dependent separation physics."
)


# ==========================================================
# 11. FOOTER
# ==========================================================

footer()
