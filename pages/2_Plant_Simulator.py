
import streamlit as st
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
csv_path = ROOT / "data" / "aspen_stream_results.csv"

st.title("Aspen Plus Simulation Results")
st.caption("Results imported from the uploaded Aspen Plus project.")

df = pd.read_csv(csv_path)

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
    (conc["hematite_kg_hr"] + conc["quartz_kg_hr"]) * 100
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

c1, c2, c3, c4 = st.columns(4)

c1.metric("Concentrate Flow", f"{conc['total_kg_hr']:.1f} kg/h")
c2.metric("Hematite Recovery", f"{recovery:.1f}%")
c3.metric("Concentrate Grade", f"{grade_dry:.2f}%")
c4.metric("Quartz Rejection", f"{quartz_rejection:.1f}%")

st.divider()

# Stream results
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

input_flow = feed["total_kg_hr"] + water["total_kg_hr"]
output_flow = conc["total_kg_hr"] + tail["total_kg_hr"]

a, b, c = st.columns(3)

a.metric("Total Input", f"{input_flow:.1f} kg/h")
b.metric("Total Output", f"{output_flow:.1f} kg/h")
c.metric(
    "Mass Balance Difference",
    f"{input_flow - output_flow:.2f} kg/h"
)

st.write(
    f"**Dry-basis concentrate grade:** {grade_dry:.2f} wt%"
)

st.write(
    f"**Wet-basis concentrate hematite fraction:** {grade_wet:.2f} wt%"
)

st.info(
    "These results represent one saved Aspen simulation case. "
    "Additional Aspen simulations are required to study how "
    "performance changes with operating conditions."
)
