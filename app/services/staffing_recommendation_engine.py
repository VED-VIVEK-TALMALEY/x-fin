from typing import Dict, List


def generate_staffing_recommendations(
    staffing: Dict,
    insights: List[Dict],
) -> List[Dict]:
    recommendations: List[Dict] = []

    data_quality = staffing.get(
        "utilization_data_quality",
        "unknown",
    )
    hours_attainment = float(
        staffing.get("hours_attainment_pct", 0) or 0
    )

    if data_quality in {
        "review_required",
        "limited",
        "missing_capacity_denominator",
    }:
        recommendations.append(
            {
                "priority": "HIGH" if data_quality == "review_required" else "MEDIUM",
                "category": "Staffing Data Validation",
                "action": (
                    "Add or validate a capacity-hours denominator before "
                    "using staffing utilization, bench, or capacity "
                    "economics for management decisions."
                ),
                "rationale": (
                    f"Current data shows {hours_attainment:.1f}% of hours "
                    "budget delivered, but hours budget is not the same "
                    "as available capacity."
                ),
                "financial_impact": 0.0,
            }
        )

    return recommendations
