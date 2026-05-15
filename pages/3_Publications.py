import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from shared_nav import render_nav

st.set_page_config(page_title="Publications | SmilX", layout="wide", initial_sidebar_state="collapsed")
render_nav("Publications")

st.title("Publications")

publications = [
    {"title": "Grammar-Driven SMILES Standardization with TokenSMILES",
     "authors": "Gonzalez-Ortiz, L. A.; Noriega, L.; Ortiz-Chi, F.; Vidales-Ayala, G.; Soberanis-Cáceres, E.; Meneses-Viveros, A.; Aspuru-Guzik, A.; Merino, G.",
     "journal": "Chem. Sci. 2025",
     "doi": "10.1039/D5SC05004A",
     "url": "https://doi.org/10.1039/D5SC05004A"},
    {"title": "In Quest of the Missing C2H6O2 Isomers in the Interstellar Medium: A Theoretical Search",
     "authors": "Noriega, L.; Gonzalez-Ortiz, L. A.; Ortíz-Chi, F.; Ramírez, S. I.; Merino, G.",
     "journal": "J. Phys. Chem. A 2024, 128 (32), 6757–6762.",
     "doi": "10.1021/acs.jpca.4c04102",
     "url": "https://doi.org/10.1021/acs.jpca.4c04102"},
    {"title": "C3H8O2 Isomers: Insights into Potential Interstellar Species",
     "authors": "Noriega, L.; González-Ortiz, L. A.; Ortíz-Chi, F.; Quintal, A.; Ramírez, S. I.; Merino, G.",
     "journal": "J. Phys. Chem. A 2024, 128 (46), 9964–9971.",
     "doi": "10.1021/acs.jpca.4c04804",
     "url": "https://doi.org/10.1021/acs.jpca.4c04804"},
    {"title": "Astrochemical Significance of C2H7NO Isomers: A Computational Perspective on Their Stability and Detectability",
     "authors": "Noriega, L.; Gonzalez-Ortiz, L. A.; Ortíz-Chi, F.; Merino, G.",
     "journal": "J. Phys. Chem. A 2025, 129 (21), 4715–4723.",
     "doi": "10.1021/acs.jpca.5c01086",
     "url": "https://doi.org/10.1021/acs.jpca.5c01086"},
    {"title": "Computational Characterization of CH4S2 Isomers as Key Candidates in Interstellar Sulfur Chemistry",
     "authors": "Flores-Larrañaga, R.; Gonzalez-Ortiz, L. A.; Ortíz-Chi, F.; Castro, M. E.; Melendez, F. J.; Noriega, L.; Merino, G.",
     "journal": "ACS Earth Space Chem. 2025",
     "doi": "10.1021/acsearthspacechem.5c00223",
     "url": "https://doi.org/10.1021/acsearthspacechem.5c00223"},
]

st.divider()

for pub in publications:
    with st.container(border=True):
        st.subheader(pub["title"])
        st.write(pub["authors"])
        st.caption(f"{pub['journal']}  |  DOI: {pub['doi']}")
        st.link_button("Open publication ↗", pub["url"])

st.divider()
st.markdown("**Web Designers:** Gabriela Yasmin Vidales Ayala & José Emmanuel Soberanis Cáceres")
