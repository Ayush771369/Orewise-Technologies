import streamlit as st

st.title("Market & Competitors")
st.write(
    "The companies below are industrial equipment suppliers and technology "
    "providers identified in the project research. They are useful benchmarks, "
    "but should not all be described as direct competitors to a small modular plant."
)

competitors = [
    ("Metso", "Integrated crushing, screening, grinding, separation, dewatering and tailings solutions.", "Broad integrated processing circuits."),
    ("Multotec", "Iron-ore processing technologies including spirals, jigs, cyclones, screens and magnetic separators.", "Relevant iron-ore flowsheets and multiple size-fraction routes."),
    ("Weir Minerals", "Slurry pumps, hydrocyclones, screening and comminution equipment.", "Strong focus on slurry transport and classification."),
    ("FLSmidth", "Mining equipment and processing technologies across crushing, grinding, classification and separation.", "Integrated equipment and process technologies."),
    ("TOMRA Mining", "Sensor-based ore sorting and pre-concentration.", "Potential rejection of waste before downstream processing, subject to ore suitability."),
]
for name, offering, difference in competitors:
    with st.expander(name):
        st.write("**Offerings:** " + offering)
        st.write("**Relevant distinction:** " + difference)

st.subheader("OreWise proposed positioning")
st.write(
    "OreWise proposes a compact, modular and lower-complexity plant concept "
    "aimed at small-scale operators. This is a proposed positioning statement, "
    "not evidence that the design is already cheaper or better than the listed suppliers."
)
st.caption("Add verified company locations, product pages, quotations and India-specific competitors before the final presentation.")
