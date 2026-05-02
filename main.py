import streamlit as st

st.set_page_config(
    page_title="SmilX",
    layout="wide",
    initial_sidebar_state="collapsed"
)

from shared_nav import render_nav
from smilx_parameters import initial_parameters
from smilx_chemical_space import chemical_space_classic, chemical_space_carbenes
from rdkit import Chem  # noqa: F401

render_nav("Explore")

parameters = initial_parameters()

if not parameters.opt_carbenes or parameters.molecular_formula["hdi"] == 0:
    with st.spinner("Please wait..."):
        chemical_space_classic(parameters)
else:
    with st.spinner("Please wait..."):
        chemical_space_carbenes(parameters)

st.divider()

st.write(
    "By integrating five syntactic constraints—including branch limitations, "
    "balanced parentheses, and aromaticity exclusion—TokenSMILES minimizes "
    "redundant enumerations for alkanes and ensures valence and octet rule "
    "compliance through semantic parsing. "
    "Implemented in SmilX, an open-source tool, TokenSMILES successfully "
    "generates SMILES for classical organic systems."
)

st.divider()
st.markdown("**Web Designers:** Gabriela Yasmin Vidales Ayala & José Emmanuel Soberanis Cáceres")
