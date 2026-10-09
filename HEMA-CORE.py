import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from Blood_V2 import Blood_group
from Blood_CBC_V2 import CBC_Analyzer
import mysql.connector
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE


def rh_check(mother_rh, baby_rh, pregnancy_num):
    if mother_rh == '-' and baby_rh == '+':
        if pregnancy_num == '1':
            return 'Monitor - first pregnancy, no antibodies yet'
        else:
            return 'High risk - HDFN'
    return 'No risk'


st.title('HEMA-CORE')

sex = st.selectbox("Sex", ['M', 'F'])
blood_group = st.selectbox("Blood Group", ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'])

st.markdown("### Units")
hb_unit = st.selectbox("Hemoglobin unit", ["g/dL", "g/L"])
wbc_unit = st.selectbox("WBC unit", ["10⁹/L", "K/µL", "/µL"])
plt_unit = st.selectbox("Platelet unit", ["10⁹/L", "K/µL", "/µL"])

if hb_unit == "g/dL":
    hb = st.slider("Hemoglobin", 5.0, 25.0, 14.0, 0.1)
else:
    hb = st.slider("Hemoglobin", 50.0, 250.0, 140.0, 1.0)

if wbc_unit == "10⁹/L":
    wbc = st.slider("WBC", 1.0, 30.0, 7.0, 0.1)
else:
    wbc = st.slider("WBC", 1000, 30000, 7000, 100)

if plt_unit == "10⁹/L":
    platelets = st.slider("Platelets", 50, 800, 250, 1)
else:
    platelets = st.slider("Platelets", 50000, 800000, 250000, 1000)

mother_rh = st.selectbox('Mother Rh', ('+', '-'))
baby_rh = st.selectbox('Baby Rh', ('+', '-'))
pregnancy_num = st.selectbox('Pregnancy number', ('1', '2', '3', '4+'))

if st.button('Run'):
    hb_val = hb
    if hb_unit == "g/L":
        hb_val = hb / 10

    wbc_val = wbc
    if wbc_unit in ["K/µL", "/µL"]:
        wbc_val = wbc / 1000

    plt_val = platelets
    if plt_unit in ["K/µL", "/µL"]:
        plt_val = platelets / 1000

    patient = CBC_Analyzer(sex, hb_val, wbc_val, plt_val)
    hb_label = patient.hb_check()
    wbc_label = patient.WBC_check()
    platelets_label = patient.Platelets_check()

    bg = Blood_group(blood_group)
    receive_list = bg.can_receive_from()

    rh_result = rh_check(mother_rh, baby_rh, pregnancy_num)

    conn = mysql.connector.connect(
        host=MYSQL_HOST, user=MYSQL_USER,
        password=MYSQL_PASSWORD, database=MYSQL_DATABASE
    )
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hematology_reports (
            id INT AUTO_INCREMENT PRIMARY KEY,
            sex VARCHAR(1),
            blood_group VARCHAR(3),
            hb FLOAT, hb_unit VARCHAR(10), hb_label VARCHAR(60),
            wbc FLOAT, wbc_unit VARCHAR(10), wbc_label VARCHAR(60),
            platelets FLOAT, plt_unit VARCHAR(10), platelets_label VARCHAR(60),
            mother_rh VARCHAR(1),
            baby_rh VARCHAR(1),
            pregnancy_num VARCHAR(2),
            rh_result VARCHAR(60)
        )
    """)

    insert_sql = """INSERT INTO hematology_reports
        (sex, blood_group,
         hb, hb_unit, hb_label,
         wbc, wbc_unit, wbc_label,
         platelets, plt_unit, platelets_label,
         mother_rh, baby_rh, pregnancy_num, rh_result)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    cursor.execute(insert_sql, (
        sex, blood_group,
        hb, hb_unit, hb_label,
        wbc, wbc_unit, wbc_label,
        platelets, plt_unit, platelets_label,
        mother_rh, baby_rh, pregnancy_num, rh_result
    ))
    conn.commit()
    cursor.close()
    conn.close()

    st.write(f"*Blood group:* {blood_group}")
    st.write(f"*Can receive from:* {receive_list}")
    st.write(f"*Hemoglobin:* {hb_label}")
    st.write(f"*WBC:* {wbc_label}")
    st.write(f"*Platelets:* {platelets_label}")

    if 'High' in rh_result:
        st.error(rh_result)
    elif 'Monitor' in rh_result:
        st.warning(rh_result)
    else:
        st.success(rh_result)

    fig, axes = plt.subplots(3, 1, figsize=(8, 5))

    ax = axes[0]
    low, high = CBC_Analyzer.parameters['hb'][sex]
    ax.axvspan(low, high, color='green', alpha=0.2)
    ax.axvline(hb_val, color='green' if 'Normal' in hb_label else 'red', linewidth=3)
    ax.set_xlim(0, 25); ax.set_yticks([])
    ax.set_title(f"Hemoglobin: {hb_label}")

    ax = axes[1]
    low, high = CBC_Analyzer.parameters['WBC']
    ax.axvspan(low, high, color='green', alpha=0.2)
    ax.axvline(wbc_val, color='green' if 'Normal' in wbc_label else 'red', linewidth=3)
    ax.set_xlim(0, 30); ax.set_yticks([])
    ax.set_title(f"WBC: {wbc_label}")

    ax = axes[2]
    low, high = CBC_Analyzer.parameters['Platelets']
    ax.axvspan(low, high, color='green', alpha=0.2)
    ax.axvline(plt_val, color='green' if 'Normal' in platelets_label else 'red', linewidth=3)
    ax.set_xlim(0, 800); ax.set_yticks([])
    ax.set_title(f"Platelets: {platelets_label}")

    plt.tight_layout()
    st.pyplot(fig)