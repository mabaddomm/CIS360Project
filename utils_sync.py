import json
import os
from pymongo import MongoClient
from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv("security.env")

def sync_atlas_to_local():
    """Pulls everything from Atlas and saves it to a local JSON for backup/deep search."""
    try:
        client = MongoClient(os.getenv("MONGODB_URI"))
        db = client["CIS_360_Project"]
        
        data_to_backup = {
            "papers": list(db["Papers"].find({})),
            "datasets": list(db["Datasets"].find({})),
            "methods": list(db["FusionMethods"].find({}))
        }
        
        # Convert MongoDB ObjectIds to strings so they can be saved to JSON
        for category in data_to_backup:
            for item in data_to_backup[category]:
                if "_id" in item:
                    item["_id"] = str(item["_id"])

        with open("local_backup.json", "w") as f:
            json.dump(data_to_backup, f, indent=4)
            
        return "✅ Sync Complete! local_backup.json updated."
    except Exception as e:
        return f"❌ Sync Failed: {e}"

def ai_deep_search(user_query):
    """The 'Nuclear Option': LLM reads the raw JSON file to find hidden matches."""
    if not os.path.exists("local_backup.json"):
        return "No local backup found. Please sync first."

    with open("local_backup.json", "r") as f:
        raw_data = f.read()

    # We send the query and the raw text (or chunks of it) to Gemini
    model = genai.GenerativeModel('gemini-2.0-flash')
    #model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    You are performing a DEEP SEARCH on a research database.
    USER QUERY: {user_query}
    RAW DATA: {raw_data[:20000]} # Gemini can handle large contexts, but we cap it for speed
    
    Instructions:
    Identify any papers or datasets that might have been missed by a standard search. 
    Explain WHY they are relevant even if keywords didn't match perfectly.
    """
    
    response = model.generate_content(prompt)
    return response.text