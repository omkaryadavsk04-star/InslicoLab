# Backend: Real Chemistry Engine

This folder is the hidden engine of our drug discovery platform.

The browser app is the part the user sees.

The backend is the part that will do serious scientific calculations.

## Why We Need A Backend

JavaScript in the browser is good for buttons, tables, and simple actions.

Python is better for scientific work.

RDKit is a Python chemistry library that can calculate real molecular descriptors from SMILES.

Our target flow:

```text
Browser -> sends SMILES -> Python backend -> RDKit calculates -> Browser shows result
```

## Files

- `main.py` starts the web API.
- `chemistry.py` contains the molecule calculation code.
- `requirements.txt` lists Python packages we need.

## Important Setup Note

Your computer currently shows Python 2.7 when we run:

```text
python --version
```

For this backend, we need modern Python:

```text
Python 3.10 or newer
```

Later we will install:

```text
fastapi
uvicorn
rdkit
```

## What Is An API?

API means the app can ask another program for an answer.

Example:

Browser asks:

```text
Please analyze this molecule: CC(=O)OC1=CC=CC=C1C(=O)O
```

Backend answers:

```text
Molecular weight: 180.16
LogP: 1.31
HBD: 1
HBA: 4
TPSA: 63.6
Lipinski: Pass
```

