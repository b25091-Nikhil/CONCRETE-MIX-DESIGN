import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="IS 10262:2019 Concrete Mix Design Calculator",
    page_icon="🏗️",
    layout="wide"
)


# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

.main-title {
    text-align: center;
    font-size: 30px;
    font-weight: 800;
    margin-bottom: 3px;
}

.sub-title {
    text-align: center;
    font-size: 17px;
    margin-bottom: 4px;
}

.group-title {
    text-align: center;
    font-size: 15px;
    font-weight: 600;
    margin-bottom: 8px;
}

.ratio-box {
    padding: 22px;
    border-radius: 14px;
    background: linear-gradient(135deg, #e8f5e9, #f1f8e9);
    border: 2px solid #2e7d32;
    text-align: center;
    margin-top: 15px;
    margin-bottom: 20px;
}

.ratio-title {
    font-size: 19px;
    font-weight: 700;
    color: #1b5e20;
}

.ratio-value {
    font-size: 32px;
    font-weight: 800;
    color: #2e7d32;
    margin-top: 5px;
}

.info-box {
    padding: 15px;
    border-radius: 10px;
    background: #eef7ff;
    border-left: 5px solid #2196f3;
    margin: 10px 0;
}

.graph-note {
    padding: 15px;
    border-radius: 10px;
    background: #f4f8f4;
    border-left: 5px solid #2e7d32;
    margin-bottom: 12px;
}

.step-box {
    padding: 16px;
    border-radius: 10px;
    background: #f7f7f7;
    border-left: 5px solid #2e7d32;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">IIT MANDI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Civil Engineering Department</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title"><b>Course: Civil Engineering Materials CE203</b></div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="group-title">Group 5 | Nikhil | Neetesh | Nitya | Meet | Mohit | Amar</div>',
    unsafe_allow_html=True
)

st.divider()

st.title("🏗️ IS 10262:2019 Concrete Mix Design Calculator")


# =========================================================
# DATA FROM CE203 MATERIAL
# =========================================================

S_VALUES = {
    "M10": 3.5,
    "M15": 3.5,
    "M20": 4.0,
    "M25": 4.0,
    "M30": 5.0,
    "M35": 5.0,
    "M40": 5.0,
    "M45": 5.0,
    "M50": 5.0,
    "M55": 6.0,
    "M60": 6.0
}

X_VALUES = {
    "M10": 5.0,
    "M15": 5.0,
    "M20": 5.5,
    "M25": 5.5,
    "M30": 6.5,
    "M35": 6.5,
    "M40": 6.5,
    "M45": 6.5,
    "M50": 6.5,
    "M55": 6.5,
    "M60": 6.5
}

WATER_50 = {
    10: 208,
    20: 186,
    40: 165
}

AIR = {
    10: 0.015,
    20: 0.010,
    40: 0.008
}

CA_TABLE = {
    10: {
        "Zone I": 0.48,
        "Zone II": 0.50,
        "Zone III": 0.52,
        "Zone IV": 0.54
    },
    20: {
        "Zone I": 0.60,
        "Zone II": 0.62,
        "Zone III": 0.64,
        "Zone IV": 0.66
    },
    40: {
        "Zone I": 0.69,
        "Zone II": 0.71,
        "Zone III": 0.72,
        "Zone IV": 0.73
    }
}

EXPOSURE = {
    "Mild": {
        "min_cement": 300,
        "max_wc": 0.55,
        "min_grade": 20
    },
    "Moderate": {
        "min_cement": 300,
        "max_wc": 0.50,
        "min_grade": 25
    },
    "Severe": {
        "min_cement": 320,
        "max_wc": 0.45,
        "min_grade": 30
    },
    "Very Severe": {
        "min_cement": 340,
        "max_wc": 0.45,
        "min_grade": 35
    },
    "Extreme": {
        "min_cement": 360,
        "max_wc": 0.40,
        "min_grade": 40
    }
}

CEMENT_ADJUSTMENT = {
    10: 40,
    20: 0,
    40: -30
}


# =========================================================
# SIDEBAR INPUTS
# =========================================================

st.sidebar.header("⚙️ Design Inputs")

grade = st.sidebar.selectbox(
    "Concrete Grade",
    list(S_VALUES.keys()),
    index=list(S_VALUES.keys()).index("M30")
)

fck = int(grade.replace("M", ""))

max_agg = st.sidebar.selectbox(
    "Maximum Aggregate Size (mm)",
    [10, 20, 40],
    index=1
)

zone = st.sidebar.selectbox(
    "Fine Aggregate Zone",
    ["Zone I", "Zone II", "Zone III", "Zone IV"],
    index=1
)

slump = st.sidebar.number_input(
    "Required Slump (mm)",
    min_value=25,
    max_value=200,
    value=100,
    step=25
)

preliminary_wc = st.sidebar.number_input(
    "Preliminary Water-Cement Ratio",
    min_value=0.25,
    max_value=0.70,
    value=0.45,
    step=0.01,
    format="%.2f"
)

exposure = st.sidebar.selectbox(
    "Exposure Condition",
    list(EXPOSURE.keys()),
    index=0
)


# =========================================================
# SPECIFIC GRAVITY
# =========================================================

st.sidebar.subheader("Specific Gravity")

sg_cement = st.sidebar.number_input(
    "Cement SG",
    min_value=2.50,
    max_value=3.50,
    value=3.15,
    step=0.01
)

sg_fa = st.sidebar.number_input(
    "Fine Aggregate SG",
    min_value=2.40,
    max_value=3.00,
    value=2.65,
    step=0.01
)

sg_ca = st.sidebar.number_input(
    "Coarse Aggregate SG",
    min_value=2.40,
    max_value=3.00,
    value=2.70,
    step=0.01
)


# =========================================================
# SUPERPLASTICIZER
# =========================================================

st.sidebar.subheader("Superplasticizer")

use_sp = st.sidebar.checkbox(
    "Use Superplasticizer"
)

if use_sp:

    sp_dosage = st.sidebar.number_input(
        "SP Dosage (% of cement)",
        min_value=0.1,
        max_value=3.0,
        value=1.0,
        step=0.1
    )

    water_reduction = st.sidebar.number_input(
        "Water Reduction (%)",
        min_value=0.0,
        max_value=50.0,
        value=20.0,
        step=1.0
    )

    sg_sp = st.sidebar.number_input(
        "SP Specific Gravity",
        min_value=0.90,
        max_value=1.50,
        value=1.10,
        step=0.01
    )

else:

    sp_dosage = 0.0
    water_reduction = 0.0
    sg_sp = 1.10


# =========================================================
# CALCULATIONS
# =========================================================

S = S_VALUES[grade]
X = X_VALUES[grade]

target_1 = fck + (1.65 * S)
target_2 = fck + X

target_strength = max(
    target_1,
    target_2
)


# =========================================================
# DURABILITY
# =========================================================

durability = EXPOSURE[exposure]

min_grade = durability["min_grade"]
max_wc_durability = durability["max_wc"]
min_cement_base = durability["min_cement"]

min_cement = (
    min_cement_base
    + CEMENT_ADJUSTMENT[max_agg]
)


# =========================================================
# ADOPTED W/C
# =========================================================

adopted_wc = min(
    preliminary_wc,
    max_wc_durability
)


# =========================================================
# WATER
# =========================================================

base_water = WATER_50[max_agg]

if slump > 50:

    water_before_sp = base_water * (
        1 + (
            0.03 *
            ((slump - 50) / 25)
        )
    )

else:

    water_before_sp = base_water


water_reduction_amount = (
    water_before_sp *
    water_reduction /
    100
)

water = (
    water_before_sp -
    water_reduction_amount
)


# =========================================================
# CEMENT
# =========================================================

cement_from_wc = (
    water /
    adopted_wc
)

cement = max(
    cement_from_wc,
    min_cement
)

actual_wc = (
    water /
    cement
)


# =========================================================
# SUPERPLASTICIZER
# =========================================================

sp_mass = (
    cement *
    sp_dosage /
    100
)


# =========================================================
# COARSE AGGREGATE FRACTION
# =========================================================

base_ca_fraction = CA_TABLE[
    max_agg
][zone]

wc_correction = (
    (0.50 - actual_wc)
    / 0.05
) * 0.01

ca_fraction = (
    base_ca_fraction +
    wc_correction
)

ca_fraction = max(
    0.40,
    min(ca_fraction, 0.85)
)

fa_fraction = (
    1 - ca_fraction
)


# =========================================================
# ABSOLUTE VOLUME
# =========================================================

cement_volume = (
    cement /
    (sg_cement * 1000)
)

water_volume = (
    water / 1000
)

sp_volume = (
    sp_mass /
    (sg_sp * 1000)
)

air_volume = AIR[max_agg]

aggregate_volume = (
    1
    - cement_volume
    - water_volume
    - sp_volume
    - air_volume
)

ca_volume = (
    aggregate_volume *
    ca_fraction
)

fa_volume = (
    aggregate_volume *
    fa_fraction
)

ca_mass = (
    ca_volume *
    sg_ca *
    1000
)

fa_mass = (
    fa_volume *
    sg_fa *
    1000
)


# =========================================================
# MIX RATIO
# =========================================================

fa_ratio = fa_mass / cement
ca_ratio = ca_mass / cement


# =========================================================
# STRENGTH CURVES FOR GRAPH
# =========================================================

CURVE_X = np.array([
    0.25,
    0.30,
    0.35,
    0.40,
    0.45,
    0.50,
    0.55,
    0.60,
    0.65
])

CURVE_1 = np.array([
    60.0,
    51.0,
    43.0,
    36.5,
    30.0,
    25.0,
    21.0,
    17.5,
    15.0
])

CURVE_2 = np.array([
    66.0,
    57.0,
    49.0,
    42.0,
    36.0,
    30.0,
    26.0,
    22.0,
    19.0
])

CURVE_3 = np.array([
    74.0,
    65.0,
    57.0,
    50.0,
    43.0,
    37.5,
    32.0,
    27.0,
    23.0
])


# Select teaching curve based on target strength

if target_strength <= 33:

    selected_curve = CURVE_1
    selected_curve_name = "Curve 1 — 33 MPa and below"

elif target_strength < 53:

    selected_curve = CURVE_2
    selected_curve_name = "Curve 2 — 43 MPa to below 53 MPa"

else:

    selected_curve = CURVE_3
    selected_curve_name = "Curve 3 — 53 MPa and above"


# Approximate W/C read from graph

if (
    target_strength >= selected_curve.min()
    and target_strength <= selected_curve.max()
):

    graph_wc = np.interp(
        target_strength,
        selected_curve[::-1],
        CURVE_X[::-1]
    )

else:

    graph_wc = None


# =========================================================
# VALIDATION
# =========================================================

checks = []

checks.append(
    (
        "Water-Cement Ratio",
        actual_wc <= max_wc_durability + 1e-9
    )
)

checks.append(
    (
        "Minimum Cement Content",
        cement >= min_cement - 1e-9
    )
)

checks.append(
    (
        "Maximum Cement Content",
        cement <= 450 + 1e-9
    )
)

checks.append(
    (
        "Minimum Grade for Exposure",
        fck >= min_grade
    )
)

checks.append(
    (
        "Coarse Aggregate Fraction",
        0.40 <= ca_fraction <= 0.85
    )
)

checks.append(
    (
        "Positive Aggregate Volume",
        aggregate_volume > 0
    )
)

design_valid = all(
    result
    for _, result in checks
)


# =========================================================
# DESIGN SUMMARY
# =========================================================

st.subheader("📌 Design Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Grade",
        grade
    )

with col2:

    st.metric(
        "Target Mean Strength",
        f"{target_strength:.2f} MPa"
    )

with col3:

    st.metric(
        "Adopted W/C",
        f"{actual_wc:.3f}"
    )

with col4:

    st.metric(
        "Cement",
        f"{cement:.1f} kg/m³"
    )


# =========================================================
# DESIGN STATUS
# =========================================================

if design_valid:

    st.success(
        "✅ Mix design satisfies the programmed design checks."
    )

else:

    st.error(
        "❌ The calculated design requires revision. "
        "Check the failed conditions below."
    )


# =========================================================
# FINAL MIX
# =========================================================

st.subheader("🏗️ Final Mix Proportions")

final_data = pd.DataFrame({

    "Material": [
        "Cement",
        "Water",
        "Fine Aggregate",
        "Coarse Aggregate",
        "Superplasticizer"
    ],

    "Quantity (kg/m³)": [
        cement,
        water,
        fa_mass,
        ca_mass,
        sp_mass
    ]
})

st.dataframe(
    final_data.style.format({
        "Quantity (kg/m³)": "{:.2f}"
    }),
    use_container_width=True,
    hide_index=True
)


# =========================================================
# MIX RATIO
# =========================================================

st.markdown(
    f"""
    <div class="ratio-box">

    <div class="ratio-title">
    Cement : Fine Aggregate : Coarse Aggregate
    </div>

    <div class="ratio-value">
    1 : {fa_ratio:.2f} : {ca_ratio:.2f}
    </div>

    </div>
    """,
    unsafe_allow_html=True
)

st.write(
    f"Water-Cement Ratio = **{actual_wc:.3f}**"
)


# =========================================================
# GRAPHS
# =========================================================

st.subheader("📈 CE203 Mix Design Graphs")

tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Strength vs W/C",
    "💧 Water vs Slump",
    "🪨 CA Correction",
    "🧱 Absolute Volume"
])


# =========================================================
# GRAPH 1
# STRENGTH VS W/C
# =========================================================

with tab1:

    st.markdown(
        """
        <div class="graph-note">

        <b>How to read the graph</b><br><br>

        1. Calculate the target mean strength.<br>
        2. Select the appropriate strength curve.<br>
        3. Move horizontally from target strength to the curve.<br>
        4. Move vertically downward to obtain the approximate W/C ratio.<br><br>

        <b>Green curve = selected teaching curve</b><br>
        <b>Green point = target mean strength</b>

        </div>
        """,
        unsafe_allow_html=True
    )

    fig1 = go.Figure()

    # Curve 1

    fig1.add_trace(
        go.Scatter(
            x=CURVE_X,
            y=CURVE_1,
            mode="lines",
            name="Curve 1",
            line=dict(width=3)
        )
    )

    # Curve 2

    fig1.add_trace(
        go.Scatter(
            x=CURVE_X,
            y=CURVE_2,
            mode="lines",
            name="Curve 2",
            line=dict(width=3)
        )
    )

    # Curve 3

    fig1.add_trace(
        go.Scatter(
            x=CURVE_X,
            y=CURVE_3,
            mode="lines",
            name="Curve 3",
            line=dict(width=3)
        )
    )

    # Selected curve

    fig1.add_trace(
        go.Scatter(
            x=CURVE_X,
            y=selected_curve,
            mode="lines",
            name="Selected Curve",
            line=dict(
                color="green",
                width=6
            )
        )
    )

    if graph_wc is not None:

        # Target point

        fig1.add_trace(
            go.Scatter(
                x=[graph_wc],
                y=[target_strength],
                mode="markers",
                name="Target Point",
                marker=dict(
                    color="green",
                    size=14,
                    line=dict(
                        color="white",
                        width=2
                    )
                )
            )
        )

        # Horizontal guide

        fig1.add_hline(
            y=target_strength,
            line_color="green",
            line_dash="dash",
            line_width=2
        )

        # Vertical guide

        fig1.add_vline(
            x=graph_wc,
            line_color="green",
            line_dash="dash",
            line_width=2
        )

    # Preliminary W/C point

    fig1.add_trace(
        go.Scatter(
            x=[preliminary_wc],
            y=[
                np.interp(
                    preliminary_wc,
                    CURVE_X,
                    selected_curve
                )
            ],
            mode="markers",
            name="Preliminary W/C",
            marker=dict(
                size=10,
                symbol="diamond"
            )
        )
    )

    fig1.update_layout(
        title="28-Day Compressive Strength vs Free W/C Ratio",
        xaxis_title="Free Water-Cement Ratio",
        yaxis_title="28-Day Compressive Strength (MPa)",
        height=520,
        hovermode="closest",
        margin=dict(
            l=60,
            r=30,
            t=70,
            b=60
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        )
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    if graph_wc is not None:

        st.success(
            f"Target mean strength = {target_strength:.2f} MPa | "
            f"Approximate graph W/C = {graph_wc:.3f} | "
            f"Your preliminary W/C = {preliminary_wc:.3f}"
        )

    else:

        st.info(
            "The target strength lies outside the displayed range "
            "of the selected teaching curve."
        )


# =========================================================
# GRAPH 2
# WATER VS SLUMP
# =========================================================

with tab2:

    st.markdown(
        """
        <div class="graph-note">

        <b>CE203 Lecture relationship</b><br><br>

        At 50 mm slump:<br>
        • 10 mm aggregate → 208 kg/m³<br>
        • 20 mm aggregate → 186 kg/m³<br>
        • 40 mm aggregate → 165 kg/m³<br><br>

        For every <b>25 mm increase above 50 mm slump</b>,
        water increases by approximately <b>3%</b>.

        </div>
        """,
        unsafe_allow_html=True
    )

    slump_values = np.arange(
        25,
        201,
        5
    )

    fig2 = go.Figure()

    for size in [10, 20, 40]:

        water_values = []

        for s in slump_values:

            base = WATER_50[size]

            if s > 50:

                value = base * (
                    1 +
                    0.03 *
                    ((s - 50) / 25)
                )

            else:

                value = base

            water_values.append(value)

        if size == max_agg:

            line_color = "green"
            line_width = 6

        else:

            line_color = None
            line_width = 3

        fig2.add_trace(
            go.Scatter(
                x=slump_values,
                y=water_values,
                mode="lines",
                name=f"{size} mm aggregate",
                line=dict(
                    color=line_color,
                    width=line_width
                )
            )

    # Current point

    fig2.add_trace(
        go.Scatter(
            x=[slump],
            y=[water_before_sp],
            mode="markers",
            name="Your input",
            marker=dict(
                color="green",
                size=14,
                line=dict(
                    color="white",
                    width=2
                )
            )
        )
    )

    fig2.add_vline(
        x=slump,
        line_color="green",
        line_dash="dash"
    )

    fig2.add_hline(
        y=water_before_sp,
        line_color="green",
        line_dash="dash"
    )

    fig2.update_layout(
        title="Reference Water Content vs Slump",
        xaxis_title="Slump (mm)",
        yaxis_title="Water Content (kg/m³)",
        height=500,
        margin=dict(
            l=60,
            r=30,
            t=70,
            b=60
        )
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.success(
        f"Your input: {max_agg} mm aggregate | "
        f"{slump} mm slump | "
        f"Water before SP = {water_before_sp:.2f} kg/m³"
    )


# =========================================================
# GRAPH 3
# COARSE AGGREGATE CORRECTION
# =========================================================

with tab3:

    st.markdown(
        """
        <div class="graph-note">

        <b>Coarse Aggregate Correction</b><br><br>

        Reference W/C = <b>0.50</b>.<br><br>

        For every <b>0.05 decrease in W/C</b>,
        the coarse aggregate fraction increases by
        <b>0.01</b>.

        <br><br>

        Example:<br>
        W/C = 0.50 → CA fraction = reference value<br>
        W/C = 0.45 → CA fraction increases by 0.01<br>
        W/C = 0.40 → CA fraction increases by 0.02

        </div>
        """,
        unsafe_allow_html=True
    )

    wc_values = np.arange(
        0.30,
        0.651,
        0.005
    )

    ca_values = []

    for wc in wc_values:

        correction_value = (
            (0.50 - wc) /
            0.05
        ) * 0.01

        value = (
            base_ca_fraction +
            correction_value
        )

        ca_values.append(value)

    fig3 = go.Figure()

    fig3.add_trace(
        go.Scatter(
            x=wc_values,
            y=ca_values,
            mode="lines",
            name="CA fraction",
            line=dict(
                width=5
            )
        )
    )

    # Reference point

    fig3.add_trace(
        go.Scatter(
            x=[0.50],
            y=[base_ca_fraction],
            mode="markers",
            name="Reference (0.50)",
            marker=dict(
                size=11,
                symbol="circle"
            )
        )
    )

    # Current mix

    fig3.add_trace(
        go.Scatter(
            x=[actual_wc],
            y=[ca_fraction],
            mode="markers",
            name="Your Mix",
            marker=dict(
                color="green",
                size=15,
                line=dict(
                    color="white",
                    width=2
                )
            )
        )
    )

    fig3.add_vline(
        x=actual_wc,
        line_color="green",
        line_dash="dash"
    )

    fig3.add_hline(
        y=ca_fraction,
        line_color="green",
        line_dash="dash"
    )

    fig3.update_layout(
        title="Coarse Aggregate Fraction vs Water-Cement Ratio",
        xaxis_title="Water-Cement Ratio",
        yaxis_title="Coarse Aggregate Fraction",
        height=500,
        margin=dict(
            l=60,
            r=30,
            t=70,
            b=60
        )
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    st.success(
        f"Reference CA fraction = {base_ca_fraction:.3f} | "
        f"Correction = {wc_correction:+.3f} | "
        f"Final CA fraction = {ca_fraction:.3f} | "
        f"FA fraction = {fa_fraction:.3f}"
    )


# =========================================================
# GRAPH 4
# ABSOLUTE VOLUME
# =========================================================

with tab4:

    st.markdown(
        """
        <div class="graph-note">

        <b>Absolute Volume Method</b><br><br>

        For 1 m³ of concrete:

        <br><br>

        Cement volume + Water volume + Aggregate volume
        + Admixture volume + Air volume = 1 m³

        </div>
        """,
        unsafe_allow_html=True
    )

    volume_names = [
        "Cement",
        "Water",
        "Fine Aggregate",
        "Coarse Aggregate",
        "SP",
        "Air"
    ]

    volume_values = [
        cement_volume,
        water_volume,
        fa_volume,
        ca_volume,
        sp_volume,
        air_volume
    ]

    fig4 = go.Figure()

    fig4.add_trace(
        go.Bar(
            x=volume_names,
            y=volume_values,
            text=[
                f"{v:.4f}"
                for v in volume_values
            ],
            textposition="outside"
        )
    )

    fig4.update_layout(
        title="Volume Distribution in 1 m³ Concrete",
        xaxis_title="Material",
        yaxis_title="Volume (m³)",
        yaxis=dict(
            range=[
                0,
                max(volume_values) * 1.25
            ]
        ),
        height=500,
        margin=dict(
            l=60,
            r=30,
            t=70,
            b=60
        )
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

    st.success(
        f"Total calculated volume = "
        f"{cement_volume + water_volume + fa_volume + "
        f"ca_volume + sp_volume + air_volume:.4f} m³"
    )


# =========================================================
# CALCULATION STEPS
# =========================================================

st.subheader("🧮 Detailed Calculation Steps")


# ---------------------------------------------------------
# STEP 1
# ---------------------------------------------------------

with st.expander(
    "1. Target Mean Strength",
    expanded=True
):

    st.markdown(
        f"""
        <div class="step-box">

        <b>Concrete Grade:</b> {grade}<br>
        <b>fck:</b> {fck:.2f} MPa<br>
        <b>Standard deviation, S:</b> {S:.2f} MPa<br>
        <b>X:</b> {X:.2f} MPa

        <br><br>

        <b>Condition 1:</b><br>
        fck + 1.65S<br>
        = {fck:.2f} + 1.65 × {S:.2f}<br>
        = <b>{target_1:.2f} MPa</b>

        <br><br>

        <b>Condition 2:</b><br>
        fck + X<br>
        = {fck:.2f} + {X:.2f}<br>
        = <b>{target_2:.2f} MPa</b>

        <br><br>

        <b>Target Mean Strength</b><br>
        max({target_1:.2f}, {target_2:.2f})
        = <b>{target_strength:.2f} MPa</b>

        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------------------------------------------------
# STEP 2
# ---------------------------------------------------------

with st.expander("2. Durability Requirements"):

    st.write(
        f"Exposure condition = **{exposure}**"
    )

    st.write(
        f"Maximum W/C ratio = **{max_wc_durability:.2f}**"
    )

    st.write(
        f"Minimum cement content = "
        f"**{min_cement_base:.0f} kg/m³**"
    )

    st.write(
        f"Aggregate-size correction = "
        f"**{CEMENT_ADJUSTMENT[max_agg]:+.0f} kg/m³**"
    )

    st.write(
        f"Minimum cement after correction = "
        f"**{min_cement:.0f} kg/m³**"
    )


# ---------------------------------------------------------
# STEP 3
# ---------------------------------------------------------

with st.expander("3. Adopted Water-Cement Ratio"):

    st.write(
        f"Preliminary W/C ratio = "
        f"**{preliminary_wc:.3f}**"
    )

    st.write(
        f"Durability maximum W/C = "
        f"**{max_wc_durability:.3f}**"
    )

    st.write(
        f"Adopted W/C = min("
        f"{preliminary_wc:.3f}, "
        f"{max_wc_durability:.3f}) "
        f"= **{adopted_wc:.3f}**"
    )

    if graph_wc is not None:

        st.info(
            f"Approximate W/C read from strength graph = "
            f"**{graph_wc:.3f}**"
        )


# ---------------------------------------------------------
# STEP 4
# ---------------------------------------------------------

with st.expander("4. Water Calculation"):

    st.write(
        f"Base water for {max_agg} mm aggregate "
        f"at 50 mm slump = "
        f"**{base_water:.0f} kg/m³**"
    )

    if slump > 50:

        increase_percent = (
            3 *
            ((slump - 50) / 25)
        )

        st.write(
            f"Water increase = "
            f"**{increase_percent:.1f}%**"
        )

    st.write(
        f"Water before SP = "
        f"**{water_before_sp:.2f} kg/m³**"
    )

    if use_sp:

        st.write(
            f"SP water reduction = "
            f"**{water_reduction_amount:.2f} kg/m³**"
        )

    st.write(
        f"Final water = "
        f"**{water:.2f} kg/m³**"
    )


# ---------------------------------------------------------
# STEP 5
# ---------------------------------------------------------

with st.expander("5. Cement Calculation"):

    st.write(
        f"Cement from W/C = "
        f"{water:.2f} / {adopted_wc:.3f}"
    )

    st.write(
        f"Calculated cement = "
        f"**{cement_from_wc:.2f} kg/m³**"
    )

    st.write(
        f"Minimum required cement = "
        f"**{min_cement:.2f} kg/m³**"
    )

    st.write(
        f"Adopted cement = "
        f"**{cement:.2f} kg/m³**"
    )

    st.write(
        f"Actual W/C = "
        f"{water:.2f} / {cement:.2f} "
        f"= **{actual_wc:.3f}**"
    )


# ---------------------------------------------------------
# STEP 6
# ---------------------------------------------------------

with st.expander("6. Coarse Aggregate Fraction"):

    st.write(
        f"Base CA fraction at W/C = 0.50 = "
        f"**{base_ca_fraction:.3f}**"
    )

    st.write(
        f"W/C correction = "
        f"**{wc_correction:+.3f}**"
    )

    st.write(
        f"Final CA fraction = "
        f"**{ca_fraction:.3f}**"
    )

    st.write(
        f"FA fraction = "
        f"1 − {ca_fraction:.3f} "
        f"= **{fa_fraction:.3f}**"
    )


# ---------------------------------------------------------
# STEP 7
# ---------------------------------------------------------

with st.expander("7. Absolute Volume Calculation"):

    st.write(
        f"Cement volume = "
        f"**{cement_volume:.4f} m³**"
    )

    st.write(
        f"Water volume = "
        f"**{water_volume:.4f} m³**"
    )

    st.write(
        f"SP volume = "
        f"**{sp_volume:.4f} m³**"
    )

    st.write(
        f"Entrapped air volume = "
        f"**{air_volume:.4f} m³**"
    )

    st.write(
        f"Total aggregate volume = "
        f"**{aggregate_volume:.4f} m³**"
    )

    st.write(
        f"Coarse aggregate volume = "
        f"**{ca_volume:.4f} m³**"
    )

    st.write(
        f"Fine aggregate volume = "
        f"**{fa_volume:.4f} m³**"
    )


# ---------------------------------------------------------
# STEP 8
# ---------------------------------------------------------

with st.expander("8. Final Aggregate Quantities"):

    st.write(
        f"Coarse aggregate = "
        f"{ca_volume:.4f} × {sg_ca:.2f} × 1000 "
        f"= **{ca_mass:.2f} kg/m³**"
    )

    st.write(
        f"Fine aggregate = "
        f"{fa_volume:.4f} × {sg_fa:.2f} × 1000 "
        f"= **{fa_mass:.2f} kg/m³**"
    )


# =========================================================
# CHECKS
# =========================================================

st.subheader("✅ Design Checks")

check_table = pd.DataFrame({
    "Check": [
        x[0]
        for x in checks
    ],
    "Status": [
        "PASS" if x[1] else "FAIL"
        for x in checks
    ]
})

st.dataframe(
    check_table,
    use_container_width=True,
    hide_index=True
)

if cement > 450:

    st.warning(
        f"Cement content = {cement:.2f} kg/m³, "
        "which exceeds 450 kg/m³. "
        "The mix should be redesigned."
    )

if fck < min_grade:

    st.warning(
        f"{grade} is below the minimum grade specified "
        f"for {exposure} exposure."
    )


# =========================================================
# DOWNLOAD RESULT
# =========================================================

st.subheader("📥 Download Mix Design")

download_df = pd.DataFrame({

    "Parameter": [
        "Concrete Grade",
        "Maximum Aggregate Size (mm)",
        "Fine Aggregate Zone",
        "Slump (mm)",
        "Exposure",
        "Target Mean Strength (MPa)",
        "Water (kg/m3)",
        "Cement (kg/m3)",
        "Fine Aggregate (kg/m3)",
        "Coarse Aggregate (kg/m3)",
        "Superplasticizer (kg/m3)",
        "Actual W/C Ratio",
        "Fine Aggregate Ratio",
        "Coarse Aggregate Ratio"
    ],

    "Value": [
        grade,
        max_agg,
        zone,
        slump,
        exposure,
        round(target_strength, 2),
        round(water, 2),
        round(cement, 2),
        round(fa_mass, 2),
        round(ca_mass, 2),
        round(sp_mass, 2),
        round(actual_wc, 3),
        round(fa_ratio, 3),
        round(ca_ratio, 3)
    ]
})

csv = download_df.to_csv(
    index=False
)

st.download_button(
    label="⬇️ Download Mix Design CSV",
    data=csv,
    file_name="IS_10262_Concrete_Mix_Design.csv",
    mime="text/csv"
)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "CE203 Civil Engineering Materials | "
    "Concrete Mix Design | "
    "Based on the supplied CE203 lecture material."
)