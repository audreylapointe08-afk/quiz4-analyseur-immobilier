from pathlib import Path

import streamlit as st

from src.ui import inject_global_styles


st.set_page_config(
    page_title="King County Real Estate Lab",
    page_icon=":material/finance_mode:",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_styles()

pages_dir = Path(__file__).parent / "pages"

navigation = st.navigation(
    [
        st.Page(pages_dir / "home.py", title="Accueil", icon=":material/home:"),
        st.Page(pages_dir / "market.py", title="Marche", icon=":material/monitoring:"),
        st.Page(pages_dir / "property_analysis.py", title="Propriete", icon=":material/home_work:"),
        st.Page(pages_dir / "ai_assistant.py", title="Assistant IA", icon=":material/psychology:"),
    ],
    position="sidebar",
)

navigation.run()
