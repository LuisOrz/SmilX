"""About SmilX · what it is, how TokenSMILES works, scope and features."""
import streamlit as st

from content import LINKS, INSTITUTION
from ui.components import html, page_header, section, gap

page_header(
    "About SmilX",
    'A grammar for exploring <span class="grad">chemical space</span>',
    "<b>SmilX</b> is open-source software for exploring the chemical space of isomers using the "
    "SMILES language under grammar constraints. Given a molecular formula, it systematically "
    "constructs chemically valid molecular graphs through a grammar-driven generation process.",
)

html(f"""
<div class="grid c4 fade d1">
  <div class="card"><div class="icon-badge">5</div><h4>Syntactic constraints</h4>
    <p>Including branch limitations, balanced parentheses and aromaticity exclusion.</p></div>
  <div class="card"><div class="icon-badge">11</div><h4>Supported elements</h4>
    <p>C, H, N, O, S, P, B, F, Cl, Br and I, each with its own valence rule.</p></div>
  <div class="card"><div class="icon-badge green">≤4</div><h4>HDI sweet spot</h4>
    <p>Accuracy comparable to existing implementations for low hydrogen deficiency.</p></div>
  <div class="card"><div class="icon-badge green">GPL</div><h4>Open source</h4>
    <p>Released under GNU GPL v3 and developed at {INSTITUTION.split(' (')[0]} (Cinvestav) Mérida.</p></div>
</div>
""")

gap()
col1, col2 = st.columns(2, gap="large")
with col1:
    html("""
<div class="card fade">
  <div class="eyebrow">The language</div>
  <h4>What is TokenSMILES?</h4>
  <p>SMILES is redundant: many different strings can describe the same molecule.
  <b>TokenSMILES</b> is a grammatical framework that standardizes SMILES into structured
  sentences made of context-free words. It does not replace SMILES; it formalizes its syntax into a
  standardized, machine-interpretable form.</p>
  <p style="margin-top:.7rem">Five syntactic constraints minimize redundant enumerations for alkanes,
  while semantic parsing rules keep every structure compliant with valence and the octet rule.</p>
</div>""")
with col2:
    html("""
<div class="card fade d1">
  <div class="eyebrow">The tool</div>
  <h4>What does SmilX do?</h4>
  <p>SmilX implements TokenSMILES as an interactive explorer. It starts from saturated carbon
  skeletons and extends them through stoichiometric modifications (bond insertion, cyclization
  and heteroatom substitution), so it reaches far beyond alkanes.</p>
  <p style="margin-top:.7rem">The result is a systematic enumeration of candidate isomers that is
  RDKit-friendly and ready for downstream cheminformatics tasks.</p>
</div>""")

gap()
section("Chemical rules enforced", "Every generated graph is checked against these rules.")
html("""
<div class="grid c4 fade">
  <div class="card"><div class="icon-badge">V</div><h4>Valence constraints</h4><p>No atom exceeds its allowed number of bonds.</p></div>
  <div class="card"><div class="icon-badge">—</div><h4>Connectivity</h4><p>Every structure is a single connected molecular graph.</p></div>
  <div class="card"><div class="icon-badge">=</div><h4>Unsaturation patterns</h4><p>Double bonds, triple bonds and rings add up to the HDI.</p></div>
  <div class="card"><div class="icon-badge">◯</div><h4>Ring closures</h4><p>Cycles are formed with explicit validity checks.</p></div>
</div>""")

gap()
section("How SmilX builds a chemical space", "The generation pipeline behind every exploration.")
html("""
<div class="pipeline fade">
  <div class="pipe"><div class="k">01</div><div><b>Parse the formula and compute the HDI</b>
    <p>The molecular formula (e.g. <code>C6H6</code>, <code>C2H5NO2</code>) is read and the Hydrogen Deficiency Index tells how many unsaturations are needed.</p></div></div>
  <div class="pipe"><div class="k">02</div><div><b>Enumerate unsaturation patterns</b>
    <p>All valid combinations of double bonds, triple bonds and rings that add up to the HDI are listed.</p></div></div>
  <div class="pipe"><div class="k">03</div><div><b>Build carbon skeletons with the grammar</b>
    <p>TokenSMILES words assemble the heavy-atom backbone and its branching. Skeletons up to 10 heavy atoms are precomputed for speed.</p></div></div>
  <div class="pipe"><div class="k">04</div><div><b>Insert bonds and close rings</b>
    <p>Each skeleton is dehydrogenated step by step: double bonds, triple bonds and ring closures, removing duplicates as it goes.</p></div></div>
  <div class="pipe"><div class="k">05</div><div><b>Substitute heteroatoms</b>
    <p>Carbon positions are replaced by N, O, S, P, B or halogens wherever valence allows, matching the exact composition of the formula.</p></div></div>
  <div class="pipe"><div class="k">06</div><div><b>Canonicalize and export</b>
    <p>RDKit canonical SMILES remove redundant isomers. The final set can be browsed and downloaded as .smi or .csv.</p></div></div>
</div>""")

gap()
section("Supported elements", "Valence used by the grammar is shown in the corner of each tile.")
ELEMENTS = [("C", "Carbon", 4, "c"), ("H", "Hydrogen", 1, "h"), ("N", "Nitrogen", 3, ""),
            ("O", "Oxygen", 2, ""), ("S", "Sulfur", 2, ""), ("P", "Phosphorus", 3, ""),
            ("B", "Boron", 3, ""), ("F", "Fluorine", 1, ""), ("Cl", "Chlorine", 1, ""),
            ("Br", "Bromine", 1, ""), ("I", "Iodine", 1, "")]
html('<div class="elements fade">' + "".join(
    f'<div class="el {cls}"><span class="val">{v}</span><div class="sym">{s}</div><div class="nm">{n}</div></div>'
    for s, n, v, cls in ELEMENTS) + "</div>")

gap()
section("Exploration modes")
html("""
<div class="grid c3 fade">
  <div class="card"><span class="tagpill green">Available</span>
    <h4 style="margin-top:.7rem!important">Exhaustive classic</h4>
    <p>Enumerates the classical isomers of the formula: every valid combination of skeleton,
    unsaturations and heteroatom positions.</p></div>
  <div class="card"><span class="tagpill green">Available</span>
    <h4 style="margin-top:.7rem!important">Classic + carbenes</h4>
    <p>Also includes divalent carbon centres, written <code>[C]</code>. Each carbene uses one
    degree of unsaturation, so it applies to formulas with HDI &gt; 0.</p></div>
  <div class="card"><span class="tagpill">In development</span>
    <h4 style="margin-top:.7rem!important">Bioinspired search</h4>
    <p>An evolutionary search with population, crossover and mutation operators and force-field
    fitness (MMFF94 or UFF), with optional TorchANI refinement.</p></div>
</div>""")

gap()
c1, c2 = st.columns([1.1, 1], gap="large")
with c1:
    section("Key features")
    html("""
<div class="card fade" style="padding:1rem 1.35rem">
<ul style="margin:0;padding-left:1.1rem">
  <li>Molecular formula parsing (e.g. <code>C6H6</code>, <code>C2H5NO2</code>)</li>
  <li>Hydrogen Deficiency Index (HDI) computation</li>
  <li>Enumeration of valid unsaturation patterns (double bonds, triple bonds, rings)</li>
  <li>Grammar-based construction of carbon skeletons and branching</li>
  <li>Cycle formation (ring closures) with validity checks</li>
  <li>Heteroatom substitution under valence constraints</li>
  <li>Interactive exploration via Streamlit, with .smi and .csv export</li>
  <li>RDKit-friendly workflow for downstream cheminformatics tasks</li>
</ul></div>""")
with c2:
    section("Scope & limitations")
    html("""
<div class="card fade d1" style="padding:1rem 1.35rem">
<ul style="margin:0;padding-left:1.1rem">
  <li>Best accuracy for molecules with low hydrogen deficiency (<b>HDI ≤ 4</b>).</li>
  <li>Highly unsaturated systems remain challenging: canonicalization artifacts call for dynamic feasibility checks.</li>
  <li>Aromaticity is excluded from the grammar, so aromatic rings appear in Kekulé form.</li>
  <li>Formulas above 10 heavy atoms are not precomputed and can take minutes.</li>
</ul></div>""")
    gap()
    section("Applications")
    html("""
<div class="chips fade" style="justify-content:flex-start">
  <span class="chip blue">Drug discovery</span><span class="chip blue">Materials design</span>
  <span class="chip blue">Machine-learning datasets</span><span class="chip blue">Astrochemistry</span>
  <span class="chip blue">Teaching cheminformatics</span>
</div>""")

gap()
section("Run SmilX locally", "Use the web app with no installation, or run it on your own machine.")
st.code(f"""git clone {LINKS['repo']}.git
cd SmilX
python -m venv venv
source venv/bin/activate          # Windows: venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run main.py""", language="bash")

gap()
html(f"""
<div class="card featured fade" style="display:flex;flex-wrap:wrap;gap:1rem;align-items:center;justify-content:space-between">
  <div><h4>Using SmilX in your research?</h4><p>Please cite the TokenSMILES paper in Chemical Science.</p></div>
  <div style="display:flex;gap:8px;flex-wrap:wrap">
    <a class="btn-link" href="{LINKS['paper']}" target="_blank" rel="noopener">Read the paper ↗</a>
    <a class="btn-link green" href="{LINKS['repo']}" target="_blank" rel="noopener">View source ↗</a>
  </div>
</div>""")
