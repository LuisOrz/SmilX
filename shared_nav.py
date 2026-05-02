import streamlit as st


def inject_base_css():
    st.markdown("""
    <style>
    #MainMenu { visibility: hidden; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    section[data-testid="stSidebar"] { display: none !important; }
    html, body, [class*="css"] {
        font-family: Arial, Helvetica, sans-serif;
        background: #030814;
        color: white;
    }
    .stApp { background: #030814 !important; color: white !important; }
    .stApp > div[data-testid="block-container"],
    div[data-testid="block-container"],
    .stMainBlockContainer,
    .main .block-container {
        padding-top: 0 !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important;
        width: 100% !important;
    }
    div[data-testid="stHorizontalBlock"]:first-of-type {
        background: #ffffff;
        border-bottom: 1px solid #e8e8e8;
        box-shadow: 0 2px 8px rgba(0,0,0,0.10);
        padding: 6px 16px !important;
        margin: 0 -1rem 1.2rem -1rem !important;
        width: calc(100% + 2rem) !important;
        align-items: center !important;
        position: sticky;
        top: 0;
        z-index: 9999;
    }
    div[data-testid="stHorizontalBlock"]:first-of-type p {
        color: #111111 !important;
        font-size: 20px !important;
        font-weight: 800 !important;
        margin: 0 !important;
        line-height: 44px !important;
    }
    div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button {
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        padding: 6px 16px !important;
        width: 100%;
        border: 1px solid #d9d9d9 !important;
        background: #ffffff !important;
        color: #111111 !important;
    }
    div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button:hover {
        background: #f0f0f0 !important;
    }
    div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button:disabled {
        border: 1px solid #111111 !important;
        background: #111111 !important;
        color: #ffffff !important;
        opacity: 1 !important;
    }
    .footer-wrap { margin: 0 auto; color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)


def render_nav(active: str):
    inject_base_css()

    targets = [
        ("Explore",      "main.py"),
        ("About",        "pages/1_About.py"),
        ("Team",         "pages/2_Team.py"),
        ("Publications", "pages/3_Publications.py"),
    ]

    cols = st.columns([1.2, 1, 1, 1, 1, 0.5])

    with cols[0]:
        st.markdown("**SmilX**")

    for i, (label, path) in enumerate(targets, start=1):
        with cols[i]:
            if label == active:
                st.button(label, key=f"nav_{label}", disabled=True,
                          use_container_width=True)
            else:
                if st.button(label, key=f"nav_{label}",
                             use_container_width=True):
                    st.switch_page(path)

    with cols[5]:
        # Plain text — no markdown link, no st.page_link
        st.markdown(
            '<a href="https://github.com/LuisOrz/SmilX" target="_blank" rel="noopener" style="font-size:24px;text-decoration:none;color:inherit;">🐙</a>',
            unsafe_allow_html=True
        )
