from . import price_reduction
from modules.utils import get_from_state as gfs
import streamlit as st

def get_commission(# region
        extended: bool,
        mortgage_amount: float,
        commission_rate,
        discounts,
        products,
        **kwargs
) -> float:
    if extended:
        commission_discount = price_reduction.commission(discounts, products)
        commission_rate = max(0, commission_rate - commission_discount)
    return int(commission_rate * mortgage_amount)
# endregion

def get_additional_cost(mortgage_amount, products, **kwargs) -> float:
    def _calculate_cost():
        if use:
            if price_type == "% kwoty kredytu":
                return int(price * mortgage_amount / 100)
            elif price_type == "zł/100k/msc salda":
                return int(price * 12)
        return 0
    result = 0
    for price_type, price, _, _, use in products:
        result += _calculate_cost()
    return result

def calculate_all(mortgage_name: str):
    settings = gfs(mortgage_name, "settings")
    appraisal, annex, other = settings["upfront"]
    st.session_state[mortgage_name]["details"]["base"]["upfront"] = {
    "commission": get_commission(extended=False, **settings),
    "appraisal": appraisal,
    "annex": annex,
    "other": other,
    }

    st.session_state[mortgage_name]["details"]["extended"]["upfront"] = {
    "commission": get_commission(extended=True, **settings),
    "appraisal": appraisal,
    "annex": annex,
    "other": other,
    "additional_cost": get_additional_cost(**settings),
    }
