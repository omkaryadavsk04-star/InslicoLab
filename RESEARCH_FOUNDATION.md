# Research Foundation For InSilicoLab

## Key Question

Do tools like SwissADME use RDKit as their whole base?

Answer: not necessarily.

SwissADME's published 2017 paper reports a backend mainly coded in Python 2.7, with molecular handling from OpenBabel, ChemAxon/JChem services, and in-house models such as iLOGP, BOILED-Egg, and Bioavailability Radar.

So SwissADME is not simply "RDKit + web page."

It is a collection of:

- cheminformatics toolkits
- published descriptor methods
- in-house predictive models
- carefully designed interpretation
- web interface

## What We Are Doing

We are using RDKit as our first chemistry engine because it is open-source, modern, powerful, and widely used.

RDKit gives us:

- molecule parsing from SMILES
- descriptors
- fingerprints
- 2D structure images
- 3D conformer generation
- substructure search
- molecular similarity
- machine learning features

But RDKit alone is not the full company.

Our product should combine:

```text
RDKit + public papers + public datasets + our own models + our own validation + our own interface
```

## Research Areas To Add

### 1. Drug-Likeness Rules

Use:

- Lipinski Rule of Five
- Veber rules
- Ghose filter
- Egan filter
- Muegge filter

Purpose:

- oral drug-likeness screening
- quick medicinal chemistry triage

### 2. SwissADME-Like Interpretation

Study:

- Bioavailability Radar
- BOILED-Egg model
- iLOGP and consensus LogP ideas
- ESOL solubility model

Purpose:

- make outputs easier to understand
- show visual interpretation, not only numbers

### 3. ADMET Machine Learning

Use datasets and benchmarks from:

- MoleculeNet
- Therapeutics Data Commons
- ChEMBL
- PubChem BioAssay
- Tox21
- ClinTox
- BBBP
- ESOL
- FreeSolv
- Lipophilicity

Purpose:

- train and compare real ML models
- avoid fake predictions
- report confidence and limitations

### 4. Molecular Similarity

Use:

- Morgan fingerprints
- Tanimoto similarity
- scaffold analysis
- matched molecular pair analysis later

Purpose:

- compare molecules
- find analogs
- guide lead optimization

### 5. Docking

Start with:

- AutoDock Vina
- Smina or Gnina later

Build our own:

- protein preparation workflow
- ligand preparation workflow
- docking UI
- result interpretation
- reports
- validation examples

Purpose:

- learn docking properly
- avoid copying proprietary docking software

### 6. Validation

Every serious prediction module needs validation.

For each model, record:

- dataset source
- number of molecules
- train/test split
- metric
- limitations
- date tested

## Scientific Honesty Rule

We must clearly label each module as:

- descriptor
- rule-based estimate
- machine learning prediction
- experimental model
- validated model

This protects users and builds trust.

## Next Product Upgrade

Add a "Research basis" or "Method" section inside the app.

For each result, the user should see:

- what method was used
- whether it is RDKit, rule-based, or ML
- related scientific reference
- limitation

