from . import additionalCosts, installments, initialCosts
from modules import utils
import numpy as np

def update(result: dict, **kwargs) -> None:
    for key in kwargs:
        if not key in result:
            result[key] = np.array([])
        result[key] = np.append(result[key], kwargs[key])

def calculate_base_general(#region
        mortgage_amount: float,
        installment_type: str,
        intrest_rates_arr: np.ndarray,
        mortgage_duration: int,
        prepayments_arr: np.ndarray = np.array([])) -> dict:
    result = dict()
    result["general"] = {}
    result["base"] = {}
    exposure = mortgage_amount
    for index in range(mortgage_duration):
        remaining_periods = mortgage_duration - index
        intrest_rate_period = utils.get_last_from_arr(intrest_rates_arr,index)
        update(# region
            result=result["general"],
            remaining_periods=remaining_periods,
            installment_number=index+1,
            exposure=exposure,
            intrest_rate_period=intrest_rate_period
            )# endregion
        capital_installment = installments.calculate_capital(installment_type, exposure, intrest_rate_period,remaining_periods)
        intrest_installment = installments.calculate_intrest(exposure, intrest_rate_period)
        prepayment = utils.get_last_from_arr(prepayments_arr, index)
        update(# region
            result=result["costs"]["monthly"]["base"],
            capital=capital_installment,
            intrest=intrest_installment,
            prepayment=prepayment)
        # endregion
        exposure = round(exposure - capital_installment - prepayment, 2)
    if exposure != 0:
        raise ValueError(f"Last element of result['exposure'] = {exposure} but should be equal to 0")
    if abs(sum(result["payments"]["capital"]) + sum(result["payments"]["prepayment"]) - mortgage_amount) > 0.001:
        raise ValueError(f'sum of capital payments = {sum(result["payments"]["capital"]) + sum(result["payments"]["prepayment"])} but should be equal to {mortgage_amount}')
    return result
# endregion

# def calculate_summary_cashflows(cashflow: dict) -> dict:
#     monthly_fees = sum(cashflow["additional_costs"]["monthly_fees"].values())
#     cost_of_capital = cashflow["payments"]["intrest"] + monthly_fees
#     cost_of_capital[0] += sum(cashflow["additional_costs"]["initial"].values())
#     expected_installment_payment = cashflow["payments"]["capital"] + cashflow["payments"]["intrest"]
#     real_installment_payment = expected_installment_payment + cashflow["payments"]["prepayment"]
#     total_capital_payment = cashflow["payments"]["capital"] + cashflow["payments"]["prepayment"]
#     total_payment = cost_of_capital + cashflow["payments"]["capital"]
#     return {
#         "monthly_fees": monthly_fees,
#         "cost_of_capital": cost_of_capital,
#         "expected_installment_payment": expected_installment_payment,
#         "real_installment_payment": real_installment_payment,
#         "total_capital_payment": total_capital_payment,
#         "total_payment": total_payment,
#     }

def calculate_totals(cashflow: dict) -> dict:
    capital = cashflow["payments"]["capital"].sum()
    intrest = cashflow["payments"]["intrest"].sum()
    prepayment = cashflow["payments"]["prepayment"].sum()
    initial = sum(cashflow["additional_costs"]["initial"].values())
    monthly_fees = cashflow["summary_cashflows"]["monthly_fees"].sum()
    cost_of_capital = cashflow["summary_cashflows"]["cost_of_capital"].sum()
    expected_installment_payment = cashflow["summary_cashflows"]["expected_installment_payment"].sum()
    real_installment_payment = cashflow["summary_cashflows"]["real_installment_payment"].sum()
    total_payment = cashflow["summary_cashflows"]["total_payment"].sum()

    return {
        "capital": capital,
        "intrest": intrest,
        "prepayment": prepayment,
        "initial": initial,
        "monthly_fees": monthly_fees,
        "cost_of_capital": cost_of_capital,
        "expected_installment_payment": expected_installment_payment,
        "real_installment_payment": real_installment_payment,
        "total_payment": total_payment,
    }

def create_entire(# region
        mortgage_amount: float,
        installment_type: str,
        intrest_rates_arr: np.ndarray,
        mortgage_duration: int,
        prepayments_arr: np.ndarray = np.array([]),
        commission_rate: float = 0,
        initial_insurance_rate: float = 0,
        appraisal_fee: float = 0,
        monthly_insurance_rate_arr: np.ndarray = np.array([]),
        yearly_credit_card_cost: float = 0,
        **kwargs
        ) -> dict:
    result = dict()
    cashflow = calculate_base(# region
        mortgage_amount=mortgage_amount,
        installment_type=installment_type,
        intrest_rates_arr=intrest_rates_arr,
        mortgage_duration=mortgage_duration,
        prepayments_arr=prepayments_arr
    )  # endregion
    exposure_cashflow = cashflow["general"]["exposure"]
    cashflow["costs"]["initial_costs"] = initialCosts.full_result(
                                        mortgage_amount,
                                        commission_rate=commission_rate,
                                        initial_insurance_rate=initial_insurance_rate,
                                        appraisal_fee=appraisal_fee,
                                        )# endregion
    cashflow["costs"]["monthly"]["base"] = additionalCosts.calculate_total_additional_costs(#region
                                        exposure_cashflow=exposure_cashflow,
                                        commission_rate=commission_rate,
                                        initial_insurance_rate=initial_insurance_rate,
                                        appraisal_fee=appraisal_fee,
                                        monthly_insurance_rate_arr=monthly_insurance_rate_arr,
                                        yearly_credit_card_cost=yearly_credit_card_cost)# endregion
    cashflow["summary_cashflows"] = calculate_summary_cashflows(cashflow,)
    cashflow["TOTALS"] = calculate_totals(cashflow)

    return cashflow
# endregion