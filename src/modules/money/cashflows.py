from .installments import calculate_capital, calculate_intrest
from . import price_reduction
import numpy as np
from modules.utils import get_from_state as gfs
import streamlit as st
from data import functions, contracts

def get_monthly_intrest_rate(# region
        exposure: float,
        extended: bool,
        property_value: float,
        risk_premium: float,
        annual_intrest_rate: float,
        discounts,
        products,
        **kwargs
) -> float:
    if exposure / property_value > 0.8:
        annual_intrest_rate += risk_premium
    if extended:
        intrest_discount = price_reduction.intrest(discounts, products)
        return max(0, (annual_intrest_rate - intrest_discount) / 12)
    else:
        return annual_intrest_rate / 12
# endregion

def get_prepayment(# region
        exposure: float,
        capital_installment: float,
        intrest_installment: float,
        additional_cost: float,
        prepayments: float,
        installment_numer: int
) -> float:
    def _find_settings():
        for _price_type, _price, start, end in prepayments:
            if start <= installment_numer <= end:
                return _price_type, _price
        return None, None
    def _find_prepayment() -> float:
        if price_type == "Kwota nadpłaty":
            prep = price
        elif price_type == "Procent raty":
            prep = round(price * base_installment/100, 2)
        elif price_type == "Cała rata":
            prep = max(0, price-base_installment)
        else:
            raise ValueError(f"Unknown type {price_type}")
        return min(prep, exposure)
    base_installment = capital_installment + intrest_installment + additional_cost
    price_type, price = _find_settings()
    if price_type:
        return _find_prepayment()
    return 0
# endregion

def get_additional_cost(exposure, products):
    def _calculate_cost():
        if use:
            if price_type == "zł/100k/msc salda":
                return round(price * exposure / 100_000, 2)
            elif price_type == "zł/msc":
                return price
        return 0
    result = 0
    for price_type, price, _, _, use in products:
        result += _calculate_cost()
    return result

def calculate_all(#region
        mortgage_name: str
):
    def _init():
        st.session_state[mortgage_name]["details"]["base"]["cashflows"]["exposure"] = np.array([mortgage_amount])
        st.session_state[mortgage_name]["details"]["extended"]["cashflows"]["exposure"] = np.array([mortgage_amount])
    def _clean():
        st.session_state[mortgage_name]["details"] = functions.build_template(contracts.mortgage.Details)
    def _details(kind: str):
        extended = kind == "extended"
        cashflows = gfs(mortgage_name, "details", kind, "cashflows")
        exposure = cashflows["exposure"][-1]
        if exposure <= 0.005:
            return
        monthly_intrest_rate = get_monthly_intrest_rate(exposure, extended, **settings)
        capital_installment = calculate_capital(  # region
            exposure,
            remaining_periods,
            installment_type,
            monthly_intrest_rate
        )  # endregion
        intrest_installment = calculate_intrest(  # region
            exposure,
            monthly_intrest_rate
        )  # endregion
        exposure -= capital_installment
        if extended:
            additional_cost = get_additional_cost(exposure, products)
            prepayment = get_prepayment(# region
                exposure,
                capital_installment,
                intrest_installment,
                additional_cost,
                prepayments,
                installment_numer
            )# endregion
            cashflows["prepayments"] = np.append(cashflows["prepayments"], prepayment)
            cashflows["additional_costs"] = np.append(cashflows["additional_costs"], additional_cost)
            exposure -= prepayment
        cashflows["capital_installment"] = np.append(cashflows["capital_installment"], round(capital_installment, 2))
        cashflows["intrest_installment"] = np.append(cashflows["intrest_installment"], round(intrest_installment, 2))
        cashflows["exposure"] = np.append(cashflows["exposure"], round(exposure, 2))
    _clean()
    settings = gfs(mortgage_name, "settings")
    duration = settings["duration"]
    installment_type = settings["installment_type"]
    mortgage_amount = settings["mortgage_amount"]
    prepayments = settings["prepayments"]
    products = settings["products"]
    _init()
    for installment_numer in range(1, duration+1):
        remaining_periods = duration - installment_numer + 1
        _details(kind="base")
        _details(kind="extended")
    # if exposure != 0:
    #     raise ValueError(f"Last element of result['exposure'] = {exposure} but should be equal to 0")
    # if abs(sum(result["payments"]["capital"]) + sum(result["payments"]["prepayment"]) - mortgage_amount) > 0.001:
    #     raise ValueError(f'sum of capital payments = {sum(result["payments"]["capital"]) + sum(result["payments"]["prepayment"])} but should be equal to {mortgage_amount}')
    # return result
# endregion

