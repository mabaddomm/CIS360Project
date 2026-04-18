import html
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

# Must match styles.css sidebar / header media query
_DESKTOP_MIN_WIDTH_PX = 992
# Query box auto-grow (see inject_query_textarea_autogrow)
_QUERY_TEXTAREA_MAX_LINES = 10
 
# Page config
st.set_page_config(
    page_title="ResearchLens AI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)
 
# Custom CSS (resolve next to this file so it loads regardless of cwd)
def load_css(file_name):
    path = Path(__file__).resolve().parent / file_name
    with open(path, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("styles.css")


def inject_sidebar_viewport_bridge():
    """
    Desktop: clear Streamlit's persisted stSidebarCollapsed-* flag and click the native
    expand control if needed so the sidebar cannot stay 'stuck' closed across refreshes.

    Tablet/phone: leave Streamlit's header + collapse behavior alone so the top bar
    can open or close the sidebar.
    """
    px = _DESKTOP_MIN_WIDTH_PX
    components.html(
        f"""
<script>
(function () {{
  var root = window.parent;
  var doc = root.document;
  var mq = root.matchMedia("(min-width: {px}px)");

  function clearCollapsedPref() {{
    try {{
      var ls = root.localStorage;
      for (var i = ls.length - 1; i >= 0; i--) {{
        var k = ls.key(i);
        if (k && k.indexOf("stSidebarCollapsed-") === 0) {{
          ls.removeItem(k);
        }}
      }}
    }} catch (e) {{}}
  }}

  function clearSidebarWidthPref() {{
    try {{
      root.localStorage.removeItem("sidebarWidth");
    }} catch (e) {{}}
  }}

  function stripResizeHandles() {{
    var side = doc.querySelector('[data-testid="stSidebar"]');
    if (!side) return;
    for (var i = 0; i < side.children.length; i++) {{
      var ch = side.children[i];
      if (ch.getAttribute("data-testid") === "stSidebarContent") continue;
      ch.style.setProperty("display", "none", "important");
      ch.style.setProperty("pointer-events", "none", "important");
      ch.style.setProperty("width", "0", "important");
      ch.style.setProperty("min-width", "0", "important");
      ch.style.setProperty("opacity", "0", "important");
    }}
  }}

  function watchSidebarForHandles() {{
    var side = doc.querySelector('[data-testid="stSidebar"]');
    if (!side || side.__researchLensHandleObserver) return;
    side.__researchLensHandleObserver = true;
    var obs = new MutationObserver(stripResizeHandles);
    obs.observe(side, {{ childList: true }});
  }}

  function tryClickExpand() {{
    var btn =
      doc.querySelector('button[aria-label="Expand sidebar"]') ||
      doc.querySelector('[data-testid="stSidebarCollapsedControl"] button') ||
      doc.querySelector('[data-testid="collapsedControl"] button');
    if (btn) {{
      btn.click();
    }}
  }}

  function syncDesktopSidebar() {{
    if (!mq.matches) return;
    clearCollapsedPref();
    tryClickExpand();
  }}

  function syncAll() {{
    clearSidebarWidthPref();
    stripResizeHandles();
    watchSidebarForHandles();
    syncDesktopSidebar();
  }}

  function init() {{
    if (!root.__researchLensSidebarBridge) {{
      root.__researchLensSidebarBridge = true;
      root.addEventListener("resize", syncAll);
    }}
    syncAll();
    setTimeout(syncAll, 60);
    setTimeout(syncAll, 300);
  }}

  init();
}})();
</script>
""",
        height=0,
        width=0,
    )


def inject_query_textarea_autogrow(max_lines: int = _QUERY_TEXTAREA_MAX_LINES) -> None:
    """
    Grow the main search textarea with content up to max_lines, then show a scrollbar.
    Streamlit keeps a fixed inline height on st.text_area; this overrides it on the client.
    """
    components.html(
        f"""
<script>
(function () {{
  var root = window.parent;
  var doc = root.document;
  var MAX = {int(max_lines)};

  function extras(el) {{
    var s = root.getComputedStyle(el);
    return (parseFloat(s.paddingTop) || 0) + (parseFloat(s.paddingBottom) || 0) +
      (parseFloat(s.borderTopWidth) || 0) + (parseFloat(s.borderBottomWidth) || 0);
  }}

  function lineH(el) {{
    var s = root.getComputedStyle(el);
    var lh = s.lineHeight;
    if (lh === "normal") {{
      var fs = parseFloat(s.fontSize) || 16;
      return fs * 1.45;
    }}
    return parseFloat(lh) || 20;
  }}

  function fit(el) {{
    if (!el || el.tagName !== "TEXTAREA") return;
    var lh = lineH(el);
    var maxPx = lh * MAX + extras(el);
    el.style.overflowY = "hidden";
    el.style.height = "1px";
    var sh = el.scrollHeight;
    var one = lh + extras(el);
    var next = Math.max(one, Math.min(sh, maxPx));
    el.style.height = next + "px";
    el.style.overflowY = sh > maxPx ? "auto" : "hidden";
  }}

  function findTa() {{
    var ta =
      doc.querySelector('[data-testid="stMain"] form[data-testid="stForm"] .stTextArea textarea') ||
      doc.querySelector('[data-testid="stMain"] .stTextArea textarea') ||
      doc.querySelector('section.main form[data-testid="stForm"] .stTextArea textarea') ||
      doc.querySelector("section.main .stTextArea textarea");
    if (ta) return ta;
    var all = doc.querySelectorAll(".stTextArea textarea");
    for (var i = 0; i < all.length; i++) {{
      if (!all[i].closest('[data-testid="stSidebar"]')) return all[i];
    }}
    return null;
  }}

  function wire(el) {{
    if (!el || el.__researchLensAutoGrow) return;
    el.__researchLensAutoGrow = true;
    function refit() {{
      root.requestAnimationFrame(function () {{ fit(el); }});
    }}
    ["input", "change", "cut", "paste"].forEach(function (ev) {{
      el.addEventListener(ev, refit);
    }});
  }}

  function sync() {{
    var el = findTa();
    if (!el) return;
    wire(el);
    fit(el);
  }}

  function scheduleSync() {{
    clearTimeout(root.__researchLensTaGrowDebounce);
    root.__researchLensTaGrowDebounce = root.setTimeout(sync, 50);
  }}

  if (!root.__researchLensTextAreaGrowInit) {{
    root.__researchLensTextAreaGrowInit = true;
    var main =
      doc.querySelector('[data-testid="stMain"]') ||
      doc.querySelector("section.main") ||
      doc.body;
    var mo = new MutationObserver(scheduleSync);
    mo.observe(main, {{ childList: true, subtree: true }});
    root.addEventListener("resize", function () {{ sync(); }});
  }}
  sync();
  root.setTimeout(sync, 50);
  root.setTimeout(sync, 200);
  root.setTimeout(sync, 600);
}})();
</script>
""",
        height=0,
        width=0,
    )


# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "input_key" not in st.session_state:
    st.session_state.input_key = 0

# Allow mobile "Try Asking" links to prefill the input.
try:
    suggested = st.query_params.get("suggest")
except Exception:
    suggested = None
if suggested:
    st.session_state.pending_query = suggested
    try:
        del st.query_params["suggest"]
    except Exception:
        pass
 
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
    <div style="font-size:0.98rem; color:#e8e6e1; line-height:1.8;">
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
    # Sticky header only during chat (welcome screen already has the hero title)
    if st.session_state.messages:
        pass

    # Chat messages or welcome screen
    st.markdown('<div class="message-container">', unsafe_allow_html=True)

    if not st.session_state.messages:
        st.markdown('''
        <div class="welcome-container">
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

        # Mobile/tablet: render "sidebar" content inline as a single HTML block
        # so it can be cleanly hidden on desktop with CSS (no duplication).
        mobile_links = "\n".join(
            f'<a class="suggestion-btn suggestion-link" href="?suggest={html.escape(s, quote=True)}">{html.escape(s)}</a>'
            for s in suggestions
        )
        st.markdown(
            f"""
<div class="mobile-sidebar-panels">
  <div class="sidebar-section">Database Stats</div>
  <div class="mobile-stats-grid">
    <div class="stat-card">
      <div class="stat-number">5</div>
      <div class="stat-label">Papers</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">5</div>
      <div class="stat-label">Methods</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">12</div>
      <div class="stat-label">Datasets</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">3</div>
      <div class="stat-label">U-Types</div>
    </div>
  </div>

  <div class="sidebar-section">Uncertainty Types</div>
  <div class="uncertainty-legend">
    <span class="uncertainty-tag u1-tag">U1</span> Conception<br>
    <span class="uncertainty-tag u2-tag">U2</span> Measurement<br>
    <span class="uncertainty-tag u3-tag">U3</span> Analysis
  </div>

  <div class="sidebar-section">Try Asking</div>
<!--   <div class="mobile-suggestions">
     {mobile_links}
   </div>  -->
</div>
""",
            unsafe_allow_html=True,
        )

        # st.markdown('<div class="mobile-sidebar-panels">', unsafe_allow_html=True)

        for s in suggestions:
            if st.button(s, key=f"sugg_{s}", use_container_width=True):
                st.session_state.pending_query = s

        # st.markdown('</div>', unsafe_allow_html=True)
    else:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                safe = html.escape(msg["content"])
                st.markdown(f'''
                <div class="user-message">
                    <div class="user-bubble">{safe}</div>
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

    # Form: submit via button (textarea uses Enter for new lines).
    default_val = ""
    if "pending_query" in st.session_state:
        default_val = st.session_state.pending_query
        del st.session_state.pending_query
        st.session_state.input_key += 1

    with st.form("search_form", clear_on_submit=True):
        col_input, col_btn = st.columns([6, 1])
        with col_input:
            user_input = st.text_area(
                "query",
                value=default_val,
                placeholder="Ask about papers, methods, etc...",
                label_visibility="collapsed",
                key=f"input_{st.session_state.input_key}",
                height=38,
            )
        with col_btn:
            send = st.form_submit_button("Search →", use_container_width=True)
 
# st.markdown('<div class="input-hint">Connected to MongoDB · ResearchLens v1.0</div>', unsafe_allow_html=True)
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
        safe_q = html.escape(query)
        return f"""
        I searched the knowledge graph for <em>"{safe_q}"</em>.<br><br>
        The database currently contains <strong>5 papers</strong>, <strong>5 methods</strong>, 
        and <strong>12 datasets</strong> related to data fusion research.<br><br>
        Try asking about:
        <ul style="margin-top:0.5rem;>
            <li>Specific uncertainty types (U1, U2, U3)</li>
            <li>Fusion methods or techniques</li>
            <li>Datasets used in the papers</li>
            <li>Papers by field of study</li>
        </ul>
        <em style="color:#555560; font-size:0.82rem;">
            Note: Full MongoDB search will be connected soon.
        </em>
        """


inject_sidebar_viewport_bridge()
inject_query_textarea_autogrow()

if send and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input.strip()})
    response = generate_placeholder_response(user_input.strip())
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.input_key += 1
    st.rerun()
