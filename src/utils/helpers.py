"""Shared parsing and validation helpers for CLI and Streamlit pages."""

from __future__ import annotations

from math import isfinite
from pathlib import Path
from typing import Optional


SUFFIX_FACTORS = {
    "p": 1e-12,
    "n": 1e-9,
    "u": 1e-6,
    "m": 1e-3,
    "k": 1e3,
    "K": 1e3,
    "M": 1e6,
    "G": 1e9,
    "g": 1e9,
}

ENGINEERING_INPUT_HINT = "Use values like 100, 2.2k, 470u, 1e3."
PROJECT_ROOT = Path(__file__).resolve().parents[2]


def parse_engineering_notation(val_str: str | None) -> Optional[float]:
    """Parse engineering notation into a finite float.

    Supports plain floats and suffixes: p, n, u, m, k, M, G.
    Inputs with unit symbols like "10kΩ" are also accepted.
    """
    if val_str is None:
        return None

    cleaned = (
        val_str.strip()
        .replace("ohm", "")
        .replace("OHM", "")
        .replace("Ohm", "")
        .replace("Ω", "")
        .replace("µ", "u")
    )
    if not cleaned:
        return None

    suffix = cleaned[-1]
    numeric_portion = cleaned
    factor = 1.0
    if suffix in SUFFIX_FACTORS:
        numeric_portion = cleaned[:-1].strip()
        factor = SUFFIX_FACTORS[suffix]

    if not numeric_portion:
        return None

    try:
        value = float(numeric_portion) * factor
    except (TypeError, ValueError):
        return None

    return value if isfinite(value) else None


def parse_required_value(label: str, raw_value: str | None, errors: list[str]) -> Optional[float]:
    """Parse a required numeric field; append a user-facing error on failure."""
    value = parse_engineering_notation(raw_value)
    if value is None:
        errors.append(f"{label}: invalid number. {ENGINEERING_INPUT_HINT}")
    return value


def require_positive(label: str, value: float, errors: list[str], allow_zero: bool = False) -> None:
    """Validate that a value is positive (or non-negative when allow_zero=True)."""
    if allow_zero and value < 0:
        errors.append(f"{label}: must be >= 0.")
    elif not allow_zero and value <= 0:
        errors.append(f"{label}: must be > 0.")


def parallel(r_a: float, r_b: float) -> Optional[float]:
    """Return equivalent resistance of two resistors in parallel."""
    denominator = r_a + r_b
    if denominator == 0:
        return None
    return (r_a * r_b) / denominator


def format_with_unit(value: float, unit: str, precision: int = 3) -> str:
    """Consistent scalar formatting for Streamlit metrics."""
    return f"{value:.{precision}f} {unit}".strip()


def get_asset_path(*parts: str) -> Path:
    """Build an absolute path inside the shared assets directory."""
    return PROJECT_ROOT.joinpath("assets", *parts)


def get_float(prompt: str, allow_blank: bool = False, default: Optional[float] = None) -> Optional[float]:
    """CLI helper: read float with engineering notation."""
    while True:
        val_str = input(prompt)
        if allow_blank and val_str.strip() == "":
            return default

        parsed_val = parse_engineering_notation(val_str)
        if parsed_val is not None:
            return parsed_val
        print(f"Invalid input. {ENGINEERING_INPUT_HINT}")


def get_binary_input(prompt: str) -> int:
    """CLI helper: read binary input (0 or 1)."""
    while True:
        val = input(prompt)
        if val in ["0", "1"]:
            return int(val)
        print("Invalid input. Please enter 0 or 1.")
