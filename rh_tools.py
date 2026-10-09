
def rh_check(mother_rh, baby_rh, pregnancy_num):
    if mother_rh == '-' and baby_rh == '+':
        if pregnancy_num == '1':
            return 'Monitor - first pregnancy, no antibodies yet'
        else :
            return 'High risk - HDFN'
    return 'No risk'
    
