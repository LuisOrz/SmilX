"""Reusable SmilX UI pieces: navbar, page header, footer and image helpers."""
import base64
import html as _html
import os

import streamlit as st

from content import LINKS, INSTITUTION, WEB_DESIGNERS
from ui.theme import WEB_VERSION

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def asset_path(rel: str) -> str:
    return os.path.join(BASE_DIR, rel)


@st.cache_data(show_spinner=False)
def img_uri(rel_path: str) -> str:
    """Return an image as a data: URI (cached), so HTML cards can embed it."""
    path = asset_path(rel_path)
    if not os.path.isfile(path):
        return ""
    ext = os.path.splitext(path)[1].lower().lstrip(".")
    mime = "jpeg" if ext in ("jpg", "jpeg") else ext
    with open(path, "rb") as f:
        return f"data:image/{mime};base64,{base64.b64encode(f.read()).decode()}"


def esc(text: str) -> str:
    return _html.escape(str(text), quote=True)


def html(markup: str) -> None:
    """Render trusted HTML written by this app (never user input unescaped)."""
    st.markdown(markup, unsafe_allow_html=True)


# ── Navbar ──────────────────────────────────────────────────────────────────
def render_nav(pages: list, current) -> None:
    """Fixed top bar. Uses st.page_link so navigation stays inside the same
    Streamlit session: no full reload, results and inputs are kept."""
    with st.container(key="smilx-nav"):
        html(
            f'<div class="smilx-brand"><img src="{img_uri("assets/logo_smilx.png")}" alt="SmilX">'
            f'<span class="tag">TokenSMILES</span></div>'
        )
        for page in pages:
            active = page.url_path == current.url_path
            if active:
                with st.container(key=f"nav-on-{page.url_path or 'home'}"):
                    st.page_link(page, label=page.title)
            else:
                st.page_link(page, label=page.title)


# ── Page header ─────────────────────────────────────────────────────────────
def page_header(eyebrow: str, title_html: str, lead: str = "") -> None:
    html(
        f'<div class="fade"><div class="eyebrow">{esc(eyebrow)}</div>'
        f'<div class="page-title">{title_html}</div>'
        + (f'<p class="page-lead">{lead}</p>' if lead else "")
        + "</div>"
    )


def section(title: str, sub: str = "") -> None:
    html(
        f'<div class="section-title">{esc(title)}</div>'
        + (f'<p class="section-sub">{sub}</p>' if sub else "")
    )


def gap() -> None:
    html('<div class="section-gap"></div>')


# ── Footer ──────────────────────────────────────────────────────────────────
def render_footer() -> None:
    html(f"""
<div class="smilx-footer">
  <div>
    <img src="{img_uri("assets/logo_smilx.png")}" alt="SmilX">
    <p>Grammar-constrained chemical space exploration of isomers with the TokenSMILES framework.</p>
    <p>{esc(INSTITUTION)}</p>
  </div>
  <div>
    <h5>Resources</h5>
    <a href="{LINKS['paper']}" target="_blank" rel="noopener">Chem. Sci. paper ↗</a>
    <a href="{LINKS['repo']}" target="_blank" rel="noopener">Source code on GitHub ↗</a>
    <a href="{LINKS['issues']}" target="_blank" rel="noopener">Report an issue ↗</a>
  </div>
  <div>
    <h5>Related tools</h5>
    <a href="{LINKS['elaya']}" target="_blank" rel="noopener">ELAYA SMILES · 3D structures ↗</a>
    <a href="{LINKS['license']}" target="_blank" rel="noopener">GNU GPL v3 license ↗</a>
  </div>
  <div class="credits">
    <span>© Cinvestav Mérida · Open source under GPL-3.0 · Web v{WEB_VERSION}</span>
    <span>Web design: <b>{esc(WEB_DESIGNERS)}</b></span>
  </div>
</div>
""")
