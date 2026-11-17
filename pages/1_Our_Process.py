
import streamlit as st

st.title("Our Process")

st.markdown("""
The OreWise mineral-processing concept is designed to upgrade
hematite–quartz ore through particle-size reduction, screening
and gravity separation.

The gravity separator uses differences in particle density
and settling behaviour to separate the heavier hematite-rich
fraction from the lighter quartz-rich fraction.
""")

st.divider()

st.subheader("Process Flow Diagram")

st.graphviz_chart("""
digraph OreWise {

    rankdir=LR;

    node [
        shape=box,
        style="rounded,filled",
        fillcolor="#EAF0F5",
        color="#34495E"
    ];

    Feed [label="ORE-FEED"];
    Mixer [label="MIXER"];
    Crusher [label="JAW CRUSHER"];
    Screen [label="VIBRATING SCREEN"];
    Water [label="WATER"];
    Mix [label="SLURRY MIXER"];
    Gravity [label="GRAVITY SEPARATOR"];
    Conc [label="CONCENTRATE"];
    Tail [label="TAILINGS"];

    Feed -> Mixer;
    Screen -> Mixer [label="Oversize Recycle", style=dashed];
    Mixer -> Crusher;
    Crusher -> Screen;
    Screen -> Mix [label="Undersize"];
    Water -> Mix;
    Mix -> Gravity;
    Gravity -> Conc;
    Gravity -> Tail;
}
""")

st.divider()

st.subheader("Equipment Description")

equipment = {
    "MIXER": """
    Combines the fresh ore feed with the oversize recycle
    stream returning from the vibrating screen.
    """,

    "JAW CRUSHER": """
    Reduces the particle size of the incoming ore.
    This prepares the material for subsequent screening
    and separation.
    """,

    "VIBRATING SCREEN": """
    Separates particles according to their size.
    Oversized particles are recycled for further crushing,
    while undersized particles proceed to the next stage.
    """,

    "WATER MIXER": """
    Combines the screened ore with water to prepare
    a slurry for gravity separation.
    """,

    "GRAVITY SEPARATOR": """
    Separates hematite and quartz based on differences
    in particle density and settling behaviour.

    The heavier hematite-rich particles are directed
    towards the concentrate stream, while the lighter
    quartz-rich particles report mainly to the tailings.
    """
}

for name, description in equipment.items():

    with st.expander(name):

        st.write(description)

st.divider()

st.subheader("Expected Products")

col1, col2 = st.columns(2)

with col1:

    st.markdown("### Hematite-rich Concentrate")

    st.write("""
    The valuable product stream containing a higher
    proportion of hematite.
    """)

with col2:

    st.markdown("### Quartz-rich Tailings")

    st.write("""
    The waste stream containing a greater proportion
    of quartz and rejected gangue material.
    """)

st.warning("""
Engineering note: The uploaded Aspen model contains the
blocks MIXER, CRUSHER, SCREEN, MIX and G-SEP.

The website describes G-SEP as the gravity separator.
Its exact physical separation mechanism and performance
should be checked against the block configuration in Aspen Plus.
""")
