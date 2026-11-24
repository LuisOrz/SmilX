<p align="center">
  <img src="https://github.com/LuisOrz/SmilX/blob/main/logo_smilx.png" width="240">
</p>

<h1 align="center">SmilX (TokenSMILES Framework)</h1>

<p align="center"><b>Grammar-Constrained Chemical Space Exploration for Isomers using SMILES</b></p>

<p align="center"><a href="https://smilx-isogenerator.streamlit.app/">🌐 Try the Web App</a></p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![RDKit](https://img.shields.io/badge/RDKit-Compatible-green)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![License](https://img.shields.io/badge/License-GPLv3-orange)
![Status](https://img.shields.io/badge/Status-Research-purple)

</p>

---

## What is SmilX?

**SmilX is a software designed to explore the chemical space of isomers using the SMILES language under grammar constraints.**

Given a **molecular formula**, SmilX systematically constructs chemically valid molecular graphs through a **grammar-driven generation process**, ensuring consistency with chemical rules such as valence constraints, connectivity, unsaturation patterns and ring closures.

It implements **TokenSMILES**, a grammatical framework that standardizes SMILES into structured sentences of context-free words. Five syntactic constraints (including branch limitations, balanced parentheses and aromaticity exclusion) minimize redundant enumerations, while semantic parsing keeps every structure valence- and octet-compliant.

Developed at **Centro de Investigación y Estudios Avanzados (CINVESTAV) Mérida**.

---

## Key Features

- Molecular formula parsing and validation (e.g., `C6H6`, `C2H5NO2`)
- Hydrogen Deficiency Index (HDI) computation
- Enumeration of valid unsaturation patterns (double bonds, triple bonds, rings)
- Grammar-based construction of carbon skeletons and branching
- Cycle formation (ring closures) with validity checks
- Heteroatom substitution under valence constraints — `N`, `O`, `S`, `P`, `B`, `F`, `Cl`, `Br`, `I`
- Optional carbene search (divalent `[C]` centres)
- Interactive molecule grid, `.smi` / `.csv` export and a link to ELAYA SMILES for 3D
- RDKit-friendly workflow for downstream cheminformatics tasks

---

## Usage

### Online (recommended)

https://smilx-isogenerator.streamlit.app/ — no installation required.

### Run locally

```bash
git clone https://github.com/LuisOrz/SmilX.git
cd SmilX
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run main.py
```

---

## Project Structure

```
SmilX
├── main.py                    # Entry point: page config, theme, navbar, router
├── app_pages/
│   ├── explore.py             # Formula input, live analysis, results grid
│   ├── about.py               # What SmilX / TokenSMILES is, pipeline, scope
│   ├── publications.py
│   ├── cite.py                # Citation, BibTeX, RIS
│   ├── team.py
│   └── support.py
├── ui/
│   ├── theme.py               # SmilX design system (CSS)
│   ├── components.py          # Navbar, headers, footer, image helpers
│   ├── isomer_modal.py        # Loader for the isomer zoom dialog + grid hooks
│   └── static/                # smilx.css, fab.js, isomer_modal.css/js, grid_hooks.js
├── content.py                 # Editable texts: team, publications, citation, links
├── isomer_info.py             # RDKit descriptors / functional groups for the zoom dialog
├── smilx_parameters.py        # Formula parsing/validation and run parameters
├── smilx_chemistry_tools.py   # TokenSMILES / SMILES objects and chemistry rules
├── smilx_chemical_space.py    # Generators (classic and carbenes)
├── dependences/valence_4/     # Precomputed skeletons (2–10 heavy atoms)
├── assets/                    # Logo, favicon, team photos, journal covers
└── .streamlit/config.toml
```

To update team members, publications or the citation, edit **`content.py`** only.

---

## Authors

Luis Armando Gonzalez-Ortiz, Lisset Noriega, Filiberto Ortiz, Gabriela Vidales-Ayala, Emmanuel Soberanis-Cáceres, Miriam Pescador-Rojas, Amilcar Meneses, Alan Aspuru-Guzik and Gabriel Merino.

Web design: Gabriela Yasmin Vidales Ayala & José Emmanuel Soberanis Cáceres.

---

## License

**GNU General Public License v3.0 (GPL-3.0)**

---

## Citation

If you use SmilX in scientific research, please cite:

Gonzalez-Ortiz, L. A.; Noriega, L.; Ortiz-Chi, F.; Vidales-Ayala, G.; Soberanis-Cáceres, E.; Meneses-Viveros, A.; Aspuru-Guzik, A.; Merino, G. Grammar-driven SMILES standardization with TokenSMILES. *Chemical Science*, 2026, 17, 1666–1675. DOI: https://doi.org/10.1039/D5SC05004A

```bibtex
@Article{D5SC05004A,
  author    = {Gonzalez-Ortiz, Luis Armando and Noriega, Lisset and Ortiz-Chi, Filiberto and Vidales-Ayala, Gabriela and Soberanis-Cáceres, Emmanuel and Meneses-Viveros, Amilcar and Aspuru-Guzik, Alan and Merino, Gabriel},
  title     = {Grammar-driven SMILES standardization with TokenSMILES},
  journal   = {Chem. Sci.},
  year      = {2026},
  volume    = {17},
  issue     = {3},
  pages     = {1666-1675},
  doi       = {10.1039/D5SC05004A}
}
```

---

## Changelog — website v2.6 (alignment pass)

- One 8 px spacing grid, verified by measurement at 1440, 1318, 1024 and 390 px wide:
  - Formula field, mode selector and *Explore* are all 48 px; their labels sit on the same line, 8 px above the controls. The text field is now styled through `stTextInputRootElement`, the element current Streamlit actually renders.
  - Results bar is one HTML row: total · Download .smi · 3D with ELAYA · ⋮. Every item is 40 px tall on the same centre line. The downloads are direct links, so nothing depends on how Streamlit stacks widgets.
  - Search row, results bar, grid toolbar and cards share the same left and right edges. Gaps: label→examples 8 px, examples→results 32 px, bar→grid 16 px, grid toolbar→cards 16 px.
  - Pagination is no longer clipped; the compact header wraps instead of cutting text.
- *Clear results* was removed: a new *Explore* replaces the results.

## Changelog — website v2.5 (no jumps, no overlaps)

- **Styles are loaded from `ui/static/*.css|js` on every rerun.** Before, they lived inside a Python module that Streamlit keeps in memory until the server restarts, so an updated app could show new pages with the *old* look (overlapping blocks, a huge ELAYA logo, borders that had been removed). The footer shows the running version (`Web v2.5`).
- **Search → results pattern:** large logo and credits on the landing page; once there are results, a compact one-line header so the formula field and the results share the first screen. On desktop no scrolling is needed after *Explore*; on phones the page moves only enough to keep the formula visible.
- Results bar is a single flexible row (total · Download .smi · 3D with ELAYA · ⋮) that wraps on small screens instead of overlapping.
- The scroll button is a small pill at the bottom centre (clear of Streamlit Cloud's corner badges) and appears only when useful: *See results*, *Scroll down* at the top of long pages, *Back to top*.

### Updating a running app

Since v2.6.1, `main.py` detects when the project's own modules changed on disk and reloads them, so a redeploy no longer mixes new pages with old modules (the cause of `ImportError` after an update). A reboot is still the cleanest option:

After replacing files, restart once so Python modules reload: stop and rerun `streamlit run main.py` locally, or use **⋮ → Reboot app** on Streamlit Community Cloud. Check the footer shows the new version.

## Changelog — website v2.4 (back to the original simplicity)

- Explore page header as in the original SmilX: logo, paper credit, institution and GPL v3 line; no extra panels.
- Explorer without frame or fill; more space between sections; "Try an example" on its own line.
- Examples and mode only set the inputs: nothing runs until **Explore** is pressed (or Enter in the formula field).
- Results row: total · *Download .smi* · *3D with ELAYA* (with the ELAYA emblem) · ⋮ menu for .csv and Clear.

## Changelog — website v2.3 (minimal layout)

- Removed the *How it works* strip, the results data line and the grid help text.
- The results header shows only the total of isomers; downloads (.smi, .csv), *3D with ELAYA* and *Clear results* are grouped in a single **Export** menu.
- Fewer borders, background fills and shadows across all pages; tighter spacing.

## Changelog — website v2.2 (explorer flow & isomer zoom)

- **Explorer order:** *How it works* now comes before the tool; the formula, mode and *Explore* sit on one row; "No formula in mind? Try an example" below.
- **"Start here" cue:** the formula field blinks until the user clicks into it (remembered for the session).
- **One compact results line:** isomer count, HDI, heavy atoms, unsaturation patterns (with explanations on hover), composition, mode and time. Compact action buttons.
- **Every Explore scrolls to the grid** automatically.
- **Grid features from mols2grid kept and explained:** Text search (ID/SMILES text) vs Substructure (SMARTS) search with highlighted matches, one-click SMARTS examples, sorting, checkboxes plus select/copy/save actions.
- **Isomer zoom:** clicking a structure opens a dialog with a large 2D depiction and RDKit-computed data: functional groups (curated SMARTS), rings and sizes, stereocenters and possible stereoisomers, MW, monoisotopic mass, HBD/HBA, rotatable bonds, TPSA, Crippen logP, Fsp3, InChI/InChIKey. It also shows whether the structure is a **known compound in PubChem** (name, IUPAC name, CID), queried live by InChIKey. ← → to browse, Esc to close.

## Changelog — website v2.1 (UX & Material dark theme)

- **Material Design dark theme:** navy-tinted surfaces instead of pure black, tonal elevation, three text-emphasis levels and a desaturated SmilX blue (`#adc6ff`). All text passes WCAG AA (≥ 4.5:1); the dimmest text is 5:1.
- **Theme no longer depends on `config.toml`:** every widget is styled in `ui/theme.py`, so pills, mode selector and focus colors look the same wherever the app is launched.
- **Compact explorer:** formula field and *Explore* on one row; examples and mode on the next; live analysis in a single strip.
- **Faster flow:** press Enter or click an example to explore immediately; switching mode refreshes visible results; the page scrolls to the results and shows a confirmation toast.
- **Animated scroll button** (bottom right): *Scroll down* → *See results* → *Back to top*.
- **2D structures back on white**, with a readable dark toolbar. The white flashes on hover/selection in mols2grid's search, sort and pagination controls are gone.

## Changelog — website v2

- **Navigation fixed:** one router (`st.navigation`) with an in-app navbar. Pages switch without reloading, and results and inputs are kept when you come back to Explore. The old menu had duplicated links and URLs that returned "Page not found".
- **Exploration runs on demand:** it starts only when you press *Explore*, not on every interaction. Results are cached per formula and mode.
- **Formula validation:** invalid input (lowercase, unsupported elements, impossible HDI) shows a clear message instead of crashing the app.
- **Halogen bug fixed:** formulas with Cl, Br or I (e.g. CH3I, C2H5Cl) used to return 0 isomers because the element order used in the final composition check did not match.
- **Concurrent users:** each run writes to its own temporary folder, so two people exploring the same formula no longer overwrite each other's files.
- New About, Publications, How to cite, Team and Support pages, plus `.csv` export.
