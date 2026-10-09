# HEMA-CORE

A unified hematology pipeline — blood compatibility, CBC interpretation, and Rh-pregnancy risk in one Streamlit dashboard, backed by MySQL.

**Live app:** [STREAMLIT_URL]

---

## What it does

HEMA-CORE merges three clinical tools into one interface:

1. **Blood compatibility** — given a recipient's ABO+Rh type, returns the donor types they can safely receive from.
2. **CBC interpreter** — given hemoglobin, WBC, and platelet counts, returns Low / Normal / High with disease labels (Anemia, Polycythemia, Leukopenia, Leukocytosis, Thrombocytopenia, Thrombocytosis, etc.).
3. **Rh-pregnancy risk** — given the mother's Rh status, baby's Rh status, and pregnancy number, returns a risk tier and clinical recommendation.

Every run logs to MySQL (`hematology_reports`) with a timestamp for an audit trail.

---

```markdown
**Sources:** WHO Hemoglobin Concentrations (2023), Tietz Clinical Chemistry (adult reference ranges), ACOG guidelines for Rh sensitization and anti-D prophylaxis.
```

## Why this project exists

HEMA-CORE was built to combine three common hematology workflows in a single, easy-to-use interface. Instead of checking blood compatibility, CBC interpretation, and Rh-pregnancy risk separately, a clinician or student can use one app to review all three in a single workflow.

This project is useful as a decision-support and learning tool, but it should be treated as a flagging aid rather than a diagnostic system.

---

## How it's built — the four-layer ladder

Each subsystem was built four times using the same logic, increasing in complexity:

| Layer | What it is |
|---|---|
| V1 | Dict + if/else — bare logic, no abstraction |
| V2 | Class with methods — state + behavior |
| V3 | CSV → validate → transform → MySQL — full ETL |
| V4 | Streamlit UI — the delivery layer |
| HEMA-CORE | Merges V4 of Arc 1 + Arc 2 + new Rh logic |

The goal of the four layers is not to ship four separate products. It is to see the same logic repeated in increasingly complete wrappers so the structure becomes familiar and reusable.

---

## Clinical reference ranges

| Parameter | Male | Female | Source |
|---|---|---|---|
| Hemoglobin (g/dL) | 13.5 – 17.5 | 12.0 – 15.5 | WHO Hemoglobin Concentrations 2023 |
| WBC (×10⁹/L) | 4.0 – 11.0 | 4.0 – 11.0 | Tietz Clinical Chemistry, standard adult |
| Platelets (×10⁹/L) | 150 – 450 | 150 – 450 | Tietz Clinical Chemistry, standard adult |

Ranges are adult-only. Pediatric and neonatal ranges differ.

---

## Validation

- **10 pytest tests** cover all Rh combinations, blood-group edge cases, and CBC boundary values (`test_hema.py`).
- **Rh logic** is validated against ACOG guidance (mother Rh−, baby Rh+, sensitized → HDFN risk; unsensitized first pregnancy → monitor, anti-D prophylaxis at 28 weeks).
- **Boundary checks** hit exact threshold values (Hb 13.5 for male, 12.0 for female) to catch `<` vs `≤` errors.

Run:

```bash
python -m pytest test_hema.py -v
```

---

## Case study — 45F with anemia

Input: Female, blood group B−, Hb 10.10 g/dL, WBC 7.00 ×10⁹/L, Platelets 180 ×10⁹/L, mother Rh−, baby Rh+, pregnancy 1.

Output:

- Blood compatibility: can receive from B− and O− only
- Hb: Anemia (below female range 12.0–15.5)
- WBC: Normal (inside 4.0–11.0)
- Platelets: Normal (inside 150–450)
- Rh status: Monitor — first pregnancy, no antibodies yet

Clinical interpretation: the CBC panel flags anemia in a pre-menopausal female, which in practice triggers iron studies and a GI workup. The Rh status is not yet sensitized, which matches the standard monitoring approach for an unsensitized first pregnancy.

---

## Limitations

- **Adult ranges only.** Pediatric and neonatal CBC ranges differ significantly from adult values.
- **"Normal" means "in reference range," not "healthy."** A chronically anemic patient at 12.5 g/dL may be normal for them and still require clinical attention.
- **Flags, does not diagnose.** HEMA-CORE surfaces abnormal values and risk tiers. It does not replace clinical judgment. Every output is a flag for further review, not a diagnosis.
- **Unit handling covers g/dL ↔ g/L for Hb, and /µL ↔ 10⁹/L for WBC and platelets.** Raw inputs are stored alongside their units in MySQL for audit. Glucose unit conversion is handled separately in the broader pipeline.
- **No age stratification.** Reference ranges do not vary by patient age. A 20-year-old and a 75-year-old receive the same thresholds.
- **Rh logic covers the two-outcome case.** It returns "high risk" or "monitor" — it does not model anti-D dosing, sensitization history from prior miscarriages or transfusions, or partial D variants.

---

## Run locally

```bash
git clone https://github.com/CodeXSourabhsingh/bio-pipelines
cd bio-pipelines
pip install -r requirements.txt
streamlit run HEMA-CORE.py
```

Run tests:

```bash
python -m pytest test_hema.py -v
```

---

## Project structure

```text
HEMA-CORE.py            Streamlit app
Blood_V2.py             Blood group class (Arc 1 V2)
Blood_CBC_V2.py         CBC analyzer class (Arc 2 V2)
Blood_CBC_V3.py         ETL pipeline (Arc 2 V3)
rh_tools.py             Rh-pregnancy logic (importable for tests)
test_hema.py            pytest suite
config.py               MySQL credentials (not committed)
requirements.txt
```

---

## Stack

Python · Streamlit · pandas · matplotlib · MySQL · pytest

---

## Author

Sourabh Singh — [LinkedIn](https://www.linkedin.com/in/sourabh-singh-7b1249434/?isSelfProfile=true) · [GitHub](https://github.com/CodeXSourabhsingh)
