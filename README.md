# Aurenx Biosystems

Company website and recovered InSilicoLab backend prototype.

## Run locally

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

If `py` is not installed, run the first command with your Python 3.11 executable instead.

Open `http://127.0.0.1:8000`.

## Website features

- Aurenx Biosystems landing page
- Active product links for InsilicoLab and ManuScripta Scientific
- Upcoming placeholders for BioForge Labs and PharmaNexus
- Animated biotechnology network hero scene
- Contact footer for `www.aurenxbio.com`, `omkaryadavsk04@gmail.com`, and `+91 77956 29905`
- Basic Privacy and Terms pages

## Main pages

- `/` Aurenx Biosystems company website
- `/insilicolab` InsilicoLab drug-discovery workbench
- `/manuscripta` ManuScripta Scientific writing service
- `/upcoming` upcoming platform placeholder
- `/privacy` privacy notice
- `/terms` website terms

## Backend features

- RDKit descriptors and molecule SVG rendering at `/api/analyze` and `/api/structure.svg`
- Lipinski rule triage
- Rule-based drug-likeness interpretation
- First-pass ADMET notes

## Notes

This project is a research and education prototype. The rule-based ADMET output is not a clinical, toxicology, or regulatory prediction.
