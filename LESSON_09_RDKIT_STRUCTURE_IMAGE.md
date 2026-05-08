# Lesson 9: RDKit Molecule Images

Today we replaced the rough browser molecule drawing with real RDKit structure rendering.

## Before

The browser drew circles and lines by itself.

That was only a visual placeholder.

## Now

The browser asks Python/RDKit:

```text
Please draw this SMILES as a 2D molecule image.
```

RDKit returns an SVG image.

SVG means scalable vector graphic. It stays sharp when resized.

## Why This Matters

Drug discovery software needs chemical structures that look correct.

Real molecule drawing helps users trust the tool.

## New API

The backend now has:

```text
/api/structure.svg?smiles=...
```

This returns a molecule image.

