import streamlit as st

_NAV_LINKS = [
    ("Explore",      "main"),
    ("About",        "1_About"),
    ("Team",         "2_Team"),
    ("Publications", "3_Publications"),
]

def _nav_html(active: str) -> str:
    items = ""
    for label, page in _NAV_LINKS:
        cls = "nav-item nav-active" if label == active else "nav-item"
        href = f"/{page}" if label != "Explore" else "/"
        items += f'<a class="{cls}" href="{href}" target="_self">{label}</a>'
    return f"""
<nav class="smilx-nav">
  <span class="smilx-logo">SmilX</span>
  <button class="nav-burger" onclick="this.closest('nav').classList.toggle('open')" aria-label="Menu">
    <span></span><span></span><span></span>
  </button>
  <div class="nav-links">{items}</div>
</nav>
<div class="nav-spacer"></div>
"""

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;500;600&family=Outfit:wght@300;400;500;600;700;800&display=swap');

:root {
    --bg:          #02040a;
    --surface:     #0b0f1c;
    --surface-2:   #111628;
    --surface-3:   #171d32;
    --border:      rgba(99,123,200,0.13);
    --border-h:    rgba(99,123,200,0.30);
    --accent:      #5b8af5;
    --accent-2:    #7ba3ff;
    --accent-glow: rgba(91,138,245,0.15);
    --accent-dim:  rgba(91,138,245,0.55);
    --green:       #3ecf8e;
    --green-dim:   rgba(62,207,142,0.10);
    --white:       #e8edf8;
    --muted:       #4a5578;
    --r:           8px;
    --r-lg:        14px;
    --nav-h:       52px;
    --fh:          'Outfit', sans-serif;
    --fm:          'IBM Plex Mono', monospace;
    --ease:        0.17s cubic-bezier(.4,0,.2,1);
}

#MainMenu, header, footer,
[data-testid="stHeader"],
[data-testid="stDecoration"],
[data-testid="stToolbar"],
section[data-testid="stSidebar"] {
    display: none !important;
    visibility: hidden !important;
}

html, body,
.stApp, .stApp > div,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"] {
    background: var(--bg) !important;
    color: var(--white) !important;
    font-family: var(--fh) !important;
}

div[data-testid="block-container"],
.stMainBlockContainer,
.main .block-container {
    padding-top:   0 !important;
    padding-left:  1.25rem !important;
    padding-right: 1.25rem !important;
    max-width:     100% !important;
}

/* ── NAVBAR ─────────────────────────────────── */
.smilx-nav {
    position:        fixed;
    top: 0; left: 0; right: 0;
    z-index:         9999;
    height:          var(--nav-h);
    background:      rgba(6,9,18,0.96);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border-bottom:   1px solid var(--border);
    display:         flex;
    align-items:     center;
    padding:         0 1.5rem;
    gap:             1.5rem;
}
.smilx-logo {
    font-family: var(--fh); font-weight: 800; font-size: 14px;
    letter-spacing: 0.12em; text-transform: uppercase;
    color: var(--white); flex-shrink: 0; margin-right: auto;
}
.nav-links { display: flex; align-items: center; gap: 2px; }
.nav-item {
    font-family: var(--fh); font-size: 13px; font-weight: 500;
    color: var(--muted); text-decoration: none;
    padding: 5px 13px; border-radius: 6px; border: 1px solid transparent;
    transition: all var(--ease); white-space: nowrap; line-height: 1;
}
.nav-item:hover { color: var(--white); background: rgba(91,138,245,0.08); }
.nav-active {
    color: var(--accent-2) !important; background: rgba(91,138,245,0.12) !important;
    border-color: rgba(91,138,245,0.22) !important; font-weight: 600 !important;
}
.nav-burger {
    display: none; flex-direction: column; gap: 5px;
    background: none; border: none; cursor: pointer; padding: 6px; flex-shrink: 0;
}
.nav-burger span {
    display: block; width: 20px; height: 2px;
    background: var(--muted); border-radius: 2px; transition: background var(--ease);
}
.nav-burger:hover span { background: var(--white); }

@media (max-width: 640px) {
    .smilx-nav {
        flex-wrap: wrap; height: auto; min-height: var(--nav-h);
        padding: 0 1rem; position: relative;
    }
    .smilx-logo  { line-height: var(--nav-h); }
    .nav-burger  { display: flex; line-height: var(--nav-h); margin-left: auto; }
    .nav-links   {
        display: none; flex-direction: column; align-items: stretch;
        width: 100%; padding: 0.5rem 0 0.75rem 0; gap: 2px;
    }
    .smilx-nav.open .nav-links { display: flex; }
    .nav-item    { padding: 10px 12px; font-size: 14px; text-align: left; }
    .nav-spacer  { height: 0 !important; }
}
.nav-spacer { height: var(--nav-h); }

/* ── TIPOGRAFÍA ─────────────────────────────── */
p, li { font-family: var(--fh) !important; line-height: 1.55 !important; color: var(--white) !important; }
h1 { font-family: var(--fh) !important; font-weight: 700 !important; letter-spacing: -0.02em !important; font-size: clamp(1.4rem,4vw,2rem) !important; margin-bottom: 0.2rem !important; }
h2 { font-family: var(--fh) !important; font-weight: 600 !important; font-size: 1.2rem !important; }
h3 { font-family: var(--fh) !important; font-weight: 600 !important; font-size: 0.95rem !important; }
hr { border: none !important; border-top: 1px solid var(--border) !important; margin: 1.25rem 0 !important; }

/* ── INPUT ──────────────────────────────────── */
.stTextInput > div > div > input {
    background: var(--surface-2) !important; border: 1px solid var(--border) !important;
    border-radius: var(--r) !important; color: var(--white) !important;
    font-family: var(--fm) !important; font-size: 14px !important;
    padding: 9px 14px !important;
    transition: border-color var(--ease), box-shadow var(--ease) !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-glow) !important; outline: none !important;
}
.stTextInput > div > div > input::placeholder { color: var(--muted) !important; }
.stTextInput label, .stSelectbox label {
    font-family: var(--fm) !important; color: var(--muted) !important;
    font-size: 10px !important; font-weight: 500 !important;
    letter-spacing: 0.12em !important; text-transform: uppercase !important;
    margin-bottom: 4px !important;
}
.stCheckbox label { font-family: var(--fh) !important; color: var(--muted) !important; font-size: 13px !important; }

/* ── BOTÓN DOWNLOAD ─────────────────────────── */
.stDownloadButton > button {
    display:                 flex !important;
    align-items:             center !important;
    justify-content:         center !important;
    border-radius:           var(--r) !important;
    font-family:             var(--fm) !important;
    font-weight:             500 !important;
    font-size:               12px !important;
    letter-spacing:          0.04em !important;
    white-space:             nowrap !important;
    padding:                 0 18px !important;
    height:                  34px !important;
    min-height:              34px !important;
    max-height:              34px !important;
    min-width:               155px !important;
    border:                  1px solid rgba(91,138,245,0.28) !important;
    background:              rgba(91,138,245,0.08) !important;
    color:                   var(--accent-2) !important;
    -webkit-text-fill-color: var(--accent-2) !important;
    transition:              all var(--ease) !important;
    overflow:                hidden !important;
}
.stDownloadButton > button * {
    white-space:             nowrap !important;
    line-height:             1 !important;
    font-size:               12px !important;
    color:                   var(--accent-2) !important;
    -webkit-text-fill-color: var(--accent-2) !important;
    margin: 0 !important; padding: 0 !important;
}
.stDownloadButton > button:hover {
    background:   rgba(91,138,245,0.16) !important;
    border-color: rgba(91,138,245,0.5) !important;
    box-shadow:   0 0 16px rgba(91,138,245,0.18) !important;
    transform:    translateY(-1px) !important;
}

/* ── BOTÓN LINK (ELAYA) ─────────────────────── */
.stLinkButton > a {
    display:                 inline-flex !important;
    align-items:             center !important;
    justify-content:         center !important;
    border-radius:           var(--r) !important;
    font-family:             var(--fm) !important;
    font-weight:             500 !important;
    font-size:               12px !important;
    letter-spacing:          0.04em !important;
    white-space:             nowrap !important;
    padding:                 0 16px !important;
    height:                  34px !important;
    min-height:              34px !important;
    max-height:              34px !important;
    border:                  1px solid rgba(62,207,142,0.28) !important;
    background:              rgba(62,207,142,0.07) !important;
    color:                   var(--green) !important;
    -webkit-text-fill-color: var(--green) !important;
    text-decoration:         none !important;
    transition:              all var(--ease) !important;
    overflow:                hidden !important;
}
.stLinkButton > a * {
    white-space:             nowrap !important;
    line-height:             1 !important;
    font-size:               12px !important;
    color:                   var(--green) !important;
    -webkit-text-fill-color: var(--green) !important;
    margin: 0 !important; padding: 0 !important;
}
.stLinkButton > a:hover {
    background:   rgba(62,207,142,0.14) !important;
    border-color: rgba(62,207,142,0.5) !important;
    box-shadow:   0 0 16px rgba(62,207,142,0.15) !important;
    transform:    translateY(-1px) !important;
}

/* ── ALERTS ─────────────────────────────────── */
.stAlert {
    background: var(--surface) !important; border: 1px solid var(--border) !important;
    border-left: 2px solid var(--accent) !important; border-radius: var(--r) !important;
}
.stAlert p { font-size: 14px !important; line-height: 1.6 !important; color: rgba(232,237,248,0.80) !important; }

/* ── CARDS ──────────────────────────────────── */
div[data-testid="stVerticalBlockBorderWrapper"] > div {
    background: var(--surface) !important; border: 1px solid var(--border) !important;
    border-radius: var(--r-lg) !important; padding: 1.1rem !important;
    transition: all var(--ease) !important;
}
div[data-testid="stVerticalBlockBorderWrapper"] > div:hover {
    border-color: var(--border-h) !important; transform: translateY(-2px) !important;
    box-shadow: 0 10px 36px rgba(0,0,0,0.5) !important;
}
div[data-testid="stVerticalBlockBorderWrapper"] h3 { font-size: 14px !important; margin-bottom: 1px !important; }

/* ── CAPTION ────────────────────────────────── */
.stCaption, [data-testid="stCaptionContainer"] p {
    color: var(--accent-dim) !important; font-family: var(--fm) !important;
    font-size: 10px !important; letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
}

/* ── FOOTER ─────────────────────────────────── */
.footer-wrap {
    color: var(--muted) !important; font-family: var(--fm) !important;
    font-size: 11px !important; letter-spacing: 0.05em !important;
}

/* ── RESULT BANNER ──────────────────────────── */
.smilx-result-banner {
    font-family: var(--fm); font-size: 11px; letter-spacing: 0.10em;
    color: var(--green); background: var(--green-dim);
    border: 1px solid rgba(62,207,142,0.18); border-left: 3px solid var(--green);
    padding: 8px 16px; border-radius: var(--r);
    display: inline-flex; align-items: center; gap: 8px;
    margin: 0.5rem 0 0.6rem 0; text-transform: uppercase;
    white-space: nowrap; max-width: 100%;
}

/* ── IFRAME ─────────────────────────────────── */
iframe {
    border-radius: var(--r-lg) !important; border: 1px solid var(--border) !important;
    overflow: hidden !important; max-width: 100% !important;
}

/* ── SELECTBOX ──────────────────────────────── */
.stSelectbox > div > div {
    background: var(--surface-2) !important; border: 1px solid var(--border) !important;
    border-radius: var(--r) !important; color: var(--white) !important;
}

/* ── GAPS ───────────────────────────────────── */
div[data-testid="stVerticalBlock"] { gap: 0.3rem !important; }
[data-testid="stVerticalBlock"] > [data-testid="element-container"] { margin-bottom: 0.15rem !important; }

/* ── ANIMACIÓN ──────────────────────────────── */
@keyframes fadeUp {
    from { opacity:0; transform:translateY(8px); }
    to   { opacity:1; transform:translateY(0); }
}
[data-testid="block-container"] > div > div > div { animation: fadeUp 0.28s ease both; }
</style>
"""


def inject_css():
    st.markdown(_CSS, unsafe_allow_html=True)


def render_nav(active: str):
    inject_css()
    st.markdown(_nav_html(active), unsafe_allow_html=True)
