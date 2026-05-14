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
                f'<div style="'
                f'display:flex;justify-content:center;align-items:center;'
                f'background:linear-gradient(135deg,#0b0f1c 0%,#060912 100%);'
                f'border-radius:16px;padding:2rem 3rem;'
                f'margin:0 auto 1.5rem auto;max-width:560px;'
                f'border:1px solid rgba(99,123,200,0.12);">'
                f'<img src="{uri}" style="width:100%;max-width:340px;height:auto;"/>'
                f'</div>',
                unsafe_allow_html=True)

        st.markdown(
            '<div style="'
            'text-align:center;max-width:700px;margin:0 auto 2rem auto;'
            'padding:1.25rem 1.5rem;border-radius:10px;'
            'border:1px solid rgba(99,123,200,0.10);'
            'background:rgba(11,15,28,0.6);">'

            '<p style="font-family:IBM Plex Mono,monospace;font-size:12px;'
            'font-style:italic;color:rgba(232,237,248,0.55);'
            'letter-spacing:0.02em;margin:0 0 0.6rem 0;line-height:1.6;">'
            '&ldquo;Grammar-Driven SMILES Standardization with TokenSMILES&rdquo;'
            '</p>'

            '<p style="font-family:Outfit,sans-serif;font-size:12px;'
            'color:rgba(232,237,248,0.38);margin:0 0 0.35rem 0;line-height:1.7;">'
            'Gonzalez-Ortiz, Noriega, Ortiz, Vidales-Ayala, Soberanis, '
            'Meneses, Aspuru-Guzik &amp; Merino'
            '</p>'

            '<p style="font-family:IBM Plex Mono,monospace;font-size:10px;'
            'color:rgba(91,138,245,0.45);letter-spacing:0.08em;'
            'text-transform:uppercase;margin:0;">'
            'Centro de Investigación y Estudios Avanzados (Cinvestav) Mérida'
            '</p>'

            '</div>',
            unsafe_allow_html=True)

        self.ask_molecular_formula()
        self.write_name_output_file()
        self.get_syntax_rules()
        self.get_cycles_pi_systems()

    def count_atoms_from_molecular_formula(self, mf):
        self.n_heavy_atoms = sum(v for k,v in mf.items() if k not in {'hdi','H'})

    def ask_molecular_formula(self):
        try:
            self.str_molecular_formula = st.text_input(
                "Molecular formula",
                value="C6H14",
                key="first",
                placeholder="e.g. C6H6, C2H5NO2"
            )
            self.opt_carbenes = st.checkbox("Search with carbenes")
            self.get_molecular_formula()
            self.is_valid_molecular_formula = True
            self.count_atoms_from_molecular_formula(self.molecular_formula)
        except Exception:
            pass

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
