from . import details
from typing import TypedDict, List, Tuple
import numpy as np

class Settings(TypedDict):
    property_value: int
    down_payment: int
    mortgage_amount: int
    LTV: float
    annual_intrest_rate: float
    commission_rate: float
    duration: int
    installment_type: str
    risk_premium: float
    prepayments: List[Tuple[str, int | float, int, int]]
    upfront: List[Tuple[float, int, int]]
    discounts: List[Tuple[float, float, bool]]
    products: List[Tuple[int | float, float, float, bool]]

class Details(TypedDict):
    base: details.Base
    extended: details.Extended

class Summaries(TypedDict):
    base_total_monthly_payment: np.ndarray
    extended_total_monthly_payment: np.ndarray