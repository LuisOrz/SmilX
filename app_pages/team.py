"""Team · the people behind SmilX / TokenSMILES."""
from content import TEAM, INSTITUTION, WEB_DESIGNERS
from ui.components import html, page_header, img_uri, esc, gap

page_header(
    "Team",
    'The people behind <span class="grad">SmilX</span>',
    f"The SmilX / TokenSMILES project is developed by a multidisciplinary team at the "
    f"<b>{esc(INSTITUTION)}</b>, working at the intersection of computational chemistry, "
    "cheminformatics and scientific software.",
)

SCHOLAR_SVG = ('<svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
               '<path d="M12 3 1 9l11 6 9-4.91V17h2V9L12 3zm-6.82 9.5L5 16.5c0 1.93 3.13 3.5 7 3.5s7-1.57 '
               '7-3.5l-.18-4-6.82 3.72-6.82-3.72z"/></svg>')
LINKEDIN_SVG = ('<svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
                '<path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9h4v12H3zM9 9h3.8v1.7h.05c.53-1 '
                '1.83-2.05 3.77-2.05C20.6 8.65 21 11.1 21 14.3V21h-4v-5.9c0-1.4-.03-3.2-1.95-3.2-1.96 0-2.25 '
                '1.52-2.25 3.1V21H9z"/></svg>')


def member_card(m: dict, i: int) -> str:
    return f"""
<div class="card member fade d{i % 3 + 1}">
  <div class="top">
    <img src="{img_uri(m['image'])}" alt="Photo of {esc(m['name'])}" loading="lazy">
    <div><h4>{esc(m['name'])}</h4><div class="role">{esc(m['role'])}</div></div>
  </div>
  <p>{esc(m['desc'])}</p>
  <div class="links">
    <a class="btn-link" href="{m['scholar']}" target="_blank" rel="noopener">{SCHOLAR_SVG} Scholar</a>
    <a class="btn-link ghost" href="{m['linkedin']}" target="_blank" rel="noopener">{LINKEDIN_SVG} LinkedIn</a>
  </div>
</div>"""


html('<div class="grid c3">' + "".join(member_card(m, i) for i, m in enumerate(TEAM)) + "</div>")

gap()
html(f"""
<div class="card fade" style="display:flex;gap:1rem;align-items:center;flex-wrap:wrap">
  <div class="icon-badge green" style="margin:0">UI</div>
  <div><h4>Web design &amp; development</h4><p>{esc(WEB_DESIGNERS)}</p></div>
</div>""")
