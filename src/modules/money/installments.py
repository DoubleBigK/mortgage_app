
def equal_capital(# region
        exposure: float,
        intrest_rate_period: float,
        remaining_periods: int
        ) -> float:
        return round(exposure * intrest_rate_period / ((1 + intrest_rate_period) ** remaining_periods - 1), 2)
# endregion

def decreasing_capital(# region
        exposure: float,
        remaining_periods: int
        ) -> float:

    return round(exposure / remaining_periods, 2)
# endregion

def calculate_capital(# region
        installment_type : str,
        exposure : float,
        intrest_rate_period: float,
        remaining_periods : int,
      ) -> float:
        if installment_type == "equal":
            return equal_capital(# region
                        exposure=exposure,
                        intrest_rate_period=intrest_rate_period,
                        remaining_periods=remaining_periods
                        )# endregion
        elif installment_type == "decreasing":
            return decreasing_capital(# region
                        exposure=exposure,
                        remaining_periods=remaining_periods
                    )# endregion
        else:
            raise ValueError(f"Unknown installment type: {installment_type}.\nShould be either decreasing or equal.")
# endregion

def calculate_intrest(# region
        exposure: float,
        intrest_rate_period: float
        ) -> float:
    return round(exposure * intrest_rate_period, 2)
# endregion





