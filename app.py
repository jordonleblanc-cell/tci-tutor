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

# --- SESSION STATE ---
if "module" not in st.session_state:
    st.session_state.module = 1
if "bot_history" not in st.session_state:
    st.session_state.bot_history = [] # To store Q&A

# --- AI FUNCTIONS ---
def get_ai_feedback(user_response, scenario_context, correct_concept):
    """Grading logic for scenarios."""
    if not api_key: return "⚠️ AI features disabled."
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

# --- MAIN APP CONTENT ---
st.title("🛡️ Therapeutic Crisis Intervention (TCI) Tutor")
st.progress(st.session_state.module / 7)

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
    ans1 = st.text_area("Using the Triune Brain model, is he being 'bad'? What is happening?", height=100)
    if st.button("Get AI Feedback"):
        with st.spinner("Checking..."):
            st.success(get_ai_feedback(ans1, "Child flips chair/curls in ball.", "Survival Brain (Fight/Flight/Freeze) & Pain-Based Behavior"))

    st.divider()

    st.subheader("📝 Module 1 Knowledge Check")
    q1 = st.radio("1. 'Pain-based behavior' means the child is:", 
                  ["Being manipulative", "Expressing trauma/distress", "Just breaking rules"], index=None, key="m1q1")
    q2 = st.radio("2. Which 'Space' involves managing lighting, noise, and clutter?", 
                  ["Ideological Space", "Physical Space", "Social Space"], index=None, key="m1q2")

    if st.button("Check Answers & Continue"):
        if q1 == "Expressing trauma/distress" and q2 == "Physical Space":
            st.balloons()
            st.success("Correct! Moving to Module 2...")
            st.session_state.module = 2
            st.session_state.scroll_needed = True
            st.rerun()
        else:
            st.error("Please review the answers.")

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
    1. What am I feeling?
    2. What does the child feel/need?
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

    st.subheader("📝 Module 2 Knowledge Check")
    q1 = st.radio("1. In which phase is a child most likely to be violent?", 
                  ["Escalation Phase", "Outburst Phase", "Recovery Phase"], index=None, key="m2q1")
    q2 = st.radio("2. What is the FIRST question you should ask yourself in a crisis?", 
                  ["What did the child do wrong?", "What am I feeling now?", "Who is to blame?"], index=None, key="m2q2")

    if st.button("Check Answers & Continue"):
        if q1 == "Outburst Phase" and q2 == "What am I feeling now?":
            st.balloons()
            st.success("Correct! Moving to Module 3...")
            st.session_state.module = 3
            st.session_state.scroll_needed = True
            st.rerun()
        else:
            st.error("Incorrect. Review the Stress Model.")

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
    ans3 = st.text_area("How do you 'Drop the Rope'?", height=100)
    if st.button("Get AI Feedback"):
        with st.spinner("Checking..."):
            st.success(get_ai_feedback(ans3, "Child challenges authority.", "Drop the rope. Validate feelings, give choices, step back."))

    st.divider()

    st.subheader("📝 Module 3 Knowledge Check")
    q1 = st.radio("1. Helping a child with a difficult task to prevent frustration is called:", 
                  ["Redirection", "Hurdle Help", "Time Away"], index=None, key="m3q1")
    q2 = st.radio("2. To avoid a power struggle, you should:", 
                  ["Argue back to win", "Drop the rope and give choices", "Demand compliance"], index=None, key="m3q2")

    if st.button("Check Answers & Continue"):
        if q1 == "Hurdle Help" and q2 == "Drop the rope and give choices":
            st.balloons()
            st.success("Correct! Moving to Module 4...")
            st.session_state.module = 4
            st.session_state.scroll_needed = True
            st.rerun()
        else:
            st.error("Incorrect. Review Behavior Support Techniques.")

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
    ans4 = st.text_area("Describe your body language and action.", height=100)
    if st.button("Get AI Feedback"):
        with st.spinner("Checking..."):
            st.success(get_ai_feedback(ans4, "Child in outburst, user is target.", "Remove the target (step away). Open stance. Hands visible."))

    st.divider()

    st.subheader("📝 Module 4 Knowledge Check")
    q1 = st.radio("1. What is the first thing to 'DO' in Crisis Co-Regulation?", 
                  ["Restrain immediately", "Take a deep breath", "Lecture the child"], index=None, key="m4q1")
    q2 = st.radio("2. During an outburst, you should:", 
                  ["Speak loudly", "Give little to no verbal directives", "Stare the child down"], index=None, key="m4q2")

    if st.button("Check Answers & Continue"):
        if q1 == "Take a deep breath" and q2 == "Give little to no verbal directives":
            st.balloons()
            st.success("Correct! Moving to Module 5...")
            st.session_state.module = 5
            st.session_state.scroll_needed = True
            st.rerun()
        else:
            st.error("Incorrect. Check the 'Crisis Co-Regulation' steps.")

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
    ans5 = st.text_area("What is the 'C' step and what does it mean?", height=100)
    if st.button("Get AI Feedback"):
        with st.spinner("Checking..."):
            st.success(get_ai_feedback(ans5, "LSI step C.", "Connect. Connect trigger -> feeling -> behavior."))

    st.divider()

    st.subheader("📝 Module 5 Knowledge Check")
    q1 = st.radio("1. What does the 'C' in I ESCAPE stand for?", 
                  ["Control the child", "Connect trigger to behavior", "Call the parents"], index=None, key="m5q1")
    q2 = st.radio("2. What is a primary goal of the LSI?", 
                  ["To punish the child", "To teach new coping skills", "To create a paper trail"], index=None, key="m5q2")

    if st.button("Check Answers & Continue"):
        if q1 == "Connect trigger to behavior" and q2 == "To teach new coping skills":
            st.balloons()
            st.success("Correct! Moving to Module 6...")
            st.session_state.module = 6
            st.session_state.scroll_needed = True
            st.rerun()
        else:
            st.error("Incorrect. Review the I ESCAPE acronym.")

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
    ans6 = st.text_area("What is the ONLY acceptable response?", height=100)
    if st.button("Get AI Feedback"):
        with st.spinner("Checking..."):
            st.success(get_ai_feedback(ans6, "Child says 'I can't breathe'.", "Release immediately or adjust position. Never ignore."))

    st.divider()

    st.subheader("📝 Module 6 Knowledge Check")
    q1 = st.radio("1. What is Positional Asphyxia?", 
                  ["A seizure", "Fatal respiratory arrest due to body position", "A panic attack"], index=None, key="m6q1")
    q2 = st.radio("2. When should a restraint end?", 
                  ["When the child apologizes", "When the child is no longer a danger", "After 15 minutes"], index=None, key="m6q2")

    if st.button("Finish Course"):
        if q1 == "Fatal respiratory arrest due to body position" and q2 == "When the child is no longer a danger":
            st.balloons()
            st.success("🎉 CONGRATULATIONS! You have completed the full TCI refresher course.")
            st.session_state.module = 7
            st.session_state.scroll_needed = True
            st.rerun()
        else:
            st.error("Incorrect. These are life-saving protocols. Please review.")

elif st.session_state.module == 7:
    st.header("🎓 Course Complete")
    st.success("You have successfully reviewed all 6 modules of the Therapeutic Crisis Intervention system.")
    st.write("Remember: **Support** first, **Teach** second.")
    if st.button("Restart Training"):
        st.session_state.module = 1
        st.session_state.scroll_needed = True
        st.rerun()
