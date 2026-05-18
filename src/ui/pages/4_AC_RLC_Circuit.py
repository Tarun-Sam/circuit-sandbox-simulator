import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from utils import helpers

st.title("AC Series RLC Circuit Analyzer")
st.caption("Analyze impedance, phase, power factor, and steady-state waveforms.")

with st.expander("Formulas"):
    st.latex(r"X_L = 2\pi fL")
    st.latex(r"X_C = \frac{1}{2\pi fC}")
    st.latex(r"Z = \sqrt{R^2 + (X_L - X_C)^2}")
    st.latex(r"\phi = \arctan\left(\frac{X_L - X_C}{R}\right)")
    st.latex(r"f_0 = \frac{1}{2\pi\sqrt{LC}}")


def reset_form() -> None:
    st.session_state.r_rlc = ""
    st.session_state.l_rlc = ""
    st.session_state.c_rlc = ""
    st.session_state.vp_rlc = ""
    st.session_state.f_rlc = ""


with st.form("rlc_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        r_str = st.text_input("Resistance R (Ohm)", key="r_rlc")
        l_str = st.text_input("Inductance L (H)", key="l_rlc")
    with col2:
        c_str = st.text_input("Capacitance C (F)", key="c_rlc")
        v_peak_str = st.text_input("Peak Voltage Vp (V)", key="vp_rlc")
    with col3:
        f_str = st.text_input("Frequency f (Hz)", key="f_rlc")

    b_col1, b_col2 = st.columns(2)
    submitted = b_col1.form_submit_button("Analyze", use_container_width=True)
    b_col2.form_submit_button("Reset", on_click=reset_form, use_container_width=True)

if submitted:
    errors: list[str] = []
    r_value = helpers.parse_required_value("Resistance R", r_str, errors)
    l_value = helpers.parse_required_value("Inductance L", l_str, errors)
    c_value = helpers.parse_required_value("Capacitance C", c_str, errors)
    v_peak = helpers.parse_required_value("Peak Voltage Vp", v_peak_str, errors)
    frequency = helpers.parse_required_value("Frequency f", f_str, errors)

    if r_value is not None:
        helpers.require_positive("Resistance R", r_value, errors)
    if l_value is not None:
        helpers.require_positive("Inductance L", l_value, errors)
    if c_value is not None:
        helpers.require_positive("Capacitance C", c_value, errors)
    if frequency is not None:
        helpers.require_positive("Frequency f", frequency, errors)

    if errors:
        for error in errors:
            st.error(error)
    else:
        omega = 2.0 * np.pi * frequency
        xl = omega * l_value
        xc = 1.0 / (omega * c_value)
        reactance = xl - xc
        impedance = np.sqrt(r_value**2 + reactance**2)

        if impedance == 0:
            st.error("Computed impedance is zero; check the input values.")
        else:
            i_peak = v_peak / impedance
            phase_rad = np.arctan2(reactance, r_value)
            phase_deg = np.degrees(phase_rad)
            power_factor = np.cos(phase_rad)
            f0 = 1.0 / (2.0 * np.pi * np.sqrt(l_value * c_value))

            st.subheader("Results")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Impedance", helpers.format_with_unit(impedance, "Ohm", precision=3))
                st.metric("Peak Current", helpers.format_with_unit(i_peak, "A", precision=6))
            with col2:
                st.metric("Phase Angle", helpers.format_with_unit(phase_deg, "deg", precision=3))
                phase_type = "lagging" if reactance > 0 else "leading"
                st.metric("Power Factor", f"{power_factor:.4f} ({phase_type})")

            st.metric(
                "Resonant Frequency",
                helpers.format_with_unit(f0, "Hz", precision=3),
                delta=f"{frequency - f0:.3f} Hz",
            )

            t = np.linspace(0.0, 3.0 / frequency, 600)
            voltage = v_peak * np.sin(omega * t)
            current = i_peak * np.sin(omega * t - phase_rad)

            fig, ax = plt.subplots()
            ax.plot(t, voltage, label="Voltage (V)")
            ax.plot(t, current, label="Current (A)", linestyle="--")
            ax.set_title("Voltage and Current Waveforms")
            ax.set_xlabel("Time (s)")
            ax.grid(True, alpha=0.4)
            ax.legend()
            st.pyplot(fig)
            plt.close(fig)
