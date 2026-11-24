"""
Isomer zoom dialog
------------------
Lives in the main Streamlit document (not inside the grid iframe) so it can
float over the page. The grid iframe calls `window.parent.smilxShowIsomer()`
with the RDKit-computed info of one isomer and a large SVG drawn by RDKit.js.
Known-compound data comes from PubChem (PUG-REST, queried by InChIKey).

Markup/behaviour live in ui/static/isomer_modal.{css,js} and grid_hooks.js.
"""
from ui.theme import css, js_file, read_static


def inject_modal() -> None:
    css("isomer_modal.css")
    js_file("isomer_modal.js")


def grid_header(payload_json: str) -> str:
    """<script> block injected into the mols2grid iframe."""
    body = read_static("grid_hooks.js").replace("__DATA__", payload_json.replace("</", "<\\/"))
    return f"<script>\n{body}\n</script>"
