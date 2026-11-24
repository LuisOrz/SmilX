"""Explore · enumerate the isomers of a molecular formula with TokenSMILES."""
import io
import json
import shutil
import time
from urllib.parse import quote

import pandas as pd
import streamlit as st

from content import LINKS, INSTITUTION, PUBLICATIONS
from isomer_info import describe_all
from smilx_parameters import parse_formula, initial_parameters, SUPPORTED_ELEMENTS
from smilx_chemical_space import chemical_space_classic, chemical_space_carbenes
from ui.components import html, img_uri, esc, gap
from ui.isomer_modal import inject_modal, grid_header
from ui.theme import run_js, js_file

EXAMPLES = ["C6H14", "C6H6", "C4H8O", "C2H5NO2", "C3H6Cl2", "C4H4"]
MODES = ["Classic", "Classic + carbenes"]
RESULT_KEY = "smilx_result"
ICON_DL = ('<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
           'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 4v12M6 10l6 6 6-6M5 20h14"/></svg>')
ICON_TABLE = ('<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
              'stroke-linecap="round" aria-hidden="true"><rect x="4" y="4" width="16" height="16" rx="2"/>'
              '<path d="M4 10h16M10 4v16"/></svg>')
ICON_MORE = ('<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
             '<circle cx="12" cy="5" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="12" cy="19" r="2"/></svg>')
PAPER = next(p for p in PUBLICATIONS if p.get("featured"))
PAPER_AUTHORS = ("Luis Armando Gonzalez-Ortiz, Lisset Noriega, Filiberto Ortiz, Gabriela Vidales-Ayala, "
                 "Emmanuel Soberanis, Amilcar Meneses, Alan Aspuru-Guzik and Gabriel Merino")

# ── State that must survive page switches ──────────────────────────────────
if "formula_input" not in st.session_state:
    st.session_state.formula_input = st.session_state.get("_formula", "C6H14")
if "mode_input" not in st.session_state or st.session_state.mode_input is None:
    st.session_state.mode_input = st.session_state.get("_mode", MODES[0])


def _remember():
    st.session_state._formula = st.session_state.formula_input
    st.session_state._mode = st.session_state.mode_input or MODES[0]


def _on_formula():            # Enter in the field → explore right away
    _remember()
    st.session_state._run = True


def _on_example():            # an example only fills the field; Explore runs it
    pick = st.session_state.get("example_pick")
    if pick:
        st.session_state.formula_input = pick
        st.session_state.example_pick = None
        _remember()


def _on_mode():
    if st.session_state.mode_input is None:
        st.session_state.mode_input = st.session_state.get("_mode", MODES[0])
    _remember()


def _clear_results():
    st.session_state.pop(RESULT_KEY, None)


# ── Engine ─────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False, max_entries=64)
def run_exploration(formula: str, carbenes: bool) -> dict:
    """Run SmilX once per (formula, mode); results are cached for every visitor."""
    params = initial_parameters(formula, carbenes)
    t0 = time.perf_counter()
    try:
        if params.opt_carbenes and params.molecular_formula["hdi"] > 0:
            space = chemical_space_carbenes(params)
            used_carbenes = True
        else:
            space = chemical_space_classic(params)
            used_carbenes = False
        smiles = [s for s in space.list_smiles if s]
    finally:
        shutil.rmtree(params.workdir, ignore_errors=True)
    return {
        "formula": params.str_molecular_formula,
        "carbenes_requested": carbenes,
        "carbenes": used_carbenes,
        "smiles": smiles,
        "seconds": time.perf_counter() - t0,
        "file_stem": params.download_name_smi[:-4],
    }


@st.cache_data(show_spinner=False, max_entries=32)
def isomer_props(smiles: tuple) -> dict:
    return describe_all(list(smiles))


# ── Hero ───────────────────────────────────────────────────────────────────
# Landing: big logo + credits. With results on screen: one compact line, so the
# formula field and the results share the first screen (no long jump to scroll).
_pending = bool(st.session_state.get("go") or st.session_state.get("_run"))
has_results = bool(st.session_state.get(RESULT_KEY)) or (
    _pending and parse_formula(st.session_state.get("formula_input", "")).ok)
if not has_results:
    html(f"""
<div class="hero fade">
  <img class="hero-logo" src="{img_uri('assets/logo_smilx.png')}" alt="SmilX" width="340" height="122">
  <div class="credit">
    <p class="a"><a href="{LINKS['paper']}" target="_blank" rel="noopener">&ldquo;{esc(PAPER['title'])}&rdquo;</a>
      by {esc(PAPER_AUTHORS)}.</p>
    <p class="a">{esc(INSTITUTION)}</p>
    <p class="i">GNU General Public License v3 · 29 June 2007 · © 2007 Free Software Foundation</p>
  </div>
</div>
""")
else:
    html(f"""
<div class="hero-compact">
  <img src="{img_uri('assets/logo_smilx.png')}" alt="SmilX" width="104" height="37">
  <p><a href="{LINKS['paper']}" target="_blank" rel="noopener">&ldquo;{esc(PAPER['title'])}&rdquo;</a>
     · Chem. Sci. 2026 · {esc(INSTITUTION.split(' (')[0])} · GPL v3</p>
</div>
""")

# ── Explorer card: formula · mode · Explore ────────────────────────────────
with st.container(key="explorer-compact" if has_results else "explorer"):
    c_in, c_mode, c_btn = st.columns([2.1, 1.55, 0.85], vertical_alignment="bottom", gap="medium")
    with c_in:
        st.text_input("Molecular formula", key="formula_input",
                      placeholder="e.g. C6H6, C2H5NO2", on_change=_on_formula, max_chars=40)
    chk = parse_formula(st.session_state.formula_input)
    with c_mode:
        st.segmented_control(
            "Exploration mode", MODES, key="mode_input", on_change=_on_mode,
            selection_mode="single", required=True,
            help="Classic: every constitutional isomer. Classic + carbenes: also structures with "
                 "divalent carbon centres, written [C]; each one uses one degree of unsaturation, "
                 "so it only changes results when HDI > 0. A bioinspired (evolutionary) search "
                 "is coming soon.",
        )
    with c_btn:
        go = st.button("Explore", type="primary", width="stretch", disabled=not chk.ok,
                       key="go", icon=":material/travel_explore:")

    st.pills("No formula in mind? Try an example", EXAMPLES, key="example_pick",
             on_change=_on_example, selection_mode="single")

    if not chk.ok:
        html(f'<p class="inline-msg {"err" if chk.raw else "warn"}"><i>!</i>{esc(chk.error)}</p>')
    elif chk.warning:
        html(f'<p class="inline-msg warn"><i>!</i>{esc(chk.warning)}</p>')

# "Start here" pulse on the formula field until the user clicks into it
run_js("""<script>
(() => {
  const b = document.body;
  try { if (sessionStorage.getItem('smilxStarted')) b.classList.add('smilx-started'); } catch (e) {}
  if (window.__smilxStartBound) return; window.__smilxStartBound = true;
  document.addEventListener('focusin', (e) => {
    if (e.target.closest && e.target.closest('.st-key-formula_input')) {
      b.classList.add('smilx-started');
      try { sessionStorage.setItem('smilxStarted', '1'); } catch (err) {}
    }
  }, true);
})();
</script>""")

# ── Run ────────────────────────────────────────────────────────────────────
just_ran = False
if (go or st.session_state.pop("_run", False)) and chk.ok:
    _remember()
    carbenes = (st.session_state.mode_input or MODES[0]) == MODES[1]
    try:
        with st.spinner(f"Building the chemical space of {chk.raw}…"):
            st.session_state[RESULT_KEY] = run_exploration(chk.raw, carbenes)
        just_ran = True
        n = len(st.session_state[RESULT_KEY]["smiles"])
        st.toast(f"{n:,} isomers found for {chk.raw}", icon=":material/check_circle:")
    except Exception as exc:  # keep the app alive and explain what happened
        _clear_results()
        st.error(f"SmilX could not explore {chk.raw}: {exc}")


# ── Results grid ───────────────────────────────────────────────────────────
GRID_CSS = """
:root { color-scheme: dark; }
body { background: #0e111a !important; margin: 0; padding: 0 0 8px;
  --m2g-black: #e6e8f0; --m2g-black-soft: #8c94ab; --m2g-black-10: #20263a;
  --m2g-bg: #1a1f2c; --m2g-border: solid 1px #4a5470; --m2g-hl: #adc6ff;
  --m2g-hl-shadow: 0 0 0 1px #adc6ff; --m2g-blue: #adc6ff; --m2g-blue-soft: rgba(173,198,255,.16);
  --m2g-br: 10px; --m2g-h: 40px; }
#mols2grid { font-family: 'Outfit', system-ui, sans-serif; color: #e6e8f0; }
#mols2grid { margin: 0 !important; padding: 0 !important; }
#mols2grid .m2g-functions { margin: 0 0 16px !important; gap: 8px; align-items: center; }
#mols2grid ul.m2g-pagination { margin: 0 !important; padding: 0 !important; }
#mols2grid ul.m2g-pagination li:first-child { margin-left: 0 !important; }
#mols2grid ul.m2g-pagination li:first-child, #mols2grid ul.m2g-pagination li:first-child a { border-top-left-radius: 10px !important; border-bottom-left-radius: 10px !important; }
#mols2grid ul.m2g-pagination li:last-child, #mols2grid ul.m2g-pagination li:last-child a { border-top-right-radius: 10px !important; border-bottom-right-radius: 10px !important; }
#mols2grid .m2g-list { margin-top: -12px !important; padding: 0 !important; }
#mols2grid .m2g-dropdown, #mols2grid .m2g-search-wrap { background: #1a1f2c !important; border: 1px solid #4a5470 !important; }
#mols2grid .m2g-dropdown:not(:focus-within):hover, #mols2grid .m2g-search-wrap:not(:focus-within):hover,
#mols2grid .m2g-sort:not(:focus-within) .m2g-order:hover { background-color: #20263a !important; border-color: #8c94ab !important; }
#mols2grid .m2g-dropdown:focus-within, #mols2grid .m2g-search-wrap:focus-within { border-color: #adc6ff !important; box-shadow: 0 0 0 1px #adc6ff !important; background: #1a1f2c !important; }
#mols2grid .m2g-dropdown .m2g-display { color: #e6e8f0; font-size: 14px; }
#mols2grid .m2g-dropdown .m2g-display::before { color: #8c94ab; }
#mols2grid .m2g-dropdown.m2g-sort .m2g-order { background-color: transparent !important; filter: invert(1) brightness(.9); border-color: #4a5470 !important; }
#mols2grid .m2g-dropdown.m2g-actions .m2g-icon { filter: invert(1) brightness(.9); }
#mols2grid select, #mols2grid select option { background: #272e44 !important; color: #e6e8f0 !important; }
#mols2grid .m2g-searchbar { color: #e6e8f0 !important; background: transparent !important; font-size: 14px; }
#mols2grid .m2g-searchbar::placeholder { color: #8c94ab; }
#mols2grid .m2g-search-options { margin-right: 4px; background: #20263a; border-radius: 8px; padding: 2px; height: 32px; line-height: 28px; }
#mols2grid .m2g-search-options .m2g-option { background: transparent !important; color: #b8bfd2 !important; border-radius: 6px !important; font-weight: 600; padding: 0 12px; cursor: pointer; }
#mols2grid .m2g-search-options .m2g-option:not(.sel):hover { background: #272e44 !important; color: #e6e8f0 !important; }
#mols2grid .m2g-search-options .m2g-option.sel { background: #adc6ff !important; color: #0b2a63 !important; }
#mols2grid ul.m2g-pagination li a, #mols2grid .m2g-pagination li { color: #b8bfd2 !important; background: #1a1f2c !important; border-color: #4a5470 !important; }
#mols2grid ul.m2g-pagination li:hover a { background: #20263a !important; color: #e6e8f0 !important; }
#mols2grid ul.m2g-pagination li.active a, #mols2grid ul.m2g-pagination li.active { background: #adc6ff !important; color: #0b2a63 !important; border-color: #adc6ff !important; }
#mols2grid ul.m2g-pagination li.disabled a { color: #4a5470 !important; }
#mols2grid .m2g-stats { color: #8c94ab; }
/* cells: classic 2D drawings on white */
#mols2grid .m2g-cell { --m2g-black: #1d2333; --m2g-black-soft: #7a8296; --m2g-blue: #3a62d6;
  background: #ffffff !important; border: 1px solid #e3e7f1 !important; border-radius: 14px !important; transition: transform .15s, box-shadow .15s; }
#mols2grid .m2g-cell:hover { transform: translateY(-2px); box-shadow: 0 0 0 2px #adc6ff, 0 10px 24px -10px rgba(0,0,0,.6); }
#mols2grid .m2g-cell:hover::after { background: transparent !important; }
#mols2grid .m2g-cell .data-img { cursor: zoom-in; }
#mols2grid .m2g-cell.m2g-phantom { background: transparent !important; border: none !important; box-shadow: none !important; }
#mols2grid .m2g-callback { display: none !important; }
#mols2grid .m2g-cb-wrap input[type=checkbox] + .m2g-cb { border-color: #8a93a8; }
#mols2grid .data-mols2grid-id-display { display: none !important; }
#mols2grid .data-ID { color: #2b4fb8 !important; font: 600 12px 'IBM Plex Mono', monospace; }
#mols2grid .data-SMILES { color: #3f4659 !important; font: 500 11.5px 'IBM Plex Mono', monospace; word-break: break-all; }
"""


def _grid_html(smiles: list[str], props: dict) -> str:
    import mols2grid
    df = pd.DataFrame({"SMILES": smiles, "ID": range(1, len(smiles) + 1)})
    payload = json.dumps({"total": len(smiles), "props": props}, separators=(",", ":"))
    header = grid_header(payload)
    grid = mols2grid.MolGrid(df, smiles_col="SMILES", size=(170, 130))   # drawn in-browser
    out = grid.display(
        subset=["ID", "img", "SMILES"],
        tooltip=None,
        n_items_per_page=30,
        selection=True,                      # checkboxes + select/copy/save actions
        callback="window.smilxOpen(data['ID']);",
        sort_by="ID",
        background_color="#ffffff",
        border="1px solid #e3e7f1",
        hover_color="rgba(173,198,255,.10)",
        gap=12,
        pad=8,
        fontfamily="'IBM Plex Mono', monospace",
        custom_css=GRID_CSS,
        custom_header=header,
    )
    return out.data


res = st.session_state.get(RESULT_KEY)
if res:
    inject_modal()
    with st.container(key="results"):
        smiles = res["smiles"]
        rchk = parse_formula(res["formula"])
        title = rchk.pretty if rchk.ok else esc(res["formula"])
        dl = ""
        if smiles:
            smi_text = "\n".join(smiles) + "\n"
            csv_buf = io.StringIO()
            pd.DataFrame({"id": range(1, len(smiles) + 1), "smiles": smiles}).to_csv(csv_buf, index=False)
            smi_uri = "data:chemical/x-daylight-smiles;charset=utf-8," + quote(smi_text)
            csv_uri = "data:text/csv;charset=utf-8," + quote(csv_buf.getvalue())
            dl = f"""
  <a class="rb-btn" href="{smi_uri}" download="{esc(res['file_stem'])}.smi">{ICON_DL}Download .smi</a>
  <a class="rb-btn elaya" href="{LINKS['elaya']}" target="_blank" rel="noopener" title="Open ELAYA SMILES to build 3D structures">
    <img src="{img_uri('assets/elaya_logo.png')}" alt="" width="22" height="22">3D with ELAYA</a>
  <details class="rb-more">
    <summary aria-label="More options" title="More options">{ICON_MORE}</summary>
    <div class="rb-menu">
      <a href="{csv_uri}" download="{esc(res['file_stem'])}.csv">{ICON_TABLE}Table (.csv)</a>
      <p>Tip: click any structure to zoom in.</p>
    </div>
  </details>"""
        html(f"""
<div class="res-bar" id="smilx-res-bar">
  <span class="result-banner"><i>✓</i><span>{len(smiles):,} isomers of {title}</span></span>
  <span class="rb-space"></span>{dl}
</div>""")
        if smiles:
            props = isomer_props(tuple(smiles))
            st.iframe(_grid_html(smiles, props), height="content")
        else:
            st.info("No isomers were generated for this formula and mode.")

    if just_ran:
        # Gentle: scroll only when the results header is below the fold, and then
        # only far enough to show the explorer + results header + first row.
        run_js(f"/* {time.time_ns()} */\n" + """
(() => {
  const go = () => {
    const bar = document.querySelector('#smilx-res-bar');
    const exp = document.querySelector('.st-key-explorer-compact, .st-key-explorer');
    if (!bar || !exp) return false;
    const vh = window.innerHeight, r = bar.getBoundingClientRect();
    if (r.top > 0 && r.bottom < vh * 0.7) return true;              // already in view
    const nav = 72, top = exp.getBoundingClientRect().top;
    const sc = document.querySelector('[data-testid="stMain"]');
    const scroller = (sc && sc.scrollHeight > sc.clientHeight) ? sc : document.scrollingElement;
    const smooth = !window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    scroller.scrollBy({ top: top - nav, behavior: smooth ? 'smooth' : 'auto' });
    return true;
  };
  let n = 0; const t = setInterval(() => { if (go() || ++n > 25) clearInterval(t); }, 120);
})();
""")
