# Lesson 10: ADMET v1

Today we added a first-pass ADMET preview.

ADMET means:

- absorption
- distribution
- metabolism
- excretion
- toxicity

## Important

This version is rule-based.

It is not a trained machine learning model.

It is not a clinical decision tool.

It helps users understand early risk signals.

## What We Added

Solubility:

Estimated with an ESOL-style logS equation based on molecular weight, LogP, rotatable bonds, and aromatic atom proportion.

GI absorption:

Estimated from polarity, hydrogen bonding, and size.

BBB likelihood:

Estimated from TPSA, LogP, hydrogen donors, and charge.

Permeability:

Estimated from TPSA and rotatable bonds.

CYP risk:

Estimated from lipophilicity and molecular size.

Toxicity flag:

Simple warning for extreme size or lipophilicity.

## Company Meaning

This makes the product more useful, but we must be honest.

Later, we need proper ADMET models trained or validated with public datasets.
