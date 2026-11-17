
import streamlit as st
import sys

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(ROOT))

from calculations.equipment_model import terminal_velocity_sphere

st.title("Engineering Calculations")

st.subheader(
    "Python Model: Particle Settling in Gravity Separation"
)

st.markdown("""
Gravity separation depends on differences in particle density,
size and settling behaviour.

Hematite has a higher density than quartz. Therefore,
under suitable conditions, hematite particles can settle
differently from quartz particles in a fluid.

This Python calculator estimates the terminal settling
velocity and particle Reynolds number for an individual
spherical particle.
""")

st.divider()

st.subheader("Input Parameters")

col1, col2 = st.columns(2)

with col1:

    diameter = st.number_input(
        "Particle Diameter (µm)",
        min_value=10.0,
        max_value=2000.0,
        value=100.0,
        step=10.0
    )

    particle_density = st.number_input(
        "Particle Density (kg/m³)",
        min_value=1000.0,
        max_value=8000.0,
        value=5250.0,
        step=50.0
    )

with col2:

    fluid_density = st.number_input(
        "Water Density (kg/m³)",
        min_value=900.0,
        max_value=1200.0,
        value=1000.0,
        step=10.0
    )

    viscosity = st.number_input(
        "Dynamic Viscosity (Pa·s)",
        min_value=0.0001,
        max_value=0.01,
        value=0.001,
        format="%.5f"
    )

st.divider()

if st.button("Calculate Settling Behaviour"):

    try:

        result = terminal_velocity_sphere(
            diameter * 1e-6,
            particle_density,
            fluid_density,
            viscosity
        )

        col1, col2 = st.columns(2)

        col1.metric(
            "Terminal Settling Velocity",
            f"{result['velocity_m_s']:.6g} m/s"
        )

        col2.metric(
            "Particle Reynolds Number",
            f"{result['reynolds_number']:.4g}"
        )

        st.success(
            f"Estimated flow regime: {result['regime']}"
        )

    except ValueError as error:

        st.error(str(error))

st.divider()

st.subheader("Governing Equations")

st.latex(
    r"Re_p = \frac{\rho_f v_t d_p}{\mu}"
)

st.latex(
    r"F_D = \frac{1}{2} C_D \rho_f A v_t^2"
)

st.write("""
Where:

- Reₚ = Particle Reynolds number
- ρf = Fluid density (kg/m³)
- vt = Terminal settling velocity (m/s)
- dp = Particle diameter (m)
- μ = Dynamic viscosity (Pa·s)
- CD = Drag coefficient
- A = Projected particle area (m²)
""")

st.divider()

st.subheader("Model Assumptions")

st.markdown("""
1. Particles are assumed to be spherical.
2. Particles settle individually in a Newtonian fluid.
3. Steady terminal settling conditions are assumed.
4. Hindered settling is neglected.
5. Particle interactions and wall effects are neglected.
6. The drag coefficient is estimated using a simplified
   correlation.
""")

st.warning("""
This is an equipment-level particle calculation.
It demonstrates the settling principles relevant to gravity
separation, but it does not independently predict the actual
G-SEP concentrate recovery or grade.
""")
