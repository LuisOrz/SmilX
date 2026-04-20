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

    .nav-wrap {
        margin: 0 -1rem 0 -1rem;
        position: sticky;
        top: 0;
        z-index: 9999;
    }

    .navbar {
        min-height: 56px;
        background: #ffffff;
        border-bottom: 1px solid #e8e8e8;
        display: flex;
        align-items: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.10);
        width: 100%;
    }

    .navbar-inner {
        width: 100%;
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 8px 24px;
        box-sizing: border-box;
    }

    .brand {
        font-size: 20px;
        font-weight: 800;
        color: #111111;
        white-space: nowrap;
        margin-right: 10px;
    }

    .nav-links {
        display: flex;
        align-items: center;
        gap: 6px;
        flex-wrap: wrap;
    }

    .nav-links a {
        text-decoration: none;
        color: #111111;
        font-size: 15px;
        font-weight: 700;
        padding: 8px 12px;
        border-radius: 8px;
        transition: background 0.2s ease;
        white-space: nowrap;
        cursor: pointer;
    }

    .nav-links a:hover {
        background: #f1f1f1;
    }

    .nav-links a.active {
        background: #111111;
        color: #ffffff;
    }

    .nav-spacer {
        margin-left: auto;
    }

    .github-box a {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 40px;
        height: 40px;
        border-radius: 8px;
        text-decoration: none;
        transition: background 0.2s ease;
        font-size: 22px;
    }

    .github-box a:hover {
        background: #f1f1f1;
    }

    .page-title {
        font-size: 2rem;
        font-weight: 800;
        color: #ffffff;
        margin: 1.2rem 0 0.5rem 0;
    }

    .page-subtitle {
        font-size: 1rem;
        color: #d6deeb;
        margin-bottom: 1.5rem;
        line-height: 1.6;
    }

    .member-card, .pub-card, .about-card, .description-text {
        background: #0b1324;
        border: 1px solid #1b263c;
        border-radius: 18px;
        padding: 18px;
        color: #f4f7fb;
        margin-bottom: 1rem;
        box-shadow: 0 6px 20px rgba(0,0,0,0.18);
        line-height: 1.65;
    }

    .member-name, .pub-title {
        font-size: 1.1rem;
        font-weight: 800;
        margin-bottom: 0.35rem;
    }

    .member-role, .pub-journal {
        color: #9fb3d9;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .member-links a, .pub-btn {
        display: inline-block;
        margin-right: 0.6rem;
        margin-top: 0.8rem;
        padding: 0.45rem 0.8rem;
        border-radius: 10px;
        text-decoration: none;
        background: #ffffff;
        color: #111111;
        font-weight: 700;
    }

    .footer-wrap {
        margin: 0 auto;
        color: #ffffff;
    }

    @media (max-width: 700px) {
        .navbar-inner {
            padding: 8px 14px;
            gap: 6px;
        }

        .brand {
            font-size: 17px;
        }

        .nav-links a {
            font-size: 13px;
            padding: 6px 8px;
        }
    }
    </style>
    """, unsafe_allow_html=True)


def render_nav(active: str):
    inject_base_css()

    active_map = {
        "Explore": "/",
        "About": "/About",
        "Team": "/Team",
        "Publications": "/Publications",
    }

    st.markdown(f"""
    <script>
    function smilxNav(path) {{
        const w = window.top || window;
        const origin = w.location.origin;
        w.location.href = origin + path;
    }}
    </script>

    <div class="nav-wrap">
        <div class="navbar">
            <div class="navbar-inner">
                <div class="brand">SmilX</div>

                <div class="nav-links">
                    <a href="javascript:void(0)" onclick="smilxNav('/')" class="{'active' if active == 'Explore' else ''}">Explore</a>
                    <a href="javascript:void(0)" onclick="smilxNav('/About')" class="{'active' if active == 'About' else ''}">About</a>
                    <a href="javascript:void(0)" onclick="smilxNav('/Team')" class="{'active' if active == 'Team' else ''}">Team</a>
                    <a href="javascript:void(0)" onclick="smilxNav('/Publications')" class="{'active' if active == 'Publications' else ''}">Publications</a>
                </div>

                <div class="nav-spacer"></div>

                <div class="github-box">
                    <a href="https://github.com/LuisOrz/SmilX" target="_blank" rel="noopener">🐙</a>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
