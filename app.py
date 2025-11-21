import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION ---
st.set_page_config(page_title="TCI Staff Training", page_icon="📘", layout="wide")

# --- API KEY SETUP ---
# Checks secrets.toml first, then falls back to sidebar input
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    api_key = st.sidebar.text_input("Enter Google API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.warning("⚠️ API Key missing. Please add it to secrets.toml or the sidebar to enable AI feedback.")

# --- SESSION STATE INITIALIZATION ---
if "module" not in st.session_state:
    st.session_state.module = 1
if "quiz_passed" not in st.session_state:
    st.session_state.quiz_passed = False

# --- HELPER FUNCTION: AI FEEDBACK ---
def get_ai_feedback(user_response, scenario_context, correct_concept):
    """Sends user response to Gemini for TCI-aligned grading."""
    if not api_key:
        return "⚠️ AI features disabled (No API Key)."
    
    # UPDATED MODEL: Using gemini-2.0-flash as per your available list
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        
        prompt = f"""
        You are an expert TCI (Therapeutic Crisis Intervention) instructor.
        
        Scenario Context: {scenario_context}
        The User was asked: "How should you respond/interpret this?"
        The User answered: "{user_response}"
        
        Task:
        1. Compare their answer to the TCI concept: '{correct_concept}'.
        2. If they align with TCI, praise them specificially on what they got right.
        3. If they are punitive, blaming, or miss the concept, gently correct them.
        4. Keep response encouraging and under 4 sentences.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error contacting AI: {e}"

# --- MAIN APP HEADER ---
st.title("🛡️ Therapeutic Crisis Intervention (TCI) Tutor")
st.progress(st.session_state.module / 7) # Progress bar

# ==========================================
# MODULE 1: Crisis Prevention & The Milieu
# ==========================================
if st.session_state.module == 1:
    st.header("Module 1: Crisis Prevention & The Therapeutic Milieu")
    
    with st.expander("📖 Study Guide: The Basics", expanded=True):
        st.markdown("""
        * **Trauma-Informed Care:** We ask "What happened to you?" not "What is wrong with you?"
        * **Pain-Based Behavior:** Aggression, withdrawal, and defiance are often expressions of pain/trauma, not willful bad behavior.
        * **The Triune Brain:** Under stress, the *Thinking Brain* shuts down and the *Survival Brain* (Fight/Flight/Freeze) takes over.
        * **The 5 Spaces:** Ideological, Physical, Cultural, Social, Emotional.
        """)

    st.subheader("🧠 AI Scenario Practice")
    st.info("""
    **Scenario:** 10-year-old Marcus flips a chair because you asked him to put away his game. 
    He screams, "You always hate me!" and runs to the corner, curling into a ball.
    """)
    
    ans1 = st.text_area("Based on TCI, is Marcus being 'bad'? Which part of his brain is in charge?", height=100)
    
    if st.button("Get Feedback"):
        if ans1:
            with st.spinner("Analyzing..."):
                feedback = get_ai_feedback(ans1, 
                    "Child flips chair and curls in ball after request.", 
                    "Pain-Based Behavior and Survival Brain (Fight/Flight/Freeze)")
                st.success(feedback)
        else:
            st.warning("Please type an answer.")

    st.divider()
    st.subheader("✅ Knowledge Check")
    q1 = st.radio("Which 'Space' involves the physical environment (lighting, noise, clutter)?", 
                  ["Ideological Space", "Physical Space", "Emotional Space"], index=None)
    
    if st.button("Submit Module 1"):
        if q1 == "Physical Space":
            st.balloons()
            st.success("Correct! Moving to Module 2...")
            st.session_state.module = 2
            st.rerun()
        else:
            st.error("Incorrect. Review the 5 Spaces.")

# ==========================================
# MODULE 2: Understanding the Crisis
# ==========================================
elif st.session_state.module == 2:
    st.header("Module 2: Understanding the Crisis")
    
    with st.expander("📖 Study Guide: The Stress Model", expanded=True):
        st.markdown("""
        * **Stress Model of Crisis:** Baseline -> Trigger -> Escalation -> Outburst -> Recovery.
        * **Two Goals of Intervention:** 1. **Support:** Reduce stress and risk immediately.
            2. **Teach:** Help children learn coping skills.
        * **The 4 Questions:** 1. What am I feeling? 
            2. What does the child feel/need? 
            3. How is the environment affecting this? 
            4. How do I best respond?
        """)

    st.subheader("🧠 AI Scenario Practice")
    st.info("""
    **Scenario:** Sarah fails a test (Trigger). She starts slamming her book, breathing fast, and pacing (Escalation).
    She has NOT attacked anyone yet.
    """)
    
    ans2 = st.text_area("Using the 'Two Goals,' what is your primary job right now?", height=100)
    
    if st.button("Get Feedback"):
        if ans2:
            with st.spinner("Analyzing..."):
                feedback = get_ai_feedback(ans2, 
                    "Child is escalating (slamming books) but not yet in outburst.", 
                    "Support: Reduce stress/risk (Environmental & Emotional Support). Teaching comes later.")
                st.success(feedback)

    st.divider()
    st.subheader("✅ Knowledge Check")
    q2 = st.radio("In which phase is the child MOST likely to be violent/aggressive?", 
                  ["Escalation Phase", "Outburst Phase", "Recovery Phase"], index=None)
    
    if st.button("Submit Module 2"):
        if q2 == "Outburst Phase":
            st.balloons()
            st.success("Correct! Moving to Module 3...")
            st.session_state.module = 3
            st.rerun()
        else:
            st.error("Incorrect. Violence peaks at the Outburst phase.")

# ==========================================
# MODULE 3: De-Escalating the Crisis
# ==========================================
elif st.session_state.module == 3:
    st.header("Module 3: De-Escalating the Crisis")
    
    with st.expander("📖 Study Guide: Tools for De-escalation", expanded=True):
        st.markdown("""
        * **Active Listening:** Validating feelings ("You seem really angry") vs judging.
        * **Behavior Support Techniques:** Prompting, Hurdle Help, Redirection, Caring Gesture.
        * **Power Struggles:** Occur when we get into a "tug of war." 
        * **Strategy:** Drop the rope! Listen, validate, give choices.
        """)

    st.subheader("🧠 AI Scenario Practice")
    st.info("""
    **Scenario:** You tell Jason to clean his room. He yells, "Make me!" 
    You feel your anger rising.
    """)
    
    ans3 = st.text_area("How do you avoid the Power Struggle here? What do you say?", height=100)
    
    if st.button("Get Feedback"):
        if ans3:
            with st.spinner("Analyzing..."):
                feedback = get_ai_feedback(ans3, 
                    "Child challenges authority ('Make me!'). Staff feels angry.", 
                    "Drop the rope. Validate feelings, give choices, step back. Do not argue.")
                st.success(feedback)

    st.divider()
    st.subheader("✅ Knowledge Check")
    q3 = st.radio("Which is a nonverbal active listening technique?", 
                  ["Asking 'Why?'", "Silence and Nods", "Giving a lecture"], index=None)
    
    if st.button("Submit Module 3"):
        if q3 == "Silence and Nods":
            st.balloons()
            st.success("Correct! Moving to Module 4...")
            st.session_state.module = 4
            st.rerun()
        else:
            st.error("Incorrect. Silence allows the child to process.")

# ==========================================
# MODULE 4: Managing the Crisis (Outburst)
# ==========================================
elif st.session_state.module == 4:
    st.header("Module 4: Managing the Crisis")
    
    with st.expander("📖 Study Guide: Crisis Co-Regulation", expanded=True):
        st.markdown("""
        * **Nonverbal Communication:** Eye contact, Body language, Personal space.
        * **Elements of Violence:** Spark, Target, Weapon, Stress/Motivation.
        * **Crisis Co-Regulation:**
            * *Think:* Ask the 4 questions.
            * *Do:* Deep breath, step back, give time, neutral stance.
            * *Say:* Very little. Calm tone.
        """)

    st.subheader("🧠 AI Scenario Practice")
    st.info("""
    **Scenario:** The child is now screaming and looking around for something to throw. 
    You are the target.
    """)
    
    ans4 = st.text_area("Describe your body language and what you do with your physical position.", height=100)
    
    if st.button("Get Feedback"):
        if ans4:
            with st.spinner("Analyzing..."):
                feedback = get_ai_feedback(ans4, 
                    "Child is in outburst, looking for weapon. User is target.", 
                    "Remove the target (step away). Open stance. Hands visible. Give space. No staring.")
                st.success(feedback)

    st.divider()
    st.subheader("✅ Knowledge Check")
    q4 = st.radio("During an outburst, what should you say?", 
                  ["A long explanation of the rules", "Very little (short, calm sentences)", "Threaten consequences"], index=None)
    
    if st.button("Submit Module 4"):
        if q4 == "Very little (short, calm sentences)":
            st.balloons()
            st.success("Correct! Moving to Module 5...")
            st.session_state.module = 5
            st.rerun()
        else:
            st.error("Incorrect. The child's listening brain is offline.")

# ==========================================
# MODULE 5: Recovery & LSI
# ==========================================
elif st.session_state.module == 5:
    st.header("Module 5: Recovery")
    
    with st.expander("📖 Study Guide: The LSI", expanded=True):
        st.markdown("""
        * **Goal:** Teach new skills and return child to normal functioning.
        * **I ESCAPE:**
            * **I**dentify a time and place to talk.
            * **E**xplore child's point of view.
            * **S**ummarize feelings/content.
            * **C**onnect trigger to feelings/behavior.
            * **A**lternative responses.
            * **P**lan/Practice.
            * **E**nter back into routine.
        """)

    st.subheader("🧠 AI Scenario Practice")
    st.info("""
    **Scenario:** The child is calm. You are doing the LSI. 
    You just finished 'Summarizing' what happened.
    """)
    
    ans5 = st.text_area("What is the next step in 'I ESCAPE' and what does it mean?", height=100)
    
    if st.button("Get Feedback"):
        if ans5:
            with st.spinner("Analyzing..."):
                feedback = get_ai_feedback(ans5, 
                    "LSI sequence: Identify, Explore, Summarize... what's next?", 
                    "Connect. Connect the trigger to the feelings and the behavior.")
                st.success(feedback)

    st.divider()
    st.subheader("✅ Knowledge Check")
    q5 = st.radio("What is the goal of the LSI?", 
                  ["To make the child apologize", "To teach new coping skills and re-enter the group", "To determine the punishment"], index=None)
    
    if st.button("Submit Module 5"):
        if q5 == "To teach new coping skills and re-enter the group":
            st.balloons()
            st.success("Correct! Moving to Module 6...")
            st.session_state.module = 6
            st.rerun()
        else:
            st.error("Incorrect. The LSI is a therapeutic learning tool, not punishment.")

# ==========================================
# MODULE 6: Safety Interventions
# ==========================================
elif st.session_state.module == 6:
    st.header("Module 6: Safety Interventions")
    
    with st.expander("📖 Study Guide: Restraints & Risk", expanded=True):
        st.markdown("""
        * **Physical Restraint:** A high-risk intervention used ONLY for imminent safety risk.
        * **Risks:** Positional Asphyxia (inability to breathe due to position), emotional trauma, injury.
        * **Never:** Put weight on chest/back. Restrain a child under 5. Ignore "I can't breathe."
        * **Goal:** Safety, not compliance.
        """)

    st.subheader("🧠 AI Scenario Practice")
    st.info("""
    **Scenario:** You are in a restraint. The child says "I can't breathe." 
    You think he is just saying it to get let go.
    """)
    
    ans6 = st.text_area("What is the ONLY acceptable response according to TCI?", height=100)
    
    if st.button("Get Feedback"):
        if ans6:
            with st.spinner("Analyzing..."):
                feedback = get_ai_feedback(ans6, 
                    "Child says 'I can't breathe' during restraint.", 
                    "Immediate action: Adjust position or release immediately. Never ignore respiratory distress.")
                st.success(feedback)

    st.divider()
    st.subheader("✅ Knowledge Check")
    q6 = st.radio("What is the definition of Positional Asphyxia?", 
                  ["Fainting from fear", "Fatal respiratory arrest caused by body position", "Hyperventilating"], index=None)
    
    if st.button("Finish Course"):
        if q6 == "Fatal respiratory arrest caused by body position":
            st.balloons()
            st.success("🎉 CONGRATULATIONS! You have completed the full TCI refresher course.")
            st.session_state.module = 7 # End state
            st.rerun()
        else:
            st.error("Incorrect. This is a life-threatening risk.")

elif st.session_state.module == 7:
    st.header("🎓 Course Complete")
    st.write("You have successfully reviewed all 6 modules of the TCI system.")
    if st.button("Restart Training"):
        st.session_state.module = 1
        st.rerun()
