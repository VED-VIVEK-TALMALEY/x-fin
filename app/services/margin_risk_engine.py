"""
Margin Risk Engine
------------------

Identifies margin deterioration at project and portfolio level.

Signals:
- gross margin compression
- cost overrun
- revenue under-realization
- negative margin
- low margin projects
"""

from __future__ import annotations

from typing import Any, Dict, List


def _float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _first(record: Dict[str, Any], *keys: str, default=None):
    for key in keys:
        if key in record and record[key] is not None:
            return record[key]
    return default


def _records(data: Any) -> List[Dict[str, Any]]:
    if data is None:
        return []

    if isinstance(data, dict):
        for key in ("projects", "records", "data", "items"):
            value = data.get(key)
            if isinstance(value, list):
                return [x for x in value if isinstance(x, dict)]
        return [data]

    if isinstance(data, list):
        return [x for x in data if isinstance(x, dict)]

    try:
        return [dict(x) for x in data]
    except TypeError:
        return []


def analyze_margin(project: Dict[str, Any]) -> Dict[str, Any]:
    revenue = _float(
        _first(
            project,
            "actual_revenue",
            "recognized_revenue",
            "revenue",
            "contract_value",
        )
    )

    cost = _float(
        _first(
            project,
            "actual_cost",
            "delivery_cost",
            "cost",
        )
    )

    budget_cost = _float(
        _first(
            project,
            "budget_cost",
            "cost_budget",
        ),
        cost,
    )

    target_margin_pct = _float(
        _first(
            project,
            "target_margin_pct",
            "budget_margin_pct",
            "planned_margin_pct",
        ),
        20.0,
    )

    actual_margin = revenue - cost

    actual_margin_pct = (
        actual_margin / revenue * 100
        if revenue
        else 0.0
    )

    margin_gap_pct = (
        actual_margin_pct - target_margin_pct
    )

    cost_overrun = max(
        cost - budget_cost,
        0.0,
    )

    risk_score = 0.0

    if margin_gap_pct < 0:
        risk_score += min(
            abs(margin_gap_pct) * 3,
            60,
        )

    if revenue > 0 and cost_overrun > 0:
        risk_score += min(
            cost_overrun / revenue * 100,
            30,
        )

    if actual_margin_pct < 0:
        risk_score += 30

    risk_score = min(
        risk_score,
        100,
    )

    if risk_score >= 70:
        risk = "HIGH"
    elif risk_score >= 35:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    project_id = _first(
        project,
        "project_id",
        "id",
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
        "revenue": revenue,
        "cost": cost,
        "budget_cost": budget_cost,
        "actual_margin": actual_margin,
        "actual_margin_pct": actual_margin_pct,
        "target_margin_pct": target_margin_pct,
        "margin_gap_pct": margin_gap_pct,
        "cost_overrun": cost_overrun,
        "risk_score": risk_score,
        "risk": risk,
    }


def analyze_margin_risk(data: Any) -> Dict[str, Any]:
    records = _records(data)

    analyzed = [
        analyze_margin(record)
        for record in records
    ]

    total_revenue = sum(
        item["revenue"]
        for item in analyzed
    )

    total_cost = sum(
        item["cost"]
        for item in analyzed
    )

    total_margin = (
        total_revenue - total_cost
    )

    portfolio_margin_pct = (
        total_margin / total_revenue * 100
        if total_revenue
        else 0.0
    )

    high_risk = [
        item
        for item in analyzed
        if item["risk"] == "HIGH"
    ]

    medium_risk = [
        item
        for item in analyzed
        if item["risk"] == "MEDIUM"
    ]

    margin_at_risk = sum(
        max(
            item["cost_overrun"],
            0.0,
        )
        + max(
            -item["margin_gap_pct"]
            * item["revenue"]
            / 100,
            0.0,
        )
        for item in analyzed
    )

    top_risks = sorted(
        analyzed,
        key=lambda x: x["risk_score"],
        reverse=True,
    )[:10]

    if high_risk:
        status = "HIGH"
    elif medium_risk:
        status = "MEDIUM"
    else:
        status = "LOW"

    return {
        "total_revenue": total_revenue,
        "total_cost": total_cost,
        "total_margin": total_margin,
        "portfolio_margin_pct": portfolio_margin_pct,
        "margin_at_risk": margin_at_risk,
        "projects_analyzed": len(analyzed),
        "high_risk_projects": len(high_risk),
        "medium_risk_projects": len(medium_risk),
        "status": status,
        "top_margin_risks": top_risks,
        "projects": analyzed,
    }


def build_margin_risk_overview(
    data: Any,
) -> Dict[str, Any]:
    return analyze_margin_risk(data)