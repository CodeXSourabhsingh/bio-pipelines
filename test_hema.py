from Blood_V2 import Blood_group
from Blood_CBC_V2 import CBC_Analyzer
from rh_tools import rh_check

def test_rh_first_pregnancy():
    assert rh_check('-', '+', '1') == 'Monitor - first pregnancy, no antibodies yet'

def test_rh_sensitized():
    assert rh_check('-', '+', '2') == 'High risk - HDFN'

def test_rh_mother_positive():
    assert rh_check('+', '+', '2') == 'No risk'

def test_rh_baby_negative():
    assert rh_check('-', '-', '3') == 'No risk'

def test_universal_donor():
    assert len(Blood_group('O-').can_donate_to()) == 8

def test_universal_recipient():
    assert len(Blood_group('AB+').can_receive_from()) == 8

def test_rh_neg_recipient_blocks_rh_pos_donor():
    receivers = Blood_group('A-').can_receive_from()
    assert 'A+' not in receivers
    assert 'O+' not in receivers

def test_hb_male_exact_low():
    p = CBC_Analyzer('M', 13.5, 7.0, 250)
    assert 'Normal' in p.hb_check()

def test_hb_male_just_below():
    p = CBC_Analyzer('M', 13.4, 7.0, 250)
    assert 'Anemia' in p.hb_check()

def test_hb_female_exact_low():
    p = CBC_Analyzer('F', 12.0, 7.0, 250)
    assert 'Normal' in p.hb_check()
