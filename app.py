import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai

# --- CONFIGURATION ---
st.set_page_config(page_title="TCI Staff Training", page_icon="🛡️", layout="centered")

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
        
        Task: Answer clearly and accurately based STRICTLY on TCI guidelines (Trauma-informed care, Stress Model, LSI, Safety). 
        Keep it concise (under 3-4 sentences).
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

# --- SIDEBAR: AI TUTOR CHAT ---
with st.sidebar:
    st.divider()
    st.subheader("💬 AI Tutor Chat")
    with st.expander("Have a question?", expanded=False):
        st.write("Ask anything about TCI definitions, concepts, or rules.")
        user_q = st.text_input("Type your question here:", key="sidebar_q")
        if st.button("Ask AI"):
            if user_q:
                with st.spinner("Thinking..."):
                    answer = ask_tci_bot(user_q)
                    st.info(f"**Answer:** {answer}")
            else:
                st.warning("Please type a question.")
    st.divider()

# --- MAIN APP ---
st.title("🛡️ Therapeutic Crisis Intervention (TCI) Tutor")
st.progress(st.session_state.module / 8)

# ==========================================
# MODULE 1: CRISIS PREVENTION
# ==========================================
if st.session_state.module == 1:
    st.header("Module 1: Crisis Prevention & The Milieu")
    
    st.subheader("1.1 The Trauma-Informed Approach")
    st.markdown("""
    * [cite_start]**Pain-Based Behavior:** Aggression, withdrawal, and defiance are often expressions of **pain or trauma**, not willful bad behavior[cite: 120].
    * **The Goal:** To help children learn to cope with stress, not just to enforce compliance.
    * **The Triune Brain:**
        * **Thinking Brain:** Reasoning (Offline during stress).
        * [cite_start]**Survival Brain:** Fight, Flight, or Freeze (In charge during stress)[cite: 588].
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
    ans1 = st.text_area("Using the Triune Brain model, is he being 'bad'? What is happening?", height=100)
    if st.button("Get AI Feedback"):
        with st.spinner("Checking..."):
            st.success(get_ai_feedback(ans1, "Child flips chair/curls in ball.", "Survival Brain (Fight/Flight/Freeze) & Pain-Based Behavior"))

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
    [cite_start]A crisis follows a curve[cite: 806]:
    1.  **Baseline:** Normal state (may still be anxious).
    2.  **Trigger:** The event that starts the stress.
    3.  **Escalation:** Agitation increases. **Intervene here!**
    4.  **Outburst:** Violence/Aggression (Survival Mode).
    5.  **Recovery:** Return to calm. Opportunity for learning.
    """)
    
    st.subheader("2.2 Goals & Assessment")
    [cite_start]st.warning("**Two Goals:** 1. Support (reduce stress/risk). 2. Teach (coping skills)[cite: 764].")
    st.markdown("""
    [cite_start]**The 4 Questions[cite: 890]:**
    1. What am I feeling now?
    2. What does this child feel, need, or want?
    3. How is the environment affecting this?
    4. How do I best respond?
    """)

    st.divider()

    st.subheader("🧠 AI Scenario Practice")
    st.write("**Scenario:** Sarah fails a test. She slams her book and paces (Escalation). She has NOT hit anyone.")
    ans2 = st.text_area("According to the 'Two Goals', what is your job right now?", height=100)
    if st.button("Get AI Feedback"):
        with st.spinner("Checking..."):
            st.success(get_ai_feedback(ans2, "Child escalating but not violent.", "Support: Reduce stress/risk. Teaching happens later."))

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
    [cite_start]Validating feelings buys time for the thinking brain[cite: 1065].
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
    [cite_start]st.markdown("**Strategy: Drop the Rope.** Listen, validate, give choices[cite: 1528].")

    st.divider()

    st.subheader("🧠 AI Scenario Practice")
    st.write("**Scenario:** You tell Jason to clean his room. He yells 'Make me!' You feel angry.")
    ans3 = st.text_area("How do you 'Drop the Rope'?", height=100)
    if st.button("Get AI Feedback"):
        with st.spinner("Checking..."):
            st.success(get_ai_feedback(ans3, "Child challenges authority.", "Drop the rope. Validate feelings, give choices, step back."))

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
    * [cite_start]**Eye Contact:** Avoid staring (it's threatening)[cite: 1582].
    * **Body Language:** Open stance, hands visible, off-center.
    * **Space:** Give MORE personal space.
    """)
    
    st.subheader("4.2 Crisis Co-Regulation")
    st.markdown("""
    When the child loses control, YOU provide the calm.
    * **Think:** Ask the 4 Questions.
    * [cite_start]**Do:** Deep breath. Step back. Give time[cite: 1783].
    * **Say:** Very little. "I can see you are upset."
    """)

    st.divider()

    st.subheader("🧠 AI Scenario Practice")
    st.write("**Scenario:** The child is screaming and looking for a weapon. You are the target.")
    ans4 = st.text_area("Describe your body language and action.", height=100)
    if st.button("Get AI Feedback"):
        with st.spinner("Checking..."):
            st.success(get_ai_feedback(ans4, "Child in outburst, user is target.", "Remove the target (step away). Open stance. Hands visible."))

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
    [cite_start]st.markdown("Goal: Return child to normal and **Teach new skills**[cite: 1952].")
    
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
    ans5 = st.text_area("What is the 'C' step and what does it mean?", height=100)
    if st.button("Get AI Feedback"):
        with st.spinner("Checking..."):
            st.success(get_ai_feedback(ans5, "LSI step C.", "Connect. Connect trigger -> feeling -> behavior."))

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
    [cite_start]**WARNING:** Restraint is ONLY for imminent safety risk[cite: 2309].
    **Risks:**
    * [cite_start]**Positional Asphyxia:** Fatal respiratory arrest caused by body position[cite: 2552].
    * **Trauma:** Re-traumatizing the child.
    """)
    
    st.subheader("6.2 Safety Principles")
    st.markdown("""
    * **Never** put weight on chest/back.
    * [cite_start]**Never** ignore "I can't breathe"[cite: 2662].
    * **Monitor:** Skin color, respiration.
    * **Goal:** Safety, not compliance.
    """)

    st.divider()

    st.subheader("🧠 AI Scenario Practice")
    st.write("**Scenario:** You are restraining a child. He says 'I can't breathe.' You think he is lying.")
    ans6 = st.text_area("What is the ONLY acceptable response?", height=100)
    if st.button("Get AI Feedback"):
        with st.spinner("Checking..."):
            st.success(get_ai_feedback(ans6, "Child says 'I can't breathe'.", "Release immediately or adjust position. Never ignore."))

    st.divider()

    if st.button("Start Final Exam 👉"):
        st.session_state.module = 7
        st.session_state.scroll_needed = True
        st.rerun()

# ==========================================
# MODULE 7: FINAL EXAM
# ==========================================
elif st.session_state.module == 7:
    st.header("📝 Final Certification Exam")
    st.write("Answer all 20 questions. Passing score: 80% (16/20).")
    
    with st.form("exam_form"):
        # QUESTIONS LIST
        q1 = st.radio("1. What is the primary goal of the TCI system?", 
             ["To enforce strict discipline", "To reduce the need for high-risk interventions", "To eliminate all emotions"])
        
        q2 = st.radio("2. A child's aggression or withdrawal is often an expression of:", 
             ["Willful bad behavior", "Pain or trauma (Pain-Based Behavior)", "Laziness"])
        
        q3 = st.radio("3. Which part of the brain controls 'Fight, Flight, or Freeze'?", 
             ["The Thinking Brain (Neocortex)", "The Emotional Brain (Limbic)", "The Survival Brain (Brain Stem)"])
        
        q4 = st.radio("4. Anything that makes challenging behavior more or less likely to occur is called a:", 
             ["Setting Condition", "Trigger", "Crisis"])
        
        q5 = st.radio("5. In the Stress Model of Crisis, which phase is the peak of violence?", 
             ["Escalation", "Outburst", "Recovery"])
        
        q6 = st.radio("6. What are the two goals of crisis intervention?", 
             ["Control & Punish", "Support & Teach", "Restrain & Isolate"])
        
        q7 = st.radio("7. What is the FIRST question you ask yourself in a crisis?", 
             ["What did the child do?", "What am I feeling now?", "Who started it?"])
        
        q8 = st.radio("8. Which is a nonverbal Active Listening technique?", 
             ["Asking 'Why?'", "Silence", "Lecturing"])
        
        q9 = st.radio("9. Helping a child with the first few steps of a difficult task is called:", 
             ["Prompting", "Hurdle Help", "Redirection"])
        
        q10 = st.radio("10. When a power struggle begins, what is the best strategy?", 
             ["Win the argument", "Drop the rope", "Threaten consequences"])
        
        q11 = st.radio("11. During an outburst, how should you handle eye contact?", 
             ["Stare them down", "Avoid it completely", "Use intermittent, non-threatening eye contact"])
        
        q12 = st.radio("12. Which of the following is an element of a violent situation?", 
             ["The Spark", "The Target", "The Weapon", "All of the above"])
        
        q13 = st.radio("13. What is the first step of Crisis Co-Regulation?", 
             ["Step back", "Take a deep breath", "Give a command"])
        
        q14 = st.radio("14. What does the 'C' in I ESCAPE stand for?", 
             ["Control the child", "Connect trigger to feelings/behavior", "Call for help"])
        
        q15 = st.radio("15. What is a primary goal of the Life Space Interview (LSI)?", 
             ["To return the child to normal functioning and teach new skills", "To make the child apologize", "To document the incident"])
        
        q16 = st.radio("16. Physical restraint should ONLY be used when:", 
             ["The child is being disrespectful", "There is imminent risk of physical harm", "The child refuses to follow directions"])
        
        q17 = st.radio("17. What is Positional Asphyxia?", 
             ["A panic attack", "Fatal respiratory arrest caused by body position", "Hyperventilation"])
        
        q18 = st.radio("18. You must NEVER put weight on a child's:", 
             ["Arms", "Legs", "Chest, back, or stomach"])
        
        q19 = st.radio("19. If a child says 'I can't breathe' during a restraint, you must:", 
             ["Tell them to calm down", "Ignore it if they are talking", "Release or adjust immediately"])
        
        q20 = st.radio("20. A restraint must end when:", 
             ["The child is no longer a danger", "The child promises to be good", "15 minutes have passed"])

        submitted = st.form_submit_button("Submit Exam")
        
        if submitted:
            score = 0
            if q1 == "To reduce the need for high-risk interventions": score += 1
            if q2 == "Pain or trauma (Pain-Based Behavior)": score += 1
            if q3 == "The Survival Brain (Brain Stem)": score += 1
            if q4 == "Setting Condition": score += 1
            if q5 == "Outburst": score += 1
            if q6 == "Support & Teach": score += 1
            if q7 == "What am I feeling now?": score += 1
            if q8 == "Silence": score += 1
            if q9 == "Hurdle Help": score += 1
            if q10 == "Drop the rope": score += 1
            if q11 == "Use intermittent, non-threatening eye contact": score += 1
            if q12 == "All of the above": score += 1
            if q13 == "Take a deep breath": score += 1
            if q14 == "Connect trigger to feelings/behavior": score += 1
            if q15 == "To return the child to normal functioning and teach new skills": score += 1
            if q16 == "There is imminent risk of physical harm": score += 1
            if q17 == "Fatal respiratory arrest caused by body position": score += 1
            if q18 == "Chest, back, or stomach": score += 1
            if q19 == "Release or adjust immediately": score += 1
            if q20 == "The child is no longer a danger": score += 1
            
            st.session_state.final_score = score
            if score >= 16:
                st.session_state.module = 8
                st.session_state.scroll_needed = True
                st.rerun()
            else:
                st.error(f"You scored {score}/20 ({(score/20)*100}%). You need 80% to pass. Please review the materials and try again.")

# ==========================================
# MODULE 8: COMPLETION
# ==========================================
elif st.session_state.module == 8:
    st.header("🎓 Certificate of Completion")
    st.balloons()
    st.success(f"CONGRATULATIONS! You passed the TCI Final Exam with a score of {st.session_state.final_score}/20.")
    
    st.markdown("""
    ### You are now trained in:
    * ✅ Crisis Prevention & The Therapeutic Milieu
    * ✅ The Stress Model of Crisis
    * ✅ De-Escalation Strategies
    * ✅ Managing Violence & Outbursts
    * ✅ The Life Space Interview (LSI)
    * ✅ Safety Interventions & Risks
    """)
    
    st.info("Please take a screenshot of this page for your supervisor.")
    
    if st.button("Restart Training"):
        st.session_state.module = 1
        st.session_state.scroll_needed = True
        st.rerun()
