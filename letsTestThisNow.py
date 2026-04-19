import streamlit as st
from pymongo import MongoClient
import google.generativeai as genai
import json
import os
import re
from dotenv import load_dotenv
from utils_sync import ai_deep_search, sync_atlas_to_local

# --- INITIALIZATION ---
load_dotenv("security.env")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

@st.cache_resource
def init_connection():
    return MongoClient(os.getenv("MONGODB_URI"))

client = init_connection()
db = client["CIS_360_Project"]
datasets_col = db["Datasets"]
papers_col = db["Papers"]
methods_col = db["FusionMethods"]
# --- ADD THIS TO YOUR SCRIPT AFTER 'methods_col = db["FusionMethods"]' ---
with st.sidebar:
    st.write("---")
    st.subheader("📡 Connection Health")
    try:
        # 1. Ping the server
        client.admin.command('ping')
        st.success("Connected to Atlas Cloud")
        
        # 2. Check document counts
        p_count = papers_col.count_documents({})
        d_count = datasets_col.count_documents({})
        
        st.metric("Papers in DB", p_count)
        st.metric("Datasets in DB", d_count)
        
        if p_count == 0:
            st.warning("Connected, but the 'Papers' collection is EMPTY.")
            
    except Exception as e:
        st.error("Connection Failed")
        st.code(str(e))

st.set_page_config(
    page_title="ResearchLens AI",
    page_icon="🔬",
    layout="wide"
)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_query_log" not in st.session_state:
    st.session_state.last_query_log = None

# --- UTILS ---
def clean_json_string(text):
    text = re.sub(r"```json|```", "", text)
    return text.strip()

SCHEMA_INFO = """
Collections:
- Datasets: {data_name, data_type (array), paper_doi, uncertainty, format}
- Papers: {_id (DOI), title, authors (array), abstract, keywords (array), field_of_study (array), is_data_fusion (bool)}
- FusionMethods: {method_name, paper_doi, description, uncertainty, dataset_ids}
"""

def get_available_model():
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods and 'flash' in m.name:
                return m.name
        return "gemini-1.5-flash"
    except:
        return "gemini-1.5-flash"

def gemini_generate_mongodb_query(user_question: str):
    """Stricter prompt to prevent 'Pipeline' errors."""
    prompt = f"""
    You are a MongoDB expert. Generate a JSON search plan for: "{user_question}"
    Schema: {SCHEMA_INFO}

    CRITICAL RULES:
    1. Return ONLY a JSON object with a "queries" key.
    2. Use ONLY simple query objects for .find(). 
    3. NO lists, NO "$match" stages, NO "pipeline".
    4. To find 'data fusion' papers, search: {{"$or": [{{"is_data_fusion": true}}, {{"title": {{"$regex": "fusion", "$options": "i"}}}}]}}
    5. Always search across title, abstract, and keywords for any topic.
    """
    try:
        model_name = get_available_model()
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        query_data = json.loads(clean_json_string(response.text))
        st.session_state.last_query_log = query_data
        return query_data
    except Exception as e:
        st.sidebar.error(f"Brain Error: {e}")
        return {"queries": []}

def execute_queries(query_plan):
    """Bulletproof execution that handles both simple queries and accidentally generated pipelines."""
    results = {"datasets": [], "papers": [], "methods": []}
    mapping = {"Datasets": datasets_col, "Papers": papers_col, "FusionMethods": methods_col}
    
    for q_obj in query_plan.get("queries", []):
        col_name = q_obj.get("collection")
        
        # LOGIC: Extract the actual query if Gemini sent a pipeline list by mistake
        raw_query = q_obj.get("query", {})
        if isinstance(q_obj.get("pipeline"), list):
            for stage in q_obj["pipeline"]:
                if "$match" in stage:
                    raw_query = stage["$match"]
                    break
        
        if col_name in mapping:
            try:
                # Use a higher limit to ensure we catch the relevant papers
                cursor = mapping[col_name].find(raw_query).limit(10)
                for doc in cursor:
                    if "_id" in doc and col_name != "Papers":
                        doc.pop("_id")
                    if col_name == "Datasets": results["datasets"].append(doc)
                    elif col_name == "Papers": results["papers"].append(doc)
                    elif col_name == "FusionMethods": results["methods"].append(doc)
            except Exception as e:
                st.sidebar.warning(f"DB Error in {col_name}: {e}")
                
    return results

def get_conversational_summary(user_question, results):
    if not any(results.values()):
        return "I checked the database but no documents matched those specific filters."
    
    prompt = f"User: {user_question}\nResults: {json.dumps(results, default=str)}\nSummarize these findings in 2 sentences."
    try:
        model_name = get_available_model()
        model = genai.GenerativeModel(model_name)
        return model.generate_content(prompt).text
    except:
        return "I found the following records in the database:"

# --- UI SIDEBAR ---
with st.sidebar:
    st.title("🔬 ResearchLens")
    st.write(f"Papers: {papers_col.count_documents({})}")
    st.write(f"Datasets: {datasets_col.count_documents({})}")
    if st.session_state.last_query_log:
        with st.expander("🛠️ Debugger"):
            st.json(st.session_state.last_query_log)
    if st.button("Clear History"):
        st.session_state.messages = []
        st.rerun()

# --- CHAT LOGIC ---
if prompt := st.chat_input("Search..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("Analyzing..."):
        query_plan = gemini_generate_mongodb_query(prompt)
        db_results = execute_queries(query_plan)
        summary = get_conversational_summary(prompt, db_results)
        st.session_state.messages.append({"role": "assistant", "content": summary, "data": db_results})
    st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "data" in msg and any(msg["data"].values()):
            t1, t2, t3 = st.tabs(["📄 Papers", "📊 Datasets", "🧪 Methods"])
            with t1:
                if msg["data"]["papers"]:
                    for p in msg["data"]["papers"]:
                        st.markdown(f"**{p.get('title')}**")
                        st.caption(f"DOI: {p.get('_id')}")
                else: st.info("None found.")
            with t2:
                if msg["data"]["datasets"]: st.dataframe(msg["data"]["datasets"])
                else: st.info("None found.")
            with t3:
                if msg["data"]["methods"]: st.write(msg["data"]["methods"])
                else: st.info("None found.")