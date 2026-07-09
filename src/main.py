import streamlit as st

from app.config import configure_streamlit
from pages import apartments_page, credits_page, dashboard, about
from state.state import initialize

configure_streamlit()
initialize()

pg = st.navigation(
    {
        "Nawigacja": [
            st.Page(
                apartments_page.render,
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
            st.Page(
                about.render,
                title="O aplikacji",
                icon="ℹ️",
                url_path="about",
            ),
        ]
    },
    position="sidebar",
)

pg.run()
