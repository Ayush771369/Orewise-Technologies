
import streamlit as st
import pandas as pd
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

load_css()

ROOT = Path(__file__).resolve().parents[1]

CSV_PATH = ROOT / "data" / "aspen_stream_results.csv"

REQUIRED_COLUMNS = [
    "stream_id",
    "description",
    "hematite_kg_hr",
    "quartz_kg_hr",
    "water_kg_hr",
    "total_kg_hr",
]


# ==========================================================
# 2. PAGE HEADER
# ==========================================================

page_header(
    title="Plant Simulator",
    eyebrow="OREWISE | PROCESS ANALYTICS",
    description=(
        "Explore the saved Aspen Plus simulation results, "
        "analyse product composition and examine the material "
        "balance of the preliminary mineral-processing plant."
    ),
)

status_pill("ASPEN PLUS RESULTS", "blue")
status_pill("SAVED OPERATING CASE", "amber")

st.divider()


# ==========================================================
# 3. LOAD AND VALIDATE DATA
# ==========================================================

@st.cache_data
def load_aspen_data(path, modified_time):
    """Load Aspen stream results from CSV."""
    return pd.read_csv(path)


if not CSV_PATH.exists():

    st.error(
        "Aspen data file not found. Please check that "
        "aspen_stream_results.csv exists inside the data folder."
    )

    st.stop()


try:

    df = load_aspen_data(
        str(CSV_PATH),
        CSV_PATH.stat().st_mtime
    )

except Exception as error:

    st.error(f"Unable to load the Aspen dataset: {error}")
    st.stop()


missing_columns = [
    column
    for column in REQUIRED_COLUMNS
    if column not in df.columns
]

if missing_columns:

    st.error(
        "The CSV file is missing required columns: "
        + ", ".join(missing_columns)
    )

    st.stop()


df["stream_id"] = df["stream_id"].astype(str).str.strip()

for column in REQUIRED_COLUMNS[2:]:

    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

if df[REQUIRED_COLUMNS[2:]].isna().any().any():

    st.error(
        "The stream dataset contains missing or non-numeric "
        "component flow values. Please inspect the CSV."
    )

    st.stop()


def get_stream(stream_name):
    """Retrieve a specific Aspen stream."""

    matches = df[df["stream_id"] == stream_name]

    if matches.empty:
        st.error(f"Required Aspen stream not found: {stream_name}")
        st.stop()

    return matches.iloc[0]


# Important external and product streams

feed = get_stream("ORE-FEED")
water = get_stream("WATER")
concentrate = get_stream("CONC")
tailings = get_stream("TAIL")


# ==========================================================
# 4. PERFORMANCE CALCULATIONS
# ==========================================================

feed_hematite = feed["hematite_kg_hr"]
feed_quartz = feed["quartz_kg_hr"]

conc_hematite = concentrate["hematite_kg_hr"]
conc_quartz = concentrate["quartz_kg_hr"]

tail_hematite = tailings["hematite_kg_hr"]
tail_quartz = tailings["quartz_kg_hr"]

# Hematite recovery

if feed_hematite > 0:

    hematite_recovery = (
        conc_hematite / feed_hematite
    ) * 100

else:
    hematite_recovery = 0


# Dry-basis concentrate grade

conc_dry_solids = conc_hematite + conc_quartz

if conc_dry_solids > 0:

    concentrate_grade = (
        conc_hematite / conc_dry_solids
    ) * 100

else:
    concentrate_grade = 0


# Wet-basis hematite fraction

if concentrate["total_kg_hr"] > 0:

    wet_hematite_fraction = (
        conc_hematite / concentrate["total_kg_hr"]
    ) * 100

else:
    wet_hematite_fraction = 0


# Quartz rejection

if feed_quartz > 0:

    quartz_rejection = (
        tail_quartz / feed_quartz
    ) * 100

else:
    quartz_rejection = 0


# ==========================================================
# 5. DASHBOARD KPI CARDS
# ==========================================================

section_title(
    "Plant Performance Overview",
    "Calculated performance indicators from the saved Aspen case."
)

c1, c2, c3, c4 = st.columns(4)

with c1:

    metric_card(
        "HEMATITE RECOVERY",
        f"{hematite_recovery:.1f}%",
        "Hematite collected in concentrate",
        accent="green"
    )

with c2:

    metric_card(
        "CONCENTRATE GRADE",
        f"{concentrate_grade:.2f}%",
        "Hematite on dry-solids basis",
        accent="amber"
    )

with c3:

    metric_card(
        "CONCENTRATE FLOW",
        f"{concentrate['total_kg_hr']:.0f}",
        "kg/h of wet product",
        accent="blue"
    )

with c4:

    metric_card(
        "QUARTZ REJECTION",
        f"{quartz_rejection:.1f}%",
        "Quartz reporting to tailings",
        accent="green"
    )


st.divider()


# ==========================================================
# 6. ADDITIONAL PROCESS INFORMATION
# ==========================================================

section_title(
    "Operating Case Information",
    "Feed and water conditions represented in the saved simulation."
)

a, b, c = st.columns(3)

with a:

    info_card(
        "FRESH ORE FEED",
        f"{feed['total_kg_hr']:,.1f} kg/h entering the process."
    )

with b:

    info_card(
        "WATER ADDITION",
        f"{water['total_kg_hr']:,.1f} kg/h added before separation."
    )

with c:

    info_card(
        "TAILINGS FLOW",
        f"{tailings['total_kg_hr']:,.1f} kg/h leaving the separator."
    )


st.divider()


# ==========================================================
# 7. PRODUCT COMPOSITION CHART
# ==========================================================

section_title(
    "Product Composition Analysis",
    "Comparison of hematite, quartz and water in the final products."
)

product_composition = pd.DataFrame({

    "Stream": [
        "Concentrate",
        "Concentrate",
        "Concentrate",
        "Tailings",
        "Tailings",
        "Tailings",
    ],

    "Component": [
        "Hematite",
        "Quartz",
        "Water",
        "Hematite",
        "Quartz",
        "Water",
    ],

    "Flow (kg/h)": [
        conc_hematite,
        conc_quartz,
        concentrate["water_kg_hr"],
        tail_hematite,
        tail_quartz,
        tailings["water_kg_hr"],
    ]
})


try:

    import plotly.express as px

    fig = px.bar(
        product_composition,
        x="Stream",
        y="Flow (kg/h)",
        color="Component",
        barmode="stack",
        color_discrete_map={
            "Hematite": "#E69B45",
            "Quartz": "#718DA1",
            "Water": "#4C9BB8",
        },
        text_auto=".0f",
    )

    fig.update_layout(
        height=410,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(
            family="Arial",
            color="#142638",
            size=12
        ),
        title=dict(
            text="Component Flow in Final Product Streams",
            x=0.02,
            font=dict(size=16)
        ),
        xaxis_title="Product stream",
        yaxis_title="Mass flow (kg/h)",
        legend_title="Component",
        margin=dict(l=25, r=25, t=65, b=25),
        bargap=0.38,
    )

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(
        gridcolor="#E8EDF1",
        zeroline=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

except ImportError:

    st.bar_chart(
        product_composition,
        x="Stream",
        y="Flow (kg/h)",
        color="Component"
    )


st.caption(
    "The concentrate contains 340 kg/h hematite and "
    "120 kg/h quartz. Tailings contain 60 kg/h hematite "
    "and 480 kg/h quartz."
)


st.divider()


# ==========================================================
# 8. COMPONENT-WISE MATERIAL BALANCE
# ==========================================================

section_title(
    "Material Balance Verification",
    "Comparison of total external component inputs and outputs."
)

balance_data = pd.DataFrame({

    "Component": [
        "Hematite",
        "Quartz",
        "Water",
    ],

    "Input (kg/h)": [
        feed_hematite,
        feed_quartz,
        water["water_kg_hr"],
    ],

    "Output (kg/h)": [
        conc_hematite + tail_hematite,
        conc_quartz + tail_quartz,
        concentrate["water_kg_hr"] + tailings["water_kg_hr"],
    ]
})

balance_data["Difference (kg/h)"] = (
    balance_data["Input (kg/h)"] -
    balance_data["Output (kg/h)"]
)

total_input = balance_data["Input (kg/h)"].sum()

total_output = balance_data["Output (kg/h)"].sum()

mass_difference = total_input - total_output

if total_input > 0:

    balance_error = (
        abs(mass_difference) / total_input
    ) * 100

else:
    balance_error = 0


b1, b2, b3 = st.columns(3)

with b1:

    metric_card(
        "TOTAL INPUT",
        f"{total_input:,.1f}",
        "kg/h",
        accent="blue"
    )

with b2:

    metric_card(
        "TOTAL OUTPUT",
        f"{total_output:,.1f}",
        "kg/h",
        accent="green"
    )

with b3:

    metric_card(
        "MASS BALANCE ERROR",
        f"{balance_error:.3f}%",
        "Absolute difference / total input",
        accent="amber"
    )


st.dataframe(
    balance_data.round(3),
    use_container_width=True,
    hide_index=True
)


if balance_error < 0.01:

    st.success(
        "The external component-wise mass balance closes "
        "within the displayed precision."
    )

else:

    st.warning(
        "The external material balance has a non-zero "
        "difference. Review the stream data."
    )


# Input/output comparison chart

try:

    balance_chart = balance_data.melt(
        id_vars="Component",
        value_vars=[
            "Input (kg/h)",
            "Output (kg/h)"
        ],
        var_name="Balance Type",
        value_name="Flow (kg/h)"
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
        font=dict(
            family="Arial",
            color="#142638"
        ),
        title="External Material Balance by Component",
        margin=dict(l=25, r=25, t=55, b=25),
    )

    balance_fig.update_yaxes(
        gridcolor="#E8EDF1"
    )

    st.plotly_chart(
        balance_fig,
        use_container_width=True
    )

except ImportError:

    st.bar_chart(
        balance_data.set_index("Component")[
            ["Input (kg/h)", "Output (kg/h)"]
        ]
    )


st.caption(
    "Internal recycle streams are not added to the external "
    "input total because they circulate within the process."
)


st.divider()


# ==========================================================
# 9. ASPEN STREAM EXPLORER
# ==========================================================

section_title(
    "Aspen Stream Explorer",
    "Inspect individual streams from the saved Aspen simulation."
)

stream_options = df["stream_id"].drop_duplicates().tolist()

selected_stream = st.selectbox(
    "Select an Aspen stream",
    stream_options,
    index=0
)

stream = df[df["stream_id"] == selected_stream].iloc[0]

st.markdown(f"### {selected_stream}")

st.write(stream["description"])

s1, s2, s3, s4 = st.columns(4)

with s1:

    st.metric(
        "Hematite",
        f"{stream['hematite_kg_hr']:,.2f} kg/h"
    )

with s2:

    st.metric(
        "Quartz",
        f"{stream['quartz_kg_hr']:,.2f} kg/h"
    )

with s3:

    st.metric(
        "Water",
        f"{stream['water_kg_hr']:,.2f} kg/h"
    )

with s4:

    st.metric(
        "Total Flow",
        f"{stream['total_kg_hr']:,.2f} kg/h"
    )


st.divider()


# ==========================================================
# 10. COMPLETE STREAM TABLE
# ==========================================================

section_title(
    "Complete Aspen Dataset",
    "All imported stream component flow rates."
)

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "stream_id": "Stream ID",
        "description": "Description",
        "hematite_kg_hr": st.column_config.NumberColumn(
            "Hematite (kg/h)",
            format="%.2f"
        ),
        "quartz_kg_hr": st.column_config.NumberColumn(
            "Quartz (kg/h)",
            format="%.2f"
        ),
        "water_kg_hr": st.column_config.NumberColumn(
            "Water (kg/h)",
            format="%.2f"
        ),
        "total_kg_hr": st.column_config.NumberColumn(
            "Total (kg/h)",
            format="%.2f"
        )
    }
)


# Download data

csv_download = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Aspen Stream Data (CSV)",
    data=csv_download,
    file_name="orewise_aspen_stream_results.csv",
    mime="text/csv",
    type="primary"
)


st.divider()


# ==========================================================
# 11. MODEL ASSUMPTIONS
# ==========================================================

section_title(
    "Simulation Scope and Model Limitations",
    "Transparency about the saved Aspen model."
)

with st.expander(
    "View simulation assumptions",
    expanded=False
):

    st.markdown("""
    **Model configuration**

    - MIXER
    - CRUSHER
    - SCREEN
    - MIX
    - G-SEP

    **Important assumptions**

    - The feed contains 40 wt% hematite and 60 wt% quartz.
    - The fresh ore feed is 1,000 kg/h.
    - Water addition is 1,200 kg/h.
    - The G-SEP separator uses specified component split fractions.

    **Model limitations**

    - The G-SEP block is a generic separation model.
    - Its output fractions are not calculated from detailed
      particle-settling physics.
    - Only one saved Aspen operating case is currently available.
    - Additional cases are needed for operating-condition trends.
    """)


st.warning(
    "This dashboard displays one saved Aspen case. "
    "It does not yet predict new Aspen outputs when operating "
    "conditions change. Multi-case lookup and interpolation "
    "can be added after additional Aspen runs are exported."
)


# ==========================================================
# 12. FOOTER
# ==========================================================

footer()
