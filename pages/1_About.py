import streamlit as st
from shared_nav import render_nav

st.set_page_config(page_title="About | SmilX", layout="wide", initial_sidebar_state="collapsed")
render_nav("About")

st.markdown(
    '<h1 style="margin-bottom:0.25rem;">About SmilX</h1>'
    '<p style="color:rgba(74,85,120,0.9);font-size:14px;margin-bottom:2rem;">'
    'Open-source chemical space explorer · CINVESTAV Mérida'
    '</p>',
    unsafe_allow_html=True
)

st.info(
    "SmilX is an open-source platform for the generation and exploration of valid "
    "SMILES strings under syntactic and semantic constraints. It integrates the "
    "TokenSMILES strategy to reduce redundant enumerations, enforce valence compliance, "
    "and support systematic exploration of chemical space for classical organic systems "
    "and related representations."
)

st.info(
    "The platform is designed to be accessible, reproducible, and useful for education "
    "and research in computational chemistry, cheminformatics, and molecular design."
)

st.divider()

st.markdown(
    "<p class='footer-wrap'>"
    "Web Designers: Gabriela Yasmin Vidales Ayala &amp; José Emmanuel Soberanis Cáceres"
    "</p>",
    unsafe_allow_html=True
)
