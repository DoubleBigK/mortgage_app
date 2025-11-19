from typing import TypedDict, List, Tuple

class Basic(TypedDict):
    property_value: int
    down_payment: int
    mortgage_amount: int
    LTV: float
    annual_intrest_rate: float
    commission_rate: float
    duration: int
    installment_type: str
    risk_premium: float

class Additional(TypedDict):
    prepayments: List[Tuple[str, int|float, int, int]]
    upfront: List[Tuple[float, int, int]]
    discounts: List[Tuple[float, float, bool]]
    products: List[Tuple[int|float, float, float, bool]]
