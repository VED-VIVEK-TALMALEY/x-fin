from typing import Dict, List


def generate_recommendations(
    reasoning: Dict,
    insights: List[Dict],
) -> List[Dict]:

    recommendations: List[Dict] = []

    # --------------------------------------------------
    # CORE METRICS
    # --------------------------------------------------

    budget_gap = float(
        reasoning.get("budget_gap", 0.0) or 0.0
    )

    forecast_gap = float(
        reasoning.get("forecast_gap", 0.0) or 0.0
    )

    forward_coverage = float(
        reasoning.get("forward_coverage", 0.0) or 0.0
    )

    weighted_pipeline = float(
        reasoning.get("weighted_pipeline", 0.0) or 0.0
    )

    committed_backlog = float(
        reasoning.get("committed_backlog", 0.0) or 0.0
    )

    committed_forecast_coverage = float(
        reasoning.get(
            "committed_forecast_coverage",
            reasoning.get(
                "forecast_confidence_base",
                0.0,
            ),
        )
        or 0.0
    )

    pipeline_dependency = float(
        reasoning.get(
            "pipeline_dependency",
            0.0,
        )
        or 0.0
    )

    forecast_risk = str(
        reasoning.get(
            "forecast_risk",
            "unknown",
        )
    ).lower()

    pipeline_risk = str(
        reasoning.get(
            "pipeline_risk",
            "unknown",
        )
    ).lower()

    # --------------------------------------------------
    # 1. REVENUE SHORTFALL
    # --------------------------------------------------

    if budget_gap < 0:

        shortfall = abs(budget_gap)

        recommendations.append({
            "priority": "HIGH",
            "category": "Revenue Recovery",
            "action": (
                "Prioritize conversion of qualified "
                "pipeline opportunities and identify "
                "near-term revenue actions required to "
                "close the budget shortfall."
            ),
            "rationale": (
                f"Actual revenue is ₹{shortfall:,.0f} "
                "below budget."
            ),
            "financial_impact": round(
                shortfall,
                2,
            ),
        })

    # --------------------------------------------------
    # 2. FORECAST SHORTFALL
    # --------------------------------------------------

    if forecast_gap < 0:

        shortfall = abs(forecast_gap)

        recommendations.append({
            "priority": "HIGH",
            "category": "Forecast Protection",
            "action": (
                "Increase conversion of high-probability "
                "pipeline and review delivery assumptions "
                "behind the current forecast."
            ),
            "rationale": (
                f"Forecast is ₹{shortfall:,.0f} "
                "below budget."
            ),
            "financial_impact": round(
                shortfall,
                2,
            ),
        })

    # --------------------------------------------------
    # 3. FORWARD COVERAGE
    # --------------------------------------------------

    if forward_coverage < 100:

        coverage_gap = (
            100
            - forward_coverage
        )

        recommendations.append({
            "priority": "HIGH",
            "category": "Pipeline Coverage",
            "action": (
                "Increase qualified pipeline and accelerate "
                "conversion of high-probability opportunities "
                "to restore forward revenue coverage."
            ),
            "rationale": (
                f"Forward coverage is "
                f"{forward_coverage:.1f}%, leaving a "
                f"{coverage_gap:.1f}% coverage gap."
            ),
            "financial_impact": round(
                weighted_pipeline,
                2,
            ),
        })

    # --------------------------------------------------
    # 4. MODERATE COVERAGE
    # --------------------------------------------------

    elif forward_coverage < 120:

        recommendations.append({
            "priority": "MEDIUM",
            "category": "Coverage Protection",
            "action": (
                "Maintain pipeline generation and selectively "
                "accelerate qualified opportunities to build "
                "additional forward revenue buffer."
            ),
            "rationale": (
                f"Forward coverage is "
                f"{forward_coverage:.1f}%, providing "
                "limited buffer against execution risk."
            ),
            "financial_impact": round(
                weighted_pipeline,
                2,
            ),
        })

    # --------------------------------------------------
    # 5. HIGH PIPELINE DEPENDENCY
    # --------------------------------------------------

    if pipeline_dependency >= 60:

        recommendations.append({
            "priority": "HIGH",
            "category": "Pipeline Risk",
            "action": (
                "Reduce dependence on weighted pipeline by "
                "prioritizing conversion of high-probability "
                "opportunities and protecting committed backlog."
            ),
            "rationale": (
                f"{pipeline_dependency:.1f}% of forward "
                "revenue depends on weighted pipeline."
            ),
            "financial_impact": round(
                weighted_pipeline,
                2,
            ),
        })

    elif pipeline_dependency >= 40:

        recommendations.append({
            "priority": "MEDIUM",
            "category": "Pipeline Management",
            "action": (
                "Monitor pipeline conversion closely and "
                "focus commercial activity on opportunities "
                "with the highest probability of realization."
            ),
            "rationale": (
                f"{pipeline_dependency:.1f}% of forward "
                "revenue depends on weighted pipeline."
            ),
            "financial_impact": round(
                weighted_pipeline,
                2,
            ),
        })

    # --------------------------------------------------
    # 6. FORECAST COMMITMENT RISK
    # --------------------------------------------------

    if committed_forecast_coverage < 50:

        recommendations.append({
            "priority": "HIGH",
            "category": "Forecast Quality",
            "action": (
                "Increase committed revenue visibility and "
                "revalidate forecast assumptions before "
                "relying on the current forecast for planning."
            ),
            "rationale": (
                f"Only {committed_forecast_coverage:.1f}% "
                "of forecast revenue is backed by committed "
                "backlog."
            ),
            "financial_impact": round(
                committed_backlog,
                2,
            ),
        })

    elif committed_forecast_coverage < 70:

        recommendations.append({
            "priority": "MEDIUM",
            "category": "Forecast Quality",
            "action": (
                "Increase visibility into pipeline conversion "
                "and strengthen committed revenue coverage "
                "behind the forecast."
            ),
            "rationale": (
                f"{committed_forecast_coverage:.1f}% of "
                "forecast revenue is currently supported "
                "by committed backlog."
            ),
            "financial_impact": round(
                committed_backlog,
                2,
            ),
        })

    # --------------------------------------------------
    # 7. FORECAST RISK
    # --------------------------------------------------

    if forecast_risk == "high":

        recommendations.append({
            "priority": "HIGH",
            "category": "Forecast Risk",
            "action": (
                "Run a downside forecast and review the "
                "largest assumptions driving forecast revenue."
            ),
            "rationale": (
                "Forecast commitment coverage is low, "
                "indicating elevated execution risk."
            ),
            "financial_impact": round(
                weighted_pipeline,
                2,
            ),
        })

    # --------------------------------------------------
    # 8. HEALTHY PERFORMANCE
    # --------------------------------------------------

    if (
        budget_gap >= 0
        and forecast_gap >= 0
        and forward_coverage >= 100
        and pipeline_risk != "high"
    ):

        recommendations.append({
            "priority": "LOW",
            "category": "Performance Protection",
            "action": (
                "Protect current delivery performance while "
                "selectively converting the highest-probability "
                "pipeline and preserving forecast headroom."
            ),
            "rationale": (
                f"Revenue is ₹{budget_gap:,.0f} above budget, "
                f"forecast is ₹{forecast_gap:,.0f} above budget, "
                f"and forward coverage is "
                f"{forward_coverage:.1f}%."
            ),
            "financial_impact": round(
                budget_gap,
                2,
            ),
        })

    # --------------------------------------------------
    # 9. STRONG FORWARD POSITION
    # --------------------------------------------------

    if (
        forward_coverage >= 120
        and forecast_gap >= 0
        and pipeline_dependency < 60
    ):

        recommendations.append({
            "priority": "LOW",
            "category": "Growth Optimization",
            "action": (
                "Use the strong forward position to prioritize "
                "higher-margin opportunities and protect "
                "delivery capacity rather than pursuing "
                "low-quality pipeline."
            ),
            "rationale": (
                f"Forward coverage is "
                f"{forward_coverage:.1f}% with "
                f"{pipeline_dependency:.1f}% pipeline dependency."
            ),
            "financial_impact": round(
                weighted_pipeline,
                2,
            ),
        })

    # --------------------------------------------------
    # 10. FALLBACK
    # --------------------------------------------------

    if not recommendations:

        recommendations.append({
            "priority": "LOW",
            "category": "Management Review",
            "action": (
                "Continue monitoring revenue performance, "
                "forecast assumptions, backlog realization "
                "and pipeline conversion."
            ),
            "rationale": (
                "No material threshold breach was identified "
                "by the current intelligence rules."
            ),
            "financial_impact": 0.0,
        })

    # --------------------------------------------------
    # PRIORITY ORDER
    # --------------------------------------------------

    priority_rank = {
        "HIGH": 0,
        "MEDIUM": 1,
        "LOW": 2,
    }

    recommendations.sort(
        key=lambda item: priority_rank.get(
            str(
                item.get(
                    "priority",
                    "LOW",
                )
            ).upper(),
            3,
        )
    )

    return recommendations