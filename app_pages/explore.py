"""Explore · enumerate the isomers of a molecular formula with TokenSMILES."""
import io
import json
import shutil
import time

import pandas as pd
import streamlit as st

from content import LINKS, PROJECT_TITLE, PROJECT_AUTHORS, INSTITUTION
from isomer_info import describe_all
from smilx_parameters import parse_formula, initial_parameters, SUPPORTED_ELEMENTS
from smilx_chemical_space import chemical_space_classic, chemical_space_carbenes
from ui.components import html, img_uri, esc, gap
from ui.isomer_modal import MODAL_CSS, MODAL_JS, GRID_JS_TEMPLATE
from ui.theme import run_js

EXAMPLES = ["C6H14", "C6H6", "C4H8O", "C2H5NO2", "C3H6Cl2", "C4H4"]
MODES = ["Classic", "Classic + carbenes"]
RESULT_KEY = "smilx_result"

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


def _on_example():            # one click on an example → explore it
    pick = st.session_state.get("example_pick")
    if pick:
        st.session_state.formula_input = pick
        st.session_state.example_pick = None
        _remember()
        st.session_state._run = True


def _on_mode():               # switching mode refreshes visible results
    if st.session_state.mode_input is None:
        st.session_state.mode_input = st.session_state.get("_mode", MODES[0])
    _remember()
    if st.session_state.get(RESULT_KEY):
        st.session_state._run = True


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
html(f"""
<div class="hero fade">
  <img class="hero-logo" src="{img_uri('assets/logo_smilx.png')}" alt="SmilX logo">
  <h1 class="tagline">Explore the chemical space of isomers with grammar-constrained SMILES</h1>
  <p class="sub">Type a molecular formula and SmilX enumerates every valid isomer it can build
  with the TokenSMILES grammar, ready to browse, inspect and download.</p>
  <div class="chips">
    <a class="chip blue" href="{LINKS['paper']}" target="_blank" rel="noopener">Chem. Sci. 2026 · TokenSMILES ↗</a>
    <span class="chip"><span class="dot"></span>Open source · GPL-3.0</span>
    <span class="chip">RDKit-validated output</span>
    <span class="chip">Cinvestav Mérida</span>
  </div>
  <div class="credit">
    <p class="t">&ldquo;{esc(PROJECT_TITLE)}&rdquo;</p>
    <p class="a">{esc(', '.join(PROJECT_AUTHORS[:-1]))} &amp; {esc(PROJECT_AUTHORS[-1])}</p>
    <p class="i">{esc(INSTITUTION)}</p>
  </div>
</div>
""")

# ── Explorer card: formula · mode · Explore ────────────────────────────────
with st.container(key="card-explorer"):
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

    c_lbl, c_pills = st.columns([0.62, 2.2], vertical_alignment="center", gap="small")
    with c_lbl:
        html('<p class="try">No formula in mind? <b>Try an example:</b></p>')
    with c_pills:
        st.pills("Examples", EXAMPLES, key="example_pick", on_change=_on_example,
                 selection_mode="single", label_visibility="collapsed")

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
body { background: #0e111a !important; margin: 0; padding: 4px 2px 6px;
  --m2g-black: #e6e8f0; --m2g-black-soft: #8c94ab; --m2g-black-10: #20263a;
  --m2g-bg: #1a1f2c; --m2g-border: solid 1px #4a5470; --m2g-hl: #adc6ff;
  --m2g-hl-shadow: 0 0 0 1px #adc6ff; --m2g-blue: #adc6ff; --m2g-blue-soft: rgba(173,198,255,.16);
  --m2g-br: 10px; --m2g-h: 40px; }
#mols2grid { font-family: 'Outfit', system-ui, sans-serif; color: #e6e8f0; }
#mols2grid .m2g-functions { margin-bottom: 12px; gap: 8px; }
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
    header = GRID_JS_TEMPLATE.replace("__DATA__", payload.replace("</", "<\\/"))
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
    st.html(MODAL_CSS)
    run_js(MODAL_JS)
    with st.container(key="results"):
        smiles = res["smiles"]
        rchk = parse_formula(res["formula"])
        title = rchk.pretty if rchk.ok else esc(res["formula"])
        c_tot, c_menu = st.columns([4, 1], vertical_alignment="center")
        with c_tot:
            html(f'<div class="res-head fade"><span class="result-banner"><i>✓</i>'
                 f'<span>{len(smiles):,} isomers of {title}</span></span></div>')
        if smiles:
            smi_text = "\n".join(smiles) + "\n"
            csv_buf = io.StringIO()
            pd.DataFrame({"id": range(1, len(smiles) + 1), "smiles": smiles}).to_csv(csv_buf, index=False)
            with c_menu:
                with st.container(key="export-menu"):
                    with st.popover("Export", icon=":material/download:"):
                        st.download_button("SMILES (.smi)", smi_text, file_name=f"{res['file_stem']}.smi",
                                           mime="chemical/x-daylight-smiles", icon=":material/download:",
                                           width="stretch")
                        st.download_button("Table (.csv)", csv_buf.getvalue(), file_name=f"{res['file_stem']}.csv",
                                           mime="text/csv", icon=":material/table_view:", width="stretch")
                        st.link_button("View in 3D with ELAYA", LINKS["elaya"], icon=":material/view_in_ar:",
                                       width="stretch")
                        st.button("Clear results", on_click=_clear_results, key="clear",
                                  icon=":material/close:", width="stretch")
                        html('<p class="pop-tip">Click a structure to zoom in. '
                             '<b>Substructure</b> search uses SMARTS, e.g. <code>C=O</code>.</p>')

            props = isomer_props(tuple(smiles))
            st.iframe(_grid_html(smiles, props), height="content")
        else:
            st.info("No isomers were generated for this formula and mode.")

    if just_ran:  # every Explore → bring the grid into view once it has its height
        run_js(f"""<script>
/* {time.time_ns()} */
(() => {{
  document.body.classList.add('smilx-started');
  let tries = 0, last = -1;
  const t = setInterval(() => {{
    const fr = document.querySelector('.st-key-results iframe');
    const target = document.querySelector('.st-key-results') || fr;
    const h = fr ? fr.getBoundingClientRect().height : 0;
    tries++;
    if ((target && h > 200 && h === last) || tries > 40) {{
      clearInterval(t);
      if (target) target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
    }}
    last = h;
  }}, 120);
}})();
</script>""")
