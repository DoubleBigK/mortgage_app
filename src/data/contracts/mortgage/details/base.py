from typing import TypedDict, List, Tuple
import numpy as np

class CashFlows(TypedDict):
    exposure: np.ndarray
    capital_installment: np.ndarray
    intrest_installment: np.ndarray

class Upfront(TypedDict):
    commission: int
    appraisal: int
    annex: int
    other: int