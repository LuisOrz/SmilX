"""Support / Contact · questions, bug reports and feature requests."""
import streamlit as st

from content import LINKS, INSTITUTION
from ui.components import html, page_header, section, gap

page_header(
    "Support & contact",
    'We are here to <span class="grad">help</span>',
    "For questions, feedback, bug reports or collaboration inquiries related to <b>SmilX</b>, "
    "use the channels below.",
)

html(f"""
<div class="grid c3 fade">
  <div class="card"><div class="icon-badge">?</div><h4>General questions</h4>
    <p>Questions about the project, the methodology or the publications. Open an issue on GitHub
    and the development team will reply.</p>
    <div class="actions" style="margin-top:.9rem"><a class="btn-link" href="{LINKS['issues']}" target="_blank" rel="noopener">Ask on GitHub ↗</a></div></div>
  <div class="card"><div class="icon-badge" style="color:#ffb4ad;border-color:rgba(245,103,91,.3);background:rgba(245,103,91,.08)">!</div><h4>Report a bug</h4>
    <p>Something failed or looks wrong? Tell us the formula and mode you used so we can reproduce it.</p>
    <div class="actions" style="margin-top:.9rem"><a class="btn-link" href="{LINKS['new_issue']}" target="_blank" rel="noopener">Report an issue ↗</a></div></div>
  <div class="card"><div class="icon-badge green">+</div><h4>Request a feature</h4>
    <p>Ideas and suggestions for improvement are welcome, from new elements to export formats.</p>
    <div class="actions" style="margin-top:.9rem"><a class="btn-link green" href="{LINKS['new_issue']}" target="_blank" rel="noopener">Suggest a feature ↗</a></div></div>
</div>""")

gap()
c1, c2 = st.columns([1.1, 1], gap="large")
with c1:
    section("What to include in a report", "Reproducible details help us identify and fix issues faster.")
    html("""
<div class="pipeline fade">
  <div class="pipe"><div class="k">01</div><div><b>Molecular formula</b><p>Exactly as you typed it, e.g. <code>C4H8O</code>.</p></div></div>
  <div class="pipe"><div class="k">02</div><div><b>Mode and settings</b><p>Classic or Classic + carbenes, and anything else you changed.</p></div></div>
  <div class="pipe"><div class="k">03</div><div><b>Error message</b><p>Copy the text or attach a screenshot if one appeared.</p></div></div>
  <div class="pipe"><div class="k">04</div><div><b>What you expected</b><p>A short description of the issue and the expected result.</p></div></div>
</div>""")
with c2:
    section("Project")
    html(f"""
<div class="card fade d1">
  <div class="lbl" style="font-family:var(--fm);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)">Software</div>
  <h4 style="margin:.15rem 0 .8rem!important">SmilX · TokenSMILES framework</h4>
  <div class="lbl" style="font-family:var(--fm);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)">Institution</div>
  <p style="margin:.15rem 0 .8rem">{INSTITUTION}</p>
  <div class="lbl" style="font-family:var(--fm);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)">Repository</div>
  <p style="margin:.15rem 0 1rem"><a href="{LINKS['repo']}" target="_blank" rel="noopener">github.com/LuisOrz/SmilX</a></p>
  <div class="actions" style="display:flex;gap:8px;flex-wrap:wrap">
    <a class="btn-link" href="{LINKS['repo']}" target="_blank" rel="noopener">Open repository ↗</a>
    <a class="btn-link green" href="{LINKS['elaya']}" target="_blank" rel="noopener">ELAYA SMILES ↗</a>
  </div>
</div>""")
    gap()
    section("Citation and academic use")
    html('<p>If you use SmilX in academic work, please cite the publication listed in '
         '<b>How to cite</b>.</p>')
    with st.container(key="green-cite"):
        st.page_link("app_pages/cite.py", label="Go to How to cite →")
