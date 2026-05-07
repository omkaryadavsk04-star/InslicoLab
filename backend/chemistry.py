"""
Chemistry calculations for InSilicoLab.

Beginner meaning:
- A function is a reusable block of code.
- This file has one main function: analyze_smiles.
- It receives SMILES text and returns molecule properties.
"""

from rdkit import Chem
from rdkit.Chem import Crippen, Descriptors, Lipinski, rdMolDescriptors


def lipinski_status(molecular_weight, logp, hbd, hba):
    """Check Lipinski's rule of five."""
    violations = 0

    if molecular_weight > 500:
        violations += 1
    if logp > 5:
        violations += 1
    if hbd > 5:
        violations += 1
    if hba > 10:
        violations += 1

    if violations == 0:
        return "Pass"
    if violations == 1:
        return "Caution"
    return "Fail"


def analyze_smiles(smiles):
    """
    Convert SMILES into a molecule and calculate real RDKit descriptors.

    If the SMILES is invalid, RDKit cannot build the molecule, so we return an error.
    """
    molecule = Chem.MolFromSmiles(smiles)

    if molecule is None:
        return {
            "ok": False,
            "error": "Invalid SMILES. RDKit could not understand this molecule.",
        }

    molecular_weight = Descriptors.MolWt(molecule)
    exact_mass = Descriptors.ExactMolWt(molecule)
    formula = rdMolDescriptors.CalcMolFormula(molecule)
    logp = Crippen.MolLogP(molecule)
    molar_refractivity = Crippen.MolMR(molecule)
    hbd = Lipinski.NumHDonors(molecule)
    hba = Lipinski.NumHAcceptors(molecule)
    tpsa = rdMolDescriptors.CalcTPSA(molecule)
    rotatable_bonds = Lipinski.NumRotatableBonds(molecule)
    heavy_atoms = Lipinski.HeavyAtomCount(molecule)
    ring_count = Lipinski.RingCount(molecule)
    aromatic_rings = Lipinski.NumAromaticRings(molecule)
    fraction_csp3 = Lipinski.FractionCSP3(molecule)
    formal_charge = Chem.GetFormalCharge(molecule)

    return {
        "ok": True,
        "smiles": smiles,
        "formula": formula,
        "molecular_weight": round(molecular_weight, 2),
        "exact_mass": round(exact_mass, 4),
        "logp": round(logp, 2),
        "molar_refractivity": round(molar_refractivity, 2),
        "hbd": hbd,
        "hba": hba,
        "tpsa": round(tpsa, 2),
        "rotatable_bonds": rotatable_bonds,
        "heavy_atoms": heavy_atoms,
        "ring_count": ring_count,
        "aromatic_rings": aromatic_rings,
        "fraction_csp3": round(fraction_csp3, 2),
        "formal_charge": formal_charge,
        "lipinski": lipinski_status(molecular_weight, logp, hbd, hba),
    }
