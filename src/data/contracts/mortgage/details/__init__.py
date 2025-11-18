from . import monthly, upfront
from typing import TypedDict
import numpy as np

class General(TypedDict):
    remaining_periods: np.ndarray
    installment_number: np.ndarray
    exposure: np.ndarray
    LTV: np.ndarray

class Monthly(TypedDict):
    base: monthly.Base
    additional: monthly.Additional
    TOTAL: np.ndarray

class Upfront(TypedDict):
    base: upfront.Base
    additional: upfront.Additional
    TOTAL: int