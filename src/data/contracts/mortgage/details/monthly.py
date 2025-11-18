from typing import TypedDict
import numpy as np

class Base(TypedDict):
    capital: np.ndarray
    intrest: np.ndarray
    prepayment: np.ndarray
    risk_premium: np.ndarray
    TOTAL: np.ndarray


class Additional(TypedDict):
    insurance: np.ndarray
    card: np.ndarray
    other: np.ndarray
    TOTAL: np.ndarray