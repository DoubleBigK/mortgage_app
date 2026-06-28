import streamlit as st

from modules.money import cashflows, summaries, upfront
import viz


def render():
    mortgage_name = "main_mortgage"
    mortgage = st.session_state[mortgage_name]

    if mortgage["settings"]["duration"] <= 0:
        st.info("Wprowadź dane kredytu na pierwszej stronie, żeby zobaczyć wykresy.")
        return

    cashflows.calculate_all(mortgage_name)
    upfront.calculate_all(mortgage_name)
    summaries.calculate_all(mortgage_name)

    st.header("Wykresy")
    viz.mortgage.cashflows(mortgage_name)


if __name__ == "__main__":
    render()
