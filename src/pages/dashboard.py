import streamlit as st

from pages import about, cashflows, charts, input_page


def render():
    data_tab, cashflow_tab, charts_tab, about_tab = st.tabs(
        ["Dane", "Cashflow", "Wykresy", "O aplikacji"]
    )

    with data_tab:
        input_page.render()
    with cashflow_tab:
        cashflows.render()
    with charts_tab:
        charts.render()
    with about_tab:
        about.render()


if __name__ == "__main__":
    render()
