
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import sys

from pathlib import Path

from styles import (
    load_css,
    page_header,
    section_title,
    metric_card,
    info_card,
    status_pill,
    footer,
)

# Import the existing engineering calculation
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from calculations.equipment_model import terminal_velocity_sphere


# ==========================================================
# 1. PAGE CONFIGURATION
# ==========================================================

load_css()

st.title("")


# ==========================================================
# 2. PAGE HEADER
# ==========================================================

page_header(
    title="Engineering Laboratory",
    eyebrow="OREWISE | FLUID PARTICLE SYSTEMS",
    description=(
        "Explore the physics of particle settling through "
        "interactive terminal-velocity calculations, Reynolds "
        "number analysis and mineral behaviour comparisons."
    )
)

status_pill("PYTHON CALCULATION", "green")
status_pill("PARTICLE SETTLING MODEL", "blue")

st.divider()


# ==========================================================
# 3. ENGINEERING INTRODUCTION
# ==========================================================

section_title(
    "Understanding Particle Behaviour",
    "The physical principles behind gravity-based mineral separation."
)

st.markdown("""
Gravity separation depends on differences in how mineral
particles behave when moving through a fluid.

Hematite has a higher density than quartz. Therefore, particles
of comparable size can have different settling velocities
in water.

This engineering laboratory uses Python to calculate the
terminal settling velocity and particle Reynolds number
of individual spherical particles.
""")

c1, c2 = st.columns(2, gap="large")

with c1:

    info_card(
        "HEMATITE | Fe₂O₃",
        """
        Valuable iron-bearing mineral.

        Approximate particle density used in the design basis:
        5,250 kg/m³.
        """
    )

with c2:

    info_card(
        "QUARTZ | SiO₂",
        """
        Unwanted gangue mineral.

        Approximate particle density used in the design basis:
        2,650 kg/m³.
        """
    )


st.divider()


# ==========================================================
# 4. INPUT PARAMETERS
# ==========================================================

section_title(
    "Particle Simulation Controls",
    "Change the particle and fluid properties to investigate settling behaviour."
)

col1, col2 = st.columns(2, gap="large")

with col1:

    st.markdown("### Particle Properties")

    hematite_density = st.number_input(
        "Hematite density (kg/m³)",
        min_value=1001.0,
        max_value=8000.0,
        value=5250.0,
        step=50.0
    )

    quartz_density = st.number_input(
        "Quartz density (kg/m³)",
        min_value=1001.0,
        max_value=8000.0,
        value=2650.0,
        step=50.0
    )

    particle_diameter = st.slider(
        "Selected particle diameter (µm)",
        min_value=10,
        max_value=1000,
        value=100,
        step=10
    )


with col2:

    st.markdown("### Fluid Properties")

    fluid_density = st.number_input(
        "Water density (kg/m³)",
        min_value=900.0,
        max_value=1200.0,
        value=1000.0,
        step=10.0
    )

    viscosity = st.number_input(
        "Dynamic viscosity (Pa·s)",
        min_value=0.0001,
        max_value=0.01,
        value=0.001,
        format="%.5f"
    )

    gravity = st.number_input(
        "Gravitational acceleration (m/s²)",
        min_value=9.0,
        max_value=10.0,
        value=9.81,
        step=0.01
    )


st.info(
    "Both mineral densities must be greater than the fluid density "
    "for the downward settling calculation used here."
)


# ==========================================================
# 5. VALIDATE INPUTS
# ==========================================================

if hematite_density <= fluid_density:

    st.error(
        "Hematite density must be greater than fluid density."
    )

    st.stop()


if quartz_density <= fluid_density:

    st.error(
        "Quartz density must be greater than fluid density."
    )

    st.stop()


if particle_diameter <= 0 or viscosity <= 0:

    st.error(
        "Particle diameter and viscosity must be positive."
    )

    st.stop()


# ==========================================================
# 6. CALCULATE SELECTED PARTICLE RESULTS
# ==========================================================

diameter_m = particle_diameter * 1e-6

try:

    hematite_result = terminal_velocity_sphere(
        diameter_m=diameter_m,
        particle_density=hematite_density,
        fluid_density=fluid_density,
        viscosity=viscosity,
        gravity=gravity
    )

    quartz_result = terminal_velocity_sphere(
        diameter_m=diameter_m,
        particle_density=quartz_density,
        fluid_density=fluid_density,
        viscosity=viscosity,
        gravity=gravity
    )

except (ValueError, ZeroDivisionError, OverflowError) as error:

    st.error(f"Calculation error: {error}")
    st.stop()


hematite_velocity = hematite_result["velocity_m_s"]
quartz_velocity = quartz_result["velocity_m_s"]

hematite_reynolds = hematite_result["reynolds_number"]
quartz_reynolds = quartz_result["reynolds_number"]


# ==========================================================
# 7. SELECTED PARTICLE RESULTS
# ==========================================================

st.divider()

section_title(
    "Calculated Particle Performance",
    f"Results for particles with a diameter of {particle_diameter} µm."
)

c1, c2 = st.columns(2, gap="large")

with c1:

    st.markdown("### Hematite")

    metric_card(
        "TERMINAL SETTLING VELOCITY",
        f"{hematite_velocity:.6g}",
        "m/s",
        accent="amber"
    )

    st.markdown("")

    metric_card(
        "PARTICLE REYNOLDS NUMBER",
        f"{hematite_reynolds:.4g}",
        hematite_result["regime"],
        accent="blue"
    )


with c2:

    st.markdown("### Quartz")

    metric_card(
        "TERMINAL SETTLING VELOCITY",
        f"{quartz_velocity:.6g}",
        "m/s",
        accent="green"
    )

    st.markdown("")

    metric_card(
        "PARTICLE REYNOLDS NUMBER",
        f"{quartz_reynolds:.4g}",
        quartz_result["regime"],
        accent="blue"
    )


# Calculate relative settling velocity

if quartz_velocity > 0:

    settling_ratio = hematite_velocity / quartz_velocity

else:

    settling_ratio = 0


st.divider()


# ==========================================================
# 8. SETTLING VELOCITY COMPARISON
# ==========================================================

section_title(
    "Mineral Settling Comparison",
    "Compare the calculated settling behaviour of hematite and quartz."
)

comparison_fig = go.Figure()

comparison_fig.add_trace(
    go.Bar(
        name="Hematite",
        x=["Hematite", "Quartz"],
        y=[hematite_velocity, 0],
        marker_color="#E69B45",
        text=[
            f"{hematite_velocity:.5g}",
            ""
        ],
        textposition="outside"
    )
)

comparison_fig.add_trace(
    go.Bar(
        name="Quartz",
        x=["Hematite", "Quartz"],
        y=[0, quartz_velocity],
        marker_color="#7192A7",
        text=[
            "",
            f"{quartz_velocity:.5g}"
        ],
        textposition="outside"
    )
)

comparison_fig.update_layout(
    barmode="overlay",
    height=370,
    paper_bgcolor="white",
    plot_bgcolor="white",
    title="Terminal Settling Velocity at Selected Particle Size",
    xaxis_title="Mineral",
    yaxis_title="Terminal velocity (m/s)",
    font=dict(
        family="Arial",
        color="#142638"
    ),
    showlegend=False,
    margin=dict(l=30, r=30, t=65, b=30)
)

comparison_fig.update_yaxes(
    gridcolor="#E8EDF1",
    zeroline=False
)

st.plotly_chart(
    comparison_fig,
    use_container_width=True
)


ratio_col1, ratio_col2 = st.columns(2)

with ratio_col1:

    metric_card(
        "SETTLING VELOCITY RATIO",
        f"{settling_ratio:.2f} : 1",
        "Hematite relative to quartz",
        accent="amber"
    )

with ratio_col2:

    difference = hematite_velocity - quartz_velocity

    metric_card(
        "VELOCITY DIFFERENCE",
        f"{difference:.6g}",
        "m/s",
        accent="green"
    )


st.caption(
    "These results compare isolated spherical particles of equal diameter. "
    "They do not predict the recovery or efficiency of a real gravity separator."
)


st.divider()


# ==========================================================
# 9. PARTICLE DIAMETER STUDY
# ==========================================================

section_title(
    "Effect of Particle Diameter",
    "Investigate how particle size affects terminal settling velocity."
)

diameters_um = np.linspace(10, 1000, 60)

hematite_velocities = []
quartz_velocities = []

hematite_re_values = []
quartz_re_values = []


for diameter in diameters_um:

    d_m = diameter * 1e-6

    try:

        h_result = terminal_velocity_sphere(
            diameter_m=d_m,
            particle_density=hematite_density,
            fluid_density=fluid_density,
            viscosity=viscosity,
            gravity=gravity
        )

        q_result = terminal_velocity_sphere(
            diameter_m=d_m,
            particle_density=quartz_density,
            fluid_density=fluid_density,
            viscosity=viscosity,
            gravity=gravity
        )

        hematite_velocities.append(
            h_result["velocity_m_s"]
        )

        quartz_velocities.append(
            q_result["velocity_m_s"]
        )

        hematite_re_values.append(
            h_result["reynolds_number"]
        )

        quartz_re_values.append(
            q_result["reynolds_number"]
        )

    except (ValueError, ZeroDivisionError, OverflowError):

        hematite_velocities.append(np.nan)
        quartz_velocities.append(np.nan)

        hematite_re_values.append(np.nan)
        quartz_re_values.append(np.nan)


# Terminal velocity graph

velocity_fig = go.Figure()

velocity_fig.add_trace(
    go.Scatter(
        x=diameters_um,
        y=hematite_velocities,
        mode="lines",
        name="Hematite",
        line=dict(
            color="#E69B45",
            width=3
        )
    )
)

velocity_fig.add_trace(
    go.Scatter(
        x=diameters_um,
        y=quartz_velocities,
        mode="lines",
        name="Quartz",
        line=dict(
            color="#426A85",
            width=3
        )
    )
)

velocity_fig.add_vline(
    x=particle_diameter,
    line_dash="dash",
    line_color="#718096",
    annotation_text="Selected size"
)

velocity_fig.update_layout(
    height=440,
    paper_bgcolor="white",
    plot_bgcolor="white",
    title="Terminal Settling Velocity vs Particle Diameter",
    xaxis_title="Particle diameter (µm)",
    yaxis_title="Terminal settling velocity (m/s)",
    font=dict(
        family="Arial",
        color="#142638"
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    margin=dict(l=30, r=30, t=85, b=40)
)

velocity_fig.update_xaxes(
    gridcolor="#E8EDF1",
    zeroline=False
)

velocity_fig.update_yaxes(
    gridcolor="#E8EDF1",
    zeroline=False
)

st.plotly_chart(
    velocity_fig,
    use_container_width=True
)


st.markdown("""
**Engineering interpretation**

At the same particle diameter and fluid conditions,
the denser hematite particles generally have a higher
settling velocity than quartz particles in this model.

Particle size also affects settling velocity.
Therefore, size control is important when preparing
ore for gravity separation.
""")


st.divider()


# ==========================================================
# 10. PARTICLE REYNOLDS NUMBER GRAPH
# ==========================================================

section_title(
    "Particle Reynolds Number Analysis",
    "Understand the flow regime associated with particle settling."
)

re_fig = go.Figure()

re_fig.add_trace(
    go.Scatter(
        x=diameters_um,
        y=hematite_re_values,
        mode="lines",
        name="Hematite",
        line=dict(
            color="#E69B45",
            width=3
        )
    )
)

re_fig.add_trace(
    go.Scatter(
        x=diameters_um,
        y=quartz_re_values,
        mode="lines",
        name="Quartz",
        line=dict(
            color="#426A85",
            width=3
        )
    )
)

re_fig.update_layout(
    height=400,
    paper_bgcolor="white",
    plot_bgcolor="white",
    title="Particle Reynolds Number vs Particle Diameter",
    xaxis_title="Particle diameter (µm)",
    yaxis_title="Particle Reynolds number",
    font=dict(
        family="Arial",
        color="#142638"
    ),
    margin=dict(l=30, r=30, t=65, b=40)
)

re_fig.update_xaxes(
    gridcolor="#E8EDF1"
)

re_fig.update_yaxes(
    gridcolor="#E8EDF1"
)

st.plotly_chart(
    re_fig,
    use_container_width=True
)


st.divider()


# ==========================================================
# 11. GOVERNING EQUATIONS
# ==========================================================

section_title(
    "Governing Equations",
    "Mathematical relationships implemented in the Python model."
)

with st.expander(
    "View equations and variable definitions",
    expanded=True
):

    st.markdown("### Force balance at terminal settling velocity")

    st.latex(
        r"""
        F_{\text{weight}}-F_{\text{buoyancy}}=F_{\text{drag}}
        """
    )

    st.latex(
        r"""
        (\rho_p-\rho_f)\frac{\pi d_p^3}{6}g
        =
        \frac{1}{2}C_D\rho_f
        \frac{\pi d_p^2}{4}v_t^2
        """
    )

    st.markdown("### Particle Reynolds number")

    st.latex(
        r"""
        Re_p=\frac{\rho_f v_t d_p}{\mu}
        """
    )

    st.markdown("### Schiller–Naumann drag coefficient")

    st.latex(
        r"""
        C_D=\frac{24}{Re_p}
        \left(1+0.15Re_p^{0.687}\right)
        """
    )

    st.markdown("""
    | Symbol | Description | Unit |
    |---|---|---|
    | ρp | Particle density | kg/m³ |
    | ρf | Fluid density | kg/m³ |
    | dp | Particle diameter | m |
    | vt | Terminal settling velocity | m/s |
    | CD | Drag coefficient | Dimensionless |
    | μ | Dynamic viscosity | Pa·s |
    | Rep | Particle Reynolds number | Dimensionless |
    | g | Gravitational acceleration | m/s² |
    """)

    st.caption(
        "The implemented model uses the Schiller–Naumann "
        "correlation below Re = 1000 and a constant drag "
        "coefficient approximation above that range."
    )


st.divider()


# ==========================================================
# 12. INDEPENDENT VERIFICATION USING STOKES' LAW
# ==========================================================

section_title(
    "Independent Verification",
    "Compare the iterative Python model with Stokes' law in the creeping-flow range."
)

st.markdown("""
For sufficiently small spherical particles at very low Reynolds
number, Stokes' law provides an independent analytical estimate
of terminal settling velocity.
""")

verification_size = st.number_input(
    "Verification particle diameter (µm)",
    min_value=1.0,
    max_value=100.0,
    value=10.0,
    step=1.0
)

verification_mineral = st.selectbox(
    "Mineral for verification",
    ["Hematite", "Quartz"]
)

if verification_mineral == "Hematite":

    verification_density = hematite_density

else:

    verification_density = quartz_density


d_verify = verification_size * 1e-6

# Python iterative model

verification_result = terminal_velocity_sphere(
    diameter_m=d_verify,
    particle_density=verification_density,
    fluid_density=fluid_density,
    viscosity=viscosity,
    gravity=gravity
)

python_velocity = verification_result["velocity_m_s"]

verification_reynolds = verification_result["reynolds_number"]


# Stokes law calculation

stokes_velocity = (
    (verification_density - fluid_density)
    * gravity
    * d_verify ** 2
    / (18 * viscosity)
)


if stokes_velocity > 0:

    percentage_difference = (
        abs(python_velocity - stokes_velocity)
        / stokes_velocity
    ) * 100

else:

    percentage_difference = np.nan


v1, v2, v3 = st.columns(3)

with v1:

    metric_card(
        "PYTHON MODEL",
        f"{python_velocity:.6g}",
        "m/s",
        accent="amber"
    )

with v2:

    metric_card(
        "STOKES' LAW",
        f"{stokes_velocity:.6g}",
        "m/s",
        accent="blue"
    )

with v3:

    metric_card(
        "PERCENTAGE DIFFERENCE",
        f"{percentage_difference:.3f}%",
        "Absolute relative difference",
        accent="green"
    )


if verification_reynolds < 0.2:

    st.success(
        f"Reynolds number = {verification_reynolds:.5f}. "
        "This is within the creeping-flow range where "
        "Stokes' law is appropriate for an isolated sphere."
    )

else:

    st.warning(
        f"Reynolds number = {verification_reynolds:.5f}. "
        "Stokes' law is not sufficiently applicable at "
        "this condition. Use the Python model result with "
        "the stated drag-correlation assumptions."
    )


st.latex(
    r"""
    v_{t,\text{Stokes}}=
    \frac{(\rho_p-\rho_f)gd_p^2}{18\mu}
    """
)


st.divider()


# ==========================================================
# 13. ASSUMPTIONS AND LIMITATIONS
# ==========================================================

section_title(
    "Model Assumptions and Limitations",
    "Conditions that affect the accuracy of the particle calculation."
)

with st.expander(
    "View engineering assumptions",
    expanded=False
):

    st.markdown("""
    **Model assumptions**

    1. Particles are spherical.
    2. Particles settle individually.
    3. The fluid behaves as a Newtonian liquid.
    4. Steady terminal settling is assumed.
    5. Hindered settling is neglected.
    6. Particle interactions are neglected.
    7. Wall effects are neglected.
    8. The drag relationship is approximated using
       the implemented correlations.

    **Engineering limitations**

    - Actual mineral particles are irregular in shape.
    - Real slurries may have higher solids concentrations.
    - Turbulence and particle interactions may affect settling.
    - Mineral liberation affects the behaviour of composite particles.
    - A single-particle calculation does not predict an entire
      gravity separator's concentrate grade or recovery.
    """)

st.warning(
    "This is an individual-particle settling model. It demonstrates "
    "the Fluid Particle Systems principles relevant to gravity "
    "separation, but it is not a validated physical model of G-SEP."
)


# ==========================================================
# 14. FOOTER
# ==========================================================

footer()
