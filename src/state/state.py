from __future__ import annotations
import streamlit as st
from typing import Any, TypedDict, get_type_hints
import numpy as np
from data import contracts
from data import functions

def initialize():
    if "main_mortgage" not in st.session_state:
        st.session_state["main_mortgage"] = functions.build_template(contracts.Mortgage)