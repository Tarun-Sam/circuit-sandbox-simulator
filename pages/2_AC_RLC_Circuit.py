import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import helpers

st.title("⚡ AC Series RLC Circuit Analyzer")

# --- Formulas Section ---
with st.expander("Formulas & Concepts Used"):
    st.markdown(
        """
        This analyzer calculates key parameters for a series RLC circuit in an AC system.

        - **Reactance ($X_L$, $X_C$):** The opposition to current flow from inductors and capacitors.
        """
    )
    st.latex(r"X_L = 2\pi fL \quad (\text{Inductive}) \qquad X_C = \frac{1}{2\pi fC} \quad (\text{Capacitive})")
    st.markdown("- **Impedance (Z):** The total opposition to current flow in an AC circuit (combining resistance and reactance).")
    st.latex(r"Z = \sqrt{R^2 + (X_L - X_C)^2}")
    st.markdown("- **Phase Angle (φ):** The angle between the voltage and current waveforms.")
    st.latex(r"\phi = \arctan\left(\frac{X_L - X_C}{R}\right)")
    st.markdown("- **Power Factor (PF):** The ratio of real power to apparent power, indicating circuit efficiency.")
    st.latex(r"PF = \cos(\phi)")
    st.markdown("- **Resonant Frequency ($f_0$):** The frequency at which the circuit is purely resistive ($X_L = X_C$).")
    st.latex(r"f_0 = \frac{1}{2\pi\sqrt{LC}}")

# --- UI and Calculation Logic (unchanged) ---
def reset_form():
    st.session_state.r_rlc = ""
    st.session_state.l_rlc = ""
    st.session_state.c_rlc = ""
    st.session_state.vp_rlc = ""
    st.session_state.f_rlc = ""

with st.form("rlc_form"):
    st.write("Enter the circuit parameters below.")
    col1, col2, col3 = st.columns(3)
    with col1:
        r_str = st.text_input("Resistance R (Ω)", key="r_rlc")
        l_str = st.text_input("Inductance L (H)", key="l_rlc")
    with col2:
        c_str = st.text_input("Capacitance C (F)", key="c_rlc")
        v_peak_str = st.text_input("Peak Voltage Vp (V)", key="vp_rlc")
    with col3:
        f_str = st.text_input("Frequency f (Hz)", key="f_rlc")
    
    b_col1, b_col2 = st.columns([1, 1])
    submitted = b_col1.form_submit_button("Analyze Circuit", use_container_width=True)
    b_col2.form_submit_button("Reset", on_click=reset_form, use_container_width=True)

if submitted:
    try:
        R=helpers.parse_engineering_notation(r_str); L=helpers.parse_engineering_notation(l_str); C=helpers.parse_engineering_notation(c_str); V_peak=helpers.parse_engineering_notation(v_peak_str); f=helpers.parse_engineering_notation(f_str); omega=2*np.pi*f; Xl=omega*L; Xc=1/(omega*C); X_total=Xl-Xc; Z=np.sqrt(R**2 + X_total**2); I_peak=V_peak/Z; phase_angle_rad=np.arctan2(X_total,R); PF=np.cos(phase_angle_rad); f0=1/(2*np.pi*np.sqrt(L*C))
        st.subheader("Analysis Results"); col1, col2=st.columns(2)
        with col1: st.metric("Total Impedance (Z)",f"{Z:.2f} Ω"); st.metric("Peak Current (Ip)",f"{I_peak*1000:.2f} mA")
        with col2: st.metric("Phase Angle (φ)",f"{np.degrees(phase_angle_rad):.2f}°"); st.metric("Power Factor (PF)",f"{PF:.3f} {'lagging' if Xl > Xc else 'leading'}")
        st.metric("Resonant Frequency (f0)",f"{f0:.2f} Hz",delta=f"{f-f0:.2f} Hz from resonance")
        st.subheader("Waveform Plot"); fig, ax=plt.subplots(); t=np.linspace(0,3/f,500); v=V_peak*np.sin(omega*t); i=I_peak*np.sin(omega*t - phase_angle_rad)
        ax.plot(t,v,label="Voltage (V)"); ax.plot(t,i,label=f"Current (A)",linestyle='--'); ax.set_title("AC Voltage and Current"); ax.set_xlabel("Time (s)"); ax.grid(True); ax.legend()
        st.pyplot(fig)
    except Exception: st.error(f"Invalid input. Please check all values.")