import streamlit as st
st.set_page_config(page_title="SmilX", layout="wide", initial_sidebar_state="collapsed")
from shared_nav import render_nav
from smilx_parameters import initial_parameters
from smilx_chemical_space import chemical_space_classic, chemical_space_carbenes
from rdkit import Chem  # noqa

render_nav("Explore")
parameters = initial_parameters()

if not parameters.opt_carbenes or parameters.molecular_formula["hdi"] == 0:
    with st.spinner("Computing chemical space…"):
        chemical_space_classic(parameters)
else:
    with st.spinner("Computing chemical space…"):
        chemical_space_carbenes(parameters)

st.divider()
