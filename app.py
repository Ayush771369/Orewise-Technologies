import streamlit as st

st.set_page_config(page_title="OreWise Technologies", page_icon="⛏️", layout="wide")

st.title("⛏️ OreWise Technologies")
st.subheader("Affordable, modular iron-ore beneficiation")
st.markdown("""
OreWise is a proposed engineering startup designing compact mineral-processing
plants for small-scale operators. The concept aims to upgrade low-grade
hematite–quartz ore through controlled size reduction, classification and
gravity concentration.
""")

c1, c2, c3 = st.columns(3)
c1.metric("Design feed rate", "1,000 kg/h")
c2.metric("Hematite in feed", "40 wt%")
c3.metric("Quartz in feed", "60 wt%")

st.markdown("### The proposed process")
st.write(
    "Raw ore → Jaw crusher → Vibrating screen → Wet grinding → "
    "Hydrocyclone/classifier → Spiral concentrator → Concentrate + tailings"
)
st.info(
    "This is a preliminary educational design. The sample simulator dataset is "
    "illustrative only and must be replaced with verified Aspen Plus V14 results "
    "before reporting plant performance."
)

st.markdown("### Explore the project")
st.markdown("""
Use the pages in the sidebar:
- **Our Process:** equipment sequence and stream descriptions.
- **Plant Simulator:** explore the supplied illustrative dataset.
- **Engineering:** assumptions, Python particle calculation and data notes.
- **Market & Competitors:** the competitor landscape supplied in the project context.
""")
