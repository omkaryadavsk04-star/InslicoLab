# Lesson 11: How We Create Our Own Methods

Yes, we can create our own methods.

But in science, a method is not just an idea.

A real method needs:

1. a scientific question
2. a dataset
3. molecular features
4. an algorithm
5. validation
6. comparison with existing methods
7. limitations
8. documentation or publication

## Example: Our Own Solubility Method

Question:

```text
Can we predict whether a molecule has good aqueous solubility?
```

Dataset:

```text
Known molecules with measured solubility values.
```

Features:

```text
LogP, molecular weight, TPSA, HBD, HBA, rings, charge, fingerprints.
```

Algorithm:

```text
Start with rules, then train machine learning models.
```

Validation:

```text
Test on molecules the model has never seen.
```

Comparison:

```text
Compare our model against simple baselines and published methods.
```

## How Companies Do It

Companies like Schrödinger and SwissADME teams build methods by combining:

- chemistry theory
- physics
- experimental data
- cheminformatics
- machine learning
- benchmarking
- years of validation

Their advantage is not only code.

Their advantage is validated scientific knowledge.

## Our Path

First, we use RDKit and published rules.

Second, we reproduce known published methods where allowed.

Third, we train our own models on public datasets.

Fourth, we validate and publish results.

Fifth, our validated models become InSilicoLab methods.

## Company Rule

Do not call something our own method just because we coded it.

Call it our own method only after we test it, compare it, and document it honestly.

