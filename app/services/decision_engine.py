from __future__ import annotations

from typing import Dict, List


def generate_decisions(
    forecast_risk: str,
    confidence_band: str,
    pipeline_dependency: float,
    forecast_headroom_pct: float,
    variance_pct: float,
    staffing_gap: float = 0.0,
) -> Dict:

    decisions: List[Dict] = []

    if forecast_risk == "high":
        decisions.append({
            "priority": "critical",
            "area": "forecast",
            "action": "Review forecast assumptions and committed coverage.",
        })

    if pipeline_dependency >= 50:
        decisions.append({
            "priority": "high",
            "area": "pipeline",
            "action": "Increase pipeline conversion or reduce forecast dependency.",
        })

    if forecast_headroom_pct < 0:
        decisions.append({
            "priority": "high",
            "area": "budget",
            "action": "Escalate forecast shortfall against budget.",
        })
    elif forecast_headroom_pct < 5:
        decisions.append({
            "priority": "medium",
            "area": "budget",
            "action": "Monitor limited budget headroom.",
        })

    if variance_pct <= -10:
        decisions.append({
            "priority": "high",
            "area": "variance",
            "action": "Investigate material negative revenue variance.",
        })

    if staffing_gap > 0:
        decisions.append({
            "priority": "high",
            "area": "staffing",
            "action": "Resolve delivery capacity shortage before accepting additional demand.",
        })

    if confidence_band in {"low", "very_low"}:
        decisions.append({
            "priority": "medium",
            "area": "confidence",
            "action": "Increase forecast evidence before committing management guidance.",
        })

    if not decisions:
        decisions.append({
            "priority": "low",
            "area": "monitoring",
            "action": "No material intervention identified from current indicators.",
        })

    priority_order = {
        "critical": 0,
        "high": 1,
        "medium": 2,
        "low": 3,
    }

    decisions.sort(
        key=lambda item: priority_order[item["priority"]]
    )

    return {
        "decision_count": len(decisions),
        "decisions": decisions,
    }