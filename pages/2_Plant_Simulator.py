
import streamlit as st
import pandas as pd
import plotly.express as px
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

# ==========================================================
# 1. PAGE SETUP
# ==========================================================

st.set_page_config(
    page_title="Plant Simulator | OreWise",
    page_icon="⛏️",
    layout="wide",
)

load_css()

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

SUMMARY_PATH = DATA_DIR / "aspen_cases_summary.csv"
STREAMS_PATH = DATA_DIR / "aspen_streams.csv"
PSD_PATH = DATA_DIR / "aspen_psd.csv"
SCREEN_PATH = DATA_DIR / "screen_performance.csv"


# ==========================================================
# 2. DATA LOADING
# ==========================================================

@st.cache_data
def load_csv(path, modified_time):
    return pd.read_csv(path)


def load_dataset(path):
    if not path.exists():
        st.error(f"Dataset not found: {path.name}")
        st.info(
            "Run scripts/build_orewise_datasets.py first "
            "to generate the Aspen CSV datasets."
        )
        st.stop()

    try:
        return load_csv(str(path), path.stat().st_mtime)
    except Exception as error:
        st.error(f"Could not read {path.name}: {error}")
        st.stop()


summary_df = load_dataset(SUMMARY_PATH)
streams_df = load_dataset(STREAMS_PATH)
psd_df = load_dataset(PSD_PATH)
screen_df = load_dataset(SCREEN_PATH)


# ==========================================================
# 3. VALIDATE DATASETS
# ==========================================================

required_summary = [
    "case_id",
    "feed_rate_kg_hr",
    "psd_id",
    "hematite_recovery_pct",
    "concentrate_grade_dry_pct",
    "concentrate_solids_kg_hr",
    "tailings_solids_kg_hr",
    "F80_mm",
    "P80_mm",
    "external_mass_balance_error_pct",
]

required_streams = [
    "case_id",
    "stream_id",
    "total_wet_flow_kg_hr",
    "dry_solids_flow_kg_hr",
    "hematite_kg_hr",
    "silica_kg_hr",
    "water_kg_hr",
]

required_psd = [
    "case_id",
    "stream_id",
    "bin_midpoint_mm",
    "mass_percent",
]

required_screen = [
    "case_id",
    "screen_aperture_mm",
    "fines_recovery_to_undersize_pct",
    "coarse_recovery_to_oversize_pct",
    "correct_placement_efficiency_pct",
]

def validate_columns(df, required, filename):
    missing = [col for col in required if col not in df.columns]

    if missing:
        st.error(
            f"{filename} is missing these columns: "
            + ", ".join(missing)
        )
        st.stop()


validate_columns(summary_df, required_summary, SUMMARY_PATH.name)
validate_columns(streams_df, required_streams, STREAMS_PATH.name)
validate_columns(psd_df, required_psd, PSD_PATH.name)
validate_columns(screen_df, required_screen, SCREEN_PATH.name)


# ==========================================================
# 4. NORMALISE DATA
# ==========================================================

summary_df["case_id"] = summary_df["case_id"].astype(str)
streams_df["case_id"] = streams_df["case_id"].astype(str)
psd_df["case_id"] = psd_df["case_id"].astype(str)
screen_df["case_id"] = screen_df["case_id"].astype(str)

streams_df["stream_id"] = streams_df["stream_id"].astype(str)
psd_df["stream_id"] = psd_df["stream_id"].astype(str)

numeric_stream_columns = [
    "total_wet_flow_kg_hr",
    "dry_solids_flow_kg_hr",
    "hematite_kg_hr",
    "silica_kg_hr",
    "water_kg_hr",
]

for col in numeric_stream_columns:
    streams_df[col] = pd.to_numeric(
        streams_df[col], errors="coerce"
    )

summary_df["feed_rate_kg_hr"] = pd.to_numeric(
    summary_df["feed_rate_kg_hr"], errors="coerce"
)

summary_df["psd_id"] = pd.to_numeric(
    summary_df["psd_id"], errors="coerce"
)


# ==========================================================
# 5. PAGE HEADER
# ==========================================================

page_header(
    title="Plant Simulator",
    eyebrow="OREWISE | ASPEN PROCESS ANALYTICS",
    description=(
        "Explore nine saved Aspen Plus operating cases, "
        "compare process streams, inspect particle-size "
        "distributions and evaluate material balances."
    ),
)

status_pill("9 ASPEN CASES", "blue")
status_pill("MULTI-CASE DATASET", "green")
status_pill("GRAVITY SEPARATION", "amber")

st.divider()


# ==========================================================
# 6. OPERATING CASE SELECTOR
# ==========================================================

section_title(
    "Select an Operating Case",
    "Choose the fresh feed rate and particle-size distribution "
    "used in the saved Aspen simulation."
)

available_feed_rates = sorted(
    summary_df["feed_rate_kg_hr"].dropna().unique()
)

if not available_feed_rates:
    st.error("No valid feed-rate values were found.")
    st.stop()

col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    selected_feed_rate = st.selectbox(
        "Fresh ore feed (kg/h)",
        available_feed_rates,
        index=(
            available_feed_rates.index(1000)
            if 1000 in available_feed_rates
            else 0
        ),
    )

available_cases = summary_df[
    summary_df["feed_rate_kg_hr"] == selected_feed_rate
].copy()

available_psd_ids = sorted(
    available_cases["psd_id"].dropna().unique()
)

with col2:
    selected_psd = st.selectbox(
        "Particle-size distribution",
        available_psd_ids,
        format_func=lambda x: f"PSD {int(x)}",
    )

selected_rows = summary_df[
    (summary_df["feed_rate_kg_hr"] == selected_feed_rate)
    & (summary_df["psd_id"] == selected_psd)
]

if selected_rows.empty:
    st.error("The selected Aspen case was not found.")
    st.stop()

case = selected_rows.iloc[0]
case_id = str(case["case_id"])

with col3:
    st.markdown(
        f"""
        <div style="
            background:#EDF3F7;
            padding:15px 18px;
            border-radius:10px;
            border-left:4px solid #E69B45;
        ">
            <div style="font-size:12px;color:#63798A;">
                SELECTED ASPEN CASE
            </div>
            <div style="
                font-size:22px;
                font-weight:750;
                color:#142638;
                margin-top:5px;
            ">
                {case_id}
            </div>
            <div style="font-size:13px;color:#63798A;">
                {selected_feed_rate:,.0f} kg/h fresh feed
                &nbsp; | &nbsp; PSD {int(selected_psd)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.caption(
    "These controls select an existing Aspen simulation case. "
    "They do not run Aspen again or predict an un-simulated case."
)

st.divider()


# ==========================================================
# 7. GET SELECTED CASE DATA
# ==========================================================

case_streams = streams_df[
    streams_df["case_id"] == case_id
].copy()

case_psd = psd_df[
    psd_df["case_id"] == case_id
].copy()

case_screen = screen_df[
    screen_df["case_id"] == case_id
].copy()

if case_streams.empty:
    st.error(f"No stream data found for case {case_id}.")
    st.stop()


def get_stream(stream_name):
    matches = case_streams[
        case_streams["stream_id"] == stream_name
    ]

    if matches.empty:
        return None

    return matches.iloc[0]


feed = get_stream("ORE-FEED")
water = get_stream("WATER")
concentrate = get_stream("CONC")
tailings = get_stream("TAIL")

if any(x is None for x in [feed, water, concentrate, tailings]):
    st.error(
        "One or more required external streams are missing "
        "from the selected Aspen case."
    )
    st.stop()


# ==========================================================
# 8. PERFORMANCE METRICS
# ==========================================================

hematite_recovery = float(case["hematite_recovery_pct"])
concentrate_grade = float(case["concentrate_grade_dry_pct"])

concentrate_flow = float(
    concentrate["total_wet_flow_kg_hr"]
)

tailings_flow = float(
    tailings["total_wet_flow_kg_hr"]
)

# Use the selected Aspen case summary as the fresh-feed source.
fresh_feed_flow = float(case["feed_rate_kg_hr"])

# Water addition remains read from the Aspen WATER stream.
water_addition = float(
    water["total_wet_flow_kg_hr"]
)

quartz_feed = float(feed["silica_kg_hr"])
quartz_tailings = float(tailings["silica_kg_hr"])

quartz_rejection = (
    quartz_tailings / quartz_feed * 100
    if quartz_feed > 0 else 0
)


# ==========================================================
# 9. PERFORMANCE DASHBOARD
# ==========================================================

section_title(
    "Plant Performance Overview",
    "Performance indicators extracted from the selected Aspen case."
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    metric_card(
        "HEMATITE RECOVERY",
        f"{hematite_recovery:.1f}%",
        "Hematite reporting to concentrate",
        accent="green",
    )

with c2:
    metric_card(
        "CONCENTRATE GRADE",
        f"{concentrate_grade:.2f}%",
        "Dry-solids hematite content",
        accent="amber",
    )

with c3:
    metric_card(
        "CONCENTRATE FLOW",
        f"{concentrate_flow:,.1f}",
        "kg/h wet product",
        accent="blue",
    )

with c4:
    metric_card(
        "QUARTZ REJECTION",
        f"{quartz_rejection:.1f}%",
        "Quartz reporting to tailings",
        accent="green",
    )

st.divider()


# ==========================================================
# 10. FEED AND PROCESS INFORMATION
# ==========================================================

section_title(
    "Operating Case Information",
    "Feed, water and particle-size characteristics."
)

a, b, c, d = st.columns(4)

with a:
    info_card(
        "FRESH ORE FEED",
        f"{fresh_feed_flow:,.1f} kg/h entering the plant.",
    )

with b:
    info_card(
        "WATER ADDITION",
        f"{water_addition:,.1f} kg/h added to the process.",
    )

with c:
    info_card(
        "FEED F80",
        f"{case['F80_mm']:.3f} mm, 80% passing size.",
    )

with d:
    info_card(
        "PRODUCT P80",
        f"{case['P80_mm']:.3f} mm, 80% passing size.",
    )

st.divider()


# ==========================================================
# 11. PROCESS STREAM COMPOSITION
# ==========================================================

section_title(
    "Product Composition Analysis",
    "Compare hematite, silica and water in the concentrate "
    "and tailings streams."
)

composition = pd.DataFrame({
    "Stream": [
        "Concentrate", "Concentrate", "Concentrate",
        "Tailings", "Tailings", "Tailings",
    ],
    "Component": [
        "Hematite", "Silica", "Water",
        "Hematite", "Silica", "Water",
    ],
    "Flow (kg/h)": [
        concentrate["hematite_kg_hr"],
        concentrate["silica_kg_hr"],
        concentrate["water_kg_hr"],
        tailings["hematite_kg_hr"],
        tailings["silica_kg_hr"],
        tailings["water_kg_hr"],
    ],
})

composition_fig = px.bar(
    composition,
    x="Stream",
    y="Flow (kg/h)",
    color="Component",
    barmode="stack",
    text_auto=".1f",
    color_discrete_map={
        "Hematite": "#E69B45",
        "Silica": "#718DA1",
        "Water": "#4C9BB8",
    },
)

composition_fig.update_layout(
    height=420,
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(family="Arial", color="#142638"),
    margin=dict(l=25, r=25, t=35, b=25),
    legend_title="Component",
)

composition_fig.update_yaxes(
    title="Mass flow (kg/h)",
    gridcolor="#E8EDF1",
)

composition_fig.update_xaxes(
    title="Product stream",
    showgrid=False,
)

st.plotly_chart(
    composition_fig,
    use_container_width=True,
)

st.divider()


# ==========================================================
# 12. MATERIAL BALANCE VERIFICATION
# ==========================================================

section_title(
    "External Material Balance",
    "Compare fresh ore and water inputs against concentrate "
    "and tailings outputs."
)

balance_data = pd.DataFrame({
    "Component": ["Hematite", "Silica", "Water"],
    "Input (kg/h)": [
        feed["hematite_kg_hr"],
        feed["silica_kg_hr"],
        water["water_kg_hr"],
    ],
    "Output (kg/h)": [
        concentrate["hematite_kg_hr"]
        + tailings["hematite_kg_hr"],

        concentrate["silica_kg_hr"]
        + tailings["silica_kg_hr"],

        concentrate["water_kg_hr"]
        + tailings["water_kg_hr"],
    ],
})

balance_data["Difference (kg/h)"] = (
    balance_data["Input (kg/h)"]
    - balance_data["Output (kg/h)"]
)

total_input = balance_data["Input (kg/h)"].sum()
total_output = balance_data["Output (kg/h)"].sum()

balance_error = (
    abs(total_input - total_output) / total_input * 100
    if total_input > 0 else 0
)

b1, b2, b3 = st.columns(3)

with b1:
    metric_card(
        "TOTAL EXTERNAL INPUT",
        f"{total_input:,.2f}",
        "kg/h",
        accent="blue",
    )

with b2:
    metric_card(
        "TOTAL EXTERNAL OUTPUT",
        f"{total_output:,.2f}",
        "kg/h",
        accent="green",
    )

with b3:
    metric_card(
        "BALANCE ERROR",
        f"{balance_error:.6f}%",
        "External mass balance",
        accent="amber",
    )

st.dataframe(
    balance_data.round(5),
    use_container_width=True,
    hide_index=True,
)

if balance_error < 0.01:
    st.success(
        "The external component-wise material balance closes "
        "within the selected tolerance."
    )
else:
    st.warning(
        "The external material balance has a non-zero difference. "
        "Review the selected stream data."
    )

balance_chart = balance_data.melt(
    id_vars="Component",
    value_vars=["Input (kg/h)", "Output (kg/h)"],
    var_name="Balance Type",
    value_name="Flow (kg/h)",
)

balance_fig = px.bar(
    balance_chart,
    x="Component",
    y="Flow (kg/h)",
    color="Balance Type",
    barmode="group",
    color_discrete_map={
        "Input (kg/h)": "#E69B45",
        "Output (kg/h)": "#203B50",
    },
)

balance_fig.update_layout(
    height=350,
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(family="Arial", color="#142638"),
    margin=dict(l=25, r=25, t=35, b=25),
)

balance_fig.update_yaxes(gridcolor="#E8EDF1")

st.plotly_chart(
    balance_fig,
    use_container_width=True,
)

st.caption(
    "Internal recycle streams are excluded from the external "
    "balance because they circulate within the process."
)

st.divider()


# ==========================================================
# 13. PARTICLE-SIZE DISTRIBUTION
# ==========================================================

section_title(
    "Particle-Size Distribution Explorer",
    "Compare the particle-size distributions of the main "
    "crushing and screening streams."
)

if not case_psd.empty:

    psd_options = case_psd["stream_id"].drop_duplicates().tolist()

    preferred_order = [
        "ORE-FEED",
        "MIXED-F",
        "OUTLET",
        "U-F",
        "O-F",
    ]

    ordered_options = [
        x for x in preferred_order if x in psd_options
    ]

    ordered_options += [
        x for x in psd_options if x not in ordered_options
    ]

    selected_psd_streams = st.multiselect(
        "Select streams to compare",
        ordered_options,
        default=[
            x for x in ["MIXED-F", "OUTLET", "U-F"]
            if x in ordered_options
        ],
    )

    psd_plot_data = case_psd[
        case_psd["stream_id"].isin(selected_psd_streams)
    ].copy()

    if not psd_plot_data.empty:

        psd_fig = px.line(
            psd_plot_data,
            x="bin_midpoint_mm",
            y="mass_percent",
            color="stream_id",
            markers=True,
            labels={
                "bin_midpoint_mm": "Particle size (mm)",
                "mass_percent": "Mass fraction in bin (%)",
                "stream_id": "Aspen stream",
            },
        )

        psd_fig.update_layout(
            height=430,
            paper_bgcolor="white",
            plot_bgcolor="white",
            font=dict(family="Arial", color="#142638"),
            margin=dict(l=25, r=25, t=35, b=25),
        )

        psd_fig.update_xaxes(
            gridcolor="#E8EDF1",
            rangemode="tozero",
        )

        psd_fig.update_yaxes(
            gridcolor="#E8EDF1",
            rangemode="tozero",
        )

        st.plotly_chart(
            psd_fig,
            use_container_width=True,
        )

    else:
        st.info("Select at least one stream to display its PSD.")

else:
    st.warning("No PSD records were found for this case.")

st.divider()


# ==========================================================
# 14. SCREEN PERFORMANCE
# ==========================================================

section_title(
    "Screen Performance",
    "Python estimates of particle-size classification performance "
    "using the assumed screen aperture."
)

if not case_screen.empty:

    screen = case_screen.iloc[0]

    s1, s2, s3 = st.columns(3)

    with s1:
        metric_card(
            "FINES RECOVERY",
            f"{screen['fines_recovery_to_undersize_pct']:.2f}%",
            "Fines reporting to undersize",
            accent="green",
        )

    with s2:
        metric_card(
            "COARSE RECOVERY",
            f"{screen['coarse_recovery_to_oversize_pct']:.2f}%",
            "Coarse particles reporting to oversize",
            accent="blue",
        )

    with s3:
        metric_card(
            "CORRECT PLACEMENT",
            f"{screen['correct_placement_efficiency_pct']:.2f}%",
            "Calculated correct particle placement",
            accent="amber",
        )

    st.info(
        f"Screen aperture used in the calculation: "
        f"{screen['screen_aperture_mm']:.2f} mm. "
        "This is a Python estimate and depends on the assumed "
        "aperture and particle-size-bin treatment."
    )

else:
    st.warning("No screen-performance record was found for this case.")

st.divider()


# ==========================================================
# 15. STREAM EXPLORER
# ==========================================================

section_title(
    "Aspen Stream Explorer",
    "Inspect the flow rate and composition of individual "
    "streams in the selected case."
)

stream_options = case_streams["stream_id"].drop_duplicates().tolist()

selected_stream = st.selectbox(
    "Choose an Aspen stream",
    stream_options,
)

stream = get_stream(selected_stream)

st.markdown(f"### {selected_stream}")

st.caption(
    "Stream data imported from the selected Aspen workbook."
)

x1, x2, x3, x4 = st.columns(4)

with x1:
    st.metric(
        "Hematite",
        f"{stream['hematite_kg_hr']:,.2f} kg/h",
    )

with x2:
    st.metric(
        "Silica",
        f"{stream['silica_kg_hr']:,.2f} kg/h",
    )

with x3:
    st.metric(
        "Water",
        f"{stream['water_kg_hr']:,.2f} kg/h",
    )

with x4:
    st.metric(
        "Total wet flow",
        f"{stream['total_wet_flow_kg_hr']:,.2f} kg/h",
    )

st.dataframe(
    case_streams[
        [
            "stream_id",
            "total_wet_flow_kg_hr",
            "dry_solids_flow_kg_hr",
            "hematite_kg_hr",
            "silica_kg_hr",
            "water_kg_hr",
        ]
    ].rename(columns={
        "stream_id": "Stream",
        "total_wet_flow_kg_hr": "Wet flow (kg/h)",
        "dry_solids_flow_kg_hr": "Dry solids (kg/h)",
        "hematite_kg_hr": "Hematite (kg/h)",
        "silica_kg_hr": "Silica (kg/h)",
        "water_kg_hr": "Water (kg/h)",
    }).round(3),
    use_container_width=True,
    hide_index=True,
)

# Download selected case stream data
stream_download = case_streams.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download Selected Case Stream Data",
    data=stream_download,
    file_name=f"orewise_streams_{case_id}.csv",
    mime="text/csv",
)

st.divider()


# ==========================================================
# 16. NINE-CASE COMPARISON
# ==========================================================

section_title(
    "Compare All Aspen Operating Cases",
    "Review how feed rate and feed particle-size distribution "
    "vary across the nine saved simulations."
)

comparison = summary_df[
    [
        "case_id",
        "feed_rate_kg_hr",
        "psd_id",
        "F80_mm",
        "P80_mm",
        "hematite_recovery_pct",
        "concentrate_grade_dry_pct",
        "concentrate_solids_kg_hr",
        "tailings_solids_kg_hr",
    ]
].copy()

comparison = comparison.sort_values(
    ["feed_rate_kg_hr", "psd_id"]
)

st.dataframe(
    comparison.rename(columns={
        "case_id": "Case",
        "feed_rate_kg_hr": "Fresh feed (kg/h)",
        "psd_id": "PSD",
        "F80_mm": "F80 (mm)",
        "P80_mm": "P80 (mm)",
        "hematite_recovery_pct": "Hematite recovery (%)",
        "concentrate_grade_dry_pct": "Concentrate grade (%)",
        "concentrate_solids_kg_hr": "Concentrate solids (kg/h)",
        "tailings_solids_kg_hr": "Tailings solids (kg/h)",
    }).round(3),
    use_container_width=True,
    hide_index=True,
)

comparison_fig = px.scatter(
    summary_df,
    x="F80_mm",
    y="P80_mm",
    color="feed_rate_kg_hr",
    symbol="psd_id",
    hover_name="case_id",
    labels={
        "F80_mm": "Feed F80 (mm)",
        "P80_mm": "Product P80 (mm)",
        "feed_rate_kg_hr": "Fresh feed (kg/h)",
        "psd_id": "PSD case",
    },
)

comparison_fig.update_layout(
    height=390,
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(family="Arial", color="#142638"),
)

comparison_fig.update_xaxes(gridcolor="#E8EDF1")
comparison_fig.update_yaxes(gridcolor="#E8EDF1")

st.plotly_chart(
    comparison_fig,
    use_container_width=True,
)

st.caption(
    "The nine cases show different feed rates and particle-size "
    "distributions. The hematite recovery and concentrate grade "
    "remain constant because the current Aspen G-SEP component "
    "split specifications are unchanged."
)

st.divider()


# ==========================================================
# 17. MODEL ASSUMPTIONS AND LIMITATIONS
# ==========================================================

section_title(
    "Simulation Scope and Model Transparency",
    "Understand what the current Aspen model represents and "
    "what it does not predict."
)

with st.expander(
    "View Aspen configuration and modelling assumptions",
    expanded=False,
):

    st.markdown("""
    **Current Aspen equipment configuration**

    - MIXER
    - CRUSHER
    - SCREEN
    - MIX
    - G-SEP (represented on the website as the gravity separator)

    **Current simulation dataset**

    - Three fresh feed rates: 750, 1,000 and 1,250 kg/h.
    - Three particle-size distribution cases.
    - Nine exported Aspen simulation cases.
    - Hematite and silica component flow rates are extracted
      from the Aspen workbooks.

    **Important separator limitation**

    The G-SEP block uses specified component split fractions.
    It is not a detailed physical model of a spiral concentrator
    or commercial gravity separator.

    **Python modelling assumptions**

    - The screen calculation uses the assumed aperture recorded
      in the generated dataset.
    - The settling model estimates isolated-particle and
      hindered-settling velocities.
    - The idealised partition and grade-recovery calculations
      are estimates, not validated equipment predictions.
    - The Bond work-index values are sensitivity assumptions,
      not measured ore properties.
    """)

st.warning(
    "Changing the feed-rate or PSD selector retrieves a saved "
    "Aspen case. The website does not run Aspen live, and it does "
    "not interpolate or extrapolate unsimulated cases."
)


# ==========================================================
# 18. FOOTER
# ==========================================================

footer()
