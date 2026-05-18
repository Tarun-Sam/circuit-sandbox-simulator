# Circuit Tutor

Circuit Tutor is a Streamlit-based circuit learning and analysis app for common electronics topics such as Ohm's law, RC filters, AC RLC behavior, BJT amplifiers, op-amp gain, and digital logic simulation.

## Requirements

- Python 3.10+
- `streamlit`
- `numpy`
- `matplotlib`

## Run Locally

```bash
pip install -r requirements.txt
python src/main.py
```

## Project Structure

- `src/main.py`: Streamlit entry point
- `src/ui/home.py`: home page
- `src/ui/pages/`: simulator and calculator pages
- `src/utils/helpers.py`: shared parsing and validation helpers
- `assets/icon.ico`: app icon
