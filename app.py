import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION ---
st.set_page_config(page_title="TCI Staff Training", page_icon="📘")

# --- SIDEBAR: API KEY ENTRY ---
# Ideally, you store this in Streamlit Secrets, but for testing, we can put it here.
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter Google API Key", type="password")
    if api_key:
        genai.configure(api_key=api_key)
    st.caption("Get your key from aistudio.google.com")

# --- AI TUTOR LOGIC ---
def get_ai_feedback(user_response, correct_concept):
    """Sends the user's answer to Gemini for grading."""
    if not api_key:
        return "⚠️ Please enter an API Key in the sidebar to get feedback."
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    # This prompt tells Gemini how to behave
    prompt = f"""
    You are an expert TCI (Therapeutic Crisis Intervention) instructor. 
    The student was asked this scenario: 'A child is screaming because he can't watch TV.'
    The correct concept they should identify is: '{correct_concept}'.
    
    The student answered: "{user_response}"
    
    1. Tell them if they are correct or incorrect based on TCI principles.
    2. If incorrect, gently explain why (Pain-Based Behavior vs Willful Defiance).
    3. Keep it encouraging and under 3 sentences.
    """
    
    response = model.generate_content(prompt)
    return response.text

# --- MAIN APP ---
st.title("📘 TCI Interactive Training")
st.write("Welcome. This tool will help you master the Therapeutic Crisis Intervention system.")

# Session State (Keeps track of where the user is)
if "step" not in st.session_state:
    st.session_state.step = 1

# ==========================================
# MODULE 1: Crisis Prevention
# ==========================================
if st.session_state.step == 1:
    st.header("Module 1: Crisis Prevention & The Milieu")
    
    st.markdown("""
    ### Key Concept: Pain-Based Behavior
    When a child in our care acts out (aggression, withdrawal, yelling), it is often not because 
    they are "bad," but because they are in **pain**. 
    
    * **Trauma Effect:** Trauma rewires the brain to be hyper-sensitive to danger.
    * **Our Goal:** We must ask "What does this child feel, need, or want?" rather than just punishing the behavior.
    """)
    
    st.divider()
    
    st.subheader("📝 Practice Scenario")
    st.info("""
    **Scenario:** 10-year-old Marcus flips a chair because you asked him to put away his game.
    He screams, "You always hate me!" and runs to the corner.
    """)
    
    user_answer = st.text_area("Based on TCI, how should you interpret Marcus's behavior? Why is he doing this?", height=100)
    
    if st.button("Submit Answer"):
        if user_answer:
            with st.spinner(" The AI Tutor is analyzing your answer..."):
                # We ask Gemini to grade it against the concept of "Pain-Based Behavior"
                feedback = get_ai_feedback(user_answer, "Pain-Based Behavior / Survival Brain expression")
                st.success("### Feedback")
                st.write(feedback)
                
                st.button("Continue to Quiz 👉", on_click=lambda: st.session_state.update({"step": 2}))
        else:
            st.warning("Please write an answer first.")

# ==========================================
# QUIZ SECTION
# ==========================================
elif st.session_state.step == 2:
    st.header("Module 1 Quiz")
    
    q1 = st.radio(
        "1. Which part of the 'Triune Brain' is in charge when a child is in 'Fight, Flight, or Freeze' mode?",
        ["The Thinking Brain (Neocortex)", "The Survival Brain (Brain Stem)", "The Happy Brain"],
        index=None
    )
    
    q2 = st.radio(
        "2. What is the primary goal of the TCI system?",
        ["To eliminate all bad behavior immediately", "To reduce the need for high-risk interventions", "To teach children strict discipline"],
        index=None
    )

    if st.button("Submit Quiz"):
        if q1 == "The Survival Brain (Brain Stem)" and q2 == "To reduce the need for high-risk interventions":
            st.balloons()
            st.success("🎉 Excellent! You have passed Module 1.")
            st.write("You are ready for the next module.")
        else:
            st.error("Not quite. Review the answers and try again.")
