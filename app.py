import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import time

# --- CONFIGURATION ---
st.set_page_config(
    page_title="TCI Staff Training",
    page_icon="🛡️",
    layout="wide",  # Wide mode for better readability
    initial_sidebar_state="expanded"
)

# --- SCROLL TO TOP LOGIC ---
def scroll_to_top():
    """Injects JS to scroll the page to the top."""
    js = """
    <script>
        var body = window.parent.document.querySelector('[data-testid="stAppViewContainer"]');
        if (body) { body.scrollTop = 0; }
        window.scrollTo(0, 0);
    </script>
    """
    components.html(js, height=0)

if "scroll_needed" in st.session_state and st.session_state.scroll_needed:
    scroll_to_top()
    st.session_state.scroll_needed = False

# --- API KEY SETUP ---
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    api_key = st.sidebar.text_input("Enter Google API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.sidebar.error("⚠️ API Key missing.")

# --- SESSION STATE ---
if "module" not in st.session_state:
    st.session_state.module = 1

# --- AI FUNCTIONS ---
def get_ai_feedback(user_response, scenario_context, correct_concept):
    if not api_key: return "⚠️ AI features disabled."
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        prompt = f"""
        You are an expert, encouraging TCI (Therapeutic Crisis Intervention) Master Trainer.
        
        Context: {scenario_context}
        User's Answer: "{user_response}"
        Target Concept: {correct_concept}
        
        Task: Provide feedback in this markdown format:
        **✅ What you did well:** (Specific praise)
        **🌱 For next time:** (Correction or refinement based strictly on TCI)
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

def ask_tci_bot(question):
    if not api_key: return "⚠️ Please enter an API Key."
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        prompt = f"""
        You are a helpful TCI Tutor. Answer this question based on TCI principles: "{question}"
        Structure:
        1. Direct Answer/Definition.
        2. "Why it matters" (Trauma context).
        3. Example/Application.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

# --- SIDEBAR NAVIGATION & TOOLS ---
with st.sidebar:
    st.header("🛡️ TCI Navigator")
    
    # Progress Bar
    progress_percent = st.session_state.module / 9
    st.progress(progress_percent)
    st.caption(f"Module {st.session_state.module} of 9")
    
    # Navigation Buttons
    st.markdown("### Quick Links")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.module = 1
            st.session_state.scroll_needed = True
            st.rerun()
    with col2:
        if st.button("📚 Study Guide", use_container_width=True):
            st.session_state.module = 7
            st.session_state.scroll_needed = True
            st.rerun()

    st.divider()
    
    # AI Chat
    st.subheader("💬 Ask the Expert")
    with st.expander("Ask a TCI Question", expanded=False):
        with st.form(key="sidebar_qa"):
            user_q = st.text_input("Question:", placeholder="e.g., What is the 'Spark'?")
            submit_q = st.form_submit_button("Ask AI")
        
        if submit_q and user_q:
            with st.spinner("Consulting manual..."):
                answer = ask_tci_bot(user_q)
                st.markdown(f"**Answer:**\n\n{answer}")

# --- MAIN CONTENT ---

# HEADER
st.title("Therapeutic Crisis Intervention (TCI) Certification")
st.markdown("---")

# ==========================================
# MODULE 1: CRISIS PREVENTION
# ==========================================
if st.session_state.module == 1:
    st.subheader("Module 1: Crisis Prevention & The Milieu")
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown("### 1.1 The Trauma-Informed Approach")
        st.write("""
        The foundation of TCI is empathy. We shift from asking *"What is wrong with this child?"* to *"What happened to this child?"*
        
        * **Pain-Based Behavior:** Behaviors like aggression, withdrawal, or defiance are often attempts to cope with pain.
        * **Goal:** Respond to the *feeling*, not just the behavior.
        """)
        
        st.info("""
        **🧠 The Triune Brain Model:**
        1.  **Thinking Brain (Neocortex):** Language, logic. (Offline during stress).
        2.  **Emotional Brain (Limbic):** The alarm system (Amygdala).
        3.  **Survival Brain (Brain Stem):** **Fight, Flight, or Freeze.**
        """)

        with st.expander("💡 Pro Tip: The 5 Spaces of the Milieu"):
            st.write("To prevent crises, we manage the environment (Milieu):")
            st.write("1. **Ideological:** Our values (Learning > Control).")
            st.write("2. **Physical:** Lighting, noise, clutter, safety.")
            st.write("3. **Cultural:** Celebrating identity.")
            st.write("4. **Social:** Routines and relationships.")
            st.write("5. **Emotional:** Emotional competence.")

    with col2:
        st.success("### 🧠 Scenario Practice")
        st.write("**Situation:** 10-year-old Marcus flips a chair because you asked him to stop playing. He screams 'I hate you!' and runs to the corner, curling into a ball.")
        
        with st.expander("Need a hint?"):
            st.write("Look at the Brain Model. Is Marcus thinking logically, or is he in survival mode?")

        with st.form("mod1_form"):
            ans1 = st.text_area("Using the Triune Brain model, explain Marcus's state. Is he just being 'bad'?", height=150)
            submit1 = st.form_submit_button("Get Feedback")
        
        if submit1 and ans1:
            with st.spinner("Trainer analyzing..."):
                st.markdown(get_ai_feedback(ans1, "Child flips chair/curls in ball.", "Survival Brain (Fight/Flight/Freeze) & Pain-Based Behavior"))

    st.divider()
    if st.button("Complete Module 1 & Continue 👉"):
        st.session_state.module = 2
        st.session_state.scroll_needed = True
        st.rerun()

# ==========================================
# MODULE 2: UNDERSTANDING CRISIS
# ==========================================
elif st.session_state.module == 2:
    st.subheader("Module 2: Understanding the Crisis")
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown("### 2.1 The Stress Model of Crisis")
        st.write("A crisis isn't an event; it's a process. If we catch it early, we can avoid the explosion.")
        st.markdown("""
        1.  **Baseline:** Normal functioning (may still be anxious).
        2.  **Trigger:** The spark (internal/external).
        3.  **Escalation:** Agitation. *Intervene here!*
        4.  **Outburst:** Violence. Survival mode.
        5.  **Recovery:** Return to calm.
        """)
        
        st.warning("""
        **The Two Goals of Crisis Intervention:**
        1.  **SUPPORT:** Reduce stress and risk immediately.
        2.  **TEACH:** Help children learn better coping skills.
        """)

        with st.expander("⚠️ Common Pitfall: The 4 Questions"):
            st.write("Before you act, you MUST ask yourself:")
            st.markdown("1. What am I feeling now? *(Self-regulation)*")
            st.markdown("2. What does the child feel, need, or want?")
            st.markdown("3. How is the environment affecting this?")
            st.markdown("4. How do I best respond?")

    with col2:
        st.success("### 🧠 Scenario Practice")
        st.write("**Situation:** Sarah fails a test (Trigger). She is now slamming her book and pacing (Escalation). She has NOT attacked anyone.")
        
        with st.expander("Need a hint?"):
            st.write("Look at the 'Two Goals'. Is this the time to Teach a lesson, or Support her?")

        with st.form("mod2_form"):
            ans2 = st.text_area("According to the 'Two Goals', what is your primary job right now?", height=150)
            submit2 = st.form_submit_button("Get Feedback")
        
        if submit2 and ans2:
            with st.spinner("Trainer analyzing..."):
                st.markdown(get_ai_feedback(ans2, "Child escalating but not violent.", "Support: Reduce stress/risk. Teaching happens later."))

    st.divider()
    if st.button("Complete Module 2 & Continue 👉"):
        st.session_state.module = 3
        st.session_state.scroll_needed = True
        st.rerun()

# ==========================================
# MODULE 3: DE-ESCALATION
# ==========================================
elif st.session_state.module == 3:
    st.subheader("Module 3: De-Escalating the Crisis")
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown("### 3.1 The Toolkit")
        st.write("We use these skills in the Escalation Phase to prevent an Outburst.")
        st.markdown("""
        * **Active Listening:** Validating feelings ("You seem angry").
        * **Behavior Support Techniques:**
            * *Hurdle Help:* Assisting with a frustrating task.
            * *Prompting:* Gentle reminders.
            * *Redirection:* Changing the focus.
            * *Proximity:* Standing near for support.
        """)
        
        st.error("""
        **Avoiding Power Struggles:**
        When a child says "Make me!", do not pull back.
        **DROP THE ROPE:** Listen, Validate, Give Choices.
        """)

    with col2:
        st.success("### 🧠 Scenario Practice")
        st.write("**Situation:** You tell Jason to clean his room. He yells 'Make me!' You feel your own anger rising.")
        
        with st.expander("Need a hint?"):
            st.write("If you argue, you join the Power Struggle. How do you disengage?")

        with st.form("mod3_form"):
            ans3 = st.text_area("How do you 'Drop the Rope' here?", height=150)
            submit3 = st.form_submit_button("Get Feedback")
        
        if submit3 and ans3:
            with st.spinner("Trainer analyzing..."):
                st.markdown(get_ai_feedback(ans3, "Child challenges authority.", "Drop the rope. Validate feelings, give choices, step back."))

    st.divider()
    if st.button("Complete Module 3 & Continue 👉"):
        st.session_state.module = 4
        st.session_state.scroll_needed = True
        st.rerun()

# ==========================================
# MODULE 4: MANAGING THE OUTBURST
# ==========================================
elif st.session_state.module == 4:
    st.subheader("Module 4: Managing the Crisis (Outburst)")
    
    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.markdown("### 4.1 When words fail...")
        st.write("In the Outburst phase, the child is in survival mode. They are reading your body, not your words.")
        
        st.info("""
        **Crisis Co-Regulation (What YOU do):**
        1.  **THINK:** Ask the 4 Questions.
        2.  **DO:** Deep breath. Step back. Open stance. Hands visible.
        3.  **SAY:** Very little. "I can see you are upset."
        """)
        
        with st.expander("The Elements of Violence"):
            st.write("To stop violence, remove one of these:")
            st.write("* **The Spark:** Triggers (often us).")
            st.write("* **The Target:** Who they are attacking.")
            st.write("* **The Weapon:** Objects.")
            st.write("* **Stress:** The pressure.")

    with col2:
        st.success("### 🧠 Scenario Practice")
        st.write("**Situation:** The child is screaming and looking for something to throw. You are the target.")
        
        with st.form("mod4_form"):
            ans4 = st.text_area("Describe your exact body language and physical action.", height=150)
            submit4 = st.form_submit_button("Get Feedback")
        
        if submit4 and ans4:
            with st.spinner("Trainer analyzing..."):
                st.markdown(get_ai_feedback(ans4, "Child in outburst, user is target.", "Remove the target (step away). Open stance. Hands visible."))

    st.divider()
    if st.button("Complete Module 4 & Continue 👉"):
        st.session_state.module = 5
        st.session_state.scroll_needed = True
        st.rerun()

# ==========================================
# MODULE 5: RECOVERY & LSI
# ==========================================
elif st.session_state.module == 5:
    st.subheader("Module 5: Recovery & The LSI")
    
    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.markdown("### 5.1 The Life Space Interview")
        st.write("Once the child is calm, we use the LSI to teach new skills.")
        
        st.info("""
        **I ESCAPE Steps:**
        * **I** - Identify time/place.
        * **E** - Explore child's view.
        * **S** - Summarize feelings/content.
        * **C** - Connect trigger to behavior.
        * **A** - Alternative responses.
        * **P** - Plan/Practice.
        * **E** - Enter back to routine.
        """)

    with col2:
        st.success("### 🧠 Scenario Practice")
        st.write("**Situation:** The child is calm. You are doing the LSI. You just Summarized what happened. What is next?")
        
        with st.form("mod5_form"):
            ans5 = st.text_area("What is the 'C' step? Why is it important?", height=150)
            submit5 = st.form_submit_button("Get Feedback")
        
        if submit5 and ans5:
            with st.spinner("Trainer analyzing..."):
                st.markdown(get_ai_feedback(ans5, "LSI step C.", "Connect. Connect trigger -> feeling -> behavior."))

    st.divider()
    if st.button("Complete Module 5 & Continue 👉"):
        st.session_state.module = 6
        st.session_state.scroll_needed = True
        st.rerun()

# ==========================================
# MODULE 6: SAFETY INTERVENTIONS
# ==========================================
elif st.session_state.module == 6:
    st.subheader("Module 6: Safety Interventions")
    
    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.error("""
        **⚠️ WARNING: HIGH RISK**
        Physical restraint is ONLY used for **imminent safety risk** (harm to self/others).
        It is NEVER used for compliance or punishment.
        """)
        
        st.markdown("### 6.1 Critical Safety Rules")
        st.write("""
        * **Positional Asphyxia:** A fatal inability to breathe caused by body position.
        * **NEVER** put weight on a child's chest, back, or stomach.
        * **NEVER** ignore "I can't breathe."
        * **Monitor:** Skin color, respiration, consciousness.
        """)

    with col2:
        st.success("### 🧠 Scenario Practice")
        st.write("**Situation:** You are restraining a child. He says 'I can't breathe.' You think he might be lying to get free.")
        
        with st.form("mod6_form"):
            ans6 = st.text_area("What is the ONLY acceptable response?", height=150)
            submit6 = st.form_submit_button("Get Feedback")
        
        if submit6 and ans6:
            with st.spinner("Trainer analyzing..."):
                st.markdown(get_ai_feedback(ans6, "Child says 'I can't breathe'.", "Release immediately or adjust position. Never ignore."))

    st.divider()
    if st.button("Complete Module 6 & Continue 👉"):
        st.session_state.module = 7
        st.session_state.scroll_needed = True
        st.rerun()

# ==========================================
# MODULE 7: STUDY GUIDE
# ==========================================
elif st.session_state.module == 7:
    st.header("📚 Comprehensive Study Guide")
    st.write("Review these cheat sheets before taking the final exam.")

    tab1, tab2, tab3, tab4 = st.tabs(["🧠 Prevention", "🛑 De-Escalation", "🔥 Crisis/Safety", "🌱 Recovery"])

    with tab1:
        st.markdown("""
        ### The Triune Brain
        1.  **Thinking Brain:** Reasoning (Offline during stress).
        2.  **Emotional Brain:** Danger detection (Amygdala).
        3.  **Survival Brain:** Fight, Flight, Freeze.
        
        ### The 5 Spaces
        Ideological, Physical, Cultural, Social, Emotional.
        """)

    with tab2:
        st.markdown("""
        ### Behavior Support Techniques
        *Prompting, Caring Gesture, Hurdle Help, Redirection, Proximity, Directive Statements, Time Away.*
        
        ### Power Struggles
        **Strategy:** Drop the Rope. (Validate, Give Choices, Remove Audience).
        """)

    with tab3:
        st.markdown("""
        ### Crisis Co-Regulation
        * **Think:** 4 Questions.
        * **Do:** Deep breath, Step back.
        * **Say:** Very little.
        
        ### Safety Interventions
        * **Criteria:** Imminent risk of harm only.
        * **Fatal Risk:** Positional Asphyxia.
        * **Rule:** Never put weight on the torso. Never ignore "I can't breathe."
        """)

    with tab4:
        st.markdown("""
        ### The LSI (I ESCAPE)
        * **I**dentify time/place.
        * **E**xplore.
        * **S**ummarize.
        * **C**onnect (Trigger -> Behavior).
        * **A**lternative responses.
        * **P**lan/Practice.
        * **E**nter back.
        """)

    st.divider()
    if st.button("Ready for Exam 👉"):
        st.session_state.module = 8
        st.session_state.scroll_needed = True
        st.rerun()

# ==========================================
# MODULE 8: FINAL EXAM
# ==========================================
elif st.session_state.module == 8:
    st.header("📝 Final Certification Exam")
    st.write("Answer all 20 questions. Passing score: 80% (16/20).")
    
    with st.form("exam_form"):
        q1 = st.radio("1. What is the primary goal of TCI?", ["Enforce discipline", "Reduce high-risk interventions", "Eliminate emotions"])
        q2 = st.radio("2. Pain-based behavior is often:", ["Willful bad behavior", "An expression of trauma/distress", "Laziness"])
        q3 = st.radio("3. Which brain part controls Fight/Flight/Freeze?", ["Thinking Brain", "Emotional Brain", "Survival Brain"])
        q4 = st.radio("4. Anything that makes challenging behavior more/less likely is a:", ["Setting Condition", "Trigger", "Crisis"])
        q5 = st.radio("5. When is a child most likely to be violent?", ["Escalation", "Outburst", "Recovery"])
        q6 = st.radio("6. The two goals of crisis intervention are:", ["Control & Punish", "Support & Teach", "Restrain & Isolate"])
        q7 = st.radio("7. First question to ask yourself in crisis:", ["What did the child do?", "What am I feeling now?", "Who started it?"])
        q8 = st.radio("8. Nonverbal active listening includes:", ["Asking 'Why?'", "Silence/Nods", "Lecturing"])
        q9 = st.radio("9. Helping a child start a frustrating task is:", ["Prompting", "Hurdle Help", "Redirection"])
        q10 = st.radio("10. Best strategy for a power struggle?", ["Win the argument", "Drop the rope", "Threaten consequences"])
        q11 = st.radio("11. Eye contact during an outburst should be:", ["Staring", "Avoided", "Intermittent/Non-threatening"])
        q12 = st.radio("12. Which is an element of violence?", ["The Spark", "The Target", "The Weapon", "All of the above"])
        q13 = st.radio("13. First step of Crisis Co-Regulation?", ["Step back", "Take a deep breath", "Give a command"])
        q14 = st.radio("14. 'C' in I ESCAPE stands for:", ["Control", "Connect trigger to behavior", "Call help"])
        q15 = st.radio("15. Goal of the LSI?", ["Return to normal/Teach skills", "Apologize", "Document"])
        q16 = st.radio("16. Use restraint ONLY when:", ["Disrespectful", "Imminent safety risk", "Refusing directions"])
        q17 = st.radio("17. Positional Asphyxia is:", ["Panic attack", "Fatal respiratory arrest due to position", "Hyperventilation"])
        q18 = st.radio("18. NEVER put weight on:", ["Arms", "Legs", "Chest/Back/Stomach"])
        q19 = st.radio("19. If child says 'I can't breathe':", ["Wait", "Ignore", "Release/Adjust immediately"])
        q20 = st.radio("20. Restraint ends when:", ["Child is no longer a danger", "Child promises to be good", "15 mins pass"])

        if st.form_submit_button("Submit Exam"):
            score = 0
            # Answer Key
            if q1 == "Reduce high-risk interventions": score += 1
            if q2 == "An expression of trauma/distress": score += 1
            if q3 == "Survival Brain": score += 1
            if q4 == "Setting Condition": score += 1
            if q5 == "Outburst": score += 1
            if q6 == "Support & Teach": score += 1
            if q7 == "What am I feeling now?": score += 1
            if q8 == "Silence/Nods": score += 1
            if q9 == "Hurdle Help": score += 1
            if q10 == "Drop the rope": score += 1
            if q11 == "Intermittent/Non-threatening": score += 1
            if q12 == "All of the above": score += 1
            if q13 == "Take a deep breath": score += 1
            if q14 == "Connect trigger to behavior": score += 1
            if q15 == "Return to normal/Teach skills": score += 1
            if q16 == "Imminent safety risk": score += 1
            if q17 == "Fatal respiratory arrest due to position": score += 1
            if q18 == "Chest/Back/Stomach": score += 1
            if q19 == "Release/Adjust immediately": score += 1
            if q20 == "Child is no longer a danger": score += 1
            
            st.session_state.final_score = score
            if score >= 16:
                st.session_state.module = 9
                st.session_state.scroll_needed = True
                st.rerun()
            else:
                st.error(f"Score: {score}/20. You need 16 to pass. Please review.")

# ==========================================
# MODULE 9: COMPLETION
# ==========================================
elif st.session_state.module == 9:
    st.balloons()
    st.header("🎓 Certificate of Completion")
    st.success(f"Certified TCI Trained Staff | Score: {st.session_state.final_score}/20")
    
    st.markdown("""
    **This certifies that the user has demonstrated knowledge in:**
    * ✅ Trauma-Informed Crisis Prevention
    * ✅ De-Escalation & Behavior Support
    * ✅ Crisis Co-Regulation & LSI
    * ✅ Safety Interventions & Risk Management
    """)
    
    st.info("🖨️ Please print this page or take a screenshot for your records.")
    
    if st.button("Start Over"):
        st.session_state.module = 1
        st.session_state.scroll_needed = True
        st.rerun()
