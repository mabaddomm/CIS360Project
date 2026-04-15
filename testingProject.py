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
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("styles.css")
 
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
    <div style="font-size:0.78rem; color:#e8e6e1; line-height:1.8;">
        <span class="uncertainty-tag u1-tag">U1</span> Conception<br>
        <span class="uncertainty-tag u2-tag">U2</span> Measurement<br>
        <span class="uncertainty-tag u3-tag">U3</span> Analysis
    </div>
    ''', unsafe_allow_html=True)
 
    st.markdown("---")
    if st.button("Clear Chat", use_container_width=True):
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
 
# --- Input area (I don't get why Claude created this input area code, it seems like this
# does nothing and all it did was create a bug where an out of place black box pops up at
# the bottom of the page... Maybe there will be a reason to have this, who knows) ---

# st.markdown('<div class="input-area" style="left: 21rem;">', unsafe_allow_html=True) 
# commented above line out
# st.markdown('<div class="input-wrapper">', unsafe_allow_html=True) 
# commented this out

 
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
 
# st.markdown('<div class="input-hint">Connected to MongoDB · ResearchLens v1.0</div>', unsafe_allow_html=True)
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
