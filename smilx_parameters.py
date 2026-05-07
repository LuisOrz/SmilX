import re, base64, os
from smilx_chemistry_tools import get_unsaturations, get_hdi
import streamlit as st

def _logo_b64(filename):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    for name in [filename, "logo_smilx_fixed.png", "logo_smilx.png"]:
        path = os.path.join(base_dir, name)
        if os.path.isfile(path):
            with open(path, "rb") as f:
                return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
    return ""

class initial_parameters:
    def __init__(self):
        uri = _logo_b64("logo_smilx_dark.png")
        if uri:
            st.markdown(
                f'<div style="display:flex;justify-content:center;background:#000;'
                f'border-radius:14px;padding:2.5rem 3rem;margin:0 auto 2rem auto;'
                f'max-width:640px;border:1px solid rgba(255,255,255,0.07);">'
                f'<img src="{uri}" style="width:100%;max-width:400px;height:auto;"/></div>',
                unsafe_allow_html=True)
        st.markdown(
            '<div style="text-align:center;font-family:DM Sans,sans-serif;font-size:13.5px;'
            'line-height:1.8;color:rgba(240,242,241,0.65);max-width:760px;margin:0 auto 2rem auto;">'
            '<em>"Grammar-Driven SMILES Standardization with TokenSMILES"</em><br>'
            'Luis Armando Gonzalez-Ortiz, Lisset Noriega, Filiberto Ortiz, '
            'Gabriela Vidales-Ayala, Emmanuel Soberanis, Amilcar Meneses, '
            'Alan Aspuru-Guzik &amp; Gabriel Merino<br>'
            '<span style="opacity:0.5;">Centro de Investigación y Estudios Avanzados (Cinvestav) Mérida</span><br>'
            '<span style="opacity:0.4;font-size:12px;">GNU General Public License v3 · Copyright © 2007 Free Software Foundation</span>'
            '</div>', unsafe_allow_html=True)
        self.ask_molecular_formula()
        self.write_name_output_file()
        self.get_syntax_rules()
        self.get_cycles_pi_systems()

    def count_atoms_from_molecular_formula(self, mf):
        self.n_heavy_atoms = sum(v for k,v in mf.items() if k not in {'hdi','H'})

    def ask_molecular_formula(self):
        try:
            self.str_molecular_formula = st.text_input("Molecular formula", value="C6H14", key="first", placeholder="e.g. C6H6, C2H5NO2")
            self.opt_carbenes = st.checkbox("Search with carbenes")
            self.get_molecular_formula()
            self.is_valid_molecular_formula = True
            self.count_atoms_from_molecular_formula(self.molecular_formula)
        except Exception: pass

    def get_molecular_formula(self):
        elems = re.findall(r'([A-Z][a-z]*)(\d*)', self.str_molecular_formula)
        if elems:
            self.molecular_formula = {e: (1 if n=='' else int(n)) for e,n in elems}
            for e in 'C','H','N','O','S','B','P','F','Cl','Br','I':
                self.molecular_formula.setdefault(e, 0)
            self.molecular_formula['hdi'] = get_hdi(self.molecular_formula)
        else:
            self.molecular_formula = None
        self.out_fm = [self.molecular_formula[e] for e in ('C','N','O','S','B','P','F','Cl','Br','I')]

    def reorder_molecular_formula(self):
        self.str_molecular_formula = ''.join(
            (e if self.molecular_formula[e]==1 else f'{e}{self.molecular_formula[e]}')
            for e in ('C','H','B','Br','Cl','F','I','N','O','P','S')
            if self.molecular_formula[e] > 0)

    def write_name_output_file(self):
        lbl = "_with_carbenes" if self.opt_carbenes else ""
        self.filename_output_pkl = self.str_molecular_formula + lbl + '.pkl'
        self.filename_output_smi = self.str_molecular_formula + lbl + '.smi'
        self.filename_output_xyz = self.str_molecular_formula + lbl + '.xyz'

    def get_syntax_rules(self):
        n = self.n_heavy_atoms
        if n in {1,2,3}: self.syntax_rules = [[0]]*n
        elif n in {4,5,6}: self.syntax_rules = [[0],[0]]+[[0,1]]*(n-3)+[[0]]
        elif n==7: self.syntax_rules = [[0],[0],[0,1],[0,1,2],[0,1,3],[0,1],[0]]
        elif n==8: self.syntax_rules = [[0],[0],[0,1],[0,1,2],[0,1,2,3],[0,1,3],[0,1],[0]]
        elif n>8: self.syntax_rules = [[0],[0],[0,1],[0,1,2],[0,1,2,3]]+[[0,1,2,3]]*(n-8)+[[0,1,3],[0,1],[0]]

    def get_cycles_pi_systems(self):
        self.cycles_pi_systems = get_unsaturations(self.molecular_formula, self.n_heavy_atoms)
