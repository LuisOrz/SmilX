"""
SmilX · grammar-constrained chemical space explorer
Entry point: `streamlit run main.py`
"""
import os

import streamlit as st

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(
    page_title="SmilX · TokenSMILES isomer explorer",
    page_icon=os.path.join(BASE_DIR, "assets", "favicon.png"),
    layout="wide",
    initial_sidebar_state="collapsed",
)

from ui.theme import inject_theme  # noqa: E402
from ui.components import render_nav, render_footer  # noqa: E402

PAGES = [
    st.Page("app_pages/explore.py", title="Explore", url_path="explore", default=True),
    st.Page("app_pages/about.py", title="About", url_path="about"),
    st.Page("app_pages/publications.py", title="Publications", url_path="publications"),
    st.Page("app_pages/cite.py", title="How to cite", url_path="cite"),
    st.Page("app_pages/team.py", title="Team", url_path="team"),
    st.Page("app_pages/support.py", title="Support", url_path="support"),
]

# Hidden built-in menu: our own navbar drives the same router, so switching
# pages never reloads the browser and session state (results, inputs) survives.
current = st.navigation(PAGES, position="hidden")

inject_theme()
render_nav(PAGES, current)
current.run()
render_footer()
