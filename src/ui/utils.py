import streamlit as st

def static_field(text: str):
    st.markdown(
        f"""
        <div style="
            padding: 0.45rem 0.75rem;
            border-radius: 0.5rem;
            background-color: #f0f2f6;
            border: 1px solid #f0f2f6;
            font-size: 0.9rem;
            color: #31333F;
            ">
            {text}
        </div>
        """,
        unsafe_allow_html=True,
    )



def input_number_key_trick(# region
        key: str,
        min_value: int | float,
        max_value: int | float,
        default: int | float = None
) -> None:
    default = default or min_value
    if key not in st.session_state:
        st.session_state[key] = default
    v = st.session_state[key]
    if v < min_value:
        v = min_value
    elif v > max_value:
        v = max_value
    st.session_state[key] = v
# endregion