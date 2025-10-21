# pages/🔌 BJT CC Amplifier.py
import streamlit as st
import helpers
import numpy as np

st.title("🔌 BJT Common-Collector (Emitter-Follower)")

# --- Formulas Section ---
with st.expander("Formulas & Concepts Used"):
    st.markdown("""
        This tool analyzes a BJT in a Common-Collector (or Emitter-Follower) configuration.
        The input is applied to the Base, and the output is taken from the Emitter.
        This configuration is known for its high input impedance and low output impedance,
        making it an ideal voltage buffer. It has a non-inverting voltage gain of approximately 1.
        
        *(Note: This calculator assumes a standard voltage-divider bias and that there is
        no collector resistor, i.e., $R_C = 0$).*
    """)
    st.subheader("DC Analysis (Q-Point)")
    st.markdown("- **Base Voltage ($V_B$):**")
    st.latex(r"V_B = V_{CC} \left(\frac{R_2}{R_1 + R_2}\right)")
    st.markdown("- **Emitter Current ($I_E$):**")
    st.latex(r"I_E = \frac{V_B - V_{BE}}{R_E} \quad (\text{assuming } V_{BE} \approx 0.7V)")
    st.markdown("- **Collector-Emitter Voltage ($V_{CEQ}$):**")
    st.latex(r"V_{CEQ} = V_{CC} - V_E = V_{CC} - (I_E R_E)")
    
    st.subheader("AC Analysis")
    st.markdown("- **Internal Emitter Resistance ($r_e'$):**")
    st.latex(r"r_e' = \frac{26 \text{mV}}{I_E}")
    st.markdown("- **Voltage Gain ($A_v$):** Non-inverting and slightly less than 1.")
    st.latex(r"A_v = \frac{R_E}{r_e' + R_E}")
    st.markdown("- **Input Impedance ($Z_{in}$):** High.")
    st.latex(r"Z_{base} = \beta (r_e' + R_E) \quad | \quad Z_{in} = R_1 \parallel R_2 \parallel Z_{base}")
    st.markdown("- **Output Impedance ($Z_{out}$):** Low.")
    st.latex(r"Z_{out} = R_E \parallel r_e'")

# --- UI and Calculation Logic ---
def reset_form():
    st.session_state.vcc_cc = ""
    st.session_state.r1_cc = ""
    st.session_state.r2_cc = ""
    st.session_state.re_cc = ""
    st.session_state.beta_cc = ""

with st.form("bjt_cc_form"):
    st.write("Enter parameters for a voltage-divider bias configuration.")
    col1, col2 = st.columns(2)
    with col1:
        vcc_str = st.text_input("Vcc (V)", key="vcc_cc")
        r1_str = st.text_input("R1 (Ω)", key="r1_cc")
        r2_str = st.text_input("R2 (Ω)", key="r2_cc")
    with col2:
        re_str = st.text_input("Re (Ω)", key="re_cc")
        beta_str = st.text_input("Beta (β)", key="beta_cc")
    
    b_col1, b_col2 = st.columns([1, 1])
    submitted = b_col1.form_submit_button("Analyze Amplifier", use_container_width=True)
    b_col2.form_submit_button("Reset", on_click=reset_form, use_container_width=True)

if submitted:
    try:
        # --- DC Analysis ---
        Vcc = helpers.parse_engineering_notation(vcc_str)
        R1 = helpers.parse_engineering_notation(r1_str)
        R2 = helpers.parse_engineering_notation(r2_str)
        Re = helpers.parse_engineering_notation(re_str)
        beta = helpers.parse_engineering_notation(beta_str)
        
        Vb = Vcc * (R2 / (R1 + R2))
        Ie = (Vb - 0.7) / Re
        Ic = Ie  # Approximation
        Vce = Vcc - (Ie * Re) # Since Vc = Vcc (no Rc) and Ve = Ie * Re
        
        # --- AC Analysis ---
        re_prime = 26e-3 / Ie
        Av = Re / (re_prime + Re)
        
        # Parallel resistor calculation
        def parallel(r_a, r_b):
            return (r_a * r_b) / (r_a + r_b)
            
        Z_base = beta * (re_prime + Re)
        Zin_bias = parallel(R1, R2)
        Zin = parallel(Zin_bias, Z_base)
        
        Zout = parallel(Re, re_prime)
        
        st.subheader("DC Q-Point Analysis")
        col1, col2 = st.columns(2)
        col1.metric("Collector Current (Icq)", f"{Ic*1000:.2f} mA")
        col2.metric("Collector-Emitter Voltage (Vceq)", f"{Vce:.2f} V")
        
        st.subheader("AC Small-Signal Analysis")
        col1, col2, col3 = st.columns(3)
        col1.metric("Voltage Gain (Av)", f"{Av:.3f}") # More precision for gain near 1
        col2.metric("Input Impedance (Zin)", f"{Zin/1000:.2f} kΩ")
        col3.metric("Output Impedance (Zout)", f"{Zout:.2f} Ω")

        if Vce < 1.0: # Need more Vce for an emitter-follower
            st.warning("Transistor may be in saturation or close to it.")
            
    except Exception as e: 
        st.error(f"Invalid input. Please check all values. Error: {e}")