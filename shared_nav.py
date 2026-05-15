import streamlit as st


def render_navbar():
    st.markdown("""
    <style>

    :root{
        --nav-h:72px;
        --bg:#050816;
        --card:#0b1020;
        --line:rgba(120,140,255,.12);
        --text:#E8EDF8;
        --muted:rgba(232,237,248,.62);
        --accent:#5B8AF5;
    }

    /* ─────────────────────────────────────────────
       GLOBAL
    ───────────────────────────────────────────── */

    html, body, [class*="css"]{
        background: var(--bg);
    }

    .main .block-container{
        padding-top: 1rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
        max-width: 1400px;
    }

    /* ─────────────────────────────────────────────
       NAVBAR
    ───────────────────────────────────────────── */

    .smilx-nav{
        width:100%;
        min-height:var(--nav-h);

        display:flex;
        align-items:center;
        justify-content:space-between;

        padding:0 1.2rem;

        background:rgba(7,12,25,.88);

        border:1px solid var(--line);
        border-radius:18px;

        backdrop-filter: blur(14px);

        margin-bottom:1.5rem;

        position:relative;
        overflow:hidden;

        gap:1rem;
        flex-wrap:nowrap;
    }

    .smilx-nav::before{
        content:'';
        position:absolute;
        inset:0;
        background:
            linear-gradient(
                90deg,
                transparent,
                rgba(91,138,245,.05),
                transparent
            );
        pointer-events:none;
    }

    /* ─────────────────────────────────────────────
       LOGO
    ───────────────────────────────────────────── */

    .smilx-logo{
        font-family:'IBM Plex Mono', monospace;
        color:var(--text);

        font-size:15px;
        font-weight:600;

        letter-spacing:.12em;

        white-space:nowrap;
        flex-shrink:0;
    }

    .smilx-logo span{
        color:var(--accent);
    }

    /* ─────────────────────────────────────────────
       LINKS
    ───────────────────────────────────────────── */

    .nav-links{
        display:flex;
        align-items:center;
        gap:.7rem;

        flex-wrap:wrap;
        justify-content:flex-end;
    }

    .nav-item{
        text-decoration:none !important;

        color:var(--muted) !important;

        font-family:'Outfit', sans-serif;
        font-size:14px;
        font-weight:500;

        padding:.7rem 1rem;

        border-radius:12px;

        transition:all .25s ease;

        border:1px solid transparent;

        white-space:nowrap;
    }

    .nav-item:hover{
        color:var(--text) !important;

        background:rgba(91,138,245,.08);

        border:1px solid rgba(91,138,245,.18);

        transform:translateY(-1px);
    }

    /* ─────────────────────────────────────────────
       MOBILE MENU BUTTON
    ───────────────────────────────────────────── */

    .nav-burger{
        display:none;

        width:42px;
        height:42px;

        border-radius:10px;

        border:1px solid rgba(91,138,245,.12);

        align-items:center;
        justify-content:center;

        cursor:pointer;

        color:white;

        background:rgba(91,138,245,.05);

        flex-shrink:0;
    }

    /* ─────────────────────────────────────────────
       RESPONSIVE
    ───────────────────────────────────────────── */

    @media (max-width: 768px) {

        div[data-testid="block-container"],
        .stMainBlockContainer,
        .main .block-container {
            padding-left: 0.7rem !important;
            padding-right: 0.7rem !important;
            max-width: 100% !important;
        }

        .smilx-nav{
            flex-wrap:wrap;

            height:auto;
            min-height:var(--nav-h);

            padding:1rem;

            gap:.8rem;
        }

        .smilx-logo{
            font-size:13px;
            line-height:1.4;
        }

        .nav-burger{
            display:flex;
            margin-left:auto;
        }

        .nav-links{
            width:100%;

            display:flex;

            flex-direction:column;

            gap:.5rem;

            padding-top:.5rem;
        }

        .nav-item{
            width:100%;

            text-align:center;

            padding:.85rem;

            font-size:14px;

            border-radius:10px;
        }

        h1{
            font-size:1.6rem !important;
        }

        h2{
            font-size:1.2rem !important;
        }

        h3{
            font-size:1rem !important;
        }

    }

    /* ─────────────────────────────────────────────
       EXTRA FIXES
    ───────────────────────────────────────────── */

    div[data-testid="stHorizontalBlock"]{
        flex-wrap:wrap !important;
        gap:.7rem !important;
    }

    .row-widget.stButton{
        width:100% !important;
    }

    .st-emotion-cache-1kyxreq{
        flex-wrap:wrap !important;
    }

    iframe{
        width:100% !important;
        border-radius:14px;
    }

    img{
        max-width:100% !important;
        height:auto !important;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="smilx-nav">

        <div class="smilx-logo">
            <span>SMILX</span> PLATFORM
        </div>

        <div class="nav-links">
            <a class="nav-item" href="#">HOME</a>
            <a class="nav-item" href="#">EXPLORE</a>
            <a class="nav-item" href="#">ABOUT</a>
            <a class="nav-item" href="#">TEAM</a>
            <a class="nav-item" href="#">PUBLICATIONS</a>
        </div>

    </div>
    """, unsafe_allow_html=True)
