print("--- BIJA: Clinical Triage Engine ---")
print("Please enter the patient's lab results below.\n")

age = int(input('Enter age: '))
amh = float(input('Enter AMH (ng/ml): '))
fsh = float(input('Enter FSH (IU/L): '))
lh_fsh_ratio = float(input('Enter LH:FSH Ratio: '))
afc = float(input('Enter AFC: '))
tsh = float(input('Enter TSH (mIU/L)'))
prolactin = float(input('Enter prolactin (ng/ml):'))
cycle = input('Enter cycle (regular/irregular): ').upper().strip()

tube_blocked = input('Enter blocked tubes (yes/no): ').upper().strip()
genetic_carrier = input('Enter known genetic carrier (yes/no): ').upper().strip()

count = float(input('Enter sperm count(M/ml): '))
motility = float(input('Enter motility(%): '))
morphology = float(input('Enter morphology(%): '))
volume = float(input('Enter semen volume (mL): '))
ph = float(input('Enter semen pH: '))
varicocele = input('Obstruction / Varicocele (yes/no): ').upper().strip()

print("\n=============================================")
print("--- BIJA CLINICAL TRIAGE REPORT ---")
print("=============================================\n")

treatment =""
reason = ""
if genetic_carrier == 'YES':
    treatment = 'IVF + PGT'
    reason = 'Known genetic carrier status detected. require preimplantation genetic testing'
elif(tube_blocked == 'YES' or
     count < 15 or motility < 40 or morphology < 4 or volume < 1.4 or ph < 7.2 or varicocele == 'YES' or amh < 1.0 or fsh > 15 or afc < 5 or age >= 40):
    needs_icsi = (count < 15 or motility < 40 or morphology < 4 or volume < 1.4 or ph < 7.2 or varicocele == 'YES')
    if needs_icsi:
        treatment = 'IVF + ICSI'
        reason = 'Combined approach: Requires IVF (due to female/age factors) and ICSI (due to male factor).'
    else:
        treatment = 'Standard IVF'
        reason = 'Require IVF due to blocked tube, diminished ovarian reserve, or advanced maternal age.'
elif (lh_fsh_ratio > 2 or cycle == 'IRREGULAR' or tsh > 4.0 or tsh < 0.4 or prolactin > 25):
    treatment = 'IUI + Ovulation Induction'
    reason = 'Signs of ovulatory(PCOS,irregular cycle,thyroid issue, or high prolactin).'
    print('Escaltion path: Move to IVF after 3 failed IUI cycles.')
else:
    treatment = 'Standard IVF'
    reason = "All panels normal, but natural conception hasn't occured after 12 month"

print(f"RECOMMENDATION: {treatment}")
print(f"RECOMMENDATION {reason}")

print("\n=============================================")
print("--- ESTIMATED SUCCESS PROBABILITY ---")
print("=============================================\n")

ivf_probabilities = {'<35': '53.2%', '35-37': '39.9%', '38-40': '26.2%', '41-42': '13.2%', '>42': '4.1%'}
iui_probabilities = {'<35': '10% - 20%', '35-37': '8% - 15%', '38-40': '5% - 10%', '>40': '<5%'}
donor_egg_probability = '51.3% - 63.6%'

def get_age_group(age):
    if age < 35: return '<35'
    elif 35 <= age <= 37: return '35-37'
    elif 38 <= age <= 41: return '38-41'
    elif 41 <= age <= 42: return '41-42'
    else: return '>42'

age_group = get_age_group(age)

if treatment in ["IVF + ICSI", "Standard IVF", "IVF + PGT"]:
    prob = ivf_probabilities.get(age_group, 'N/A')
    print(f"Your chance of a live birth per cycle with {treatment} is approximately: {prob}")

elif treatment == "IUI + Ovulation Induction":
    prob = iui_probabilities.get(age_group, 'N/A')
    print(f"Your chance of a live birth per cycle with IUI is approximately: {prob}")

print("\nDISCLAIMER: These are population averages based on national data. Consult a reproductive endocrinologist.")