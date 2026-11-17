
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pathlib import Path
import sys

from styles import (
    load_css,
    page_header,
    section_title,
    metric_card,
    info_card,
    status_pill,
    footer,
)

# ==========================================================
# 1. PATHS AND EXISTING PYTHON MODEL
# ==========================================================

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

sys.path.insert(0, str(ROOT))

from calculations.equipment_model import terminal_velocity_sphere


# ==========================================================
# 2. PAGE CONFIGURATION AND STYLE
# ==========================================================

load_css()

st.title("")

page_header(
    title="Engineering Laboratory",
    eyebrow="OREWISE | FLUID PARTICLE SYSTEMS",
    description=(
        "Explore particle settling, gravity-separation behaviour "
        "and crusher energy through interactive Python calculations "
        "and multi-case Aspen simulation datasets."
    ),
)

status_pill("PYTHON CALCULATIONS", "green")
status_pill("ASPEN DATA INTEGRATED", "blue")
status_pill("GRAVITY SEPARATION", "amber")

st.divider()


# ==========================================================
# 3. DATA LOADING
# ==========================================================

DATA_FILES = {
    "settling": DATA_DIR / "settling_velocity_curves.csv",
    "partition": DATA_DIR / "settling_partition_by_size.csv",
    "grade": DATA_DIR / "idealized_grade_recovery_curve.csv",
    "bond": DATA_DIR / "bond_crusher_power.csv",
}


@st.cache_data
def read_dataset(path, modified_time):
    return pd.read_csv(path)


def load_dataset(key):
    path = DATA_FILES[key]

    if not path.exists():
        st.error(
            f"Missing dataset: {path.name}. "
            "Run scripts/build_orewise_datasets.py first."
        )
        st.stop()

    try:
        return read_dataset(str(path), path.stat().st_mtime)
    except Exception as error:
        st.error(f"Could not load {path.name}: {error}")
        st.stop()


settling_df = load_dataset("settling")
partition_df = load_dataset("partition")
grade_df = load_dataset("grade")
bond_df = load_dataset("bond")


# ==========================================================
# 4. DATA VALIDATION
# ==========================================================

required_columns = {
    "settling": [
        "case_id",
        "feed_rate_kg_hr",
        "psd_id",
        "particle_diameter_mm",
        "hematite_isolated_m_s",
        "quartz_isolated_m_s",
        "hematite_Re",
        "quartz_Re",
        "hematite_hindered_estimate_m_s",
        "quartz_hindered_estimate_m_s",
        "slurry_solids_volume_fraction",
    ],
    "partition": [
        "case_id",
        "particle_diameter_mm",
        "hematite_settling_velocity_m_s",
        "quartz_settling_velocity_m_s",
        "hematite_hindered_velocity_m_s",
        "quartz_hindered_velocity_m_s",
        "cut_velocity_m_s",
        "hematite_to_fast_product_pct",
        "quartz_to_fast_product_pct",
    ],
    "grade": [
        "case_id",
        "cut_velocity_m_s",
        "hematite_recovery_pct",
        "silica_recovery_to_concentrate_pct",
        "idealized_concentrate_grade_pct",
        "aspen_hematite_recovery_pct",
        "aspen_concentrate_grade_dry_pct",
    ],
    "bond": [
        "case_id",
        "Bond_Wi_kWh_per_t",
        "F80_mm",
        "P80_mm",
        "specific_energy_kWh_per_t",
        "crusher_throughput_including_recycle_t_hr",
        "theoretical_power_kW",
    ],
}


def validate_dataset(df, key):
    missing = [
        col for col in required_columns[key]
        if col not in df.columns
    ]

    if missing:
        st.error(
            f"{DATA_FILES[key].name} is missing columns: "
            + ", ".join(missing)
        )
        st.stop()


validate_dataset(settling_df, "settling")
validate_dataset(partition_df, "partition")
validate_dataset(grade_df, "grade")
validate_dataset(bond_df, "bond")


# Standardise case IDs for filtering.
for df in [settling_df, partition_df, grade_df, bond_df]:
    df["case_id"] = df["case_id"].astype(str)


# ==========================================================
# 5. CASE SELECTOR
# ==========================================================

all_cases = sorted(
    set(settling_df["case_id"])
    & set(partition_df["case_id"])
    & set(grade_df["case_id"])
    & set(bond_df["case_id"])
)

if not all_cases:
    st.error("No common Aspen case IDs found across the datasets.")
    st.stop()

section_title(
    "Engineering Case Selection",
    "Choose one of the nine Aspen operating cases to explore "
    "its associated Python engineering calculations."
)

default_case = "1000_1" if "1000_1" in all_cases else all_cases[0]

selected_case = st.selectbox(
    "Select Aspen case",
    all_cases,
    index=all_cases.index(default_case),
    format_func=lambda x: (
        f"{x.replace('_', ' | PSD ')} "
        f"(Feed {int(x.split('_')[0]):,} kg/h)"
    ),
)

case_settling = settling_df[
    settling_df["case_id"] == selected_case
].copy()

case_partition = partition_df[
    partition_df["case_id"] == selected_case
].copy()

case_grade = grade_df[
    grade_df["case_id"] == selected_case
].copy()

case_bond = bond_df[
    bond_df["case_id"] == selected_case
].copy()

case_feed_rate = int(case_settling["feed_rate_kg_hr"].iloc[0])
case_psd_id = int(case_settling["psd_id"].iloc[0])

s1, s2, s3 = st.columns(3)

with s1:
    metric_card(
        "SELECTED CASE",
        selected_case,
        "Aspen simulation case",
        accent="blue",
    )

with s2:
    metric_card(
        "FRESH FEED RATE",
        f"{case_feed_rate:,}",
        "kg/h",
        accent="amber",
    )

with s3:
    metric_card(
        "PARTICLE SIZE CASE",
        f"PSD {case_psd_id}",
        "Aspen feed distribution",
        accent="green",
    )

st.caption(
    "Selecting a case retrieves its saved Aspen-derived datasets. "
    "It does not run Aspen or create a new simulation."
)

st.divider()


# ==========================================================
# 6. ENGINEERING INTRODUCTION
# ==========================================================

section_title(
    "Understanding Particle Behaviour",
    "The physical principles behind gravity-based mineral separation."
)

st.markdown("""
Gravity separation uses differences in mineral particle behaviour
in a fluid.

Hematite is denser than quartz. For particles of comparable size,
hematite generally settles faster in water. This difference can
help separate valuable iron-bearing minerals from unwanted gangue.

The laboratory combines:
- An interactive single-particle settling calculator.
- Python-generated settling and partition datasets.
- Aspen-derived process operating cases.
- Bond-equation crusher energy sensitivity calculations.
""")

c1, c2 = st.columns(2, gap="large")

with c1:
    info_card(
        "HEMATITE | Fe₂O₃",
        """
        Valuable iron-bearing mineral.

        Approximate particle density used in the model:
        5,250 kg/m³.
        """
    )

with c2:
    info_card(
        "QUARTZ | SiO₂",
        """
        Unwanted gangue mineral.

        Approximate particle density used in the model:
        2,650 kg/m³.
        """
    )

st.divider()


# ==========================================================
# 7. INTERACTIVE SINGLE-PARTICLE CALCULATOR
# ==========================================================

section_title(
    "Interactive Particle Settling Calculator",
    "Change particle and fluid properties to calculate terminal "
    "settling velocity and Reynolds number."
)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("### Particle Properties")

    hematite_density = st.number_input(
        "Hematite density (kg/m³)",
        min_value=1001.0,
        max_value=8000.0,
        value=5250.0,
        step=50.0,
    )

    quartz_density = st.number_input(
        "Quartz density (kg/m³)",
        min_value=1001.0,
        max_value=8000.0,
        value=2650.0,
        step=50.0,
    )

    particle_diameter = st.slider(
        "Selected particle diameter (µm)",
        min_value=10,
        max_value=1000,
        value=100,
        step=10,
    )

with col2:
    st.markdown("### Fluid Properties")

    fluid_density = st.number_input(
        "Water density (kg/m³)",
        min_value=900.0,
        max_value=1200.0,
        value=1000.0,
        step=10.0,
    )

    viscosity = st.number_input(
        "Dynamic viscosity (Pa·s)",
        min_value=0.0001,
        max_value=0.01,
        value=0.001,
        format="%.5f",
    )

    gravity = st.number_input(
        "Gravitational acceleration (m/s²)",
        min_value=9.0,
        max_value=10.0,
        value=9.81,
        step=0.01,
    )

if hematite_density <= fluid_density:
    st.error("Hematite density must exceed fluid density.")
    st.stop()

if quartz_density <= fluid_density:
    st.error("Quartz density must exceed fluid density.")
    st.stop()

if particle_diameter <= 0 or viscosity <= 0:
    st.error("Particle diameter and viscosity must be positive.")
    st.stop()


# ==========================================================
# 8. CALCULATE SINGLE-PARTICLE RESULTS
# ==========================================================

diameter_m = particle_diameter * 1e-6

try:
    hematite_result = terminal_velocity_sphere(
        diameter_m=diameter_m,
        particle_density=hematite_density,
        fluid_density=fluid_density,
        viscosity=viscosity,
        gravity=gravity,
    )

    quartz_result = terminal_velocity_sphere(
        diameter_m=diameter_m,
        particle_density=quartz_density,
        fluid_density=fluid_density,
        viscosity=viscosity,
        gravity=gravity,
    )

except (ValueError, ZeroDivisionError, OverflowError) as error:
    st.error(f"Calculation error: {error}")
    st.stop()

hematite_velocity = hematite_result["velocity_m_s"]
quartz_velocity = quartz_result["velocity_m_s"]

hematite_reynolds = hematite_result["reynolds_number"]
quartz_reynolds = quartz_result["reynolds_number"]

settling_ratio = (
    hematite_velocity / quartz_velocity
    if quartz_velocity > 0 else np.nan
)

st.divider()

section_title(
    "Calculated Particle Performance",
    f"Interactive results for particles with a diameter of "
    f"{particle_diameter} µm."
)

c1, c2 = st.columns(2, gap="large")

with c1:
    st.markdown("### Hematite")

    metric_card(
        "TERMINAL SETTLING VELOCITY",
        f"{hematite_velocity:.6g}",
        "m/s",
        accent="amber",
    )

    metric_card(
        "PARTICLE REYNOLDS NUMBER",
        f"{hematite_reynolds:.4g}",
        hematite_result["regime"],
        accent="blue",
    )

with c2:
    st.markdown("### Quartz")

    metric_card(
        "TERMINAL SETTLING VELOCITY",
        f"{quartz_velocity:.6g}",
        "m/s",
        accent="green",
    )

    metric_card(
        "PARTICLE REYNOLDS NUMBER",
        f"{quartz_reynolds:.4g}",
        quartz_result["regime"],
        accent="blue",
    )

comparison_fig = go.Figure()

comparison_fig.add_trace(
    go.Bar(
        x=["Hematite", "Quartz"],
        y=[hematite_velocity, quartz_velocity],
        marker_color=["#E69B45", "#426A85"],
        text=[
            f"{hematite_velocity:.5g}",
            f"{quartz_velocity:.5g}",
        ],
        textposition="outside",
    )
)

comparison_fig.update_layout(
    height=360,
    paper_bgcolor="white",
    plot_bgcolor="white",
    title="Terminal Settling Velocity at Selected Particle Size",
    xaxis_title="Mineral",
    yaxis_title="Terminal velocity (m/s)",
    showlegend=False,
    font=dict(family="Arial", color="#142638"),
)

comparison_fig.update_yaxes(gridcolor="#E8EDF1")

st.plotly_chart(
    comparison_fig,
    use_container_width=True,
)

r1, r2 = st.columns(2)

with r1:
    metric_card(
        "SETTLING VELOCITY RATIO",
        f"{settling_ratio:.2f} : 1",
        "Hematite relative to quartz",
        accent="amber",
    )

with r2:
    metric_card(
        "VELOCITY DIFFERENCE",
        f"{hematite_velocity - quartz_velocity:.6g}",
        "m/s",
        accent="green",
    )

st.caption(
    "This calculator uses the existing Python equipment model. "
    "It represents isolated spherical particles, not the complete "
    "performance of a commercial gravity separator."
)

st.divider()


# ==========================================================
# 9. SETTLING VELOCITY DATASET
# ==========================================================

section_title(
    "Settling Velocity Analysis",
    "Python-generated settling curves for hematite and quartz "
    "under the selected Aspen case conditions."
)

plot_type = st.radio(
    "Velocity model",
    [
        "Isolated particle",
        "Hindered settling estimate",
    ],
    horizontal=True,
)

if plot_type == "Isolated particle":
    h_col = "hematite_isolated_m_s"
    q_col = "quartz_isolated_m_s"
    velocity_label = "Isolated settling velocity (m/s)"
else:
    h_col = "hematite_hindered_estimate_m_s"
    q_col = "quartz_hindered_estimate_m_s"
    velocity_label = "Hindered settling estimate (m/s)"

settling_fig = go.Figure()

settling_fig.add_trace(
    go.Scatter(
        x=case_settling["particle_diameter_mm"] * 1000,
        y=case_settling[h_col],
        mode="lines",
        name="Hematite",
        line=dict(color="#E69B45", width=3),
    )
)

settling_fig.add_trace(
    go.Scatter(
        x=case_settling["particle_diameter_mm"] * 1000,
        y=case_settling[q_col],
        mode="lines",
        name="Quartz",
        line=dict(color="#426A85", width=3),
    )
)

settling_fig.add_vline(
    x=particle_diameter,
    line_dash="dash",
    line_color="#718096",
    annotation_text="Interactive calculator size",
)

settling_fig.update_layout(
    height=430,
    paper_bgcolor="white",
    plot_bgcolor="white",
    title="Settling Velocity vs Particle Diameter",
    xaxis_title="Particle diameter (µm)",
    yaxis_title=velocity_label,
    font=dict(family="Arial", color="#142638"),
    legend=dict(orientation="h", y=1.1),
)

settling_fig.update_xaxes(gridcolor="#E8EDF1")
settling_fig.update_yaxes(gridcolor="#E8EDF1")

st.plotly_chart(
    settling_fig,
    use_container_width=True,
)

volume_fraction = float(
    case_settling["slurry_solids_volume_fraction"].iloc[0]
)

info_card(
    "SLURRY SOLIDS VOLUME FRACTION",
    f"{volume_fraction:.4f} ({volume_fraction * 100:.2f}%) "
    "for the selected case. The hindered-settling curve applies "
    "a Richardson–Zaki type correction to isolated-particle velocity."
)

st.caption(
    "Source: settling_velocity_curves.csv. These are Python "
    "estimates using the stated mineral and fluid properties."
)

st.divider()


# ==========================================================
# 10. PARTICLE REYNOLDS NUMBER ANALYSIS
# ==========================================================

section_title(
    "Particle Reynolds Number Analysis",
    "Examine how particle size influences the settling flow regime."
)

re_fig = go.Figure()

re_fig.add_trace(
    go.Scatter(
        x=case_settling["particle_diameter_mm"] * 1000,
        y=case_settling["hematite_Re"],
        mode="lines",
        name="Hematite",
        line=dict(color="#E69B45", width=3),
    )
)

re_fig.add_trace(
    go.Scatter(
        x=case_settling["particle_diameter_mm"] * 1000,
        y=case_settling["quartz_Re"],
        mode="lines",
        name="Quartz",
        line=dict(color="#426A85", width=3),
    )
)

re_fig.add_hline(
    y=0.2,
    line_dash="dash",
    annotation_text="Approximate creeping-flow reference",
)

re_fig.update_layout(
    height=400,
    paper_bgcolor="white",
    plot_bgcolor="white",
    title="Particle Reynolds Number vs Particle Diameter",
    xaxis_title="Particle diameter (µm)",
    yaxis_title="Particle Reynolds number",
    font=dict(family="Arial", color="#142638"),
)

re_fig.update_xaxes(gridcolor="#E8EDF1")
re_fig.update_yaxes(gridcolor="#E8EDF1")

st.plotly_chart(
    re_fig,
    use_container_width=True,
)

st.caption(
    "Reynolds number is dimensionless. The flow regime affects "
    "the drag relationship used to estimate terminal velocity."
)

st.divider()


# ==========================================================
# 11. GRAVITY SEPARATOR PARTITION ANALYSIS
# ==========================================================

section_title(
    "Gravity Separator: Particle Partition",
    "Explore the idealised Python estimate of how hematite and "
    "quartz particles report to the faster-settling product."
)

st.markdown("""
The partition dataset estimates the percentage of each mineral
reporting to the fast-settling product at different particle sizes.

This is an idealised Python model. It is not a measured partition
curve and is not the Aspen G-SEP component split result.
""")

partition_fig = go.Figure()

partition_fig.add_trace(
    go.Scatter(
        x=case_partition["particle_diameter_mm"],
        y=case_partition["hematite_to_fast_product_pct"],
        mode="lines+markers",
        name="Hematite to fast product",
        line=dict(color="#E69B45", width=3),
    )
)

partition_fig.add_trace(
    go.Scatter(
        x=case_partition["particle_diameter_mm"],
        y=case_partition["quartz_to_fast_product_pct"],
        mode="lines+markers",
        name="Quartz to fast product",
        line=dict(color="#426A85", width=3),
    )
)

partition_fig.update_layout(
    height=430,
    paper_bgcolor="white",
    plot_bgcolor="white",
    title="Idealised Particle Partition vs Particle Diameter",
    xaxis_title="Particle diameter (mm)",
    yaxis_title="Reporting to fast product (%)",
    font=dict(family="Arial", color="#142638"),
    yaxis=dict(range=[0, 105], gridcolor="#E8EDF1"),
    xaxis=dict(gridcolor="#E8EDF1"),
)

st.plotly_chart(
    partition_fig,
    use_container_width=True,
)

partition_table = case_partition[
    [
        "particle_diameter_mm",
        "hematite_hindered_velocity_m_s",
        "quartz_hindered_velocity_m_s",
        "cut_velocity_m_s",
        "hematite_to_fast_product_pct",
        "quartz_to_fast_product_pct",
    ]
].rename(columns={
    "particle_diameter_mm": "Particle size (mm)",
    "hematite_hindered_velocity_m_s": "Hematite hindered velocity (m/s)",
    "quartz_hindered_velocity_m_s": "Quartz hindered velocity (m/s)",
    "cut_velocity_m_s": "Cut velocity (m/s)",
    "hematite_to_fast_product_pct": "Hematite to fast product (%)",
    "quartz_to_fast_product_pct": "Quartz to fast product (%)",
})

with st.expander("View particle partition data"):
    st.dataframe(
        partition_table.round(5),
        use_container_width=True,
        hide_index=True,
    )

st.caption(
    "Source: settling_partition_by_size.csv. The model assumes "
    "the same particle-size distribution for both minerals."
)

st.divider()


# ==========================================================
# 12. IDEALISED GRADE-RECOVERY ANALYSIS
# ==========================================================

section_title(
    "Gravity Separation: Grade–Recovery Trade-off",
    "Investigate how the idealised Python separator cut velocity "
    "changes predicted grade and hematite recovery."
)

st.markdown("""
The idealised model varies cut velocity and estimates the
resulting hematite recovery, silica recovery to concentrate,
and concentrate grade.

The Aspen reference values are displayed separately for comparison.
They are based on the specified G-SEP component split fractions
in the saved Aspen cases.
""")

grade_fig = go.Figure()

grade_fig.add_trace(
    go.Scatter(
        x=case_grade["hematite_recovery_pct"],
        y=case_grade["idealized_concentrate_grade_pct"],
        mode="lines",
        name="Python idealised model",
        line=dict(color="#E69B45", width=3),
        customdata=case_grade["cut_velocity_m_s"],
        hovertemplate=(
            "Hematite recovery: %{x:.2f}%"
            "<br>Idealised grade: %{y:.2f}%"
            "<br>Cut velocity: %{customdata:.5f} m/s"
            "<extra></extra>"
        ),
    )
)

aspen_recovery = float(
    case_grade["aspen_hematite_recovery_pct"].iloc[0]
)

aspen_grade = float(
    case_grade["aspen_concentrate_grade_dry_pct"].iloc[0]
)

grade_fig.add_trace(
    go.Scatter(
        x=[aspen_recovery],
        y=[aspen_grade],
        mode="markers",
        name="Aspen G-SEP result",
        marker=dict(
            color="#426A85",
            size=13,
            symbol="diamond",
            line=dict(color="white", width=1),
        ),
        hovertemplate=(
            "Aspen hematite recovery: %{x:.2f}%"
            "<br>Aspen concentrate grade: %{y:.2f}%"
            "<extra></extra>"
        ),
    )
)

grade_fig.update_layout(
    height=460,
    paper_bgcolor="white",
    plot_bgcolor="white",
    title="Concentrate Grade vs Hematite Recovery",
    xaxis_title="Hematite recovery (%)",
    yaxis_title="Concentrate grade (%)",
    font=dict(family="Arial", color="#142638"),
    legend=dict(orientation="h", y=1.12),
)

grade_fig.update_xaxes(gridcolor="#E8EDF1")
grade_fig.update_yaxes(gridcolor="#E8EDF1")

st.plotly_chart(
    grade_fig,
    use_container_width=True,
)

g1, g2 = st.columns(2)

with g1:
    metric_card(
        "ASPEN HEMATITE RECOVERY",
        f"{aspen_recovery:.2f}%",
        "Fixed G-SEP component split result",
        accent="blue",
    )

with g2:
    metric_card(
        "ASPEN CONCENTRATE GRADE",
        f"{aspen_grade:.2f}%",
        "Dry-solids basis",
        accent="green",
    )

st.warning(
    "The Python idealised grade–recovery curve is not an Aspen "
    "prediction or a validated gravity-separator performance model. "
    "The Aspen point is shown separately and should not be interpreted "
    "as a point generated by the Python curve."
)

st.divider()


# ==========================================================
# 13. BOND CRUSHER ENERGY AND POWER
# ==========================================================

section_title(
    "Crusher Energy and Power Analysis",
    "Explore theoretical crushing energy using the Bond equation "
    "for different assumed work-index values."
)

st.markdown("""
The Bond equation estimates the specific energy required for
comminution from the feed and product characteristic sizes.

The work-index values in this dataset are sensitivity assumptions.
They are not measured properties of the ore.
""")

available_wi = sorted(
    case_bond["Bond_Wi_kWh_per_t"].unique()
)

selected_wi = st.select_slider(
    "Assumed Bond work index (kWh/t)",
    options=available_wi,
    value=available_wi[1] if len(available_wi) > 1 else available_wi[0],
)

selected_bond = case_bond[
    case_bond["Bond_Wi_kWh_per_t"] == selected_wi
].iloc[0]

b1, b2, b3, b4 = st.columns(4)

with b1:
    metric_card(
        "BOND WORK INDEX",
        f"{selected_wi:.1f}",
        "kWh/t",
        accent="amber",
    )

with b2:
    metric_card(
        "SPECIFIC ENERGY",
        f"{selected_bond['specific_energy_kWh_per_t']:.4f}",
        "kWh/t",
        accent="blue",
    )

with b3:
    metric_card(
        "CRUSHER THROUGHPUT",
        f"{selected_bond['crusher_throughput_including_recycle_t_hr']:.3f}",
        "t/h including recycle",
        accent="green",
    )

with b4:
    metric_card(
        "THEORETICAL POWER",
        f"{selected_bond['theoretical_power_kW']:.3f}",
        "kW",
        accent="amber",
    )

bond_fig = go.Figure()

bond_fig.add_trace(
    go.Bar(
        x=case_bond["Bond_Wi_kWh_per_t"],
        y=case_bond["theoretical_power_kW"],
        marker_color="#E69B45",
        text=case_bond["theoretical_power_kW"].map(
            lambda x: f"{x:.3f}"
        ),
        textposition="outside",
    )
)

bond_fig.add_vline(
    x=selected_wi,
    line_dash="dash",
    line_color="#426A85",
    annotation_text="Selected work index",
)

bond_fig.update_layout(
    height=400,
    paper_bgcolor="white",
    plot_bgcolor="white",
    title="Theoretical Crusher Power vs Bond Work Index",
    xaxis_title="Bond work index (kWh/t)",
    yaxis_title="Theoretical power (kW)",
    showlegend=False,
    font=dict(family="Arial", color="#142638"),
)

bond_fig.update_xaxes(gridcolor="#E8EDF1")
bond_fig.update_yaxes(gridcolor="#E8EDF1")

st.plotly_chart(
    bond_fig,
    use_container_width=True,
)

with st.expander("View Bond calculation data"):
    st.dataframe(
        case_bond[
            [
                "Bond_Wi_kWh_per_t",
                "F80_mm",
                "P80_mm",
                "specific_energy_kWh_per_t",
                "crusher_throughput_including_recycle_t_hr",
                "theoretical_power_kW",
            ]
        ].rename(columns={
            "Bond_Wi_kWh_per_t": "Bond work index (kWh/t)",
            "F80_mm": "F80 (mm)",
            "P80_mm": "P80 (mm)",
            "specific_energy_kWh_per_t": "Specific energy (kWh/t)",
            "crusher_throughput_including_recycle_t_hr": "Throughput (t/h)",
            "theoretical_power_kW": "Theoretical power (kW)",
        }).round(5),
        use_container_width=True,
        hide_index=True,
    )

st.caption(
    "Source: bond_crusher_power.csv. Theoretical power is calculated "
    "from Bond specific energy multiplied by crusher throughput."
)

st.divider()


# ==========================================================
# 14. GOVERNING EQUATIONS
# ==========================================================

section_title(
    "Governing Equations",
    "Mathematical relationships used in the engineering calculations."
)

with st.expander("Terminal settling and Reynolds number", expanded=True):

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

    st.markdown("### Bond comminution equation")

    st.latex(
        r"""
        E=10W_i\left(
        \frac{1}{\sqrt{P_{80}}}
        -
        \frac{1}{\sqrt{F_{80}}}
        \right)
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
    | Wi | Bond work index | kWh/t |
    | F80 | Feed size at 80% passing | µm in Bond equation |
    | P80 | Product size at 80% passing | µm in Bond equation |
    | E | Specific comminution energy | kWh/t |
    """)

    st.caption(
        "The Bond equation in the generated dataset uses F80 and P80 "
        "converted from millimetres to micrometres."
    )

st.divider()


# ==========================================================
# 15. INDEPENDENT VERIFICATION USING STOKES' LAW
# ==========================================================

section_title(
    "Independent Verification",
    "Compare the iterative Python model with Stokes' law in "
    "the creeping-flow range."
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
    step=1.0,
)

verification_mineral = st.selectbox(
    "Mineral for verification",
    ["Hematite", "Quartz"],
)

verification_density = (
    hematite_density
    if verification_mineral == "Hematite"
    else quartz_density
)

d_verify = verification_size * 1e-6

try:
    verification_result = terminal_velocity_sphere(
        diameter_m=d_verify,
        particle_density=verification_density,
        fluid_density=fluid_density,
        viscosity=viscosity,
        gravity=gravity,
    )
except (ValueError, ZeroDivisionError, OverflowError) as error:
    st.error(f"Verification calculation error: {error}")
    st.stop()

python_velocity = verification_result["velocity_m_s"]
verification_reynolds = verification_result["reynolds_number"]

stokes_velocity = (
    (verification_density - fluid_density)
    * gravity
    * d_verify ** 2
    / (18 * viscosity)
)

percentage_difference = (
    abs(python_velocity - stokes_velocity)
    / stokes_velocity * 100
    if stokes_velocity > 0 else np.nan
)

v1, v2, v3 = st.columns(3)

with v1:
    metric_card(
        "PYTHON MODEL",
        f"{python_velocity:.6g}",
        "m/s",
        accent="amber",
    )

with v2:
    metric_card(
        "STOKES' LAW",
        f"{stokes_velocity:.6g}",
        "m/s",
        accent="blue",
    )

with v3:
    metric_card(
        "PERCENTAGE DIFFERENCE",
        f"{percentage_difference:.3f}%",
        "Absolute relative difference",
        accent="green",
    )

if verification_reynolds < 0.2:
    st.success(
        f"Reynolds number = {verification_reynolds:.5f}. "
        "This is within the creeping-flow range where Stokes' law "
        "is appropriate for an isolated sphere."
    )
else:
    st.warning(
        f"Reynolds number = {verification_reynolds:.5f}. "
        "Stokes' law is not sufficiently applicable at this condition."
    )

st.latex(
    r"""
    v_{t,\text{Stokes}}=
    \frac{(\rho_p-\rho_f)gd_p^2}{18\mu}
    """
)

st.divider()


# ==========================================================
# 16. ASSUMPTIONS AND LIMITATIONS
# ==========================================================

section_title(
    "Model Assumptions and Limitations",
    "Understand the difference between Aspen results, Python "
    "estimates and engineering assumptions."
)

with st.expander("View engineering assumptions", expanded=False):

    st.markdown("""
    **Aspen simulation results**

    - The process cases are imported from nine Aspen workbooks.
    - G-SEP uses specified component split fractions.
    - Aspen recovery and concentrate grade remain fixed across
      the current cases because those split specifications are
      unchanged.

    **Particle settling model**

    - Particles are spherical.
    - Particles settle individually for the isolated-particle model.
    - The fluid is treated as Newtonian.
    - Steady terminal settling is assumed.
    - Wall effects and particle interactions are neglected.
    - Hindered settling is estimated using a Richardson–Zaki
      type correction.

    **Gravity partition model**

    - It is an idealised Python estimate.
    - The same particle-size distribution is assumed for hematite
      and quartz.
    - The model is not a validated commercial separator model.
    - It does not directly predict real plant recovery.

    **Crusher energy model**

    - Bond work-index values are sensitivity assumptions.
    - They are not measured ore properties.
    - The calculation is a theoretical energy estimate, not a
      motor or equipment vendor power guarantee.

    **General engineering limitations**

    - Actual mineral particles are irregular in shape.
    - Real slurries may have higher solids concentrations.
    - Turbulence and particle interactions can affect settling.
    - Mineral liberation affects the behaviour of composite particles.
    - Actual separator performance depends on equipment geometry
      and operating conditions.
    """)

st.warning(
    "Python settling, partition, grade–recovery and Bond results "
    "are engineering estimates. They must not be presented as "
    "direct Aspen outputs or validated commercial equipment performance."
)


# ==========================================================
# 17. DATASET DOWNLOADS
# ==========================================================

section_title(
    "Engineering Dataset Downloads",
    "Download the generated datasets used in this laboratory."
)

download_items = [
    ("Settling velocity curves", settling_df, "settling_velocity_curves.csv"),
    ("Gravity partition", partition_df, "settling_partition_by_size.csv"),
    ("Idealised grade–recovery", grade_df, "idealized_grade_recovery_curve.csv"),
    ("Bond crusher power", bond_df, "bond_crusher_power.csv"),
]

download_cols = st.columns(2)

for index, (label, df, filename) in enumerate(download_items):
    with download_cols[index % 2]:
        st.download_button(
            label=f"Download {label}",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name=filename,
            mime="text/csv",
            key=f"download_{filename}",
            use_container_width=True,
        )

st.divider()


# ==========================================================
# 18. FOOTER
# ==========================================================

footer()
