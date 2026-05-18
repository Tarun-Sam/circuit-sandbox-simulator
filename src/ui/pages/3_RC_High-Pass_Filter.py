import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from utils import helpers

st.title("RC High-Pass Filter Analyzer")
st.caption("Compute cutoff frequency and plot the magnitude response.")

with st.expander("Formulas"):
    st.latex(r"f_c = \frac{1}{2\pi RC}")
    st.latex(r"M_{dB} = 20 \log_{10}\left(\frac{f/f_c}{\sqrt{1 + (f/f_c)^2}}\right)")


def reset_form() -> None:
    st.session_state.r_hp_filter = ""
    st.session_state.c_hp_filter = ""


with st.form("rc_high_pass_form"):
    col1, col2 = st.columns(2)
    with col1:
        r_str = st.text_input("Resistance R (Ohm)", key="r_hp_filter")
    with col2:
        c_str = st.text_input("Capacitance C (F)", key="c_hp_filter")

    b_col1, b_col2 = st.columns(2)
    submitted = b_col1.form_submit_button("Analyze", use_container_width=True)
    b_col2.form_submit_button("Reset", on_click=reset_form, use_container_width=True)

if submitted:
    errors: list[str] = []
    r_value = helpers.parse_required_value("Resistance R", r_str, errors)
    c_value = helpers.parse_required_value("Capacitance C", c_str, errors)

    if r_value is not None:
        helpers.require_positive("Resistance R", r_value, errors)
    if c_value is not None:
        helpers.require_positive("Capacitance C", c_value, errors)

    if errors:
        for error in errors:
            st.error(error)
    else:
        fc = 1.0 / (2.0 * np.pi * r_value * c_value)
        st.metric("Cutoff Frequency (-3 dB)", helpers.format_with_unit(fc, "Hz", precision=3))

        lower_exp = np.log10(fc) - 3
        upper_exp = np.log10(fc) + 3
        freq = np.logspace(lower_exp, upper_exp, 600)
        ratio = freq / fc
        magnitude = ratio / np.sqrt(1.0 + ratio**2)
        response_db = 20.0 * np.log10(np.clip(magnitude, 1e-15, None))

        fig, ax = plt.subplots()
        ax.semilogx(freq, response_db)
        ax.set_title("Bode Magnitude")
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Magnitude (dB)")
        ax.grid(which="both", linestyle="--", alpha=0.5)
        ax.axvline(fc, color="r", linestyle="--", label=f"fc = {fc:.3g} Hz")
        ax.axhline(-3, color="g", linestyle=":", label="-3 dB")
        ax.legend()
        st.pyplot(fig)
        plt.close(fig)
