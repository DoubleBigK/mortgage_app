import numpy as np
import streamlit as st


def calculate_all(mortgage_name):
    mrt_dict = st.session_state[mortgage_name]
    base = mrt_dict["details"]["base"]["cashflows"]
    mrt_dict["summaries"]["base_total_monthly_payment"] = (base["capital_installment"] + base["intrest_installment"]).astype(int)
    extended = mrt_dict["details"]["extended"]["cashflows"]
    mrt_dict["summaries"]["extended_total_monthly_payment"] = (extended["capital_installment"] + extended[
       "intrest_installment"] + extended["prepayments"] + extended["additional_costs"]).astype(int)
