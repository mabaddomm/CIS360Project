from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.db import datasets_col, methods_col, papers_col


def _safe_list_cursor(cursor) -> List[Dict[str, Any]]:
    data = []
    for doc in cursor:
        if "_id" in doc:
            doc["_id"] = str(doc["_id"])
        data.append(doc)
    return data


def search_by_dataset_name(dataset_name: str) -> Dict[str, Any]:
    datasets = _safe_list_cursor(
        datasets_col.find(
            {"data_name": {"$regex": dataset_name, "$options": "i"}},
            {
                "paper_doi": 1,
                "data_name": 1,
                "data_type": 1,
                "spatial_coverage": 1,
                "temporal_coverage": 1,
                "format": 1,
                "uncertainty": 1,
            },
        )
    )

    dataset_ids = [d["_id"] for d in datasets]
    methods = _safe_list_cursor(
        methods_col.find(
            {"dataset_ids": {"$in": dataset_ids}},
            {
                "paper_doi": 1,
                "method_name": 1,
                "description": 1,
                "uncertainty": 1,
                "dataset_ids": 1,
            },
        )
    )

    paper_dois = list(
        set([d.get("paper_doi") for d in datasets if d.get("paper_doi")] + [m.get("paper_doi") for m in methods if m.get("paper_doi")])
    )
    papers = _safe_list_cursor(
        papers_col.find(
            {"_id": {"$in": paper_dois}},
            {
                "title": 1,
                "publication_title": 1,
                "publication_date": 1,
                "keywords": 1,
                "abstract": 1,
            },
        )
    )

    result = {"datasets": datasets, "methods": methods, "papers": papers}
    return result


def search_by_method_name(method_name: str) -> Dict[str, Any]:
    methods = _safe_list_cursor(
        methods_col.find(
            {"method_name": {"$regex": method_name, "$options": "i"}},
            {
                "paper_doi": 1,
                "method_name": 1,
                "description": 1,
                "dataset_ids": 1,
                "uncertainty": 1,
            },
        )
    )

    dataset_ids = []
    for method in methods:
        dataset_ids.extend(method.get("dataset_ids", []))
    dataset_ids = list(set(dataset_ids))

    datasets = _safe_list_cursor(
        datasets_col.find(
            {"_id": {"$in": dataset_ids}},
            {
                "paper_doi": 1,
                "data_name": 1,
                "data_type": 1,
                "spatial_coverage": 1,
                "temporal_coverage": 1,
                "uncertainty": 1,
            },
        )
    )

    paper_dois = list(
        set([m.get("paper_doi") for m in methods if m.get("paper_doi")] + [d.get("paper_doi") for d in datasets if d.get("paper_doi")])
    )
    papers = _safe_list_cursor(
        papers_col.find(
            {"_id": {"$in": paper_dois}},
            {
                "title": 1,
                "publication_title": 1,
                "publication_date": 1,
                "keywords": 1,
            },
        )
    )

    result = {"datasets": datasets, "methods": methods, "papers": papers}
    return result


def find_u2_for_data_type(data_type: str) -> Dict[str, Any]:
    datasets = _safe_list_cursor(
        datasets_col.find(
            {
                "data_type": {"$regex": data_type, "$options": "i"},
                "uncertainty.U2_measurement": {"$exists": True, "$ne": ""},
            },
            {
                "paper_doi": 1,
                "data_name": 1,
                "data_type": 1,
                "uncertainty": 1,
                "spatial_coverage": 1,
                "temporal_coverage": 1,
            },
        )
    )

    paper_dois = list(set([d.get("paper_doi") for d in datasets if d.get("paper_doi")]))
    papers = _safe_list_cursor(
        papers_col.find(
            {"_id": {"$in": paper_dois}},
            {
                "title": 1,
                "publication_title": 1,
                "publication_date": 1,
                "keywords": 1,
            },
        )
    )

    result = {"datasets": datasets, "papers": papers}
    return result


def papers_with_both_u1_and_u3() -> Dict[str, Any]:
    methods = _safe_list_cursor(
        methods_col.find(
            {
                "uncertainty.U1_conception": {"$exists": True, "$ne": ""},
                "uncertainty.U3_analysis": {"$exists": True, "$ne": ""},
            },
            {"paper_doi": 1, "method_name": 1, "uncertainty": 1},
        )
    )
    paper_dois = list(set([m.get("paper_doi") for m in methods if m.get("paper_doi")]))
    papers = _safe_list_cursor(
        papers_col.find(
            {"_id": {"$in": paper_dois}},
            {"title": 1, "publication_title": 1, "publication_date": 1},
        )
    )
    return {"methods": methods, "papers": papers}


def methods_for_both_datasets(dataset_a: str, dataset_b: str) -> Dict[str, Any]:
    ds_a = datasets_col.find_one({"data_name": {"$regex": dataset_a, "$options": "i"}})
    ds_b = datasets_col.find_one({"data_name": {"$regex": dataset_b, "$options": "i"}})

    if not ds_a or not ds_b:
        return {
            "datasets": [doc for doc in [ds_a, ds_b] if doc],
            "methods": [],
            "papers": [],
            "message": "One or both datasets were not found.",
        }

    methods = _safe_list_cursor(
        methods_col.find(
            {"dataset_ids": {"$all": [str(ds_a["_id"]), str(ds_b["_id"])]}},
            {"paper_doi": 1, "method_name": 1, "description": 1, "uncertainty": 1},
        )
    )
    paper_dois = list(set([m.get("paper_doi") for m in methods if m.get("paper_doi")]))
    papers = _safe_list_cursor(
        papers_col.find(
            {"_id": {"$in": paper_dois}},
            {"title": 1, "publication_title": 1, "publication_date": 1},
        )
    )

    return {
        "datasets": [
            {
                "_id": str(ds_a["_id"]),
                "data_name": ds_a.get("data_name"),
                "paper_doi": ds_a.get("paper_doi"),
            },
            {
                "_id": str(ds_b["_id"]),
                "data_name": ds_b.get("data_name"),
                "paper_doi": ds_b.get("paper_doi"),
            },
        ],
        "methods": methods,
        "papers": papers,
    }


def most_popular_dataset() -> Optional[Dict[str, Any]]:
    pipeline = [
        {"$unwind": "$dataset_ids"},
        {"$group": {"_id": "$dataset_ids", "method_count": {"$sum": 1}}},
        {"$sort": {"method_count": -1}},
        {"$limit": 1},
    ]

    top = list(methods_col.aggregate(pipeline))
    if not top:
        return None

    dataset_id = top[0]["_id"]
    dataset = datasets_col.find_one(
        {"_id": dataset_id},
        {"data_name": 1, "paper_doi": 1, "data_type": 1, "uncertainty": 1},
    )
    if not dataset:
        return None

    return {
        "dataset": {
            "_id": str(dataset.get("_id")),
            "data_name": dataset.get("data_name"),
            "paper_doi": dataset.get("paper_doi"),
            "data_type": dataset.get("data_type", []),
            "uncertainty": dataset.get("uncertainty", {}),
        },
        "method_count": top[0].get("method_count", 0),
    }


def summary_counts() -> Dict[str, int]:
    return {
        "papers": papers_col.count_documents({}),
        "datasets": datasets_col.count_documents({}),
        "fusion_methods": methods_col.count_documents({}),
        "u1_methods": methods_col.count_documents({"uncertainty.U1_conception": {"$exists": True, "$ne": ""}}),
        "u2_datasets": datasets_col.count_documents({"uncertainty.U2_measurement": {"$exists": True, "$ne": ""}}),
        "u3_methods": methods_col.count_documents({"uncertainty.U3_analysis": {"$exists": True, "$ne": ""}}),
    }
