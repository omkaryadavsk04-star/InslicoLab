# Lesson 5: Connecting The Website To RDKit

Before this lesson, the browser calculated molecule properties using rough JavaScript estimates.

Now the browser tries to call the Python backend first.

## What Happens Now

When you type a SMILES and click Analyze:

```text
Browser -> sends SMILES to Python -> RDKit calculates -> browser shows result
```

If the Python backend is running, the app shows:

```text
Engine: RDKit
```

If the Python backend is not running, the app falls back to the old simple calculator and shows:

```text
Engine: Local
```

## Why This Matters

Local JavaScript estimates are only for learning.

RDKit results are real cheminformatics descriptors and are much closer to tools like SwissADME.

## Backend Address

The backend runs on your own computer:

```text
http://127.0.0.1:8000
```

This means it is local, private, and not online.

