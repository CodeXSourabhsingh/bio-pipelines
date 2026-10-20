import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import mysql.connector
from Glucose_Diabetes_risk_V2 import GD_risk
from Pharmacokinetics_dosage_tracker_V2 import PK_Dosage

try:
    from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE
except ImportError:
    MYSQL_HOST = None

st.set_page_config(page_title="METABO-CORE", layout="centered")

st.title("METABO-CORE")
st.write("Metabolic risk assessment and pharmacokinetic dose estimation in one interface.")

def write_row(row):
    if not MYSQL_HOST:
        return False
        
    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST, user=MYSQL_USER,
            password=MYSQL_PASSWORD, database=MYSQL_DATABASE,
            connection_timeout=3
        )
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metabo_core_results (
                id INT AUTO_INCREMENT PRIMARY KEY,
                type VARCHAR(20),
                fg FLOAT, pmg FLOAT, glucose_risk VARCHAR(30),
                weight FLOAT, half_life FLOAT, target FLOAT, drug VARCHAR(50),
                vd FLOAT, loading_dose FLOAT, maintenance_dose FLOAT, steady_state FLOAT,
                logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            INSERT INTO metabo_core_results
            (type, fg, pmg, glucose_risk,
             weight, half_life, target, drug,
             vd, loading_dose, maintenance_dose, steady_state)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row.get('type'),
            row.get('fg'), row.get('pmg'), row.get('glucose_risk'),
            row.get('weight'), row.get('half_life'), row.get('target'), row.get('drug'),
            row.get('vd'), row.get('loading_dose'),
            row.get('maintenance_dose'), row.get('steady_state'),
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        return False


tab1, tab2 = st.tabs(["Glucose Risk", "PK Dosage"])

with tab1:
    st.subheader("Glucose Risk Assessment")
    st.write("Fasting and post-meal glucose → risk classification.")

    fg = st.slider("Fasting Glucose (mg/dL)", 50, 250, 95, 1)
    pmg = st.slider("Post-Meal Glucose (mg/dL)", 80, 350, 130, 1)

    if st.button("Assess glucose risk"):

        patient = GD_risk(fg, pmg)
        fg_tier = patient.FG_check()
        pmg_tier = patient.PMG_check()
        final = patient.combined_risk()

        st.write(f"**Fasting Glucose:** {fg_tier}")
        st.write(f"**Post-Meal Glucose:** {pmg_tier}")

        if final == 'Diabetic':
            st.error(f"**Final: {final}**")
        elif final == 'PreDiabetic':
            st.warning(f"**Final: {final}**")
        else:
            st.success(f"**Final: {final}**")

        fig, axes = plt.subplots(2, 1, figsize=(8, 5))

        ax = axes[0]
        ax.axvspan(0, 100, color='green', alpha=0.25)
        ax.axvspan(100, 126, color='gold', alpha=0.35)
        ax.axvspan(126, 250, color='red', alpha=0.25)
        ax.axvline(fg, color='black', linewidth=3)
        ax.set_xlim(0, 250); ax.set_yticks([])
        ax.set_title(f"Fasting Glucose: {fg_tier} ({fg} mg/dL)")

        ax = axes[1]
        ax.axvspan(0, 140, color='green', alpha=0.25)
        ax.axvspan(140, 200, color='gold', alpha=0.35)
        ax.axvspan(200, 350, color='red', alpha=0.25)
        ax.axvline(pmg, color='black', linewidth=3)
        ax.set_xlim(0, 350); ax.set_yticks([])
        ax.set_title(f"Post-Meal Glucose: {pmg_tier} ({pmg} mg/dL)")

        plt.tight_layout()
        st.pyplot(fig)

        ok = write_row({
            'type': 'glucose',
            'fg': float(fg), 'pmg': float(pmg),
            'glucose_risk': final,
        })
        if not ok:
            st.caption("DB logging skipped.")

with tab2:
    st.subheader("Pharmacokinetic Dose Estimation")

    VD_TABLE = {
        'Warfarin':     0.14,
        'Digoxin':      7.0,
        'Theophylline': 0.5,
        'Gentamicin':   0.25,
        'Metformin':    1.0,
    }

    drug = st.selectbox("Drug", list(VD_TABLE.keys()))
    weight = st.slider("Patient weight (kg)", 30.0, 150.0, 70.0, 0.5)
    half_life = st.slider("Drug half-life (hours)", 1.0, 72.0, 40.0, 0.5)
    target = st.slider("Target plasma concentration (mg/L)", 0.1, 5.0, 2.0, 0.1)

    if st.button("Calculate dose"):

        pk = PK_Dosage(weight, half_life, target, drug)
        vd = pk.vd()
        ld = pk.ld()
        md = pk.md()
        ss = pk.steady_state()
        k = 0.693 / half_life

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Volume of Distribution", f"{vd:.2f} L")
            st.metric("Loading Dose", f"{ld:.2f} mg")
        with col2:
            st.metric("Maintenance Dose (12h)", f"{md:.2f} mg")
            st.metric("Steady State", f"{ss:.1f} hours")

        t = np.linspace(0, 5 * half_life, 100)
        C = target * np.exp(-k * t)

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(t, C, color='steelblue', linewidth=2, label='Plasma concentration')
        ax.axhline(y=target, color='grey', linestyle='--', linewidth=1, label=f'Target: {target} mg/L')
        ax.axvline(x=ss, color='orange', linestyle=':', linewidth=1, label=f'Steady state: {ss:.0f}h')
        ax.set_xlabel("Time (hours)")
        ax.set_ylabel("Concentration (mg/L)")
        ax.set_title(f"{drug} — {weight} kg, half-life {half_life}h")
        ax.legend()
        ax.grid(alpha=0.3)

        st.pyplot(fig)

        ok = write_row({
            'type': 'pk',
            'weight': float(weight), 'half_life': float(half_life),
            'target': float(target), 'drug': drug,
            'vd': float(vd), 'loading_dose': float(ld),
            'maintenance_dose': float(md), 'steady_state': float(ss),
        })
        if not ok:
            st.caption("DB logging skipped.")

st.divider()
st.caption("⚠️ **DISCLAIMER:** This tool is for educational and clinical decision support purposes only.")
st.caption("It is NOT a substitute for professional medical advice, diagnosis, or treatment.")
st.caption("All outputs, calculations, and triage recommendations must be independently verified by a qualified healthcare provider.")
st.caption("Do not prescribe or make clinical decisions based solely on this software.")
