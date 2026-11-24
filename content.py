"""
Static content for the SmilX website: links, publications, team and citation.
Edit this file to update the About / Publications / Team / How to cite pages.
"""

LINKS = {
    "app": "https://smilx-isogenerator.streamlit.app/",
    "repo": "https://github.com/LuisOrz/SmilX",
    "issues": "https://github.com/LuisOrz/SmilX/issues",
    "new_issue": "https://github.com/LuisOrz/SmilX/issues/new",
    "paper": "https://doi.org/10.1039/D5SC05004A",
    "elaya": "https://elaya-smiles.onrender.com/",
    "license": "https://www.gnu.org/licenses/gpl-3.0.html",
}

INSTITUTION = "Centro de Investigación y Estudios Avanzados (Cinvestav) Mérida"

PROJECT_TITLE = "Grammar-Driven SMILES Language with TokenSMILES and GenSMILES"
PROJECT_AUTHORS = [
    "Luis Armando Gonzalez-Ortiz", "Lisset Noriega", "Filiberto Ortiz",
    "Gabriela Vidales-Ayala", "Emmanuel Soberanis-Cáceres", "Miriam Pescador-Rojas",
    "Amilcar Meneses", "Alan Aspuru-Guzik", "Gabriel Merino",
]

WEB_DESIGNERS = "Gabriela Yasmin Vidales Ayala & José Emmanuel Soberanis Cáceres"

# ── Publications ────────────────────────────────────────────────────────────
PUBLICATIONS = [
    {
        "title": "Grammar-Driven SMILES Standardization with TokenSMILES",
        "authors": "Gonzalez-Ortiz, L. A.; Noriega, L.; Ortiz-Chi, F.; Vidales-Ayala, G.; "
                   "Soberanis-Cáceres, E.; Meneses-Viveros, A.; Aspuru-Guzik, A.; Merino, G.",
        "journal": "Chemical Science",
        "ref": "Chem. Sci. 2026, 17 (3), 1666–1675",
        "year": 2026,
        "doi": "10.1039/D5SC05004A",
        "cover": "assets/publications/10.1039_D5SC05004A.jpg",
        "tag": "SmilX · TokenSMILES",
        "featured": True,
    },
    {
        "title": "Computational Characterization of CH4S2 Isomers as Key Candidates in "
                 "Interstellar Sulfur Chemistry",
        "authors": "Flores-Larrañaga, R.; Gonzalez-Ortiz, L. A.; Ortíz-Chi, F.; Castro, M. E.; "
                   "Melendez, F. J.; Noriega, L.; Merino, G.",
        "journal": "ACS Earth and Space Chemistry",
        "ref": "ACS Earth Space Chem. 2025",
        "year": 2025,
        "doi": "10.1021/acsearthspacechem.5c00223",
        "cover": "assets/publications/10.1021_acsearthspacechem_5c00223.jpg",
        "tag": "Astrochemistry",
    },
    {
        "title": "Astrochemical Significance of C2H7NO Isomers: A Computational Perspective "
                 "on Their Stability and Detectability",
        "authors": "Noriega, L.; Gonzalez-Ortiz, L. A.; Ortíz-Chi, F.; Merino, G.",
        "journal": "The Journal of Physical Chemistry A",
        "ref": "J. Phys. Chem. A 2025, 129 (21), 4715–4723",
        "year": 2025,
        "doi": "10.1021/acs.jpca.5c01086",
        "cover": "assets/publications/10.1021_acs_jpca_5c01086.jpg",
        "tag": "Astrochemistry",
    },
    {
        "title": "C3H8O2 Isomers: Insights into Potential Interstellar Species",
        "authors": "Noriega, L.; González-Ortiz, L. A.; Ortíz-Chi, F.; Quintal, A.; "
                   "Ramírez, S. I.; Merino, G.",
        "journal": "The Journal of Physical Chemistry A",
        "ref": "J. Phys. Chem. A 2024, 128 (46), 9964–9971",
        "year": 2024,
        "doi": "10.1021/acs.jpca.4c04804",
        "cover": "assets/publications/10.1021_acs_jpca_4c04804.jpg",
        "tag": "Astrochemistry",
    },
    {
        "title": "In Quest of the Missing C2H6O2 Isomers in the Interstellar Medium: "
                 "A Theoretical Search",
        "authors": "Noriega, L.; Gonzalez-Ortiz, L. A.; Ortíz-Chi, F.; Ramírez, S. I.; Merino, G.",
        "journal": "The Journal of Physical Chemistry A",
        "ref": "J. Phys. Chem. A 2024, 128 (32), 6757–6762",
        "year": 2024,
        "doi": "10.1021/acs.jpca.4c04102",
        "cover": "assets/publications/10.1021_acs_jpca_4c04102.jpg",
        "tag": "Astrochemistry",
    },
]

# ── Team ────────────────────────────────────────────────────────────────────
TEAM = [
    {
        "name": "Luis Armando Gonzalez-Ortiz",
        "role": "Developer of SmilX / TokenSMILES",
        "desc": "Researcher focused on computational chemistry, cheminformatics, and "
                "grammar-based representations of chemical space.",
        "scholar": "https://scholar.google.com/citations?user=ZxlNW8cAAAAJ&hl=es",
        "linkedin": "https://www.linkedin.com/in/luis-ortiz-5b691127a/",
        "image": "assets/team/LuisGonzalez.jpg",
        "lead": True,
    },
    {
        "name": "Lisset Noriega",
        "role": "Researcher",
        "desc": "Computational chemist working on astrochemistry and theoretical "
                "exploration of molecular isomers.",
        "scholar": "https://scholar.google.com/citations?user=HIVYndUAAAAJ&hl=es",
        "linkedin": "https://www.linkedin.com/in/lisset-noriega-7bb9b657/",
        "image": "assets/team/LissNoriega.jpg",
    },
    {
        "name": "Filiberto Ortiz-Chi",
        "role": "Researcher",
        "desc": "Researcher in theoretical chemistry and molecular structure prediction.",
        "scholar": "https://scholar.google.com/citations?user=XBuoYGIAAAAJ&hl=es",
        "linkedin": "https://www.linkedin.com/in/filiberto-ortiz-chi-13b197147/",
        "image": "assets/team/FilibertoOrtiz.jpg",
    },
    {
        "name": "Gabriela Vidales-Ayala",
        "role": "Researcher · Web design",
        "desc": "Researcher in computational chemistry and molecular modeling.",
        "scholar": "https://scholar.google.com/citations?user=V_1RlBoAAAAJ&hl=es",
        "linkedin": "https://www.linkedin.com/in/gabriela-vidales/",
        "image": "assets/team/GabrielaVidales.jpg",
    },
    {
        "name": "Emmanuel Soberanis-Cáceres",
        "role": "Researcher · Web design",
        "desc": "Researcher focused on theoretical and computational chemistry.",
        "scholar": "https://scholar.google.com/citations?user=-LIcrVcAAAAJ&hl=es",
        "linkedin": "https://www.linkedin.com/in/e-soberanis/",
        "image": "assets/team/EmmanuelSoberanis.jpg",
    },
    {
        "name": "Miriam Pescador-Rojas",
        "role": "Researcher",
        "desc": "Researcher in computational chemistry and molecular modeling.",
        "scholar": "https://scholar.google.com/citations?hl=es&user=ft4MoT0AAAAJ",
        "linkedin": "https://www.linkedin.com/in/miriam-pescador-rojas-b5890796/",
        "image": "assets/team/MiriamPescador.jpg",
    },
    {
        "name": "Amilcar Meneses-Viveros",
        "role": "Researcher",
        "desc": "Researcher working on computational chemistry and molecular design.",
        "scholar": "https://scholar.google.com/citations?user=uyqyGxMAAAAJ&hl=es",
        "linkedin": "https://www.linkedin.com/in/amilcar-meneses-2b72a632/",
        "image": "assets/team/AmilcarMeneses.jpg",
    },
    {
        "name": "Alan Aspuru-Guzik",
        "role": "Professor",
        "desc": "Leading researcher in AI-driven chemistry, quantum chemistry, and "
                "molecular discovery.",
        "scholar": "https://scholar.google.com/citations?user=Ag_6KEgAAAAJ&hl=es",
        "linkedin": "https://www.linkedin.com/in/alanaspuru/",
        "image": "assets/team/AlanAspuru.jpg",
    },
    {
        "name": "Gabriel Merino",
        "role": "Professor",
        "desc": "Professor of theoretical chemistry specializing in molecular structure "
                "and chemical bonding.",
        "scholar": "https://scholar.google.com/citations?user=qRD50m4AAAAJ&hl=es",
        "linkedin": "https://www.linkedin.com/in/gabriel-merino-5653b22b8/",
        "image": "assets/team/GabrielMerino.jpg",
    },
]

# ── Citation ────────────────────────────────────────────────────────────────
CITATION_TEXT = (
    "Gonzalez-Ortiz, L. A.; Noriega, L.; Ortiz-Chi, F.; Vidales-Ayala, G.; "
    "Soberanis-Cáceres, E.; Meneses-Viveros, A.; Aspuru-Guzik, A.; Merino, G. "
    "Grammar-Driven SMILES Standardization with TokenSMILES. "
    "Chem. Sci. 2026, 17 (3), 1666–1675. https://doi.org/10.1039/D5SC05004A"
)

BIBTEX = """@Article{D5SC05004A,
  author    = {Gonzalez-Ortiz, Luis Armando and Noriega, Lisset and Ortiz-Chi, Filiberto and Vidales-Ayala, Gabriela and Soberanis-Cáceres, Emmanuel and Meneses-Viveros, Amilcar and Aspuru-Guzik, Alan and Merino, Gabriel},
  title     = {Grammar-driven SMILES standardization with TokenSMILES},
  journal   = {Chem. Sci.},
  year      = {2026},
  volume    = {17},
  issue     = {3},
  pages     = {1666-1675},
  publisher = {The Royal Society of Chemistry},
  doi       = {10.1039/D5SC05004A},
  url       = {http://dx.doi.org/10.1039/D5SC05004A}
}"""

RIS = """TY  - JOUR
AU  - Gonzalez-Ortiz, Luis Armando
AU  - Noriega, Lisset
AU  - Ortiz-Chi, Filiberto
AU  - Vidales-Ayala, Gabriela
AU  - Soberanis-Cáceres, Emmanuel
AU  - Meneses-Viveros, Amilcar
AU  - Aspuru-Guzik, Alan
AU  - Merino, Gabriel
TI  - Grammar-driven SMILES standardization with TokenSMILES
JO  - Chem. Sci.
PY  - 2026
VL  - 17
IS  - 3
SP  - 1666
EP  - 1675
PB  - The Royal Society of Chemistry
DO  - 10.1039/D5SC05004A
UR  - http://dx.doi.org/10.1039/D5SC05004A
ER  - """

ABSTRACT = (
    "The redundancy of SMILES notation, where multiple strings can describe the same "
    "molecule, remains a challenge in computational chemistry and cheminformatics. To "
    "mitigate this issue, we introduce TokenSMILES, a grammatical framework that "
    "standardizes SMILES into structured sentences composed of context-free words. By "
    "applying five syntactic constraints (including branch limitations, balanced "
    "parentheses, and aromaticity exclusion), TokenSMILES minimizes redundant SMILES "
    "enumerations for alkanes while maintaining valence and octet compliance through "
    "semantic parsing rules. TokenSMILES does not replace SMILES but rather formalizes its "
    "syntax into a standardized, machine-interpretable form. This grammatical structure "
    "enables controlled generation and manipulation of valid SMILES strings, ensuring "
    "syntactic and semantic consistency while substantially reducing redundancy. "
    "Implemented into SmilX, an open-source tool, TokenSMILES generates valid SMILES with "
    "accuracy comparable to existing computational implementations for molecules with low "
    "hydrogen deficiency (HDI ≤ 4). Its applicability extends beyond alkanes through "
    "stoichiometric modifications such as bond insertion, cyclization, and heteroatom "
    "substitution. Nevertheless, challenges remain for highly unsaturated systems, where "
    "canonicalization artifacts highlight the need for dynamic feasibility checks. By "
    "integrating linguistic principles with cheminformatics, TokenSMILES establishes a "
    "scalable framework for systematic chemical space exploration, supporting applications "
    "in drug discovery, materials design, and machine learning-driven molecular innovation."
)
