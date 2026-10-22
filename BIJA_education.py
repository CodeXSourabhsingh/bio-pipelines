
print("--- BIJA: Fertility Education Tool ---")
x = input('Who is using this tool today? (Male, Female, Both): ').upper().strip()

if x == 'MALE':
    print("\n--- Male Fertility Questions ---")
    Mq1 = int(input('Enter your age: '))
    Mq2 = input('How long have you been trying?: ') # Fixed: Removed int() here
    Mq3 = input('Do you have any children from a previous relationship? (Yes/No): ').upper().strip()
    Mq4 = input('Have you ever had a hernia surgery, a varicocele, or an undescended testicle? (Yes/No): ').upper().strip()
    Mq5 = input('Have you ever had a semen analysis done? (Yes/No): ').upper().strip()

    print("\n--- YOUR FERTILITY EDUCATION SUMMARY ---")
    print("Male factors account for nearly 40-50% of infertility cases. Do not assume the issue is only with your partner.")
    
    if Mq4 == 'YES':
        print("- Because you mentioned a history of hernia, varicocele, or undescended testicle, it is highly recommended that you see a urologist. These are physical blockages that can often be fixed.")
    
    if Mq5 == 'NO':
        print ("- Get a Semen Analysis. It is the fastest and cheapest test to rule out 50% of the puzzle.")
    else:

        print("- You have had a Semen analysis before. Please bring those results to your doctor to see if your numbers have changed.")
        
    print("\nACTION STEP: Book an appointment with a general practitioner or urologist for a semen analysis.")

    print("\n--- YOUR FERTILITY EDUCATION SUMMARY ---")

elif x == 'FEMALE':
    print("\n--- Female Fertility Questions ---")
    Fq1 = int(input('Enter your age: '))
    Fq2 = float(input('How long have you been trying (years)?: '))
    Fq3 = input('Are your menstrual cycles (regular/irregular/no cycle)?: ').upper().strip()
    Fq4 = input('Have you ever been diagnosed with PCOS, endometriosis, or blocked tubes? (Yes/No): ').upper().strip()
    Fq5 = input('Have you ever been pregnant before? (Yes/No): ').upper().strip()

    print("\n--- YOUR FERTILITY EDUCATION SUMMARY ---")
    
   
    if Fq3 == 'IRREGULAR' or Fq3 == 'NO CYCLE' or Fq3 == 'NOCYCLE':
        print("- Because your cycles are irregular, you may not be ovulating every month. This is very common (often related to PCOS) and is highly treatable.")
    
   
    if Fq4 == 'YES':
        print("- Because you have a known history (PCOS, Endometriosis, or blocked tubes), you should not wait to see a specialist. These conditions require specific medical interventions.")
    
   
    if Fq1 >= 35:
        print("- Because you are over 35, the clinical guideline is to see a doctor after 6 months of trying, rather than a full year, as egg quality and quantity decline faster after this age.")

    if (Fq1 >= 35 and Fq2 >= 0.5) or (Fq2 >= 1.0) or (Fq3 == 'IRREGULAR') or (Fq4 == 'YES'):
        
        print("- ACTION STEP: Ask your doctor for a Basic fertility panel. Specifically ask for:")
        print("  - AMH Blood Test (checks ovarian reserve)")
        print("  - Day 3 FSH (checks ovarian function)")
        print("  - Pelvic Ultrasound (checks follicle count)")
    else:
        print("- ACTION STEP: Keep tracking your cycle. If you don't conceive within a year, consult a doctor.")

else: 
    print("\n--- Both Partners Questions ---")
    
    print("\n[MALE PARTNER]")
    Mq1 = int(input('Enter MALE age: '))
    Mq2 = input('How long have you (as a couple) been trying?: ') 
    Mq3 = input('Does the male partner have any children from a previous relationship? (Yes/No): ').upper().strip()
    Mq4 = input('Has the male partner ever had a hernia surgery, varicocele, or undescended testicle? (Yes/No): ').upper().strip()
    Mq5 = input('Has the male partner ever had a semen analysis done? (Yes/No): ').upper().strip()

    print("\n[FEMALE PARTNER]")
    Fq1 = int(input('Enter FEMALE age: '))
    Fq3 = input('Are the female partner\'s cycles regular, irregular, or no cycle? ').upper().strip()
    Fq4 = input('Has the female partner ever been diagnosed with PCOS, endometriosis, or blocked tubes? (Yes/No): ').upper().strip()
    Fq5 = input('Has the female partner ever been pregnant before? (Yes/No): ').upper().strip()

    print("\n--- YOUR FERTILITY EDUCATION SUMMARY ---")
    print("Fertility is a two-person puzzle. You must check both sides.")
    
    print("\nFOR HIM:")
    if Mq5 == 'NO':
        print("- Get a Semen Analysis. It is the fastest and cheapest test to rule out 50% of the puzzle.")
    if Mq4 == 'YES':
        print("- See a urologist due to your medical history (hernia/varicocele).")
        
    print("\nFOR HER:")
    if Fq3 == 'IRREGULAR' or Fq3 == 'NO CYCLE' or Fq3 == 'NOCYCLE':
        print("- Bring up the irregular cycles to a gynecologist. This points to ovulation issues.")
    if Fq1 >= 35:
        print("- Book an appointment with a reproductive endocrinologist soon, as the female partner is over 35.")
        
    print("\nACTION STEP: Both of you should book an appointment with a fertility specialist (Reproductive Endocrinologist) together.")
    print("Bring these questions with you so you don't forget them in the doctor's office.")