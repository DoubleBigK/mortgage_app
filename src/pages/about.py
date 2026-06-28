import streamlit as st

def render():
    st.header("O aplikacji")
    st.markdown(
        """
        Aplikacja służy do ogarnięcia kredytów
        """
    )

RENDER = render


if __name__ == "__main__":
    render()
