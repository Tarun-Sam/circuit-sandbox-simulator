# Circuit Sandbox Simulator ⚡

A multi-page web application built with Python and Streamlit, providing a suite of interactive calculators for common electrical and computer engineering problems. This project is designed for ECE students, hobbyists, and professionals looking for a quick and accessible analysis tool.

**➡️ [Click Here to View the Live Web App!](https://circuit-sandbox-simulator-anmrmcmle6usalcp4lxrk2.streamlit.app/)**

---

## Features

This application includes several dedicated modules:

* **💡 Ohm's Law Calculator:** Quickly solve for voltage, current, or resistance in basic DC circuits.
* **⚡ AC Series RLC Circuit Analyzer:** A comprehensive tool that calculates impedance, phase angle, power factor, and resonance. It also provides an interactive plot of the voltage and current waveforms.
* **📊 RC Low-Pass Filter Analyzer:** Design and analyze a simple low-pass filter. The tool calculates the cutoff frequency and generates a professional Bode plot of the magnitude response.
* **🔌 BJT Common-Emitter Amplifier:** Perform DC Q-point and AC small-signal analysis on a standard voltage-divider biased BJT amplifier.
* **🤖 Digital Logic Gate Simulator:** A simple simulator for basic logic gates including AND, OR, NAND, NOR, XOR, and NOT.

## Technologies Used

* **Python**: The core programming language.
* **Streamlit**: For creating and deploying the interactive web interface.
* **NumPy**: For numerical calculations and array manipulation.
* **Matplotlib**: For generating the plots in the AC RLC and RC Filter modules.

## How to Run Locally

1.  Clone this repository.
2.  Create and activate a virtual environment:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```
3.  Install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```
4.  Run the Streamlit application:
    ```bash
    streamlit run app.py
    ```
