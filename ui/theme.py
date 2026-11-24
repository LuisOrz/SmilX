"""
SmilX design system
-------------------
One stylesheet for every page. The identity of SmilX is preserved:
deep-space navy background, SmilX blue accent, mint green for success,
Outfit for text and IBM Plex Mono for technical labels.
"""
import streamlit as st

CSS = r"""
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
    --amber:       #f5b85b;
    --red:         #f5675b;
    --white:       #e8edf8;
    --text-2:      #9aa5c7;
    --muted:       #5d6a92;
    --r:           8px;
    --r-lg:        14px;
    --r-xl:        20px;
    --nav-h:       60px;
    --maxw:        1180px;
    --fh:          'Outfit', sans-serif;
    --fm:          'IBM Plex Mono', monospace;
    --ease:        0.18s cubic-bezier(.4,0,.2,1);
}

/* ── Streamlit chrome ───────────────────────────────────────────── */
#MainMenu, footer,
[data-testid="stHeader"], [data-testid="stDecoration"],
[data-testid="stToolbar"], [data-testid="stStatusWidget"],
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebarNav"] { display: none !important; }

html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: var(--bg) !important;
    color: var(--white) !important;
    font-family: var(--fh) !important;
}
/* Ambient glow + faint lattice, in SmilX blue */
[data-testid="stAppViewContainer"]::before {
    content: ""; position: fixed; inset: 0; pointer-events: none; z-index: 0;
    background:
        radial-gradient(900px 480px at 50% -120px, rgba(91,138,245,0.16), transparent 70%),
        radial-gradient(600px 420px at 100% 40%, rgba(62,207,142,0.05), transparent 70%),
        radial-gradient(rgba(123,163,255,0.07) 1px, transparent 1px);
    background-size: auto, auto, 28px 28px;
    mask-image: linear-gradient(to bottom, #000 0%, #000 55%, transparent 100%);
}
[data-testid="stMain"] { position: relative; z-index: 1; }

[data-testid="stMainBlockContainer"], .block-container {
    max-width: var(--maxw) !important;
    padding: calc(var(--nav-h) + 1.75rem) 1.5rem 2rem !important;
}
[data-testid="stVerticalBlock"] { gap: 0.85rem; }

/* ── Typography ─────────────────────────────────────────────────── */
p, li, label { font-family: var(--fh); }
p, li { color: var(--text-2); line-height: 1.65; }
strong, b { color: var(--white); font-weight: 600; }
h1, h2, h3, h4 { font-family: var(--fh) !important; color: var(--white) !important; }
a { color: var(--accent-2); }
code { font-family: var(--fm) !important; }
[data-testid="stMarkdownContainer"] p code, li code {
    background: rgba(91,138,245,0.10) !important; color: var(--accent-2) !important;
    border: 1px solid rgba(91,138,245,0.18); border-radius: 5px; padding: 1px 6px;
}
[data-testid="stHeadingWithActionElements"] a,
[data-testid="stHeaderActionElements"] { display: none !important; }
hr { border: none !important; border-top: 1px solid var(--border) !important; margin: 1.5rem 0 !important; }

/* ── Navbar (keyed container → fixed glass bar) ─────────────────── */
.st-key-smilx-nav {
    position: fixed !important; top: 0; left: 0; right: 0; z-index: 999990;
    height: var(--nav-h);
    background: rgba(4,7,15,0.82);
    backdrop-filter: blur(18px) saturate(140%); -webkit-backdrop-filter: blur(18px) saturate(140%);
    border-bottom: 1px solid var(--border);
    display: flex !important; flex-direction: row !important; align-items: center !important;
    gap: 4px !important; padding: 0 max(1.5rem, calc((100vw - var(--maxw)) / 2 + 1.5rem)) !important;
    overflow-x: auto; scrollbar-width: none;
}
.st-key-smilx-nav::-webkit-scrollbar { display: none; }
.st-key-smilx-nav > div { width: auto !important; flex: 0 0 auto !important; }
.st-key-smilx-nav > div:first-child { margin-right: auto; }
.st-key-smilx-nav [data-testid="stElementContainer"] { width: auto !important; }
.st-key-smilx-nav [data-testid="stMarkdownContainer"] { margin: 0 !important; }
.st-key-smilx-nav [data-testid="stElementContainer"] { margin-top: 0 !important; margin-bottom: 0 !important; }
.st-key-smilx-nav [data-testid="stMarkdown"] { display: flex; align-items: center; }
.smilx-brand { margin: 0; display: flex; align-items: center; gap: 10px; text-decoration: none !important; }
.smilx-brand img { height: 22px; width: auto; display: block; }
.smilx-brand .tag {
    font-family: var(--fm); font-size: 9.5px; letter-spacing: .14em; text-transform: uppercase;
    color: var(--accent-2); border: 1px solid rgba(91,138,245,.28); background: rgba(91,138,245,.08);
    padding: 3px 7px; border-radius: 999px; white-space: nowrap;
}
.st-key-smilx-nav a[data-testid="stPageLink-NavLink"] {
    padding: 8px 13px !important; border-radius: 8px !important; margin: 0 !important;
    border: 1px solid transparent !important; background: transparent !important;
    transition: all var(--ease) !important; white-space: nowrap !important;
}
.st-key-smilx-nav a[data-testid="stPageLink-NavLink"] p {
    font-family: var(--fh) !important; font-size: 14px !important; font-weight: 500 !important;
    color: var(--text-2) !important; white-space: nowrap !important; line-height: 1 !important; margin: 0 !important;
}
.st-key-smilx-nav a[data-testid="stPageLink-NavLink"]:hover { background: rgba(91,138,245,0.08) !important; }
.st-key-smilx-nav a[data-testid="stPageLink-NavLink"]:hover p { color: var(--white) !important; }
.st-key-smilx-nav div[class*="st-key-nav-on"] a[data-testid="stPageLink-NavLink"] {
    background: rgba(91,138,245,0.12) !important; border-color: rgba(91,138,245,0.26) !important;
}
.st-key-smilx-nav div[class*="st-key-nav-on"] a[data-testid="stPageLink-NavLink"] p {
    color: var(--accent-2) !important; font-weight: 600 !important;
}
.st-key-smilx-nav div[class*="st-key-nav-on"] { width: auto !important; flex: 0 0 auto !important; }
/* In-page links styled as green pill buttons */
div[class*="st-key-green"] a[data-testid="stPageLink-NavLink"] {
    display: inline-flex !important; padding: 8px 14px !important; border-radius: 9px !important;
    border: 1px solid rgba(62,207,142,.32) !important; background: rgba(62,207,142,.08) !important; transition: all var(--ease) !important;
}
div[class*="st-key-green"] a[data-testid="stPageLink-NavLink"] p { font-family: var(--fm) !important; font-size: 12.5px !important; color: var(--green) !important; margin: 0 !important; }
div[class*="st-key-green"] a[data-testid="stPageLink-NavLink"]:hover { background: rgba(62,207,142,.15) !important; border-color: rgba(62,207,142,.55) !important; }
@media (max-width: 760px) {
    :root { --nav-h: 56px; }
    .smilx-brand .tag { display: none; }
    .st-key-smilx-nav { padding: 0 .75rem !important;
        -webkit-mask-image: linear-gradient(90deg, #000 82%, transparent); mask-image: linear-gradient(90deg, #000 82%, transparent); }
    .st-key-smilx-nav a[data-testid="stPageLink-NavLink"] { padding: 7px 9px !important; }
    .st-key-smilx-nav a[data-testid="stPageLink-NavLink"] p { font-size: 13px !important; }
    [data-testid="stMainBlockContainer"], .block-container { padding-left: 1rem !important; padding-right: 1rem !important; }
}

/* ── Page header ────────────────────────────────────────────────── */
.eyebrow {
    font-family: var(--fm); font-size: 11px; font-weight: 500; letter-spacing: .16em;
    text-transform: uppercase; color: var(--accent-2);
    display: inline-flex; align-items: center; gap: 8px; margin-bottom: .6rem;
}
.eyebrow::before { content: ""; width: 18px; height: 1px; background: var(--accent); }
.page-title {
    font-family: var(--fh); font-weight: 700; letter-spacing: -0.025em; line-height: 1.08;
    font-size: clamp(2rem, 4.4vw, 3rem); color: var(--white); margin: 0 0 .7rem 0;
}
.page-title .grad {
    background: linear-gradient(92deg, var(--accent-2), #a9c1ff 45%, var(--green));
    -webkit-background-clip: text; background-clip: text; color: transparent;
}
.page-lead { font-size: 1.08rem; color: var(--text-2); max-width: 760px; margin: 0 0 1.4rem 0; line-height: 1.65; }
.section-title { font-family: var(--fh); font-weight: 650; font-size: 1.35rem; color: var(--white); margin: 0 0 .3rem 0; letter-spacing: -0.01em; }
.section-sub { color: var(--muted); font-size: .95rem; margin: 0 0 1rem 0; }
.section-gap { height: 2.2rem; }

/* ── Hero (Explore) ─────────────────────────────────────────────── */
.hero { text-align: center; padding: .5rem 0 .4rem; }
.hero-logo { width: min(400px, 78vw); height: auto; filter: drop-shadow(0 0 28px rgba(91,138,245,.30)); margin: .25rem auto 1.1rem; display: block; }
.hero h1.tagline {
    font-family: var(--fh) !important; font-weight: 600 !important; font-size: clamp(1.2rem, 2.6vw, 1.6rem) !important;
    letter-spacing: -0.01em; color: var(--white) !important; margin: 0 0 .5rem 0 !important; padding: 0 !important;
}
.hero p.sub { max-width: 680px; margin: 0 auto 1rem; color: var(--text-2); font-size: 1rem; }
.chips { display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; margin: .25rem 0 0; }
.chip {
    font-family: var(--fm); font-size: 11px; letter-spacing: .04em; color: var(--text-2);
    padding: 5px 11px; border-radius: 999px; border: 1px solid var(--border); background: rgba(11,15,28,.7);
    display: inline-flex; align-items: center; gap: 6px; text-decoration: none !important; white-space: nowrap;
}
.chip .dot { width: 6px; height: 6px; border-radius: 50%; background: var(--green); box-shadow: 0 0 8px var(--green); }
.chip.blue { color: var(--accent-2); border-color: rgba(91,138,245,.28); background: rgba(91,138,245,.08); }
a.chip:hover { border-color: var(--border-h); color: var(--white); }
.credit {
    max-width: 760px; margin: 1.1rem auto 0; padding: .9rem 1.2rem; border-radius: 12px;
    border: 1px solid var(--border); background: rgba(11,15,28,.55); text-align: center;
}
.credit .t { font-family: var(--fm); font-style: italic; font-size: 12px; color: rgba(232,237,248,.7); margin: 0 0 .35rem; }
.credit .a { font-size: 12.5px; color: var(--muted); margin: 0 0 .3rem; line-height: 1.6; }
.credit .i { font-family: var(--fm); font-size: 10px; letter-spacing: .1em; text-transform: uppercase; color: var(--accent-dim); margin: 0; }

/* ── Cards (bordered containers + HTML cards) ───────────────────── */
[data-testid="stVerticalBlockBorderWrapper"], div[class*="st-key-card"] {
    background: linear-gradient(180deg, rgba(17,22,40,.72), rgba(11,15,28,.72)) !important;
    border: 1px solid var(--border) !important; border-radius: var(--r-lg) !important;
}
div[class*="st-key-card"] { padding: 1.25rem 1.35rem !important; box-shadow: 0 20px 60px -30px rgba(0,0,0,.8); }
.card {
    background: linear-gradient(180deg, rgba(17,22,40,.72), rgba(11,15,28,.72));
    border: 1px solid var(--border); border-radius: var(--r-lg); padding: 1.25rem 1.35rem;
    transition: border-color var(--ease), transform var(--ease), box-shadow var(--ease); height: 100%;
}
.card:hover { border-color: var(--border-h); transform: translateY(-2px); box-shadow: 0 14px 40px -18px rgba(0,0,0,.7); }
.card h4 { font-size: 1.02rem !important; font-weight: 600 !important; margin: 0 0 .35rem 0 !important; padding: 0 !important; }
.card p { font-size: .93rem; margin: 0; }
.icon-badge {
    width: 38px; height: 38px; border-radius: 10px; display: grid; place-items: center; margin-bottom: .8rem;
    background: rgba(91,138,245,.10); border: 1px solid rgba(91,138,245,.22); color: var(--accent-2);
    font-family: var(--fm); font-weight: 600; font-size: 13px;
}
.icon-badge.green { background: var(--green-dim); border-color: rgba(62,207,142,.25); color: var(--green); }
.grid { display: grid; gap: 14px; }
.grid.c2 { grid-template-columns: repeat(2, minmax(0,1fr)); }
.grid.c3 { grid-template-columns: repeat(3, minmax(0,1fr)); }
.grid.c4 { grid-template-columns: repeat(4, minmax(0,1fr)); }
@media (max-width: 900px) { .grid.c3, .grid.c4 { grid-template-columns: repeat(2, minmax(0,1fr)); } }
@media (max-width: 600px) { .grid.c2, .grid.c3, .grid.c4 { grid-template-columns: 1fr; } }

/* ── Steps (how it works) ───────────────────────────────────────── */
.steps { display: grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap: 12px; }
.step { display: flex; gap: 12px; align-items: flex-start; padding: 1rem 1.1rem; border-radius: 12px; border: 1px solid var(--border); background: rgba(11,15,28,.6); }
.step .n { flex: 0 0 30px; height: 30px; border-radius: 50%; display: grid; place-items: center; font-family: var(--fm); font-size: 12px; font-weight: 600; color: var(--green); border: 1.5px solid rgba(62,207,142,.55); background: var(--green-dim); }
.step b { display: block; color: var(--white); font-size: .98rem; margin-bottom: 2px; }
.step span { color: var(--muted); font-size: .88rem; line-height: 1.45; }
@media (max-width: 760px) { .steps { grid-template-columns: 1fr; } }

/* ── Pipeline (About) ───────────────────────────────────────────── */
.pipeline { position: relative; display: grid; gap: 10px; }
.pipe { display: grid; grid-template-columns: 44px 1fr; gap: 14px; align-items: start; padding: .95rem 1.1rem; border-radius: 12px; border: 1px solid var(--border); background: rgba(11,15,28,.6); }
.pipe .k { width: 44px; height: 44px; border-radius: 12px; display: grid; place-items: center; font-family: var(--fm); font-size: 13px; font-weight: 600; color: var(--accent-2); background: rgba(91,138,245,.10); border: 1px solid rgba(91,138,245,.24); }
.pipe b { color: var(--white); font-size: 1rem; }
.pipe p { margin: .15rem 0 0; font-size: .92rem; }

/* ── Element tiles ──────────────────────────────────────────────── */
.elements { display: grid; grid-template-columns: repeat(auto-fill, minmax(78px, 1fr)); gap: 10px; }
.el { border-radius: 12px; border: 1px solid var(--border); background: rgba(17,22,40,.7); padding: .6rem .7rem .55rem; position: relative; }
.el .sym { font-family: var(--fh); font-size: 1.55rem; font-weight: 700; color: var(--white); line-height: 1.1; }
.el .nm { font-size: 10.5px; color: var(--muted); }
.el .val { position: absolute; top: 7px; right: 9px; font-family: var(--fm); font-size: 10px; color: var(--accent-2); }
.el.c { border-color: rgba(91,138,245,.4); background: rgba(91,138,245,.10); }
.el.h .sym { color: var(--text-2); }

/* ── Inputs ─────────────────────────────────────────────────────── */
[data-testid="stTextInput"] input {
    background: var(--surface-2) !important; color: var(--white) !important;
    font-family: var(--fm) !important; font-size: 17px !important; letter-spacing: .02em;
    padding: 12px 16px !important; height: 50px !important;
}
[data-testid="stTextInput"] [data-baseweb="input"], [data-testid="stTextInput"] [data-baseweb="base-input"] {
    background: var(--surface-2) !important; border-radius: 10px !important; border-color: var(--border) !important;
}
[data-testid="stTextInput"] [data-baseweb="input"]:focus-within {
    border-color: var(--accent) !important; box-shadow: 0 0 0 3px var(--accent-glow) !important;
}
[data-testid="stTextInput"] input::placeholder { color: var(--muted) !important; }
[data-testid="stWidgetLabel"] p, .field-label {
    font-family: var(--fm) !important; color: var(--text-2) !important; font-size: 11px !important;
    font-weight: 500 !important; letter-spacing: .12em !important; text-transform: uppercase !important;
}
[data-testid="InputInstructions"] { display: none !important; }
[data-testid="stRadio"] label p { font-family: var(--fh) !important; font-size: 14.5px !important; color: var(--white) !important; letter-spacing: 0 !important; text-transform: none !important; }
[data-testid="stRadio"] [data-testid="stWidgetLabel"] p { font-family: var(--fm) !important; font-size: 11px !important; color: var(--text-2) !important; letter-spacing: .12em !important; text-transform: uppercase !important; }

/* ── Buttons ────────────────────────────────────────────────────── */
[data-testid="stBaseButton-primary"] {
    background: linear-gradient(135deg, #5b8af5 0%, #4a74e0 100%) !important; border: 1px solid rgba(123,163,255,.5) !important;
    color: #fff !important; border-radius: 10px !important; height: 50px; font-weight: 600 !important;
    box-shadow: 0 8px 26px -10px rgba(91,138,245,.8) !important; transition: all var(--ease) !important;
}
[data-testid="stBaseButton-primary"] p { font-family: var(--fh) !important; font-size: 15.5px !important; font-weight: 600 !important; color: #fff !important; }
[data-testid="stBaseButton-primary"]:hover { transform: translateY(-1px); box-shadow: 0 12px 30px -10px rgba(91,138,245,.95) !important; filter: brightness(1.07); }
[data-testid="stBaseButton-primary"]:disabled { opacity: .45; filter: grayscale(.4); box-shadow: none !important; }
[data-testid="stBaseButton-secondary"], [data-testid="stBaseButton-tertiary"] {
    background: rgba(17,22,40,.8) !important; border: 1px solid var(--border) !important; border-radius: 999px !important;
    color: var(--text-2) !important; transition: all var(--ease) !important; min-height: 32px !important; padding: 2px 14px !important;
}
[data-testid="stBaseButton-secondary"] p { font-family: var(--fm) !important; font-size: 12.5px !important; color: var(--text-2) !important; }
[data-testid="stBaseButton-secondary"]:hover { border-color: rgba(91,138,245,.45) !important; background: rgba(91,138,245,.10) !important; }
[data-testid="stBaseButton-secondary"]:hover p { color: var(--accent-2) !important; }

[data-testid="stDownloadButton"] button, [data-testid="stLinkButton"] a {
    border-radius: 10px !important; height: 42px !important; min-height: 42px !important; padding: 0 16px !important;
    border: 1px solid rgba(91,138,245,0.30) !important; background: rgba(91,138,245,0.08) !important;
    transition: all var(--ease) !important; text-decoration: none !important; width: 100%;
}
[data-testid="stDownloadButton"] button p, [data-testid="stLinkButton"] a p,
[data-testid="stDownloadButton"] button span, [data-testid="stLinkButton"] a span {
    font-family: var(--fm) !important; font-size: 12.5px !important; font-weight: 500 !important;
    color: var(--accent-2) !important; white-space: nowrap !important;
}
[data-testid="stDownloadButton"] button:hover, [data-testid="stLinkButton"] a:hover {
    background: rgba(91,138,245,0.16) !important; border-color: rgba(91,138,245,.55) !important;
    box-shadow: 0 0 18px rgba(91,138,245,.18) !important; transform: translateY(-1px);
}
.st-key-elaya-btn [data-testid="stLinkButton"] a, div[class*="st-key-green"] [data-testid="stLinkButton"] a {
    border-color: rgba(62,207,142,0.32) !important; background: rgba(62,207,142,0.08) !important;
}
.st-key-elaya-btn [data-testid="stLinkButton"] a p, div[class*="st-key-green"] [data-testid="stLinkButton"] a p { color: var(--green) !important; }
.st-key-elaya-btn [data-testid="stLinkButton"] a:hover, div[class*="st-key-green"] [data-testid="stLinkButton"] a:hover {
    background: rgba(62,207,142,0.15) !important; border-color: rgba(62,207,142,.55) !important; box-shadow: 0 0 18px rgba(62,207,142,.16) !important;
}

.st-key-clear button { border-radius: 10px !important; height: 42px !important; min-height: 42px !important; width: 100%; }
.st-key-clear button p { font-family: var(--fm) !important; font-size: 12.5px !important; }

/* ── Formula analysis panel ─────────────────────────────────────── */
.analysis { border-radius: 12px; border: 1px solid var(--border); background: rgba(2,4,10,.55); padding: 1rem 1.1rem; margin-bottom: .35rem; }
.analysis .head { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: .7rem; }
.analysis .f { font-family: var(--fh); font-size: 1.7rem; font-weight: 700; color: var(--white); letter-spacing: .01em; }
.analysis .f sub { font-size: .62em; color: var(--accent-2); }
.analysis .lbl { font-family: var(--fm); font-size: 10px; letter-spacing: .14em; text-transform: uppercase; color: var(--muted); }
.kv { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
.kv div { border-radius: 10px; background: rgba(17,22,40,.8); border: 1px solid var(--border); padding: .55rem .65rem; }
.kv b { display: block; font-family: var(--fm); font-size: 1.15rem; font-weight: 600; color: var(--white); }
.kv span { font-family: var(--fm); font-size: 9.5px; letter-spacing: .1em; text-transform: uppercase; color: var(--muted); }
.atoms { display: flex; flex-wrap: wrap; gap: 6px; margin-top: .7rem; }
.atoms span { font-family: var(--fm); font-size: 11.5px; padding: 3px 9px; border-radius: 999px; background: rgba(91,138,245,.08); border: 1px solid rgba(91,138,245,.2); color: var(--accent-2); }
.msg { margin-top: .75rem; font-size: 13px; line-height: 1.5; padding: .6rem .75rem; border-radius: 9px; }
.msg.err { color: #ffb4ad; background: rgba(245,103,91,.09); border: 1px solid rgba(245,103,91,.28); }
.msg.warn { color: #ffd9a1; background: rgba(245,184,91,.08); border: 1px solid rgba(245,184,91,.28); }
.msg.ok { color: #9ff0c9; background: var(--green-dim); border: 1px solid rgba(62,207,142,.25); }
[data-testid="stMarkdownContainer"] p.soon { font-family: var(--fm) !important; font-size: 11.5px !important; color: var(--muted) !important; margin: .1rem 0 0; }
.soon b { color: var(--amber); font-weight: 500; }

/* ── Results ────────────────────────────────────────────────────── */
.result-banner {
    font-family: var(--fm); font-size: 11.5px; letter-spacing: .1em; text-transform: uppercase;
    color: var(--green); background: var(--green-dim); border: 1px solid rgba(62,207,142,0.2);
    border-left: 3px solid var(--green); padding: 9px 16px; border-radius: var(--r); display: inline-flex; gap: 8px; align-items: center;
}
.stats { display: grid; grid-template-columns: repeat(4, minmax(0,1fr)); gap: 12px; margin: .9rem 0 .9rem; }
.stat { border-radius: 12px; border: 1px solid var(--border); background: linear-gradient(180deg, rgba(17,22,40,.75), rgba(11,15,28,.75)); padding: .9rem 1rem; }
.stat b { display: block; font-family: var(--fh); font-size: 1.75rem; font-weight: 700; color: var(--white); line-height: 1.1; }
.stat b.g { color: var(--green); }
.stat span { font-family: var(--fm); font-size: 10px; letter-spacing: .12em; text-transform: uppercase; color: var(--muted); }
@media (max-width: 760px) { .stats { grid-template-columns: repeat(2, minmax(0,1fr)); } }
iframe { border-radius: var(--r-lg) !important; border: 1px solid var(--border) !important; background: var(--surface) !important; }

/* ── Alerts / expanders / code ──────────────────────────────────── */
[data-testid="stAlert"] > div { background: var(--surface) !important; border: 1px solid var(--border) !important; border-left: 3px solid var(--accent) !important; border-radius: var(--r) !important; }
[data-testid="stExpander"] details { background: rgba(11,15,28,.6) !important; border: 1px solid var(--border) !important; border-radius: 12px !important; }
[data-testid="stExpander"] summary p { font-family: var(--fh) !important; color: var(--white) !important; font-weight: 500; }
[data-testid="stCode"] pre, [data-testid="stCode"] > div { background: #070a14 !important; border-radius: 12px !important; }
[data-testid="stCode"] { border: 1px solid var(--border); border-radius: 12px; }
[data-testid="stCode"] code, [data-testid="stCode"] code * { font-size: 12.5px !important; font-family: var(--fm) !important; }
[data-testid="stSpinner"] p, [data-testid="stSpinner"] i { color: var(--accent-2) !important; }

/* ── Publications ───────────────────────────────────────────────── */
.pub { display: grid; grid-template-columns: 112px 1fr; gap: 1.2rem; align-items: start; }
.pub img { width: 112px; border-radius: 8px; border: 1px solid var(--border); box-shadow: 0 10px 30px -12px rgba(0,0,0,.9); display: block; }
.pub .meta { font-family: var(--fm); font-size: 11px; letter-spacing: .08em; text-transform: uppercase; color: var(--accent-dim); margin-bottom: .35rem; }
.pub h3 { font-size: 1.12rem !important; font-weight: 600 !important; line-height: 1.35 !important; margin: 0 0 .45rem 0 !important; padding: 0 !important; }
.pub .au { font-size: .9rem; color: var(--muted); margin: 0 0 .6rem 0; }
.pub .ref { font-family: var(--fm); font-size: 12px; color: var(--text-2); }
.pub .actions { display: flex; flex-wrap: wrap; gap: 8px; margin-top: .8rem; }
.btn-link {
    font-family: var(--fm); font-size: 12px; font-weight: 500; padding: 7px 13px; border-radius: 9px; text-decoration: none !important;
    color: var(--accent-2) !important; border: 1px solid rgba(91,138,245,.3); background: rgba(91,138,245,.08); transition: all var(--ease); white-space: nowrap;
    display: inline-flex; align-items: center; gap: 6px;
}
.btn-link:hover { background: rgba(91,138,245,.16); border-color: rgba(91,138,245,.55); }
.btn-link.green { color: var(--green) !important; border-color: rgba(62,207,142,.3); background: rgba(62,207,142,.08); }
.btn-link.green:hover { background: rgba(62,207,142,.15); border-color: rgba(62,207,142,.55); }
.btn-link.ghost { color: var(--text-2) !important; border-color: var(--border); background: transparent; }
.tagpill { font-family: var(--fm); font-size: 10px; letter-spacing: .08em; text-transform: uppercase; padding: 3px 8px; border-radius: 999px; border: 1px solid var(--border); color: var(--text-2); }
.tagpill.green { color: var(--green); border-color: rgba(62,207,142,.3); background: var(--green-dim); }
.featured { position: relative; overflow: hidden; border-color: rgba(91,138,245,.32); }
.featured::after { content: ""; position: absolute; inset: -1px; pointer-events: none; border-radius: inherit; background: radial-gradient(600px 200px at 0% 0%, rgba(91,138,245,.12), transparent 70%); }
@media (max-width: 600px) { .pub { grid-template-columns: 80px 1fr; gap: .9rem; } .pub img { width: 80px; } }

/* ── Team ───────────────────────────────────────────────────────── */
.member { text-align: left; display: flex; flex-direction: column; gap: .8rem; }
.member .top { display: flex; gap: .9rem; align-items: center; }
.member img { width: 68px; height: 68px; border-radius: 50%; object-fit: cover; border: 2px solid rgba(91,138,245,.35); box-shadow: 0 0 0 4px rgba(91,138,245,.07); flex: 0 0 auto; }
.member h4 { margin: 0 !important; font-size: 1.02rem !important; line-height: 1.25 !important; }
.member .role { font-family: var(--fm); font-size: 10.5px; letter-spacing: .08em; text-transform: uppercase; color: var(--accent-2); margin-top: 3px; }
.member p { font-size: .9rem; }
.member .links { display: flex; gap: 8px; margin-top: auto; }

/* ── Footer ─────────────────────────────────────────────────────── */
.smilx-footer { margin-top: 3.5rem; padding: 1.6rem 0 .5rem; border-top: 1px solid var(--border); display: grid; grid-template-columns: 1.4fr 1fr 1fr; gap: 1.5rem; }
.smilx-footer img { height: 20px; width: auto; margin-bottom: .6rem; opacity: .95; }
.smilx-footer p { font-size: 12.5px; color: var(--muted); margin: 0 0 .25rem; line-height: 1.6; }
.smilx-footer h5 { font-family: var(--fm); font-size: 10px; letter-spacing: .14em; text-transform: uppercase; color: var(--text-2); margin: 0 0 .6rem; font-weight: 500; }
.smilx-footer a { display: block; font-size: 13px; color: var(--muted); text-decoration: none; margin-bottom: .3rem; transition: color var(--ease); }
.smilx-footer a:hover { color: var(--accent-2); }
.smilx-footer .credits { grid-column: 1 / -1; display: flex; flex-wrap: wrap; justify-content: space-between; gap: .5rem; border-top: 1px solid var(--border); padding-top: 1rem; margin-top: .4rem; }
.smilx-footer .credits span { font-family: var(--fm); font-size: 10.5px; letter-spacing: .05em; color: var(--muted); }
.smilx-footer .credits b { color: var(--text-2); font-weight: 500; }
@media (max-width: 760px) { .smilx-footer { grid-template-columns: 1fr 1fr; } .smilx-footer > div:first-child { grid-column: 1 / -1; } }

/* ── Motion ─────────────────────────────────────────────────────── */
@keyframes fadeUp { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: none; } }
.fade { animation: fadeUp .45s cubic-bezier(.2,.7,.2,1) both; }
.fade.d1 { animation-delay: .06s; } .fade.d2 { animation-delay: .12s; } .fade.d3 { animation-delay: .18s; }
@media (prefers-reduced-motion: reduce) { .fade { animation: none; } .card:hover { transform: none; } }
</style>
"""


def inject_theme() -> None:
    st.html(CSS)
