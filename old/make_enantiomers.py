from rdkit import Chem
from rdkit.Chem import AllChem

def smiles_to_3d(smiles, max_iters=200):
    # Convert SMILES to RDKit molecule
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError("Invalid SMILES string.")

    # Add hydrogens
    mol = Chem.AddHs(mol)

    # Generate 3D coordinates
    params = AllChem.ETKDGv3()   # Good balance of speed + quality
    AllChem.EmbedMolecule(mol, params)

    # Optimize geometry using UFF
    AllChem.UFFOptimizeMolecule(mol, maxIters=max_iters)

    return mol


import pandas as pd
import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem

# -------------------------------------------------------------
# 3D generation helper
# -------------------------------------------------------------
def smiles_to_3d(smiles, max_iter=200):
    mol = Chem.MolFromSmiles(smiles)
    mol = Chem.AddHs(mol)

    # Embed 3D structure
    params = AllChem.ETKDGv3()
    AllChem.EmbedMolecule(mol, params)

    # Geometry optimization (UFF)
    AllChem.UFFOptimizeMolecule(mol, maxIters=max_iter)

    # Extract coords + atomic numbers
    conf = mol.GetConformer()
    coords = conf.GetPositions()
    Z = [atom.GetAtomicNum() for atom in mol.GetAtoms()]

    return np.array(coords, dtype=float), np.array(Z, dtype=int)


# -------------------------------------------------------------
# Main script
# -------------------------------------------------------------
def generate_npz(csv_path="chiral_smiles.csv", out_path="chiral_structures.npz"):
    df = pd.read_csv(csv_path)

    R_list = []
    Z_list = []
    handedness_list = []
    smiles_list = []

    for _, row in df.iterrows():
        smiles = row["SMILES"]
        hand = row["Isomer"]  # R or S
        try:
            coords, Z = smiles_to_3d(smiles)
        except Exception as e:
            print(e)
            break
        R_list.append(coords)
        Z_list.append(Z)
        handedness_list.append(hand)
        smiles_list.append(smiles)

    # Convert to object arrays (variable-size molecules)
    R_arr = np.array(R_list, dtype=object)
    Z_arr = np.array(Z_list, dtype=object)
    H_arr = np.array(handedness_list, dtype=object)
    Smiles_arr = np.array(smiles_list, dtype=object)
    # Save
    np.savez(out_path, R=R_arr, Z=Z_arr, handedness=H_arr, smile=Smiles_arr)
    print(f"Saved: {out_path}")


# -------------------------------------------------------------
# Run
# -------------------------------------------------------------
if __name__ == "__main__":
    generate_npz()

