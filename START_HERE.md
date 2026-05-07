# InSilicoLab: Start Here

You are building a drug discovery software company from the basics.

This project will grow slowly:

1. Simple web page
2. Real molecule calculations with RDKit
3. Protein and ligand upload
4. Docking with AutoDock Vina
5. AI models for ADMET, toxicity, and activity prediction
6. Reports and a professional user interface

## What The Current App Is

The current app is a small web page. It has three files:

- `index.html` is the skeleton. It creates buttons, input boxes, sections, and tables.
- `styles.css` is the design. It controls colors, layout, spacing, and the app look.
- `app.js` is the brain. It reacts when you click buttons and calculates rough molecule properties.

## Important Meaning

Frontend means the part you see in the browser.

Backend means the hidden engine that does heavier work, usually with Python.

RDKit is a chemistry toolkit. It can understand molecules properly from SMILES.

Docking means trying to predict how a small molecule fits inside a protein binding site.

ADMET means absorption, distribution, metabolism, excretion, and toxicity.

## Our Learning Rule

We will not memorize everything.

We will build one small thing, understand it, then build the next thing.

## Lesson 1: What Is A Web App?

A web app is like a clinic form, but interactive.

Example:

1. You type a molecule SMILES.
2. You click Analyze.
3. The app reads your input.
4. The app calculates something.
5. The app shows a result.

In code:

- HTML creates the form.
- JavaScript reads the form.
- JavaScript calculates the result.
- HTML displays the result.

## Lesson 2: What Is SMILES?

SMILES is a text way to write a molecule.

Aspirin:

```text
CC(=O)OC1=CC=CC=C1C(=O)O
```

This text represents atoms and bonds. Real chemistry software like RDKit converts this text into a molecule object that computers can understand.

## Lesson 3: Why Our First App Is Not Like SwissADME Yet

SwissADME uses proper cheminformatics models.

Our first app only uses rough JavaScript estimates. It is for learning software structure.

The next scientific upgrade is:

```text
SMILES -> Python backend -> RDKit -> real descriptors -> browser result
```

That is our next major build step.

