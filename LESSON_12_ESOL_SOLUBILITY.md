# Lesson 12: ESOL-Style Solubility

Today we started our first paper-inspired method track: solubility.

## What Is Solubility?

Solubility tells how well a compound dissolves in water.

In drug discovery, poor solubility can cause poor absorption and formulation problems.

## What Is logS?

logS is a common way to express aqueous solubility.

More negative values usually mean poorer solubility.

Example:

```text
logS = -2 is better than logS = -6
```

## What We Added

We added an ESOL-style equation:

```text
logS = 0.16 - 0.63 logP - 0.0062 MW + 0.066 RB - 0.74 AP
```

Where:

- logP = lipophilicity
- MW = molecular weight
- RB = rotatable bonds
- AP = aromatic atom proportion

## Why This Matters

This is a step beyond simple rules.

It uses a published descriptor-style model form.

It is still not our final proprietary method, but it teaches us how methods are built:

```text
descriptors -> equation/model -> prediction -> validation
```

## Next Step

To make our own solubility method, we need:

- a public solubility dataset
- RDKit descriptors
- train/test split
- model training
- validation metrics
- comparison with ESOL

