# pages/🔌 BJT CB Amplifier.py
import streamlit as st
import helpers

st.title("🔌 BJT Common-Base Amplifier")

# --- Formulas Section ---
with st.expander("Formulas & Concepts Used"):
    st.markdown("This tool analyzes a BJT in a standard voltage-divider bias, Common-Base configuration. The input is applied to the Emitter and the output is taken from the Collector.")
    st.subheader("DC Analysis (Q-Point)")
    st.markdown("The DC analysis is identical to the Common-Emitter configuration.")
    st.latex(r"V_B = V_{CC} \left(\frac{R_2}{R_1 + R_2}\right) \quad I_E = \frac{V_B - 0.7V}{R_E}")
    st.latex(r"V_{CEQ} = V_{CC} - I_C R_C - I_E R_E \quad (\text{where } I_C \approx I_E)")
    st.subheader("AC Analysis")
    st.markdown("- **Internal Emitter Resistance ($r_e'$):**")
    st.latex(r"r_e' = \frac{26 \text{mV}}{I_E}")
    st.markdown("- **Voltage Gain ($A_v$):** Non-inverting and typically high.")
    st.latex(r"A_v \approx \frac{R_C}{r_e'}")
    st.markdown("- **Input Impedance ($Z_{in}$):** Very low, a key characteristic.")
    st.latex(r"Z_{in} = R_E \parallel r_e' \approx r_e'")
    st.markdown("- **Output Impedance ($Z_{out}$):** High, essentially just $R_C$.")
    st.latex(r"Z_{out} \approx R_C")

# --- UI and Calculation Logic ---
def reset_form():
    st.session_state.vcc_cb = ""
    st.session_state.r1_cb = ""
    st.session_state.r2_cb = ""
    st.session_state.rc_cb = ""
    st.session_state.re_cb = ""
    st.session_state.beta_cb = ""

with st.form("bjt_cb_form"):
    st.write("Enter parameters for a voltage-divider bias configuration.")
    col1, col2 = st.columns(2)
    with col1:
        vcc_str = st.text_input("Vcc (V)", key="vcc_cb")
        r1_str = st.text_input("R1 (Ω)", key="r1_cb")
        r2_str = st.text_input("R2 (Ω)", key="r2_cb")
    with col2:
        rc_str = st.text_input("Rc (Ω)", key="rc_cb")
        re_str = st.text_input("Re (Ω)", key="re_cb")
        beta_str = st.text_input("Beta (β)", key="beta_cb")
    
    b_col1, b_col2 = st.columns([1, 1])
    submitted = b_col1.form_submit_button("Analyze Amplifier", use_container_width=True)
    b_col2.form_submit_button("Reset", on_click=reset_form, use_container_width=True)

if submitted:
    try:
        # DC Analysis (same as CE)
        Vcc=helpers.parse_engineering_notation(vcc_str); R1=helpers.parse_engineering_notation(r1_str)
        R2=helpers.parse_engineering_notation(r2_str); Rc=helpers.parse_engineering_notation(rc_str)
        Re=helpers.parse_engineering_notation(re_str); beta=helpers.parse_engineering_notation(beta_str)
        Vb=Vcc*(R2/(R1+R2)); Ve=Vb-0.7; Ie=Ve/Re; Ic=Ie; Vce=Vcc-(Ic*Rc)-Ve
        
        # AC Analysis (different from CE)
        re_prime = 26e-3 / Ie
        Av = Rc / re_prime
        Zin = (Re * re_prime) / (Re + re_prime) # Zin is RE || r_e'
        Zout = Rc
        
        st.subheader("DC Q-Point Analysis")
        col1, col2 = st.columns(2)
        col1.metric("Collector Current (Icq)",f"{Ic*1000:.2f} mA")
        col2.metric("Collector-Emitter Voltage (Vceq)",f"{Vce:.2f} V")
        
        st.subheader("AC Small-Signal Analysis")
        col1, col2, col3 = st.columns(3)
        col1.metric("Voltage Gain (Av)", f"{Av:.2f}")
        col2.metric("Input Impedance (Zin)", f"{Zin:.2f} Ω")
        col3.metric("Output Impedance (Zout)", f"{Zout/1000:.2f} kΩ")

        if Vce < 0.2: st.warning("Transistor may be in saturation.")
    except Exception: 
        st.error(f"Invalid input. Please check all values.")