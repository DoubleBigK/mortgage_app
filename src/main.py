import streamlit as st

from app.config import configure_streamlit
from pages import credits_page, dashboard, dummy_page
from state.state import initialize

configure_streamlit()
initialize()

pg = st.navigation(
    {
        "Nawigacja": [
            st.Page(
                dummy_page.render,
                title="Mieszkania",
                icon="🏢",
                url_path="mieszkania",
                default=True,
            ),
            st.Page(
                credits_page.render,
                title="Kredyty",
                icon="💳",
                url_path="kredyty",
            ),
            st.Page(
                dashboard.render,
                title="Kalkulator",
                icon="🧮",
                url_path="kalkulator",
            ),
        ]
    },
    position="sidebar",
)

pg.run()
