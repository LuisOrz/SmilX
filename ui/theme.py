"""
SmilX design system loader
--------------------------
The look of the site lives in plain files under ui/static/:

    smilx.css         Material-dark theme in the SmilX palette (all widgets)
    fab.js            floating "scroll" button
    isomer_modal.*    isomer zoom dialog
    grid_hooks.js     hooks injected into the mols2grid iframe

They are read from disk on every rerun (cached by modification time), so
editing a style takes effect on the next page load, without restarting
Streamlit. Python modules, by contrast, stay cached in memory until the
server restarts; keeping the styles out of Python avoids serving a stale look.
"""
import base64
import os

import streamlit as st

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
WEB_VERSION = "2.6"

_cache: dict[str, tuple[float, str]] = {}


def read_static(name: str) -> str:
    path = os.path.join(STATIC_DIR, name)
    mtime = os.path.getmtime(path)
    hit = _cache.get(path)
    if hit and hit[0] == mtime:
        return hit[1]
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    _cache[path] = (mtime, text)
    return text


def css(name: str) -> None:
    st.html(f"<style>\n{read_static(name)}\n</style>")


def _js(body: str) -> str:
    """Ship JavaScript as base64 so Streamlit's HTML sanitizer cannot alter it."""
    b64 = base64.b64encode(body.encode("utf-8")).decode()
    return ("<script>eval(new TextDecoder('utf-8').decode("
            f"Uint8Array.from(atob('{b64}'), c => c.charCodeAt(0))))</script>")


def run_js(script: str) -> None:
    """Run a JS snippet in the page. Accepts code with or without <script> tags."""
    body = script.strip()
    if body.startswith("<script>") and body.endswith("</script>"):
        body = body[len("<script>"):-len("</script>")]
    st.html(_js(body), unsafe_allow_javascript=True)


def js_file(name: str) -> None:
    run_js(read_static(name))


def inject_theme() -> None:
    css("smilx.css")
    js_file("fab.js")
