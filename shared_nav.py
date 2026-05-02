import streamlit as st


def render_nav(active: str):
    st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    section[data-testid="stSidebar"] {display: none !important;}

    html, body, [class*="css"] {
        font-family: Arial, Helvetica, sans-serif;
        background: #030814;
        color: white;
    }
    .stApp {background: #030814 !important; color: white !important;}

    div[data-testid="block-container"],
    .stMainBlockContainer,
    .main .block-container {
        padding-top: 0 !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important;
    }

    /* ── Navbar ── */
    div[data-testid="stHorizontalBlock"]:first-of-type {
        background: #ffffff !important;
        border-bottom: 1px solid #e8e8e8 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.10) !important;
        padding: 4px 16px !important;
        margin: 0 -1rem 1.5rem -1rem !important;
        width: calc(100% + 2rem) !important;
        align-items: center !important;
    }
    div[data-testid="stHorizontalBlock"]:first-of-type p {
        color: #111 !important;
        font-size: 20px !important;
        font-weight: 800 !important;
        margin: 0 !important;
        line-height: 42px !important;
    }

    /* Botones normales del navbar */
    div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button {
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        padding: 5px 14px !important;
        width: 100% !important;
        border: 1px solid #d9d9d9 !important;
        background: #ffffff !important;
        color: #111111 !important;
        box-shadow: none !important;
        transition: background 0.15s !important;
    }
    div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button:hover {
        background: #f0f0f0 !important;
        border-color: #bbb !important;
        color: #111111 !important;
    }

    /* Botón activo (página actual) — disabled */
    div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button[disabled],
    div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button:disabled {
        border: 2px solid #111111 !important;
        background: #111111 !important;
        color: #ffffff !important;
        opacity: 1 !important;
        cursor: default !important;
        -webkit-text-fill-color: #ffffff !important;
    }
    /* Forzar color del texto del span interno del botón activo */
    div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button[disabled] p,
    div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button:disabled p,
    div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button[disabled] span,
    div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button:disabled span {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }

    /* ── Botones Download SMILES y 3D with ELAYA ── */
    .stDownloadButton > button {
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        border: 1px solid #555 !important;
        background: #1a1f2e !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        box-shadow: none !important;
    }
    .stDownloadButton > button:hover {
        background: #2a3248 !important;
        border-color: #aaa !important;
        color: #ffffff !important;
    }
    .stLinkButton > a {
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        border: 1px solid #555 !important;
        background: #1a1f2e !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        text-decoration: none !important;
        box-shadow: none !important;
        display: inline-block;
        padding: 6px 18px;
    }
    .stLinkButton > a:hover {
        background: #2a3248 !important;
        border-color: #aaa !important;
        color: #ffffff !important;
    }

    .footer-wrap {color: #ffffff;}
    </style>
    """, unsafe_allow_html=True)

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
