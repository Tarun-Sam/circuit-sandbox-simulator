# app.py
import streamlit as st

st.set_page_config(
    page_title="Circuit Sandbox Simulator",
    page_icon="⚡", # You can use an emoji as an icon
    layout="centered" # Use "wide" or "centered"
)

st.title("Welcome to the Circuit Sandbox Simulator! 🚀")
st.write("---")
st.header("An Interactive Toolkit for ECE Students and Hobbyists")

st.markdown(
    """
    This web application is a collection of powerful calculators for common
    electrical and electronics engineering problems.

    **👈 Select a calculator from the sidebar** to get started.

    ### Features Include:
    - **Ohm's Law Calculator** for basic DC analysis.
    - **RC Low-Pass & High-Pass Filters** with interactive Bode plots.
    - **AC Series RLC Circuit Analyzer** with impedance, power, and resonance calculations.
    - **BJT Amplifiers (CE, CC, CB):** Q-point and AC analysis for all three basic configurations.
    - **Op-Amp (Inverting & Non-Inverting):** Gain and impedance calculations for ideal op-amps.
    - **Digital Logic Gate Simulator** for basic logic operations.
    """
)
st.write("---")
st.caption("Built with Python & Streamlit.") # Added a small footer