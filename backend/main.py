"""
InSilicoLab backend API.

Beginner meaning:
- FastAPI creates a small web server.
- The browser can send molecule data to this server.
- The server sends back calculated chemistry results.
"""

from pathlib import Path

from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from chemistry import analyze_smiles, smiles_to_svg


app = FastAPI(title="InSilicoLab Chemistry API")
PROJECT_ROOT = Path(__file__).resolve().parent.parent

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MoleculeRequest(BaseModel):
    """Data shape expected from the browser."""

    smiles: str


@app.get("/api")
def home():
    return {
        "name": "InSilicoLab Chemistry API",
        "status": "running",
    }


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/api/analyze")
def analyze_api(request: MoleculeRequest):
    return analyze_smiles(request.smiles)


@app.post("/analyze")
def analyze(request: MoleculeRequest):
    return analyze_smiles(request.smiles)


@app.get("/api/structure.svg")
def structure_svg(smiles: str):
    svg = smiles_to_svg(smiles)
    if svg is None:
        raise HTTPException(status_code=400, detail="Invalid SMILES")
    return Response(content=svg, media_type="image/svg+xml")


@app.get("/")
def website():
    return FileResponse(PROJECT_ROOT / "index.html")


app.mount("/", StaticFiles(directory=PROJECT_ROOT, html=True), name="frontend")
