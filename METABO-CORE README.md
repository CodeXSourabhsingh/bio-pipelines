# METABO-CORE

**A unified clinical pipeline for metabolic risk assessment and pharmacokinetic dose estimation, built with Streamlit and MySQL.**

Live demo: <LIVE_URL_PLACEHOLDER>  
GitHub: <GITHUB_REPO_PLACEHOLDER>

---

## Table of Contents

- [What it does](#what-it-does)
- [Quick features](#quick-features)
- [Architecture (The Four-Layer Ladder)](#architecture-the-four-layer-ladder)
- [Validation & Testing](#validation--testing)
- [Clinical reference ranges & formulas](#clinical-reference-ranges--formulas)
- [Data logging & schema](#data-logging--schema)
- [Limitations](#limitations)
- [Tech stack](#tech-stack)
- [Run locally](#run-locally)
- [How AI was used](#how-ai-was-used)
- [License & Contributing](#license--contributing)

---

## What it does

METABO-CORE merges two clinical tools into a single, human-in-the-loop interface:

1. **Metabolic Risk (Glucose)**
   - Evaluates fasting and post-meal glucose values and classifies risk tier: **Normal**, **PreDiabetic**, or **Diabetic**.
   - Displays the patient’s measurements on a visual range band to show where the readings fall against published clinical thresholds.

2. **Pharmacokinetics (PK)**
   - Calculates **Volume of Distribution (Vd)**, **Loading Dose**, **Maintenance Dose**, and **Steady State** time based on patient weight, drug half-life, and target plasma concentration.
   - Renders an exponential decay curve showing drug clearance over time and highlights the target concentration line.

Every run is logged into MySQL to a single, discriminated table: **metabo_core_results**.

---

## Quick features

- Two-tab Streamlit dashboard (Glucose + PK)
- Unified logging to MySQL with a single result table and a `type` discriminator
- Visual analytics for glucose clinical range bands and PK decay curves
- Standard PK calculations grounded in clinically recognized formulas
- Human-in-the-loop decision support: flags and calculates, but does not prescribe

---

## Architecture (The Four-Layer Ladder)

METABO-CORE follows a progressive architecture model that reflects the project’s evolution:

| Layer | Description |
|---|---|
| **V1** | Dict + if/else logic for rapid prototyping |
| **V2** | Class-based logic with state and behavior encapsulation |
| **V3** | CSV → validate → transform → MySQL ETL pipeline |
| **V4** | Streamlit UI as the user-facing delivery layer |

**METABO-CORE** brings together the V2 logic from both clinical arcs into a two-tab Streamlit dashboard and stores all results in a single MySQL table using a `type` column to distinguish record types such as `glucose` and `pk`.

---

## Validation & Testing

- **15 pytest tests** cover the complete logic engine.
- **Glucose tests** verify boundary conditions, including exact thresholds for **PreDiabetic** vs **Diabetic** for both fasting and post-meal glucose.
- **PK tests** verify the mathematical formulas, including **Warfarin** and **Digoxin** calculations against hand-calculated expected values.
- **Hierarchy rule tests** explicitly confirm that if either glucose value is diabetic, the final result is diabetic.

This test suite is designed to validate both edge cases and standard clinical input patterns.

---

## Clinical reference ranges & formulas

### Glucose — ADA / WHO thresholds

| Metric | Normal | PreDiabetic | Diabetic |
|---|---|---|---|
| **Fasting glucose** | < 100 mg/dL | 100–125 mg/dL | ≥ 126 mg/dL |
| **Post-meal glucose (2h)** | < 140 mg/dL | 140–199 mg/dL | ≥ 200 mg/dL |

> Final glucose classification follows the **worst (highest-risk)** of the two values. If either reading is diabetic, the patient is classified as **Diabetic**.

### Pharmacokinetics (standard equations)

- **Vd = weight × Vd_per_kg**
- **k = ln(2) / half-life**
- **CL = k × Vd**
- **Loading dose = Vd × target_concentration**
- **Maintenance dose = CL × target_concentration**
- **Steady state ≈ 4–5 × half-life**

This tool is intended for **clinical flagging and decision support**. It does not prescribe therapy.

---

## Data logging & schema

All runs are recorded to the MySQL table **metabo_core_results** as a single unified dataset with a discriminating `type` column.

| Column | Type | Notes |
|---|---|---|
| `id` | INT (PK) | Auto-generated row identifier |
| `created_at` | DATETIME | Timestamp of the run |
| `type` | ENUM('glucose', 'pk') | Result category discriminator |
| `fasting_glucose` | FLOAT | Fasting value in mg/dL |
| `post_meal_glucose` | FLOAT | Post-meal value in mg/dL |
| `glucose_risk` | VARCHAR | Final glucose classification |
| `drug` | VARCHAR | Drug name for PK calculations |
| `weight_kg` | FLOAT | Patient body weight |
| `half_life_h` | FLOAT | Drug half-life in hours |
| `target_conc` | FLOAT | Target concentration |
| `vd_l` | FLOAT | Calculated Vd |
| `loading_dose_mg` | FLOAT | Calculated loading dose |
| `maintenance_dose_mg` | FLOAT | Calculated maintenance dose |
| `steady_state_h` | FLOAT | Estimated steady-state time |
| `payload_json` | JSON | Full record for audit and reproducibility |
| `user_id` | VARCHAR | Optional clinician or session identifier |

This unified logging model simplifies auditing, comparisons across clinical runs, and future integration work.

---

## Limitations

- **Adult glucose ranges only**: the current logic is not validated for pediatric or pregnancy-specific thresholds.
- **No organ-system modeling**: the PK module is purely mathematical and does not account for renal, hepatic, or cardiac impairment.
- **Maintenance dosing assumption**: the PK tool uses standard **12-hour dosing intervals** for the maintenance dose calculation.
- **Decision-support only**: the application is designed to **flag and estimate**, not to prescribe therapy.

---

## Tech Stack

| Category | Tools |
|---|---|
| **Core** | Python |
| **UI** | Streamlit |
| **Data processing** | pandas, numpy |
| **Visualization** | matplotlib |
| **Database** | MySQL |
| **Testing** | pytest |

---

## Run locally

Clone the repository and run the application locally:

```bash
git clone https://github.com/CodeXSourabhsingh/bio-pipelines.git
cd bio-pipelines
pip install -r requirements.txt
streamlit run app.py
```

### Local configuration

If your environment requires MySQL connectivity, set the relevant database variables before starting the app:

```bash
export METABO_CORE_DB_HOST=localhost
export METABO_CORE_DB_PORT=3306
export METABO_CORE_DB_USER=root
export METABO_CORE_DB_PASSWORD=your_password
export METABO_CORE_DB_NAME=metabo_core
```

---

## How AI was used

AI was used as a coding partner for syntax, scaffolding, and boilerplate generation. The architecture, clinical logic routing, boundary testing, and user experience design were directed and reviewed by the developer. AI accelerated implementation without replacing domain logic or engineering judgment.

---

## License & Contributing

- **License**: TODO — add the appropriate open-source license for the project (for example, MIT or Apache-2.0).
- **Contributing**: Contributions are welcome. Please keep changes scoped, document new logic clearly, and include tests for any new mathematical or clinical behavior.

---

This project is designed to support **clinical interpretation and decision support** using structured logic, transparent calculations, and auditable logging.
