import streamlit as st

# ─────────────────────────────────────────────────────────────────────────────
# CSS global inyectado con st.markdown — el único método confiable en
# Streamlit Cloud (no depende de cross-frame access bloqueado por CSP).
# ─────────────────────────────────────────────────────────────────────────────

_CSS_CONTENT = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600&display=swap');

/* ═══════════════════════════════════════════════
   TOKENS DE DISEÑO
═══════════════════════════════════════════════ */
:root {
    --bg:           #050508;
    --surface:      #0d0d12;
    --surface-2:    #13131a;
    --surface-3:    #1a1a24;
    --border:       rgba(255,255,255,0.07);
    --border-hover: rgba(200,221,215,0.22);
    --accent:       #c8ddd7;
    --accent-2:     #8eb8b0;
    --accent-glow:  rgba(200,221,215,0.12);
    --accent-dim:   rgba(200,221,215,0.50);
    --white:        #eef1f0;
    --muted:        #5a6b66;
    --muted-2:      #3d4f4a;
    --radius:       10px;
    --radius-lg:    16px;
    --nav-bg:       #ffffff;
    --nav-text:     #0d0d12;
    --nav-border:   #e8e8e8;
    --font-head:    'Syne', sans-serif;
    --font-mono:    'Space Mono', monospace;
    --font-body:    'DM Sans', sans-serif;
    --transition:   0.22s cubic-bezier(0.4, 0, 0.2, 1);
}

/* ═══════════════════════════════════════════════
   RESET & BASE
═══════════════════════════════════════════════ */
#MainMenu, header, footer { visibility: hidden; }
section[data-testid="stSidebar"] { display: none !important; }
[data-testid="stHeader"]          { display: none !important; }
[data-testid="stDecoration"]      { display: none !important; }

html, body {
    background:  var(--bg) !important;
    color:       var(--white) !important;
    font-family: var(--font-body) !important;
}

.stApp,
.stApp > div,
[data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
}

/* ═══════════════════════════════════════════════
   BLOCK CONTAINER
═══════════════════════════════════════════════ */
div[data-testid="block-container"],
.stMainBlockContainer,
.main .block-container {
    padding-top:   0 !important;
    padding-left:  2.5rem !important;
    padding-right: 2.5rem !important;
    max-width:     100% !important;
}

/* ═══════════════════════════════════════════════
   NAVBAR
═══════════════════════════════════════════════ */
div[data-testid="stHorizontalBlock"]:first-of-type {
    background:    var(--nav-bg) !important;
    border-bottom: 1px solid var(--nav-border) !important;
    box-shadow:    0 1px 0 rgba(0,0,0,0.04),
                   0 4px 24px rgba(0,0,0,0.06) !important;
    padding:       0 28px !important;
    margin:        0 -2.5rem 3rem -2.5rem !important;
    width:         calc(100% + 5rem) !important;
    align-items:   center !important;
    min-height:    58px !important;
    position:      sticky !important;
    top:           0 !important;
    z-index:       999 !important;
}

/* Logo "SmilX" */
div[data-testid="stHorizontalBlock"]:first-of-type p {
    color:          var(--nav-text) !important;
    font-family:    var(--font-head) !important;
    font-size:      18px !important;
    font-weight:    800 !important;
    letter-spacing: 0.04em !important;
    margin:         0 !important;
    line-height:    58px !important;
}

/* Botones nav — inactivos */
div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button {
    background:     transparent !important;
    color:          #555555 !important;
    border:         none !important;
    border-radius:  8px !important;
    box-shadow:     none !important;
    font-family:    var(--font-body) !important;
    font-weight:    500 !important;
    font-size:      14px !important;
    letter-spacing: 0.01em !important;
    padding:        8px 18px !important;
    width:          100% !important;
    transition:     all var(--transition) !important;
}
div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button:hover {
    background: #f5f5f5 !important;
    color:      #111111 !important;
}

/* Botón nav — activo (disabled) */
div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button[disabled],
div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button:disabled {
    background:              #111111 !important;
    color:                   #ffffff !important;
    border:                  none !important;
    border-radius:           8px !important;
    opacity:                 1 !important;
    cursor:                  default !important;
    -webkit-text-fill-color: #ffffff !important;
    font-weight:             600 !important;
    letter-spacing:          0.02em !important;
}
div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button[disabled] p,
div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button[disabled] span,
div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button:disabled p,
div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button:disabled span {
    color:                   #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

/* ═══════════════════════════════════════════════
   BOTONES DE ACCIÓN (Download / Link)
═══════════════════════════════════════════════ */
.stDownloadButton > button {
    border-radius:           var(--radius) !important;
    font-family:             var(--font-body) !important;
    font-weight:             600 !important;
    font-size:               13px !important;
    letter-spacing:          0.02em !important;
    padding:                 10px 22px !important;
    border:                  1px solid var(--border-hover) !important;
    background:              linear-gradient(135deg, var(--surface-3) 0%, var(--surface-2) 100%) !important;
    color:                   var(--accent) !important;
    -webkit-text-fill-color: var(--accent) !important;
    box-shadow:              0 2px 12px rgba(0,0,0,0.4),
                             inset 0 1px 0 rgba(255,255,255,0.04) !important;
    transition:              all var(--transition) !important;
}
.stDownloadButton > button:hover {
    background:   linear-gradient(135deg, #1e2e2a 0%, #182520 100%) !important;
    border-color: var(--accent-2) !important;
    box-shadow:   0 4px 20px rgba(200,221,215,0.15),
                  inset 0 1px 0 rgba(255,255,255,0.06) !important;
    transform:    translateY(-1px) !important;
}

.stLinkButton > a {
    border-radius:           var(--radius) !important;
    font-family:             var(--font-body) !important;
    font-weight:             600 !important;
    font-size:               13px !important;
    letter-spacing:          0.02em !important;
    padding:                 10px 22px !important;
    border:                  1px solid var(--border-hover) !important;
    background:              linear-gradient(135deg, var(--surface-3) 0%, var(--surface-2) 100%) !important;
    color:                   var(--accent) !important;
    -webkit-text-fill-color: var(--accent) !important;
    text-decoration:         none !important;
    display:                 inline-block !important;
    box-shadow:              0 2px 12px rgba(0,0,0,0.4),
                             inset 0 1px 0 rgba(255,255,255,0.04) !important;
    transition:              all var(--transition) !important;
}
.stLinkButton > a:hover {
    background:   linear-gradient(135deg, #1e2e2a 0%, #182520 100%) !important;
    border-color: var(--accent-2) !important;
    box-shadow:   0 4px 20px rgba(200,221,215,0.15),
                  inset 0 1px 0 rgba(255,255,255,0.06) !important;
    transform:    translateY(-1px) !important;
}

/* ═══════════════════════════════════════════════
   INPUTS DE TEXTO
═══════════════════════════════════════════════ */
.stTextInput > div > div > input {
    background:    var(--surface-2) !important;
    border:        1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color:         var(--white) !important;
    font-family:   var(--font-mono) !important;
    font-size:     15px !important;
    padding:       11px 16px !important;
    transition:    border-color var(--transition),
                   box-shadow var(--transition) !important;
    box-shadow:    inset 0 2px 6px rgba(0,0,0,0.3) !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent-2) !important;
    box-shadow:   inset 0 2px 6px rgba(0,0,0,0.3),
                  0 0 0 3px var(--accent-glow) !important;
    outline:      none !important;
}
.stTextInput > div > div > input::placeholder {
    color: var(--muted-2) !important;
}

/* ═══════════════════════════════════════════════
   LABELS
═══════════════════════════════════════════════ */
.stTextInput label, .stSelectbox label {
    font-family:    var(--font-body) !important;
    color:          var(--muted) !important;
    font-size:      11px !important;
    font-weight:    600 !important;
    letter-spacing: 0.10em !important;
    text-transform: uppercase !important;
    margin-bottom:  6px !important;
}

/* ═══════════════════════════════════════════════
   CHECKBOX
═══════════════════════════════════════════════ */
.stCheckbox label {
    font-family: var(--font-body) !important;
    color:       var(--accent-dim) !important;
    font-size:   14px !important;
    font-weight: 400 !important;
}

/* ═══════════════════════════════════════════════
   DIVIDER
═══════════════════════════════════════════════ */
hr {
    border:     none !important;
    border-top: 1px solid var(--border) !important;
    margin:     3rem 0 !important;
}

/* ═══════════════════════════════════════════════
   TIPOGRAFÍA GENERAL
═══════════════════════════════════════════════ */
p, li, span {
    font-family: var(--font-body) !important;
    line-height: 1.80 !important;
    color:       var(--white) !important;
}
h1 {
    font-family:    var(--font-head) !important;
    font-weight:    800 !important;
    letter-spacing: -0.02em !important;
    font-size:      2.4rem !important;
}
h2 {
    font-family:    var(--font-head) !important;
    font-weight:    700 !important;
    letter-spacing: -0.015em !important;
}
h3 {
    font-family:    var(--font-head) !important;
    font-weight:    600 !important;
    letter-spacing: -0.01em !important;
}

/* ═══════════════════════════════════════════════
   ALERT / INFO BOXES
═══════════════════════════════════════════════ */
.stAlert {
    background:    linear-gradient(135deg, var(--surface-2) 0%, var(--surface-3) 100%) !important;
    border:        1px solid var(--border) !important;
    border-left:   3px solid var(--accent-2) !important;
    border-radius: var(--radius) !important;
    color:         var(--white) !important;
    box-shadow:    0 4px 20px rgba(0,0,0,0.3) !important;
}

/* ═══════════════════════════════════════════════
   CARDS (Team, Publications)
═══════════════════════════════════════════════ */
div[data-testid="stVerticalBlockBorderWrapper"] > div {
    background:    linear-gradient(160deg, var(--surface-2) 0%, var(--surface) 100%) !important;
    border:        1px solid var(--border) !important;
    border-radius: var(--radius-lg) !important;
    padding:       1.5rem !important;
    transition:    box-shadow var(--transition),
                   border-color var(--transition),
                   transform var(--transition) !important;
    box-shadow:    0 2px 8px rgba(0,0,0,0.3),
                   inset 0 1px 0 rgba(255,255,255,0.03) !important;
}
div[data-testid="stVerticalBlockBorderWrapper"] > div:hover {
    box-shadow:   0 8px 32px rgba(0,0,0,0.5),
                  0 0 0 1px var(--border-hover),
                  inset 0 1px 0 rgba(255,255,255,0.05) !important;
    border-color: var(--border-hover) !important;
    transform:    translateY(-2px) !important;
}

/* ═══════════════════════════════════════════════
   IFRAME (mols2grid)
═══════════════════════════════════════════════ */
iframe {
    border-radius: var(--radius-lg) !important;
    border:        1px solid var(--border) !important;
    overflow:      hidden !important;
    box-shadow:    0 8px 32px rgba(0,0,0,0.4) !important;
}

/* ═══════════════════════════════════════════════
   RESULT BANNER
═══════════════════════════════════════════════ */
.smilx-result-banner {
    font-family:    var(--font-mono);
    font-size:      11px;
    letter-spacing: 0.10em;
    color:          var(--accent);
    background:     linear-gradient(90deg, rgba(200,221,215,0.07) 0%, transparent 100%);
    border:         1px solid rgba(200,221,215,0.15);
    border-left:    3px solid var(--accent);
    padding:        10px 20px;
    border-radius:  var(--radius);
    display:        inline-flex;
    align-items:    center;
    gap:            10px;
    margin:         0.75rem 0 1.5rem 0;
    text-transform: uppercase;
}

/* ═══════════════════════════════════════════════
   FOOTER
═══════════════════════════════════════════════ */
.footer-wrap {
    color:          var(--muted) !important;
    font-family:    var(--font-body) !important;
    font-size:      12px !important;
    letter-spacing: 0.02em !important;
}

/* ═══════════════════════════════════════════════
   SELECTBOX
═══════════════════════════════════════════════ */
.stSelectbox > div > div {
    background:    var(--surface-2) !important;
    border:        1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color:         var(--white) !important;
}

/* ═══════════════════════════════════════════════
   ANIMACIÓN DE ENTRADA
═══════════════════════════════════════════════ */
@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(14px); }
    to   { opacity: 1; transform: translateY(0); }
}

div[data-testid="block-container"] > div > div > div {
    animation: fadeSlideUp 0.45s cubic-bezier(0.4, 0, 0.2, 1) both;
}
</style>
"""


def inject_css():
    """Inyecta el CSS global mediante st.markdown — método confiable en Streamlit Cloud."""
    st.markdown(_CSS_CONTENT, unsafe_allow_html=True)


def render_nav(active: str):
    inject_css()

    pages = [
        ("Explore",      "main.py"),
        ("About",        "pages/1_About.py"),
        ("Team",         "pages/2_Team.py"),
        ("Publications", "pages/3_Publications.py"),
    ]

    cols = st.columns([1.5, 1, 1, 1, 1])
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
