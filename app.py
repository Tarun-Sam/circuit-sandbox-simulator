# app.py
import streamlit as st

st.set_page_config(
    page_title="Circuit Sandbox Simulator",
    page_icon="⚡",
    layout="centered"
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
    - **AC Series RLC Circuit Analyzer** with impedance, power, and resonance calculations.
    - **RC Low-Pass Filter Designer** with an interactive Bode plot.
    - **BJT Common-Emitter Amplifier** Q-point and AC analysis.
    - **Digital Logic Gate Simulator** for basic logic operations.
    """
)