import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION ---
st.set_page_config(page_title="TCI Staff Training", page_icon="🛡️", layout="wide")

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

# --- MAIN APP ---
st.title("🛡️ Therapeutic Crisis Intervention (TCI) Tutor")
st.progress(st.session_state.module / 7)

# ==========================================
# MODULE 1: CRISIS PREVENTION
# ==========================================
if st.session_state.module == 1:
    st.header("Module 1: Crisis Prevention & The Milieu")
    
    # --- TEACHING CONTENT ---
    col1, col2 = st.columns([2, 1])
    with col1:
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
        [cite_start]The "Milieu" is the environment. We must manage 5 spaces[cite: 350]:
        1. **Ideological:** Values (Learning > Control).
        2. **Physical:** Safety, noise, lighting, clutter.
        3. **Cultural:** Accepting the child's identity.
        4. **Social:** Relationships and routines.
        5. **Emotional:** Safety and emotional competence.
        """)

    with col2:
        st.markdown("### 🧠 AI Scenario")
        st.write("**Scenario:** Marcus (10yo) flips a chair because he has to stop playing. He screams 'I hate you!' and curls into a ball.")
        ans1 = st.text_area("Using the Triune Brain, is he being 'bad'? What is happening?", height=150)
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
            st.rerun()
        else:
            st.error("Please review the answers. Hint: Think about what drives the behavior and look at the definitions of the Spaces.")

# ==========================================
# MODULE 2: UNDERSTANDING CRISIS
# ==========================================
elif st.session_state.module == 2:
    st.header("Module 2: Understanding the Crisis")
    
    col1, col2 = st.columns([2, 1])
    with col1:
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
        st.warning("**Two Goals:** 1. Support (reduce stress/risk). 2. Teach (coping skills).")
        st.markdown("""
        [cite_start]**The 4 Questions[cite: 889]:**
        1. What am I feeling?
        2. What does the child feel/need?
        3. How is the environment affecting this?
        4. How do I best respond?
        """)

    with col2:
        st.markdown("### 🧠 AI Scenario")
        st.write("**Scenario:** Sarah fails a test. She slams her book and paces (Escalation). She has NOT hit anyone.")
        ans2 = st.text_area("According to the 'Two Goals', what is your job right now?", height=150)
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
            st.rerun()
        else:
            st.error("Incorrect. Review the Stress Model and the 4 Questions.")

# ==========================================
# MODULE 3: DE-ESCALATION
# ==========================================
elif st.session_state.module == 3:
    st.header("Module 3: De-Escalating the Crisis")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("3.1 Active Listening")
        st.markdown("""
        [cite_start]Validating feelings buys time for the thinking brain[cite: 1059].
        * **Nonverbal:** Silence, nods, facial expression.
        * **Reflective:** "You seem really angry about..."
        """)
        
        st.subheader("3.2 Behavior Support Techniques")
        st.info("""
        * **Prompting:** Gentle reminders.
        * [cite_start]**Hurdle Help:** Assisting with a frustrating task[cite: 1305].
        * **Redirection:** Shifting focus.
        * **Proximity:** Moving closer to support.
        * **Caring Gesture:** Building connection.
        """)
        
        st.subheader("3.3 Power Struggles")
        [cite_start]st.markdown("**Strategy: Drop the Rope.** Listen, validate, give choices[cite: 1528].")

    with col2:
        st.markdown("### 🧠 AI Scenario")
        st.write("**Scenario:** You tell Jason to clean his room. He yells 'Make me!' You feel angry.")
        ans3 = st.text_area("How do you 'Drop the Rope'?", height=150)
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
            st.rerun()
        else:
            st.error("Incorrect. Review Behavior Support Techniques.")

# ==========================================
# MODULE 4: MANAGING THE OUTBURST
# ==========================================
elif st.session_state.module == 4:
    st.header("Module 4: Managing the Crisis")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("4.1 Nonverbal Communication")
        st.markdown("""
        * **Eye Contact:** Avoid staring (it's threatening).
        * **Body Language:** Open stance, hands visible, off-center.
        * [cite_start]**Space:** Give MORE personal space[cite: 1608].
        """)
        
        st.subheader("4.2 Crisis Co-Regulation")
        st.markdown("""
        [cite_start]When the child loses control, YOU provide the calm[cite: 1737].
        * **Think:** Ask the 4 Questions.
        * **Do:** Deep breath. Step back. Give time.
        * **Say:** Very little. "I can see you are upset."
        """)

    with col2:
        st.markdown("### 🧠 AI Scenario")
        st.write("**Scenario:** The child is screaming and looking for a weapon. You are the target.")
        ans4 = st.text_area("Describe your body language and action.", height=150)
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
            st.rerun()
        else:
            st.error("Incorrect. Check the 'Crisis Co-Regulation' steps.")

# ==========================================
# MODULE 5: RECOVERY & LSI
# ==========================================
elif st.session_state.module == 5:
    st.header("Module 5: Recovery")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("5.1 The Life Space Interview (LSI)")
        [cite_start]st.markdown("Goal: Return child to normal and **Teach new skills**[cite: 1952].")
        
        st.subheader("5.2 I ESCAPE Steps")
        st.info("""
        * **I** - Identify time/place.
        * **E** - Explore child's view.
        * **S** - Summarize feelings.
        * [cite_start]**C** - Connect trigger to behavior[cite: 2021].
        * **A** - Alternative responses.
        * **P** - Plan/Practice.
        * **E** - Enter back to routine.
        """)

    with col2:
        st.markdown("### 🧠 AI Scenario")
        st.write("**Scenario:** You are doing the LSI. You just Summarized. What comes next?")
        ans5 = st.text_area("What is the 'C' step and what does it mean?", height=150)
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
            st.rerun()
        else:
            st.error("Incorrect. Review the I ESCAPE acronym.")

# ==========================================
# MODULE 6: SAFETY INTERVENTIONS
# ==========================================
elif st.session_state.module == 6:
    st.header("Module 6: Safety Interventions")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("6.1 Physical Restraint Risks")
        st.error("""
        [cite_start]**WARNING:** Restraint is ONLY for imminent safety risk[cite: 2309].
        **Risks:**
        * [cite_start]**Positional Asphyxia:** Fatal respiratory arrest caused by body position[cite: 2552].
        * **Trauma:** Re-traumatizing the child.
        """)
        
        st.subheader("6.2 Safety Principles")
        st.markdown("""
        * [cite_start]**Never** put weight on chest/back[cite: 2651].
        * [cite_start]**Never** ignore "I can't breathe"[cite: 2662].
        * [cite_start]**Monitor:** Skin color, respiration[cite: 2637].
        * **Goal:** Safety, not compliance.
        """)

    with col2:
        st.markdown("### 🧠 AI Scenario")
        st.write("**Scenario:** You are restraining a child. He says 'I can't breathe.' You think he is lying.")
        ans6 = st.text_area("What is the ONLY acceptable response?", height=150)
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
            st.rerun()
        else:
            st.error("Incorrect. These are life-saving protocols. Please review.")

elif st.session_state.module == 7:
    st.header("🎓 Course Complete")
    st.success("You have successfully reviewed all 6 modules of the Therapeutic Crisis Intervention system.")
    st.write("Remember: **Support** first, **Teach** second.")
    if st.button("Restart Training"):
        st.session_state.module = 1
        st.rerun()
