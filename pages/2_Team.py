import streamlit as st
from shared_nav import render_nav

st.set_page_config(page_title="Team | SmilX", layout="wide", initial_sidebar_state="collapsed")
render_nav("Team")

st.title("Team")
st.write("The SmilX / TokenSMILES project is developed by researchers at **Centro de Investigación y Estudios Avanzados (CINVESTAV) Mérida**.")

team = [
    {"name": "Luis Armando Gonzalez-Ortiz", "role": "Developer of SmilX / TokenSMILES",
     "desc": "Researcher focused on computational chemistry, cheminformatics, and grammar-based representations of chemical space.",
     "scholar": "https://scholar.google.com/", "linkedin": "https://linkedin.com/"},
    {"name": "Lisset Noriega", "role": "Researcher",
     "desc": "Computational chemist working on astrochemistry and theoretical exploration of molecular isomers.",
     "scholar": "https://scholar.google.com/", "linkedin": "https://linkedin.com/"},
    {"name": "Filiberto Ortiz-Chi", "role": "Researcher",
     "desc": "Researcher in theoretical chemistry and molecular structure prediction.",
     "scholar": "https://scholar.google.com/", "linkedin": "https://linkedin.com/"},
    {"name": "Gabriela Vidales-Ayala", "role": "Web Designer",
     "desc": "Researcher in computational chemistry and molecular modeling.",
     "scholar": "https://scholar.google.com/", "linkedin": "https://linkedin.com/"},
    {"name": "Emmanuel Soberanis-Cáceres", "role": "Web Designer",
     "desc": "Researcher focused on theoretical and computational chemistry.",
     "scholar": "https://scholar.google.com/", "linkedin": "https://linkedin.com/"},
    {"name": "Miriam Pescador-Rojas", "role": "Researcher",
     "desc": "Researcher in computational chemistry and molecular modeling.",
     "scholar": "https://scholar.google.com/", "linkedin": "https://linkedin.com/"},
    {"name": "Amilcar Meneses-Viveros", "role": "Researcher",
     "desc": "Researcher working on computational chemistry and molecular design.",
     "scholar": "https://scholar.google.com/", "linkedin": "https://linkedin.com/"},
    {"name": "Alan Aspuru-Guzik", "role": "Professor",
     "desc": "Leading researcher in AI-driven chemistry, quantum chemistry, and molecular discovery.",
     "scholar": "https://scholar.google.com/", "linkedin": "https://linkedin.com/"},
    {"name": "Gabriel Merino", "role": "Professor",
     "desc": "Professor of theoretical chemistry specializing in molecular structure and chemical bonding.",
     "scholar": "https://scholar.google.com/", "linkedin": "https://linkedin.com/"},
]

st.divider()

for i in range(0, len(team), 3):
    cols = st.columns(3, gap="medium")
    for col, member in zip(cols, team[i:i+3]):
        with col:
            with st.container(border=True):
                st.subheader(member["name"])
                st.caption(member["role"])
                st.write(member["desc"])
                col_a, col_b = st.columns(2)
                with col_a:
                    st.link_button("Google Scholar", member["scholar"], use_container_width=True)
                with col_b:
                    st.link_button("LinkedIn", member["linkedin"], use_container_width=True)

st.divider()
st.markdown("**Web Designers:** Gabriela Yasmin Vidales Ayala & José Emmanuel Soberanis Cáceres")
