import streamlit as st
import ui
from modules.money import cashflows, upfront, summaries
import viz
def render():
    ui.inputs.mortgage.standard("main_mortgage")
    cashflows.calculate_all("main_mortgage")
    upfront.calculate_all("main_mortgage")
    summaries.calculate_all("main_mortgage")
    ui.summary.mortgage_display("main_mortgage")
    viz.mortgage.cashflows("main_mortgage")
    #st.write(st.session_state["main_mortgage"])


if __name__ == "__main__":
    render()