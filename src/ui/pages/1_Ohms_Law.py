import streamlit as st

from utils import helpers

st.title("Ohm's Law Calculator")
st.caption("Enter exactly two known values and compute the third.")

with st.expander("Formulas"):
    st.latex(r"V = I \times R")
    st.latex(r"I = \frac{V}{R}")
    st.latex(r"R = \frac{V}{I}")


def reset_values() -> None:
    st.session_state.v_input = ""
    st.session_state.i_input = ""
    st.session_state.r_input = ""


st.text_input("Voltage (V)", key="v_input")
st.text_input("Current (A)", key="i_input")
st.text_input("Resistance (Ohm)", key="r_input")

col1, col2 = st.columns(2)
calculate_button = col1.button("Calculate", use_container_width=True)
col2.button("Reset", on_click=reset_values, use_container_width=True)

if calculate_button:
    raw_values = {
        "Voltage (V)": st.session_state.v_input,
        "Current (A)": st.session_state.i_input,
        "Resistance (Ohm)": st.session_state.r_input,
    }

    provided_fields = [name for name, raw in raw_values.items() if raw.strip()]
    if len(provided_fields) != 2:
        st.error("Provide exactly two values and leave one field blank.")
    else:
        errors: list[str] = []
        parsed = {
            name: helpers.parse_required_value(name, raw_values[name], errors)
            if name in provided_fields
            else None
            for name in raw_values
        }

        if errors:
            for error in errors:
                st.error(error)
        else:
            v = parsed["Voltage (V)"]
            i = parsed["Current (A)"]
            r = parsed["Resistance (Ohm)"]

            if r is not None and r < 0:
                st.error("Resistance must be non-negative.")
            elif v is None:
                st.success(f"Calculated Voltage: {i * r:.4f} V")
            elif i is None:
                if r == 0:
                    st.error("Resistance must be non-zero when solving for current.")
                else:
                    st.success(f"Calculated Current: {v / r:.6g} A")
            else:
                if i == 0:
                    st.error("Current must be non-zero when solving for resistance.")
                else:
                    st.success(f"Calculated Resistance: {v / i:.4f} Ohm")
