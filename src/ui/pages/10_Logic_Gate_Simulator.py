import streamlit as st

st.title("Digital Logic Gate Simulator")
st.caption("Evaluate gate output for binary inputs.")

with st.expander("Boolean Expressions"):
    st.markdown(
        """
        - AND: `Q = A.B`
        - OR: `Q = A + B`
        - NAND: `Q = NOT(A.B)`
        - NOR: `Q = NOT(A + B)`
        - XOR: `Q = A XOR B`
        - NOT: `Q = NOT(A)`
        - BUF: `Q = A`
        """
    )


def reset_logic() -> None:
    st.session_state.gate_key = "AND"
    st.session_state.a_key = 0
    st.session_state.b_key = 0


def compute_logic(gate: str, a_val: int, b_val: int | None = None) -> int:
    if gate == "AND":
        return int(a_val and b_val)
    if gate == "OR":
        return int(a_val or b_val)
    if gate == "NAND":
        return int(not (a_val and b_val))
    if gate == "NOR":
        return int(not (a_val or b_val))
    if gate == "XOR":
        return int(a_val ^ b_val)
    if gate == "NOT":
        return int(not a_val)
    if gate == "BUF":
        return int(a_val)
    raise ValueError(f"Unsupported gate: {gate}")


st.selectbox("Gate", ["AND", "OR", "NAND", "NOR", "XOR", "NOT", "BUF"], key="gate_key")

col1, col2 = st.columns(2)
with col1:
    st.selectbox("Input A", [0, 1], key="a_key")
with col2:
    if st.session_state.gate_key in {"NOT", "BUF"}:
        st.selectbox("Input B", [0, 1], key="b_key", disabled=True)
    else:
        st.selectbox("Input B", [0, 1], key="b_key")

b_col1, b_col2 = st.columns(2)
simulate_button = b_col1.button("Simulate", use_container_width=True)
b_col2.button("Reset", on_click=reset_logic, use_container_width=True)

if simulate_button:
    gate = st.session_state.gate_key
    a_val = int(st.session_state.a_key)
    b_val = int(st.session_state.b_key)

    if gate in {"NOT", "BUF"}:
        result = compute_logic(gate, a_val)
        st.success(f"{gate}({a_val}) = {result}")
    else:
        result = compute_logic(gate, a_val, b_val)
        st.success(f"{gate}({a_val}, {b_val}) = {result}")
