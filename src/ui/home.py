import streamlit as st


def render() -> None:
    st.title("Circuit Sandbox Simulator")
    st.caption(
        "Interactive circuit analysis tools for core ECE workflows: DC, AC, filters, amplifiers, and logic."
    )

    st.divider()

    left_col, right_col = st.columns([3, 2])
    with left_col:
        st.markdown("### What You Can Do")
        st.markdown(
            """
            - Solve Ohm's law relationships from any two known values
            - Analyze RC filters using cutoff frequency and Bode magnitude curves
            - Evaluate AC series RLC impedance, phase, and waveform behavior
            - Compute BJT amplifier operating points and small-signal behavior
            - Estimate inverting and non-inverting op-amp gain
            - Simulate basic logic gates and verify truth-table outputs
            """
        )

    with right_col:
        st.markdown("### Typical Use Cases")
        st.info(
            """
            - Lab verification
            - Exam preparation
            - Parameter exploration
            """
        )

    st.divider()


if __name__ == "__main__":
    render()
