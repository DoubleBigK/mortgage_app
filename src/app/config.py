from dataclasses import dataclass, asdict
import streamlit as st

@dataclass(frozen=True)
class AppConfig:

    layout: str = "wide"
    initial_sidebar_state: str = "expanded"


DEFAULT_APP_CONFIG = AppConfig()

def configure_streamlit(config: AppConfig = DEFAULT_APP_CONFIG, **overrides) -> None:
    """Ustawia globalny config Streamlita (raz, w mainie)."""
    import streamlit as st
    # st.set_option("logger.level", "error")
    data = asdict(config) | overrides
    st.set_page_config(**data)

