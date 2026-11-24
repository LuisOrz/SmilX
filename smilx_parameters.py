"""
SmilX · input parameters
------------------------
Parses and validates a molecular formula and prepares everything the
TokenSMILES generators need (syntax rules, unsaturation patterns, output
file names). This module has no UI code: the Explore page builds the
interface and calls `parse_formula()` / `initial_parameters` directly.
"""
import os
import re
import tempfile
from dataclasses import dataclass, field

from smilx_chemistry_tools import get_unsaturations, get_hdi

# Elements understood by the TokenSMILES grammar and their valences
SUPPORTED_ELEMENTS = ("C", "H", "N", "O", "S", "P", "B", "F", "Cl", "Br", "I")
VALENCES = {"C": 4, "N": 3, "P": 3, "B": 3, "O": 2, "S": 2,
            "H": 1, "F": 1, "Cl": 1, "Br": 1, "I": 1}

# Heavy-atom counts with precomputed skeletons in dependences/valence_4/
PRECOMPUTED_MAX_HEAVY_ATOMS = 10

_TOKEN = re.compile(r"([A-Z][a-z]?)(\d*)")


@dataclass
class FormulaCheck:
    """Result of parsing a molecular formula (used for live validation)."""
    raw: str
    ok: bool = False
    error: str = ""
    warning: str = ""
    counts: dict = field(default_factory=dict)
    hdi: int | None = None
    n_heavy_atoms: int = 0

    @property
    def pretty(self) -> str:
        """Hill-ordered formula with HTML subscripts."""
        order = ["C", "H"] + sorted(e for e in self.counts if e not in ("C", "H"))
        out = ""
        for e in order:
            n = self.counts.get(e, 0)
            if n:
                out += e + (f"<sub>{n}</sub>" if n > 1 else "")
        return out


def parse_formula(text: str) -> FormulaCheck:
    """Parse and validate a molecular formula such as 'C6H6' or 'C2H5NO2'."""
    raw = (text or "").strip().replace(" ", "")
    chk = FormulaCheck(raw=raw)
    if not raw:
        chk.error = "Enter a molecular formula to begin."
        return chk

    # The whole string must be made of Element+count tokens
    if "".join(m.group(0) for m in _TOKEN.finditer(raw)) != raw:
        chk.error = ("Could not read that formula. Use element symbols with a capital "
                     "first letter, e.g. C6H6 or C2H5NO2.")
        return chk

    counts: dict[str, int] = {}
    for sym, num in _TOKEN.findall(raw):
        if sym not in VALENCES:
            chk.error = (f"Element '{sym}' is not supported. SmilX works with "
                         + ", ".join(SUPPORTED_ELEMENTS) + ".")
            return chk
        counts[sym] = counts.get(sym, 0) + (int(num) if num else 1)

    if any(v == 0 for v in counts.values()):
        chk.error = "Atom counts must be at least 1."
        return chk

    heavy = sum(v for k, v in counts.items() if k != "H")
    if heavy == 0:
        chk.error = "The formula needs at least one heavy (non-hydrogen) atom."
        return chk

    full = {e: counts.get(e, 0) for e in SUPPORTED_ELEMENTS}
    hdi = get_hdi(full)
    chk.counts, chk.n_heavy_atoms = counts, heavy
    if hdi is None:
        chk.error = ("This formula has no valid hydrogen deficiency index "
                     "(odd or negative). Check the number of hydrogens.")
        return chk

    chk.hdi = hdi
    chk.ok = True
    if heavy > PRECOMPUTED_MAX_HEAVY_ATOMS:
        chk.warning = (f"{heavy} heavy atoms: skeletons above "
                       f"{PRECOMPUTED_MAX_HEAVY_ATOMS} are not precomputed, so the "
                       "exploration may take several minutes.")
    return chk


class initial_parameters:
    """Container consumed by chemical_space_classic / chemical_space_carbenes."""

    def __init__(self, str_molecular_formula: str, opt_carbenes: bool = False,
                 workdir: str | None = None):
        chk = parse_formula(str_molecular_formula)
        if not chk.ok:
            raise ValueError(chk.error)

        self.str_molecular_formula = chk.raw
        self.opt_carbenes = bool(opt_carbenes)
        self.is_valid_molecular_formula = True
        self.workdir = workdir or tempfile.mkdtemp(prefix="smilx_")

        self.get_molecular_formula()
        self.count_atoms_from_molecular_formula(self.molecular_formula)
        self.write_name_output_file()
        self.get_syntax_rules()
        self.get_cycles_pi_systems()

    def count_atoms_from_molecular_formula(self, mf):
        self.n_heavy_atoms = sum(v for k, v in mf.items() if k not in {"hdi", "H"})

    def get_molecular_formula(self):
        self.molecular_formula = {}
        for e, n in _TOKEN.findall(self.str_molecular_formula):
            self.molecular_formula[e] = self.molecular_formula.get(e, 0) + (int(n) if n else 1)
        for e in SUPPORTED_ELEMENTS:
            self.molecular_formula.setdefault(e, 0)
        self.molecular_formula["hdi"] = get_hdi(
            {e: self.molecular_formula[e] for e in SUPPORTED_ELEMENTS})
        self.out_fm = [self.molecular_formula[e]
                       for e in ("C", "N", "O", "S", "B", "P", "F", "Cl", "Br", "I")]

    def reorder_molecular_formula(self):
        self.str_molecular_formula = "".join(
            (e if self.molecular_formula[e] == 1 else f"{e}{self.molecular_formula[e]}")
            for e in ("C", "H", "B", "Br", "Cl", "F", "I", "N", "O", "P", "S")
            if self.molecular_formula[e] > 0)

    def write_name_output_file(self):
        lbl = "_with_carbenes" if self.opt_carbenes else ""
        stem = self.str_molecular_formula + lbl
        # Each run writes to its own folder, so simultaneous users never collide
        self.filename_output_pkl = os.path.join(self.workdir, stem + ".pkl")
        self.filename_output_smi = os.path.join(self.workdir, stem + ".smi")
        self.filename_output_xyz = os.path.join(self.workdir, stem + ".xyz")
        self.download_name_smi = stem + ".smi"

    def get_syntax_rules(self):
        n = self.n_heavy_atoms
        if n in {1, 2, 3}:
            self.syntax_rules = [[0]] * n
        elif n in {4, 5, 6}:
            self.syntax_rules = [[0], [0]] + [[0, 1]] * (n - 3) + [[0]]
        elif n == 7:
            self.syntax_rules = [[0], [0], [0, 1], [0, 1, 2], [0, 1, 3], [0, 1], [0]]
        elif n == 8:
            self.syntax_rules = [[0], [0], [0, 1], [0, 1, 2], [0, 1, 2, 3], [0, 1, 3], [0, 1], [0]]
        elif n > 8:
            self.syntax_rules = ([[0], [0], [0, 1], [0, 1, 2], [0, 1, 2, 3]]
                                 + [[0, 1, 2, 3]] * (n - 8) + [[0, 1, 3], [0, 1], [0]])

    def get_cycles_pi_systems(self):
        self.cycles_pi_systems = get_unsaturations(self.molecular_formula, self.n_heavy_atoms)
