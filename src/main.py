import streamlit as st
from app.config import configure_streamlit
from state.state import initialize
configure_streamlit()
initialize()
pg = st.navigation(
    {
        "Podstawowe operacje": [
            st.Page(
                page = "pages/input_page.py",
                title="Wprowadź dane",
                icon="🏠",
            )
        ],
        "Informacje": [
            st.Page(
                page = "pages/about.py",
                title="O aplikacji",
                icon="ℹ️",
            )
        ]

    }
)

pg.run()