import streamlit as st

from utils import helpers

st.title("BJT Common-Collector (Emitter Follower)")
st.caption("Emitter follower DC bias and impedance/gain approximation.")

with st.expander("Formulas"):
    st.latex(r"V_B = V_{CC}\left(\frac{R_2}{R_1 + R_2}\right)")
    st.latex(r"I_E = \frac{V_B - 0.7}{R_E}")
    st.latex(r"r_e' = \frac{26mV}{I_E}")
    st.latex(r"A_v = \frac{R_E}{r_e' + R_E}")
    st.latex(r"Z_{in} \approx (R_1 || R_2) || [\beta(r_e' + R_E)]")
    st.latex(r"Z_{out} \approx R_E || r_e'")


def reset_form() -> None:
    st.session_state.vcc_cc = ""
    st.session_state.r1_cc = ""
    st.session_state.r2_cc = ""
    st.session_state.re_cc = ""
    st.session_state.beta_cc = ""


with st.form("bjt_cc_form"):
    col1, col2 = st.columns(2)
    with col1:
        vcc_str = st.text_input("Vcc (V)", key="vcc_cc")
        r1_str = st.text_input("R1 (Ohm)", key="r1_cc")
        r2_str = st.text_input("R2 (Ohm)", key="r2_cc")
    with col2:
        re_str = st.text_input("Re (Ohm)", key="re_cc")
        beta_str = st.text_input("Beta", key="beta_cc")

    b_col1, b_col2 = st.columns(2)
    submitted = b_col1.form_submit_button("Analyze", use_container_width=True)
    b_col2.form_submit_button("Reset", on_click=reset_form, use_container_width=True)

if submitted:
    errors: list[str] = []
    vcc = helpers.parse_required_value("Vcc", vcc_str, errors)
    r1 = helpers.parse_required_value("R1", r1_str, errors)
    r2 = helpers.parse_required_value("R2", r2_str, errors)
    re = helpers.parse_required_value("Re", re_str, errors)
    beta = helpers.parse_required_value("Beta", beta_str, errors)

    for label, value in (("R1", r1), ("R2", r2), ("Re", re), ("Beta", beta)):
        if value is not None:
            helpers.require_positive(label, value, errors)

    if vcc is not None and vcc <= 0:
        errors.append("Vcc: must be > 0.")

    if errors:
        for error in errors:
            st.error(error)
    else:
        vb = vcc * (r2 / (r1 + r2))
        ve = vb - 0.7
        if ve <= 0:
            st.error("Bias point invalid: Vb - 0.7 must be > 0 for conduction.")
        else:
            ie = ve / re
            ic = ie
            vce = vcc - ve
            re_prime = 26e-3 / ie
            av = re / (re_prime + re)

            z_base = beta * (re_prime + re)
            zin_bias = helpers.parallel(r1, r2)
            zin = helpers.parallel(zin_bias, z_base)
            zout = helpers.parallel(re, re_prime)

            st.subheader("DC Q-Point")
            col1, col2 = st.columns(2)
            col1.metric("Collector Current Icq", helpers.format_with_unit(ic * 1000.0, "mA", precision=3))
            col2.metric("Collector-Emitter Voltage Vceq", helpers.format_with_unit(vce, "V", precision=3))

            st.subheader("AC Small-Signal")
            col1, col2, col3 = st.columns(3)
            col1.metric("Voltage Gain Av", f"{av:.4f}")
            col2.metric("Input Impedance Zin", helpers.format_with_unit(zin, "Ohm", precision=3))
            col3.metric("Output Impedance Zout", helpers.format_with_unit(zout, "Ohm", precision=3))

            if vce < 1.0:
                st.warning("Vce is low; emitter follower may be near saturation.")
