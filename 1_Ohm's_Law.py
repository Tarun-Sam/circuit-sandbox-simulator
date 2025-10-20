import streamlit as st
import helpers

st.title("💡 Ohm's Law Calculator")
st.write("Enter exactly TWO known values. The third will be calculated.")

def reset_values():
    st.session_state.v_input = ""
    st.session_state.i_input = ""
    st.session_state.r_input = ""

# Removed placeholder arguments
st.text_input("Voltage (V)", key="v_input")
st.text_input("Current (I)", key="i_input")
st.text_input("Resistance (R)", key="r_input")

col1, col2 = st.columns([1, 1])
calculate_button = col1.button("Calculate", use_container_width=True)
reset_button = col2.button("Reset", on_click=reset_values, use_container_width=True)

if calculate_button:
    V = helpers.parse_engineering_notation(st.session_state.v_input) if st.session_state.v_input else None
    I = helpers.parse_engineering_notation(st.session_state.i_input) if st.session_state.i_input else None
    R = helpers.parse_engineering_notation(st.session_state.r_input) if st.session_state.r_input else None
    
    known_values = sum(val is not None for val in [V, I, R])
    
    if known_values != 2:
        st.error("Error: Please provide exactly TWO known values.")
    else:
        try:
            if V is None: st.success(f"Calculated Voltage: {I * R:.4f} V")
            elif I is None: st.success(f"Calculated Current: {V / R:.4g} A")
            elif R is None: st.success(f"Calculated Resistance: {V / I:.4f} Ω")
        except ZeroDivisionError:
            st.error("Error: Division by zero.")