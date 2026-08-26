from typing import Dict, List, Optional


def _num(value) -> float:
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def _add(recommendations: List[Dict], item: Dict) -> None:
    key = (
        item.get("category"),
        item.get("action"),
    )
    if not any(
        (x.get("category"), x.get("action")) == key
        for x in recommendations
    ):
        recommendations.append(item)


def generate_recommendations(
    reasoning: Dict,
    insights: List[Dict],
    risk: Optional[Dict] = None,
    monte_carlo: Optional[Dict] = None,
) -> List[Dict]:
    """Generate deduplicated, decision-oriented finance actions."""

    risk = risk or {}
    monte_carlo = monte_carlo or {}
    recommendations: List[Dict] = []

    budget_gap = _num(reasoning.get("budget_gap"))
    forecast_gap = _num(reasoning.get("forecast_gap"))
    forward_coverage = _num(reasoning.get("forward_coverage"))
    weighted_pipeline = _num(reasoning.get("weighted_pipeline"))
    committed_backlog = _num(reasoning.get("committed_backlog"))
    committed_coverage = _num(
        risk.get(
            "committed_forecast_coverage",
            reasoning.get("committed_forecast_coverage"),
        )
    )
    pipeline_dependency = _num(
        risk.get(
            "pipeline_dependency",
            reasoning.get("pipeline_dependency"),
        )
    )
    forecast_risk = str(
        risk.get("forecast_risk", reasoning.get("forecast_risk", "unknown"))
    ).lower()
    overall_risk = str(
        risk.get("overall_risk", "unknown")
    ).lower()

    # 1. Revenue gap
    if budget_gap < 0:
        _add(
            recommendations,
            {
                "priority": "HIGH",
                "category": "Revenue Recovery",
                "action": (
                    "Prioritize qualified pipeline conversion and identify "
                    "near-term commercial actions required to close the "
                    "revenue shortfall."
                ),
                "rationale": (
                    f"Actual revenue is ₹{abs(budget_gap):,.0f} below budget."
                ),
                "financial_impact": round(abs(budget_gap), 2),
            },
        )

    # 2. Forecast gap
    if forecast_gap < 0:
        _add(
            recommendations,
            {
                "priority": "HIGH",
                "category": "Forecast Protection",
                "action": (
                    "Increase conversion of high-probability pipeline and "
                    "revalidate delivery assumptions behind the forecast."
                ),
                "rationale": (
                    f"Forecast is ₹{abs(forecast_gap):,.0f} below budget."
                ),
                "financial_impact": round(abs(forecast_gap), 2),
            },
        )

    # 3. Coverage
    if forward_coverage < 100:
        _add(
            recommendations,
            {
                "priority": "HIGH",
                "category": "Pipeline Coverage",
                "action": (
                    "Increase qualified pipeline and accelerate conversion "
                    "of high-probability opportunities."
                ),
                "rationale": (
                    f"Forward coverage is {forward_coverage:.1f}%, below "
                    "the 100% budget coverage threshold."
                ),
                "financial_impact": round(weighted_pipeline, 2),
            },
        )
    elif forward_coverage < 120:
        _add(
            recommendations,
            {
                "priority": "MEDIUM",
                "category": "Coverage Protection",
                "action": (
                    "Maintain pipeline generation and selectively accelerate "
                    "qualified opportunities to build additional buffer."
                ),
                "rationale": (
                    f"Forward coverage is {forward_coverage:.1f}%, leaving "
                    "limited buffer."
                ),
                "financial_impact": round(weighted_pipeline, 2),
            },
        )

    # 4. Commitment quality
    if committed_coverage < 50:
        _add(
            recommendations,
            {
                "priority": "HIGH",
                "category": "Forecast Quality",
                "action": (
                    "Increase committed-revenue visibility and revalidate "
                    "the forecast assumptions before using it as a planning "
                    "baseline."
                ),
                "rationale": (
                    f"Only {committed_coverage:.1f}% of forecast revenue is "
                    "supported by committed backlog."
                ),
                "financial_impact": round(committed_backlog, 2),
            },
        )
    elif committed_coverage < 70:
        _add(
            recommendations,
            {
                "priority": "MEDIUM",
                "category": "Forecast Quality",
                "action": (
                    "Strengthen committed revenue coverage and improve "
                    "visibility into pipeline conversion."
                ),
                "rationale": (
                    f"{committed_coverage:.1f}% of forecast revenue is "
                    "currently supported by committed backlog."
                ),
                "financial_impact": round(committed_backlog, 2),
            },
        )

    # 5. Pipeline dependency
    if pipeline_dependency > 50:
        _add(
            recommendations,
            {
                "priority": "HIGH",
                "category": "Pipeline Risk",
                "action": (
                    "Prioritize conversion of the highest-probability "
                    "opportunities and reduce dependence on lower-confidence "
                    "pipeline."
                ),
                "rationale": (
                    f"{pipeline_dependency:.1f}% of forward revenue depends "
                    "on weighted pipeline."
                ),
                "financial_impact": round(weighted_pipeline, 2),
            },
        )
    elif pipeline_dependency >= 40:
        _add(
            recommendations,
            {
                "priority": "MEDIUM",
                "category": "Pipeline Management",
                "action": (
                    "Monitor pipeline conversion closely and focus commercial "
                    "activity on opportunities with the highest probability "
                    "of realization."
                ),
                "rationale": (
                    f"{pipeline_dependency:.1f}% of forward revenue depends "
                    "on weighted pipeline."
                ),
                "financial_impact": round(weighted_pipeline, 2),
            },
        )

    # 6. Downside / risk
    budget_analysis = monte_carlo.get("budget_analysis", {})
    probability_below = _num(
        budget_analysis.get("probability_below_budget")
    )

    if probability_below >= 25:
        _add(
            recommendations,
            {
                "priority": "HIGH" if probability_below >= 50 else "MEDIUM",
                "category": "Scenario Risk",
                "action": (
                    "Use the Monte Carlo downside range to stress-test the "
                    "planning baseline and identify the pipeline assumptions "
                    "that must hold to protect budget."
                ),
                "rationale": (
                    f"Monte Carlo simulations show a "
                    f"{probability_below:.1f}% probability of finishing "
                    "below budget."
                ),
                "financial_impact": round(
                    abs(_num(budget_analysis.get("p10_vs_budget"))),
                    2,
                ),
            },
        )

    # 7. High qualitative risk, but avoid duplicate "run downside forecast"
    if overall_risk == "high" and not any(
        item.get("category") == "Scenario Risk"
        for item in recommendations
    ):
        _add(
            recommendations,
            {
                "priority": "HIGH",
                "category": "Forecast Risk Management",
                "action": (
                    "Revalidate the highest-value pipeline opportunities "
                    "and use the downside scenario as the planning guardrail."
                ),
                "rationale": (
                    f"Overall risk is high with {committed_coverage:.1f}% "
                    f"committed coverage and {pipeline_dependency:.1f}% "
                    "pipeline dependency."
                ),
                "financial_impact": round(weighted_pipeline, 2),
            },
        )

    # 8. Healthy position
    if (
        not recommendations
        and budget_gap >= 0
        and forecast_gap >= 0
        and forward_coverage >= 100
    ):
        _add(
            recommendations,
            {
                "priority": "LOW",
                "category": "Performance Protection",
                "action": (
                    "Protect current delivery performance while selectively "
                    "converting the highest-probability pipeline."
                ),
                "rationale": (
                    f"Actual revenue is ₹{budget_gap:,.0f} above budget and "
                    f"forward coverage is {forward_coverage:.1f}%."
                ),
                "financial_impact": round(budget_gap, 2),
            },
        )

    priority_rank = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    recommendations.sort(
        key=lambda item: priority_rank.get(
            str(item.get("priority", "LOW")).upper(), 3
        )
    )

    return recommendations
