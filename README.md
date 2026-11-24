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
│   └── components.py          # Navbar, headers, footer, image helpers
├── content.py                 # Editable texts: team, publications, citation, links
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
