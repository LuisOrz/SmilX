"""Explore · enumerate the isomers of a molecular formula with TokenSMILES."""
import io
import json
import shutil
import time
from urllib.parse import quote

import pandas as pd
import streamlit as st

from content import LINKS, INSTITUTION, PUBLICATIONS
from isomer_info import describe_all, FUNCTIONAL_GROUPS
from smilx_chemistry_tools import get_unsaturations
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
    st.session_state.formula_input = st.session_state.get("_formula", "")
if "mode_input" not in st.session_state or st.session_state.mode_input is None:
    st.session_state.mode_input = st.session_state.get("_mode", MODES[0])


def _remember():
    st.session_state._formula = st.session_state.formula_input
    st.session_state._mode = st.session_state.mode_input or MODES[0]


def _on_formula():            # value committed (Enter or leaving the field): just remember it
    _remember()


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


# ── Hero (always the same, before and after exploring) ────────────────────
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

# ── Explorer card: formula · mode · Explore ────────────────────────────────
with st.container(key="explorer"):
    c_in, c_mode, c_btn = st.columns([2.1, 1.55, 0.85], vertical_alignment="bottom", gap="medium")
    with c_in:
        st.text_input("Molecular formula", key="formula_input",
                      placeholder="Type a formula, e.g. C6H6", on_change=_on_formula, max_chars=40)
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

    if not chk.ok and chk.raw:            # empty field: the typing animation is the hint
        html(f'<p class="inline-msg err"><i>!</i>{esc(chk.error)}</p>')
    elif chk.warning:
        html(f'<p class="inline-msg warn"><i>!</i>{esc(chk.warning)}</p>')

# Typing animation in the empty formula field (examples typed and deleted)
run_js("window.__smilxExamples = " + json.dumps(EXAMPLES) + ";")
js_file("typewriter.js")

# Enter in the formula field = press Explore (leaving the field does not explore)
run_js("""
(() => {
  if (window.__smilxEnter) return; window.__smilxEnter = true;
  document.addEventListener('keydown', (e) => {
    if (e.key !== 'Enter' || !e.target.closest || !e.target.closest('.st-key-formula_input')) return;
    let n = 0;
    const t = setInterval(() => {          // wait for Streamlit to commit the value
      const b = document.querySelector('.st-key-go button');
      if ((b && !b.disabled) || ++n > 20) { clearInterval(t); if (b && !b.disabled) b.click(); }
    }, 120);
  }, true);
})();
""")

# "Start here" label on the formula field until the user clicks into it
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
#mols2grid .m2g-dropdown.m2g-actions { width: 40px !important; }
#mols2grid .m2g-dropdown.m2g-actions .m2g-icon { filter: none !important; }
#mols2grid .m2g-dropdown.m2g-actions .m2g-icon svg { fill: #e6e8f0 !important; }
#mols2grid .m2g-dropdown.m2g-actions:hover .m2g-icon svg { fill: #ffffff !important; }
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
/* zoom affordance */
#mols2grid .m2g-cell .smx-zoom { position: absolute; right: 8px; top: 8px; width: 28px; height: 28px; border-radius: 50%;
  display: grid; place-items: center; color: #2b4fb8; background: #eef2ff; cursor: zoom-in; z-index: 3;
  opacity: 0; transform: scale(.85); transition: opacity .15s, transform .15s; }
#mols2grid .m2g-cell:hover .smx-zoom, #mols2grid .m2g-cell.smx-hint .smx-zoom { opacity: 1; transform: none; }
@media (hover: none) { #mols2grid .m2g-cell .smx-zoom { opacity: 1; transform: none; } }
#mols2grid .m2g-cell.smx-hint { animation: smxHint 1.8s ease-in-out infinite; }
#mols2grid .m2g-cell .smx-hint-label { display: none; }
#mols2grid .m2g-cell.smx-hint .smx-hint-label { display: block; position: absolute; left: 50%; bottom: 34px; transform: translateX(-50%);
  background: #233a6b; color: #d9e2ff; font: 600 12px 'Outfit', system-ui, sans-serif; padding: 4px 10px; border-radius: 999px;
  white-space: nowrap; pointer-events: none; z-index: 3; box-shadow: 0 4px 10px rgba(0,0,0,.25); }
@keyframes smxHint {
  0%, 100% { box-shadow: 0 0 0 0 rgba(173,198,255,0), 0 0 0 rgba(91,138,245,0); }
  50% { box-shadow: 0 0 0 3px rgba(173,198,255,.95), 0 0 26px rgba(91,138,245,.65); }
}
@media (prefers-reduced-motion: reduce) { #mols2grid .m2g-cell.smx-hint { animation: none; box-shadow: 0 0 0 3px #adc6ff; } }
#mols2grid .m2g-cb-wrap input[type=checkbox] + .m2g-cb { border-color: #8a93a8; }
#mols2grid .data-mols2grid-id-display { display: none !important; }
#mols2grid .data-ID { color: #2b4fb8 !important; font: 600 12px 'IBM Plex Mono', monospace; }
#mols2grid .data-SMILES { color: #3f4659 !important; font: 500 11.5px 'IBM Plex Mono', monospace; word-break: break-all; }
"""


GROUP_SMARTS = dict(FUNCTIONAL_GROUPS)


def _summary_html(chk, smiles: list[str], props: dict, res: dict) -> str:
    """Chemical-space summary under the grid. Every number is counted from the
    RDKit data of the isomers shown above (no external or estimated values)."""
    info = [v for v in props.values() if v]
    n = len(smiles)
    if not info:
        return ""
    groups: dict[str, int] = {}
    for v in info:
        for g in v["groups"]:
            groups[g] = groups.get(g, 0) + 1
    ring_sizes: dict[int, int] = {}
    for v in info:
        for size in set(v["ring_sizes"]):
            ring_sizes[size] = ring_sizes.get(size, 0) + 1
    cyclic = sum(1 for v in info if v["rings"])
    chiral = sum(1 for v in info if v["stereocenters"] or v["stereo_double_bonds"])
    total_stereo = sum((v["stereoisomers"] or 1) for v in info)
    first = info[0]
    pats = []
    if chk.ok:
        mf = {e: chk.counts.get(e, 0) for e in SUPPORTED_ELEMENTS}
        mf["hdi"] = chk.hdi
        pats = [u for u in get_unsaturations(mf, chk.n_heavy_atoms)
                if chk.hdi == u.double_bonds + 2 * u.triple_bonds + u.cycles]

    def stat(value, label, tip=""):
        t = f' class="tip" tabindex="0" data-tip="{esc(tip)}"' if tip else ""
        return f'<div class="ss-stat"><b>{value}</b><span{t}>{esc(label)}</span></div>'

    stats = "".join([
        stat(f"{first['mw']:.2f}", "g/mol (all isomers)", "Same molecular formula, so every isomer has the same molar mass."),
        stat(chk.hdi if chk.ok else "—", "HDI", "Hydrogen deficiency index: rings + π bonds the formula requires."),
        stat(len(pats), "unsaturation patterns", "Combinations of double bonds, triple bonds and rings that add up to the HDI."),
        stat(f"{n - cyclic} / {cyclic}", "acyclic / cyclic"),
        stat(chiral, "with stereo elements", "Isomers with a stereocenter or a stereogenic double bond (RDKit)."),
        stat(f"{total_stereo:,}", "stereoisomers in total", "Sum of the possible stereoisomers of every constitutional isomer (RDKit enumeration)."),
    ])

    rows = []
    for name, count in sorted(groups.items(), key=lambda kv: (-kv[1], kv[0])):
        pct = 100 * count / n
        sma = GROUP_SMARTS.get(name)
        attrs = (f'data-smarts="{esc(sma)}" role="button" tabindex="0" title="Show only these in the grid"'
                 if sma else 'title="Not searchable by SMARTS"')
        rows.append(f'<div class="ss-row{" link" if sma else ""}" {attrs}><span class="nm">{esc(name)}</span>'
                    f'<span class="bar"><i style="width:{pct:.1f}%"></i></span><span class="ct">{count}</span></div>')
    groups_html = "".join(rows) or '<p class="ss-note">No functional groups: saturated hydrocarbons only.</p>'
    rings_html = " · ".join(f"{k}-membered <b>{v}</b>" for k, v in sorted(ring_sizes.items())) or "none"

    return f"""
<section class="ss fade">
  <div class="ss-head"><h3>Chemical space of {chk.pretty if chk.ok else esc(res['formula'])}</h3>
    <span class="ss-note">Counted with RDKit from the {n:,} isomers above</span></div>
  <div class="ss-stats">{stats}</div>
  <div class="ss-cols">
    <div><h4>Functional groups <span class="ss-note">click one to filter the grid</span></h4>
      <div class="ss-groups">{groups_html}</div>
      <button class="ss-reset" type="button" data-smarts="">Show all isomers</button></div>
    <div><h4>Rings</h4><p class="ss-rings">{rings_html}</p>
      <p class="ss-note">Isomers containing at least one ring of each size.</p></div>
  </div>
</section>"""


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
        # results on screen → the "Start here" cue has done its job
        run_js("document.body.classList.add('smilx-started'); try { sessionStorage.setItem('smilxStarted', '1'); } catch (e) {}")
        if smiles:
            props = isomer_props(tuple(smiles))
            st.iframe(_grid_html(smiles, props), height="content")
            html(_summary_html(rchk, smiles, props, res))
        else:
            st.info("No isomers were generated for this formula and mode.")

    run_js("""
(() => {
  if (window.__smilxSS) return; window.__smilxSS = true;
  const act = (el) => {
    const fr = document.querySelector('.st-key-results iframe');
    try { fr.contentWindow.smilxSmarts(el.dataset.smarts); } catch (e) { return; }
    document.querySelectorAll('.ss-row.on').forEach(r => r.classList.remove('on'));
    if (el.classList.contains('ss-row')) el.classList.add('on');
    const bar = document.getElementById('smilx-res-bar');
    if (bar) bar.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };
  document.addEventListener('click', (e) => { const el = e.target.closest && e.target.closest('[data-smarts]'); if (el && el.closest('.ss')) act(el); });
  document.addEventListener('keydown', (e) => { if ((e.key === 'Enter' || e.key === ' ') && e.target.matches && e.target.matches('.ss [data-smarts]')) { e.preventDefault(); act(e.target); } });
})();
""")

    if just_ran:
        # Gentle: scroll only when the results header is below the fold, and then
        # only far enough to show the explorer + results header + first row.
        run_js(f"/* {time.time_ns()} */\n" + """
(() => {
  const go = () => {
    const bar = document.querySelector('#smilx-res-bar');
    const exp = document.querySelector('.st-key-explorer');
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
