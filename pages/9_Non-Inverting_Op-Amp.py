# pages/09_🔌_Non-Inverting_Op-Amp.py
import streamlit as st
import helpers
import numpy as np

# --- Page Configuration (Optional but recommended) ---
# This gives your content more space and can help with line wrapping.
# You might want to put this in your main 'Hello.py' file instead.
# st.set_page_config(layout="wide")

# --- Title (Shortened) ---
# Shortened the title to help ensure it stays on one line
st.title("🔌 Non-Inverting Op-Amp")

# --- Image (Fixed Link) ---
# Replaced the broken imgur link with a valid one
st.image("https://i.imgur.com/vXYtH8C.png", width=400, caption="Non-Inverting Op-Amp Configuration")


# --- Formulas Section ---
with st.expander("Formulas & Concepts Used"):
    st.markdown("""
        This tool analyzes a standard Non-Inverting Operational Amplifier.
        The input signal is applied directly to the non-inverting (+) terminal.
        The feedback network (like a voltage divider) is connected to the inverting (-) terminal.
        This configuration produces an amplified, non-inverted (in-phase) output.

        *(Note: This calculation assumes an ideal Op-Amp.)*
    """)
    st.subheader("Voltage Gain ($A_v$)")
    st.markdown("The gain is determined by the ratio of the two resistors and is always 1 or greater.")
    st.latex(r"A_v = \frac{V_{out}}{V_{in}} = 1 + \frac{R_f}{R_{in}}")
    st.markdown("- **Input Impedance ($Z_{in}$):**")
    st.markdown("Because the input signal goes directly to the op-amp's non-inverting terminal, the input impedance is considered infinitely high.")
    st.latex(r"Z_{in} \approx \infty \Omega")
    st.markdown("- **Output Impedance ($Z_{out}$):**")
    st.markdown("Due to the ideal op-amp assumption, the output impedance is $0 \Omega$.")
    st.latex(r"Z_{out} \approx 0 \Omega")

# --- UI and Calculation Logic ---
def reset_form():
    st.session_state.rin_noninv = ""
    st.session_state.rf_noninv = ""

with st.form("opamp_noninv_form"):
    st.write("Enter the resistor values for the non-inverting amplifier.")
    col1, col2 = st.columns(2)
    with col1:
        rin_str = st.text_input("Input Resistor $R_{in}$ (Ω)", key="rin_noninv")
    with col2:
        rf_str = st.text_input("Feedback Resistor $R_f$ (Ω)", key="rf_noninv")

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
            Av = 1 + (R_f / R_in)
            Zin = float('inf')
            Zout = 0.0

            st.subheader("Analysis Results")
            col1, col2, col3 = st.columns(3)
            col1.metric("Voltage Gain (Av)", f"{Av:.2f}")
            col2.metric("Input Impedance (Zin)", "∞ Ω (Ideal)")
            col3.metric("Output Impedance (Zout)", f"{Zout:.1f} Ω")

    except Exception as e:
        st.error(f"Invalid input. Please check all values. Error: {e}")