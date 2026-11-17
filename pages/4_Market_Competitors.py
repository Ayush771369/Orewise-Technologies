
import streamlit as st
import pandas as pd

from styles import (
    load_css,
    page_header,
    section_title,
    info_card,
    status_pill,
    footer,
)


# ==========================================================
# 1. PAGE CONFIGURATION
# ==========================================================

load_css()


# ==========================================================
# 2. PAGE HEADER
# ==========================================================

page_header(
    title="Market & Competitors",
    eyebrow="OREWISE | MARKET INTELLIGENCE",
    description=(
        "Understanding the mineral-processing industry, "
        "evaluating existing technology providers and "
        "positioning OreWise within the beneficiation market."
    )
)

status_pill("INDUSTRY RESEARCH", "blue")
status_pill("COMPETITIVE ANALYSIS", "amber")

st.divider()


# ==========================================================
# 3. MARKET INTRODUCTION
# ==========================================================

section_title(
    "Understanding the Market",
    "Why mineral beneficiation creates an engineering opportunity."
)

st.markdown("""
Iron ore extracted from mines contains valuable iron-bearing
minerals together with unwanted gangue materials.

Mineral beneficiation improves the quality of the valuable
mineral product through operations such as crushing, screening,
grinding, classification, gravity separation and magnetic
separation.

Large industrial suppliers already provide advanced mineral-
processing equipment and integrated plant solutions.

OreWise explores a more focused opportunity: a compact,
modular mineral-processing concept aimed at smaller-scale
operators.
""")

st.divider()


# ==========================================================
# 4. MARKET TECHNOLOGY AREAS
# ==========================================================

section_title(
    "Key Industry Technology Areas",
    "The major technology categories represented in our competitor research."
)

col1, col2, col3 = st.columns(3, gap="large")

with col1:

    info_card(
        "COMMINUTION",
        """
        Crushing and grinding reduce ore particle size
        and help prepare material for downstream mineral
        liberation and separation.
        """
    )

with col2:

    info_card(
        "CLASSIFICATION",
        """
        Screening and hydrocyclones separate particles
        according to size and settling behaviour.
        """
    )

with col3:

    info_card(
        "BENEFICIATION",
        """
        Gravity concentration, magnetic separation and
        sensor-based sorting can upgrade mineral products
        by exploiting different material properties.
        """
    )


st.divider()


# ==========================================================
# 5. COMPETITOR DATA
# ==========================================================

competitors = [

    {
        "name": "Metso",
        "category": "Integrated processing solutions",
        "classification": "Direct / industry benchmark",
        "offerings": (
            "Crushing, screening, grinding, magnetic separation, "
            "flotation, filtration, thickening and tailings management."
        ),
        "strength": (
            "Develops integrated mineral-processing circuits "
            "and provides equipment across multiple plant stages."
        ),
        "comparison": (
            "OreWise proposes a simpler, smaller-capacity "
            "processing concept rather than a large integrated "
            "industrial solution."
        ),
        "website": "https://www.metso.com/",
    },

    {
        "name": "Multotec",
        "category": "Mineral beneficiation specialist",
        "classification": "Direct / technology benchmark",
        "offerings": (
            "Spiral concentrators, jigs, screens, cyclones, "
            "magnetic separation and mineral-processing solutions."
        ),
        "strength": (
            "Offers specialised equipment and processing routes "
            "for iron-ore treatment across different particle sizes."
        ),
        "comparison": (
            "OreWise proposes to combine basic size preparation "
            "and gravity-separation principles into a compact "
            "plant concept."
        ),
        "website": "https://www.multotec.com/",
    },

    {
        "name": "Weir Minerals",
        "category": "Mining equipment supplier",
        "classification": "Equipment-level competitor",
        "offerings": (
            "Slurry pumps, hydrocyclones, screening, crushing "
            "and slurry-handling equipment."
        ),
        "strength": (
            "Specialises in equipment for material transport, "
            "comminution and slurry classification."
        ),
        "comparison": (
            "OreWise focuses on an overall small-plant concept "
            "rather than the supply of individual equipment units."
        ),
        "website": "https://www.global.weir/",
    },

    {
        "name": "FLSmidth / FLS",
        "category": "Mining process technology",
        "classification": "Direct / industry benchmark",
        "offerings": (
            "Crushing, grinding, classification, separation, "
            "material handling and mineral-processing technologies."
        ),
        "strength": (
            "Provides technologies and integrated solutions "
            "for mining and mineral-processing operations."
        ),
        "comparison": (
            "OreWise proposes a more focused concept with "
            "moderate processing capacity and a simplified "
            "equipment arrangement."
        ),
        "website": "https://fls.com/en",
    },

    {
        "name": "TOMRA Mining",
        "category": "Sensor-based ore sorting",
        "classification": "Alternative technology",
        "offerings": (
            "Sensor-based ore sorting and pre-concentration "
            "technologies for suitable mineral-processing applications."
        ),
        "strength": (
            "Identifies and separates particles using measured "
            "material properties, potentially rejecting waste "
            "before further processing."
        ),
        "comparison": (
            "OreWise proposes a water-based particle preparation "
            "and gravity-separation route rather than sensor-based "
            "sorting."
        ),
        "website": "https://www.tomra.com/mining",
    },

]


# ==========================================================
# 6. COMPETITOR SHOWCASE
# ==========================================================

section_title(
    "Our Competitor Landscape",
    "Five relevant industrial companies and technology providers."
)

for start in range(0, len(competitors), 2):

    row = competitors[start:start + 2]

    col1, col2 = st.columns(2, gap="large")

    for company, column in zip(row, [col1, col2]):

        with column:

            st.markdown(
                f"### {company['name']}"
            )

            status_pill(
                company["classification"],
                "amber"
            )

            st.caption(company["category"])

            info_card(
                "Technology and Offerings",
                company["offerings"]
            )

            st.markdown("**Key Strength**")

            st.write(company["strength"])

            st.markdown("**Comparison with OreWise**")

            st.write(company["comparison"])

            st.link_button(
                "Visit Official Website",
                company["website"],
                use_container_width=True
            )

            st.markdown("")


st.divider()


# ==========================================================
# 7. COMPETITOR COMPARISON TABLE
# ==========================================================

section_title(
    "Technology Comparison",
    "How existing providers differ in their technological focus."
)

comparison = pd.DataFrame({

    "Company": [
        "Metso",
        "Multotec",
        "Weir Minerals",
        "FLS / FLSmidth",
        "TOMRA Mining"
    ],

    "Main Focus": [
        "Integrated mineral processing",
        "Beneficiation equipment",
        "Mining equipment and slurry systems",
        "Mining process technologies",
        "Sensor-based ore sorting"
    ],

    "Relevant Technologies": [
        "Crushing, grinding, separation",
        "Spirals, screens, jigs, cyclones",
        "Pumps, screens, cyclones",
        "Crushing, grinding, separation",
        "Sensor sorting and pre-concentration"
    ],

    "Relationship to OreWise": [
        "Integrated solution benchmark",
        "Beneficiation technology benchmark",
        "Equipment-level competitor",
        "Integrated solution benchmark",
        "Alternative separation route"
    ]

})

st.dataframe(
    comparison,
    use_container_width=True,
    hide_index=True
)


st.divider()


# ==========================================================
# 8. OREWISE POSITIONING
# ==========================================================

section_title(
    "Where OreWise Fits",
    "Our proposed position in the mineral-processing landscape."
)

st.markdown("""
Most of the companies in our study provide equipment,
specialised technologies or integrated industrial
processing solutions.

OreWise is developing a different initial proposition:
a compact and modular processing concept based on a
specific mineral system and a moderate processing capacity.
""")

col1, col2 = st.columns(2, gap="large")

with col1:

    info_card(
        "EXISTING INDUSTRIAL SOLUTIONS",
        """
        Established suppliers offer extensive equipment
        portfolios, specialised technologies, integrated
        plant engineering and large-scale industrial
        service capabilities.
        """
    )

with col2:

    info_card(
        "PROPOSED OREWISE SOLUTION",
        """
        A focused 1 tonne/hour plant concept for
        hematite–quartz beneficiation, combining crushing,
        screening, water addition and gravity-separation
        principles.
        """
    )


st.divider()


# ==========================================================
# 9. PROPOSED DIFFERENTIATION
# ==========================================================

section_title(
    "Our Proposed Competitive Differentiation",
    "The design objectives that define the OreWise concept."
)

d1, d2 = st.columns(2, gap="large")

with d1:

    info_card(
        "01 | MODULAR PLANT CONCEPT",
        """
        A compact equipment arrangement intended to
        simplify the preliminary plant design and
        process operation.
        """
    )

    info_card(
        "02 | FOCUSED MINERAL SYSTEM",
        """
        A specific hematite–quartz feed composition
        and beneficiation objective provide a clear
        initial engineering design basis.
        """
    )

with d2:

    info_card(
        "03 | PARTICLE-BASED ENGINEERING",
        """
        Python calculations demonstrate the influence
        of particle density and size on settling behaviour.
        """
    )

    info_card(
        "04 | DIGITAL PROCESS DEMONSTRATION",
        """
        A Streamlit website combines process information,
        Aspen stream data and Python calculations
        in one accessible platform.
        """
    )


st.warning(
    "OreWise's lower-cost positioning is a design objective, "
    "not yet a demonstrated economic advantage. A detailed "
    "capital-cost and operating-cost comparison is required "
    "before claiming proven cost competitiveness."
)


st.divider()


# ==========================================================
# 10. TARGET CUSTOMERS
# ==========================================================

section_title(
    "Our Target Customers",
    "The proposed customer group for the OreWise business concept."
)

customers = [

    (
        "Small-scale Mining Operators",
        "Operators looking for a preliminary modular "
        "mineral-beneficiation solution."
    ),

    (
        "Low-grade Iron Ore Processors",
        "Businesses evaluating methods to improve the "
        "hematite content of their product."
    ),

    (
        "Regional Mineral Processing Businesses",
        "Companies interested in smaller-capacity "
        "equipment and simplified plant arrangements."
    ),

]

customer_columns = st.columns(3, gap="large")

for customer, column in zip(
    customers,
    customer_columns
):

    with column:

        info_card(
            customer[0],
            customer[1]
        )


st.divider()


# ==========================================================
# 11. FUTURE DEVELOPMENT
# ==========================================================

section_title(
    "Future Business and Technology Development",
    "How OreWise can evolve beyond the preliminary design."
)

st.markdown("""
Potential future development areas include:

- Experimental validation of gravity-separation performance.
- Detailed separator and equipment sizing.
- Evaluation of mineral liberation requirements.
- Water recovery and recycling.
- Energy and operating-cost optimisation.
- Pilot-scale testing.
- Additional Aspen operating-condition studies.
- Economic comparison against established technologies.
""")


st.divider()


# ==========================================================
# 12. FOOTER
# ==========================================================

footer()
