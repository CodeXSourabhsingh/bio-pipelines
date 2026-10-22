import streamlit as st
import matplotlib.pyplot as plt

try:
    from BIJA_MYSQL import insert_report
except ImportError:
    def insert_report(**kwargs): pass

st.set_page_config(page_title="BIJA Fertility Triage", layout="wide", page_icon="🩺")

st.title("🩺 BIJA: Clinical Fertility Triage")
st.markdown("""
> **Welcome to BIJA.** 
> 
> Talking about fertility can be stressful, and looking at lab numbers can feel cold. Before we ask you any questions, take a breath. There are no wrong answers here. This tool is private, anonymous, and built to help you understand your biology, not to judge it.
""")
st.divider()

tab1, tab2 = st.tabs(["📚 Patient Education", "📊 Clinical Calculation Engine"])

with tab1:
    st.header("Understand Your Options")
    
    st.info("""
    **If you don't have lab results yet, you are in the right place.** 
    Most people don't know their AMH or FSH until they ask for them. Let's look at your history first so we can build the exact list of questions you should ask your doctor.
    """)
    
    user_type = st.radio("Who is using this tool today?", ["👨 Male", "👩 Female", "👫 Both"], horizontal=True)
    
    if user_type == "👨 Male" or user_type == "👫 Both":
        with st.expander("🧬 Male Partner Questions", expanded=True):
            m_age = st.number_input("Male Age", min_value=18, max_value=60, value=30)
            m_trying = st.number_input("Years trying (Male)", min_value=0.0, value=1.0)
            m_varicocele = st.selectbox("History of hernia or varicocele?", ["No", "Yes"])
            m_semen = st.selectbox("Had a semen analysis?", ["No", "Yes"])
            
    if user_type == "👩 Female" or user_type == "👫 Both":
        with st.expander("🩸 Female Partner Questions", expanded=True):
            f_age_edu = st.number_input("Female Age", min_value=18, max_value=60, value=30)
            f_trying = st.number_input("Years trying (Female)", min_value=0.0, value=1.0)
            f_cycle = st.selectbox("Cycle", ["Regular", "Irregular", "No cycle"])
            f_history = st.selectbox("History of PCOS, Endometriosis, or blocked tubes?", ["No", "Yes"])
            f_pregnant = st.selectbox("Have you ever been pregnant before?", ["No", "Yes"])

    if st.button("Generate Education Plan", type="primary"):
        male_edu_text = ""
        female_edu_text = ""
        both_edu_text = ""

        if user_type == "👨 Male" or user_type == "👫 Both":
            if m_varicocele == "Yes":
                male_edu_text += "- Urology Consult: A varicocele (enlarged veins) or hernia can impair sperm production and may require surgical correction. You should see a urologist for evaluation.\n"
            if m_semen == "No":
                male_edu_text += "- Immediate Next Step: Get a Semen Analysis. It is the fastest, least invasive test to rule out 50% of the fertility puzzle.\n"
                
        if user_type == "👩 Female" or user_type == "👫 Both":
            if f_cycle in ["Irregular", "No cycle"]:
                female_edu_text += "- Ovulation Check: Irregular cycles mean you may not be ovulating every month. This is often related to PCOS and is highly treatable.\n"
            if f_history == "Yes":
                female_edu_text += "- Specialist Referral: Because you have a known history (PCOS, Endometriosis, or blocked tubes), you should not wait to see a reproductive specialist.\n"
            if f_age_edu >= 35:
                female_edu_text += "- Age Guideline: Because you are over 35, the clinical guideline is to see a doctor after 6 months of trying, rather than a full year.\n"
            
            if (f_age_edu >= 35 and f_trying >= 0.5) or (f_trying >= 1.0) or (f_cycle in ["Irregular", "No cycle"]) or (f_history == "Yes"):
                female_edu_text += "- ACTION STEP: Ask your doctor for a Basic fertility panel. Specifically ask for: AMH, Day 3 FSH, and a Pelvic Ultrasound.\n"
            else:
                female_edu_text += "- Next Step: Keep tracking your cycle. If you don't conceive within a year, consult a doctor.\n"

        if user_type == "👫 Both":
            both_edu_text = "Combined Action Plan: Both partners should book an appointment with a reproductive endocrinologist together and bring these questions."

        st.session_state.edu_user_type = user_type
        st.session_state.edu_male = male_edu_text
        st.session_state.edu_female = female_edu_text
        st.session_state.edu_both = both_edu_text

        try:
            insert_report(mode=user_type, male_edu=male_edu_text, female_edu=female_edu_text, both_edu=both_edu_text)
        except Exception:
            pass

    if "edu_user_type" in st.session_state:
        st.divider()
        u_type = st.session_state.edu_user_type
        
        if u_type == "👨 Male" or u_type == "👫 Both":
            st.subheader("🧬 Male Action Plan")
            if st.session_state.edu_male:
                st.warning(st.session_state.edu_male)
            else:
                st.success("✅ No immediate male factor red flags detected from your history.")
                
        if u_type == "👩 Female" or u_type == "👫 Both":
            st.subheader("🩸 Female Action Plan")
            if st.session_state.edu_female:
                st.warning(st.session_state.edu_female)
            else:
                st.success("✅ No immediate female factor red flags detected from your history.")

        if u_type == "👫 Both":
            st.subheader("🤝 Combined Action Plan")
            st.info(st.session_state.edu_both)

        st.divider()
        st.markdown("""
        *Remember: You are not a lab report. You are not a statistic. This information is to help you walk into your doctor's office with confidence and vocabulary. The next step is a conversation with a professional who can look at you, not just your numbers.*
        """)

with tab2:
    st.header("Clinical Triage Engine")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🩸 Female Panel")
        f_age_calc = st.number_input("Female Age (Calc)", min_value=18, max_value=55, value=32)
        amh = st.number_input("AMH (ng/mL)", min_value=0.0, value=2.0, step=0.1)
        fsh = st.number_input("FSH (IU/L)", min_value=0.0, value=6.0, step=0.1)
        lh_fsh = st.number_input("LH:FSH Ratio", min_value=0.0, value=1.5, step=0.1)
        afc = st.number_input("Antral Follicle Count (AFC)", min_value=0, value=15)
        tsh = st.number_input("TSH (mIU/L)", min_value=0.0, value=2.0, step=0.1)
        prolactin = st.number_input("Prolactin (ng/mL)", min_value=0.0, value=10.0, step=0.1)
        cycle_calc = st.selectbox("Cycle (Calc)", ["Regular", "Irregular"])
        tube_blocked = st.selectbox("Blocked tubes?", ["No", "Yes"])
        genetic = st.selectbox("Known genetic carrier?", ["No", "Yes"])
        
    with col2:
        st.subheader("🧬 Male Panel")
        count = st.number_input("Sperm count (M/mL)", min_value=0.0, value=50.0, step=1.0)
        motility = st.number_input("Motility (%)", min_value=0.0, value=60.0, step=1.0)
        morphology = st.number_input("Morphology (%)", min_value=0.0, value=10.0, step=1.0)
        volume = st.number_input("Semen Volume (mL)", min_value=0.0, value=3.0, step=0.1)
        ph = st.number_input("Semen pH", min_value=0.0, value=7.5, step=0.1)
        varicocele_calc = st.selectbox("Obstruction / Varicocele? (Calc)", ["No", "Yes"])

    st.divider()
    
    if st.button("🩺 Generate Clinical Report", type="primary"):
        
        if genetic == "Yes":
            treatment = "IVF + PGT"
            reason = "Known genetic carrier status detected. Requires Preimplantation Genetic Testing."
        elif (tube_blocked == "Yes" or count < 15 or motility < 40 or morphology < 4 or volume < 1.4 or ph < 7.2 or varicocele_calc == "Yes" or amh < 1.0 or fsh > 15 or afc < 5 or f_age_calc >= 40):
            needs_icsi = (count < 15 or motility < 40 or morphology < 4 or volume < 1.4 or ph < 7.2 or varicocele_calc == "Yes")
            if needs_icsi:
                treatment = "IVF + ICSI"
                reason = "Combined approach: Requires IVF (due to female/age factors) and ICSI (due to male factor)."
            else:
                treatment = "Standard IVF"
                reason = "Requires IVF due to blocked tubes, diminished ovarian reserve, or advanced maternal age."
        elif (lh_fsh > 2 or cycle_calc == "Irregular" or tsh > 4.0 or tsh < 0.4 or prolactin > 25):
            treatment = "IUI + Ovulation Induction"
            reason = "Signs of ovulatory dysfunction (PCOS, irregular cycles, thyroid issue, or high prolactin)."
        else:
            treatment = "Standard IVF"
            reason = "All panels normal, but natural conception hasn't occurred after 12 months."

        st.session_state.treatment = treatment
        st.session_state.reason = reason
        st.session_state.amh_val = amh
        st.session_state.fsh_val = fsh
        st.session_state.lh_val = round(lh_fsh * fsh, 1)
        st.session_state.f_age = f_age_calc

        try:
            insert_report(mode="Calculation", calc_result=treatment)
        except Exception:
            pass

    if "treatment" in st.session_state:
        
        st.subheader("📋 Diagnostic Output")
        
        res_col1, res_col2 = st.columns([1, 2])
        
        with res_col1:
            st.metric(label="Recommended Treatment", value=st.session_state.treatment)
        with res_col2:
            st.info(f"**Clinical Reason:** {st.session_state.reason}")

        st.divider()
        
        st.subheader("📈 Hormonal Profile")
        
        fig, axes = plt.subplots(3, 1, figsize=(10, 7))
        plt.style.use('dark_background')
        
        ax1 = axes[0]
        ax1.axvspan(0, 1.0, color='#ff4b4b', alpha=0.3)
        ax1.axvspan(1.0, 4.0, color='#2ecc71', alpha=0.3)
        ax1.axvspan(4.0, 8.0, color='#f1c40f', alpha=0.3)
        ax1.axvline(st.session_state.amh_val, color='white', linewidth=4)
        ax1.set_xlim(0, 8)
        ax1.set_yticks([])
        ax1.set_title(f"AMH (ng/mL) — Patient Value: {st.session_state.amh_val}", fontweight='bold')
        
        ax1.text(0.5, 0.5, 'Low Reserve', ha='center', va='center', fontweight='bold', color='white')
        ax1.text(2.5, 0.5, 'Normal', ha='center', va='center', fontweight='bold', color='white')
        ax1.text(6.0, 0.5, 'PCOS Risk', ha='center', va='center', fontweight='bold', color='black')

        ax2 = axes[1]
        ax2.axvspan(0, 3.5, color='#f1c40f', alpha=0.3)
        ax2.axvspan(3.5, 12.5, color='#2ecc71', alpha=0.3)
        ax2.axvspan(12.5, 25, color='#ff4b4b', alpha=0.3)
        ax2.axvline(st.session_state.fsh_val, color='white', linewidth=4)
        ax2.set_xlim(0, 25)
        ax2.set_yticks([])
        ax2.set_title(f"FSH (mIU/mL) — Patient Value: {st.session_state.fsh_val}", fontweight='bold')
        
        ax2.text(1.75, 0.5, 'Low', ha='center', va='center', fontweight='bold', color='black')
        ax2.text(8.0, 0.5, 'Normal', ha='center', va='center', fontweight='bold', color='white')
        ax2.text(18.5, 0.5, 'High (DOR Risk)', ha='center', va='center', fontweight='bold', color='white')

        ax3 = axes[2]
        ax3.axvspan(0, 2.4, color='#f1c40f', alpha=0.3)
        ax3.axvspan(2.4, 12.6, color='#2ecc71', alpha=0.3)
        ax3.axvspan(12.6, 25, color='#ff4b4b', alpha=0.3)
        ax3.axvline(st.session_state.lh_val, color='white', linewidth=4)
        ax3.set_xlim(0, 25)
        ax3.set_yticks([])
        ax3.set_title(f"LH (mIU/mL) — Patient Value: {st.session_state.lh_val}", fontweight='bold')
        
        ax3.text(1.2, 0.5, 'Low', ha='center', va='center', fontweight='bold', color='black')
        ax3.text(7.5, 0.5, 'Normal', ha='center', va='center', fontweight='bold', color='white')
        ax3.text(18.5, 0.5, 'High (PCOS Risk)', ha='center', va='center', fontweight='bold', color='white')

        plt.tight_layout()
        st.pyplot(fig)
        
        st.divider()
        
        st.subheader("📊 Estimated Success Probability")
        
        ivf_probabilities = {'<35': '53.2%', '35-37': '39.9%', '38-40': '26.2%', '41-42': '13.2%', '>42': '4.1%'}
        iui_probabilities = {'<35': '10% - 20%', '35-37': '8% - 15%', '38-40': '5% - 10%', '>40': '<5%'}
        
        def get_age_group(a):
            if a < 35: return '<35'
            elif 35 <= a <= 37: return '35-37'
            elif 38 <= a <= 40: return '38-40'
            elif 41 <= a <= 42: return '41-42'
            else: return '>42'

        age_group = get_age_group(st.session_state.f_age)
        current_treatment = st.session_state.treatment

        if current_treatment in ["IVF + ICSI", "Standard IVF", "IVF + PGT"]:
            prob = ivf_probabilities.get(age_group, 'N/A')
            st.success(f"**Live Birth Rate:** Estimated chance of live birth per cycle with {current_treatment} is **{prob}**")
        elif current_treatment == "IUI + Ovulation Induction":
            prob = iui_probabilities.get(age_group, 'N/A')
            st.success(f"**Live Birth Rate:** Estimated chance of live birth per cycle with IUI is **{prob}**")

        st.caption("⚠️ **DISCLAIMER:** These are population averages based on national data (SART/CDC). This tool is for triage and education only. It is not a medical prescription. Consult a reproductive endocrinologist for personalized medical advice.")