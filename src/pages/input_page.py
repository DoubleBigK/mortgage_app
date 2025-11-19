import streamlit as st
import ui

def RENDER():
    ui.inputs.mortgage.standard("main_mortgage")
    st.write(st.session_state["main_mortgage"])
    # inputs.basic_mortgage_params()
    # inputs.additional_products()
    # st.session_state["cashflow"] = cashFlow.create_entire(**st.session_state["mortgage_params"])
    # summary.mortgage_display(**st.session_state)
    # st.write(st.session_state["cashflow"])

if __name__ == "__main__":
    RENDER()