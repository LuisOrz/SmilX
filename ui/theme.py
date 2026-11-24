"""
SmilX design system · Material Design dark theme
------------------------------------------------
SmilX identity (navy space, SmilX blue, mint green, Outfit + IBM Plex Mono)
expressed with the Material Design dark-theme rules:

* No pure black: a navy-tinted dark surface (#0e111a) lets elevation show.
* Elevation = lighter tonal surfaces (surface-1 … surface-4), not heavy shadows.
* Text emphasis: high (≈87 %), medium (≈70 %) and low (≈55 %) on-surface tones,
  all ≥ 4.5:1 against every surface, so important information never fades.
* Desaturated primary (tone 80 of SmilX blue, #adc6ff) for text, icons and
  filled buttons with dark "on-primary" text; the saturated #5b8af5 is kept
  for glows, focus rings and the brand gradient only.
* Every widget is styled here explicitly, so the look does not depend on
  .streamlit/config.toml being found.
"""
import base64

import streamlit as st

CSS = r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Outfit:wght@400;500;600;700;800&display=swap');

:root {
    color-scheme: dark;
    /* Surfaces (elevation dp0 → dp4) */
    --bg:          #0e111a;
    --surface:     #151924;   /* dp1  cards                 */
    --surface-2:   #1a1f2c;   /* dp2  inputs, inner panels  */
    --surface-3:   #20263a;   /* dp3  hover, chips          */
    --surface-4:   #272e44;   /* dp4  menus, tooltips       */
    --outline-v:   #2b3247;   /* subtle borders             */
    --outline:     #4a5470;   /* emphasized borders         */
    /* Text emphasis */
    --on:          #e6e8f0;   /* high   ≈ 87 %  (15.6:1) */
    --on-2:        #b8bfd2;   /* medium ≈ 70 %  (10.0:1) */
    --on-3:        #8c94ab;   /* low    ≈ 55 %  ( 6.0:1) */
    --on-dis:      rgba(230,232,240,.38);
    /* SmilX blue, Material tones */
    --brand:       #5b8af5;   /* identity: glows, rings, gradients */
    --primary:     #adc6ff;   /* tone 80: text, icons, filled bg   */
    --primary-h:   #c4d5ff;
    --on-primary:  #0b2a63;
    --primary-c:   #233a6b;   /* container */
    --on-primary-c:#d9e2ff;
    --primary-08:  rgba(173,198,255,.08);
    --primary-12:  rgba(173,198,255,.12);
    --primary-24:  rgba(173,198,255,.24);
    /* SmilX mint (success / secondary) */
    --green:       #6fdba6;
    --green-c:     #133d2b;
    --on-green-c:  #a8f2cc;
    --green-12:    rgba(111,219,166,.12);
    /* Feedback */
    --error:       #ffb4ab;
    --error-c:     #5a1d19;
    --warn:        #f5c36b;
    --warn-c:      #4a3510;

    --r: 10px; --r-lg: 16px; --r-xl: 28px;
    --nav-h: 60px; --maxw: 1180px;
    --fh: 'Outfit', system-ui, sans-serif;
    --fm: 'IBM Plex Mono', ui-monospace, monospace;
    --ease: 0.18s cubic-bezier(.2,0,0,1);
    --e1: 0 1px 2px rgba(0,0,0,.45), 0 1px 3px 1px rgba(0,0,0,.25);
    --e3: 0 4px 8px 3px rgba(0,0,0,.30), 0 1px 3px rgba(0,0,0,.45);
}

/* ── Streamlit chrome ───────────────────────────────────────────── */
#MainMenu, footer,
[data-testid="stHeader"], [data-testid="stDecoration"],
[data-testid="stToolbar"], [data-testid="stStatusWidget"],
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebarNav"] { display: none !important; }

html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: var(--bg) !important; color: var(--on) !important; font-family: var(--fh) !important;
}
[data-testid="stAppViewContainer"]::before {
    content: ""; position: fixed; inset: 0; pointer-events: none; z-index: 0;
    background:
        radial-gradient(900px 440px at 50% -140px, rgba(91,138,245,0.13), transparent 70%),
        radial-gradient(rgba(173,198,255,0.05) 1px, transparent 1px);
    background-size: auto, 28px 28px;
    mask-image: linear-gradient(to bottom, #000 0%, #000 45%, transparent 95%);
}
[data-testid="stMain"] { position: relative; z-index: 1; }
[data-testid="stMainBlockContainer"], .block-container {
    max-width: var(--maxw) !important;
    padding: calc(var(--nav-h) + 1.75rem) 1.5rem 2rem !important;
}
[data-testid="stVerticalBlock"] { gap: 0.85rem; }
::selection { background: rgba(173,198,255,.30); }
*:focus-visible { outline: 2px solid var(--primary) !important; outline-offset: 2px; }

/* ── Typography ─────────────────────────────────────────────────── */
p, li, label { font-family: var(--fh); }
p, li { color: var(--on-2); line-height: 1.65; }
strong, b { color: var(--on); font-weight: 600; }
h1, h2, h3, h4 { font-family: var(--fh) !important; color: var(--on) !important; }
a { color: var(--primary); }
code { font-family: var(--fm) !important; }
[data-testid="stMarkdownContainer"] p code, li code {
    background: var(--primary-08) !important; color: var(--primary) !important;
    border: 1px solid var(--primary-12); border-radius: 6px; padding: 1px 6px;
}
[data-testid="stHeadingWithActionElements"] a, [data-testid="stHeaderActionElements"] { display: none !important; }
hr { border: none !important; border-top: 1px solid var(--outline-v) !important; margin: 1.5rem 0 !important; }

/* ── Navbar ─────────────────────────────────────────────────────── */
.st-key-smilx-nav {
    position: fixed !important; top: 0; left: 0; right: 0; z-index: 999990; height: var(--nav-h);
    background: rgba(14,17,26,0.86);
    backdrop-filter: blur(16px) saturate(140%); -webkit-backdrop-filter: blur(16px) saturate(140%);
    border-bottom: 1px solid var(--outline-v);
    display: flex !important; flex-direction: row !important; align-items: center !important;
    gap: 4px !important; padding: 0 max(1.5rem, calc((100vw - var(--maxw)) / 2 + 1.5rem)) !important;
    overflow-x: auto; scrollbar-width: none;
}
.st-key-smilx-nav::-webkit-scrollbar { display: none; }
.st-key-smilx-nav > div { width: auto !important; flex: 0 0 auto !important; }
.st-key-smilx-nav > div:first-child { margin-right: auto; }
.st-key-smilx-nav [data-testid="stElementContainer"] { width: auto !important; margin-top: 0 !important; margin-bottom: 0 !important; }
.st-key-smilx-nav [data-testid="stMarkdownContainer"] { margin: 0 !important; }
.st-key-smilx-nav [data-testid="stMarkdown"] { display: flex; align-items: center; }
.smilx-brand { margin: 0; display: flex; align-items: center; gap: 10px; }
.smilx-brand img { height: 22px; width: auto; display: block; }
.smilx-brand .tag {
    font-family: var(--fm); font-size: 10px; letter-spacing: .12em; text-transform: uppercase; white-space: nowrap;
    color: var(--primary); background: var(--primary-08); border: 1px solid var(--primary-24); padding: 3px 8px; border-radius: 999px;
}
.st-key-smilx-nav a[data-testid="stPageLink-NavLink"] {
    padding: 8px 14px !important; border-radius: 999px !important; margin: 0 !important;
    border: none !important; background: transparent !important; transition: background var(--ease) !important;
}
.st-key-smilx-nav a[data-testid="stPageLink-NavLink"] p {
    font-family: var(--fh) !important; font-size: 14px !important; font-weight: 500 !important;
    color: var(--on-2) !important; white-space: nowrap !important; line-height: 1 !important; margin: 0 !important;
}
.st-key-smilx-nav a[data-testid="stPageLink-NavLink"]:hover { background: rgba(230,232,240,.08) !important; }
.st-key-smilx-nav a[data-testid="stPageLink-NavLink"]:hover p { color: var(--on) !important; }
.st-key-smilx-nav div[class*="st-key-nav-on"] { width: auto !important; flex: 0 0 auto !important; }
.st-key-smilx-nav div[class*="st-key-nav-on"] a[data-testid="stPageLink-NavLink"] { background: var(--primary-c) !important; }
.st-key-smilx-nav div[class*="st-key-nav-on"] a[data-testid="stPageLink-NavLink"] p { color: var(--on-primary-c) !important; font-weight: 600 !important; }
@media (max-width: 760px) {
    :root { --nav-h: 56px; }
    .smilx-brand .tag { display: none; }
    .st-key-smilx-nav { padding: 0 .75rem !important;
        -webkit-mask-image: linear-gradient(90deg, #000 84%, transparent); mask-image: linear-gradient(90deg, #000 84%, transparent); }
    .st-key-smilx-nav a[data-testid="stPageLink-NavLink"] { padding: 7px 10px !important; }
    .st-key-smilx-nav a[data-testid="stPageLink-NavLink"] p { font-size: 13px !important; }
    [data-testid="stMainBlockContainer"], .block-container { padding-left: 1rem !important; padding-right: 1rem !important; }
}

/* In-page links styled as tonal green buttons */
div[class*="st-key-green"] a[data-testid="stPageLink-NavLink"] {
    display: inline-flex !important; padding: 9px 16px !important; border-radius: 999px !important;
    background: var(--green-c) !important; border: none !important; transition: filter var(--ease) !important;
}
div[class*="st-key-green"] a[data-testid="stPageLink-NavLink"] p { font-family: var(--fh) !important; font-weight: 600 !important; font-size: 14px !important; color: var(--on-green-c) !important; margin: 0 !important; }
div[class*="st-key-green"] a[data-testid="stPageLink-NavLink"]:hover { filter: brightness(1.18); }

/* ── Page header ────────────────────────────────────────────────── */
.eyebrow {
    font-family: var(--fm); font-size: 12px; font-weight: 500; letter-spacing: .14em; text-transform: uppercase;
    color: var(--primary); display: inline-flex; align-items: center; gap: 8px; margin-bottom: .6rem;
}
.eyebrow::before { content: ""; width: 18px; height: 2px; border-radius: 2px; background: var(--primary); }
.page-title { font-family: var(--fh); font-weight: 700; letter-spacing: -0.025em; line-height: 1.08;
    font-size: clamp(2rem, 4.4vw, 3rem); color: var(--on); margin: 0 0 .7rem 0; }
.page-title .grad, .grad {
    background: linear-gradient(92deg, var(--primary), #c9d8ff 45%, var(--green));
    -webkit-background-clip: text; background-clip: text; color: transparent;
}
.page-lead { font-size: 1.08rem; color: var(--on-2); max-width: 760px; margin: 0 0 1.4rem 0; line-height: 1.65; }
.section-title { font-family: var(--fh); font-weight: 650; font-size: 1.35rem; color: var(--on); margin: 0 0 .3rem 0; letter-spacing: -0.01em; }
.section-sub { color: var(--on-3); font-size: .97rem; margin: 0 0 1rem 0; }
.section-gap { height: 2rem; }

/* ── Hero ───────────────────────────────────────────────────────── */
.hero { text-align: center; padding: .25rem 0 0; }
.hero-logo { width: min(380px, 76vw); height: auto; filter: drop-shadow(0 0 26px rgba(91,138,245,.32)); margin: .1rem auto 1rem; display: block; }
.hero h1.tagline { font-family: var(--fh) !important; font-weight: 600 !important; font-size: clamp(1.2rem, 2.6vw, 1.6rem) !important;
    letter-spacing: -0.01em; color: var(--on) !important; margin: 0 0 .5rem 0 !important; padding: 0 !important; }
.hero p.sub { max-width: 680px; margin: 0 auto 1rem; color: var(--on-2); font-size: 1.02rem; }
.chips { display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; margin: .25rem 0 0; }
.chip { font-family: var(--fm); font-size: 11.5px; letter-spacing: .02em; color: var(--on-2); padding: 5px 12px; border-radius: 8px;
    border: 1px solid var(--outline-v); background: var(--surface); display: inline-flex; align-items: center; gap: 6px;
    text-decoration: none !important; white-space: nowrap; }
.chip .dot { width: 7px; height: 7px; border-radius: 50%; background: var(--green); }
.chip.blue { color: var(--on-primary-c); border-color: transparent; background: var(--primary-c); }
a.chip:hover { filter: brightness(1.15); }
.credit { max-width: 760px; margin: 1.1rem auto 0; padding: .9rem 1.2rem; border-radius: var(--r-lg); background: var(--surface); border: 1px solid var(--outline-v); text-align: center; }
.credit .t { font-family: var(--fm); font-style: italic; font-size: 12.5px; color: var(--on-2); margin: 0 0 .35rem; }
.credit .a { font-size: 13px; color: var(--on-3); margin: 0 0 .3rem; line-height: 1.6; }
.credit .i { font-family: var(--fm); font-size: 10.5px; letter-spacing: .1em; text-transform: uppercase; color: var(--primary); opacity: .85; margin: 0; }

/* ── Cards / surfaces ───────────────────────────────────────────── */
div[class*="st-key-card"] {
    background: var(--surface) !important; border: 1px solid var(--outline-v) !important;
    border-radius: var(--r-xl) !important; padding: 1.4rem 1.5rem 1.3rem !important; box-shadow: var(--e1);
}
.card { background: var(--surface); border: 1px solid var(--outline-v); border-radius: var(--r-lg); padding: 1.25rem 1.35rem;
    transition: background var(--ease), border-color var(--ease), box-shadow var(--ease); height: 100%; }
.card:hover { background: var(--surface-2); border-color: var(--outline); box-shadow: var(--e3); }
.card h4 { font-size: 1.04rem !important; font-weight: 600 !important; margin: 0 0 .35rem 0 !important; padding: 0 !important; }
.card p { font-size: .95rem; margin: 0; }
.icon-badge { width: 40px; height: 40px; border-radius: 12px; display: grid; place-items: center; margin-bottom: .8rem;
    background: var(--primary-c); color: var(--on-primary-c); font-family: var(--fm); font-weight: 600; font-size: 13px; }
.icon-badge.green { background: var(--green-c); color: var(--on-green-c); }
.grid { display: grid; gap: 14px; }
.grid.c2 { grid-template-columns: repeat(2, minmax(0,1fr)); }
.grid.c3 { grid-template-columns: repeat(3, minmax(0,1fr)); }
.grid.c4 { grid-template-columns: repeat(4, minmax(0,1fr)); }
@media (max-width: 900px) { .grid.c3, .grid.c4 { grid-template-columns: repeat(2, minmax(0,1fr)); } }
@media (max-width: 600px) { .grid.c2, .grid.c3, .grid.c4 { grid-template-columns: 1fr; } }

/* Steps / pipeline */
.steps { display: grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap: 12px; }
.step { display: flex; gap: 12px; align-items: flex-start; padding: 1rem 1.1rem; border-radius: var(--r-lg); background: var(--surface); border: 1px solid var(--outline-v); }
.step .n { flex: 0 0 32px; height: 32px; border-radius: 50%; display: grid; place-items: center; font-family: var(--fm); font-size: 13px; font-weight: 600; color: var(--on-green-c); background: var(--green-c); }
.step b { display: block; color: var(--on); font-size: 1rem; margin-bottom: 2px; }
.step span { color: var(--on-2); font-size: .9rem; line-height: 1.5; }
@media (max-width: 760px) { .steps { grid-template-columns: 1fr; } }
.pipeline { display: grid; gap: 10px; }
.pipe { display: grid; grid-template-columns: 44px 1fr; gap: 14px; align-items: start; padding: .95rem 1.1rem; border-radius: var(--r-lg); background: var(--surface); border: 1px solid var(--outline-v); }
.pipe .k { width: 44px; height: 44px; border-radius: 12px; display: grid; place-items: center; font-family: var(--fm); font-size: 13px; font-weight: 600; color: var(--on-primary-c); background: var(--primary-c); }
.pipe b { color: var(--on); font-size: 1rem; }
.pipe p { margin: .15rem 0 0; font-size: .94rem; }

/* Element tiles */
.elements { display: grid; grid-template-columns: repeat(auto-fill, minmax(80px, 1fr)); gap: 10px; }
.el { border-radius: 12px; background: var(--surface); border: 1px solid var(--outline-v); padding: .6rem .7rem .55rem; position: relative; }
.el .sym { font-family: var(--fh); font-size: 1.55rem; font-weight: 700; color: var(--on); line-height: 1.1; }
.el .nm { font-size: 11px; color: var(--on-3); }
.el .val { position: absolute; top: 7px; right: 9px; font-family: var(--fm); font-size: 11px; color: var(--primary); }
.el.c { background: var(--primary-c); border-color: transparent; }
.el.c .nm { color: var(--on-primary-c); }

/* ── Field labels ───────────────────────────────────────────────── */
[data-testid="stWidgetLabel"] p, .field-label {
    font-family: var(--fh) !important; color: var(--on-2) !important; font-size: 13px !important;
    font-weight: 600 !important; letter-spacing: .01em !important; text-transform: none !important;
}
[data-testid="stWidgetLabel"] [data-testid="stTooltipHoverTarget"] svg, [data-testid="stTooltipIcon"] svg { color: var(--on-3) !important; stroke: var(--on-3) !important; }
.hint { font-size: 12.5px; color: var(--on-3); margin: .35rem 0 0; line-height: 1.5; }
.hint kbd { font-family: var(--fm); font-size: 11px; color: var(--on-2); background: var(--surface-3); border: 1px solid var(--outline); border-bottom-width: 2px; border-radius: 5px; padding: 0 5px; }

/* ── Text input (Material outlined field) ───────────────────────── */
[data-testid="stTextInput"] [data-baseweb="input"], [data-testid="stTextInput"] [data-baseweb="base-input"] {
    background: var(--surface-2) !important; border-radius: 12px !important;
}
[data-testid="stTextInput"] [data-baseweb="input"] { border: 1px solid var(--outline) !important; }
[data-testid="stTextInput"] [data-baseweb="input"]:hover { border-color: var(--on-3) !important; }
[data-testid="stTextInput"] [data-baseweb="input"]:focus-within { border-color: var(--primary) !important; box-shadow: 0 0 0 1px var(--primary) !important; }
[data-testid="stTextInput"] input {
    background: transparent !important; color: var(--on) !important; caret-color: var(--primary);
    font-family: var(--fm) !important; font-size: 18px !important; font-weight: 500; letter-spacing: .03em;
    padding: 12px 16px !important; height: 52px !important;
}
[data-testid="stTextInput"] input::placeholder { color: var(--on-3) !important; }
[data-testid="InputInstructions"] { display: none !important; }

/* ── Pills & segmented control ──────────────────────────────────── */
[data-testid="stButtonGroup"] { gap: 8px !important; flex-wrap: wrap; }
[data-testid="stButtonGroup"] button:not([aria-label^="Help"]) {
    background: var(--surface-2) !important; border: 1px solid var(--outline) !important; color: var(--on-2) !important;
    border-radius: 8px !important; min-height: 34px !important; padding: 4px 14px !important; transition: all var(--ease) !important; box-shadow: none !important;
}
[data-testid="stButtonGroup"] button:not([aria-label^="Help"]) p { font-family: var(--fm) !important; font-size: 13px !important; color: var(--on-2) !important; font-weight: 500 !important; }
[data-testid="stButtonGroup"] button:not([aria-label^="Help"]):hover { background: var(--surface-3) !important; border-color: var(--on-3) !important; }
[data-testid="stButtonGroup"] button:not([aria-label^="Help"]):hover p { color: var(--on) !important; }
[data-testid="stButtonGroup"] button:not([aria-label^="Help"])[kind$="Active"], [data-testid="stButtonGroup"] button:not([aria-label^="Help"])[aria-checked="true"],
[data-testid="stButtonGroup"] button:not([aria-label^="Help"])[aria-pressed="true"], [data-testid*="Active"] {
    background: var(--primary-c) !important; border-color: var(--primary-c) !important;
}
[data-testid="stButtonGroup"] button:not([aria-label^="Help"])[kind$="Active"] p, [data-testid="stButtonGroup"] button:not([aria-label^="Help"])[aria-checked="true"] p,
[data-testid="stButtonGroup"] button:not([aria-label^="Help"])[aria-pressed="true"] p, [data-testid*="Active"] p { color: var(--on-primary-c) !important; font-weight: 600 !important; }
/* segmented: one connected control */
.st-key-mode_input [data-testid="stButtonGroup"] { gap: 0 !important; flex-wrap: nowrap; }
.st-key-mode_input [data-testid="stButtonGroup"] button:not([aria-label^="Help"]) { border-radius: 0 !important; min-height: 40px !important; padding: 4px 18px !important; }
.st-key-mode_input [data-testid="stButtonGroup"] button:not([aria-label^="Help"]) p { font-family: var(--fh) !important; font-size: 14px !important; }
.st-key-mode_input [data-testid="stButtonGroup"] button:not([aria-label^="Help"]):first-child { border-radius: 999px 0 0 999px !important; }
.st-key-mode_input [data-testid="stButtonGroup"] button:not([aria-label^="Help"]):last-child { border-radius: 0 999px 999px 0 !important; margin-left: -1px; }

[data-testid="stWidgetLabel"] [data-testid="stTooltipIcon"] button { background: transparent !important; border: none !important; color: var(--on-3) !important; }
[data-testid="stWidgetLabel"] [data-testid="stTooltipIcon"] button:hover { color: var(--primary) !important; }
/* Radio fallback */
[data-testid="stRadio"] label p { font-family: var(--fh) !important; color: var(--on) !important; }
[data-testid="stRadio"] [role="radio"] > div:first-child, [data-baseweb="radio"] div[class] { border-color: var(--primary) !important; }

/* ── Buttons ────────────────────────────────────────────────────── */
[data-testid="stBaseButton-primary"] {
    background: var(--primary) !important; border: none !important; color: var(--on-primary) !important;
    border-radius: 999px !important; height: 52px; min-height: 52px; font-weight: 600 !important; box-shadow: var(--e1) !important;
    transition: background var(--ease), box-shadow var(--ease), transform var(--ease) !important;
}
[data-testid="stDownloadButton"] button [data-testid="stIconMaterial"], [data-testid="stLinkButton"] a [data-testid="stIconMaterial"],
[data-testid="stButton"] button [data-testid="stIconMaterial"] { color: inherit; font-size: 18px !important; }
[data-testid="stDownloadButton"] button, [data-testid="stLinkButton"] a { color: var(--primary) !important; }
.st-key-elaya-btn [data-testid="stLinkButton"] a { color: var(--on-green-c) !important; }
[data-testid="stBaseButton-primary"] p { font-family: var(--fh) !important; font-size: 16px !important; font-weight: 600 !important; color: var(--on-primary) !important; }
[data-testid="stBaseButton-primary"]:hover { background: var(--primary-h) !important; box-shadow: var(--e3), 0 0 24px rgba(91,138,245,.35) !important; }
[data-testid="stBaseButton-primary"]:active { transform: scale(.985); }
[data-testid="stBaseButton-primary"]:disabled { background: rgba(230,232,240,.12) !important; box-shadow: none !important; }
[data-testid="stBaseButton-primary"]:disabled p { color: var(--on-dis) !important; }

[data-testid="stButton"] [data-testid="stBaseButton-secondary"],
[data-testid="stDownloadButton"] button, [data-testid="stLinkButton"] a {
    background: transparent !important; border: 1px solid var(--outline) !important; border-radius: 999px !important;
    min-height: 42px !important; height: 42px; padding: 0 18px !important; text-decoration: none !important;
    transition: background var(--ease), border-color var(--ease) !important; width: 100%;
}
[data-testid="stButton"] [data-testid="stBaseButton-secondary"] p, [data-testid="stDownloadButton"] button p, [data-testid="stLinkButton"] a p {
    font-family: var(--fh) !important; font-size: 14px !important; font-weight: 600 !important; color: var(--primary) !important; white-space: nowrap !important;
}
[data-testid="stButton"] [data-testid="stBaseButton-secondary"]:hover, [data-testid="stDownloadButton"] button:hover, [data-testid="stLinkButton"] a:hover {
    background: var(--primary-08) !important; border-color: var(--primary) !important;
}
.st-key-elaya-btn [data-testid="stLinkButton"] a { background: var(--green-c) !important; border-color: transparent !important; }
.st-key-elaya-btn [data-testid="stLinkButton"] a p { color: var(--on-green-c) !important; }
.st-key-elaya-btn [data-testid="stLinkButton"] a:hover { filter: brightness(1.18); }
.st-key-clear button { border-color: var(--outline-v) !important; }
.st-key-clear button p { color: var(--on-2) !important; }

/* ── Formula analysis strip ─────────────────────────────────────── */
.analysis { display: flex; flex-wrap: wrap; align-items: center; gap: 10px 18px; padding: .8rem 1rem; border-radius: 14px;
    background: var(--surface-2); border: 1px solid var(--outline-v); margin-top: .2rem; }
.analysis .f { font-family: var(--fh); font-size: 1.6rem; font-weight: 700; color: var(--on); letter-spacing: .01em; line-height: 1; min-width: 3.5rem; }
.analysis .f sub { font-size: .6em; color: var(--primary); }
.analysis .sep { width: 1px; align-self: stretch; background: var(--outline-v); }
.analysis .m { display: flex; flex-direction: column; line-height: 1.15; }
.analysis .m b { font-family: var(--fm); font-size: 1.15rem; font-weight: 600; color: var(--on); }
.analysis .m span { font-size: 11.5px; color: var(--on-3); font-weight: 500; }
.analysis .atoms { display: flex; flex-wrap: wrap; gap: 6px; }
.analysis .atoms span { font-family: var(--fm); font-size: 12px; padding: 3px 9px; border-radius: 6px; background: var(--surface-3); color: var(--on-2); }
.status { margin-left: auto; display: inline-flex; align-items: center; gap: 7px; font-size: 13px; font-weight: 600; padding: 6px 12px; border-radius: 999px; line-height: 1.3; }
.status.ok { background: var(--green-c); color: var(--on-green-c); }
.status.warn { background: var(--warn-c); color: #ffe0a8; }
.status.err { background: var(--error-c); color: var(--error); margin-left: 0; }
.status i { font-style: normal; font-weight: 700; }
@media (max-width: 760px) { .analysis .sep { display: none; } .status { margin-left: 0; } }
.msg { font-size: 13.5px; line-height: 1.5; padding: .7rem .9rem; border-radius: 12px; margin-top: .2rem; }
.msg.err { color: var(--error); background: var(--error-c); }
.msg.warn { color: #ffe0a8; background: var(--warn-c); }
.soon { font-size: 12.5px !important; color: var(--on-3) !important; margin: .1rem 0 .3rem !important; }
.soon b { color: var(--warn); font-weight: 600; }
.soon, [data-testid="stMarkdownContainer"] p.soon { font-family: var(--fh) !important; }

/* ── Results ────────────────────────────────────────────────────── */
.result-head { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 10px; }
.result-banner { font-family: var(--fh); font-size: 15px; font-weight: 600; color: var(--on-green-c); background: var(--green-c);
    padding: 9px 16px; border-radius: 999px; display: inline-flex; gap: 8px; align-items: center; }
.result-banner sub { font-size: .7em; }
.result-banner i { font-style: normal; display: grid; place-items: center; width: 20px; height: 20px; border-radius: 50%; background: var(--green); color: var(--green-c); font-size: 12px; }
.stats { display: grid; grid-template-columns: repeat(4, minmax(0,1fr)); gap: 12px; margin: .8rem 0 .9rem; }
.stat { border-radius: var(--r-lg); background: var(--surface); border: 1px solid var(--outline-v); padding: .85rem 1rem; }
.stat b { display: block; font-family: var(--fh); font-size: 1.75rem; font-weight: 700; color: var(--on); line-height: 1.1; }
.stat b.g { color: var(--green); }
.stat span { font-size: 12.5px; font-weight: 500; color: var(--on-3); }
@media (max-width: 760px) { .stats { grid-template-columns: repeat(2, minmax(0,1fr)); } }
iframe { border-radius: var(--r-lg) !important; border: 1px solid var(--outline-v) !important; background: var(--surface) !important; }

/* ── Alerts, expander, tabs, code, toast, tooltip ───────────────── */
[data-testid="stAlert"] > div { background: var(--surface-2) !important; border: none !important; border-radius: 12px !important; color: var(--on) !important; }
[data-testid="stExpander"] details { background: var(--surface) !important; border: 1px solid var(--outline-v) !important; border-radius: 14px !important; }
[data-testid="stExpander"] summary:hover { background: var(--surface-2) !important; }
[data-testid="stExpander"] summary p { font-family: var(--fh) !important; color: var(--on) !important; font-weight: 600; }
[data-testid="stExpander"] summary svg { color: var(--on-2) !important; fill: var(--on-2) !important; }
[data-testid="stTabs"] button[role="tab"] p { font-family: var(--fh) !important; color: var(--on-3) !important; font-weight: 600 !important; font-size: 14px !important; }
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] p { color: var(--primary) !important; }
[data-testid="stTabs"] [data-baseweb="tab-highlight"] { background: var(--primary) !important; height: 3px !important; border-radius: 3px 3px 0 0; }
[data-testid="stTabs"] [data-baseweb="tab-border"] { background: var(--outline-v) !important; }
[data-testid="stCode"] { border: 1px solid var(--outline-v); border-radius: 12px; }
[data-testid="stCode"] pre, [data-testid="stCode"] > div { background: #0a0d14 !important; border-radius: 12px !important; }
[data-testid="stCode"] code, [data-testid="stCode"] code * { font-size: 12.5px !important; font-family: var(--fm) !important; }
[data-testid="stSpinner"] p, [data-testid="stSpinner"] i { color: var(--primary) !important; font-family: var(--fh) !important; }
[data-testid="stToast"] { background: var(--surface-4) !important; color: var(--on) !important; border-radius: 12px !important; box-shadow: var(--e3) !important; }
[data-testid="stToast"] p { color: var(--on) !important; font-family: var(--fh) !important; }
[data-baseweb="popover"] > div, [data-testid="stTooltipContent"] { background: var(--surface-4) !important; color: var(--on) !important; border-radius: 10px !important; }
[data-baseweb="popover"] p { color: var(--on) !important; }

/* ── Publications ───────────────────────────────────────────────── */
.pub { display: grid; grid-template-columns: 112px 1fr; gap: 1.2rem; align-items: start; }
.pub img { width: 112px; border-radius: 8px; box-shadow: var(--e3); display: block; }
.pub .meta { font-family: var(--fm); font-size: 11.5px; letter-spacing: .06em; text-transform: uppercase; color: var(--primary); margin-bottom: .35rem; }
.pub h3 { font-size: 1.14rem !important; font-weight: 600 !important; line-height: 1.35 !important; margin: 0 0 .45rem 0 !important; padding: 0 !important; }
.pub .au { font-size: .92rem; color: var(--on-3); margin: 0 0 .6rem 0; }
.pub .ref { font-family: var(--fm); font-size: 12.5px; color: var(--on-2); }
.pub .actions, .actions { display: flex; flex-wrap: wrap; gap: 8px; margin-top: .8rem; }
.btn-link { font-family: var(--fh); font-size: 13.5px; font-weight: 600; padding: 7px 15px; border-radius: 999px; text-decoration: none !important;
    color: var(--primary) !important; border: 1px solid var(--outline); background: transparent; transition: background var(--ease), border-color var(--ease);
    white-space: nowrap; display: inline-flex; align-items: center; gap: 6px; }
.btn-link:hover { background: var(--primary-08); border-color: var(--primary); }
.btn-link.green { color: var(--on-green-c) !important; background: var(--green-c); border-color: transparent; }
.btn-link.green:hover { filter: brightness(1.18); }
.btn-link.ghost { color: var(--on-2) !important; border-color: var(--outline-v); }
.tagpill { font-family: var(--fm); font-size: 10.5px; letter-spacing: .06em; text-transform: uppercase; padding: 3px 8px; border-radius: 6px; background: var(--surface-3); color: var(--on-2); }
.tagpill.green { color: var(--on-green-c); background: var(--green-c); }
.featured { border-color: var(--primary-24) !important; background: linear-gradient(135deg, rgba(35,58,107,.55), var(--surface) 55%) !important; }
@media (max-width: 600px) { .pub { grid-template-columns: 80px 1fr; gap: .9rem; } .pub img { width: 80px; } }

/* ── Team ───────────────────────────────────────────────────────── */
.member { display: flex; flex-direction: column; gap: .8rem; }
.member .top { display: flex; gap: .9rem; align-items: center; }
.member img { width: 68px; height: 68px; border-radius: 50%; object-fit: cover; border: 2px solid var(--primary-c); flex: 0 0 auto; }
.member h4 { margin: 0 !important; font-size: 1.04rem !important; line-height: 1.25 !important; }
.member .role { font-size: 12.5px; font-weight: 600; color: var(--primary); margin-top: 3px; }
.member p { font-size: .92rem; }
.member .links { display: flex; gap: 8px; margin-top: auto; }

/* ── Footer ─────────────────────────────────────────────────────── */
.smilx-footer { margin-top: 3.5rem; padding: 1.6rem 0 .5rem; border-top: 1px solid var(--outline-v); display: grid; grid-template-columns: 1.4fr 1fr 1fr; gap: 1.5rem; }
.smilx-footer img { height: 20px; width: auto; margin-bottom: .6rem; }
.smilx-footer p { font-size: 13px; color: var(--on-3); margin: 0 0 .25rem; line-height: 1.6; }
.smilx-footer h5 { font-family: var(--fh); font-size: 12px; font-weight: 600; letter-spacing: .08em; text-transform: uppercase; color: var(--on-2); margin: 0 0 .6rem; }
.smilx-footer a { display: block; font-size: 13.5px; color: var(--on-3); text-decoration: none; margin-bottom: .35rem; transition: color var(--ease); }
.smilx-footer a:hover { color: var(--primary); }
.smilx-footer .credits { grid-column: 1 / -1; display: flex; flex-wrap: wrap; justify-content: space-between; gap: .5rem; border-top: 1px solid var(--outline-v); padding-top: 1rem; margin-top: .4rem; }
.smilx-footer .credits span { font-size: 12px; color: var(--on-3); }
.smilx-footer .credits b { color: var(--on-2); font-weight: 600; }
@media (max-width: 760px) { .smilx-footer { grid-template-columns: 1fr 1fr; } .smilx-footer > div:first-child { grid-column: 1 / -1; } }

/* ── Scroll FAB (Material extended FAB) ─────────────────────────── */
#smilx-fab {
    position: fixed; right: 24px; bottom: 24px; z-index: 999995; height: 56px; min-width: 56px; padding: 0 18px;
    display: inline-flex; align-items: center; justify-content: center; gap: 10px; border: none; cursor: pointer;
    border-radius: 16px; background: var(--primary-c); color: var(--on-primary-c); box-shadow: var(--e3), 0 0 0 1px rgba(173,198,255,.10);
    font: 600 14.5px var(--fh); letter-spacing: .01em;
    opacity: 0; transform: translateY(16px) scale(.92); pointer-events: none;
    transition: opacity .25s ease, transform .25s cubic-bezier(.2,0,0,1), background .18s ease, box-shadow .18s ease;
}
#smilx-fab.show { opacity: 1; transform: none; pointer-events: auto; }
#smilx-fab:hover { background: #2c4880; box-shadow: 0 8px 12px 6px rgba(0,0,0,.30), 0 4px 4px rgba(0,0,0,.4), 0 0 22px rgba(91,138,245,.35); }
#smilx-fab:focus-visible { outline: 2px solid var(--primary); outline-offset: 3px; }
#smilx-fab svg { width: 22px; height: 22px; transition: transform .3s cubic-bezier(.2,0,0,1); }
#smilx-fab.down svg { animation: fabBounce 1.6s ease-in-out infinite; }
#smilx-fab.up svg { transform: rotate(180deg); }
#smilx-fab .lbl { white-space: nowrap; }
#smilx-fab.down.pulse { animation: fabGlow 2.4s ease-in-out infinite; }
@keyframes fabBounce { 0%,100% { transform: translateY(-2px); } 50% { transform: translateY(4px); } }
@keyframes fabGlow { 0%,100% { box-shadow: var(--e3); } 50% { box-shadow: var(--e3), 0 0 26px rgba(91,138,245,.55); } }
@media (max-width: 760px) { #smilx-fab { right: 16px; bottom: 16px; } #smilx-fab .lbl { display: none; } #smilx-fab { padding: 0; width: 56px; } }

/* ── Motion ─────────────────────────────────────────────────────── */
@keyframes fadeUp { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: none; } }
.fade { animation: fadeUp .45s cubic-bezier(.2,.7,.2,1) both; }
.fade.d1 { animation-delay: .06s; } .fade.d2 { animation-delay: .12s; } .fade.d3 { animation-delay: .18s; }
@media (prefers-reduced-motion: reduce) {
    .fade, #smilx-fab.down svg, #smilx-fab.down.pulse { animation: none !important; }
}
</style>
"""

# Floating "scroll" button. Lives in the main document so it can find
# Streamlit's scroll container; one instance, re-used across reruns/pages.
FAB_JS = r"""
<script>
(() => {
  const doc = document;
  // Built with DOM calls: Streamlit's sanitizer drops scripts whose strings contain tags
  function arrow() {
    const NS = 'http://www.w3.org/2000/svg';
    const svg = doc.createElementNS(NS, 'svg');
    svg.setAttribute('viewBox', '0 0 24 24'); svg.setAttribute('fill', 'none');
    svg.setAttribute('stroke', 'currentColor'); svg.setAttribute('stroke-width', '2.4');
    svg.setAttribute('stroke-linecap', 'round'); svg.setAttribute('stroke-linejoin', 'round');
    svg.setAttribute('aria-hidden', 'true');
    const path = doc.createElementNS(NS, 'path'); path.setAttribute('d', 'M12 5v14M5 12l7 7 7-7');
    svg.appendChild(path); return svg;
  }
  function scroller() {
    const c = [doc.querySelector('[data-testid="stMain"]'), doc.querySelector('[data-testid="stAppViewContainer"]'),
               doc.querySelector('.stApp'), doc.scrollingElement];
    for (const el of c) if (el && el.scrollHeight - el.clientHeight > 4 &&
        (el === doc.scrollingElement || /(auto|scroll)/.test(getComputedStyle(el).overflowY))) return el;
    return doc.scrollingElement;
  }
  let fab = doc.getElementById('smilx-fab');
  if (!fab) {
    fab = doc.createElement('button');
    fab.id = 'smilx-fab'; fab.type = 'button';
    const lbl = doc.createElement('span'); lbl.className = 'lbl'; lbl.textContent = 'Scroll down';
    fab.appendChild(arrow()); fab.appendChild(lbl);
    doc.body.appendChild(fab);
    fab.addEventListener('click', () => {
      const s = scroller(), vh = s.clientHeight;
      if (fab.classList.contains('up')) { s.scrollTo({ top: 0, behavior: 'smooth' }); return; }
      const res = doc.querySelector('.st-key-results');
      if (res) {
        const top = res.getBoundingClientRect().top;
        if (top > vh * 0.6) { s.scrollBy({ top: top - 80, behavior: 'smooth' }); return; }
      }
      s.scrollBy({ top: vh * 0.8, behavior: 'smooth' });
    });
  }
  function update() {
    const s = scroller();
    const max = s.scrollHeight - s.clientHeight;
    if (max < 160) { fab.classList.remove('show'); return; }
    const atEnd = s.scrollTop > max - 140;
    const res = doc.querySelector('.st-key-results');
    const resBelow = res && res.getBoundingClientRect().top > s.clientHeight * 0.6;
    fab.classList.add('show');
    fab.classList.toggle('up', atEnd);
    fab.classList.toggle('down', !atEnd);
    fab.classList.toggle('pulse', !atEnd && s.scrollTop < 40);
    const label = atEnd ? 'Back to top' : (resBelow ? 'See results' : 'Scroll down');
    const span = fab.querySelector('.lbl');
    if (span.textContent !== label) span.textContent = label;
    fab.setAttribute('aria-label', label); fab.title = label;
  }
  if (!window.__smilxFab) {
    window.__smilxFab = true;
    doc.addEventListener('scroll', update, true);
    window.addEventListener('resize', update);
    setInterval(update, 700);
  }
  setTimeout(update, 50);
})();
</script>
"""


def _js(script_html: str) -> str:
    """Ship a <script> as base64 so Streamlit's HTML sanitizer cannot alter it."""
    body = script_html.strip()
    body = body[len("<script>"):-len("</script>")]
    return f"<script>eval(atob('{base64.b64encode(body.encode()).decode()}'))</script>"


def run_js(script_html: str) -> None:
    st.html(_js(script_html), unsafe_allow_javascript=True)


def inject_theme() -> None:
    st.html(CSS)
    run_js(FAB_JS)
