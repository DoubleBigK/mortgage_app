from typing import Any
import numpy as np
import streamlit as st


def int_to_roman(num: int) -> str:
    if not 1 <= num <= 3999:
        raise ValueError("Number must be in 1–3999 range")

    values = [
        1000,
        900,
        500,
        400,
        100,
        90,
        50,
        40,
        10,
        9,
        5,
        4,
        1
    ]
    symbols = [
        "M",
        "CM",
        "D",
        "CD",
        "C",
        "XC",
        "L",
        "XL",
        "X",
        "IX",
        "V",
        "IV",
        "I"
    ]
    result = []
    for v, s in zip(values, symbols):
        while num >= v:
            result.append(s)
            num -= v

    return "".join(result)

def set_in_state(value: float,*keys)->None:
    if not keys:
        raise ValueError("Podaj przynajmniej jeden klucz")
    d = st.session_state
    for key in keys[:-1]:
        if key not in d or not isinstance(d[key], dict):
            d[key] = {}
        d = d[key]
    d[keys[-1]] = value

def get_from_state(*keys: str, default: Any = None) -> Any:
    if not keys:
        return st.session_state
    d: Any = st.session_state
    for key in keys:
        if key not in d:
            return default
        d = d[key]
    return d

def compute_proportional_cost(base_amount: float, rate: float) -> float:
    return round(base_amount * rate, 2)

def compute_proportional_cost_cashflow(# region
        base_amount_arr: np.ndarray,
        rate_arr: np.ndarray,
        extend_value: float = None
        ) -> np.ndarray:
    if len(base_amount_arr) < len(rate_arr):
        raise ValueError(f"""base_amount_arr must be at least same lenght as rate_arr.
                            base_amount_arr: {base_amount_arr},
                            rate_arr: {rate_arr}
                            """
                         )
    return multiply_uneven_arrays(base_amount_arr,rate_arr,extend_value).round(2)
# endregion

def get_last_from_arr(arr: np.ndarray, index: int) -> Any:
    try:
        if arr.size == 0:
            return 0
        if len(arr) > index:
            return arr[index]
        else:
            return arr[-1]
    except:
        raise ValueError(f"{arr}, {index}, {len(arr)}, {len(arr) > index}")

def multiply_uneven_arrays(arr1: np.ndarray, arr2: np.ndarray, extend_value: float = None)-> np.ndarray:
    longer = arr1 if len(arr1) > len(arr2) else arr2
    shorter = arr1 if len(arr1) <= len(arr2) else arr2
    if shorter.size == 0:
        default = 0
    else:
        default = shorter[-1]
    extend_value = np.array([extend_value if extend_value else default]*(len(longer)-len(shorter)))
    shorter = np.concatenate([shorter, extend_value], axis=0)
    return longer * shorter

def format_pln(x: float) -> str:
    return f"{x:,.0f}".replace(",", " ") + " zł"

def format_pln_full(x: float) -> str:
    """Pełna liczba z grupowaniem tysięcy."""
    sign = "-" if x < 0 else ""
    n = abs(x)
    s = f"{n:,.0f}".replace(",", " ")
    return f"{sign}{s} zł"

def _format_polish_decimal(value: float, digits: int = 1) -> str:
    s = f"{value:.{digits}f}".rstrip("0").rstrip(".")
    return s.replace(".", ",")

def format_pln_compact(x: float) -> str:
    sign = "-" if x < 0 else ""
    n = abs(x)

    if n < 100_000:
        body = f"{n:,.0f}".replace(",", " ")
    elif n < 1_000_000:
        body = _format_polish_decimal(n / 1_000, 1) + " k"
    elif n < 1_000_000_000:
        body = _format_polish_decimal(n / 1_000_000, 2) + " M"
    else:
        body = _format_polish_decimal(n / 1_000_000_000, 2) + " mld"

    return f"{sign}{body} zł"

def format_to_percentage(value: float) -> str:
    sign = "-" if value < 0 else ""
    return f"{value*100:.2f}%"
def last_or_default(arr: np.ndarray, default=None):
    return arr[-1] if arr.size else default