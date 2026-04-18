from flask import Blueprint, request, jsonify
from app.services.agent_service import run_agent

agent_bp = Blueprint("agent", __name__)

@agent_bp.route("/agent/query", methods=["POST"])
def agent_query():
    data = request.get_json()
    query = data.get("query", "").strip()

    if not query:
        return jsonify({"error": "Query is required"}), 400

    result = run_agent(query)
    return jsonify(result)