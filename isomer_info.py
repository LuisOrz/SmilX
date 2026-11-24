"""
Isomer information for the zoom panel
-------------------------------------
Everything here is computed deterministically with RDKit from the SMILES that
SmilX generates; nothing is looked up or guessed. Known-compound data (name,
CID) is fetched separately in the browser from PubChem by InChIKey.
"""
from rdkit import Chem, RDLogger
from rdkit.Chem import Crippen, Descriptors, Lipinski, rdMolDescriptors
from rdkit.Chem.EnumerateStereoisomers import EnumerateStereoisomers, StereoEnumerationOptions

RDLogger.DisableLog("rdApp.*")

# Curated SMARTS (Daylight conventions). Order = display order.
FUNCTIONAL_GROUPS = [
    ("Carboxylic acid", "[CX3](=O)[OX2H1]"),
    ("Acyl halide",     "[CX3](=O)[F,Cl,Br,I]"),
    ("Ester",           "[#6][CX3](=O)[OX2H0][#6]"),
    ("Amide",           "[NX3][CX3](=[OX1])"),
    ("Aldehyde",        "[$([CX3H1](=O)[#6]),$([CX3H2]=O)]"),
    ("Ketone",          "[#6][CX3](=O)[#6]"),
    ("Ketene",          "[CX3]=[CX2]=[OX1]"),
    ("Alcohol",         "[OX2H][CX4]"),
    ("Enol",            "[OX2H][CX3]=[CX3]"),
    ("Peroxide (O–O)",  "[OX2][OX2]"),
    ("Epoxide",         "[OX2r3]1[#6r3][#6r3]1"),
    ("Ether",           "[OX2H0]([#6;!$([CX3]=[O,S,N])])[#6;!$([CX3]=[O,S,N])]"),
    ("Primary amine",   "[NX3;H2;!$(N[CX3]=[O,S,N])][#6]"),
    ("Secondary amine", "[NX3;H1;!$(N[CX3]=[O,S,N])]([#6])[#6]"),
    ("Tertiary amine",  "[NX3;H0;!$(N[CX3]=[O,S,N])]([#6])([#6])[#6]"),
    ("Imine",           "[CX3]=[NX2]"),
    ("Nitrile",         "[NX1]#[CX2]"),
    ("Azo (N=N)",       "[NX2]=[NX2]"),
    ("Hydrazine (N–N)", "[NX3][NX3]"),
    ("N–O bond",        "[#7]-[#8]"),
    ("Thiol",           "[SX2H]"),
    ("Sulfide",         "[SX2H0]([#6])[#6]"),
    ("Disulfide",       "[SX2][SX2]"),
    ("Thiocarbonyl",    "[CX3]=[SX1]"),
    ("Alkene (C=C)",    "[CX3]=[CX3]"),
    ("Alkyne (C≡C)",    "[CX2]#[CX2]"),
    ("Cumulated double bonds", "[*]=[X2]=[*]"),
    ("Alkyl halide",    "[CX4][F,Cl,Br,I]"),
    ("Vinyl halide",    "[CX3]([F,Cl,Br,I])=[CX3]"),
    ("Phosphine",       "[PX3]"),
    ("Borane",          "[BX3]"),
]
_FG = [(name, Chem.MolFromSmarts(sma)) for name, sma in FUNCTIONAL_GROUPS]
_ACYCLIC_ETHER = Chem.MolFromSmarts("[OX2H0;!r3]([#6;!$([CX3]=[O,S,N])])[#6;!$([CX3]=[O,S,N])]")
_STEREO_OPTS = StereoEnumerationOptions(unique=True, onlyUnassigned=True, maxIsomers=512)


def _r(x, n=2):
    return round(float(x), n)


def describe(smiles: str) -> dict | None:
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    ri = mol.GetRingInfo()
    ring_sizes = sorted(len(r) for r in ri.AtomRings())
    bonds = {"double": 0, "triple": 0}
    for b in mol.GetBonds():
        if b.GetBondType() == Chem.BondType.DOUBLE:
            bonds["double"] += 1
        elif b.GetBondType() == Chem.BondType.TRIPLE:
            bonds["triple"] += 1

    groups = [name for name, patt in _FG if patt is not None and mol.HasSubstructMatch(patt)]
    if "Epoxide" in groups and "Ether" in groups and not mol.HasSubstructMatch(_ACYCLIC_ETHER):
        groups.remove("Ether")
    carbenes = sum(1 for a in mol.GetAtoms()
                   if a.GetSymbol() == "C" and a.GetNumRadicalElectrons() == 2)
    if carbenes:
        groups.insert(0, "Carbene (divalent C)")

    # Stereochemistry: SmilX enumerates constitutional isomers without stereo labels
    centers = Chem.FindMolChiralCenters(mol, includeUnassigned=True, useLegacyImplementation=False)
    stereo_db = sum(1 for si in Chem.FindPotentialStereo(mol)
                    if si.type == Chem.StereoType.Bond_Double)
    try:
        n_stereo = len(list(EnumerateStereoisomers(mol, options=_STEREO_OPTS)))
    except Exception:
        n_stereo = None

    flags = []
    if any(s in (3, 4) for s in ring_sizes):
        flags.append("Small ring (3- or 4-membered): strained")
    if any(s <= 7 for s in ring_sizes) and mol.HasSubstructMatch(Chem.MolFromSmarts("[R]#[R]")):
        flags.append("Triple bond inside a ring of ≤ 7 atoms")
    if mol.HasSubstructMatch(Chem.MolFromSmarts("[R]=[R;X2]=[R]")):
        flags.append("Cumulated double bonds inside a ring")

    try:
        inchi = Chem.MolToInchi(mol)
        inchikey = Chem.InchiToInchiKey(inchi) if inchi else ""
    except Exception:
        inchi, inchikey = "", ""

    return {
        "smiles": Chem.MolToSmiles(mol),
        "formula": rdMolDescriptors.CalcMolFormula(mol),
        "inchi": inchi,
        "inchikey": inchikey,
        "mw": _r(Descriptors.MolWt(mol)),
        "exact_mass": _r(Descriptors.ExactMolWt(mol), 4),
        "rings": len(ring_sizes),
        "ring_sizes": ring_sizes,
        "double_bonds": bonds["double"],
        "triple_bonds": bonds["triple"],
        "stereocenters": len(centers),
        "stereo_double_bonds": stereo_db,
        "stereoisomers": n_stereo,
        "hbd": Lipinski.NumHDonors(mol),
        "hba": Lipinski.NumHAcceptors(mol),
        "rot_bonds": Lipinski.NumRotatableBonds(mol),
        "tpsa": _r(rdMolDescriptors.CalcTPSA(mol)),
        "logp": _r(Crippen.MolLogP(mol)),
        "fsp3": _r(rdMolDescriptors.CalcFractionCSP3(mol)),
        "groups": groups,
        "flags": flags,
    }


def describe_all(smiles_list: list[str]) -> dict:
    """{ID (1-based, as shown in the grid): info}"""
    return {i + 1: describe(s) for i, s in enumerate(smiles_list)}
