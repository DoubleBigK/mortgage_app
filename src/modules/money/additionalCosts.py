import numpy as np
from modules import utils

def calculate_monthly_insurance_cost(exposure_cashflow: np.ndarray, monthly_insurance_rate_arr: np.ndarray) -> np.ndarray:
    return utils.compute_proportional_cost_cashflow(exposure_cashflow, monthly_insurance_rate_arr)

def calculate_monthly_credit_card_cost(mortgage_duration: int, yearly_credit_card_cost: float) -> np.ndarray:
    monthly_credit_card_cost = round(yearly_credit_card_cost / 12, 2)
    return np.array([monthly_credit_card_cost]*mortgage_duration)

def full_result(    # region
        exposure_cashflow: np.ndarray,
        monthly_insurance_rate_arr: np.ndarray,
        yearly_credit_card_cost: float
        ) -> dict :
    mortgage_duration=len(exposure_cashflow)
    return {
        "insurance_cost": calculate_monthly_insurance_cost(exposure_cashflow, monthly_insurance_rate_arr),
        "credit_card_cost": calculate_monthly_credit_card_cost(mortgage_duration, yearly_credit_card_cost)
    }
   # endregion
