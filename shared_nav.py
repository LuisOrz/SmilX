import streamlit as st

# ─────────────────────────────────────────────────────────────────────────────
# CSS global — se inyecta con st.markdown + unsafe_allow_html=True
# (components.html usa un iframe aislado y NO afecta el DOM de Streamlit)
# ─────────────────────────────────────────────────────────────────────────────
_CSS = """
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600&display=swap" rel="stylesheet">
<style>

/* ── Ocultar chrome de Streamlit ── */
#MainMenu          { visibility: hidden; }
header             { visibility: hidden; }
footer             { visibility: hidden; }
section[data-testid="stSidebar"] { display: none !important; }

/* ── Variables ── */
:root {
    --bg:        #000000;
    --surface:   #0a0a0a;
    --surface-2: #111111;
    --border:    rgba(255,255,255,0.09);
    --accent:    #c8ddd7;
    --accent-d:  rgba(200,221,215,0.55);
    --white:     #f0f2f1;
    --muted:     #6b7a75;
    --radius:    10px;
    --fh:        'Space Mono', monospace;
    --fb:        'DM Sans', sans-serif;
}

/* ── Fondo global negro ── */
html, body, [class*="css"]          { background: var(--bg) !important; color: var(--white) !important; font-family: var(--fb) !important; }
.stApp                              { background: var(--bg) !important; color: var(--white) !important; }
.stApp > div                        { background: var(--bg) !important; }
[data-testid="stAppViewContainer"]  { background: var(--bg) !important; }
[data-testid="stHeader"]            { background: var(--bg) !important; }
[data-testid="stToolbar"]           { background: var(--bg) !important; }
[data-testid="stDecoration"]        { background: var(--bg) !important; }
[data-testid="block-container"],
.stMainBlockContainer,
.main .block-container {
    background:    var(--bg) !important;
    padding-top:   0      !important;
    padding-left:  2rem   !important;
    padding-right: 2rem   !important;
    max-width:     100%   !important;
}

/* ── Navbar: fondo BLANCO, texto/iconos NEGROS ── */
div[data-testid="stHorizontalBlock"]:first-of-type {
    background:    #ffffff                    !important;
    border-bottom: 1px solid #e0e0e0          !important;
    box-shadow:    0 2px 12px rgba(0,0,0,.08) !important;
    padding:       6px 24px                   !important;
    margin:        0 -2rem 2.5rem -2rem       !important;
    width:         calc(100% + 4rem)          !important;
    align-items:   center                     !important;
}
div[data-testid="stHorizontalBlock"]:first-of-type p {
    color:          #111111         !important;
    font-family:    var(--fh)       !important;
    font-size:      17px            !important;
    font-weight:    700             !important;
    letter-spacing: 0.05em         !important;
    margin:         0               !important;
    line-height:    46px            !important;
}

/* Botones nav inactivos */
div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button {
    border-radius:  var(--radius)   !important;
    font-family:    var(--fb)       !important;
    font-weight:    600             !important;
    font-size:      13px            !important;
    padding:        7px 16px        !important;
    width:          100%            !important;
    border:         1.5px solid #d8d8d8 !important;
    background:     #ffffff         !important;
    color:          #333333         !important;
    box-shadow:     none            !important;
    transition:     all 0.18s ease  !important;
}
div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button:hover {
    background:  #f3f3f3                        !important;
    border-color:#aaaaaa                        !important;
    color:       #111111                        !important;
    transform:   translateY(-1px)               !important;
    box-shadow:  0 3px 10px rgba(0,0,0,.08)    !important;
}

/* Botón nav activo (disabled) */
div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button[disabled],
div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button:disabled {
    border:                  2px solid #0a0a0a  !important;
    background:              #0a0a0a            !important;
    color:                   #ffffff            !important;
    opacity:                 1                  !important;
    cursor:                  default            !important;
    -webkit-text-fill-color: #ffffff            !important;
}
div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button[disabled] p,
div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button:disabled p,
div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button[disabled] span,
div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button:disabled span {
    color:                   #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

/* ── Botones descarga / link ── */
.stDownloadButton > button {
    border-radius:           var(--radius)              !important;
    font-family:             var(--fb)                  !important;
    font-weight:             600                        !important;
    font-size:               13px                       !important;
    padding:                 9px 20px                   !important;
    border:                  1.5px solid rgba(255,255,255,.18) !important;
    background:              var(--surface-2)           !important;
    color:                   var(--white)               !important;
    -webkit-text-fill-color: var(--white)               !important;
    box-shadow:              0 2px 10px rgba(0,0,0,.3)  !important;
    transition:              all 0.18s ease              !important;
}
.stDownloadButton > button:hover {
    background:  #1a2530                         !important;
    border-color:rgba(255,255,255,.32)            !important;
    transform:   translateY(-1px)                !important;
    box-shadow:  0 5px 16px rgba(0,0,0,.45)     !important;
}
.stLinkButton > a {
    border-radius:           var(--radius)              !important;
    font-family:             var(--fb)                  !important;
    font-weight:             600                        !important;
    font-size:               13px                       !important;
    padding:                 9px 20px                   !important;
    border:                  1.5px solid rgba(255,255,255,.18) !important;
    background:              var(--surface-2)           !important;
    color:                   var(--white)               !important;
    -webkit-text-fill-color: var(--white)               !important;
    text-decoration:         none                       !important;
    box-shadow:              0 2px 10px rgba(0,0,0,.3)  !important;
    display:                 inline-block               !important;
    transition:              all 0.18s ease              !important;
}
.stLinkButton > a:hover {
    background:  #1a2530                     !important;
    border-color:rgba(255,255,255,.32)        !important;
    transform:   translateY(-1px)            !important;
}

/* ── Input de texto ── */
.stTextInput > div > div > input {
    background:   var(--surface)        !important;
    border:       1.5px solid var(--border) !important;
    border-radius:var(--radius)         !important;
    color:        var(--white)          !important;
    font-family:  var(--fb)             !important;
    font-size:    15px                  !important;
    padding:      10px 14px             !important;
    transition:   border-color 0.18s   !important;
}
.stTextInput > div > div > input:focus {
    border-color:rgba(255,255,255,.30)  !important;
    box-shadow:  0 0 0 3px rgba(255,255,255,.04) !important;
}
.stTextInput label, .stSelectbox label {
    font-family:    var(--fb)           !important;
    color:          var(--muted)        !important;
    font-size:      12px                !important;
    font-weight:    500                 !important;
    letter-spacing: 0.07em             !important;
    text-transform: uppercase           !important;
}

/* ── Checkbox ── */
.stCheckbox label {
    font-family: var(--fb)      !important;
    color:       var(--accent-d)!important;
    font-size:   14px           !important;
}

/* ── Divisor ── */
hr { border-color: var(--border) !important; margin: 2.5rem 0 !important; }

/* ── Tipografía general ── */
p, li, span { font-family: var(--fb) !important; line-height: 1.75 !important; }
h1, h2, h3  { font-family: var(--fh) !important; letter-spacing: -0.01em !important; }

/* ── Alert / info ── */
.stAlert {
    background:    var(--surface-2) !important;
    border:        1px solid var(--border) !important;
    border-radius: var(--radius)    !important;
    color:         var(--white)     !important;
}

/* ── Cards con borde (Team / Publications) ── */
div[data-testid="stVerticalBlockBorderWrapper"] > div {
    background:    var(--surface)   !important;
    border:        1px solid var(--border) !important;
    border-radius: 14px             !important;
    padding:       1.4rem           !important;
    transition:    box-shadow .22s ease, border-color .22s ease !important;
}
div[data-testid="stVerticalBlockBorderWrapper"] > div:hover {
    box-shadow:   0 6px 28px rgba(0,0,0,.55) !important;
    border-color: rgba(255,255,255,.16)       !important;
}

/* ── iframe mols2grid ── */
iframe {
    border-radius: 12px !important;
    border:        1px solid var(--border) !important;
    overflow:      hidden !important;
}

/* ── Banner de resultado ── */
.smilx-result-banner {
    font-family:    var(--fh);
    font-size:      12px;
    letter-spacing: 0.08em;
    color:          var(--accent);
    background:     var(--surface-2);
    border:         1px solid var(--border);
    border-left:    3px solid var(--accent);
    padding:        10px 20px;
    border-radius:  var(--radius);
    display:        inline-block;
    margin:         0.5rem 0 1.2rem 0;
    text-transform: uppercase;
}

/* ── Footer ── */
.footer-wrap {
    color:       var(--muted)   !important;
    font-family: var(--fb)      !important;
    font-size:   12px           !important;
}
</style>
"""


def render_nav(active: str):
    # st.markdown con unsafe_allow_html=True inyecta en el DOM principal de Streamlit.
    # NO usar components.html() — ese método crea un iframe aislado y el CSS
    # no llega al resto de la página.
    st.markdown(_CSS, unsafe_allow_html=True)

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
