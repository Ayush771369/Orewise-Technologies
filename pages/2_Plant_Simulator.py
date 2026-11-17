
import streamlit as st
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

csv_path = ROOT / "data" / "aspen_stream_results.csv"

st.title("Aspen Plus Simulation Results")

st.caption(
    "Results imported from the uploaded Aspen Plus simulation."
)

# Load Aspen stream data
df = pd.read_csv(csv_path)

# Identify important streams
conc = df[df["stream_id"] == "CONC"].iloc[0]

tail = df[df["stream_id"] == "TAIL"].iloc[0]

feed = df[df["stream_id"] == "ORE-FEED"].iloc[0]

water = df[df["stream_id"] == "WATER"].iloc[0]

# Calculate performance indicators
recovery = (
    conc["hematite_kg_hr"] /
    feed["hematite_kg_hr"] * 100
)

grade_dry = (
    conc["hematite_kg_hr"] /
    (
        conc["hematite_kg_hr"] +
        conc["quartz_kg_hr"]
    ) * 100
)

grade_wet = (
    conc["hematite_kg_hr"] /
    conc["total_kg_hr"] * 100
)

quartz_rejection = (
    tail["quartz_kg_hr"] /
    feed["quartz_kg_hr"] * 100
)

# Performance indicators
st.subheader("Plant Performance")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Concentrate Flow",
    f"{conc['total_kg_hr']:.1f} kg/h"
)

col2.metric(
    "Hematite Recovery",
    f"{recovery:.1f}%"
)

col3.metric(
    "Concentrate Grade",
    f"{grade_dry:.2f}%"
)

col4.metric(
    "Quartz Rejection",
    f"{quartz_rejection:.1f}%"
)

st.divider()

# Aspen stream results
st.subheader("Aspen Stream Results")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

st.divider()

# Product composition chart
st.subheader("Product Composition")

chart_data = pd.DataFrame({

    "Hematite": [
        conc["hematite_kg_hr"],
        tail["hematite_kg_hr"]
    ],

    "Quartz": [
        conc["quartz_kg_hr"],
        tail["quartz_kg_hr"]
    ],

    "Water": [
        conc["water_kg_hr"],
        tail["water_kg_hr"]
    ]

}, index=["Concentrate", "Tailings"])

st.bar_chart(chart_data)

st.divider()

# Mass balance
st.subheader("Overall Mass Balance")

input_flow = (
    feed["total_kg_hr"] +
    water["total_kg_hr"]
)

output_flow = (
    conc["total_kg_hr"] +
    tail["total_kg_hr"]
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Input",
    f"{input_flow:.1f} kg/h"
)

col2.metric(
    "Total Output",
    f"{output_flow:.1f} kg/h"
)

col3.metric(
    "Mass Balance Difference",
    f"{input_flow - output_flow:.2f} kg/h"
)

st.write(
    f"**Dry-basis concentrate grade:** {grade_dry:.2f} wt%"
)

st.write(
    f"**Wet-basis hematite fraction in concentrate:** "
    f"{grade_wet:.2f} wt%"
)

st.info("""
The results represent one saved Aspen Plus operating case.
The performance indicators are calculated from the component
flow rates in the Aspen stream data.
""")

st.warning("""
Only one operating case is currently available.
Additional Aspen simulations are required to study how
gravity-separation performance changes with operating conditions.
""")
