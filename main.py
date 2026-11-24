"""
SmilX · grammar-constrained chemical space explorer
Entry point: `streamlit run main.py`
"""
import os
import sys

import streamlit as st

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ── Never run with stale code ──────────────────────────────────────────────
# Streamlit re-executes page scripts on every run, but modules they import
# (ui/, content.py, smilx_*.py …) stay cached in memory until the server
# restarts. After a redeploy that mixes new pages with old modules and fails
# with ImportError. Each run checks the project's own modules against their
# files on disk and, if any changed, drops them all so they import fresh.
def _project_modules():
    for name, mod in list(sys.modules.items()):
        path = getattr(mod, "__file__", None) or ""
        if name != "__main__" and path.startswith(BASE_DIR + os.sep):
            yield name, mod, path


def _mtime(path):
    try:
        return os.path.getmtime(path)
    except OSError:
        return None


if any(getattr(m, "_smilx_mtime", None) != _mtime(p) for _, m, p in _project_modules()):
    for _name, _mod, _path in list(_project_modules()):
        sys.modules.pop(_name, None)

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

# Remember which file version each project module was loaded from
for _name, _mod, _path in _project_modules():
    try:
        _mod._smilx_mtime = _mtime(_path)
    except Exception:
        pass
