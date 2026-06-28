import streamlit as st

from modules.money import cashflow_table, cashflows, summaries, upfront


def render():
    mortgage_name = "main_mortgage"
    mortgage = st.session_state[mortgage_name]

    if mortgage["settings"]["duration"] <= 0:
        st.info("Wprowadź dane kredytu na pierwszej stronie, żeby zobaczyć cashflow.")
        return

    cashflows.calculate_all(mortgage_name)
    upfront.calculate_all(mortgage_name)
    summaries.calculate_all(mortgage_name)

    table = cashflow_table.build_cashflow_table(mortgage)

    st.header("Cashflow")
    st.dataframe(table, use_container_width=True, hide_index=True)
    st.download_button(
        label="Pobierz CSV",
        data=cashflow_table.cashflow_table_to_csv(table),
        file_name="cashflow.csv",
        mime="text/csv",
    )


if __name__ == "__main__":
    render()
