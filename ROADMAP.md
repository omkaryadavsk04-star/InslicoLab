# InSilicoLab Company Roadmap

## Mission

Build an affordable AI-assisted in silico drug discovery platform for students, researchers, and small laboratories.

## Phase 1: Learning Prototype

Goal: Understand web apps and molecule input.

Features:

- SMILES input
- simple molecule property display
- compound table
- CSV export

Status: started.

## Phase 2: Real Chemistry Engine

Goal: Replace rough JavaScript calculations with real RDKit calculations.

Status: backend structure created. Conda environment `insilicolab` installed with Python 3.11, RDKit, FastAPI, and Uvicorn.

Features:

- Python FastAPI backend
- RDKit molecular weight
- RDKit LogP
- RDKit HBD and HBA
- RDKit TPSA
- Lipinski rule check

## Phase 3: ADMET Prediction

Goal: Add better drug-likeness and ADMET models.

Features:

- solubility prediction
- toxicity prediction
- BBB/permeability prediction
- CYP risk prediction
- confidence score

## Phase 4: Docking

Goal: Add protein-ligand docking.

Features:

- upload PDB protein
- upload ligand or SMILES
- ligand preparation
- binding box selection
- AutoDock Vina docking
- docking score table
- 3D pose viewer

## Phase 5: AI Discovery Assistant

Goal: Help users make decisions.

Features:

- rank compounds
- suggest analogs
- explain property problems
- generate new molecule ideas
- compare compounds

## Phase 6: Company Product

Goal: Turn the prototype into a real product.

Needed:

- product website
- user accounts
- cloud jobs
- database
- documentation
- pricing
- pilot users
- advisor network
