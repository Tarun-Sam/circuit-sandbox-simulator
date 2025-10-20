import streamlit as st

st.title("🤖 Digital Logic Gate Simulator")

# Resets dropdowns to a default state
def reset_logic():
    st.session_state.gate_key = 'AND'
    st.session_state.a_key = 0
    st.session_state.b_key = 0

st.selectbox("Select a Gate:", ['AND', 'OR', 'NAND', 'NOR', 'XOR', 'NOT', 'BUF'], key="gate_key")

col1, col2 = st.columns(2)
with col1:
    st.selectbox("Input A:", [0, 1], key="a_key")

with col2:
    if st.session_state.gate_key not in ['NOT', 'BUF']:
        st.selectbox("Input B:", [0, 1], key="b_key")
    else:
        st.write("") # Placeholder for alignment

b_col1, b_col2 = st.columns([1, 1])
simulate_button = b_col1.button("Simulate", use_container_width=True)
b_col2.button("Reset", on_click=reset_logic, use_container_width=True)

if simulate_button:
    gate = st.session_state.gate_key
    a = st.session_state.a_key
    result = 0
    if gate in ['NOT', 'BUF']:
        if gate == 'NOT': result = int(not a)
        elif gate == 'BUF': result = a
    else:
        b = st.session_state.b_key
        if gate == 'AND': result = int(a and b)
        elif gate == 'OR': result = int(a or b)
        elif gate == 'NAND': result = int(not (a and b))
        elif gate == 'NOR': result = int(not (a or b))
        elif gate == 'XOR': result = int(a ^ b)
    
    st.success(f"Result: {result}")