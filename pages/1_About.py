import streamlit as st
from shared_nav import render_nav

st.set_page_config(page_title="About | SmilX", layout="wide", initial_sidebar_state="collapsed")
render_nav("About")

st.title("About")

st.info(
    "SmilX is an open-source platform for the generation and exploration of valid SMILES strings "
    "under syntactic and semantic constraints. It integrates the TokenSMILES strategy to reduce "
    "redundant enumerations, enforce valence compliance, and support systematic exploration of "
    "chemical space for classical organic systems and related representations."
)

st.info(
    "The platform is designed to be accessible, reproducible, and useful for education and "
    "research in computational chemistry, cheminformatics, and molecular design."
)

st.divider()
st.markdown("**Web Designers:** Gabriela Yasmin Vidales Ayala & José Emmanuel Soberanis Cáceres")
