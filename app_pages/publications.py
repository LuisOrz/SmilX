"""Publications · TokenSMILES paper and research that uses SmilX-style isomer exploration."""
import streamlit as st

from content import PUBLICATIONS
from ui.components import html, page_header, img_uri, esc

page_header(
    "Publications",
    'Research behind <span class="grad">SmilX</span>',
    "The TokenSMILES framework and a series of computational studies on interstellar isomers "
    "from the team at Cinvestav Mérida.",
)

years = sorted({p["year"] for p in PUBLICATIONS}, reverse=True)
html(f"""
<div class="chips fade" style="justify-content:flex-start;margin-bottom:1.4rem">
  <span class="chip blue">{len(PUBLICATIONS)} peer-reviewed articles</span>
  <span class="chip">{years[-1]}–{years[0]}</span>
  <span class="chip">Chem. Sci. · J. Phys. Chem. A · ACS Earth Space Chem.</span>
</div>""")


def pub_card(p: dict, delay: int) -> str:
    url = f"https://doi.org/{p['doi']}"
    cover = img_uri(p["cover"])
    tag_cls = "green" if p.get("featured") else ""
    extra = ' featured' if p.get("featured") else ''
    return f"""
<div class="card fade d{min(delay, 3)}{extra}" style="margin-bottom:14px">
  <div class="pub">
    <a href="{url}" target="_blank" rel="noopener"><img src="{cover}" alt="Cover of {esc(p['journal'])}"></a>
    <div>
      <div class="meta">{esc(p['journal'])} · {p['year']} &nbsp;<span class="tagpill {tag_cls}">{esc(p['tag'])}</span></div>
      <h3>{esc(p['title'])}</h3>
      <p class="au">{esc(p['authors'])}</p>
      <div class="ref">{esc(p['ref'])} · DOI {esc(p['doi'])}</div>
      <div class="actions">
        <a class="btn-link" href="{url}" target="_blank" rel="noopener">Open publication ↗</a>
      </div>
    </div>
  </div>
</div>"""


for year in years:
    html(f'<div class="eyebrow" style="margin-top:.8rem">{year}</div>')
    items = [p for p in PUBLICATIONS if p["year"] == year]
    html("".join(pub_card(p, i) for i, p in enumerate(items)))
    if any(p.get("featured") for p in items):
        with st.container(key="green-cite-link"):
            st.page_link("app_pages/cite.py", label="Using SmilX? See how to cite it →")
