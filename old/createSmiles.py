#!/usr/bin/env python3
"""
Generate N enantiomeric pairs (each pair has exactly 1 chiral center)
and print lines like:
Molecule,R,SMILES
Molecule,S,SMILES

No blank lines between samples. Labels R/S are assigned based on RDKit CIP code.
Requires: RDKit
"""

import random
import sys
from rdkit import Chem
from rdkit.Chem.EnumerateStereoisomers import EnumerateStereoisomers, StereoEnumerationOptions

# ---------- Settings ----------
TARGET_PAIRS = 500  # number of enantiomeric pairs to find
MAX_TRIES = 20000
DUMMY = "Molecule"
random.seed(42)

# ---------- Simple templates (use '*' as placeholder) ----------
# Keep templates simple to avoid complex bracket insertion problems
TEMPLATES = [
    "C(*)C",
    "CC(*)C",
    "C(*)Cl",
    "C(*)F",
    "C(*)Br",
    "C(*)c1ccccc1",
    "C1CC(*)CC1",
    "CC(*)O",
    "C(*)O",
    "C(*)N",
    "C(*)C(=O)O",
    "C(*)C#N",
    "c1cc(*)ccc1",
    "CC(*)C(=O)O",
    "C(*)S",
]

# ---------- Substituents (no square brackets allowed) ----------
# Avoid any substituent that contains '[' or ']' to prevent bracket insertion issues.
SUBSTITUENTS = [
    "C", "CC", "CCC", "CCCC",
    "O", "OC", "CO", "COC",
    "N", "CN", "NC", 
    "Cl", "Br", "F", "I",
    "c1ccccc1", "c1ccncc1",  # phenyl, pyridine-like
    "C#N", "C(=O)O", "C(=O)N",
    "S", "SC", "OCC", "NCC",
    "OC(=O)C", "CCO", "CCN",
]

# ---------- Helpers ----------
def safe_fill(template, substituent):
    """Replace '*' in template with substituent (simple string replace)."""
    if "*" not in template:
        # fallback: append substituent
        return template + substituent
    return template.replace("*", substituent, 1)

def valid_smiles(smi):
    """Return True if RDKit can parse and sanitize the SMILES."""
    try:
        m = Chem.MolFromSmiles(smi)
        return m is not None
    except Exception:
        return False

def enumerate_chiral_pair(smi):
    """
    Enumerate stereoisomers of smi and return a pair of SMILES (r_smi, s_smi)
    where each has exactly one chiral center and they are enantiomers.
    Returns None if criteria not met.
    """
    try:
        mol = Chem.MolFromSmiles(smi)
        if mol is None:
            return None
        opts = StereoEnumerationOptions(onlyUnassigned=True, unique=True)
        isomers = list(EnumerateStereoisomers(mol, options=opts))
        if len(isomers) < 2:
            return None

        # keep those with exactly 1 assigned chiral center
        chiral_iso = []
        for iso in isomers:
            # sanitize and assign stereochem
            Chem.AssignStereochemistry(iso, cleanIt=True, force=True, flagPossibleStereoCenters=True)
            centers = Chem.FindMolChiralCenters(iso, includeUnassigned=False)
            if len(centers) == 1:
                chiral_iso.append(iso)

        # need exactly two distinct stereoisomers with one chiral center
        # remove duplicates by canonical isomeric SMILES
        smi_list = sorted({Chem.MolToSmiles(m, isomericSmiles=True, canonical=True) for m in chiral_iso})
        if len(smi_list) != 2:
            return None

        # determine which SMILES is R and which is S based on CIP at the single chiral atom
        # For each molecule, find the atom with _CIPCode
        labeled = {}
        for s in smi_list:
            m2 = Chem.MolFromSmiles(s)
            Chem.AssignStereochemistry(m2, cleanIt=True, force=True, flagPossibleStereoCenters=True)
            cip_codes = []
            for atom in m2.GetAtoms():
                if atom.HasProp("_CIPCode"):
                    cip_codes.append(atom.GetProp("_CIPCode"))
            # expect exactly one CIP code (R or S); otherwise fail
            if len(cip_codes) != 1:
                return None
            labeled[cip_codes[0]] = s

        # Expect keys 'R' and 'S'
        if ("R" in labeled) and ("S" in labeled):
            return labeled["R"], labeled["S"]
        else:
            return None

    except Exception:
        return None

# ---------- Main loop ----------
pairs = []
tries = 0
while len(pairs) < TARGET_PAIRS and tries < MAX_TRIES:
    tries += 1
    tpl = random.choice(TEMPLATES)
    sub = random.choice(SUBSTITUENTS)

    # ensure substituent safe (no brackets)
    if "[" in sub or "]" in sub:
        continue

    candidate = safe_fill(tpl, sub)

    # quick parse check
    if not valid_smiles(candidate):
        continue

    res = enumerate_chiral_pair(candidate)
    if res is None:
        continue

    # avoid duplicates
    # store canonical tuple (R_smi, S_smi)
    pair = tuple(res)
    if pair in pairs:
        continue

    pairs.append(pair)

# warn if not enough pairs
if len(pairs) < TARGET_PAIRS:
    print(f"Warning: only found {len(pairs)} pairs after {tries} tries", file=sys.stderr)

# Print lines: no blank lines, dummy first column "Molecule"
# Each line format: Molecule,R,SMILES  or  Molecule,S,SMILES
for r_s in pairs:
    r_smi, s_smi = r_s
    print(f"{DUMMY},R,{r_smi}")
    print(f"{DUMMY},S,{s_smi}")

