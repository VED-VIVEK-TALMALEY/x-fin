from typing import Dict, List


def generate_staffing_insights(
    staffing: Dict,
) -> List[Dict]:
    insights: List[Dict] = []

    hours_attainment = float(
        staffing.get("hours_attainment_pct", 0) or 0
    )
    hours_variance_pct = float(
        staffing.get("hours_variance_pct", 0) or 0
    )
    budget_utilization = staffing.get(
        "budget_utilization"
    )
    data_quality = staffing.get(
        "utilization_data_quality",
        "unknown",
    )

    if data_quality in {
        "review_required",
        "limited",
        "missing_capacity_denominator",
    }:
        severity = (
            "HIGH"
            if data_quality == "review_required"
            else "MEDIUM"
        )

        insights.append(
            {
                "severity": severity,
                "category": "Staffing Data Quality",
                "metric": "Capacity Denominator",
                "message": (
                    "The current data supports hours-versus-budget "
                    "analysis, but not a true utilization or bench "
                    "calculation because capacity hours are not "
                    "available."
                ),
                "value": None,
            }
        )

    severity = (
        "HIGH"
        if abs(hours_variance_pct) >= 20
        else "MEDIUM"
        if abs(hours_variance_pct) >= 10
        else "LOW"
    )

    direction = "above" if hours_variance_pct >= 0 else "below"

    insights.append(
        {
            "severity": severity,
            "category": "Staffing",
            "metric": "Hours vs Budget",
            "message": (
                f"Actual delivery hours are {hours_attainment:.1f}% "
                f"of the hours budget ({abs(hours_variance_pct):.1f}% "
                f"{direction} budget)."
            ),
            "value": round(hours_attainment, 2),
        }
    )

    if budget_utilization is not None:
        insights.append(
            {
                "severity": "LOW",
                "category": "Staffing",
                "metric": "Budget Utilization",
                "message": (
                    f"Budget utilization is {float(budget_utilization):.1f}%. "
                    "This is a planning assumption and cannot be directly "
                    "compared with actual utilization without capacity data."
                ),
                "value": round(float(budget_utilization), 2),
            }
        )

    return insights
