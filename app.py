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

st.markdown("### Current Aspen Process")

st.write(
    "Fresh Ore → Mixer → Crusher → Screen → "
    "Water Addition → Separator → Concentrate + Tailings"
)

st.info(
    "The website includes stream results from the uploaded "
    "Aspen Plus simulation. The current dataset represents "
    "one saved operating case."
)
