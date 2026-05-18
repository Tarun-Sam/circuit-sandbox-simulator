import streamlit as st

from utils import helpers

st.title("Inverting Op-Amp")
st.caption("Ideal inverting amplifier gain and impedance estimates.")

with st.expander("Formulas"):
    st.latex(r"A_v = \frac{V_{out}}{V_{in}} = -\frac{R_f}{R_{in}}")
    st.latex(r"Z_{in} = R_{in}")
    st.latex(r"Z_{out} \approx 0")


def reset_form() -> None:
    st.session_state.rin_opamp = ""
    st.session_state.rf_opamp = ""


with st.form("opamp_inv_form"):
    col1, col2 = st.columns(2)
    with col1:
        rin_str = st.text_input("Input Resistor Rin (Ohm)", key="rin_opamp")
    with col2:
        rf_str = st.text_input("Feedback Resistor Rf (Ohm)", key="rf_opamp")

    b_col1, b_col2 = st.columns(2)
    submitted = b_col1.form_submit_button("Analyze", use_container_width=True)
    b_col2.form_submit_button("Reset", on_click=reset_form, use_container_width=True)

if submitted:
    errors: list[str] = []
    r_in = helpers.parse_required_value("Rin", rin_str, errors)
    r_f = helpers.parse_required_value("Rf", rf_str, errors)

    if r_in is not None:
        helpers.require_positive("Rin", r_in, errors)
    if r_f is not None:
        helpers.require_positive("Rf", r_f, errors, allow_zero=True)

    if errors:
        for error in errors:
            st.error(error)
    else:
        av = -r_f / r_in

        col1, col2, col3 = st.columns(3)
        col1.metric("Voltage Gain Av", f"{av:.4f}")
        col2.metric("Input Impedance Zin", helpers.format_with_unit(r_in, "Ohm", precision=3))
        col3.metric("Output Impedance Zout", "~0 Ohm")

        if abs(av) < 1:
            st.info("Gain magnitude is below 1, so this configuration attenuates.")
