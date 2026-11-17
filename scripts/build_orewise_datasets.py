"""
OREWISE TECHNOLOGIES
Multi-case Aspen and Python Dataset Builder

Reads nine Aspen material-stream Excel exports and produces
clean CSV datasets for the OreWise Streamlit website.

Run from the project root:
    python scripts/build_orewise_datasets.py

Required packages:
    pandas
    numpy
    openpyxl
"""

from pathlib import Path
import math
import re

import numpy as np
import pandas as pd
from openpyxl import load_workbook


# ==========================================================
# 1. PROJECT PATHS AND ENGINEERING INPUTS
# ==========================================================

ROOT = Path(__file__).resolve().parents[1]

RAW_DIR = ROOT / "datas" / "aspen_raw"
OUTPUT_DIR = ROOT / "data"

SCREEN_APERTURE_MM = 1.0

BOND_WI_VALUES = [5, 10, 15, 20, 25]

RHO_HEMATITE = 5250.0
RHO_SILICA = 2650.0
RHO_WATER = 997.0

MU_WATER = 0.00089
GRAVITY = 9.80665

PARTITION_SHARPNESS = 6.0

PSD_STREAMS = [
    "ORE-FEED",
    "MIXED-F",
    "OUTLET",
    "U-F",
    "O-F",
]

REQUIRED_STREAMS = [
    "ORE-FEED",
    "MIXED",
    "MIXED-F",
    "OUTLET",
    "U-F",
    "O-F",
    "CONC",
    "TAIL",
    "WATER",
]


# ==========================================================
# 2. EXCEL READING HELPERS
# ==========================================================

def find_row(ws, label, column=3, start=1):
    """Find a row by its label in Excel column C."""

    for row in range(start, ws.max_row + 1):

        value = ws.cell(row, column).value

        if (
            isinstance(value, str)
            and value.strip().lower() == label.lower()
        ):
            return row

    raise ValueError(
        f"Could not find row labelled {label!r} "
        f"in worksheet {ws.title}."
    )


def get_stream_columns(ws):
    """Map Aspen stream names to their Excel column numbers."""

    header_row = find_row(ws, "Stream Name")

    columns = {}

    for col in range(5, ws.max_column + 1):

        value = ws.cell(header_row, col).value

        if isinstance(value, str) and value.strip():

            columns[value.strip()] = col

    return columns


def get_cell_value(ws, row, column):
    value = ws.cell(row, column).value

    if value is None:
        return 0.0

    return float(value)


def find_mass_flow_rows(ws):
    """Find rows labelled Mass Flows with kg/hr units."""

    result = []

    for row in range(1, ws.max_row + 1):

        label = ws.cell(row, 3).value
        units = ws.cell(row, 4).value

        if (
            isinstance(label, str)
            and label.strip().lower() == "mass flows"
            and isinstance(units, str)
            and units.strip().lower() == "kg/hr"
        ):
            result.append(row)

    return result


def find_component_rows(
    ws,
    start_row,
    end_row,
    components
):
    """
    Find component mass-flow rows between two substream sections.

    Uses the first matching occurrence in the specified section.
    """

    result = {}

    for row in range(start_row, end_row + 1):

        name = ws.cell(row, 3).value
        units = ws.cell(row, 4).value

        if not isinstance(name, str):
            continue

        name = name.strip()

        if (
            name in components
            and isinstance(units, str)
            and units.strip().lower() == "kg/hr"
        ):
            result.setdefault(name, row)

    missing = [
        c for c in components
        if c not in result
    ]

    if missing:
        raise ValueError(
            f"Missing component mass-flow rows: {missing}"
        )

    return result


# ==========================================================
# 3. READ ONE ASPEN WORKBOOK
# ==========================================================

def read_aspen_case(path):
    """
    Read total streams, dry-solids streams and PSD distributions
    from one Aspen Material worksheet.
    """

    match = re.search(
        r"aspen_(\d+)_(\d+)",
        path.stem,
        re.IGNORECASE
    )

    if not match:
        raise ValueError(
            f"Filename must contain feed rate and PSD number: {path.name}"
        )

    feed_rate_label = int(match.group(1))
    psd_id = int(match.group(2))

    workbook = load_workbook(
        path,
        data_only=True,
        read_only=True
    )

    try:

        if "Material" in workbook.sheetnames:
            ws = workbook["Material"]
        else:
            ws = workbook[workbook.sheetnames[0]]

        columns = get_stream_columns(ws)

        missing_streams = [
            s for s in REQUIRED_STREAMS
            if s not in columns
        ]

        if missing_streams:
            raise ValueError(
                f"{path.name}: missing streams {missing_streams}"
            )

        # Locate MIXED and CIPSD substreams.

        mixed_row = find_row(ws, "MIXED Substream")
        cipsd_row = find_row(ws, "CIPSD Substream")

        mass_rows = find_mass_flow_rows(ws)

        wet_mass_rows = [
            r for r in mass_rows
            if mixed_row < r < cipsd_row
        ]

        dry_mass_rows = [
            r for r in mass_rows
            if r > cipsd_row
        ]

        if not wet_mass_rows:
            raise ValueError(
                f"{path.name}: cannot locate MIXED substream mass flows."
            )

        if not dry_mass_rows:
            raise ValueError(
                f"{path.name}: cannot locate CIPSD mass flows."
            )

        # The first mass-flow row after MIXED Substream is
        # the overall stream mass flow, including liquid water.
        wet_mass_row = wet_mass_rows[0]

        # The first mass-flow row after CIPSD Substream is
        # the dry-solids mass flow.
        dry_mass_row = dry_mass_rows[0]

        # Find component rows in their respective sections.

        wet_components = find_component_rows(
            ws,
            wet_mass_row + 1,
            cipsd_row - 1,
            ["HEMAT", "SILIC", "WATER"]
        )

        dry_components = find_component_rows(
            ws,
            dry_mass_row + 1,
            ws.max_row,
            ["HEMAT", "SILIC"]
        )

        # Extract wet total stream flows.

        wet_flows = {
            stream: get_cell_value(
                ws,
                wet_mass_row,
                columns[stream]
            )
            for stream in REQUIRED_STREAMS
        }

        # Extract dry-solids stream flows.

        dry_flows = {
            stream: get_cell_value(
                ws,
                dry_mass_row,
                columns[stream]
            )
            for stream in REQUIRED_STREAMS
        }

        # Extract component flows.

        wet_component_flows = {}

        for component, row in wet_components.items():

            wet_component_flows[component] = {
                stream: get_cell_value(
                    ws,
                    row,
                    columns[stream]
                )
                for stream in REQUIRED_STREAMS
            }

        dry_component_flows = {}

        for component, row in dry_components.items():

            dry_component_flows[component] = {
                stream: get_cell_value(
                    ws,
                    row,
                    columns[stream]
                )
                for stream in REQUIRED_STREAMS
            }

        # Locate PSD table.

        psd_row = find_row(
            ws,
            "PSD",
            start=cipsd_row
        )

        psd_rows = []

        for row in range(psd_row + 1, ws.max_row + 1):

            label = ws.cell(row, 3).value

            if (
                isinstance(label, str)
                and "mm" in label.lower()
            ):
                psd_rows.append(row)

            elif psd_rows:
                break

        if len(psd_rows) < 2:
            raise ValueError(
                f"{path.name}: insufficient PSD rows."
            )

        # Aspen exports bins 0–1, 1–2, ... mm.
        # Use the midpoint of each one-mm bin.

        lower_edges = np.arange(
            len(psd_rows),
            dtype=float
        )

        upper_edges = lower_edges + 1.0

        midpoints = (
            lower_edges + upper_edges
        ) / 2.0

        psd = {}

        for stream in PSD_STREAMS:

            values = np.array([
                get_cell_value(
                    ws,
                    row,
                    columns[stream]
                )
                for row in psd_rows
            ], dtype=float)

            total = values.sum()

            if total <= 0:
                raise ValueError(
                    f"{path.name}: PSD for {stream} is empty."
                )

            # Normalise to mass fractions.

            psd[stream] = values / total

        return {

            "case_id": f"{feed_rate_label}_{psd_id}",

            "feed_rate_label": feed_rate_label,

            "psd_id": psd_id,

            "wet_flows": wet_flows,

            "dry_flows": dry_flows,

            "wet_components": wet_component_flows,

            "dry_components": dry_component_flows,

            "size_lower_mm": lower_edges,

            "size_upper_mm": upper_edges,

            "size_mid_mm": midpoints,

            "psd": psd,

            "source_file": path.name,

        }

    finally:

        workbook.close()


# ==========================================================
# 4. PARTICLE SIZE PERCENTILE
# ==========================================================

def percentile_size(
    mass_fraction,
    lower_edges,
    upper_edges,
    percentile=0.80
):
    """Calculate F80 or P80 using within-bin interpolation."""

    values = np.asarray(
        mass_fraction,
        dtype=float
    )

    total = values.sum()

    if total <= 0:
        return np.nan

    values = values / total

    cumulative = np.cumsum(values)

    index = int(
        np.searchsorted(
            cumulative,
            percentile,
            side="left"
        )
    )

    index = min(index, len(values) - 1)

    previous = (
        cumulative[index - 1]
        if index > 0
        else 0.0
    )

    within_bin = (
        percentile - previous
    ) / max(values[index], 1e-15)

    within_bin = float(
        np.clip(within_bin, 0.0, 1.0)
    )

    return (
        lower_edges[index]
        + within_bin * (
            upper_edges[index] - lower_edges[index]
        )
    )


# ==========================================================
# 5. PARTICLE SETTLING FUNCTIONS
# ==========================================================

def drag_coefficient(reynolds):

    if reynolds <= 0:
        return 0.0

    if reynolds < 1000:

        return (
            24.0 / reynolds
        ) * (
            1.0 + 0.15 * reynolds**0.687
        )

    return 0.44


def terminal_velocity(
    diameter_m,
    particle_density
):
    """Solve the spherical-particle terminal settling force balance."""

    if diameter_m <= 0:
        return 0.0

    delta_rho = particle_density - RHO_WATER

    if delta_rho <= 0:
        return 0.0

    def residual(velocity):

        reynolds = (
            RHO_WATER
            * velocity
            * diameter_m
            / MU_WATER
        )

        cd = drag_coefficient(reynolds)

        weight_buoyancy = (
            math.pi / 6.0
            * diameter_m**3
            * delta_rho
            * GRAVITY
        )

        drag = (
            0.5
            * cd
            * RHO_WATER
            * (math.pi / 4.0)
            * diameter_m**2
            * velocity**2
        )

        return drag - weight_buoyancy

    low = 0.0
    high = 10.0

    # Expand the upper limit if necessary.

    while residual(high) < 0 and high < 100:
        high *= 2.0

    for _ in range(100):

        middle = (low + high) / 2.0

        if residual(middle) > 0:
            high = middle
        else:
            low = middle

    return (low + high) / 2.0


def particle_reynolds(
    velocity,
    diameter_m
):
    return (
        RHO_WATER
        * velocity
        * diameter_m
        / MU_WATER
    )


def richardson_zaki_exponent(reynolds):

    if reynolds < 0.2:
        return 4.65

    if reynolds < 1.0:
        return 4.35

    if reynolds < 500.0:
        return 4.45 * reynolds**(-0.03)

    return 2.39


def hindered_velocity(
    terminal,
    diameter_m,
    solids_volume_fraction
):

    reynolds = particle_reynolds(
        terminal,
        diameter_m
    )

    exponent = richardson_zaki_exponent(
        reynolds
    )

    correction = max(
        0.0,
        1.0 - solids_volume_fraction
    ) ** exponent

    return terminal * correction


def logistic_partition(
    velocity,
    cut_velocity,
    sharpness
):

    velocity = np.maximum(
        np.asarray(velocity, dtype=float),
        1e-15
    )

    return 1.0 / (
        1.0 + (
            cut_velocity / velocity
        ) ** sharpness
    )


# ==========================================================
# 6. SCREEN PERFORMANCE
# ==========================================================

def calculate_screen_performance(
    case,
    aperture_mm
):

    psd = case["psd"]

    lower = case["size_lower_mm"]
    upper = case["size_upper_mm"]

    screen_feed = case["dry_flows"]["OUTLET"]
    under_flow = case["dry_flows"]["U-F"]
    over_flow = case["dry_flows"]["O-F"]

    below_fraction = np.clip(
        (aperture_mm - lower) / (upper - lower),
        0.0,
        1.0
    )

    above_fraction = 1.0 - below_fraction

    feed_fines = (
        screen_feed
        * np.sum(psd["OUTLET"] * below_fraction)
    )

    under_fines = (
        under_flow
        * np.sum(psd["U-F"] * below_fraction)
    )

    feed_coarse = (
        screen_feed
        * np.sum(psd["OUTLET"] * above_fraction)
    )

    over_coarse = (
        over_flow
        * np.sum(psd["O-F"] * above_fraction)
    )

    fines_recovery = (
        under_fines / feed_fines * 100.0
        if feed_fines > 0
        else np.nan
    )

    coarse_recovery = (
        over_coarse / feed_coarse * 100.0
        if feed_coarse > 0
        else np.nan
    )

    correct_placement = (
        (under_fines + over_coarse)
        / screen_feed * 100.0
        if screen_feed > 0
        else np.nan
    )

    return {

        "screen_aperture_mm": aperture_mm,

        "screen_fines_feed_kg_hr": feed_fines,

        "screen_coarse_feed_kg_hr": feed_coarse,

        "fines_recovery_to_undersize_pct": fines_recovery,

        "coarse_recovery_to_oversize_pct": coarse_recovery,

        "correct_placement_efficiency_pct": correct_placement,

        "misplaced_fines_kg_hr": max(
            0.0,
            feed_fines - under_fines
        ),

        "misplaced_coarse_kg_hr": max(
            0.0,
            feed_coarse - over_coarse
        ),

    }


# ==========================================================
# 7. CALCULATE ONE CASE
# ==========================================================

def process_case(case):

    case_id = case["case_id"]

    dry = case["dry_flows"]
    wet = case["wet_flows"]

    wet_components = case["wet_components"]
    dry_components = case["dry_components"]

    psd = case["psd"]

    H_feed = dry_components["HEMAT"]["ORE-FEED"]
    Q_feed = dry_components["SILIC"]["ORE-FEED"]

    H_conc = dry_components["HEMAT"]["CONC"]
    Q_conc = dry_components["SILIC"]["CONC"]

    H_tail = dry_components["HEMAT"]["TAIL"]
    Q_tail = dry_components["SILIC"]["TAIL"]

    water_added = wet_components["WATER"]["WATER"]

    H_conc_water = wet_components["WATER"]["CONC"]
    H_tail_water = wet_components["WATER"]["TAIL"]

    # ---------------- Recovery and grade ----------------

    hematite_recovery = (
        H_conc / H_feed * 100.0
        if H_feed > 0
        else np.nan
    )

    concentrate_dry = dry["CONC"]

    concentrate_grade = (
        H_conc / concentrate_dry * 100.0
        if concentrate_dry > 0
        else np.nan
    )

    silica_recovery = (
        Q_conc / Q_feed * 100.0
        if Q_feed > 0
        else np.nan
    )

    quartz_rejection = (
        Q_tail / Q_feed * 100.0
        if Q_feed > 0
        else np.nan
    )

    # ---------------- External mass balances ----------------

    external_input = (
        wet["ORE-FEED"]
        + wet["WATER"]
    )

    external_output = (
        wet["CONC"]
        + wet["TAIL"]
    )

    total_balance_error = (
        (external_input - external_output)
        / external_input * 100.0
        if external_input > 0
        else np.nan
    )

    dry_balance_error = (
        (
            dry["ORE-FEED"]
            - dry["CONC"]
            - dry["TAIL"]
        )
        / dry["ORE-FEED"] * 100.0
        if dry["ORE-FEED"] > 0
        else np.nan
    )

    # ---------------- Slurry concentration ----------------

    solids_mass = H_feed + Q_feed

    solids_volume = (
        H_feed / RHO_HEMATITE
        + Q_feed / RHO_SILICA
    )

    water_volume = (
        water_added / RHO_WATER
    )

    solids_mass_fraction = (
        solids_mass / (solids_mass + water_added)
        if solids_mass + water_added > 0
        else np.nan
    )

    solids_volume_fraction = (
        solids_volume / (solids_volume + water_volume)
        if solids_volume + water_volume > 0
        else np.nan
    )

    # ---------------- Particle size percentiles ----------------

    F80 = percentile_size(
        psd["MIXED-F"],
        case["size_lower_mm"],
        case["size_upper_mm"]
    )

    P80 = percentile_size(
        psd["OUTLET"],
        case["size_lower_mm"],
        case["size_upper_mm"]
    )

    reduction_ratio = (
        F80 / P80
        if P80 > 0
        else np.nan
    )

    # ---------------- Screen performance ----------------

    screen = calculate_screen_performance(
        case,
        SCREEN_APERTURE_MM
    )

    # ---------------- Case summary ----------------

    summary = {

        "case_id": case_id,

        "source_file": case["source_file"],

        "feed_rate_kg_hr": case["feed_rate_label"],

        "psd_id": case["psd_id"],

        "fresh_feed_kg_hr": dry["ORE-FEED"],

        "crusher_feed_including_recycle_kg_hr": dry["MIXED-F"],

        "crusher_product_screen_feed_kg_hr": dry["OUTLET"],

        "screen_undersize_kg_hr": dry["U-F"],

        "screen_oversize_kg_hr": dry["O-F"],

        "concentrate_solids_kg_hr": dry["CONC"],

        "tailings_solids_kg_hr": dry["TAIL"],

        "concentrate_wet_kg_hr": wet["CONC"],

        "tailings_wet_kg_hr": wet["TAIL"],

        "water_addition_kg_hr": water_added,

        "concentrate_water_kg_hr": H_conc_water,

        "tailings_water_kg_hr": H_tail_water,

        "hematite_feed_kg_hr": H_feed,

        "silica_feed_kg_hr": Q_feed,

        "hematite_concentrate_kg_hr": H_conc,

        "silica_concentrate_kg_hr": Q_conc,

        "hematite_tailings_kg_hr": H_tail,

        "silica_tailings_kg_hr": Q_tail,

        "hematite_recovery_pct": hematite_recovery,

        "concentrate_grade_dry_pct": concentrate_grade,

        "silica_recovery_to_concentrate_pct": silica_recovery,

        "quartz_rejection_pct": quartz_rejection,

        "slurry_solids_mass_fraction_pct": solids_mass_fraction * 100.0,

        "slurry_solids_volume_fraction_pct": solids_volume_fraction * 100.0,

        "F80_mm": F80,

        "P80_mm": P80,

        "crusher_reduction_ratio": reduction_ratio,

        "external_input_kg_hr": external_input,

        "external_output_kg_hr": external_output,

        "external_mass_balance_error_pct": total_balance_error,

        "dry_solids_balance_error_pct": dry_balance_error,

        **screen,

    }

    # ---------------- Stream data ----------------

    streams = []

    for stream in REQUIRED_STREAMS:

        streams.append({

            "case_id": case_id,

            "feed_rate_kg_hr": case["feed_rate_label"],

            "psd_id": case["psd_id"],

            "stream_id": stream,

            "total_wet_flow_kg_hr": wet[stream],

            "dry_solids_flow_kg_hr": dry[stream],

            "hematite_kg_hr": dry_components["HEMAT"][stream],

            "silica_kg_hr": dry_components["SILIC"][stream],

            "water_kg_hr": wet_components["WATER"][stream],

        })

    # ---------------- PSD data ----------------

    psd_rows = []

    for stream in PSD_STREAMS:

        fractions = psd[stream]

        stream_flow = dry[stream]

        for index, fraction in enumerate(fractions):

            psd_rows.append({

                "case_id": case_id,

                "feed_rate_kg_hr": case["feed_rate_label"],

                "psd_id": case["psd_id"],

                "stream_id": stream,

                "bin_lower_mm": case["size_lower_mm"][index],

                "bin_upper_mm": case["size_upper_mm"][index],

                "bin_midpoint_mm": case["size_mid_mm"][index],

                "mass_fraction": fraction,

                "mass_percent": fraction * 100.0,

                "estimated_bin_mass_kg_hr": fraction * stream_flow,

            })

    # ---------------- Bond energy sensitivity ----------------

    bond_rows = []

    F80_um = F80 * 1000.0
    P80_um = P80 * 1000.0

    if F80_um <= P80_um:

        raise ValueError(
            f"{case_id}: F80 must exceed P80 for this Bond calculation."
        )

    crusher_throughput_t_hr = dry["MIXED-F"] / 1000.0

    for Wi in BOND_WI_VALUES:

        specific_energy = 10.0 * Wi * (
            1.0 / math.sqrt(P80_um)
            - 1.0 / math.sqrt(F80_um)
        )

        bond_rows.append({

            "case_id": case_id,

            "feed_rate_kg_hr": case["feed_rate_label"],

            "psd_id": case["psd_id"],

            "Bond_Wi_kWh_per_t": Wi,

            "F80_mm": F80,

            "P80_mm": P80,

            "specific_energy_kWh_per_t": specific_energy,

            "crusher_throughput_including_recycle_t_hr": crusher_throughput_t_hr,

            "theoretical_power_kW": (
                specific_energy * crusher_throughput_t_hr
            ),

        })

    # ---------------- Settling and hindered settling ----------------

    diameter_grid_mm = np.logspace(
        np.log10(0.05),
        np.log10(10.0),
        120
    )

    settling_rows = []

    for diameter_mm in diameter_grid_mm:

        diameter_m = diameter_mm / 1000.0

        vh = terminal_velocity(
            diameter_m,
            RHO_HEMATITE
        )

        vq = terminal_velocity(
            diameter_m,
            RHO_SILICA
        )

        reh = particle_reynolds(vh, diameter_m)
        req = particle_reynolds(vq, diameter_m)

        hindered_h = hindered_velocity(
            vh,
            diameter_m,
            solids_volume_fraction
        )

        hindered_q = hindered_velocity(
            vq,
            diameter_m,
            solids_volume_fraction
        )

        settling_rows.append({

            "case_id": case_id,

            "feed_rate_kg_hr": case["feed_rate_label"],

            "psd_id": case["psd_id"],

            "particle_diameter_mm": diameter_mm,

            "hematite_isolated_m_s": vh,

            "quartz_isolated_m_s": vq,

            "hematite_Re": reh,

            "quartz_Re": req,

            "hematite_hindered_estimate_m_s": hindered_h,

            "quartz_hindered_estimate_m_s": hindered_q,

            "slurry_solids_volume_fraction": solids_volume_fraction,

        })

    # ---------------- Idealised partition by PSD bin ----------------

    active = (
        (psd["U-F"] > 0)
        & (case["size_mid_mm"] > 0)
    )

    diameters_m = (
        case["size_mid_mm"][active] / 1000.0
    )

    weights = psd["U-F"][active].copy()
    weights = weights / weights.sum()

    v_h = np.array([
        terminal_velocity(d, RHO_HEMATITE)
        for d in diameters_m
    ])

    v_q = np.array([
        terminal_velocity(d, RHO_SILICA)
        for d in diameters_m
    ])

    vh_h = np.array([
        hindered_velocity(
            v,
            d,
            solids_volume_fraction
        )
        for v, d in zip(v_h, diameters_m)
    ])

    vh_q = np.array([
        hindered_velocity(
            v,
            d,
            solids_volume_fraction
        )
        for v, d in zip(v_q, diameters_m)
    ])

    median_index = int(
        np.searchsorted(
            np.cumsum(weights),
            0.5
        )
    )

    median_index = min(
        median_index,
        len(weights) - 1
    )

    cut_velocity = math.sqrt(
        vh_h[median_index]
        * vh_q[median_index]
    )

    p_h = logistic_partition(
        vh_h,
        cut_velocity,
        PARTITION_SHARPNESS
    )

    p_q = logistic_partition(
        vh_q,
        cut_velocity,
        PARTITION_SHARPNESS
    )

    partition_rows = []

    for i, d in enumerate(diameters_m):

        partition_rows.append({

            "case_id": case_id,

            "feed_rate_kg_hr": case["feed_rate_label"],

            "psd_id": case["psd_id"],

            "particle_diameter_mm": d * 1000.0,

            "mass_fraction_assumed_for_each_mineral": weights[i],

            "hematite_settling_velocity_m_s": v_h[i],

            "quartz_settling_velocity_m_s": v_q[i],

            "hematite_hindered_velocity_m_s": vh_h[i],

            "quartz_hindered_velocity_m_s": vh_q[i],

            "cut_velocity_m_s": cut_velocity,

            "hematite_to_fast_product_pct": p_h[i] * 100.0,

            "quartz_to_fast_product_pct": p_q[i] * 100.0,

        })

    # ---------------- Idealised grade-recovery sweep ----------------

    all_velocities = np.concatenate([vh_h, vh_q])

    cut_values = np.logspace(
        np.log10(max(all_velocities.min() * 0.5, 1e-12)),
        np.log10(all_velocities.max() * 2.0),
        100
    )

    grade_recovery_rows = []

    for cut in cut_values:

        ph = logistic_partition(
            vh_h,
            cut,
            PARTITION_SHARPNESS
        )

        pq = logistic_partition(
            vh_q,
            cut,
            PARTITION_SHARPNESS
        )

        hematite_recovery_ideal = float(
            np.sum(weights * ph)
        )

        silica_recovery_ideal = float(
            np.sum(weights * pq)
        )

        hematite_in_product = (
            H_feed * hematite_recovery_ideal
        )

        silica_in_product = (
            Q_feed * silica_recovery_ideal
        )

        grade = (
            hematite_in_product
            / (hematite_in_product + silica_in_product)
            * 100.0
            if hematite_in_product + silica_in_product > 0
            else np.nan
        )

        grade_recovery_rows.append({

            "case_id": case_id,

            "feed_rate_kg_hr": case["feed_rate_label"],

            "psd_id": case["psd_id"],

            "cut_velocity_m_s": cut,

            "hematite_recovery_pct": hematite_recovery_ideal * 100.0,

            "silica_recovery_to_concentrate_pct": silica_recovery_ideal * 100.0,

            "idealized_concentrate_grade_pct": grade,

            "aspen_hematite_recovery_pct": hematite_recovery,

            "aspen_concentrate_grade_dry_pct": concentrate_grade,

        })

    return {

        "summary": summary,

        "streams": streams,

        "psd": psd_rows,

        "bond": bond_rows,

        "settling": settling_rows,

        "partition": partition_rows,

        "grade_recovery": grade_recovery_rows,

    }


# ==========================================================
# 8. PROCESS ALL NINE CASES
# ==========================================================

def main():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    if not RAW_DIR.exists():

        raise FileNotFoundError(
            f"Raw Aspen folder not found: {RAW_DIR}"
        )

    files = sorted(
        RAW_DIR.glob("aspen_*.xlsx")
    )

    if not files:

        raise FileNotFoundError(
            f"No aspen_*.xlsx files found in {RAW_DIR}"
        )

    expected_cases = 9

    if len(files) != expected_cases:

        print(
            f"WARNING: Found {len(files)} Aspen workbooks; "
            f"expected {expected_cases}."
        )

    summary_rows = []
    all_streams = []
    all_psd = []
    all_bond = []
    all_settling = []
    all_partition = []
    all_grade_recovery = []

    screen_rows = []

    failed_files = []

    for file_path in files:

        print(f"Processing: {file_path.name}")

        try:

            case = read_aspen_case(file_path)

            result = process_case(case)

            summary_rows.append(result["summary"])

            all_streams.extend(result["streams"])

            all_psd.extend(result["psd"])

            all_bond.extend(result["bond"])

            all_settling.extend(result["settling"])

            all_partition.extend(result["partition"])

            all_grade_recovery.extend(result["grade_recovery"])

            screen_rows.append({

                "case_id": result["summary"]["case_id"],

                "feed_rate_kg_hr": result["summary"]["feed_rate_kg_hr"],

                "psd_id": result["summary"]["psd_id"],

                **{
                    k: result["summary"][k]
                    for k in [
                        "screen_aperture_mm",
                        "screen_fines_feed_kg_hr",
                        "screen_coarse_feed_kg_hr",
                        "fines_recovery_to_undersize_pct",
                        "coarse_recovery_to_oversize_pct",
                        "correct_placement_efficiency_pct",
                        "misplaced_fines_kg_hr",
                        "misplaced_coarse_kg_hr",
                    ]
                }

            })

        except Exception as error:

            failed_files.append(
                (file_path.name, str(error))
            )

            print(
                f"ERROR processing {file_path.name}: {error}"
            )

    if not summary_rows:

        raise RuntimeError(
            "No Aspen cases were processed successfully."
        )

    # ======================================================
    # 9. SAVE CSV OUTPUTS
    # ======================================================

    outputs = {

        "aspen_cases_summary.csv": summary_rows,

        "aspen_streams.csv": all_streams,

        "aspen_psd.csv": all_psd,

        "screen_performance.csv": screen_rows,

        "settling_velocity_curves.csv": all_settling,

        "settling_partition_by_size.csv": all_partition,

        "idealized_grade_recovery_curve.csv": all_grade_recovery,

        "bond_crusher_power.csv": all_bond,

    }

    for filename, rows in outputs.items():

        output_path = OUTPUT_DIR / filename

        pd.DataFrame(rows).to_csv(
            output_path,
            index=False
        )

        print(
            f"Saved: {output_path}"
        )

    # ======================================================
    # 10. SAVE PROCESSING REPORT
    # ======================================================

    summary_df = pd.DataFrame(summary_rows)

    report_lines = [
        "OREWISE TECHNOLOGIES — MULTI-CASE PROCESSING REPORT",
        "=" * 55,
        f"Successfully processed cases: {len(summary_df)}",
        "",
        "ASPEN CASES",
        summary_df[
            [
                "case_id",
                "feed_rate_kg_hr",
                "psd_id",
                "F80_mm",
                "P80_mm",
                "hematite_recovery_pct",
                "concentrate_grade_dry_pct",
                "external_mass_balance_error_pct"
            ]
        ].to_string(index=False),
        "",
        "IMPORTANT MODELLING NOTES",
        "- Aspen stream and separator results are imported from each workbook.",
        "- The G-SEP separator uses specified component split fractions.",
        "- Settling and partition outputs are Python estimates, not Aspen outputs.",
        "- Mineral-specific size distributions are not available; the same PSD is assumed for both minerals.",
        "- Screen aperture is assumed to be 1.0 mm and must be checked against Aspen.",
        "- Bond work index values are sensitivity assumptions, not measured ore properties.",
        "- The idealised grade-recovery curve is not a validated separator model.",
        "",
        "Failed files:",
        str(failed_files),
    ]

    report_path = OUTPUT_DIR / "multi_case_processing_report.txt"

    report_path.write_text(
        "\n".join(report_lines),
        encoding="utf-8"
    )

    print("\n" + "\n".join(report_lines))

    if failed_files:

        raise RuntimeError(
            "Some Aspen workbooks failed. Review "
            "multi_case_processing_report.txt before website integration."
        )

    if len(summary_df) != expected_cases:

        raise RuntimeError(
            f"Expected {expected_cases} cases, "
            f"but processed {len(summary_df)}."
        )

    print("\nSUCCESS: All Aspen cases processed.")
    print("Website CSV datasets are ready.")


if __name__ == "__main__":
    main()