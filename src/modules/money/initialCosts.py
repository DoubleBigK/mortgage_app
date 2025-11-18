import numpy as np
from modules import utils

def calculate_commission(mortgage_amount: float, commission_rate: float) -> float:
    return utils.compute_proportional_cost(mortgage_amount, commission_rate)

def calculate_initial_insurance_fee(mortgage_amount: float, initial_insurance_rate: float) -> float:
    return utils.compute_proportional_cost(mortgage_amount, initial_insurance_rate)

def full_result(# region
        mortgage_amount: float,
        commission_rate: float,
        initial_insurance_rate: float,
        appraisal_fee: float) -> dict :
    return {
        "commission": calculate_commission(commission_rate, mortgage_amount),
        "initial_insurance": calculate_initial_insurance_fee(mortgage_amount, initial_insurance_rate),
        "appraisal": appraisal_fee
        }
# endregion

