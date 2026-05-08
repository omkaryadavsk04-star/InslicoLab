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
        "interpretation": interpret_drug_likeness(
            molecular_weight,
            logp,
            hbd,
            hba,
            tpsa,
            rotatable_bonds,
            ring_count,
            fraction_csp3,
        ),
    }


def classify(value, good_limit, caution_limit, higher_is_worse=True):
    """Return Good, Moderate, or Risk based on simple medicinal chemistry limits."""
    if higher_is_worse:
        if value <= good_limit:
            return "Good"
        if value <= caution_limit:
            return "Moderate"
        return "Risk"

    if value >= good_limit:
        return "Good"
    if value >= caution_limit:
        return "Moderate"
    return "Risk"


def interpret_drug_likeness(molecular_weight, logp, hbd, hba, tpsa, rotatable_bonds, ring_count, fraction_csp3):
    """
    Create a simple explanation for students and early researchers.

    This is not a clinical or regulatory ADMET prediction. It is a rule-based guide.
    """
    size = classify(molecular_weight, 450, 500)
    lipophilicity = classify(logp, 3.5, 5)
    polarity = classify(tpsa, 90, 140)
    flexibility = classify(rotatable_bonds, 7, 10)
    h_bonding = "Good" if hbd <= 3 and hba <= 7 else "Moderate" if hbd <= 5 and hba <= 10 else "Risk"
    shape = classify(fraction_csp3, 0.35, 0.15, higher_is_worse=False)

    risk_count = [size, lipophilicity, polarity, flexibility, h_bonding].count("Risk")
    moderate_count = [size, lipophilicity, polarity, flexibility, h_bonding].count("Moderate")

    if risk_count == 0 and moderate_count <= 1:
        overall = "Strong"
        summary = "This molecule has a strong oral drug-likeness profile by basic descriptor rules."
    elif risk_count <= 1:
        overall = "Moderate"
        summary = "This molecule has a usable profile, but one or more properties may need optimization."
    else:
        overall = "Weak"
        summary = "This molecule has multiple descriptor risks for oral drug-likeness."

    suggestions = []
    if molecular_weight > 500:
        suggestions.append("Reduce molecular size if oral exposure is the goal.")
    if logp > 5:
        suggestions.append("Reduce lipophilicity to lower solubility and promiscuity risk.")
    if tpsa > 140:
        suggestions.append("Reduce polarity to improve passive permeability.")
    if rotatable_bonds > 10:
        suggestions.append("Reduce flexibility to improve permeability and binding efficiency.")
    if hbd > 5 or hba > 10:
        suggestions.append("Reduce hydrogen bonding load for better oral drug-likeness.")
    if ring_count == 0:
        suggestions.append("Consider whether adding a ring could improve shape and binding selectivity.")

    if not suggestions:
        suggestions.append("Move this compound to ADMET prediction or docking for deeper evaluation.")

    return {
        "overall": overall,
        "summary": summary,
        "size": size,
        "lipophilicity": lipophilicity,
        "polarity": polarity,
        "flexibility": flexibility,
        "h_bonding": h_bonding,
        "shape": shape,
        "suggestions": suggestions,
    }
