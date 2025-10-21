# pages/📊 RC High-Pass Filter.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import helpers

st.title("📊 RC High-Pass Filter Analyzer")

# --- Formulas Section ---
with st.expander("Formulas & Concepts Used"):
    st.markdown(
        """
        This tool analyzes a simple RC High-Pass Filter. This circuit allows high-frequency signals to pass while attenuating (reducing) low-frequency signals.

        - **Cutoff Frequency ($f_c$):** This is the frequency at which the filter's output power is reduced by half, also known as the -3dB point.
        """
    )
    st.latex(r"f_c = \frac{1}{2\pi RC}")
    st.markdown(
        """
        - **Magnitude (Bode Plot):** The plot shows the filter's gain in decibels (dB) versus frequency. The gain is calculated as:
        """
    )
    st.latex(r"M_{dB} = 20 \log_{10}\left(\frac{f/f_c}{\sqrt{1 + (f/f_c)^2}}\right)")

# --- UI and Calculation Logic ---
def reset_form():
    st.session_state.r_hp_filter = ""
    st.session_state.c_hp_filter = ""

with st.form("rc_hp_filter_form"):
    col1, col2 = st.columns(2)
    with col1:
        r_str = st.text_input("Resistance R (Ω)", key="r_hp_filter")
    with col2:
        c_str = st.text_input("Capacitance C (F)", key="c_hp_filter")
    
    b_col1, b_col2 = st.columns([1, 1])
    submitted = b_col1.form_submit_button("Analyze Filter", use_container_width=True)
    b_col2.form_submit_button("Reset", on_click=reset_form, use_container_width=True)

if submitted:
    try:
        R=helpers.parse_engineering_notation(r_str); C=helpers.parse_engineering_notation(c_str)
        fc=1/(2*np.pi*R*C)
        
        st.metric("Cutoff Frequency (-3dB)",f"{fc:.2f} Hz")
        st.subheader("Bode Plot (Magnitude Response)")
        
        fig, ax=plt.subplots()
        # Frequency range starts lower to show the "stop" band
        freq=np.logspace(np.log10(fc) - 3, int(np.log10(fc) + 2), 500) 
        
        # High-pass filter magnitude calculation
        magnitude = (freq / fc) / np.sqrt(1 + (freq / fc)**2)
        H_db = 20 * np.log10(magnitude)
        
        ax.semilogx(freq,H_db); ax.set_title('Magnitude Response'); ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Magnitude (dB)'); ax.grid(which='both',linestyle='--')
        ax.axvline(fc,color='r',linestyle='--',label=f'Cutoff = {fc:.2f} Hz')
        ax.axhline(-3,color='g',linestyle=':',label='-3 dB Point'); ax.legend()
        st.pyplot(fig)
    except Exception: 
        st.error(f"Invalid input. Please check all values.")