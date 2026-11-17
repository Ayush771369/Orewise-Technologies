
import streamlit as st

st.set_page_config(
    page_title="OreWise Technologies",
    page_icon="⛏️",
    layout="wide"
)

st.title("⛏️ OreWise Technologies")

st.subheader(
    "Affordable, Modular Iron Ore Beneficiation"
)

st.markdown("""
OreWise Technologies is a proposed engineering startup focused on
developing affordable, modular mineral-processing plants for
small-scale mining operators.

Our proposed plant upgrades hematite–quartz ore by using
particle-size reduction, screening and gravity separation.
""")

st.divider()

st.subheader("Our Design Basis")

col1, col2, col3 = st.columns(3)

col1.metric("Fresh Ore Feed", "1,000 kg/h")
col2.metric("Hematite Content", "40 wt%")
col3.metric("Quartz Content", "60 wt%")

st.divider()

st.subheader("Our Mineral Processing Route")

st.write("""
Raw Ore → Mixer → Jaw Crusher → Vibrating Screen →
Water Addition → Gravity Separator →
Hematite-rich Concentrate + Quartz-rich Tailings
""")

st.graphviz_chart("""
digraph OreWise {

    rankdir=LR;

    node [
        shape=box,
        style="rounded,filled",
        fillcolor="#EAF0F5",
        color="#34495E"
    ];

    Feed [label="Raw Ore Feed"];
    Mixer [label="Mixer"];
    Crusher [label="Jaw Crusher"];
    Screen [label="Vibrating Screen"];
    Water [label="Water Addition"];
    Mix [label="Slurry Mixer"];
    Gravity [label="Gravity Separator"];
    Conc [label="Hematite-rich Concentrate"];
    Tail [label="Quartz-rich Tailings"];

    Feed -> Mixer;
    Mixer -> Crusher;
    Crusher -> Screen;
    Screen -> Mix;
    Water -> Mix;
    Mix -> Gravity;
    Gravity -> Conc;
    Gravity -> Tail;
}
""")

st.info("""
The website includes stream results from the uploaded Aspen Plus
simulation. The current Aspen dataset represents one saved
operating case.
""")

st.divider()

st.subheader("Explore Our Website")

st.markdown("""
Use the navigation menu to explore:

- **Our Process:** Equipment and process-flow explanation.
- **Plant Simulator:** Aspen Plus stream results and plant performance.
- **Engineering Calculations:** Python particle-settling calculations.
- **Market & Competitors:** Industrial competitors and market positioning.
""")

st.caption(
    "OreWise Technologies | ChE 303 Fluid Particle Systems Project"
)
