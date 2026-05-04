import re
import base64
import os
from smilx_chemistry_tools import get_unsaturations, get_hdi
import streamlit as st


def _get_logo_base64(filename: str) -> str:
    """Load a PNG logo from the same directory as this file and return base64 data-URI.
    Falls back through logo_smilx_fixed.png → logo_smilx.png if the requested file
    does not exist (avoids Streamlit Cloud MediaFileStorageError).
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [filename, "logo_smilx_fixed.png", "logo_smilx.png"]
    for name in candidates:
        path = os.path.join(base_dir, name)
        if os.path.isfile(path):
            with open(path, "rb") as f:
                data = base64.b64encode(f.read()).decode()
            return f"data:image/png;base64,{data}"
    return ""


class initial_parameters:
# ─────────────────────────────────────────────── Section 0 – Header
    def __init__(self):

        # ── Logo block: black background, proportional, centred ──────────────
        logo_uri = _get_logo_base64("logo_smilx_dark.png")
        if logo_uri:
            st.markdown(
                f"""
                <div style="
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    background: #000000;
                    border-radius: 14px;
                    padding: 2.5rem 3rem;
                    margin: 0 auto 2rem auto;
                    max-width: 640px;
                    border: 1px solid rgba(255,255,255,0.07);
                ">
                    <img src="{logo_uri}"
                         style="width:100%;max-width:400px;height:auto;display:block;" />
                </div>
                """,
                unsafe_allow_html=True,
            )

        # ── Citation / meta text ─────────────────────────────────────────────
        st.markdown(
            """
            <div style="
                text-align: center;
                font-family: 'DM Sans', sans-serif;
                font-size: 13.5px;
                line-height: 1.8;
                color: rgba(240,242,241,0.65);
                max-width: 760px;
                margin: 0 auto 2rem auto;
            ">
              <em>"Grammar-Driven SMILES Standardization with TokenSMILES"</em><br>
              Luis Armando Gonzalez-Ortiz, Lisset Noriega, Filiberto Ortiz,
              Gabriela Vidales-Ayala, Emmanuel Soberanis, Amilcar Meneses,
              Alan Aspuru-Guzik &amp; Gabriel Merino<br>
              <span style="opacity:0.5;">Centro de Investigación y Estudios Avanzados (Cinvestav) Mérida</span><br>
              <span style="opacity:0.4;font-size:12px;">
                GNU General Public License v3 &nbsp;·&nbsp; Copyright © 2007 Free Software Foundation
              </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        self.ask_molecular_formula()
        self.write_name_output_file()
        self.get_syntax_rules()
        self.get_cycles_pi_systems()

# ─────────────────────────────────────────────── Section 1 – Formula parsing
    def count_atoms_from_molecular_formula(self, molecular_formula):
        self.n_heavy_atoms = 0
        for element, atoms in zip(molecular_formula.keys(), molecular_formula.values()):
            if element not in {'hdi', 'H'}:
                self.n_heavy_atoms += atoms

    def ask_molecular_formula(self):
        try:
            self.str_molecular_formula = st.text_input(
                "Molecular formula",
                value="C6H14",
                key="first",
                placeholder="e.g. C6H6, C2H5NO2",
            )
            self.opt_carbenes = st.checkbox("Search with carbenes")
            self.get_molecular_formula()
            self.is_valid_molecular_formula = True
            self.count_atoms_from_molecular_formula(self.molecular_formula)
        except Exception:
            pass

    def get_molecular_formula(self):
        elements_y_atoms = re.findall(r'([A-Z][a-z]*)(\d*)', self.str_molecular_formula)
        if elements_y_atoms:
            self.molecular_formula = {}
            for i_tuple in elements_y_atoms:
                if i_tuple[1] == '':
                    self.molecular_formula[i_tuple[0]] = 1
                else:
                    self.molecular_formula[i_tuple[0]] = int(i_tuple[1])
            for i_element in 'C', 'H', 'N', 'O', 'S', 'B', 'P', 'F', 'Cl', 'Br', 'I':
                if i_element not in self.molecular_formula:
                    self.molecular_formula[i_element] = 0
            self.molecular_formula['hdi'] = get_hdi(self.molecular_formula)
        else:
            self.molecular_formula = None

        self.out_fm = []
        for i_element in 'C', 'N', 'O', 'S', 'B', 'P', 'F', 'Cl', 'Br', 'I':
            self.out_fm.append(self.molecular_formula[i_element])

    def reorder_molecular_formula(self):
        self.str_molecular_formula = ''
        for i_element in 'C', 'H', 'B', 'Br', 'Cl', 'F', 'I', 'N', 'O', 'P', 'S':
            if self.molecular_formula[i_element] > 0:
                if self.molecular_formula[i_element] == 1:
                    self.str_molecular_formula += f'{i_element}'
                else:
                    self.str_molecular_formula += f'{i_element}{self.molecular_formula[i_element]}'

# ─────────────────────────────────────────────── Section 2 – File names
    def write_name_output_file(self):
        label_carbenes = "_with_carbenes" if self.opt_carbenes else ""
        self.filename_output_pkl = self.str_molecular_formula + label_carbenes + '.pkl'
        self.filename_output_smi = self.str_molecular_formula + label_carbenes + '.smi'
        self.filename_output_xyz = self.str_molecular_formula + label_carbenes + '.xyz'

# ─────────────────────────────────────────────── Section 3 – Syntax rules
    def get_syntax_rules(self):
        n = self.n_heavy_atoms
        if n in {1, 2, 3}:
            self.syntax_rules = [[0] for _ in range(n)]
        elif n in {4, 5, 6}:
            self.syntax_rules = [[0], [0]] + [[0, 1] for _ in range(n - 3)] + [[0]]
        elif n == 7:
            self.syntax_rules = [[0], [0], [0, 1], [0, 1, 2], [0, 1, 3], [0, 1], [0]]
        elif n == 8:
            self.syntax_rules = [[0], [0], [0, 1], [0, 1, 2], [0, 1, 2, 3], [0, 1, 3], [0, 1], [0]]
        elif n > 8:
            self.syntax_rules = [[0], [0], [0, 1], [0, 1, 2], [0, 1, 2, 3]]
            self.syntax_rules += [[0, 1, 2, 3] for _ in range(n - 8)]
            self.syntax_rules += [[0, 1, 3], [0, 1], [0]]

# ─────────────────────────────────────────────── Section 4 – Cycles / pi systems
    def get_cycles_pi_systems(self):
        self.cycles_pi_systems = get_unsaturations(self.molecular_formula, self.n_heavy_atoms)
