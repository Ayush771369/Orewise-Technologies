import streamlit as st
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from calculations.equipment_model import terminal_velocity_sphere

st.title("Engineering Calculations")
st.subheader("Python equipment-level calculation: particle settling")

st.write(
    "A particle-settling calculation is included to demonstrate how particle "
    "diameter, particle density and fluid properties influence settling. "
    "It is relevant to understanding classification and the particle behaviour "
    "that underpins gravity separation. It is not a validated spiral-separator "
    "performance model."
)

c1, c2 = st.columns(2)
with c1:
    diameter_um = st.number_input("Particle diameter (µm)", 10.0, 2000.0, 100.0, 10.0)
    particle_density = st.number_input("Particle density (kg/m³)", 1000.0, 8000.0, 5250.0, 50.0)
with c2:
    fluid_density = st.number_input("Water density (kg/m³)", 900.0, 1200.0, 1000.0, 10.0)
    viscosity = st.number_input("Dynamic viscosity (Pa·s)", 0.0001, 0.01, 0.0010, format="%.5f")
    gravity = st.number_input("Gravitational acceleration (m/s²)", 9.0, 10.0, 9.81, 0.01)

if st.button("Calculate settling behaviour"):
    out = terminal_velocity_sphere(
        diameter_um * 1e-6, particle_density, fluid_density, viscosity, gravity
    )
    st.metric("Terminal settling velocity", f"{out['velocity_m_s']:.6g} m/s")
    st.metric("Particle Reynolds number", f"{out['reynolds_number']:.4g}")
    st.write(f"Drag regime estimate: **{out['regime']}**")

st.subheader("Model and assumptions")
st.latex(r"Re_p = \\frac{\\rho_f v_t d_p}{\\mu}")
st.latex(r"F_D = \\frac{1}{2} C_D \\rho_f A v_t^2")
st.write(
    "The code balances particle weight minus buoyancy against drag for a "
    "spherical particle. The drag coefficient uses the Schiller–Naumann "
    "correlation in its usual low-to-moderate Reynolds-number range. "
    "Assumptions: isolated spherical particle, Newtonian fluid, steady terminal "
    "settling, no hindered settling, no particle interaction and no wall effects."
)
st.warning(
    "This is a simplified single-particle model. Real ore particles are irregular, "
    "and slurry concentration, turbulence and particle interactions can change "
    "settling behaviour."
)
