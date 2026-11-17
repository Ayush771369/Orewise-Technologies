import streamlit as st
import pandas as pd
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from calculations.interpolation import interpolate_results, load_dataset

st.title("Plant Simulator")
st.caption("Dataset-driven demonstration — replace the illustrative CSV with Aspen-exported results.")

csv_path = ROOT / "data" / "aspen_results_sample.csv"
df = load_dataset(csv_path)

st.sidebar.header("Operating conditions")
feed_min, feed_max = int(df.feed_rate_kg_hr.min()), int(df.feed_rate_kg_hr.max())
p80_min, p80_max = int(df.grind_p80_um.min()), int(df.grind_p80_um.max())

feed = st.sidebar.slider("Feed rate (kg/h)", feed_min, feed_max, 1000, 100)
p80 = st.sidebar.slider("Grinding product P80 (µm)", p80_min, p80_max, 500, 50)

try:
    result = interpolate_results(df, feed, p80)
    st.subheader("Estimated results from the supplied dataset")
    a, b, c = st.columns(3)
    a.metric("Concentrate flow", f"{result['concentrate_mass_kg_hr']:.1f} kg/h")
    b.metric("Hematite recovery", f"{result['hematite_recovery_pct']:.1f}%")
    c.metric("Concentrate hematite", f"{result['concentrate_hematite_wt_pct']:.1f} wt%")

    d, e = st.columns(2)
    d.metric("Tailings flow", f"{result['tailings_mass_kg_hr']:.1f} kg/h")
    e.metric("Tailings hematite", f"{result['tailings_hematite_wt_pct']:.1f} wt%")

    st.subheader("Effect of grinding size at the selected feed rate")
    curve = df[df.feed_rate_kg_hr == feed].sort_values("grind_p80_um")
    if not curve.empty:
        st.line_chart(curve.set_index("grind_p80_um")[[
            "hematite_recovery_pct", "concentrate_hematite_wt_pct"
        ]])
        st.caption("X-axis: grinding product P80 (µm). Y-axis: percentage.")
    st.subheader("Interpolated values")
    st.dataframe(pd.DataFrame([result]).round(2), use_container_width=True)
except ValueError as exc:
    st.error(str(exc))

st.info(
    "Valid range is limited to the minimum and maximum values in the CSV. "
    "The app does not extrapolate outside this range."
)
