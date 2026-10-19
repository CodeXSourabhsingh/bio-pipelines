# METABO‑CORE

**A unified clinical pipeline for metabolic risk assessment and pharmacokinetic dose estimation.**

Streamlit · MySQL · Python

Live demo: <LIVE_URL_PLACEHOLDER>  
Repo: <GITHUB_REPO_PLACEHOLDER>

---

## Summary

METABO‑CORE combines two clinician‑facing calculators into a single, auditable Streamlit dashboard:

- Metabolic risk (glucose): classifies fasting and 2‑hour post‑meal glucose into **Normal**, **PreDiabetic**, or **Diabetic** and visualizes values on a clinical range band.
- Pharmacokinetics (PK): computes **Vd**, **Loading Dose**, **Maintenance Dose**, and **Steady‑State** time from patient weight, drug half‑life, and target concentration, and plots an exponential decay curve.

All runs are recorded to a single MySQL table (`metabo_core_results`) for audit and downstream analytics.

---

## Highlights

- Two‑tab Streamlit UI (Glucose | PK)
- Unified MySQL logging with a `type` discriminator (glucose / pk)
- Clear, auditable calculations and visualizations
- Human‑in‑the‑loop: flags and estimates; does not prescribe

---

## What it does (concise)

1. Metabolic Risk (Glucose)
   - Inputs: fasting glucose, 2‑hour post‑meal glucose
   - Output: risk tier (Normal / PreDiabetic / Diabetic)
   - Visualization: range band showing patient position vs thresholds

2. Pharmacokinetics (PK)
   - Inputs: drug name, patient weight, half‑life, target concentration
   - Outputs: Vd, elimination constant (k), Clearance (CL), Loading Dose, Maintenance Dose, estimated steady state
   - Visualization: exponential concentration decay with target line and steady‑state marker

---

## Architecture — The Four‑Layer Ladder

- **V1:** Dict + if/else (prototype logic)
- **V2:** Class + methods (encapsulated clinical logic)
- **V3:** CSV → validate → transform → MySQL (ETL)
- **V4:** Streamlit UI (delivery)

METABO‑CORE integrates the V2 logic of both clinical arcs into a two‑tab Streamlit dashboard and persists results in a discriminated MySQL table (`type` column).

---

## Validation & Testing

- **15 pytest tests** verify the core engine.
  - Glucose boundary tests validate exact thresholds for fasting and post‑meal categories.
  - PK tests validate formulas and example drugs (Warfarin, Digoxin) against hand‑calculated results.
  - Hierarchy rule: if either fasting or post‑meal is Diabetic → final label is Diabetic.

---

## Clinical reference ranges & formulas

Glucose (ADA / WHO):

| Measure | Normal | PreDiabetic | Diabetic |
|---|---:|---:|---:|
| Fasting | < 100 mg/dL | 100–125 mg/dL | ≥ 126 mg/dL |
| 2‑hr post‑meal | < 140 mg/dL | 140–199 mg/dL | ≥ 200 mg/dL |

PK equations (used by the tool):

- Vd = weight × Vd_per_kg
- k = ln(2) / half_life
- CL = k × Vd
- Loading dose = Vd × target_concentration
- Maintenance rate = CL × target_concentration
- Maintenance dose per interval = Maintenance rate × dosing_interval (default 12h)
- Steady state ≈ 4× half_life (practical estimate)

Note: METABO‑CORE performs calculations for decision support and does not issue prescriptions.

---

## Data model (summary)

All runs are logged to `metabo_core_results` with fields such as:

- id, created_at, type (`glucose` | `pk`)
- fasting_glucose, post_meal_glucose, glucose_risk
- drug, weight_kg, half_life_h, target_conc
- vd_l, loading_dose_mg, maintenance_dose_mg, steady_state_h
- payload_json (inputs + outputs), user_id

This single, discriminated table simplifies audit trails and analytics.

---

## Limitations

- Adult glucose reference ranges only (no pediatric or pregnancy ranges).
- PK calculations are mathematical models only — organ dysfunction and interactions are not modeled.
- Maintenance dose calculations assume a 12‑hour dosing interval unless configured otherwise.
- Intended for clinical decision support (flagging/estimation), not for autonomous prescribing.

---

## Tech stack

Python · Streamlit · pandas · numpy · matplotlib · MySQL · pytest

---

## Run locally

```bash
git clone https://github.com/CodeXSourabhsingh/bio-pipelines.git
cd bio-pipelines
pip install -r requirements.txt
streamlit run app.py
```

Environment variables (example):

```bash
export METABO_CORE_DB_HOST=localhost
export METABO_CORE_DB_PORT=3306
export METABO_CORE_DB_USER=root
export METABO_CORE_DB_PASSWORD=your_password
export METABO_CORE_DB_NAME=metabo_core
```

For quick local testing, you can substitute MySQL with an in‑memory CSV or SQLite fixture.

---

## How AI was used

AI assisted with syntax, scaffolding, and boilerplate. All clinical logic, architecture decisions, testing, and UI design were developer‑directed and validated.

---

## Author

Sourabh Singh — [LinkedIn] · [GitHub] · [Architecture Notebook]

---

If you want further edits, tell me what to change.