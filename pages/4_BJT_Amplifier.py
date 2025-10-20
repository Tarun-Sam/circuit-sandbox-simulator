import streamlit as st
import helpers

st.title("🔌 BJT Common-Emitter Amplifier")

# --- Formulas Section ---
with st.expander("Formulas & Concepts Used"):
    st.markdown("This tool analyzes a BJT in a standard voltage-divider bias configuration.")
    st.subheader("DC Analysis (Q-Point)")
    st.markdown("- **Base Voltage ($V_B$):** Set by the voltage divider rule.")
    st.latex(r"V_B = V_{CC} \left(\frac{R_2}{R_1 + R_2}\right)")
    st.markdown("- **Emitter Current ($I_E$):** Found using the base voltage, assuming $V_{BE} \approx 0.7V$.")
    st.latex(r"I_E = \frac{V_B - V_{BE}}{R_E}")
    st.markdown("- **Collector-Emitter Voltage ($V_{CEQ}$):** The DC voltage across the transistor.")
    st.latex(r"V_{CEQ} = V_{CC} - I_C R_C - I_E R_E \quad (\text{where } I_C \approx I_E)")
    st.subheader("AC Analysis")
    st.markdown("- **Internal Emitter Resistance ($r_e'$):** A dynamic resistance dependent on the DC emitter current.")
    st.latex(r"r_e' = \frac{26 \text{mV}}{I_E}")
    st.markdown("- **Voltage Gain ($A_v$):** The ratio of output to input voltage (assuming the emitter resistor is bypassed by a capacitor).")
    st.latex(r"A_v = -\frac{R_C}{r_e'}")


# --- UI and Calculation Logic (unchanged) ---
def reset_form():
    st.session_state.vcc_bjt = ""
    st.session_state.r1_bjt = ""
    st.session_state.r2_bjt = ""
    st.session_state.rc_bjt = ""
    st.session_state.re_bjt = ""
    st.session_state.beta_bjt = ""

with st.form("bjt_form"):
    st.write("Enter parameters for a voltage-divider bias configuration.")
    col1, col2 = st.columns(2)
    with col1:
        vcc_str = st.text_input("Vcc (V)", key="vcc_bjt")
        r1_str = st.text_input("R1 (Ω)", key="r1_bjt")
        r2_str = st.text_input("R2 (Ω)", key="r2_bjt")
    with col2:
        rc_str = st.text_input("Rc (Ω)", key="rc_bjt")
        re_str = st.text_input("Re (Ω)", key="re_bjt")
        beta_str = st.text_input("Beta (β)", key="beta_bjt")
    
    b_col1, b_col2 = st.columns([1, 1])
    submitted = b_col1.form_submit_button("Analyze Amplifier", use_container_width=True)
    b_col2.form_submit_button("Reset", on_click=reset_form, use_container_width=True)

if submitted:
    try:
        Vcc=helpers.parse_engineering_notation(vcc_str); R1=helpers.parse_engineering_notation(r1_str); R2=helpers.parse_engineering_notation(r2_str); Rc=helpers.parse_engineering_notation(rc_str); Re=helpers.parse_engineering_notation(re_str); beta=helpers.parse_engineering_notation(beta_str)
        Vb=Vcc*(R2/(R1+R2)); Ve=Vb-0.7; Ie=Ve/Re; Ic=Ie; Vce=Vcc-(Ic*Rc)-Ve; re_prime=26e-3/Ie; Av=-Rc/re_prime
        st.subheader("DC Q-Point Analysis"); col1, col2=st.columns(2)
        col1.metric("Collector Current (Icq)",f"{Ic*1000:.2f} mA"); col2.metric("Collector-Emitter Voltage (Vceq)",f"{Vce:.2f} V")
        st.subheader("AC Small-Signal Analysis"); col1, col2=st.columns(2)
        col1.metric("Internal Resistance (r_e')",f"{re_prime:.2f} Ω"); col2.metric("Voltage Gain (Av)",f"{Av:.2f}")
        if Vce < 0.2: st.warning("Transistor may be in saturation.")
    except Exception: st.error(f"Invalid input. Please check all values.")