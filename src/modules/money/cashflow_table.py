from __future__ import annotations

import pandas as pd


def build_cashflow_table(mortgage: dict) -> pd.DataFrame:
    base = mortgage["details"]["base"]["cashflows"]
    extended = mortgage["details"]["extended"]["cashflows"]

    rows = []
    periods = max(
        len(base["capital_installment"]),
        len(extended["capital_installment"]),
    )

    for month in range(1, periods + 1):
        base_capital = _value_at(base["capital_installment"], month - 1)
        base_interest = _value_at(base["intrest_installment"], month - 1)
        extended_capital = _value_at(extended["capital_installment"], month - 1)
        extended_interest = _value_at(extended["intrest_installment"], month - 1)
        extended_prepayment = _value_at(extended["prepayments"], month - 1)
        extended_additional_cost = _value_at(extended["additional_costs"], month - 1)

        rows.append(
            {
                "Miesiac": month,
                "Bazowe saldo poczatkowe": _value_at(base["exposure"], month - 1),
                "Bazowe rata kapitalowa": base_capital,
                "Bazowe rata odsetkowa": base_interest,
                "Bazowe rata laczna": base_capital + base_interest,
                "Bazowe saldo koncowe": _value_at(base["exposure"], month),
                "Laczne saldo poczatkowe": _value_at(extended["exposure"], month - 1),
                "Laczne rata kapitalowa": extended_capital,
                "Laczne rata odsetkowa": extended_interest,
                "Laczne nadplata": extended_prepayment,
                "Laczne koszty dodatkowe": extended_additional_cost,
                "Laczne rata laczna": (
                    extended_capital
                    + extended_interest
                    + extended_prepayment
                    + extended_additional_cost
                ),
                "Laczne saldo koncowe": _value_at(extended["exposure"], month),
            }
        )

    return pd.DataFrame(rows)


def cashflow_table_to_csv(table: pd.DataFrame) -> bytes:
    return table.to_csv(index=False, sep=";", decimal=",").encode("utf-8-sig")


def _value_at(values, index: int) -> float:
    if len(values) <= index:
        return 0.0
    return round(float(values[index]), 2)
