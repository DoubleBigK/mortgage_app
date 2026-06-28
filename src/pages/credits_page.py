import streamlit as st


def render():
    first_tab, second_tab = st.tabs(["Kredyty 1", "Kredyty 2"])

    with first_tab:
        st.header("Kredyty 1")
        st.write("Pierwsza dummy podstrona kredytów.")
    with second_tab:
        st.header("Kredyty 2")
        st.write("Druga dummy podstrona kredytów.")


if __name__ == "__main__":
    render()
