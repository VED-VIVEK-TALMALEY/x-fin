"""
Revenue Leakage Engine
----------------------

Detects potential revenue leakage from project-level financial data.

The engine is deliberately data-source agnostic. It accepts dictionaries,
lists of dictionaries, pandas-like records, or a project collection.

Leakage signals:
- Billing below contract value
- Revenue below expected revenue
- Cost overruns
- Margin compression
- Unbilled / incomplete delivery
- Pipeline-to-revenue conversion gaps
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional


def _to_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _first(record: Dict[str, Any], *keys: str, default: Any = None) -> Any:
    for key in keys:
        if key in record and record[key] is not None:
            return record[key]
    return default


def _records(data: Any) -> List[Dict[str, Any]]:
    if data is None:
        return []

    if isinstance(data, dict):
        for key in (
            "projects",
            "records",
            "data",
            "items",
            "results",
        ):
            value = data.get(key)
            if isinstance(value, list):
                return [
                    item for item in value
                    if isinstance(item, dict)
                ]

        return [data]

    if isinstance(data, list):
        return [
            item for item in data
            if isinstance(item, dict)
        ]

    try:
        return [
            dict(item)
            for item in data
            if isinstance(item, dict)
        ]
    except TypeError:
        return []


def analyze_project(project: Dict[str, Any]) -> Dict[str, Any]:
    contract_value = _to_float(
        _first(
            project,
            "contract_value",
            "contract_revenue",
            "project_value",
            "booked_revenue",
            "revenue",
        )
    )

    recognized_revenue = _to_float(
        _first(
            project,
            "recognized_revenue",
            "actual_revenue",
            "billed_revenue",
            "revenue_recognized",
        )
    )

    expected_revenue = _to_float(
        _first(
            project,
            "expected_revenue",
            "forecast_revenue",
            "revenue_forecast",
        ),
        contract_value,
    )

    actual_cost = _to_float(
        _first(
            project,
            "actual_cost",
            "delivery_cost",
            "cost",
        )
    )

    budget_cost = _to_float(
        _first(
            project,
            "budget_cost",
            "cost_budget",
        ),
        actual_cost,
    )

    progress = _to_float(
        _first(
            project,
            "progress_pct",
            "completion_pct",
            "completion",
            "delivery_progress",
        )
    )

    if progress <= 1:
        progress *= 100

    status = str(
        _first(project, "status", "project_status", default="")
    ).lower()

    revenue_gap = max(expected_revenue - recognized_revenue, 0.0)

    cost_overrun = max(actual_cost - budget_cost, 0.0)

    if contract_value > 0:
        realization_pct = (
            recognized_revenue / contract_value * 100
        )
    else:
        realization_pct = 0.0

    if contract_value > 0:
        expected_realization_pct = (
            expected_revenue / contract_value * 100
        )
    else:
        expected_realization_pct = 0.0

    margin = recognized_revenue - actual_cost

    margin_pct = (
        margin / recognized_revenue * 100
        if recognized_revenue
        else 0.0
    )

    leakage_components = {
        "revenue_gap": revenue_gap,
        "cost_overrun": cost_overrun,
    }

    # If a project is substantially complete but revenue realization is low,
    # treat the unrecognized amount as a potential leakage signal.
    completion_gap = 0.0

    if progress >= 70 and expected_revenue > recognized_revenue:
        completion_gap = revenue_gap * min(progress / 100, 1.0)

    potential_leakage = (
        revenue_gap
        + cost_overrun
        + completion_gap
    )

    signals: List[str] = []

    if revenue_gap > 0:
        signals.append("revenue_realization_gap")

    if cost_overrun > 0:
        signals.append("cost_overrun")

    if progress >= 70 and revenue_gap > 0:
        signals.append("delivery_revenue_mismatch")

    if margin_pct < 0:
        signals.append("negative_margin")

    if (
        status in {"completed", "complete", "delivered"}
        and revenue_gap > 0
    ):
        signals.append("completed_project_unrealized_revenue")

    if potential_leakage <= 0:
        severity = "LOW"
    elif potential_leakage >= max(contract_value * 0.10, 1):
        severity = "HIGH"
    elif potential_leakage >= max(contract_value * 0.03, 1):
        severity = "MEDIUM"
    else:
        severity = "LOW"

    project_id = _first(
        project,
        "project_id",
        "id",
        "project",
        default="unknown",
    )

    return {
        "project_id": project_id,
        "project_name": _first(
            project,
            "project_name",
            "name",
            default=str(project_id),
        ),
        "business_unit": _first(
            project,
            "business_unit",
            "unit",
            default="Unknown",
        ),
        "contract_value": contract_value,
        "recognized_revenue": recognized_revenue,
        "expected_revenue": expected_revenue,
        "revenue_gap": revenue_gap,
        "cost_overrun": cost_overrun,
        "completion_pct": progress,
        "realization_pct": realization_pct,
        "expected_realization_pct": expected_realization_pct,
        "margin": margin,
        "margin_pct": margin_pct,
        "potential_leakage": potential_leakage,
        "severity": severity,
        "signals": signals,
    }


def analyze_revenue_leakage(
    data: Any,
    materiality_threshold: float = 0.0,
) -> Dict[str, Any]:
    projects = _records(data)

    analyzed = [
        analyze_project(project)
        for project in projects
    ]

    material = [
        item
        for item in analyzed
        if item["potential_leakage"] > materiality_threshold
    ]

    material.sort(
        key=lambda item: item["potential_leakage"],
        reverse=True,
    )

    total_leakage = sum(
        item["potential_leakage"]
        for item in material
    )

    revenue_gap = sum(
        item["revenue_gap"]
        for item in material
    )

    cost_overrun = sum(
        item["cost_overrun"]
        for item in material
    )

    high_risk = sum(
        1
        for item in material
        if item["severity"] == "HIGH"
    )

    medium_risk = sum(
        1
        for item in material
        if item["severity"] == "MEDIUM"
    )

    return {
        "total_potential_leakage": total_leakage,
        "revenue_realization_gap": revenue_gap,
        "cost_overrun": cost_overrun,
        "projects_analyzed": len(analyzed),
        "projects_with_leakage": len(material),
        "high_risk_projects": high_risk,
        "medium_risk_projects": medium_risk,
        "leakage_rate_pct": (
            len(material) / len(analyzed) * 100
            if analyzed
            else 0.0
        ),
        "top_leakage_projects": material[:10],
        "all_findings": material,
    }


def build_revenue_leakage_overview(
    data: Any,
) -> Dict[str, Any]:
    result = analyze_revenue_leakage(data)

    if result["high_risk_projects"] > 0:
        status = "HIGH"
    elif result["medium_risk_projects"] > 0:
        status = "MEDIUM"
    elif result["projects_with_leakage"] > 0:
        status = "LOW"
    else:
        status = "NONE"

    result["status"] = status

    return result