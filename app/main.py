from __future__ import annotations

import html
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

try:
    from rdkit import Chem
    from rdkit.Chem import Crippen, Descriptors, Draw, Lipinski, rdMolDescriptors
except Exception:  # pragma: no cover - fallback keeps the prototype usable without RDKit.
    Chem = None
    Crippen = None
    Descriptors = None
    Draw = None
    Lipinski = None
    rdMolDescriptors = None


ROOT = Path(__file__).resolve().parent.parent
STATIC_DIR = ROOT / "static"

app = FastAPI(title="InSilicoLab Chemistry API", version="0.1.0")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class MoleculeRequest(BaseModel):
    """Data shape expected from the browser."""

    smiles: str


@app.get("/api")
def home() -> dict[str, str]:
    return {"name": "InSilicoLab Chemistry API", "status": "running"}


@app.get("/health")
def health() -> dict[str, bool]:
    return {"ok": True}


@app.get("/")
def website() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/styles.css")
def styles() -> FileResponse:
    return FileResponse(STATIC_DIR / "styles.css")


@app.get("/app.js")
def script() -> FileResponse:
    return FileResponse(STATIC_DIR / "app.js")


@app.get("/insilicolab")
def insilicolab_page() -> FileResponse:
    return FileResponse(STATIC_DIR / "insilicolab.html")


@app.get("/insilicolab.css")
def insilicolab_styles() -> FileResponse:
    return FileResponse(STATIC_DIR / "insilicolab.css")


@app.get("/insilicolab.js")
def insilicolab_script() -> FileResponse:
    return FileResponse(STATIC_DIR / "insilicolab.js")


@app.get("/manuscripta")
def manuscripta_page() -> FileResponse:
    return FileResponse(STATIC_DIR / "manuscripta.html")


@app.get("/upcoming")
def upcoming_page() -> FileResponse:
    return FileResponse(STATIC_DIR / "upcoming.html")


@app.get("/privacy")
def privacy_page() -> FileResponse:
    return FileResponse(STATIC_DIR / "privacy.html")


@app.get("/terms")
def terms_page() -> FileResponse:
    return FileResponse(STATIC_DIR / "terms.html")


def lipinski_label(mw: float, logp: float, hbd: int, hba: int) -> str:
    violations = sum([mw > 500, logp > 5, hbd > 5, hba > 10])
    if violations == 0:
        return "Pass"
    if violations == 1:
        return "Caution"
    return "Fail"


def band(value: float, good_max: float, moderate_max: float) -> str:
    if value <= good_max:
        return "Good"
    if value <= moderate_max:
        return "Moderate"
    return "Risk"


def build_interpretation(result: dict[str, Any]) -> dict[str, Any]:
    size = band(result["molecular_weight"], 500, 650)
    lipophilicity = band(result["logp"], 5, 6.5)
    polarity = "Good" if 20 <= result["tpsa"] <= 130 else "Moderate" if result["tpsa"] <= 160 else "Risk"
    flexibility = band(result["rotatable_bonds"], 8, 12)
    h_bonding = "Good" if result["hbd"] <= 5 and result["hba"] <= 10 else "Risk"
    shape = "Good" if result["fraction_csp3"] >= 0.25 else "Risk"

    risks = [size, lipophilicity, polarity, flexibility, h_bonding, shape].count("Risk")
    overall = "Strong" if result["lipinski"] == "Pass" and risks <= 1 else "Moderate" if risks <= 2 else "Weak"

    suggestions: list[str] = []
    if result["molecular_weight"] > 500:
        suggestions.append("Consider trimming molecular size to improve oral drug-likeness.")
    if result["logp"] > 5:
        suggestions.append("High lipophilicity may affect solubility and off-target binding.")
    if result["tpsa"] > 130:
        suggestions.append("High polarity may reduce passive membrane permeability.")
    if result["rotatable_bonds"] > 10:
        suggestions.append("High flexibility can reduce binding efficiency and oral exposure.")
    if not suggestions:
        suggestions.append("Move this compound to ADMET prediction or docking for deeper evaluation.")

    return {
        "overall": overall,
        "summary": f"This molecule has a {overall.lower()} oral drug-likeness profile by basic descriptor rules.",
        "size": size,
        "lipophilicity": lipophilicity,
        "polarity": polarity,
        "flexibility": flexibility,
        "h_bonding": h_bonding,
        "shape": shape,
        "suggestions": suggestions,
    }


def build_admet(result: dict[str, Any]) -> dict[str, Any]:
    solubility = "Good" if result["logp"] <= 3 and result["molecular_weight"] <= 450 else "Moderate" if result["logp"] <= 5 else "Low"
    gi = "High" if result["tpsa"] <= 130 and result["molecular_weight"] <= 500 else "Moderate"
    bbb = "Likely" if result["tpsa"] < 90 and result["logp"] <= 4 and result["formal_charge"] == 0 else "Unlikely"
    permeability = "Good" if result["tpsa"] <= 130 and result["rotatable_bonds"] <= 10 else "Limited"
    cyp_risk = "Elevated" if result["logp"] > 4 or result["aromatic_rings"] >= 3 else "Low"
    toxicity_flag = "Review" if result["formal_charge"] != 0 or result["logp"] > 5.5 else "Low"

    notes = []
    if bbb == "Likely":
        notes.append("Low polarity and neutral charge suggest possible CNS penetration.")
    if cyp_risk == "Elevated":
        notes.append("Lipophilicity or aromaticity suggests CYP interaction risk worth testing.")
    if toxicity_flag == "Review":
        notes.append("Flagged for medicinal chemistry review before prioritization.")
    if not notes:
        notes.append("No major rule-based ADMET concern detected in this first-pass screen.")

    return {
        "solubility": solubility,
        "gi_absorption": gi,
        "bbb": bbb,
        "permeability": permeability,
        "cyp_risk": cyp_risk,
        "toxicity_flag": toxicity_flag,
        "notes": notes,
    }


def analyze_with_rdkit(smiles: str) -> dict[str, Any]:
    if Chem is None:
        raise RuntimeError("RDKit is not installed")

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise HTTPException(status_code=400, detail="Invalid SMILES string")

    mw = round(Descriptors.MolWt(mol), 2)
    logp = round(Crippen.MolLogP(mol), 2)
    hbd = int(Lipinski.NumHDonors(mol))
    hba = int(Lipinski.NumHAcceptors(mol))
    result: dict[str, Any] = {
        "ok": True,
        "smiles": smiles,
        "formula": rdMolDescriptors.CalcMolFormula(mol),
        "molecular_weight": mw,
        "exact_mass": round(Descriptors.ExactMolWt(mol), 4),
        "logp": logp,
        "molar_refractivity": round(Crippen.MolMR(mol), 2),
        "hbd": hbd,
        "hba": hba,
        "tpsa": round(rdMolDescriptors.CalcTPSA(mol), 2),
        "rotatable_bonds": int(Lipinski.NumRotatableBonds(mol)),
        "heavy_atoms": int(mol.GetNumHeavyAtoms()),
        "ring_count": int(rdMolDescriptors.CalcNumRings(mol)),
        "aromatic_rings": int(rdMolDescriptors.CalcNumAromaticRings(mol)),
        "fraction_csp3": round(rdMolDescriptors.CalcFractionCSP3(mol), 2),
        "formal_charge": int(sum(atom.GetFormalCharge() for atom in mol.GetAtoms())),
        "lipinski": lipinski_label(mw, logp, hbd, hba),
    }
    result["interpretation"] = build_interpretation(result)
    result["admet"] = build_admet(result)
    return result


@app.post("/api/analyze")
@app.post("/analyze")
def analyze_api(payload: MoleculeRequest) -> dict[str, Any]:
    smiles = payload.smiles.strip()
    if not smiles:
        raise HTTPException(status_code=400, detail="SMILES is required")
    return analyze_with_rdkit(smiles)


@app.get("/api/structure.svg")
def structure_svg(smiles: str = Query(...)) -> Response:
    if Chem is None or Draw is None:
        safe = html.escape(smiles[:80])
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="420" height="260" viewBox="0 0 420 260">
<rect width="420" height="260" fill="#f7fbf9"/>
<text x="210" y="120" text-anchor="middle" font-family="Segoe UI, sans-serif" font-size="16" fill="#60706a">RDKit unavailable</text>
<text x="210" y="150" text-anchor="middle" font-family="Consolas, monospace" font-size="13" fill="#17201d">{safe}</text>
</svg>"""
        return Response(svg, media_type="image/svg+xml")

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise HTTPException(status_code=400, detail="Invalid SMILES string")

    drawer = Draw.MolDraw2DSVG(420, 260)
    drawer.DrawMolecule(mol)
    drawer.FinishDrawing()
    return Response(drawer.GetDrawingText(), media_type="image/svg+xml")
