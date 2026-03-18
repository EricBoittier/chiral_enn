import numpy as np
from dscribe.descriptors import SOAP
import ase

# ------------------------------
# Load your data
# ------------------------------
data = np.load("chiral_structures.npz", allow_pickle=True)
R_list = data["R"]          # list of coordinates arrays (N_atoms x 3)
Z_list = data["Z"]          # list of atomic numbers arrays
handedness = data["handedness"]  # list of "R"/"S"

# ------------------------------
# Prepare species list (all unique elements)
# ------------------------------
unique_species = sorted({z for Z in Z_list for z in Z})
print("Species in dataset:", unique_species)

# ------------------------------
# Build SOAP object
# ------------------------------
soap = SOAP(
    species=unique_species,  # list of atomic numbers
    periodic=False,
    r_cut=5.0,      # cutoff radius in angstroms
    n_max=8,        # number of radial basis functions
    l_max=6,        # maximum degree of spherical harmonics
    sigma=0.5,     # Gaussian smearing width
    average="inner"   # average over all atomic centers to get one vector per molecule
)

# ------------------------------
# Compute SOAP descriptors for each molecule
# ------------------------------
descriptors = []
for R, Z in zip(R_list, Z_list):
    atoms_obj = ase.Atoms(Z,R)
    # DScribe expects atomic numbers as int array, positions as float array
    desc = soap.create(atoms_obj)  # returns 1D vector if average=True
    descriptors.append(desc)

descriptors = np.array(descriptors)  # shape: (N_molecules, descriptor_length)
print("Descriptor array shape:", descriptors.shape)

# ------------------------------
# Save descriptors + labels
# ------------------------------
np.savez("soap_descriptors.npz", X=descriptors, y=handedness)
print("SOAP descriptors saved to soap_descriptors.npz")

