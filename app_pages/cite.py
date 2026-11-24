"""How to cite SmilX / TokenSMILES."""
import streamlit as st

from content import LINKS, CITATION_TEXT, BIBTEX, RIS, ABSTRACT, PUBLICATIONS
from ui.components import html, page_header, section, gap, img_uri, esc

page_header(
    "How to cite",
    'Cite <span class="grad">SmilX</span> in your work',
    "If you use SmilX or the TokenSMILES grammar in your research, please cite the following "
    "publication. It helps us keep the project open and maintained.",
)

paper = next(p for p in PUBLICATIONS if p.get("featured"))
html(f"""
<div class="card featured fade">
  <div class="pub">
    <a href="{LINKS['paper']}" target="_blank" rel="noopener"><img src="{img_uri(paper['cover'])}" alt="Chemical Science cover"></a>
    <div>
      <div class="meta">Chemical Science · 2026 &nbsp;<span class="tagpill green">Primary reference</span></div>
      <h3>{esc(paper['title'])}</h3>
      <p class="au">{esc(paper['authors'])}</p>
      <div class="ref">Chem. Sci. 2026, 17 (3), 1666–1675 · The Royal Society of Chemistry · DOI {esc(paper['doi'])}</div>
      <div class="actions">
        <a class="btn-link" href="{LINKS['paper']}" target="_blank" rel="noopener">Open publication ↗</a>
        <a class="btn-link ghost" href="{LINKS['repo']}" target="_blank" rel="noopener">Software repository ↗</a>
      </div>
    </div>
  </div>
</div>""")

gap()
section("Copy a citation", "Use the copy button in the top-right corner of each block.")
tab_txt, tab_bib, tab_ris = st.tabs(["Text (ACS style)", "BibTeX", "RIS / EndNote"])
with tab_txt:
    st.code(CITATION_TEXT, language=None, wrap_lines=True)
with tab_bib:
    st.code(BIBTEX, language="bibtex")
    st.download_button("⬇  Download .bib", BIBTEX, file_name="smilx_tokensmiles.bib", mime="application/x-bibtex")
with tab_ris:
    st.code(RIS, language=None)
    st.download_button("⬇  Download .ris", RIS, file_name="smilx_tokensmiles.ris", mime="application/x-research-info-systems")

gap()
section("Abstract")
html(f'<div class="card fade"><p style="font-size:.97rem">{esc(ABSTRACT)}</p></div>')

gap()
section("Software & license")
html(f"""
<div class="grid c2 fade">
  <div class="card"><div class="icon-badge">{{ }}</div><h4>Source code</h4>
    <p>The official implementation of the SmilX / TokenSMILES framework is on GitHub.</p>
    <div class="actions" style="margin-top:.8rem"><a class="btn-link" href="{LINKS['repo']}" target="_blank" rel="noopener">github.com/LuisOrz/SmilX ↗</a></div></div>
  <div class="card"><div class="icon-badge green">GPL</div><h4>GNU General Public License v3</h4>
    <p>29 June 2007 · Copyright © 2007 Free Software Foundation. You may use, study, share and modify SmilX under its terms.</p>
    <div class="actions" style="margin-top:.8rem"><a class="btn-link green" href="{LINKS['license']}" target="_blank" rel="noopener">Read the license ↗</a></div></div>
</div>""")
