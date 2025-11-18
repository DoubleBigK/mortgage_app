from . import mortgage
from typing import TypedDict

class Mortgage(TypedDict):
    settings: mortgage.Settings
    base_price: mortgage.Details
    reductions: mortgage.Details
    final_price: mortgage.Details
