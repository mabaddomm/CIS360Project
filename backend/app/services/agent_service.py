from __future__ import annotations

import json
import os
from typing import Any, Dict, Tuple

from dotenv import load_dotenv
from openai import OpenAI

from app.services.mongo_service import (
    find_u2_for_data_type,
    methods_for_both_datasets,
    most_popular_dataset,
    papers_with_both_u1_and_u3,
    search_by_dataset_name,
    search_by_method_name,
)

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

TOOLS = [
    {
        "type": "function",
        "name": "search_dataset",
        "description": "Find a dataset and return related datasets, methods, and papers by dataset name.",
        "parameters": {
            "type": "object",
            "properties": {
                "dataset_name": {"type": "string"}
            },
            "required": ["dataset_name"]
        }
    },
    {
        "type": "function",
        "name": "search_method",
        "description": "Find a fusion method and return related methods, datasets, and papers by method name.",
        "parameters": {
            "type": "object",
            "properties": {
                "method_name": {"type": "string"}
            },
            "required": ["method_name"]
        }
    },
    {
        "type": "function",
        "name": "find_u2_uncertainty",
        "description": "Find papers and datasets that report U2 measurement uncertainty for a given data type.",
        "parameters": {
            "type": "object",
            "properties": {
                "data_type": {"type": "string"}
            },
            "required": ["data_type"]
        }
    },
    {
        "type": "function",
        "name": "methods_for_both_datasets",
        "description": "Find fusion methods that were applied to both dataset A and dataset B.",
        "parameters": {
            "type": "object",
            "properties": {
                "dataset_a": {"type": "string"},
                "dataset_b": {"type": "string"}
            },
            "required": ["dataset_a", "dataset_b"]
        }
    },
    {
        "type": "function",
        "name": "popular_dataset",
        "description": "Find the most connected or most popular dataset in the graph.",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "type": "function",
        "name": "papers_with_both_u1_and_u3",
        "description": "Find papers whose linked methods include both U1 conception and U3 analysis uncertainty.",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }
]


def execute_tool(name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    if name == "search_dataset":
        return search_by_dataset_name(args["dataset_name"])
    if name == "search_method":
        return search_by_method_name(args["method_name"])
    if name == "find_u2_uncertainty":
        return find_u2_for_data_type(args["data_type"])
    if name == "methods_for_both_datasets":
        return methods_for_both_datasets(args["dataset_a"], args["dataset_b"])
    if name == "popular_dataset":
        return most_popular_dataset() or {"message": "No popular dataset found."}
    if name == "papers_with_both_u1_and_u3":
        return papers_with_both_u1_and_u3()
    return {"error": f"Unknown tool: {name}"}


def run_agent(user_query: str) -> Tuple[str, Dict[str, Any]]:
    if not OPENAI_API_KEY:
        return (
            "OPENAI_API_KEY is not set. Add it in backend/.env before using the agent endpoint.",
            {},
        )

    client = OpenAI(api_key=OPENAI_API_KEY)

    first_response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": (
                    "You are ResearchAI, a database assistant over a local MongoDB knowledge base. "
                    "Use tools for factual lookup. Do not invent papers, datasets, methods, or uncertainty. "
                    "Uncertainty framework: U1=conception, U2=measurement, U3=analysis."
                ),
            },
            {"role": "user", "content": user_query},
        ],
        tools=TOOLS,
    )

    tool_outputs = {}
    function_calls = [item for item in first_response.output if item.type == "function_call"]

    if not function_calls:
        text = getattr(first_response, "output_text", "No answer generated.")
        return text, tool_outputs

    last_response_id = first_response.id
    for call in function_calls:
        args = json.loads(call.arguments or "{}")
        result = execute_tool(call.name, args)
        tool_outputs[call.name] = result
        followup = client.responses.create(
            model=OPENAI_MODEL,
            previous_response_id=last_response_id,
            input=[
                {
                    "type": "function_call_output",
                    "call_id": call.call_id,
                    "output": json.dumps(result),
                }
            ],
        )
        last_response_id = followup.id

    return getattr(followup, "output_text", "No answer generated."), tool_outputs
