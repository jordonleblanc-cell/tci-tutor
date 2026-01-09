import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import matplotlib.pyplot as plt
import numpy as np
import time

# --- CONFIGURATION ---
st.set_page_config(
    page_title="TCI Interactive Master Class", 
    page_icon="🛡️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR LMS FEEL ---
st.markdown("""
<style>
    .main-header { font-size: 2.5rem; color: #1E3A8A; font-weight: 700; }
    .sub-header { font-size: 1.5rem; color: #3B82F6; font-weight: 600; }
    .highlight { background-color: #FEF3C7; padding: 10px; border-radius: 5px; border-left: 5px solid #F59E0B; }
    .concept-card { background-color: #F3F4F6; padding: 20px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); margin-bottom: 20px; }
    .stButton>button { width: 100%; border-radius: 5px; }
    .success-box { background-color: #D1FAE5; padding: 15px; border-radius: 5px; color: #065F46; }
    .warning-box { background-color: #FEE2E2; padding: 15px; border-radius: 5px; color: #991B1B; }
</style>
""", unsafe_allow_html=True)

# --- STATE MANAGEMENT ---
if "module" not in st.session_state: st.session_state.module = "Home"
if "quiz_score" not in st.session_state: st.session_state.quiz_score = 0
if "roleplay_history" not in st.session_state: st.session_state.roleplay_history = []
if "roleplay_active" not in st.session_state: st.session_state.roleplay_active = False

# --- API SETUP ---
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    api_key = st.sidebar.text_input("🔑 Enter Google API Key", type="password")
    if not api_key:
        st.sidebar.warning("API Key required for AI Features")

if api_key:
    genai.configure(api_key=api_key)

# --- HELPER FUNCTIONS ---

def draw_stress_model():
    """Generates the TCI Stress Model Curve visual."""
    x = np.linspace(0, 10, 500)
    # Simulate the curve: Baseline -> Trigger -> Escalation -> Outburst -> Recovery
    y = np.piecewise(x, 
        [x < 2, (x >= 2) & (x < 4), (x >= 4) & (x < 6), (x >= 6) & (x < 8), x >= 8],
        [1, lambda x: x-1, lambda x: 2*(x-3)+1, lambda x: -2*(x-8)+1, 1]
    )
    
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(x, y, color='#3B82F6', linewidth=3)
    ax.fill_between(x, y, color='#DBEAFE', alpha=0.5)
    
    # Annotations
    ax.annotate('Baseline', xy=(1, 1.2), xytext=(1, 2), arrowprops=dict(facecolor='black', arrowstyle='->'))
    ax.annotate('Trigger', xy=(2.1, 1.2), xytext=(2.5, 0.5), arrowprops=dict(facecolor='red', arrowstyle='->'), color='red')
    ax.annotate('Escalation\n(Intervene Here!)', xy=(4, 3), xytext=(2.5, 4), arrowprops=dict(facecolor='green', arrowstyle='->'), color='green', fontweight='bold')
    ax.annotate('Outburst', xy=(6, 5), xytext=(6, 6), arrowprops=dict(facecolor='red', arrowstyle='->'), color='red', fontweight='bold')
    ax.annotate('Recovery\n(LSI)', xy=(8.5, 2), xytext=(8, 4), arrowprops=dict(facecolor='black', arrowstyle='->'))

    ax.set_title("The Stress Model of Crisis", fontsize=14)
    ax.set_yticks([])
    ax.set_xticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    return fig

def get_ai_tutor(prompt):
    """Generic Tutor Logic"""
    if not api_key: return "⚠️ Please connect API Key."
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        full_prompt = f"You are a master TCI (Therapeutic Crisis Intervention) instructor. Concise, encouraging, and strictly adhering to TCI Cornell University standards. \n\n{prompt}"
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

def run_roleplay(user_input, scenario):
    """Handles the back-and-forth simulation."""
    if not api_key: return "⚠️ API Key needed."
    
    model = genai.GenerativeModel("gemini-2.0-flash")
    
    history_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.roleplay_history])
    
    system_prompt = f"""
    You are roleplaying a traumatized child in a residential facility. 
    Scenario: {scenario}
    
    Rules for you (The Child):
    1. Act your age (approx 12-14).
    2. Start in the 'Escalation' phase. 
    3. If the user (Staff) validates your feelings and uses 'Drop the Rope', you de-escalate slightly.
    4. If the user argues, orders, or threatens, you escalate significantly.
    5. Keep responses short (1-2 sentences).
    
    Current History:
    {history_text}
    
    User (Staff) just said: "{user_input}"
    
    Respond as the child.
    """
    
    try:
        response = model.generate_content(system_prompt)
        return response.text
    except Exception as e:
        return "Error in simulation."

# --- NAVIGATION ---
st.sidebar.title("📍 TCI Navigator")
nav_options = {
    "Home": "🏠 Dashboard",
    "Mod1": "🧠 1. Prevention & Milieu",
    "Mod2": "📈 2. Stress Model & Curve",
    "Mod3": "🛑 3. De-Escalation Tools",
    "Mod4": "🔥 4. The Outburst",
    "Mod5": "🌱 5. Recovery (LSI)",
    "Dojo": "🥋 AI Roleplay Dojo",
    "Exam": "📝 Final Exam"
}

selection = st.sidebar.radio("Go to:", list(nav_options.keys()), format_func=lambda x: nav_options[x])
st.session_state.module = selection

st.sidebar.markdown("---")
st.sidebar.metric("Progress", f"{len(st.session_state.roleplay_history)} Interactions", delta_color="off")

# ==========================================
# PAGE: DASHBOARD
# ==========================================
if st.session_state.module == "Home":
    st.markdown("<div class='main-header'>🛡️ TCI Interactive Master Class</div>", unsafe_allow_html=True)
    st.markdown("### *Therapeutic Crisis Intervention Training*")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        Welcome to the enhanced TCI training platform. This tool is designed to move beyond reading and into **understanding and application**.
        
        **What you will learn:**
        * **Prevention:** How to set up a safe environment.
        * **De-escalation:** Verbal tools to calm a crisis.
        * **Safety:** Protecting the child and yourself.
        * **Recovery:** Turning crisis into a learning moment.
        """)
        
        st.info("💡 **Tip:** Use the 'AI Roleplay Dojo' to practice your skills against a simulated child before the exam!")

    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/2921/2921226.png", width=150)
        st.markdown("**Status:** In Training")

# ==========================================
# PAGE: MODULE 1 - PREVENTION
# ==========================================
elif st.session_state.module == "Mod1":
    st.markdown("<div class='main-header'>Module 1: Prevention & The Milieu</div>", unsafe_allow_html=True)
    
    st.markdown("### 1.1 The Therapeutic Milieu")
    st.write("The 'Milieu' is the living environment. We must manage 5 distinct spaces to prevent crisis.")
    
    tabs = st.tabs(["🏛️ Ideological", "🛋️ Physical", "🎭 Cultural", "🤝 Social", "❤️ Emotional"])
    
    with tabs[0]:
        st.success("**Ideological:** The philosophy. (e.g., Do we believe children do well if they can?)")
    with tabs[1]:
        st.warning("**Physical:** The setting. (Lights, noise, clutter, weapons, potential hazards).")
    with tabs[2]:
        st.info("**Cultural:** Accepting differences. (Food, customs, celebrations, avoiding bias).")
    with tabs[3]:
        st.error("**Social:** Relationships. (Group dynamics, peer interactions, staff consistency).")
    with tabs[4]:
        st.success("**Emotional:** Safety. (Does the child feel safe to express feelings without ridicule?)")

    st.markdown("---")
    st.markdown("### 1.2 The Triune Brain")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class='concept-card'>
        <h4>🧠 The Thinking Brain (Neocortex)</h4>
        Rational thought, planning, language. <br>
        <i>Status during crisis:</i> <b>OFFLINE</b>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='concept-card'>
        <h4>❤️ The Emotional Brain (Limbic)</h4>
        The 'Sentry'. Scans for danger. Emotion center. <br>
        <i>Status during crisis:</i> <b>HIGH ALERT</b>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='concept-card'>
        <h4>🦎 The Survival Brain (Brain Stem)</h4>
        Fight, Flight, Freeze. Automatic functions. <br>
        <i>Status during crisis:</i> <b>IN CHARGE</b>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.info("📝 **Key Takeaway:** You cannot reason with a child in the Survival Brain. You must lower their stress to get the Thinking Brain back online.")

# ==========================================
# PAGE: MODULE 2 - STRESS MODEL
# ==========================================
elif st.session_state.module == "Mod2":
    st.markdown("<div class='main-header'>Module 2: The Stress Model of Crisis</div>", unsafe_allow_html=True)
    
    st.write("Understanding *where* a child is on this curve determines *what* you do.")
    
    # Render the Matplotlib Chart
    st.pyplot(draw_stress_model())
    
    st.markdown("### Interactive Phase Explorer")
    phase = st.select_slider("Slide to see staff interventions for each phase:", 
        options=["Baseline", "Triggering Event", "Escalation", "Outburst", "Recovery"])
    
    if phase == "Baseline":
        st.success("🟢 **Goal:** Support Environment. **Action:** Build relationships, maintain routines.")
    elif phase == "Triggering Event":
        st.warning("🟡 **Goal:** Manage Environment. **Action:** Remove trigger if possible, validate feelings.")
    elif phase == "Escalation":
        st.error("🟠 **Goal:** Provide Support. **Action:** Co-regulation, Directive statements, Leave the room.")
    elif phase == "Outburst":
        st.error("🔴 **Goal:** Safety. **Action:** Remove the audience, Remove the target, Physical safety.")
    elif phase == "Recovery":
        st.info("🔵 **Goal:** Teach. **Action:** Life Space Interview (LSI).")

# ==========================================
# PAGE: MODULE 3 - DE-ESCALATION
# ==========================================
elif st.session_state.module == "Mod3":
    st.markdown("<div class='main-header'>Module 3: De-Escalation Tools</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### The 'Behavior Support' Toolbox")
        with st.expander("🛠️ Prompting"):
            st.write("Signaling to a child to begin a desired behavior. (e.g., pointing to the schedule).")
        with st.expander("🛠️ Hurdle Help"):
            st.write("Assisting with the first few steps of a frustrating task to get momentum going.")
        with st.expander("🛠️ Caring Gesture"):
            st.write("A smile, a hand on the shoulder (if appropriate), or a kind word to build connection.")
        with st.expander("🛠️ Proximity"):
            st.write("Moving near the child to provide structure and support (not to threaten).")
        with st.expander("🛠️ Redirection"):
            st.write("Shifting focus to a new, neutral, or positive activity.")

    with col2:
        st.markdown("### 🛑 Power Struggles")
        st.markdown("""
        <div class='warning-box'>
        <b>The Trap:</b> You demand compliance -> Child resists -> You increase pressure -> Child explodes.
        <br><br>
        <b>The Solution: DROP THE ROPE.</b>
        </div>
        """, unsafe_allow_html=True)
        st.write("1. Take a deep breath.")
        st.write("2. Validate the feeling ('I see you're angry').")
        st.write("3. Give choices, not orders.")
        st.write("4. Step back.")

    st.markdown("---")
    st.markdown("### 🧠 Knowledge Check")
    q3 = st.radio("A child is refusing to do homework because it looks too hard. You sit down and say 'Let's do the first problem together.' What technique is this?", 
        ["Prompting", "Hurdle Help", "Redirection"])
    
    if q3 == "Hurdle Help":
        st.success("Correct! You lowered the hurdle.")
    elif q3:
        st.error("Incorrect. Try again.")

# ==========================================
# PAGE: MODULE 4 - OUTBURST
# ==========================================
elif st.session_state.module == "Mod4":
    st.markdown("<div class='main-header'>Module 4: Managing The Outburst</div>", unsafe_allow_html=True)
    
    st.error("⚠️ **CRITICAL:** The goal here is SAFETY, not compliance.")
    
    st.markdown("### 4.1 Non-Verbal Co-Regulation")
    st.write("When a child is in the Survival Brain, words often just add noise. Use your body.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/5556/5556468.png", width=80)
        st.markdown("**1. Silence**")
        st.caption("Stop talking. Give time.")
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/64/64572.png", width=80)
        st.markdown("**2. Distance**")
        st.caption("Give extra personal space.")
    with col3:
        st.image("https://cdn-icons-png.flaticon.com/512/17/17736.png", width=80)
        st.markdown("**3. Stance**")
        st.caption("Open hands, turned 45 degrees.")

    st.markdown("---")
    st.markdown("### 4.2 The Elements of Violence")
    st.write("To stop violence, you must remove one of these 4 elements:")
    
    cols = st.columns(4)
    cols[0].metric("The Spark", "Trigger", delta="- Remove it")
    cols[1].metric("The Target", "You/Other", delta="- Step Away")
    cols[2].metric("The Weapon", "Object", delta="- Remove it")
    cols[3].metric("Motivation", "Stress", delta="- Co-regulate")

# ==========================================
# PAGE: MODULE 5 - LSI
# ==========================================
elif st.session_state.module == "Mod5":
    st.markdown("<div class='main-header'>Module 5: The Life Space Interview (LSI)</div>", unsafe_allow_html=True)
    
    st.write("The LSI is a therapeutic conversation to turn the crisis into a learning experience.")
    
    st.markdown("### The Acronym: I E S C A P E")
    
    lsi_step = st.selectbox("Select a step to learn more:", 
        ["I - Isolate", "E - Explore", "S - Summarize", "C - Connect", "A - Alternative", "P - Plan", "E - Enter"])
    
    if "I - Isolate" in lsi_step:
        st.info("**I - Isolate the conversation.** Find a quiet place. Ensure the child is calm (Baseline).")
    elif "E - Explore" in lsi_step:
        st.info("**E - Explore the child's point of view.** Ask 'What happened?' Listen without judgment.")
    elif "S - Summarize" in lsi_step:
        st.info("**S - Summarize feelings and content.** 'So, you got angry because he took your pen?'")
    elif "C - Connect" in lsi_step:
        st.success("**C - Connect trigger to behavior.** 'When you felt angry (Feeling), you threw the chair (Behavior).'")
    elif "A - Alternative" in lsi_step:
        st.warning("**A - Alternative responses.** 'What could you do next time you feel that angry instead of throwing a chair?'")
    elif "P - Plan" in lsi_step:
        st.info("**P - Plan/Practice.** 'Let's practice saying 'I need a break'.'")
    elif "E - Enter" in lsi_step:
        st.info("**E - Enter back into the routine.** Welcome them back to the group.")

    st.markdown("### ✍️ LSI Fix-It")
    st.write("Scenario: A staff member says: *'You threw the chair because you are a bad kid.'*")
    user_fix = st.text_input("Rewrite this to be a therapeutic 'Connect' statement:")
    
    if st.button("Check My Answer"):
        feedback = get_ai_tutor(f"Rate this LSI Connect statement replacement: '{user_fix}'. Compare it to 'You threw the chair because you were angry.'")
        st.write(feedback)

# ==========================================
# PAGE: ROLEPLAY DOJO
# ==========================================
elif st.session_state.module == "Dojo":
    st.markdown("<div class='main-header'>🥋 AI Roleplay Dojo</div>", unsafe_allow_html=True)
    st.markdown("Test your skills against a simulated child in crisis.")
    
    # Scene Setup
    if not st.session_state.roleplay_active:
        scenario_choice = st.selectbox("Choose a Scenario:", 
            ["The Video Game Refusal (Escalation)", 
             "The Dinner Argument (Defiance)", 
             "The Homework Meltdown (Fear-based)"])
        
        if st.button("Start Simulation"):
            st.session_state.roleplay_active = True
            st.session_state.roleplay_history = []
            st.session_state.current_scenario = scenario_choice
            
            # Initial AI Message
            initial_msg = "I hate this place! You can't make me do anything! (Slams door)"
            st.session_state.roleplay_history.append({"role": "Child", "content": initial_msg})
            st.rerun()
            
    else:
        st.success(f"**Scenario:** {st.session_state.current_scenario}")
        
        # Chat Display
        for msg in st.session_state.roleplay_history:
            if msg['role'] == "Child":
                st.markdown(f"**🧒 Child:** {msg['content']}")
            else:
                st.markdown(f"**🛡️ You:** {msg['content']}")
        
        # Input
        with st.form("roleplay_input"):
            user_text = st.text_input("Your Response (Use TCI techniques):")
            submitted = st.form_submit_button("Send")
            
            if submitted and user_text:
                st.session_state.roleplay_history.append({"role": "Staff", "content": user_text})
                
                with st.spinner("Child is reacting..."):
                    ai_reply = run_roleplay(user_text, st.session_state.current_scenario)
                    st.session_state.roleplay_history.append({"role": "Child", "content": ai_reply})
                st.rerun()

        if st.button("End Simulation & Reset"):
            st.session_state.roleplay_active = False
            st.session_state.roleplay_history = []
            st.rerun()

# ==========================================
# PAGE: EXAM
# ==========================================
elif st.session_state.module == "Exam":
    st.markdown("<div class='main-header'>📝 Final Certification Exam</div>", unsafe_allow_html=True)
    
    questions = {
        "1. What is the goal of crisis intervention?": ["Compliance", "Support & Teach", "Punishment"],
        "2. Which brain is in charge during an outburst?": ["Thinking Brain", "Emotional Brain", "Survival Brain"],
        "3. What is the first question you ask yourself?": ["What did he do?", "What am I feeling?", "Who is watching?"],
        "4. In the Stress Model, where should you intervene?": ["Trigger", "Escalation", "Outburst"],
        "5. 'Drop the Rope' is used for:": ["Safety", "Power Struggles", "Hygiene"],
        "6. In 'I ESCAPE', what is 'C'?": ["Control", "Connect", "Contain"],
        "7. Can you restrain a child for property destruction?": ["Yes", "No (Unless imminent safety risk)", "Only if expensive"],
        "8. Positional Asphyxia affects:": ["Digestion", "Breathing/Respiration", "Movement"]
    }
    
    correct_answers = ["Support & Teach", "Survival Brain", "What am I feeling?", "Escalation", "Power Struggles", "Connect", "No (Unless imminent safety risk)", "Breathing/Respiration"]
    
    with st.form("final_exam"):
        answers = []
        for q, opts in questions.items():
            answers.append(st.radio(q, opts))
            st.markdown("---")
            
        submit_exam = st.form_submit_button("Submit Final Exam")
        
        if submit_exam:
            score = 0
            for i, ans in enumerate(answers):
                if ans == correct_answers[i]:
                    score += 1
            
            st.session_state.quiz_score = score
            
            if score >= 7:
                st.balloons()
                st.success(f"🎉 PASSED! Score: {score}/8")
                st.markdown("""
                <div class='success-box'>
                <b>CERTIFICATE OF COMPLETION</b><br>
                This user has demonstrated competency in Therapeutic Crisis Intervention concepts.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error(f"Score: {score}/8. You need 7 to pass. Please review the modules.")
