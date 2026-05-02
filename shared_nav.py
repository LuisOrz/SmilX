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
    body { background: #030814; }
    .stApp {
        background: #030814 !important;
        color: white !important;
        overflow-x: hidden !important;
    }

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

    /* Navbar row */
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
        padding: 0 !important;
        line-height: 44px !important;
    }
    div[data-testid="stHorizontalBlock"]:first-of-type .stPageLink a {
        display: block;
        text-align: center;
        padding: 6px 16px;
        border-radius: 10px;
        background: #ffffff;
        color: #111111 !important;
        font-weight: 700;
        text-decoration: none !important;
        border: 1px solid #d9d9d9;
        font-size: 14px;
        transition: background 0.15s;
    }
    div[data-testid="stHorizontalBlock"]:first-of-type .stPageLink a:hover {
        background: #f0f0f0 !important;
    }
    div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button {
        border-radius: 10px !important;
        border: 1px solid #111111 !important;
        background: #111111 !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        padding: 6px 16px !important;
        width: 100%;
        cursor: default !important;
        opacity: 1 !important;
    }
    div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button:disabled {
        opacity: 1 !important;
        color: #ffffff !important;
        background: #111111 !important;
    }
    div[data-testid="stHorizontalBlock"]:first-of-type a[href*="github"] {
        font-size: 24px;
        text-decoration: none !important;
        display: block;
        text-align: right;
        line-height: 44px;
    }
    .footer-wrap { margin: 0 auto; color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)


def render_nav(active: str):
    inject_base_css()

    # URL-based navigation — works on Streamlit Cloud and locally
    # Streamlit Cloud maps filenames to slugs: 1_About -> About, etc.
    targets = [
        ("Explore",      "/"),
        ("About",        "/About"),
        ("Team",         "/Team"),
        ("Publications", "/Publications"),
    ]

    cols = st.columns([1.2, 1, 1, 1, 1, 0.5])

    with cols[0]:
        st.markdown("**SmilX**")

    for i, (label, url) in enumerate(targets, start=1):
        with cols[i]:
            if label == active:
                st.button(label, key=f"nav_{label}", disabled=True,
                          use_container_width=True)
            else:
                st.page_link(url, label=label, use_container_width=True)

    with cols[5]:
        st.markdown("[🐙](https://github.com/LuisOrz/SmilX)")
