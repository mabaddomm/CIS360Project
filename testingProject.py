import streamlit as st
import time
from pymongo import MongoClient

import os
from dotenv import load_dotenv

load_dotenv("security.env")

client = MongoClient(os.getenv("MONGODB_URI"))
db = client["CIS_360_Project"]
datasets = db["Datasets"]
papers = db["Papers"]
methods = db["FusionMethods"]


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
        # Display all messages from session state
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
                    <div class="assistant-bubble">
                ''', unsafe_allow_html=True)
                
                # Display datasets
                if msg["content"]["datasets"]:
                    for d in msg["content"]["datasets"]:
                        st.markdown(f"""
                        <div class="result-card">
                            <div class="result-title">{d.get('data_name', 'N/A')}</div>
                            <div class="result-meta">{d.get('paper_doi', 'No DOI')}</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Display methods
                if msg["content"]["methods"]:
                    for m in msg["content"]["methods"]:
                        st.markdown(f"""
                        <div class="result-card">
                            <div class="result-title">{m.get('method_name', 'N/A')}</div>
                            <div class="result-meta">{m.get('description', 'No description')}</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Display papers
                if msg["content"]["papers"]:
                    for p in msg["content"]["papers"]:
                        st.markdown(f"""
                        <div class="result-card">
                            <div class="result-title">{p.get('title', 'N/A')}</div>
                            <div class="result-meta">{p.get('doi', 'No DOI')}</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown("""
                    </div>
                </div>
                """, unsafe_allow_html=True)
 
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
 
def generate_response(query):
    """
    Query MongoDB and return results from datasets, methods, and papers collections.
    """
    try:
        results = []

        # 1. Dataset search
        dataset_hits = list(datasets.find({
            "$or": [
                {"data_name": {"$regex": query, "$options": "i"}},
                {"data_type": {"$regex": query, "$options": "i"}},
                {"paper_doi": {"$regex": query, "$options": "i"}}
            ]
        }).limit(10))

        # 2. Method search
        method_hits = list(methods.find({
            "method_name": {"$regex": query, "$options": "i"}
        }).limit(10))

        # 3. Paper search
        paper_hits = list(papers.find({
            "$or": [
                {"title": {"$regex": query, "$options": "i"}},
                {"doi": {"$regex": query, "$options": "i"}}
            ]
        }).limit(10))

        return {
            "datasets": dataset_hits,
            "methods": method_hits,
            "papers": paper_hits
        }
    except Exception as e:
        st.error(f"Database error: {str(e)}")
        return {"datasets": [], "methods": [], "papers": []}

# --- Handle input ---
if (send or user_input) and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input.strip()})
    response = generate_response(user_input.strip())
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.input_key += 1
    st.rerun()