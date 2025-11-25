import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai

# --- CONFIGURATION ---
st.set_page_config(page_title="TCI Staff Training", page_icon="🛡️", layout="wide")

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
    st.warning("⚠️ API Key missing. Please add it to secrets.toml or the sidebar.")

# --- SESSION STATE ---
if "module" not in st.session_state:
    st.session_state.module = 1

# --- AI FEEDBACK FUNCTION ---
def get_ai_feedback(user_response, scenario_context, correct_concept):
    if not api_key:
        return "⚠️ AI features disabled."
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        prompt = f"""
        You are an expert TCI instructor.
        Scenario: {scenario_context}
        User Answer: "{user_response}"
        Task: Compare answer to TCI concept '{correct_concept}'. 
        Provide specific, encouraging feedback. Correct any punitive or non-therapeutic language.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

def ask_tci_bot(question):
    """General Q&A logic for the sidebar bot."""
    if not api_key: return "⚠️ Please enter an API Key."
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        prompt = f"""
        You are a helpful TCI (Therapeutic Crisis Intervention) Tutor.
        The user has a question about the material.
        User Question: "{question}"
        
        Task: Provide a detailed, comprehensive answer based STRICTLY on TCI principles.
        1. Define the concept clearly.
        2. Explain the 'Why': How does this help a traumatized child?
        3. Provide a practical example of how this looks in action.
        4. Structure your answer with bullet points or bold text for readability.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

# --- SIDEBAR: NAVIGATION & CHAT ---
with st.sidebar:
    st.header("📍 Menu")
    
    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button("🏠 Start"):
            st.session_state.module = 1
            st.session_state.scroll_needed = True
            st.rerun()
    with col_nav2:
        if st.button("📚 Study Guide"):
            st.session_state.module = 7
            st.session_state.scroll_needed = True
            st.rerun()
            
    st.divider()
    
    st.subheader("💬 AI Tutor Chat")
    with st.expander("Have a question?", expanded=False):
        st.write("Ask anything about TCI definitions, concepts, or rules.")
        
        with st.form(key="sidebar_qa_form"):
            user_q = st.text_input("Type question & hit Enter:")
            submit_q = st.form_submit_button("Ask AI")
            
        if submit_q and user_q:
            with st.spinner("Thinking..."):
                answer = ask_tci_bot(user_q)
                st.markdown(f"**Answer:**\n\n{answer}")
    st.divider()

# --- MAIN APP ---
st.title("🛡️ Therapeutic Crisis Intervention (TCI) Tutor")
st.progress(st.session_state.module / 9)

# ==========================================
# MODULE 1: CRISIS PREVENTION
# ==========================================
if st.session_state.module == 1:
    st.header("Module 1: Crisis Prevention & The Milieu")
    
    st.subheader("1.1 The Trauma-Informed Approach")
    st.markdown("""
    * **Pain-Based Behavior:** Aggression, withdrawal, and defiance are often expressions of **pain or trauma**, not willful bad behavior.
    * **The Goal:** To help children learn to cope with stress, not just to enforce compliance.
    * **The Triune Brain:**
        * **Thinking Brain:** Reasoning (Offline during stress).
        * **Survival Brain:** Fight, Flight, or Freeze (In charge during stress).
    """)
    
    st.subheader("1.2 The Therapeutic Milieu")
    st.info("""
    The "Milieu" is the environment. We must manage 5 spaces:
    1. **Ideological:** Values (Learning > Control).
    2. **Physical:** Safety, noise, lighting, clutter.
    3. **Cultural:** Accepting the child's identity.
    4. **Social:** Relationships and routines.
    5. **Emotional:** Safety and emotional competence.
    """)

    st.divider()

    st.subheader("🧠 AI Scenario Practice")
    st.write("**Scenario:** Marcus (10yo) flips a chair because he has to stop playing. He screams 'I hate you!' and curls into a ball.")
    
    with st.form(key="mod1_form"):
        ans1 = st.text_area("Using the Triune Brain model, is he being 'bad'? What is happening?", height=100)
        submit1 = st.form_submit_button("Get AI Feedback")
    
    if submit1:
        if ans1:
            with st.spinner("Checking..."):
                st.success(get_ai_feedback(ans1, "Child flips chair/curls in ball.", "Survival Brain (Fight/Flight/Freeze) & Pain-Based Behavior"))
        else:
            st.warning("Please type an answer first.")

    st.divider()

    if st.button("Continue to Module 2 👉"):
        st.session_state.module = 2
        st.session_state.scroll_needed = True
        st.rerun()

# ==========================================
# MODULE 2: UNDERSTANDING CRISIS
# ==========================================
elif st.session_state.module == 2:
    st.header("Module 2: Understanding the Crisis")
    
    st.subheader("2.1 The Stress Model of Crisis")
    st.markdown("""
    A crisis follows a curve:
    1.  **Baseline:** Normal state (may still be anxious).
    2.  **Trigger:** The event that starts the stress.
    3.  **Escalation:** Agitation increases. **Intervene here!**
    4.  **Outburst:** Violence/Aggression (Survival Mode).
    5.  **Recovery:** Return to calm. Opportunity for learning.
    """)
    
    st.subheader("2.2 Goals & Assessment")
    st.warning("**Two Goals:** 1. Support (reduce stress/risk). 2. Teach (coping skills).")
    st.markdown("""
    **The 4 Questions:**
    1. What am I feeling now?
    2. What does this child feel, need, or want?
    3. How is the environment affecting this?
    4. How do I best respond?
    """)

    st.divider()

    st.subheader("🧠 AI Scenario Practice")
    st.write("**Scenario:** Sarah fails a test. She slams her book and paces (Escalation). She has NOT hit anyone.")
    
    with st.form(key="mod2_form"):
        ans2 = st.text_area("According to the 'Two Goals', what is your job right now?", height=100)
        submit2 = st.form_submit_button("Get AI Feedback")
        
    if submit2:
        if ans2:
            with st.spinner("Checking..."):
                st.success(get_ai_feedback(ans2, "Child escalating but not violent.", "Support: Reduce stress/risk. Teaching happens later."))
        else:
            st.warning("Please type an answer first.")

    st.divider()

    if st.button("Continue to Module 3 👉"):
        st.session_state.module = 3
        st.session_state.scroll_needed = True
        st.rerun()

# ==========================================
# MODULE 3: DE-ESCALATION
# ==========================================
elif st.session_state.module == 3:
    st.header("Module 3: De-Escalating the Crisis")
    
    st.subheader("3.1 Active Listening")
    st.markdown("""
    Validating feelings buys time for the thinking brain.
    * **Nonverbal:** Silence, nods, facial expression.
    * **Reflective:** "You seem really angry about..."
    """)
    
    st.subheader("3.2 Behavior Support Techniques")
    st.info("""
    * **Prompting:** Gentle reminders.
    * **Hurdle Help:** Assisting with a frustrating task.
    * **Redirection:** Shifting focus.
    * **Proximity:** Moving closer to support.
    * **Caring Gesture:** Building connection.
    """)
    
    st.subheader("3.3 Power Struggles")
    st.markdown("**Strategy: Drop the Rope.** Listen, validate, give choices.")

    st.divider()

    st.subheader("🧠 AI Scenario Practice")
    st.write("**Scenario:** You tell Jason to clean his room. He yells 'Make me!' You feel angry.")
    
    with st.form(key="mod3_form"):
        ans3 = st.text_area("How do you 'Drop the Rope'?", height=100)
        submit3 = st.form_submit_button("Get AI Feedback")
    
    if submit3:
        if ans3:
            with st.spinner("Checking..."):
                st.success(get_ai_feedback(ans3, "Child challenges authority.", "Drop the rope. Validate feelings, give choices, step back."))
        else:
            st.warning("Please type an answer first.")

    st.divider()

    if st.button("Continue to Module 4 👉"):
        st.session_state.module = 4
        st.session_state.scroll_needed = True
        st.rerun()

# ==========================================
# MODULE 4: MANAGING THE OUTBURST
# ==========================================
elif st.session_state.module == 4:
    st.header("Module 4: Managing the Crisis")
    
    st.subheader("4.1 Nonverbal Communication")
    st.markdown("""
    * **Eye Contact:** Avoid staring (it's threatening).
    * **Body Language:** Open stance, hands visible, off-center.
    * **Space:** Give MORE personal space.
    """)
    
    st.subheader("4.2 Crisis Co-Regulation")
    st.markdown("""
    When the child loses control, YOU provide the calm.
    * **Think:** Ask the 4 Questions.
    * **Do:** Deep breath. Step back. Give time.
    * **Say:** Very little. "I can see you are upset."
    """)

    st.divider()

    st.subheader("🧠 AI Scenario Practice")
    st.write("**Scenario:** The child is screaming and looking for a weapon. You are the target.")
    
    with st.form(key="mod4_form"):
        ans4 = st.text_area("Describe your body language and action.", height=100)
        submit4 = st.form_submit_button("Get AI Feedback")
    
    if submit4:
        if ans4:
            with st.spinner("Checking..."):
                st.success(get_ai_feedback(ans4, "Child in outburst, user is target.", "Remove the target (step away). Open stance. Hands visible."))
        else:
            st.warning("Please type an answer first.")

    st.divider()

    if st.button("Continue to Module 5 👉"):
        st.session_state.module = 5
        st.session_state.scroll_needed = True
        st.rerun()

# ==========================================
# MODULE 5: RECOVERY & LSI
# ==========================================
elif st.session_state.module == 5:
    st.header("Module 5: Recovery")
    
    st.subheader("5.1 The Life Space Interview (LSI)")
    st.markdown("Goal: Return child to normal and **Teach new skills**.")
    
    st.subheader("5.2 I ESCAPE Steps")
    st.info("""
    * **I** - Identify time/place.
    * **E** - Explore child's view.
    * **S** - Summarize feelings.
    * **C** - Connect trigger to behavior.
    * **A** - Alternative responses.
    * **P** - Plan/Practice.
    * **E** - Enter back to routine.
    """)

    st.divider()

    st.subheader("🧠 AI Scenario Practice")
    st.write("**Scenario:** The child is calm. You are doing the LSI. You just Summarized. What comes next?")
    
    with st.form(key="mod5_form"):
        ans5 = st.text_area("What is the 'C' step and what does it mean?", height=100)
        submit5 = st.form_submit_button("Get AI Feedback")
    
    if submit5:
        if ans5:
            with st.spinner("Checking..."):
                st.success(get_ai_feedback(ans5, "LSI step C.", "Connect. Connect trigger -> feeling -> behavior."))
        else:
            st.warning("Please type an answer first.")

    st.divider()

    if st.button("Continue to Module 6 👉"):
        st.session_state.module = 6
        st.session_state.scroll_needed = True
        st.rerun()

# ==========================================
# MODULE 6: SAFETY INTERVENTIONS
# ==========================================
elif st.session_state.module == 6:
    st.header("Module 6: Safety Interventions")
    
    st.subheader("6.1 Physical Restraint Risks")
    st.error("""
    **WARNING:** Restraint is ONLY for imminent safety risk.
    **Risks:**
    * **Positional Asphyxia:** Fatal respiratory arrest caused by body position.
    * **Trauma:** Re-traumatizing the child.
    """)
    
    st.subheader("6.2 Safety Principles")
    st.markdown("""
    * **Never** put weight on chest/back.
    * **Never** ignore "I can't breathe".
    * **Monitor:** Skin color, respiration.
    * **Goal:** Safety, not compliance.
    """)

    st.divider()

    st.subheader("🧠 AI Scenario Practice")
    st.write("**Scenario:** You are restraining a child. He says 'I can't breathe.' You think he is lying.")
    
    with st.form(key="mod6_form"):
        ans6 = st.text_area("What is the ONLY acceptable response?", height=100)
        submit6 = st.form_submit_button("Get AI Feedback")
    
    if submit6:
        if ans6:
            with st.spinner("Checking..."):
                st.success(get_ai_feedback(ans6, "Child says 'I can't breathe'.", "Release immediately or adjust position. Never ignore."))
        else:
            st.warning("Please type an answer first.")

    st.divider()

    if st.button("Continue to Study Guide 👉"):
        st.session_state.module = 7
        st.session_state.scroll_needed = True
        st.rerun()

# ==========================================
# MODULE 7: COMPREHENSIVE STUDY GUIDE
# ==========================================
elif st.session_state.module == 7:
    st.header("📚 TCI Comprehensive Study Guide")
    st.markdown("Review this detailed content before taking the Final Exam.")

    tab1, tab2, tab3, tab4 = st.tabs(["🧠 Prevention", "🛑 De-Escalation", "🔥 Crisis/Safety", "🌱 Recovery (LSI)"])

    with tab1:
        st.subheader("The Core Concepts")
        st.markdown("""
        **1. The Goal of TCI:**
        To reduce or eliminate the need for high-risk interventions (restraints) and replace them with therapeutic support.
        
        **2. Setting Conditions:**
        Anything that makes a challenging behavior more or less likely to occur. 
        * *Example:* A loud room (Physical) or a tired child (Biological).
        
        **3. Pain-Based Behavior:**
        Behaviors are expressions of needs. Aggression, defiance, and withdrawal are often trauma responses—the child's way of handling pain.
        """)
        
        st.info("""
        **The Triune Brain Model (The Hierarchy):**
        1.  **Thinking Brain (Neocortex):** Rational thought, language. *Offline during stress.*
        2.  **Emotional Brain (Limbic):** The "Sentry" (Amygdala) scans for danger.
        3.  **Survival Brain (Brain Stem):** **Fight, Flight, or Freeze.** *Trauma makes the 'Sentry' over-sensitive, hijacking the brain into survival mode quickly.*
        """)
        
        st.markdown("""
        **The 5 Spaces of the Therapeutic Milieu:**
        * **Ideological:** The organization's philosophy (Learning > Control).
        * **Physical:** The environment (Noise, light, clutter, safety).
        * **Cultural:** Accepting and celebrating the child's identity.
        * **Social:** Relationships, routines, and group dynamics.
        * **Emotional:** The sense of safety and the staff's emotional competence.
        """)

    with tab2:
        st.subheader("De-Escalation Strategies")
        st.markdown("""
        **Active Listening:**
        * Validating feelings ("You seem upset") vs. Judging behavior.
        * *Why?* It buys time for the Thinking Brain to come back online.
        
        **8 Behavior Support Techniques:**
        1.  **Managing the Environment:** Removing triggers (e.g., dimming lights).
        2.  **Prompting:** Gentle signals to remind child of expectations.
        3.  **Caring Gesture:** A smile or word to build connection ("I care about you").
        4.  **Hurdle Help:** Assisting with a difficult task to lower frustration.
        5.  **Redirection/Distraction:** Turning focus to a neutral/positive activity.
        6.  **Proximity:** Moving closer to provide support (not threat).
        7.  **Directive Statements:** Clear, simple instructions ("Please sit down").
        8.  **Time Away:** Asking child to go to a quiet place to self-regulate.
        
        **Emotional First Aid:**
        * **Goals:** Provide support, Resolve immediate crisis, Keep child in activity.
        """)
        
        st.error("""
        **POWER STRUGGLES (The Tug of War)**
        * **Definition:** When staff enters a conflict to "win" against the child.
        * **Strategy: DROP THE ROPE.**
        * **How:** Listen, Validate feelings, Give choices, Remove the audience.
        """)

    with tab3:
        st.subheader("Managing the Crisis")
        st.markdown("""
        **The Stress Model of Crisis (The Curve):**
        * **Baseline:** Normal state.
        * **Trigger:** The event/stimulus.
        * **Escalation:** Agitation. (Use Behavior Support here!).
        * **Outburst:** Violence/Aggression. (Safety Interventions here!).
        * **Recovery:** Return to baseline. (LSI here!).
        
        **Crisis Co-Regulation (What to do during Outburst):**
        * **THINK (4 Questions):** 1. What am I feeling? 
            2. What does the child feel/need? 
            3. How is the environment affecting this? 
            4. How do I best respond?
        * **DO:** Take a deep breath. Step back (give space). Hands visible. Neutral stance.
        * **SAY:** Very little. "I can see you are upset." "I am here to help."
        
        **The Elements of Violence:**
        To stop violence, remove one: **The Spark** (Trigger), **The Target** (Person), **The Weapon** (Object), **Stress/Motivation**.
        """)
        
        st.warning("""
        **SAFETY INTERVENTIONS (Physical Restraint)**
        * **Definition:** Use of trained staff to hold a child to contain acute physical behavior.
        * **CRITERIA:** ONLY used when there is **imminent risk of physical harm** to self or others.
        * **NEVER:** Used for discipline, compliance, or disrespect.
        * **POSITIONAL ASPHYXIA:** Fatal respiratory arrest caused by body position.
        * **FATAL ERRORS:** Placing weight on chest/back. Ignoring "I can't breathe."
        * **MONITOR:** Skin color, respiration, level of consciousness.
        """)

    with tab4:
        st.subheader("Recovery & The LSI")
        st.markdown("""
        **The Life Space Interview (LSI):**
        A therapeutic verbal strategy used *after* the crisis to turn the event into a learning experience.
        
        **GOALS:**
        1.  Return child to normal functioning.
        2.  Clarify the event.
        3.  Repair the relationship.
        4.  **Teach new coping skills.**
        5.  Re-enter the child into the routine.
        """)
        
        st.success("""
        **The Steps (I ESCAPE):**
        * **I - Identify** a time and place to talk. (Quiet, private).
        * **E - Explore** the child's point of view. ("What happened?").
        * **S - Summarize** feelings and content. ("So you were angry because...").
        * **C - Connect** trigger to feelings to behavior. ("When X happened, you felt Y, so you did Z.").
        * **A - Alternative** responses. ("What could you do next time instead of hitting?").
        * **P - Plan/Practice.** ("Let's practice taking a deep breath.").
        * **E - Enter** back into the routine. ("Welcome back to the group.").
        """)

    st.divider()
    if st.button("Ready for Final Exam 👉"):
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
        q1 = st.radio("1. What is the primary goal of the TCI system?", ["Enforce discipline", "Reduce high-risk interventions", "Eliminate emotions"])
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
