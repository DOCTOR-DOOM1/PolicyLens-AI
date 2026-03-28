import streamlit as st
import time
from pdf_generator import generate_policy_pdf
from rag_engine import analyze_eligibility, ask_policylens, compare_policies

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="PolicyLens AI", page_icon="🏛️", layout="wide", initial_sidebar_state="expanded")

if 'nav_radio' not in st.session_state:
    st.session_state.nav_radio = "🏠 Home"

def change_page(page_name):
    st.session_state.nav_radio = page_name

# --- CUSTOM CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@500;600;700;800&display=swap');

    /* Global Typography */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #1e293b;
    }
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif;
        color: #0f172a;
        font-weight: 700;
    }
    
    /* Main Background */
    .stApp {
        background-color: #f8fafc;
        background-image: radial-gradient(at 0% 0%, hsla(253,16%,7%,0.03) 0, transparent 50%), 
                          radial-gradient(at 50% 0%, hsla(225,39%,30%,0.03) 0, transparent 50%), 
                          radial-gradient(at 100% 0%, hsla(339,49%,30%,0.03) 0, transparent 50%);
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid #1e293b;
    }
    [data-testid="stSidebar"] * {
        color: #f1f5f9 !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        padding: 10px 15px;
        border-radius: 8px;
        transition: all 0.2s ease;
        margin-bottom: 5px;
    }
    [data-testid="stSidebar"] .stRadio label:hover {
        background-color: #1e293b;
    }

    /* Primary Button Styling */
    .stButton > button, 
    div[data-testid*="stButton"] > button,
    button[data-testid*="baseButton"] {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 5px 24px !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 4px 6px -1px rgba(99, 102, 241, 0.4), 0 2px 4px -1px rgba(99, 102, 241, 0.2) !important;
        transition: all 0.3s ease !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.2) !important;
    }
    .stButton > button p, 
    .stButton > button span,
    .stButton > button div,
    div[data-testid*="stButton"] > button p,
    button[data-testid*="baseButton"] p,
    button[data-testid*="baseButton"] div,
    .stButton > button *,
    div[data-testid*="stButton"] > button * {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    .stButton > button:hover,
    div[data-testid*="stButton"] > button:hover,
    button[data-testid*="baseButton"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.5), 0 4px 6px -2px rgba(99, 102, 241, 0.3) !important;
    }
    .stButton > button:active,
    div[data-testid*="stButton"] > button:active,
    button[data-testid*="baseButton"]:active {
        transform: translateY(0px) !important;
    }

    /* Cards / Containers */
    .premium-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(226, 232, 240, 0.8);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
    }
    .premium-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }
    
    /* Card Badge/Tag */
    .card-badge {
        background: #e0e7ff;
        color: #4338ca;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        display: inline-block;
        margin-right: 8px;
        margin-top: 10px;
    }

    /* Input Fields styling */
    .stTextInput input, .stSelectbox div[data-baseweb="select"], .stNumberInput input {
        border-radius: 8px !important;
        border: 1px solid #cbd5e1 !important;
        padding: 5px !important;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
        transition: all 0.2s ease !important;
        color: #1e293b !important;
    }
    .stTextInput input:focus, .stSelectbox > div > div:focus-within, .stNumberInput input:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2) !important;
    }

    /* Hero Section */
    .hero-title {
        background: linear-gradient(135deg, #0f172a 0%, #334155 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        line-height: 1.2 !important;
        margin-bottom: 1rem;
        font-family: 'Outfit', sans-serif;
    }
    .hero-subtitle {
        color: #475569;
        font-size: 1.2rem;
        line-height: 1.6;
        margin-bottom: 2rem;
        max-width: 800px;
    }

    /* Chat Messages */
    .stChatMessage {
        background: white;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        margin-bottom: 15px;
    }
    
    /* Divider */
    hr {
        border-color: #e2e8f0;
        margin: 2rem 0;
    }
    
    /* Fix for metric styling */
    [data-testid="stMetricValue"] {
        font-family: 'Outfit', sans-serif;
        color: #4f46e5;
        font-weight: 700;
        font-size: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; margin-bottom: 20px; font-size: 28px;'>🏛️ PolicyLens</h2>", unsafe_allow_html=True)
    
    # Navigation Radio
    page = st.radio(
        "Navigation",
        ["🏠 Home", "✨ Eligibility Checker", "🤖 AI Assistant", "⚖️ Compare Policies", "⚙️ Settings"],
        key="nav_radio",
        label_visibility="collapsed"
    )
    
    st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);">
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="width: 32px; height: 32px; background: linear-gradient(135deg, #6366f1, #4f46e5); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; color: white;">RS</div>
            <div>
                <div style="font-weight: 600; font-size: 14px; color: white;">Rahul Sharma</div>
                <div style="font-size: 12px; color: #94a3b8;">Pro Member</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- PAGE 1: HOME ---
if page == "🏠 Home":
    st.markdown("<h1 class='hero-title'>Discover Government Schemes You Deserve</h1>", unsafe_allow_html=True)
    st.markdown("<p class='hero-subtitle'>PolicyLens AI scans over <strong>2,500+ central & state schemes</strong> from government portals, automatically matches them to your unique profile, and explains benefits in simple, jargon-free language.</p>", unsafe_allow_html=True)
    
    col1, col2, col3, _ = st.columns([1, 1, 1, 1.5])
    with col1:
        st.button("✨ Check Eligibility", use_container_width=True, on_click=change_page, args=("✨ Eligibility Checker",))
    with col2:
        st.button("🎙️ Talk to Voice AI", use_container_width=True, on_click=change_page, args=("🤖 AI Assistant",))
    with col3:
        # A secondary looking button by wrapping it in standard Streamlit button but custom text
        st.button("⚖️ Compare Schemes", use_container_width=True, on_click=change_page, args=("⚖️ Compare Policies",))
        
    st.divider()
    
    
    # Global Search
    st.markdown("<h3 style='margin-bottom: 15px;'>Quick Search</h3>", unsafe_allow_html=True)
    search_col, btn_col = st.columns([4, 1])
    with search_col:
        search_query = st.text_input("Search", placeholder="Search for 'PM Awas Yojana', 'health insurance', 'farmer subsidy'...", label_visibility="collapsed")
    with btn_col:
        search_btn = st.button("Search Database", use_container_width=True)
        
    if search_btn and search_query:
        with st.spinner("Searching Local Policies..."):
            ans = ask_policylens(search_query)
        st.markdown(f"<div class='premium-card' style='margin-top: 15px;'>{ans}</div>", unsafe_allow_html=True)

# --- PAGE 2: ELIGIBILITY CHECKER ---
elif page == "✨ Eligibility Checker":
    st.markdown("<h1 style='margin-bottom: 10px;'>Intelligent Eligibility Match</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #475569; margin-bottom: 30px;'>Fill in your details below. Our RAG engine will semantically match your profile against thousands of local and central policy documents.</p>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #334155; font-size: 1.2rem; margin-bottom: 20px;'>👤 Personal Information</h3>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            full_name = st.text_input("Full Name", "Rahul Sharma")
            age = st.number_input("Age", min_value=18, max_value=100, value=32)
        with c2:
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            category = st.selectbox("Category", ["General", "OBC", "SC", "ST"])
        with c3:
            marital_status = st.selectbox("Marital Status", ["Married", "Single", "Divorced", "Widowed"])
            dependents = st.number_input("Dependents / Children", min_value=0, max_value=10, value=2)
        st.markdown("</div>", unsafe_allow_html=True)
            
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #334155; font-size: 1.2rem; margin-bottom: 20px;'>💼 Financial & Occupational Details</h3>", unsafe_allow_html=True)
        c4, c5, c6 = st.columns(3)
        with c4:
            income = st.selectbox("Annual Family Income", ["Under ₹1 Lakh", "₹1 - 3 Lakh", "₹3 - 6 Lakh", "₹6 - 8 Lakh", "Above ₹8 Lakh"])
            bpl = st.selectbox("Are you a BPL Card Holder?", ["No", "Yes"])
        with c5:
            occupation = st.selectbox("Primary Occupation", ["Private Employee", "Farmer", "Business/Entrepreneur", "Student", "Unemployed"])
            pucca_house = st.selectbox("Own a Pucca House?", ["No", "Yes"])
        with c6:
            state_res = st.selectbox("State of Residence", ["Central (All India)", "Delhi", "Maharashtra", "Uttar Pradesh", "Karnataka", "Tamil Nadu", "Other"])
            disability = st.selectbox("Disability Status", ["None", "Physical", "Visual", "Hearing"])
        st.markdown("</div>", unsafe_allow_html=True)

    # Collect data dictionary
    user_data = {
        "Full Name": full_name, "Age": str(age), "Gender": gender, "Category": category,
        "Marital Status": marital_status, "Dependents": str(dependents), "Income": income,
        "BPL Holder": bpl, "Occupation": occupation, "Pucca House": pucca_house,
        "State": state_res, "Disability": disability
    }
            
    if st.button("🚀 Run AI Match Analysis", use_container_width=True):
        st.markdown("<br>", unsafe_allow_html=True)
        with st.status("🧠 Analyzing policy vectors...", expanded=True) as status:
            st.write("Connecting to ChromaDB index...")
            time.sleep(0.5)
            st.write("Extracting semantic embeddings for user profile...")
            # CALL ENGINE HERE
            matched_schemes = analyze_eligibility(user_data)
            
            # Sort the schemes on relevance (highest match % first)
            try:
                matched_schemes.sort(key=lambda x: int(str(x.get('match', '0')).replace('%', '')), reverse=True)
            except Exception as e:
                pass
                
            status.update(label=f"Analysis Complete! Found {len(matched_schemes)} matching schemes.", state="complete", expanded=False)
            
        if len(matched_schemes) > 0:
            st.success(f"Analysis successful! Found **{len(matched_schemes)}** potential schemes for your profile.")
        else:
            st.warning("No scheme matches could be aggressively verified for your precise profile parameters at this time. Try 'Central (All India)'.")

        st.markdown("<br>", unsafe_allow_html=True)
        safe_name = full_name.replace(' ', '_')

        for idx, scheme in enumerate(matched_schemes):
            badge_html = "".join([f'<span class="card-badge">{b}</span>' for b in scheme['badges']])
            
            st.markdown(f"""
            <div class="premium-card" style="border-left: 5px solid {scheme['border_color']}; margin-bottom: 5px;">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <h3 style="margin-top:0; color: #0f172a;">{scheme['name']}</h3>
                    <span style="background: {scheme['bg_color']}; color: {scheme['text_color']}; padding: 4px 12px; border-radius: 20px; font-weight: bold;">{scheme['match']} Match</span>
                </div>
                <p style="color: #475569; margin-top: 10px; margin-bottom: 10px;">{scheme['description']}</p>
                {badge_html}
            </div>
            """, unsafe_allow_html=True)
            
            # Individual PDF Generator Button linked to this specific scheme context
            pdf_bytes = generate_policy_pdf(user_data, scheme['name'])
            
            dl_col1, dl_col2 = st.columns([3, 2])
            with dl_col1:
                st.markdown("<p style='font-size: 13px; color: #64748b; padding-top: 8px;'>Auto-fill this scheme's application draft using your AI Profile mapping</p>", unsafe_allow_html=True)
            with dl_col2:
                st.download_button(
                    label=f"📥 Download Draft ({scheme['name'][:10]}...)",
                    data=bytes(pdf_bytes),
                    file_name=f"Application_{safe_name}_{scheme['name'].split()[0]}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    key=f"dl_pdf_{idx}"
                )
            
            st.markdown("<br>", unsafe_allow_html=True)

# --- PAGE 3: COMPARE POLICIES ---
elif page == "⚖️ Compare Policies":
    st.markdown("<h1>⚖️ Policy Comparison Tool</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #475569; margin-bottom: 20px;'>Confused between two government schemes? Let the AI diff them strictly based on local database records.</p>", unsafe_allow_html=True)
    
    colA, colB = st.columns(2)
    with colA:
        policy_a = st.text_input("First Policy", placeholder="e.g. PM Awas Yojana (Urban)")
    with colB:
        policy_b = st.text_input("Second Policy", placeholder="e.g. PM Awas Yojana (Rural)")
        
    if st.button("Run Advanced Comparison", use_container_width=True) and policy_a and policy_b:
        with st.spinner("Extracting parameters and semantically isolating eligibility differences..."):
            diff_text = compare_policies(policy_a, policy_b)
        st.markdown(f"<div class='premium-card' style='margin-top: 20px;'>\n\n{diff_text}\n\n</div>", unsafe_allow_html=True)

# --- PAGE 4: AI ASSISTANT ---
elif page == "🤖 AI Assistant":
    st.markdown("<h1>PolicyVoice AI 🎙️</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #f0fdf4; border: 1px solid #bbf7d0; padding: 12px 20px; border-radius: 8px; margin-bottom: 20px; display: flex; align-items: center; gap: 10px;">
        <div style="width: 10px; height: 10px; background: #22c55e; border-radius: 50%; box-shadow: 0 0 10px #22c55e;"></div>
        <span style="color: #166534; font-weight: 500;">System Online — Powered by Groq, Cartesia Audio & Local Network RAG</span>
    </div>
    """, unsafe_allow_html=True)
    
    import os
    import subprocess
    import sys
    import time
    from livekit.api import AccessToken, VideoGrants
    from dotenv import load_dotenv
    load_dotenv()
    
    st.markdown("<h3 style='margin-top: 30px; margin-bottom: 15px;'>Native Voice Call</h3>", unsafe_allow_html=True)
    st.write("Toggle the switch below to connect to the backend AI and use your microphone natively within this dashboard.")
    
    if "agent_process" not in st.session_state:
        st.session_state.agent_process = None
    if "http_server" not in st.session_state:
        st.session_state.http_server = None
        
    on = st.toggle("Power On Backend Voice Agent", value=False)
    
    if on:
        if st.session_state.agent_process is None:
            # Start the agent using the correct venv python silently
            kwargs = {}
            if os.name == 'nt':
                kwargs['creationflags'] = 0x08000000 # CREATE_NO_WINDOW
                # Terminate any existing voice_agent.py processes to avoid port collisions
                subprocess.run('wmic process where "name=\'python.exe\' and commandline like \'%voice_agent.py%\'" call terminate', capture_output=True, shell=True)
            else:
                subprocess.run(['pkill', '-f', 'voice_agent.py'])
                
            kwargs["stdout"] = open("voice_agent_out.log", "w")
            kwargs["stderr"] = subprocess.STDOUT
            st.session_state.agent_process = subprocess.Popen([sys.executable, "voice_agent.py", "dev"], **kwargs)
            
            import socket
            s = socket.socket()
            s.bind(('', 0))
            free_port = s.getsockname()[1]
            s.close()
            st.session_state.widget_port = free_port
            
            # Start a local HTTP server on the free port to serve the HTML file (fixes Chrome mic blocking)
            st.session_state.http_server = subprocess.Popen([sys.executable, "-m", "http.server", str(free_port), "--bind", "127.0.0.1"], **kwargs)
            time.sleep(1) # wait for servers to boot
            
        # Generate WebRTC Token
        room_name = "policylens-room"
        try:
            grant = VideoGrants(room_join=True, room=room_name)
            access_token = AccessToken(
                os.getenv('LIVEKIT_API_KEY'),
                os.getenv('LIVEKIT_API_SECRET')
            )
            access_token.with_identity("User_UI")
            access_token.with_name("WebInterface")
            access_token.with_grants(grant)
            token = access_token.to_jwt()
            
            # Update the HTML file with real tokens before serving it
            with open("livekit_widget.html", "r") as f:
                html_code = f.read()
            html_code = html_code.replace("[[LIVEKIT_URL]]", os.getenv("LIVEKIT_URL"))
            html_code = html_code.replace("[[LIVEKIT_TOKEN]]", token)
            
            # We temporarily write the finalized widget out for the HTTP server to serve
            with open("livekit_widget_hosted.html", "w", encoding="utf-8") as f:
                f.write(html_code)
                
            iframe_html = f'<iframe src="http://127.0.0.1:{st.session_state.widget_port}/livekit_widget_hosted.html" style="width: 100%; border: none; height: 350px; border-radius: 12px; background: transparent;" allow="microphone"></iframe>'
            st.markdown(iframe_html, unsafe_allow_html=True)
            
            st.success("✅ Voice Backend Initialized seamlessly on localhost!")
        except Exception as e:
            st.error(f"Missing API parameters in .env file: {e}")
            
    else:
        if st.session_state.agent_process is not None:
            st.session_state.agent_process.terminate()
            st.session_state.agent_process = None
        if st.session_state.http_server is not None:
            st.session_state.http_server.terminate()
            st.session_state.http_server = None
        st.info("The agent is offline. Toggle the switch to begin.")

# --- PAGE 5: SETTINGS ---
elif page == "⚙️ Settings":
    st.markdown("<h1>AI Preferences & Localization</h1>", unsafe_allow_html=True)
    
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.markdown("<h3>🌐 Voice & Interface Language</h3>", unsafe_allow_html=True)
    st.write("Our AI engine dynamically adapts to the language spoken or selected here.")
    
    lang1, lang2, lang3, lang4 = st.columns(4)
    with lang1:
        st.button("🇮🇳 English (Default)", type="primary", use_container_width=True)
    with lang2:
        st.button("🇮🇳 Hindi (हिन्दी)", use_container_width=True)
    with lang3:
        st.button("🇮🇳 Marathi (मराठी)", use_container_width=True)
    with lang4:
        st.button("🇮🇳 Tamil (தமிழ்)", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.markdown("<h3>⚙️ Engine Configuration</h3>", unsafe_allow_html=True)
    st.toggle("Use Premium GPT-4o for complex queries (Overrides Llama3 Local)", value=True)
    st.toggle("Enable Voice Output (Cartesia TTS)", value=True)
    st.toggle("Stream RAG Document Chunks to Dashboard", value=False)
    st.markdown("</div>", unsafe_allow_html=True)