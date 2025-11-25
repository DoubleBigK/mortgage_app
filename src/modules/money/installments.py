from .. import utils
def equal_capital(# region
        exposure: float,
        monthly_intrest_rate: float,
        remaining_periods: int
        ) -> float:
        return round(exposure * monthly_intrest_rate / ((1 + monthly_intrest_rate) ** remaining_periods - 1), 2)
# endregion

def decreasing_capital(# region
        exposure: float,
        remaining_periods: int
        ) -> float:

    return round(exposure / remaining_periods, 2)
# endregion

def calculate_capital(# region
        exposure : float,
        remaining_periods: int,
        installment_type : str,
        monthly_intrest_rate: float,
) -> float:
    if installment_type == "fixed":
        return equal_capital(# region
                    exposure=exposure,
                    monthly_intrest_rate=monthly_intrest_rate,
                    remaining_periods=remaining_periods
                    )# endregion
    elif installment_type == "decreasing":
        return decreasing_capital(# region
                    exposure=exposure,
                    remaining_periods=remaining_periods
                )# endregion
    else:
        raise ValueError(f"Unknown installment type: {installment_type}.\nShould be either fixed or equal.")
# endregion

def calculate_intrest(# region
        exposure: float,
        monthly_intrest_rate: float,
) -> float:
    return round(exposure * monthly_intrest_rate, 2)
# endregion



