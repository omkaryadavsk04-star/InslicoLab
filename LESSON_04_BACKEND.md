# Lesson 4: Backend And RDKit

Today we created the backend structure.

## Simple Meaning

The frontend is what you see.

The backend is the hidden laboratory.

In our company, the backend will do the real scientific work:

- molecule calculation
- ADMET prediction
- docking
- AI model execution
- report generation

## Why Python?

Python is popular in science because many scientific tools use it.

Drug discovery tools like RDKit, DeepChem, PyTorch, and docking scripts work well with Python.

## Why RDKit?

RDKit understands chemical structures.

For example, it can convert this:

```text
CC(=O)OC1=CC=CC=C1C(=O)O
```

into a real molecule object.

Then RDKit can calculate:

- molecular weight
- LogP
- H-bond donors
- H-bond acceptors
- TPSA
- rotatable bonds

## What We Built

We created:

```text
backend/main.py
backend/chemistry.py
backend/requirements.txt
backend/README.md
```

## What We Need Next

Your computer currently uses old Python 2.7.

To run modern chemistry software, we need Python 3.10 or newer.

Next company step:

1. Install Python 3.
2. Create a virtual environment.
3. Install RDKit and FastAPI.
4. Run our backend.
5. Connect the browser app to the backend.

