import streamlit as st
import time
 
# Page config
st.set_page_config(
    page_title="ResearchLens AI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)
 
# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&display=swap');
 
    /* Global */
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }
 
    .stApp {
        background-color: #0f0f11;
        color: #e8e6e1;
    }
 
    /* Hide default streamlit elements */
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
        max-width: 100%;
    }
 
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #111114;
        border-right: 1px solid #1e1e24;
        padding: 0;
    }
 
    [data-testid="stSidebar"] .block-container {
        padding: 2rem 1.25rem;
    }
 
    .sidebar-logo {
        font-family: 'DM Serif Display', serif;
        font-size: 1.5rem;
        color: #e8e6e1;
        letter-spacing: -0.02em;
        margin-bottom: 0.25rem;
    }
 
    .sidebar-tagline {
        font-size: 0.75rem;
        color: #555560;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 2rem;
    }
 
    .sidebar-section {
        font-size: 0.65rem;
        color: #444450;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 0.75rem;
        margin-top: 1.75rem;
    }
 
    .suggestion-btn {
        background: #17171c;
        border: 1px solid #22222a;
        border-radius: 8px;
        padding: 0.6rem 0.85rem;
        color: #8a8a99;
        font-size: 0.8rem;
        cursor: pointer;
        margin-bottom: 0.4rem;
        width: 100%;
        text-align: left;
        transition: all 0.2s;
        font-family: 'DM Sans', sans-serif;
    }
 
    .suggestion-btn:hover {
        background: #1d1d24;
        color: #c8c6c0;
        border-color: #2e2e3a;
    }
 
    .stat-card {
        background: #17171c;
        border: 1px solid #1e1e26;
        border-radius: 10px;
        padding: 0.85rem 1rem;
        margin-bottom: 0.5rem;
    }
 
    .stat-number {
        font-family: 'DM Serif Display', serif;
        font-size: 1.5rem;
        color: #c8a876;
        line-height: 1;
    }
 
    .stat-label {
        font-size: 0.72rem;
        color: #555560;
        margin-top: 0.2rem;
    }
 
    /* Main chat area */
    .chat-header {
        padding: 1.5rem 3rem 1rem;
        border-bottom: 1px solid #1a1a20;
        background: #0f0f11;
        position: sticky;
        top: 0;
        z-index: 100;
    }
 
    .chat-title {
        font-family: 'DM Serif Display', serif;
        font-size: 1.1rem;
        color: #e8e6e1;
        margin: 0;
    }
 
    .chat-subtitle {
        font-size: 0.75rem;
        color: #444450;
        margin: 0.2rem 0 0 0;
    }
 
    /* Messages */
    .message-container {
        padding: 1.5rem 3rem;
        max-width: 860px;
        margin: 0 auto;
    }
 
    .user-message {
        display: flex;
        justify-content: flex-end;
        margin-bottom: 1.25rem;
    }
 
    .user-bubble {
        background: #1e2a3a;
        border: 1px solid #253545;
        border-radius: 18px 18px 4px 18px;
        padding: 0.85rem 1.2rem;
        max-width: 70%;
        font-size: 0.9rem;
        color: #c8d8e8;
        line-height: 1.6;
    }
 
    .assistant-message {
        display: flex;
        justify-content: flex-start;
        margin-bottom: 1.25rem;
        gap: 0.85rem;
        align-items: flex-start;
    }
 
    .assistant-avatar {
        width: 32px;
        height: 32px;
        background: linear-gradient(135deg, #c8a876, #8a6a3a);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.85rem;
        flex-shrink: 0;
        margin-top: 2px;
    }
 
    .assistant-bubble {
        background: #141418;
        border: 1px solid #1e1e26;
        border-radius: 4px 18px 18px 18px;
        padding: 0.85rem 1.2rem;
        max-width: 75%;
        font-size: 0.9rem;
        color: #c8c6c0;
        line-height: 1.7;
    }
 
    .result-card {
        background: #0f0f13;
        border: 1px solid #1e1e28;
        border-left: 3px solid #c8a876;
        border-radius: 8px;
        padding: 1rem 1.1rem;
        margin: 0.6rem 0;
    }
 
    .result-title {
        font-family: 'DM Serif Display', serif;
        font-size: 0.95rem;
        color: #e8e6e1;
        margin-bottom: 0.3rem;
    }
 
    .result-meta {
        font-size: 0.75rem;
        color: #555560;
        margin-bottom: 0.4rem;
    }
 
    .result-tag {
        display: inline-block;
        background: #1a1a22;
        border: 1px solid #252530;
        border-radius: 4px;
        padding: 0.15rem 0.5rem;
        font-size: 0.7rem;
        color: #7a7a8a;
        margin-right: 0.3rem;
        margin-top: 0.3rem;
    }
 
    .uncertainty-tag {
        display: inline-block;
        border-radius: 4px;
        padding: 0.15rem 0.5rem;
        font-size: 0.7rem;
        margin-right: 0.3rem;
        margin-top: 0.3rem;
        font-weight: 500;
    }
 
    .u1-tag { background: #1a1a2e; border: 1px solid #2a2a4e; color: #8888cc; }
    .u2-tag { background: #1a2a1a; border: 1px solid #2a4a2a; color: #88cc88; }
    .u3-tag { background: #2a1a1a; border: 1px solid #4a2a2a; color: #cc8888; }
 
    /* Welcome screen */
    .welcome-container {
        text-align: center;
        padding: 4rem 2rem;
        max-width: 600px;
        margin: 0 auto;
    }
 
    .welcome-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
 
    .welcome-title {
        font-family: 'DM Serif Display', serif;
        font-size: 2rem;
        color: #e8e6e1;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
 
    .welcome-subtitle {
        font-size: 0.9rem;
        color: #555560;
        line-height: 1.6;
        margin-bottom: 2.5rem;
    }
 
    .example-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.75rem;
        text-align: left;
    }
 
    .example-card {
        background: #141418;
        border: 1px solid #1e1e26;
        border-radius: 10px;
        padding: 0.9rem 1rem;
        cursor: pointer;
        transition: all 0.2s;
    }
 
    .example-card:hover {
        background: #1a1a20;
        border-color: #2a2a36;
    }
 
    .example-label {
        font-size: 0.7rem;
        color: #c8a876;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.3rem;
    }
 
    .example-text {
        font-size: 0.83rem;
        color: #8a8a99;
        line-height: 1.4;
    }
 
    /* Input area */
    .input-area {
        position: fixed;
        bottom: 0;
        right: 0;
        padding: 1.25rem 3rem 1.5rem;
        background: linear-gradient(to top, #0f0f11 85%, transparent);
        z-index: 100;
    }
 
    .input-wrapper {
        max-width: 860px;
        margin: 0 auto;
        position: relative;
    }
 
    /* Streamlit input override */
    .stTextInput input {
        background: #141418 !important;
        border: 1px solid #252530 !important;
        border-radius: 14px !important;
        color: #e8e6e1 !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.9rem !important;
        padding: 0.85rem 1.2rem !important;
        padding-right: 3rem !important;
    }
 
    .stTextInput input:focus {
        border-color: #c8a876 !important;
        box-shadow: 0 0 0 2px rgba(200, 168, 118, 0.1) !important;
    }
 
    .stTextInput input::placeholder {
        color: #444450 !important;
    }
 
    /* Button */
    .stButton button {
        background: #c8a876 !important;
        color: #0f0f11 !important;
        border: none !important;
        border-radius: 10px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        padding: 0.6rem 1.5rem !important;
        transition: all 0.2s !important;
    }
 
    .stButton button:hover {
        background: #d4b882 !important;
        transform: translateY(-1px) !important;
    }
 
    /* Divider */
    .input-hint {
        text-align: center;
        font-size: 0.7rem;
        color: #333340;
        margin-top: 0.6rem;
    }
 
    /* Typing indicator */
    .typing-dot {
        display: inline-block;
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #c8a876;
        margin: 0 2px;
        animation: typing 1.2s infinite;
    }
 
    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }
 
    @keyframes typing {
        0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
        30% { transform: translateY(-4px); opacity: 1; }
    }
 
    /* Scrollbar */
    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #222228; border-radius: 2px; }
 
</style>
""", unsafe_allow_html=True)
 
# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "input_key" not in st.session_state:
    st.session_state.input_key = 0
 
# --- Sidebar ---
with st.sidebar:
    st.markdown('<div class="sidebar-logo">🔬 ResearchLens</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-tagline">Scientific Knowledge Graph</div>', unsafe_allow_html=True)
 
    # Stats
    st.markdown('<div class="sidebar-section">Database Stats</div>', unsafe_allow_html=True)
 
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('''
        <div class="stat-card">
            <div class="stat-number">5</div>
            <div class="stat-label">Papers</div>
        </div>''', unsafe_allow_html=True)
    with col2:
        st.markdown('''
        <div class="stat-card">
            <div class="stat-number">5</div>
            <div class="stat-label">Methods</div>
        </div>''', unsafe_allow_html=True)
 
    col3, col4 = st.columns(2)
    with col3:
        st.markdown('''
        <div class="stat-card">
            <div class="stat-number">12</div>
            <div class="stat-label">Datasets</div>
        </div>''', unsafe_allow_html=True)
    with col4:
        st.markdown('''
        <div class="stat-card">
            <div class="stat-number">3</div>
            <div class="stat-label">U-Types</div>
        </div>''', unsafe_allow_html=True)
 
    # Suggested queries
    st.markdown('<div class="sidebar-section">Try Asking</div>', unsafe_allow_html=True)
 
    suggestions = [
        "Show fusion methods for satellite imagery",
        "Papers with U2 measurement uncertainty",
        "Which datasets are most commonly used?",
        "Find all feature-level fusion papers",
        "Show methods used for time series data",
    ]
 
    for s in suggestions:
        if st.button(s, key=f"sug_{s}", use_container_width=True):
            st.session_state.pending_query = s
 
    # Uncertainty legend
    st.markdown('<div class="sidebar-section">Uncertainty Types</div>', unsafe_allow_html=True)
    st.markdown('''
    <div style="font-size:0.78rem; color:#666672; line-height:1.8;">
        <span class="uncertainty-tag u1-tag">U1</span> Conception<br>
        <span class="uncertainty-tag u2-tag">U2</span> Measurement<br>
        <span class="uncertainty-tag u3-tag">U3</span> Analysis
    </div>
    ''', unsafe_allow_html=True)
 
    st.markdown("---")
    if st.button("🗑 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
 
# --- Main area ---
col_main = st.columns([1])[0]
 
with col_main:
    # Header
    st.markdown('''
    <div class="chat-header">
        <p class="chat-title">Knowledge Graph Search</p>
        <p class="chat-subtitle">Ask anything about the papers, methods, datasets, or uncertainties in the database</p>
    </div>
    ''', unsafe_allow_html=True)
 
    # Chat messages or welcome screen
    st.markdown('<div class="message-container">', unsafe_allow_html=True)
 
    if not st.session_state.messages:
        st.markdown('''
        <div class="welcome-container">
            <div class="welcome-icon">🔬</div>
            <h1 class="welcome-title">ResearchLens AI</h1>
            <p class="welcome-subtitle">
                Search through our scientific knowledge graph using natural language.
                Ask about papers, fusion methods, datasets, or uncertainty types.
            </p>
            <div class="example-grid">
                <div class="example-card">
                    <div class="example-label">🔗 Linkage</div>
                    <div class="example-text">Find methods used for both satellite and sensor data</div>
                </div>
                <div class="example-card">
                    <div class="example-label">⚠️ Uncertainty</div>
                    <div class="example-text">Papers reporting U2 measurement uncertainty</div>
                </div>
                <div class="example-card">
                    <div class="example-label">📊 Discovery</div>
                    <div class="example-text">Which dataset appears most across papers?</div>
                </div>
                <div class="example-card">
                    <div class="example-label">🧪 Methods</div>
                    <div class="example-text">Show all feature-level fusion techniques</div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    else:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f'''
                <div class="user-message">
                    <div class="user-bubble">{msg["content"]}</div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="assistant-message">
                    <div class="assistant-avatar">🔬</div>
                    <div class="assistant-bubble">{msg["content"]}</div>
                </div>
                ''', unsafe_allow_html=True)
 
    st.markdown('</div>', unsafe_allow_html=True)
 
    # Spacer for fixed input
    st.markdown("<div style='height: 120px'></div>", unsafe_allow_html=True)
 
# --- Input area ---
st.markdown('<div class="input-area" style="left: 21rem;">', unsafe_allow_html=True)
st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)
 
col_input, col_btn = st.columns([6, 1])
 
with col_input:
    # Check for pending query from sidebar
    default_val = ""
    if "pending_query" in st.session_state:
        default_val = st.session_state.pending_query
        del st.session_state.pending_query
 
    user_input = st.text_input(
        "query",
        value=default_val,
        placeholder="Ask about papers, methods, datasets, or uncertainties...",
        label_visibility="collapsed",
        key=f"input_{st.session_state.input_key}"
    )
 
with col_btn:
    send = st.button("Search →", use_container_width=True)
 
st.markdown('<div class="input-hint">Connected to MongoDB · ResearchLens v1.0</div>', unsafe_allow_html=True)
st.markdown('</div></div>', unsafe_allow_html=True)
 
# --- Handle input ---
def generate_placeholder_response(query):
    """
    Placeholder response function.
    Replace this with your actual MongoDB + AI search logic later.
    """
    query_lower = query.lower()
 
    if any(word in query_lower for word in ["u2", "measurement", "sensor"]):
        return """
        Found <strong>3 papers</strong> reporting U2 (Measurement) uncertainty:<br><br>
        <div class="result-card">
            <div class="result-title">High-Performance Transformer Tracking</div>
            <div class="result-meta">IEEE TPAMI · 2023 · DOI: 10.1109/TPAMI.2022.3232535</div>
            <span class="uncertainty-tag u2-tag">U2</span>
            <span class="result-tag">VOT Benchmark</span>
            <span class="result-tag">Feature Fusion</span>
        </div>
        <div class="result-card">
            <div class="result-title">Multi-scale Tool Wear Monitoring</div>
            <div class="result-meta">Journal of Manufacturing Systems · 2023</div>
            <span class="uncertainty-tag u2-tag">U2</span>
            <span class="result-tag">PHM Dataset</span>
            <span class="result-tag">Sensor Signals</span>
        </div>
        """
    elif any(word in query_lower for word in ["method", "fusion", "technique"]):
        return """
        Found <strong>5 fusion methods</strong> in the database:<br><br>
        <div class="result-card">
            <div class="result-title">TransT — Attention-Based Feature Fusion</div>
            <div class="result-meta">Feature-level fusion · Computer Vision</div>
            <span class="uncertainty-tag u1-tag">U1</span>
            <span class="uncertainty-tag u3-tag">U3</span>
        </div>
        <div class="result-card">
            <div class="result-title">MDIP — Math-Data Integrated Prediction</div>
            <div class="result-meta">Model-level fusion · Marine Engineering</div>
            <span class="uncertainty-tag u1-tag">U1</span>
            <span class="uncertainty-tag u3-tag">U3</span>
        </div>
        <div class="result-card">
            <div class="result-title">MODC-MMFL — Multi-scale Convolution Fusion</div>
            <div class="result-meta">Feature-level fusion · Manufacturing</div>
            <span class="uncertainty-tag u1-tag">U1</span>
            <span class="uncertainty-tag u3-tag">U3</span>
        </div>
        """
    elif any(word in query_lower for word in ["dataset", "data", "popular", "common"]):
        return """
        Here are the datasets in the knowledge graph, ordered by usage:<br><br>
        <div class="result-card">
            <div class="result-title">ETT (Electricity Transformer Temperature)</div>
            <div class="result-meta">4 variants · DFNet · CSV · Apache 2.0</div>
            <span class="result-tag">Time-series</span>
            <span class="result-tag">Energy</span>
            <span class="uncertainty-tag u2-tag">U2</span>
        </div>
        <div class="result-card">
            <div class="result-title">VOT Benchmark Datasets</div>
            <div class="result-meta">TransT · Image sequences · GPL 3.0</div>
            <span class="result-tag">Computer Vision</span>
            <span class="uncertainty-tag u2-tag">U2</span>
        </div>
        <div class="result-card">
            <div class="result-title">PHM 2010 Tool Wear Dataset</div>
            <div class="result-meta">MODC-MMFL · CSV · PHM Society Copyright</div>
            <span class="result-tag">Manufacturing</span>
            <span class="uncertainty-tag u2-tag">U2</span>
        </div>
        """
    else:
        return f"""
        I searched the knowledge graph for <em>"{query}"</em>.<br><br>
        The database currently contains <strong>5 papers</strong>, <strong>5 methods</strong>, 
        and <strong>12 datasets</strong> related to data fusion research.<br><br>
        Try asking about:
        <ul style="margin-top:0.5rem; color:#8a8a99;">
            <li>Specific uncertainty types (U1, U2, U3)</li>
            <li>Fusion methods or techniques</li>
            <li>Datasets used in the papers</li>
            <li>Papers by field of study</li>
        </ul>
        <em style="color:#555560; font-size:0.82rem;">
            Note: Full MongoDB search will be connected soon.
        </em>
        """
 
if (send or user_input) and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input.strip()})
    response = generate_placeholder_response(user_input.strip())
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.input_key += 1
    st.rerun()
