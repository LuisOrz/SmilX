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

    /* All nav buttons base style */
    div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button {
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        padding: 6px 16px !important;
        width: 100%;
        border: 1px solid #d9d9d9 !important;
        background: #ffffff !important;
        color: #111111 !important;
        transition: background 0.15s !important;
    }
    div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button:hover {
        background: #f0f0f0 !important;
        color: #111111 !important;
    }

    /* Active button override */
    div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button:disabled {
        border: 1px solid #111111 !important;
        background: #111111 !important;
        color: #ffffff !important;
        opacity: 1 !important;
        cursor: default !important;
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
                # Active page: disabled button (no navigation)
                st.button(label, key=f"nav_{label}", disabled=True,
                          use_container_width=True)
            else:
                # Inactive page: clickable button that switches page
                if st.button(label, key=f"nav_{label}",
                             use_container_width=True):
                    st.switch_page(path)

    with cols[5]:
        st.markdown("[🐙](https://github.com/LuisOrz/SmilX)")
