import streamlit as st

st.title("Our Process")
st.write(
    "The preliminary OreWise flowsheet prepares hematite–quartz ore for "
    "gravity concentration. Classification prepares and controls the feed; "
    "the spiral concentrator is the principal beneficiation stage."
)

st.graphviz_chart("""
digraph OreWise {
  rankdir=LR;
  node [shape=box, style="rounded,filled", fillcolor="#EAF0F5", color="#34495E"];
  Feed -> Crusher -> Screen -> Grinding -> Classifier -> Spiral;
  Screen -> Recycle [label="Oversize", style=dashed];
  Recycle -> Crusher [style=dashed];
  Classifier -> Slimes [label="Fines/slimes"];
  Spiral -> Concentrate [label="Hematite-rich"];
  Spiral -> Tailings [label="Quartz-rich"];
}
""")

st.subheader("Equipment and purpose")
equipment = [
    ("CRU-1 — Jaw crusher", "Primary particle-size reduction of incoming run-of-mine ore."),
    ("SCR-1 — Vibrating screen", "Separates by particle size; oversize is recycled to the crusher."),
    ("GR-1 — Wet grinding mill", "Further size reduction to promote liberation of hematite from quartz."),
    ("CLA-1 — Hydrocyclone/classifier", "Controls slurry particle-size distribution and manages fine/slimes material."),
    ("SP-1 — Spiral concentrator", "Gravity concentration based on differences in particle density and flow behaviour."),
]
for name, purpose in equipment:
    with st.expander(name):
        st.write(purpose)

st.warning(
    "The liberation size and actual separation performance are ore-specific. "
    "The proposed grinding target and all equipment efficiencies require "
    "validation through mineralogical testing and/or suitable experimental data."
)

st.subheader("Design basis")
st.table({
    "Parameter": ["Feed rate", "Hematite", "Quartz", "Temperature", "Pressure"],
    "Proposed value": ["1,000 kg/h", "40 wt%", "60 wt%", "25 °C", "1 bar"],
    "Status": ["Design assumption"] * 5
})
