from Glucose_Diabetes_risk_V2 import GD_risk
from Pharmacokinetics_dosage_tracker_V2 import PK_Dosage


# ---------- Glucose tests ----------
def test_fg_normal():
    p = GD_risk(95, 130)
    assert p.FG_check() == 'Normal'

def test_fg_prediabetic():
    p = GD_risk(110, 130)
    assert p.FG_check() == 'PreDiabetic'

def test_fg_diabetic():
    p = GD_risk(130, 130)
    assert p.FG_check() == 'Diabetic'

def test_pmg_normal():
    p = GD_risk(95, 120)
    assert p.PMG_check() == 'Normal'

def test_pmg_prediabetic():
    p = GD_risk(95, 150)
    assert p.PMG_check() == 'PreDiabetic'

def test_pmg_diabetic():
    p = GD_risk(95, 210)
    assert p.PMG_check() == 'Diabetic'

def test_combined_normal():
    p = GD_risk(95, 120)
    assert p.combined_risk() == 'Normal'

def test_combined_prediabetic():
    p = GD_risk(110, 150)
    assert p.combined_risk() == 'PreDiabetic'

def test_combined_diabetic_one_side():
    # FG diabetic, PMG prediabetic → final should be Diabetic
    p = GD_risk(130, 150)
    assert p.combined_risk() == 'Diabetic'

def test_combined_diabetic_both():
    p = GD_risk(140, 210)
    assert p.combined_risk() == 'Diabetic'


# ---------- PK tests ----------
def test_warfarin_vd():
    p = PK_Dosage(70, 40, 2.0, 'Warfarin')
    assert round(p.vd(), 2) == 9.80

def test_warfarin_loading_dose():
    p = PK_Dosage(70, 40, 2.0, 'Warfarin')
    assert round(p.ld(), 2) == 19.60

def test_warfarin_maintenance_dose():
    p = PK_Dosage(70, 40, 2.0, 'Warfarin')
    assert round(p.md(), 2) == 4.07

def test_warfarin_steady_state():
    p = PK_Dosage(70, 40, 2.0, 'Warfarin')
    assert round(p.steady_state(), 1) == 200.0

def test_digoxin_vd():
    # 55 kg × 7.0 L/kg = 385 L
    p = PK_Dosage(55, 30, 0.5, 'Digoxin')
    assert round(p.vd(), 1) == 385.0