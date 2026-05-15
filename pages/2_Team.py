import streamlit as st
from shared_nav import render_nav

st.set_page_config(page_title="Team | SmilX", layout="wide", initial_sidebar_state="collapsed")
render_nav("Team")

st.markdown(
    '<h1 style="margin-bottom:0.25rem;">Team</h1>'
    '<p style="color:rgba(74,85,120,0.9);font-size:14px;margin-bottom:1.5rem;">'
    'Centro de Investigación y Estudios Avanzados (CINVESTAV) Mérida'
    '</p>',
    unsafe_allow_html=True
)

st.info(
    "SmilX is developed by a multidisciplinary team of researchers and designers "
    "at CINVESTAV Mérida, working at the intersection of computational chemistry, "
    "cheminformatics, and scientific software development."
)

st.divider()

st.markdown(
    "<p class='footer-wrap'>"
    "Web Designers: Gabriela Yasmin Vidales Ayala &amp; José Emmanuel Soberanis Cáceres"
    "</p>",
    unsafe_allow_html=True
)
