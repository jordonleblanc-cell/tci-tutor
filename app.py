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
    .concept-card { background-color: #F3F4F6; color: #1F2937; padding: 20px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); margin-bottom: 20px; }
    .stButton>button { width: 100%; border-radius: 5px; }
    .success-box { background-color: #D1FAE5; padding: 15px; border-radius: 5px; color: #065F46; }
    .warning-box { background-color: #FEE2E2; padding: 15px; border-radius: 5px; color: #991B1B; }
</style>
""", unsafe_allow_html=True)

# --- TCI KNOWLEDGE BASE (EXTRACTED FROM UPLOADED PDF) ---
TCI_MANUAL_CONTENT = """
CORE DEFINITIONS:
1. THE GOAL OF TCI: To prevent and de-escalate potential crises, build capacity of staff to manage aggression, reduce injury, and create a learning culture.
2. SETTING CONDITIONS: Anything that makes challenging behavior or traumatic stress responses more or less likely to occur. (e.g., hot room, hungry child, chaotic environment).
3. PAIN-BASED BEHAVIOR: Behavior is an expression of need. Aggression, rigidity, withdrawal, impulsive outbursts, and self-injury are often expressions of trauma and pain.
4. THE TRIUNE BRAIN:
    - Thinking Brain (Neocortex): Reasoning, language. OFFLINE during crisis.
    - Emotional Brain (Limbic/Amygdala): The "Sentry" scans for danger. Center for emotions.
    - Survival Brain (Brain Stem): Reptilian brain. Responsible for Fight, Flight, Freeze. IN CHARGE during crisis.
5. THE THERAPEUTIC MILIEU (5 SPACES):
    - Ideological: The philosophy (Learning > Control).
    - Physical: The environment (Safe, clean, calming).
    - Cultural: Accepting/celebrating identity.
    - Social: Relationships and routines.
    - Emotional: Safety and emotional competence.
6. THE 6 DOMAINS OF TCI SYSTEM:
    1) Leadership & Program Support
    2) Child & Family Inclusion
    3) Clinical Participation
    4) Supervision & Post-Crisis Response
    5) Training & Competency Standards
    6) Documentation, Incident Monitoring & Feedback
7. THE STRESS MODEL OF CRISIS (PHASES):
    - Baseline (Normal state)
    - Triggering Event (Agitation)
    - Escalation (Aggression/Defiance - INTERVENE HERE)
    - Outburst (Violence - Safety Interventions)
    - Recovery (Return to baseline - LSI)
8. LIFE SPACE INTERVIEW (LSI) - "I ESCAPE":
    - I: Isolate the conversation (Quiet place).
    - E: Explore child's point of view.
    - S: Summarize feelings and content.
    - C: Connect trigger to behavior ("When X happened, you felt Y, so you did Z").
    - A: Alternative responses (What to do next time).
    - P: Plan/Practice.
    - E: Enter back into routine.
"""

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

# --- NAVIGATION CONSTANTS ---
nav_options = {
    "Home": "🏠 Dashboard",
    "Mod1": "🧠 1. Prevention & Domains",
    "Mod2": "📈 2. Stress Model & Curve",
    "Mod3": "🛑 3. De-Escalation Tools",
    "Mod4": "🔥 4. The Outburst",
    "Mod5": "🌱 5. Recovery (LSI)",
    "Dojo": "🥋 AI Roleplay Dojo",
    "Exam": "📝 Final Exam"
}
nav_keys = list(nav_options.keys())

# --- HELPER FUNCTIONS ---

def render_navigation_footer():
    """Renders Previous/Next buttons at the bottom of pages."""
    st.markdown("---")
    col_prev, col_spacer, col_next = st.columns([1, 4, 1])
    
    current_idx = nav_keys.index(st.session_state.module)
    
    with col_prev:
        if current_idx > 0:
            if st.button("⬅️ Previous Module", key="prev_btn"):
                st.session_state.module = nav_keys[current_idx - 1]
                st.rerun()
    
    with col_next:
        if current_idx < len(nav_keys) - 1:
            if st.button("Next Module ➡️", key="next_btn"):
                st.session_state.module = nav_keys[current_idx + 1]
                st.rerun()

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
    """Tutor Logic trained on specific PDF content"""
    if not api_key: return "⚠️ Please connect API Key."
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        # INJECT THE PDF CONTENT INTO SYSTEM PROMPT
        full_prompt = f"""
        You are a master TCI (Therapeutic Crisis Intervention) instructor. 
        You MUST base your answers on the following official TCI definitions:
        
        {TCI_MANUAL_CONTENT}
        
        User Question: {prompt}
        
        Task: Provide a concise, encouraging answer strictly adhering to the definitions above.
        """
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

def run_roleplay(user_input, scenario):
    """Handles the back-and-forth simulation using TCI principles."""
    if not api_key: return "⚠️ API Key needed."
    
    model = genai.GenerativeModel("gemini-2.0-flash")
    
    history_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.roleplay_history])
    
    system_prompt = f"""
    You are roleplaying a traumatized child in a residential facility.
    
    CONTEXT (TCI PRINCIPLES):
    - You are displaying "Pain-Based Behavior" (aggression/defiance is due to trauma/pain, not badness).
    - You are currently in the 'Escalation' or 'Outburst' phase of the Stress Model.
    - Your 'Thinking Brain' is offline; you are in 'Survival Brain' (Fight/Flight).
    
    Scenario: {scenario}
    
    Rules for you (The Child):
    1. Act your age (approx 12-14).
    2. If the user (Staff) uses "Co-Regulation" strategies (silence, distance, validating feelings), you de-escalate.
    3. If the user argues, lectures, or threatens (Power Struggle), you escalate significantly.
    4. Keep responses short (1-2 sentences).
    
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

# --- NAVIGATION SIDEBAR ---
st.sidebar.title("📍 TCI Navigator")

# Logic to sync sidebar with session state
if st.session_state.module not in nav_keys:
    st.session_state.module = "Home"

current_idx = nav_keys.index(st.session_state.module)

# The sidebar radio button
selected_nav = st.sidebar.radio(
    "Go to:", 
    nav_keys, 
    index=current_idx,
    format_func=lambda x: nav_options[x],
    key="nav_radio"
)

# If the user clicked the radio button, update state and rerun
if selected_nav != st.session_state.module:
    st.session_state.module = selected_nav
    st.rerun()

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
        * **Prevention:** How to set up a safe environment and the **6 Domains**.
        * **De-escalation:** Verbal tools to calm a crisis.
        * **Safety:** Protecting the child and yourself.
        * **Recovery:** Turning crisis into a learning moment using **I ESCAPE**.
        """)
        
        st.info("💡 **Tip:** Use the 'AI Roleplay Dojo' to practice your skills against a simulated child before the exam!")

    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/2921/2921226.png", width=150)
        st.markdown("**Status:** In Training")

    render_navigation_footer()

# ==========================================
# PAGE: MODULE 1 - PREVENTION
# ==========================================
elif st.session_state.module == "Mod1":
    st.markdown("<div class='main-header'>Module 1: Prevention & The Milieu</div>", unsafe_allow_html=True)
    
    st.markdown("### 1.1 The TCI System: The Six Domains")
    st.write("To effectively prevent crises, the organization must attend to these 6 domains:")
    
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.markdown("""
        * **1. Leadership & Support:** Clear philosophy (Learning > Control).
        * **2. Child & Family Inclusion:** Active participation in decisions.
        * **3. Clinical Participation:** Individual Crisis Support Plans (ICSP).
        """)
    with col_d2:
        st.markdown("""
        * **4. Supervision & Post-Crisis:** Coaching and debriefing.
        * **5. Training:** Competency standards.
        * **6. Documentation:** Incident monitoring and feedback.
        """)

    st.markdown("---")
    st.markdown("### 1.2 The Therapeutic Milieu")
    st.write("The 'Milieu' is the living environment. We must manage 5 distinct spaces.")
    
    tabs = st.tabs(["🏛️ Ideological", "🛋️ Physical", "🎭 Cultural", "🤝 Social", "❤️ Emotional"])
    
    with tabs[0]:
        st.success("**Ideological:** The philosophy. Do we value learning over control? Do we believe children do well if they can?")
    with tabs[1]:
        st.warning("**Physical:** The setting. Lighting, noise, clutter. Is it safe? Does it feel safe?")
    with tabs[2]:
        st.info("**Cultural:** Accepting and celebrating differences. Understanding the child's worldview.")
    with tabs[3]:
        st.error("**Social:** Relationships, routines, and group dynamics. Peer interactions.")
    with tabs[4]:
        st.success("**Emotional:** Safety. Does the child feel safe to express feelings without ridicule?")

    st.markdown("---")
    st.markdown("### 1.3 The Triune Brain")
    
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
        <h4>❤️ The Emotional Brain (Limbic/Amygdala)</h4>
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
        st.info("📝 **Pain-Based Behavior:**\n\nAggression, withdrawal, and defiance are often expressions of trauma and pain. \n\n**Setting Conditions:** Anything that makes these behaviors more or less likely to occur.")

    render_navigation_footer()

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
        st.success("🟢 **Phase:** Baseline\n\n**Goal:** Support Environment.\n\n**Action:** Build relationships, maintain routines.")
    elif phase == "Triggering Event":
        st.warning("🟡 **Phase:** Triggering Event\n\n**Goal:** Manage Environment.\n\n**Action:** Remove trigger if possible, validate feelings.")
    elif phase == "Escalation":
        st.error("🟠 **Phase:** Escalation (Agitation)\n\n**Goal:** Provide Support.\n\n**Action:** Co-regulation, Directive statements, Leave the room. **INTERVENE HERE!**")
    elif phase == "Outburst":
        st.error("🔴 **Phase:** Outburst (Violence)\n\n**Goal:** Safety.\n\n**Action:** Remove the audience, Remove the target, Physical safety.")
    elif phase == "Recovery":
        st.info("🔵 **Phase:** Recovery\n\n**Goal:** Teach.\n\n**Action:** Life Space Interview (LSI).")

    render_navigation_footer()

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

    render_navigation_footer()

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

    render_navigation_footer()

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

    render_navigation_footer()

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

    render_navigation_footer()

# ==========================================
# PAGE: EXAM
# ==========================================
elif st.session_state.module == "Exam":
    st.markdown("<div class='main-header'>📝 Comprehensive Practice Exam</div>", unsafe_allow_html=True)
    st.info("ℹ️ **Note:** This is a practice tool. The official TCI certification exam must be taken in person.")
    st.write("Answer all 50 questions. Passing score: 80% (40/50).")

    # List of 50 Questions
    exam_questions = [
        {"q": "1. What is the primary goal of the TCI system?", 
         "options": ["To enforce strict discipline", "To reduce high-risk interventions and teach coping skills", "To eliminate all emotions"], 
         "correct": "To reduce high-risk interventions and teach coping skills"},
        
        {"q": "2. Anything that makes challenging behavior more or less likely to occur is called a:", 
         "options": ["Trigger", "Setting Condition", "Crisis"], 
         "correct": "Setting Condition"},
        
        {"q": "3. Aggression, withdrawal, and defiance are often expressions of:", 
         "options": ["Bad character", "Pain or trauma (Pain-Based Behavior)", "Lack of intelligence"], 
         "correct": "Pain or trauma (Pain-Based Behavior)"},
        
        {"q": "4. Which part of the Triune Brain is responsible for reasoning and language?", 
         "options": ["Survival Brain", "Emotional Brain", "Thinking Brain (Neocortex)"], 
         "correct": "Thinking Brain (Neocortex)"},
        
        {"q": "5. During a crisis, the Thinking Brain is usually:", 
         "options": ["Fully functional", "Offline", "In charge"], 
         "correct": "Offline"},
        
        {"q": "6. Which part of the brain is the 'Sentry' that scans for danger?", 
         "options": ["Amygdala (Emotional Brain)", "Prefrontal Cortex", "Brain Stem"], 
         "correct": "Amygdala (Emotional Brain)"},
        
        {"q": "7. Which part of the brain controls Fight, Flight, or Freeze?", 
         "options": ["Thinking Brain", "Survival Brain (Brain Stem)", "Emotional Brain"], 
         "correct": "Survival Brain (Brain Stem)"},
        
        {"q": "8. The 5 spaces of the Therapeutic Milieu are: Ideological, Physical, Cultural, Social, and...", 
         "options": ["Financial", "Emotional", "Educational"], 
         "correct": "Emotional"},
        
        {"q": "9. Which TCI Domain involves the philosophy that learning is more important than control?", 
         "options": ["Leadership & Program Support", "Documentation", "Clinical Participation"], 
         "correct": "Leadership & Program Support"},
        
        {"q": "10. In the Stress Model of Crisis, what follows the 'Triggering Event'?", 
         "options": ["Recovery", "Escalation", "Outburst"], 
         "correct": "Escalation"},
        
        {"q": "11. At which stage of the Stress Model should staff intervene to prevent violence?", 
         "options": ["Outburst", "Escalation", "Recovery"], 
         "correct": "Escalation"},
        
        {"q": "12. What is the first of the 'Four Questions' you ask yourself in a crisis?", 
         "options": ["What did the child do?", "What am I feeling now?", "How do I stop this?"], 
         "correct": "What am I feeling now?"},
        
        {"q": "13. What is the second of the 'Four Questions'?", 
         "options": ["What does the child feel, need, or want?", "Is anyone watching?", "Who started it?"], 
         "correct": "What does the child feel, need, or want?"},
        
        {"q": "14. Nonverbal active listening includes:", 
         "options": ["Lecturing", "Silence, nods, and facial expression", "Asking 'Why?'"], 
         "correct": "Silence, nods, and facial expression"},
        
        {"q": "15. 'Hurdle Help' is defined as:", 
         "options": ["Doing the work for the child", "Assisting with the first few steps of a frustrating task", "ignoring the child"], 
         "correct": "Assisting with the first few steps of a frustrating task"},
        
        {"q": "16. 'Prompting' is:", 
         "options": ["A gentle signal (gesture/words) to remind a child of expectations", "Ordering a child to stop", "Threatening consequences"], 
         "correct": "A gentle signal (gesture/words) to remind a child of expectations"},
        
        {"q": "17. 'Proximity' as a support technique means:", 
         "options": ["Moving far away", "Moving closer to provide support/safety", "Touching the child"], 
         "correct": "Moving closer to provide support/safety"},
        
        {"q": "18. 'Redirection' involves:", 
         "options": ["Shifting focus to a neutral/positive activity", "Punishing the behavior", "Analyzing the behavior"], 
         "correct": "Shifting focus to a neutral/positive activity"},
        
        {"q": "19. A 'Caring Gesture' is:", 
         "options": ["A bribe", "A brief act/word to build connection and reduce stress", "A reward for good behavior"], 
         "correct": "A brief act/word to build connection and reduce stress"},
        
        {"q": "20. When a power struggle begins, the best strategy is to:", 
         "options": ["Win the argument", "Drop the rope", "Assert authority loudly"], 
         "correct": "Drop the rope"},
        
        {"q": "21. During an outburst, your eye contact should be:", 
         "options": ["Staring intensely", "Intermittent and non-threatening", "Completely avoided"], 
         "correct": "Intermittent and non-threatening"},
        
        {"q": "22. The four elements of a potentially violent situation are: Spark, Target, Weapon, and...", 
         "options": ["Motivation/Stress", "Opportunity", "Location"], 
         "correct": "Motivation/Stress"},
        
        {"q": "23. To stop violence, you must remove:", 
         "options": ["All four elements", "At least one element", "Only the weapon"], 
         "correct": "At least one element"},
        
        {"q": "24. In Crisis Co-Regulation, the 'Think' step involves:", 
         "options": ["Planning punishment", "Asking the 4 Questions", "Calling the police"], 
         "correct": "Asking the 4 Questions"},
        
        {"q": "25. In Crisis Co-Regulation, the 'Do' step involves:", 
         "options": ["Deep breath, step back, neutral stance", "Grabbing the child", "Yelling 'Stop!'"], 
         "correct": "Deep breath, step back, neutral stance"},
        
        {"q": "26. The goal of the LSI (Life Space Interview) is to:", 
         "options": ["Punish the child", "Return to normal and teach new skills", "Document the incident"], 
         "correct": "Return to normal and teach new skills"},
        
        {"q": "27. In the acronym I ESCAPE, 'I' stands for:", 
         "options": ["Ignore", "Isolate the conversation", "Investigate"], 
         "correct": "Isolate the conversation"},
        
        {"q": "28. In I ESCAPE, the first 'E' stands for:", 
         "options": ["Explore the child's point of view", "Enter the room", "Evaluate the risk"], 
         "correct": "Explore the child's point of view"},
        
        {"q": "29. In I ESCAPE, 'S' stands for:", 
         "options": ["Silence", "Summarize feelings and content", "Stop talking"], 
         "correct": "Summarize feelings and content"},
        
        {"q": "30. In I ESCAPE, 'C' stands for:", 
         "options": ["Control the child", "Connect trigger to behavior", "Correct the behavior"], 
         "correct": "Connect trigger to behavior"},
        
        {"q": "31. In I ESCAPE, 'A' stands for:", 
         "options": ["Alternative responses", "Ask for help", "Argue"], 
         "correct": "Alternative responses"},
        
        {"q": "32. In I ESCAPE, 'P' stands for:", 
         "options": ["Plan/Practice", "Punish", "Promise"], 
         "correct": "Plan/Practice"},
        
        {"q": "33. In I ESCAPE, the last 'E' stands for:", 
         "options": ["End the shift", "Enter back into the routine", "Escalate"], 
         "correct": "Enter back into the routine"},
        
        {"q": "34. Physical restraint should ONLY be used when:", 
         "options": ["The child is disrespectful", "There is imminent risk of physical harm", "The child refuses to move"], 
         "correct": "There is imminent risk of physical harm"},
        
        {"q": "35. Restraint should NEVER be used for:", 
         "options": ["Safety", "Compliance or discipline", "Self-defense"], 
         "correct": "Compliance or discipline"},
        
        {"q": "36. Positional Asphyxia is:", 
         "options": ["A panic attack", "Fatal respiratory arrest due to body position", "A minor injury"], 
         "correct": "Fatal respiratory arrest due to body position"},
        
        {"q": "37. You should NEVER put weight on a child's:", 
         "options": ["Arms", "Chest, back, or stomach", "Legs"], 
         "correct": "Chest, back, or stomach"},
        
        {"q": "38. If a child says 'I can't breathe' during a restraint, you must:", 
         "options": ["Ignore it if they are talking", "Release or adjust immediately", "Wait 5 minutes"], 
         "correct": "Release or adjust immediately"},
        
        {"q": "39. During a restraint, you must monitor:", 
         "options": ["Skin color and respiration", "The time only", "The other children"], 
         "correct": "Skin color and respiration"},
        
        {"q": "40. A 'Setting Condition' in the Ideological space would be:", 
         "options": ["A cluttered room", "A culture of learning vs. control", "A hungry child"], 
         "correct": "A culture of learning vs. control"},
        
        {"q": "41. Which is an example of an Emotional Space setting condition?", 
         "options": ["Personal belongings", "Sense of safety/trust", "Lighting"], 
         "correct": "Sense of safety/trust"},
        
        {"q": "42. 'Reflective Practice' means:", 
         "options": ["Mirroring the child", "Thinking about one's actions to improve learning", "Ignoring mistakes"], 
         "correct": "Thinking about one's actions to improve learning"},
        
        {"q": "43. The 'Target' in a violent situation is usually:", 
         "options": ["The weapon", "The staff member or another child", "The trigger"], 
         "correct": "The staff member or another child"},
        
        {"q": "44. 'Drop the Rope' helps to avoid:", 
         "options": ["Falling down", "Power Struggles", "Documentation"], 
         "correct": "Power Struggles"},
        
        {"q": "45. When we validate a child's feelings, we are using:", 
         "options": ["Active Listening", "Prompting", "Restraint"], 
         "correct": "Active Listening"},
        
        {"q": "46. Emotional First Aid goals include: Provide support, Resolve immediate crisis, and...", 
         "options": ["Keep the child in the activity", "Send the child to bed", "Isolate the child"], 
         "correct": "Keep the child in the activity"},
        
        {"q": "47. The 'Conflict Cycle' describes how:", 
         "options": ["Stress leads to feelings, behavior, and adult response", "Children fight each other", "Staff argue with supervisors"], 
         "correct": "Stress leads to feelings, behavior, and adult response"},
        
        {"q": "48. Individual Crisis Support Plans (ICSP) should be reviewed:", 
         "options": ["Never", "After every crisis or regularly", "Once a year only"], 
         "correct": "After every crisis or regularly"},
        
        {"q": "49. Which statement is a 'Connect' statement in LSI?", 
         "options": ["'You are grounded.'", "'When he took your toy, you felt mad, so you hit him.'", "'Don't do that again.'"], 
         "correct": "'When he took your toy, you felt mad, so you hit him.'"},
        
        {"q": "50. A child in the 'Recovery' phase needs:", 
         "options": ["Strict punishment", "The Life Space Interview (LSI)", "To be ignored"], 
         "correct": "The Life Space Interview (LSI)"}
    ]
    
    with st.form("final_exam_50"):
        user_answers = []
        for item in exam_questions:
            # index=None ensures no answer is pre-selected
            ans = st.radio(item["q"], item["options"], index=None, key=item["q"])
            user_answers.append(ans)
            st.markdown("---")
            
        submit_exam = st.form_submit_button("Submit Final Exam")
        
        if submit_exam:
            score = 0
            unanswered = 0
            for i, ans in enumerate(user_answers):
                if ans is None:
                    unanswered += 1
                elif ans == exam_questions[i]["correct"]:
                    score += 1
            
            st.session_state.quiz_score = score
            
            if unanswered > 0:
                st.warning(f"⚠️ You left {unanswered} questions blank. Please answer all questions.")
            elif score >= 40: # 80% of 50 is 40
                st.balloons()
                st.success(f"🎉 PASSED! Score: {score}/50 ({(score/50)*100}%)")
                st.markdown("""
                <div class='success-box'>
                <b>PRACTICE EXAM COMPLETE</b><br>
                You have demonstrated competency in TCI concepts and are ready for the real in-person exam.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error(f"Score: {score}/50 ({(score/50)*100}%). You need 40 to pass. Please review the modules.")

    render_navigation_footer()
