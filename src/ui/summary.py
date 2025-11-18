import streamlit as st
from modules import utils

def number_decomposition(component_dict: dict):
    with st.container(border=True):
        if len(component_dict["names"]) != len(component_dict["values"]):
            raise ValueError(f'Number of components does not match number of values: {component_dict["names"]}, {component_dict["values"]}')
        function = component_dict["function"] if component_dict["function"] is not None else lambda x: x
        total = sum(component_dict["values"])
        _, c2, _ = st.columns([1, 2, 1])
        with c2:
            st.markdown(
                f"""
                <div style="
                    display:flex;
                    flex-direction:column;
                    align-items:center;
                ">
                    <div style="
                        font-size:1.1rem;
                        color:#6b7280;
                        white-space:nowrap;
                    ">
                        {component_dict["total_name"]}
                    </div>
                    <div style="
                        font-size:2rem;
                        font-weight:600;
                        margin-top:0.25rem;
                        white-space:nowrap;
                    ">
                        {function(total)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        cols = st.columns(len(component_dict["names"]))

        for col, label, value in zip(cols, component_dict["names"], component_dict["values"]):
            with col:
                st.markdown(
                    f"""
                    <div style="
                        display:flex;
                        flex-direction:column;
                        align-items:center;
                        text-align:center;
                    ">
                        <div style="font-size:1.2rem;line-height:.8;">
                            ⬆️
                        </div>
                        <div style="
                            font-size:0.8rem;
                            color:#6b7280;
                            margin-top:0.25rem;
                            white-space:nowrap;
                        ">
                            {label}
                        </div>
                        <div style="
                            font-size:1.2rem;
                            font-weight:600;
                            margin-top:0.1rem;
                            white-space:nowrap;
                        ">
                            {function(value)}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

def mortgage_display(**mortgage):
    col1, col2, col3 = st.columns(3)
    with col1:
        component_dict = {
            "total_name": "Koszty początkowe",
            "function": utils.format_pln_compact,
            "names": ["Bazowe", "Ubezp. początkowe", "Wycena"],
            "values": [
                mortgage["details"]["upfront"]["initial"]["commission"],
                mortgage["details"]["upfront"]["initial"]["initial_insurance_fee"],
                mortgage["details"]["upfront"]["initial"]["appraisal_fee"]
            ],
            }
        number_decomposition(component_dict)

    with col2:
        component_dict = {
            "total_name": "Koszty miesięczne (I miesiąc)",
            "function": utils.format_pln_compact,
            "names": ["Rata", "Nadpłata", "Pozostałe koszty"],
            "values": [
                st.session_state["cashflow"]["summary_cashflows"]["expected_installment_payment"][0],
                st.session_state["cashflow"]["payments"]["prepayment"][0],
                st.session_state["cashflow"]["summary_cashflows"]["monthly_fees"][0],
                ],
            }
        number_decomposition(component_dict)

    with col3:
        component_dict = {
            "total_name": "Koszty całkowite",
            "function": utils.format_pln_compact,
            "names": ["Odsetki", "Początkowe", "Pozostałe"],
            "values": [
                st.session_state["cashflow"]["TOTALS"]["intrest"],
                st.session_state["cashflow"]["TOTALS"]["initial"],
                st.session_state["cashflow"]["TOTALS"]["monthly_fees"],
            ],
        }
        number_decomposition(component_dict)