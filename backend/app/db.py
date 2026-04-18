import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI","mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "data_fusion_ontology")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

papers_col = db["papers"]
datasets_col = db["datasets"]
methods_col = db["fusion_methods"]

