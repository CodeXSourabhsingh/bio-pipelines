# METABO-CORE

Integrated metabolic risk and pharmacokinetic dose estimation — a two-tab clinical decision-support tool.

- Tab 1: Glucose risk assessment (flagging mode)
- Tab 2: Pharmacokinetic (PK) dose estimation (indicative)

Built with Python, Streamlit, Pandas, NumPy, Matplotlib, and MySQL. Designed human-in-the-loop.

## What it does

### Tab 1 — Glucose Risk Assessment
- Input: fasting glucose and post-meal glucose.
- Output: risk classification (Normal, PreDiabetic, Diabetic) based on published threshold values.
- Visualized as a simple bar chart against normal ranges.

### Tab 2 — Pharmacokinetic Dose Estimation
- Input: drug, patient weight, half-life, and target plasma concentration.
- Output: Volume of Distribution (Vd), Loading Dose, Maintenance Dose, and Steady State.
- Visualized as an exponential concentration decay curve over time.
- Includes a concentration decay chart showing the target line and steady-state point.

## Architecture

This tool was designed on paper before any code was written. The full flowchart is in the Architecture Notebook.

Pipeline:
Input → Pandas calculation → MySQL logging → Matplotlib visualisation → Streamlit UI

Philosophy: Mode is a data decision, not a capability decision.

Every clinical tool has two possible modes: flag or prescribe. The choice depends on the integrity of the input data.

- Indicative data → flag. (This is the current version.)
- Verified, patient-specific data → prescribe. (Same architecture, different data requirement.)

Building both is the same engineering. Choosing the right one is the discipline.

## Tests

15 pytest tests covering:

- Glucose boundary conditions (Normal / PreDiabetic / Diabetic thresholds)
- Combined risk hierarchy (worst side drives the final label)
- PK formula verification (Vd, loading dose, maintenance dose, steady state) against hand-calculated values
- Multi-drug validation (Warfarin, Digoxin)

## How to run locally

```bash
git clone https://github.com/CodeXSourabhsingh/bio-pipelines.git
cd bio-pipelines
pip install -r requirements.txt
streamlit run app.py
```

## Stack

Python · Streamlit · Pandas · NumPy · Matplotlib · MySQL

## Author

Sourabh Singh — [LinkedIn] · [GitHub] · [Architecture Notebook]

---
