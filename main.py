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
    with st.spinner("Computing chemical space…"):
        chemical_space_classic(parameters)
else:
    with st.spinner("Computing chemical space…"):
        chemical_space_carbenes(parameters)

st.divider()

st.markdown(
    """
    <p style="
        font-family:'DM Sans',sans-serif;
        font-size:14px;
        line-height:1.8;
        color:rgba(240,242,241,0.55);
        max-width:820px;
    ">
    By integrating five syntactic constraints — including branch limitations,
    balanced parentheses, and aromaticity exclusion — TokenSMILES minimises
    redundant enumerations for alkanes and ensures valence and octet-rule
    compliance through semantic parsing. Implemented in SmilX, an open-source
    tool, TokenSMILES successfully generates SMILES for classical organic systems.
    </p>
    """,
    unsafe_allow_html=True,
)

st.divider()
st.markdown(
    "<p class='footer-wrap'>Web Designers: Gabriela Yasmin Vidales Ayala &amp; José Emmanuel Soberanis Cáceres</p>",
    unsafe_allow_html=True,
)
