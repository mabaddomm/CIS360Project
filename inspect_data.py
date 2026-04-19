import os
from pymongo import MongoClient
from dotenv import load_dotenv
import json

load_dotenv("security.env")

client = MongoClient(os.getenv("MONGODB_URI"))
db = client["CIS_360_Project"]

print("=" * 80)
print("FULL MONGODB DATA STRUCTURE")
print("=" * 80)

collections = ["Datasets", "Papers", "FusionMethods"]

for col_name in collections:
    collection = db[col_name]
    count = collection.count_documents({})
    
    print(f"\n\n{'#' * 80}")
    print(f"# {col_name}: {count} documents")
    print(f"{'#' * 80}\n")
    
    # Show all documents
    all_docs = list(collection.find({}))
    for i, doc in enumerate(all_docs, 1):
        print(f"\n--- Document {i} ---")
        if "_id" in doc:
            del doc["_id"]
        print(json.dumps(doc, indent=2, default=str))

print("\n" + "=" * 80)
print("END ANALYSIS")
print("=" * 80)