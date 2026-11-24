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

EXAMPLES = ["C6H14", "C6H6", "C4H8O", "C2H5NO2", "C3H6Cl2", "C4H4"]
MODES = ["Classic", "Classic + carbenes"]
RESULT_KEY = "smilx_result"

# ── State that must survive page switches ──────────────────────────────────
# Widget values are dropped by Streamlit when you leave a page, so we mirror
# them into plain session keys and restore them on return.
if "formula_input" not in st.session_state:
    st.session_state.formula_input = st.session_state.get("_formula", "C6H14")
if "mode_input" not in st.session_state:
    st.session_state.mode_input = st.session_state.get("_mode", MODES[0])


def _remember():
    st.session_state._formula = st.session_state.formula_input
    st.session_state._mode = st.session_state.mode_input


def _use_example():
    pick = st.session_state.get("example_pick")
    if pick:
        st.session_state.formula_input = pick
        st.session_state.example_pick = None
        _remember()


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
    left, right = st.columns([1.25, 1], gap="large")

    with left:
        st.text_input(
            "Molecular formula",
            key="formula_input",
            placeholder="e.g. C6H6, C2H5NO2",
            on_change=_remember,
            max_chars=40,
        )
        st.pills(
            "Try an example",
            EXAMPLES,
            key="example_pick",
            on_change=_use_example,
            selection_mode="single",
        )
        st.radio(
            "Exploration mode",
            MODES,
            key="mode_input",
            horizontal=True,
            on_change=_remember,
            help="Carbenes adds divalent carbon centres, written [C]. Each one uses up "
                 "one degree of unsaturation, so this mode only changes the result when HDI > 0.",
        )
        html('<p class="soon">Bioinspired (evolutionary) search · <b>coming soon</b></p>')

    chk = parse_formula(st.session_state.formula_input)

    with right:
        if chk.ok:
            pats = unsaturation_patterns(chk)
            atoms = "".join(
                f"<span>{esc(e)} × {n}</span>" for e, n in chk.counts.items())
            msg = (f'<div class="msg warn">{esc(chk.warning)}</div>' if chk.warning else
                   '<div class="msg ok">Formula looks good. Ready to explore.</div>')
            html(f"""
<div class="analysis fade">
  <div class="head"><span class="lbl">Formula analysis</span><span class="f">{chk.pretty}</span></div>
  <div class="kv">
    <div><b>{chk.n_heavy_atoms}</b><span>Heavy atoms</span></div>
    <div><b>{chk.hdi}</b><span>HDI</span></div>
    <div><b>{len(pats)}</b><span>Unsat. patterns</span></div>
  </div>
  <div class="atoms">{atoms}</div>
  {msg}
</div>""")
        else:
            html(f"""
<div class="analysis">
  <div class="head"><span class="lbl">Formula analysis</span><span class="f">—</span></div>
  <div class="msg {'err' if chk.raw else 'warn'}">{esc(chk.error)}</div>
  <p style="font-size:12.5px;margin:.8rem 0 0;color:var(--muted)">Supported elements:
  {', '.join(SUPPORTED_ELEMENTS)}</p>
</div>""")

        go = st.button("Explore chemical space  →", type="primary",
                       width="stretch", disabled=not chk.ok, key="go")

# ── Run ────────────────────────────────────────────────────────────────────
if go and chk.ok:
    _remember()
    carbenes = st.session_state.mode_input == MODES[1]
    try:
        with st.spinner(f"Building the chemical space of {chk.raw}…"):
            st.session_state[RESULT_KEY] = run_exploration(chk.raw, carbenes)
    except Exception as exc:  # keep the app alive and explain what happened
        _clear_results()
        st.error(f"SmilX could not explore {chk.raw}: {exc}")


# ── Results ────────────────────────────────────────────────────────────────
def _grid_html(smiles: list[str]) -> str:
    import mols2grid
    df = pd.DataFrame({"SMILES": smiles, "ID": range(1, len(smiles) + 1)})
    css = """
body { background: #0b0f1c !important; margin: 0; padding: 12px 10px 4px;
       --m2g-black: rgba(232,237,248,.85); --m2g-black-soft: rgba(154,165,199,.6);
       --m2g-black-10: rgba(99,123,200,.13); --m2g-bg: #111628;
       --m2g-border: solid 1px rgba(99,123,200,.22); --m2g-hl: #5b8af5;
       --m2g-hl-shadow: inset 0 0 0 1px #5b8af5; --m2g-blue: #5b8af5;
       --m2g-blue-soft: rgba(91,138,245,.2); --m2g-br: 8px; }
#mols2grid { font-family: 'IBM Plex Mono', monospace; }
#mols2grid .m2g-cell { border-radius: 12px !important; transition: transform .15s, box-shadow .15s, border-color .15s; }
#mols2grid .m2g-cell:hover { transform: translateY(-2px); border-color: rgba(91,138,245,.6) !important;
       box-shadow: 0 10px 26px -12px rgba(91,138,245,.55); }
#mols2grid .data-ID { color: #7ba3ff; font-size: 11px; }
#mols2grid .data-mols2grid-id-display { display: none !important; }
#mols2grid .data-SMILES { color: #9aa5c7; font-size: 11px; }
#mols2grid input, #mols2grid .m2g-searchbar { background: #111628 !important; color: #e8edf8 !important; }
#mols2grid ul.m2g-pagination li a { color: #9aa5c7; }
#mols2grid ul.m2g-pagination li.active a { color: #fff; }
#mols2grid .m2g-dropdown, #mols2grid .m2g-search-options { color: #e8edf8; }
#mols2grid .m2g-functions { margin-bottom: 12px; }
"""
    from rdkit.Chem import Draw
    opts = Draw.MolDrawOptions()
    opts.setBackgroundColour((0.067, 0.086, 0.157, 1.0))
    opts.updateAtomPalette({
        -1: (0.91, 0.93, 0.97), 0: (0.91, 0.93, 0.97), 6: (0.91, 0.93, 0.97),
        7: (0.48, 0.64, 1.0), 8: (1.0, 0.48, 0.45), 16: (0.96, 0.78, 0.36),
        15: (1.0, 0.62, 0.3), 5: (1.0, 0.72, 0.62), 9: (0.24, 0.81, 0.56),
        17: (0.24, 0.81, 0.56), 35: (0.85, 0.47, 0.35), 53: (0.72, 0.5, 1.0),
    })
    opts.bondLineWidth = 2
    grid = mols2grid.MolGrid(df, smiles_col="SMILES", size=(170, 130),
                             prerender=True, MolDrawOptions=opts)
    out = grid.display(
        subset=["ID", "img", "SMILES"],
        n_items_per_page=30,
        selection=False,
        background_color="#111628",
        border="1px solid rgba(99,123,200,.18)",
        hover_color="rgba(91,138,245,.06)",
        gap=10,
        pad=8,
        fontfamily="'IBM Plex Mono', monospace",
        custom_css=css,
    )
    return out.data


res = st.session_state.get(RESULT_KEY)
if res:
    gap()
    smiles = res["smiles"]
    mode_label = "Classic + carbenes" if res["carbenes"] else "Classic"
    note = ""
    if res["carbenes_requested"] and not res["carbenes"]:
        note = " · no unsaturation, so carbenes do not apply"
    rchk = parse_formula(res["formula"])
    html(f"""
<div class="fade">
  <div class="result-banner">✓ Exploration completed · {len(smiles):,} isomers of {esc(res['formula'])}</div>
  <div class="stats">
    <div class="stat"><b class="g">{len(smiles):,}</b><span>Isomers found</span></div>
    <div class="stat"><b>{rchk.hdi if rchk.ok else '—'}</b><span>HDI</span></div>
    <div class="stat"><b>{rchk.n_heavy_atoms if rchk.ok else '—'}</b><span>Heavy atoms</span></div>
    <div class="stat"><b>{res['seconds']:.2f}s</b><span>{esc(mode_label)}{esc(note)}</span></div>
  </div>
</div>""")

    if smiles:
        smi_text = "\n".join(smiles) + "\n"
        csv_buf = io.StringIO()
        pd.DataFrame({"id": range(1, len(smiles) + 1), "smiles": smiles}).to_csv(csv_buf, index=False)
        c1, c2, c3, c4 = st.columns([1, 1, 1.15, 0.85])
        with c1:
            st.download_button("⬇  Download .smi", smi_text, file_name=f"{res['file_stem']}.smi",
                               mime="chemical/x-daylight-smiles", width="stretch")
        with c2:
            st.download_button("⬇  Download .csv", csv_buf.getvalue(), file_name=f"{res['file_stem']}.csv",
                               mime="text/csv", width="stretch")
        with c3:
            with st.container(key="elaya-btn"):
                st.link_button("⧉  View in 3D with ELAYA", LINKS["elaya"], width="stretch")
        with c4:
            st.button("Clear results", on_click=_clear_results, width="stretch", key="clear")

        grid = _grid_html(smiles)
        if hasattr(st, "iframe"):          # Streamlit ≥ 1.5x: auto-height iframe
            st.iframe(grid, height="content")
        else:                              # older Streamlit fallback
            rows = -(-min(len(smiles), 30) // 5)
            st.components.v1.html(grid, height=90 + rows * 185, scrolling=True)

        with st.expander(f"All {len(smiles):,} SMILES as plain text"):
            st.code(smi_text, language=None)
    else:
        st.info("No isomers were generated for this formula and mode.")
else:
    gap()
    section("How it works", "Three steps from a formula to a browsable set of isomers.")
    html("""
<div class="steps fade d1">
  <div class="step"><div class="n">1</div><div><b>Enter a formula</b>
    <span>Any combination of C, H, N, O, S, P, B, F, Cl, Br and I, e.g. C6H6 or C2H5NO2.</span></div></div>
  <div class="step"><div class="n">2</div><div><b>Grammar-driven enumeration</b>
    <span>TokenSMILES builds skeletons, inserts bonds and rings, and substitutes heteroatoms under valence rules.</span></div></div>
  <div class="step"><div class="n">3</div><div><b>Browse &amp; download</b>
    <span>Inspect every isomer, export .smi or .csv, and send structures to ELAYA SMILES for 3D.</span></div></div>
</div>""")
