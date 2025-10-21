# pages/08_🔌_Inverting_Op-Amp.py
import streamlit as st
import helpers
import numpy as np

st.title("🔌 Inverting Op-Amp Amplifier")
# ✅ Added a valid image display using st.image
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Op-Amp_Inverting_Amplifier.svg/300px-Op-Amp_Inverting_Amplifier.svg.png", caption="Inverting Op-Amp Configuration")

# --- Formulas Section ---
with st.expander("Formulas & Concepts Used"):
    st.markdown("""
        This tool analyzes a standard Inverting Operational Amplifier.
        The input signal (via $R_{in}$) is applied to the inverting (-) terminal,
        and the non-inverting (+) terminal is connected to ground.
        This configuration produces an amplified and inverted output signal.

        *(Note: This calculation assumes an ideal Op-Amp, which has
        infinite gain, infinite input impedance, and zero output impedance.)*
    """)
    st.subheader("Voltage Gain ($A_v$)")
    st.markdown("The gain is determined by the ratio of the feedback resistor to the input resistor.")
    st.latex(r"A_v = \frac{V_{out}}{V_{in}} = -\frac{R_f}{R_{in}}")
    st.markdown("- **Input Impedance ($Z_{in}$):**")
    st.markdown("Because the inverting terminal is a 'virtual ground', the input impedance seen by the source is simply $R_{in}$.")
    st.latex(r"Z_{in} = R_{in}")
    st.markdown("- **Output Impedance ($Z_{out}$):**")
    st.markdown("Due to the ideal op-amp assumption, the output impedance is $0 \Omega$.")
    st.latex(r"Z_{out} \approx 0 \Omega")

# --- UI and Calculation Logic ---
def reset_form():
    st.session_state.rin_opamp = ""
    st.session_state.rf_opamp = ""

with st.form("opamp_inv_form"):
    st.write("Enter the resistor values for the inverting amplifier.")
    col1, col2 = st.columns(2)
    with col1:
        rin_str = st.text_input("Input Resistor $R_{in}$ (Ω)", key="rin_opamp")
    with col2:
        rf_str = st.text_input("Feedback Resistor $R_f$ (Ω)", key="rf_opamp")

    b_col1, b_col2 = st.columns([1, 1])
    submitted = b_col1.form_submit_button("Analyze Amplifier", use_container_width=True)
    b_col2.form_submit_button("Reset", on_click=reset_form, use_container_width=True)

if submitted:
    try:
        # --- Calculations ---
        R_in = helpers.parse_engineering_notation(rin_str)
        R_f = helpers.parse_engineering_notation(rf_str)

        if R_in == 0:
            st.error("Input Resistor (R_in) cannot be zero.")
        else:
            Av = -R_f / R_in
            Zin = R_in
            Zout = 0.0

            st.subheader("Analysis Results")
            col1, col2, col3 = st.columns(3)
            col1.metric("Voltage Gain (Av)", f"{Av:.2f}")
            col2.metric("Input Impedance (Zin)", f"{Zin/1000:.2f} kΩ" if Zin >= 1000 else f"{Zin:.2f} Ω")
            col3.metric("Output Impedance (Zout)", f"{Zout:.1f} Ω")

            if abs(Av) < 1:
                st.info("Note: The magnitude of the gain is less than 1. This is an attenuator.")

    except Exception as e:
        st.error(f"Invalid input. Please check all values. Error: {e}")