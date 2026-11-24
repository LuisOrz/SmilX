"""Explore · enumerate the isomers of a molecular formula with TokenSMILES."""
import io
import shutil
import time

import pandas as pd
import streamlit as st

from content import LINKS, PROJECT_TITLE, PROJECT_AUTHORS, INSTITUTION
from smilx_chemistry_tools import get_unsaturations
from smilx_parameters import parse_formula, initial_parameters, SUPPORTED_ELEMENTS
from smilx_chemical_space import chemical_space_classic, chemical_space_carbenes
from ui.components import html, img_uri, esc, section, gap
from ui.theme import run_js

EXAMPLES = ["C6H14", "C6H6", "C4H8O", "C2H5NO2", "C3H6Cl2", "C4H4"]
MODES = ["Classic", "Classic + carbenes"]
RESULT_KEY = "smilx_result"

# ── State that must survive page switches ──────────────────────────────────
# Streamlit drops widget values when you leave a page, so they are mirrored
# into plain session keys and restored when you come back.
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
def unsaturation_patterns(chk):
    mf = {e: chk.counts.get(e, 0) for e in SUPPORTED_ELEMENTS}
    mf["hdi"] = chk.hdi
    pats = get_unsaturations(mf, chk.n_heavy_atoms)
    return [u for u in pats if chk.hdi == u.double_bonds + 2 * u.triple_bonds + u.cycles]


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


# ── Hero ───────────────────────────────────────────────────────────────────
html(f"""
<div class="hero fade">
  <img class="hero-logo" src="{img_uri('assets/logo_smilx.png')}" alt="SmilX logo">
  <h1 class="tagline">Explore the chemical space of isomers with grammar-constrained SMILES</h1>
  <p class="sub">Type a molecular formula and SmilX enumerates every valid isomer it can build
  with the TokenSMILES grammar, ready to browse, download, or take to 3D.</p>
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

gap()

# ── Explorer card ──────────────────────────────────────────────────────────
with st.container(key="card-explorer"):
    # Row 1 · formula + action, side by side
    c_in, c_btn = st.columns([3.2, 1], vertical_alignment="bottom", gap="small")
    with c_in:
        st.text_input("Molecular formula", key="formula_input",
                      placeholder="e.g. C6H6, C2H5NO2", on_change=_on_formula, max_chars=40)
    chk = parse_formula(st.session_state.formula_input)
    with c_btn:
        go = st.button("Explore  →", type="primary", width="stretch",
                       disabled=not chk.ok, key="go", help="Or press Enter in the formula field")

    # Row 2 · examples + mode
    c_ex, c_mode = st.columns([1.45, 1], gap="large")
    with c_ex:
        st.pills("Try an example (runs instantly)", EXAMPLES, key="example_pick",
                 on_change=_on_example, selection_mode="single")
    with c_mode:
        st.segmented_control(
            "Exploration mode", MODES, key="mode_input", on_change=_on_mode,
            selection_mode="single", required=True,
            help="Carbenes adds divalent carbon centres, written [C]. Each one uses up one "
                 "degree of unsaturation, so it only changes results when HDI > 0.",
        )
        html('<p class="soon">Bioinspired (evolutionary) search · <b>coming soon</b></p>')

    # Row 3 · live formula analysis, one compact strip
    if chk.ok:
        pats = unsaturation_patterns(chk)
        atoms = "".join(f"<span>{esc(e)}·{n}</span>" for e, n in chk.counts.items())
        status = (f'<span class="status warn"><i>!</i>{esc(chk.warning)}</span>' if chk.warning
                  else '<span class="status ok"><i>✓</i>Ready to explore</span>')
        html(f"""
<div class="analysis">
  <span class="f">{chk.pretty}</span><span class="sep"></span>
  <span class="m"><b>{chk.n_heavy_atoms}</b><span>heavy atoms</span></span>
  <span class="m"><b>{chk.hdi}</b><span>HDI</span></span>
  <span class="m"><b>{len(pats)}</b><span>unsaturation patterns</span></span>
  <span class="sep"></span><span class="atoms">{atoms}</span>
  {status}
</div>""")
    else:
        html(f"""
<div class="analysis">
  <span class="status {'err' if chk.raw else 'warn'}"><i>!</i>{esc(chk.error)}</span>
  <span class="m"><span>Supported: {' · '.join(SUPPORTED_ELEMENTS)}</span></span>
</div>""")

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


# ── Results grid (2D structures on white, toolbar in SmilX dark) ───────────
GRID_CSS = """
:root { color-scheme: dark; }
body { background: #151924 !important; margin: 0; padding: 14px 12px 6px;
  --m2g-black: #e6e8f0; --m2g-black-soft: #8c94ab; --m2g-black-10: #20263a;
  --m2g-bg: #1a1f2c; --m2g-border: solid 1px #4a5470; --m2g-hl: #adc6ff;
  --m2g-hl-shadow: 0 0 0 1px #adc6ff; --m2g-blue: #adc6ff; --m2g-blue-soft: rgba(173,198,255,.16);
  --m2g-br: 10px; --m2g-h: 40px; }
#mols2grid { font-family: 'Outfit', system-ui, sans-serif; color: #e6e8f0; }
/* toolbar: no white flashes on hover/focus, readable text everywhere */
#mols2grid .m2g-functions { margin-bottom: 14px; gap: 8px; }
#mols2grid .m2g-dropdown, #mols2grid .m2g-search-wrap { background: #1a1f2c !important; border: 1px solid #4a5470 !important; }
#mols2grid .m2g-dropdown:not(:focus-within):hover, #mols2grid .m2g-search-wrap:not(:focus-within):hover,
#mols2grid .m2g-sort:not(:focus-within) .m2g-order:hover { background-color: #20263a !important; border-color: #8c94ab !important; }
#mols2grid .m2g-dropdown:focus-within, #mols2grid .m2g-search-wrap:focus-within { border-color: #adc6ff !important; box-shadow: 0 0 0 1px #adc6ff !important; background: #1a1f2c !important; }
#mols2grid .m2g-dropdown .m2g-display { color: #e6e8f0; font-size: 14px; }
#mols2grid .m2g-dropdown .m2g-display::before { color: #8c94ab; }
#mols2grid .m2g-dropdown.m2g-sort .m2g-order { background-color: transparent !important; filter: invert(1) brightness(.9); border-color: #4a5470 !important; }
#mols2grid select, #mols2grid select option { background: #272e44 !important; color: #e6e8f0 !important; }
#mols2grid .m2g-searchbar { color: #e6e8f0 !important; background: transparent !important; font-size: 14px; }
#mols2grid .m2g-search-options { margin-right: 4px; background: #20263a; border-radius: 8px; padding: 2px; height: 32px; line-height: 28px; }
#mols2grid .m2g-search-options .m2g-option { background: transparent !important; color: #b8bfd2 !important; border-radius: 6px !important; font-weight: 600; padding: 0 12px; }
#mols2grid .m2g-search-options .m2g-option:not(.sel):hover { background: #272e44 !important; color: #e6e8f0 !important; }
#mols2grid .m2g-search-options .m2g-option.sel { background: #adc6ff !important; color: #0b2a63 !important; }
#mols2grid .m2g-dropdown.m2g-actions { display: none !important; }
/* pagination */
#mols2grid ul.m2g-pagination li a, #mols2grid .m2g-pagination li { color: #b8bfd2 !important; background: #1a1f2c !important; border-color: #4a5470 !important; }
#mols2grid ul.m2g-pagination li:hover a { background: #20263a !important; color: #e6e8f0 !important; }
#mols2grid ul.m2g-pagination li.active a, #mols2grid ul.m2g-pagination li.active { background: #adc6ff !important; color: #0b2a63 !important; border-color: #adc6ff !important; }
#mols2grid ul.m2g-pagination li.disabled a { color: #4a5470 !important; }
/* cells: classic white 2D drawings */
#mols2grid .m2g-cell { background: #ffffff !important; border: 1px solid #e3e7f1 !important; border-radius: 14px !important;
  transition: transform .15s, box-shadow .15s; }
#mols2grid .m2g-cell:hover { transform: translateY(-2px); box-shadow: 0 0 0 2px #adc6ff, 0 10px 24px -10px rgba(0,0,0,.6); }
#mols2grid .m2g-cell:hover::after { background: transparent !important; }
#mols2grid .data-mols2grid-id-display { display: none !important; }
#mols2grid .data-ID { color: #2b4fb8 !important; font: 600 12px 'IBM Plex Mono', monospace; }
#mols2grid .data-SMILES { color: #3f4659 !important; font: 500 11.5px 'IBM Plex Mono', monospace; word-break: break-all; }
"""


def _grid_html(smiles: list[str]) -> str:
    import mols2grid
    df = pd.DataFrame({"SMILES": smiles, "ID": range(1, len(smiles) + 1)})
    grid = mols2grid.MolGrid(df, smiles_col="SMILES", size=(170, 130), prerender=True)
    out = grid.display(
        subset=["ID", "img", "SMILES"],
        tooltip=None,
        n_items_per_page=30,
        selection=False,
        background_color="#ffffff",
        border="1px solid #e3e7f1",
        hover_color="rgba(173,198,255,.10)",
        gap=12,
        pad=8,
        fontfamily="'IBM Plex Mono', monospace",
        custom_css=GRID_CSS,
    )
    return out.data


res = st.session_state.get(RESULT_KEY)
if res:
    gap()
    with st.container(key="results"):
        smiles = res["smiles"]
        mode_label = "Classic + carbenes" if res["carbenes"] else "Classic"
        if res["carbenes_requested"] and not res["carbenes"]:
            mode_label += " (HDI 0: no carbenes possible)"
        rchk = parse_formula(res["formula"])
        html(f"""
<div class="fade">
  <div class="result-head">
    <span class="result-banner"><i>✓</i><span>{len(smiles):,} isomers of {rchk.pretty if rchk.ok else esc(res['formula'])}</span></span>
  </div>
  <div class="stats">
    <div class="stat"><b class="g">{len(smiles):,}</b><span>Isomers found</span></div>
    <div class="stat"><b>{rchk.hdi if rchk.ok else '—'}</b><span>Hydrogen deficiency index</span></div>
    <div class="stat"><b>{rchk.n_heavy_atoms if rchk.ok else '—'}</b><span>Heavy atoms</span></div>
    <div class="stat"><b>{res['seconds']:.2f}s</b><span>{esc(mode_label)}</span></div>
  </div>
</div>""")

        if smiles:
            smi_text = "\n".join(smiles) + "\n"
            csv_buf = io.StringIO()
            pd.DataFrame({"id": range(1, len(smiles) + 1), "smiles": smiles}).to_csv(csv_buf, index=False)
            c1, c2, c3, c4 = st.columns([1, 1, 1.25, 0.8])
            with c1:
                st.download_button("Download .smi", smi_text, file_name=f"{res['file_stem']}.smi",
                                   mime="chemical/x-daylight-smiles", width="stretch",
                                   icon=":material/download:")
            with c2:
                st.download_button("Download .csv", csv_buf.getvalue(), file_name=f"{res['file_stem']}.csv",
                                   mime="text/csv", width="stretch", icon=":material/table_view:")
            with c3:
                with st.container(key="elaya-btn"):
                    st.link_button("View in 3D with ELAYA", LINKS["elaya"], width="stretch",
                                   icon=":material/view_in_ar:")
            with c4:
                st.button("Clear", on_click=_clear_results, width="stretch", key="clear",
                          icon=":material/close:")

            st.iframe(_grid_html(smiles), height="content")

            with st.expander(f"All {len(smiles):,} SMILES as plain text"):
                st.code(smi_text, language=None)
        else:
            st.info("No isomers were generated for this formula and mode.")

    if just_ran:  # bring the fresh results into view
        run_js("""<script>
setTimeout(() => { const r = document.querySelector('.st-key-results');
  if (r) r.scrollIntoView({ behavior: 'smooth', block: 'start' }); }, 400);
</script>""")
else:
    gap()
    section("How it works", "Three steps from a formula to a browsable set of isomers.")
    html("""
<div class="steps fade d1">
  <div class="step"><div class="n">1</div><div><b>Enter a formula</b>
    <span>Any combination of C, H, N, O, S, P, B, F, Cl, Br and I. Press Enter or pick an example.</span></div></div>
  <div class="step"><div class="n">2</div><div><b>Grammar-driven enumeration</b>
    <span>TokenSMILES builds skeletons, inserts bonds and rings, and substitutes heteroatoms under valence rules.</span></div></div>
  <div class="step"><div class="n">3</div><div><b>Browse &amp; download</b>
    <span>Search and sort the 2D structures, export .smi or .csv, and open ELAYA SMILES for 3D.</span></div></div>
</div>""")
