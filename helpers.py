# helpers.py
# Contains utility functions for user input and parsing.

from typing import Optional

def parse_engineering_notation(val_str: str) -> Optional[float]:
    """
    Parses a string with engineering suffixes into a float.
    Returns None if the string is not a valid number.
    
    Examples:
    "10k" -> 10000.0
    "1u"  -> 0.000001
    """
    val_str = val_str.strip()
    suffixes = {
        'p': 1e-12, 'n': 1e-9, 'u': 1e-6, 'm': 1e-3,
        'k': 1e3,   'M': 1e6, 'G': 1e9
    }
    if not val_str:
        return None
    
    suffix = val_str[-1]
    if suffix in suffixes:
        num_part = val_str[:-1]
        try:
            return float(num_part) * suffixes[suffix]
        except (ValueError, TypeError):
            return None
    try:
        return float(val_str)
    except ValueError:
        return None

def get_float(prompt: str, allow_blank: bool = False, default: Optional[float] = None) -> Optional[float]:
    """
    Gets a float from the user, with support for engineering notation.
    """
    while True:
        val_str = input(prompt)
        if allow_blank and val_str.strip() == "":
            return default
        
        parsed_val = parse_engineering_notation(val_str)
        if parsed_val is not None:
            return parsed_val
        else:
            print("Invalid input. Please enter a number (e.g., 100, 10k, 2.2m, 1u).")

def get_binary_input(prompt: str) -> int:
    """Gets a binary (0 or 1) input from the user."""
    while True:
        val = input(prompt)
        if val in ['0', '1']:
            return int(val)
        print("Invalid input. Please enter 0 or 1.")