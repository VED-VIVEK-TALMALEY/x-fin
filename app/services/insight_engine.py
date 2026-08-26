from typing import Dict, List, Optional


def _num(value) -> float:
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def _add_unique(insights: List[Dict], item: Dict) -> None:
    key = (
        item.get("category"),
        item.get("metric"),
    )
    if not any(
        (x.get("category"), x.get("metric")) == key
        for x in insights
    ):
        insights.append(item)


def generate_insights(
    reasoning: Dict,
    risk: Optional[Dict] = None,
    monte_carlo: Optional[Dict] = None,
    staffing: Optional[Dict] = None,
) -> List[Dict]:
    """Generate one non-duplicated executive insight per metric."""

    risk = risk or {}
    monte_carlo = monte_carlo or {}
    staffing = staffing or {}

    insights: List[Dict] = []

    actual = _num(reasoning.get("actual_revenue"))
    budget = _num(reasoning.get("budget_revenue"))
    forecast = _num(reasoning.get("forecast_revenue"))
    budget_gap = _num(reasoning.get("budget_gap"))
    budget_gap_pct = _num(reasoning.get("budget_gap_pct"))
    forecast_gap = _num(reasoning.get("forecast_gap"))
    forecast_gap_pct = _num(reasoning.get("forecast_gap_pct"))
    forward_coverage = _num(reasoning.get("forward_coverage"))
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
    committed_mix = _num(
        reasoning.get("committed_revenue_mix")
    )
    forecast_risk = str(
        risk.get("forecast_risk", reasoning.get("forecast_risk", "unknown"))
    ).lower()
    pipeline_risk = str(
        risk.get("pipeline_risk", reasoning.get("pipeline_risk", "unknown"))
    ).lower()

    # Revenue performance
    _add_unique(
        insights,
        {
            "severity": "LOW" if budget_gap >= 0 else "HIGH",
            "category": "Revenue",
            "metric": "Actual vs Budget",
            "message": (
                f"Actual revenue is {abs(budget_gap_pct):.1f}% "
                f"{'above' if budget_gap >= 0 else 'below'} budget."
            ),
            "value": round(budget_gap, 2),
        },
    )

    # Forecast
    _add_unique(
        insights,
        {
            "severity": "LOW" if forecast_gap >= 0 else "HIGH",
            "category": "Forecast",
            "metric": "Forecast vs Budget",
            "message": (
                f"Current forecast is {abs(forecast_gap_pct):.1f}% "
                f"{'above' if forecast_gap >= 0 else 'below'} budget."
            ),
            "value": round(forecast_gap, 2),
        },
    )

    # Forward coverage
    if forward_coverage >= 120:
        severity = "LOW"
        message = (
            f"Forward revenue coverage is {forward_coverage:.1f}% "
            "of budget, providing a strong coverage position."
        )
    elif forward_coverage >= 100:
        severity = "MEDIUM"
        message = (
            f"Forward revenue coverage is {forward_coverage:.1f}% "
            "of budget, providing limited buffer."
        )
    else:
        severity = "HIGH"
        message = (
            f"Forward revenue coverage is only {forward_coverage:.1f}% "
            "of budget, indicating a coverage gap."
        )

    _add_unique(
        insights,
        {
            "severity": severity,
            "category": "Coverage",
            "metric": "Forward Revenue Coverage",
            "message": message,
            "value": round(forward_coverage, 2),
        },
    )

    # Forecast quality
    if committed_coverage < 50:
        severity = "HIGH"
        message = (
            f"Only {committed_coverage:.1f}% of forecast revenue is "
            "supported by committed backlog, creating meaningful "
            "execution risk."
        )
    elif committed_coverage < 70:
        severity = "MEDIUM"
        message = (
            f"{committed_coverage:.1f}% of forecast revenue is supported "
            "by committed backlog; the remainder depends on conversion "
            "and execution."
        )
    else:
        severity = "LOW"
        message = (
            f"{committed_coverage:.1f}% of forecast revenue is supported "
            "by committed backlog."
        )

    _add_unique(
        insights,
        {
            "severity": severity,
            "category": "Forecast Quality",
            "metric": "Committed Forecast Coverage",
            "message": message,
            "value": round(committed_coverage, 2),
        },
    )

    # Pipeline dependency
    if pipeline_dependency > 50:
        severity = "HIGH"
    elif pipeline_dependency >= 40:
        severity = "MEDIUM"
    else:
        severity = "LOW"

    _add_unique(
        insights,
        {
            "severity": severity,
            "category": "Pipeline Risk",
            "metric": "Pipeline Dependency",
            "message": (
                f"{pipeline_dependency:.1f}% of forward revenue depends "
                "on weighted pipeline."
            ),
            "value": round(pipeline_dependency, 2),
        },
    )

    # Revenue mix
    _add_unique(
        insights,
        {
            "severity": (
                "LOW" if committed_mix >= 60
                else "MEDIUM" if committed_mix >= 40
                else "HIGH"
            ),
            "category": "Revenue Quality",
            "metric": "Committed Revenue Mix",
            "message": (
                f"{committed_mix:.1f}% of forward revenue is supported "
                f"by committed backlog, while "
                f"{pipeline_dependency:.1f}% depends on weighted pipeline."
            ),
            "value": round(committed_mix, 2),
        },
    )

    # Risk classification
    if forecast_risk in {"high", "medium", "moderate"}:
        _add_unique(
            insights,
            {
                "severity": "HIGH" if forecast_risk == "high" else "MEDIUM",
                "category": "Forecast Risk",
                "metric": "Forecast Risk",
                "message": (
                    f"Forecast risk is {forecast_risk} because only "
                    f"{committed_coverage:.1f}% of forecast revenue is "
                    "supported by committed backlog."
                ),
                "value": round(committed_coverage, 2),
            },
        )

    if pipeline_risk == "high":
        _add_unique(
            insights,
            {
                "severity": "HIGH",
                "category": "Pipeline Risk",
                "metric": "Pipeline Risk",
                "message": (
                    f"Pipeline risk is high because {pipeline_dependency:.1f}% "
                    "of forward revenue depends on weighted pipeline."
                ),
                "value": round(pipeline_dependency, 2),
            },
        )

    # Monte Carlo
    budget_analysis = monte_carlo.get("budget_analysis", {})
    distribution = monte_carlo.get("distribution", {})
    if budget_analysis:
        probability = _num(
            budget_analysis.get("probability_above_budget")
        )
        _add_unique(
            insights,
            {
                "severity": (
                    "LOW" if probability >= 75
                    else "MEDIUM" if probability >= 50
                    else "HIGH"
                ),
                "category": "Monte Carlo Forecast",
                "metric": "Probability of Beating Budget",
                "message": (
                    f"Monte Carlo simulations indicate a "
                    f"{probability:.1f}% probability of finishing "
                    "at or above budget."
                ),
                "value": round(probability, 2),
            },
        )

        if distribution:
            p10 = _num(distribution.get("p10"))
            p50 = _num(distribution.get("p50"))
            p90 = _num(distribution.get("p90"))
            _add_unique(
                insights,
                {
                    "severity": "MEDIUM",
                    "category": "Forecast Range",
                    "metric": "P10 / P50 / P90",
                    "message": (
                        f"Monte Carlo forecast range is ₹{p10:,.0f} at P10, "
                        f"₹{p50:,.0f} at P50, and ₹{p90:,.0f} at P90."
                    ),
                    "value": round(p50, 2),
                },
            )

    # Staffing
    if staffing:
        data_quality = staffing.get(
            "utilization_data_quality", "normal"
        )
        hours_attainment = _num(
            staffing.get("hours_attainment_pct")
        )
        if data_quality == "review_required":
            _add_unique(
                insights,
                {
                    "severity": "HIGH",
                    "category": "Staffing Data Quality",
                    "metric": "Capacity Denominator",
                    "message": (
                        "Staffing hours are materially above the hours "
                        "budget, but the current schema does not contain "
                        "a true capacity-hours denominator. Do not interpret "
                        "this as 181% utilization without validating the "
                        "capacity basis."
                    ),
                    "value": round(hours_attainment, 2),
                },
            )

    # Silence unused locals intentionally kept for readable input contract.
    _ = (actual, budget, forecast)

    return insights
