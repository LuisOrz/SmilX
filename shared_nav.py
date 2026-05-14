import streamlit as st

_CSS_CONTENT = """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;500;600&family=Outfit:wght@300;400;500;600;700;800&display=swap');

:root {
    --bg:            #02040a;
    --surface:       #0b0f1c;
    --surface-2:     #111628;
    --surface-3:     #171d32;
    --border:        rgba(99,123,200,0.12);
    --border-hover:  rgba(99,123,200,0.30);
    --accent:        #5b8af5;
    --accent-2:      #7ba3ff;
    --accent-glow:   rgba(91,138,245,0.15);
    --accent-dim:    rgba(91,138,245,0.55);
    --green:         #3ecf8e;
    --green-dim:     rgba(62,207,142,0.10);
    --white:         #e8edf8;
    --muted:         #4a5578;
    --radius:        8px;
    --radius-lg:     14px;
    --nav-h:         52px;
    --font-head:     'Outfit', sans-serif;
    --font-mono:     'IBM Plex Mono', monospace;
    --font-body:     'Outfit', sans-serif;
    --transition:    0.18s cubic-bezier(0.4, 0, 0.2, 1);
}

#MainMenu, header, footer { visibility: hidden; }
section[data-testid="stSidebar"]   { display: none !important; }
[data-testid="stHeader"]           { display: none !important; }
[data-testid="stDecoration"]       { display: none !important; }
[data-testid="stToolbar"]          { display: none !important; }

html, body {
    background: var(--bg) !important;
    color: var(--white) !important;
    font-family: var(--font-body) !important;
}

.stApp,
.stApp > div,
[data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
}

div[data-testid="block-container"],
.stMainBlockContainer,
.main .block-container {
    padding-top:   0 !important;
    padding-left:  2rem !important;
    padding-right: 2rem !important;
    max-width:     100% !important;
}

/* ── NAVBAR ────────────────────────────────── */
div[data-testid="stHorizontalBlock"]:first-of-type {
    background:              rgba(6, 9, 18, 0.95) !important;
    backdrop-filter:         blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border-bottom:           1px solid var(--border) !important;
    padding:                 0 1.5rem !important;
    margin:                  0 -2rem 1.25rem -2rem !important;
    width:                   calc(100% + 4rem) !important;
    align-items:             center !important;
    min-height:              var(--nav-h) !important;
    max-height:              var(--nav-h) !important;
    position:                sticky !important;
    top:                     0 !important;
    z-index:                 999 !important;
}

div[data-testid="stHorizontalBlock"]:first-of-type p {
    color:          var(--white) !important;
    font-family:    var(--font-head) !important;
    font-size:      15px !important;
    font-weight:    700 !important;
    letter-spacing: 0.10em !important;
    margin:         0 !important;
    line-height:    var(--nav-h) !important;
    text-transform: uppercase !important;
}

div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button {
    background:     transparent !important;
    color:          var(--muted) !important;
    border:         none !important;
    border-radius:  6px !important;
    box-shadow:     none !important;
    font-family:    var(--font-body) !important;
    font-weight:    500 !important;
    font-size:      13px !important;
    letter-spacing: 0.03em !important;
    padding:        6px 14px !important;
    height:         32px !important;
    min-height:     unset !important;
    width:          100% !important;
    transition:     all var(--transition) !important;
}
div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button:hover {
    background: rgba(91,138,245,0.08) !important;
    color:      var(--white) !important;
}

div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button[disabled],
div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button:disabled {
    background:              rgba(91,138,245,0.12) !important;
    color:                   var(--accent-2) !important;
    border:                  1px solid rgba(91,138,245,0.25) !important;
    border-radius:           6px !important;
    opacity:                 1 !important;
    cursor:                  default !important;
    -webkit-text-fill-color: var(--accent-2) !important;
    font-weight:             600 !important;
}
div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button[disabled] p,
div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button[disabled] span,
div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button:disabled p,
div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button:disabled span {
    color:                   var(--accent-2) !important;
    -webkit-text-fill-color: var(--accent-2) !important;
}

/* ── BOTONES DE ACCIÓN ─────────────────────── */
.stDownloadButton > button {
    border-radius:           var(--radius) !important;
    font-family:             var(--font-mono) !important;
    font-weight:             500 !important;
    font-size:               12px !important;
    letter-spacing:          0.03em !important;
    padding:                 8px 18px !important;
    border:                  1px solid rgba(91,138,245,0.28) !important;
    background:              rgba(91,138,245,0.08) !important;
    color:                   var(--accent-2) !important;
    -webkit-text-fill-color: var(--accent-2) !important;
    transition:              all var(--transition) !important;
}
.stDownloadButton > button:hover {
    background:   rgba(91,138,245,0.16) !important;
    border-color: rgba(91,138,245,0.5) !important;
    box-shadow:   0 0 20px rgba(91,138,245,0.18) !important;
    transform:    translateY(-1px) !important;
}

.stLinkButton > a {
    border-radius:           var(--radius) !important;
    font-family:             var(--font-mono) !important;
    font-weight:             500 !important;
    font-size:               12px !important;
    letter-spacing:          0.03em !important;
    padding:                 8px 18px !important;
    border:                  1px solid rgba(62,207,142,0.28) !important;
    background:              rgba(62,207,142,0.07) !important;
    color:                   var(--green) !important;
    -webkit-text-fill-color: var(--green) !important;
    text-decoration:         none !important;
    display:                 inline-block !important;
    transition:              all var(--transition) !important;
}
.stLinkButton > a:hover {
    background:   rgba(62,207,142,0.14) !important;
    border-color: rgba(62,207,142,0.5) !important;
    box-shadow:   0 0 20px rgba(62,207,142,0.15) !important;
    transform:    translateY(-1px) !important;
}

/* ── INPUT ─────────────────────────────────── */
.stTextInput > div > div > input {
    background:    var(--surface-2) !important;
    border:        1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color:         var(--white) !important;
    font-family:   var(--font-mono) !important;
    font-size:     14px !important;
    padding:       9px 14px !important;
    transition:    border-color var(--transition), box-shadow var(--transition) !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow:   0 0 0 3px var(--accent-glow) !important;
    outline:      none !important;
}
.stTextInput > div > div > input::placeholder {
    color: var(--muted) !important;
}

.stTextInput label,
.stSelectbox label {
    font-family:    var(--font-mono) !important;
    color:          var(--muted) !important;
    font-size:      10px !important;
    font-weight:    500 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    margin-bottom:  4px !important;
}

.stCheckbox label {
    font-family: var(--font-body) !important;
    color:       var(--muted) !important;
    font-size:   13px !important;
}

/* ── TIPOGRAFÍA ────────────────────────────── */
p, li, span {
    font-family: var(--font-body) !important;
    line-height: 1.55 !important;
    color:       var(--white) !important;
}
h1 {
    font-family:    var(--font-head) !important;
    font-weight:    700 !important;
    letter-spacing: -0.02em !important;
    font-size:      2rem !important;
    margin-bottom:  0.2rem !important;
}
h2 {
    font-family:    var(--font-head) !important;
    font-weight:    600 !important;
    letter-spacing: -0.01em !important;
    font-size:      1.25rem !important;
}
h3 {
    font-family:    var(--font-head) !important;
    font-weight:    600 !important;
    font-size:      1rem !important;
}

hr {
    border:     none !important;
    border-top: 1px solid var(--border) !important;
    margin:     1.5rem 0 !important;
}

/* ── ALERTS ────────────────────────────────── */
.stAlert {
    background:    var(--surface) !important;
    border:        1px solid var(--border) !important;
    border-left:   2px solid var(--accent) !important;
    border-radius: var(--radius) !important;
}
.stAlert p {
    font-size:   14px !important;
    line-height: 1.6 !important;
    color:       rgba(232,237,248,0.80) !important;
}

/* ── CARDS ─────────────────────────────────── */
div[data-testid="stVerticalBlockBorderWrapper"] > div {
    background:    var(--surface) !important;
    border:        1px solid var(--border) !important;
    border-radius: var(--radius-lg) !important;
    padding:       1.2rem !important;
    transition:    all var(--transition) !important;
}
div[data-testid="stVerticalBlockBorderWrapper"] > div:hover {
    border-color: var(--border-hover) !important;
    transform:    translateY(-2px) !important;
    box-shadow:   0 12px 40px rgba(0,0,0,0.5) !important;
}

div[data-testid="stVerticalBlockBorderWrapper"] h3 {
    font-size:     15px !important;
    font-weight:   600 !important;
    margin-bottom: 1px !important;
}

/* ── IFRAME ────────────────────────────────── */
iframe {
    border-radius: var(--radius-lg) !important;
    border:        1px solid var(--border) !important;
    overflow:      hidden !important;
}

/* ── RESULT BANNER ─────────────────────────── */
.smilx-result-banner {
    font-family:    var(--font-mono);
    font-size:      11px;
    letter-spacing: 0.10em;
    color:          var(--green);
    background:     var(--green-dim);
    border:         1px solid rgba(62,207,142,0.18);
    border-left:    3px solid var(--green);
    padding:        8px 16px;
    border-radius:  var(--radius);
    display:        inline-flex;
    align-items:    center;
    gap:            10px;
    margin:         0.6rem 0 0.8rem 0;
    text-transform: uppercase;
}

/* ── FOOTER ────────────────────────────────── */
.footer-wrap {
    color:          var(--muted) !important;
    font-family:    var(--font-mono) !important;
    font-size:      11px !important;
    letter-spacing: 0.05em !important;
}

/* ── SELECTBOX ─────────────────────────────── */
.stSelectbox > div > div {
    background:    var(--surface-2) !important;
    border:        1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color:         var(--white) !important;
}

/* ── CAPTION ───────────────────────────────── */
.stCaption {
    color:          var(--accent-dim) !important;
    font-family:    var(--font-mono) !important;
    font-size:      10px !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
}

/* ── COMPRESIÓN DE ESPACIOS INTERNOS ───────── */
div[data-testid="stVerticalBlock"] > div {
    gap: 0.35rem !important;
}
[data-testid="stVerticalBlock"] > [data-testid="element-container"] {
    margin-bottom: 0.2rem !important;
}

/* ── ENTRADA ───────────────────────────────── */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}
div[data-testid="block-container"] > div > div > div {
    animation: fadeUp 0.30s cubic-bezier(0.4, 0, 0.2, 1) both;
}
</style>
"""


def inject_css():
    st.markdown(_CSS_CONTENT, unsafe_allow_html=True)


def render_nav(active: str):
    inject_css()

    pages = [
        ("Explore",      "main.py"),
        ("About",        "pages/1_About.py"),
        ("Team",         "pages/2_Team.py"),
        ("Publications", "pages/3_Publications.py"),
    ]

    cols = st.columns([1.2, 0.8, 0.8, 0.8, 0.8])
    with cols[0]:
        st.markdown("**SmilX**")

    for i, (label, path) in enumerate(pages, start=1):
        with cols[i]:
            if label == active:
                st.button(label, key=f"nav_{label}", disabled=True,
                          use_container_width=True)
            else:
                if st.button(label, key=f"nav_{label}",
                             use_container_width=True):
                    st.switch_page(path)
