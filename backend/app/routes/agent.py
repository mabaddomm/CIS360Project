from flask import Blueprint, request, jsonify
from app.services.agent_service import run_agent

agent_bp = Blueprint("agent", __name__)

@agent_bp.route("/agent/query", methods=["POST"])
def agent_query():
    data = request.get_json() or {}
    query = str(data.get("query", "")).strip()

    if not query:
        return jsonify({"error": "Query is required"}), 400

    answer, raw_data = run_agent(query)

    return jsonify({
        "answer": answer,
        "tool_used": list(raw_data.keys())[0] if raw_data else "",
        "raw_data": raw_data
    }), 200