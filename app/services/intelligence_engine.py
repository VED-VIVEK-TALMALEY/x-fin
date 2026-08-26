from typing import Any, Dict

from app.services.backlog_engine import calculate_backlog
from app.services.finance_queries import (
    get_budget_summary,
    get_finance_summary,
    get_pipeline_summary,
)
from app.services.finance_reasoning import explain_financial_position
from app.services.forecast_engine import build_forecast
from app.services.insight_engine import generate_insights
from app.services.monte_carlo_engine import run_monte_carlo_forecast
from app.services.recommendation_engine import generate_recommendations
from app.services.risk_engine import calculate_forecast_risk
from app.services.staffing_engine import calculate_staffing_position
from app.services.staffing_insight_engine import generate_staffing_insights
from app.services.staffing_recommendation_engine import (
    generate_staffing_recommendations,
)


def _num(value: Any) -> float:
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def _round_dict(value: Dict[str, Any], digits: int = 2) -> Dict[str, Any]:
    result = {}
    for key, item in value.items():
        if isinstance(item, dict):
            result[key] = _round_dict(item, digits)
        elif isinstance(item, float):
            result[key] = round(item, digits)
        else:
            result[key] = item
    return result


def build_intelligence_overview(db) -> Dict[str, Any]:
    """
    Canonical X-Fin intelligence orchestration.

    Every downstream consumer should use this result rather than
    recomputing forecast/risk metrics independently.
    """

    # --------------------------------------------------
    # SOURCE DATA
    # --------------------------------------------------
    finance = get_finance_summary(db) or {}
    budget = get_budget_summary(db) or {}
    pipeline = get_pipeline_summary(db) or {}
    backlog = calculate_backlog(db) or {}

    actual_revenue = _num(finance.get("actual_revenue"))
    actual_cost = _num(finance.get("actual_cost"))
    budget_revenue = _num(budget.get("budget_revenue"))
    budget_utilization = _num(budget.get("budget_utilization"))
    pipeline_value = _num(pipeline.get("pipeline_value"))
    weighted_pipeline = _num(pipeline.get("weighted_pipeline"))
    committed_backlog = _num(backlog.get("committed_backlog"))
    uncommitted_pipeline = _num(backlog.get("uncommitted_pipeline"))

    # --------------------------------------------------
    # CANONICAL DETERMINISTIC FORECAST
    # --------------------------------------------------
    forecast_result = build_forecast(
        committed_backlog=committed_backlog,
        weighted_pipeline=weighted_pipeline,
        utilization=budget_utilization,
        target_utilization=0.75,
        risk_rate=0.05,
    )

    canonical_forecast = _num(forecast_result.forecast_revenue)
    utilization_adjustment = _num(
        forecast_result.utilization_adjustment
    )
    # Internally positive = magnitude of execution haircut.
    risk_adjustment = abs(_num(forecast_result.risk_adjustment))

    forecast_decomposition = {
        "committed_backlog": round(committed_backlog, 2),
        "weighted_pipeline": round(weighted_pipeline, 2),
        "utilization_adjustment": round(utilization_adjustment, 2),
        "risk_adjustment": round(-risk_adjustment, 2),
        "forecast_revenue": round(canonical_forecast, 2),
    }

    # --------------------------------------------------
    # RISK
    # --------------------------------------------------
    risk = calculate_forecast_risk(
        forecast_revenue=canonical_forecast,
        committed_backlog=committed_backlog,
        weighted_pipeline=weighted_pipeline,
        budget_revenue=budget_revenue,
        risk_adjustment=risk_adjustment,
    )

    # --------------------------------------------------
    # FINANCIAL REASONING
    # --------------------------------------------------
    reasoning = explain_financial_position(
        actual_revenue=actual_revenue,
        budget_revenue=budget_revenue,
        forecast_revenue=canonical_forecast,
        committed_backlog=committed_backlog,
        weighted_pipeline=weighted_pipeline,
    )

    # Risk engine is authoritative for risk metrics.
    reasoning.update(
        {
            "forward_position": (
                "strong"
                if risk["headroom_status"] == "strong"
                else risk["headroom_status"]
            ),
            "committed_forecast_coverage": risk[
                "committed_forecast_coverage"
            ],
            "committed_revenue_mix": (
                committed_backlog
                / (committed_backlog + weighted_pipeline)
                * 100
                if committed_backlog + weighted_pipeline > 0
                else 0.0
            ),
            "pipeline_dependency": risk["pipeline_dependency"],
            "forecast_risk": risk["forecast_risk"],
            "pipeline_risk": risk["pipeline_risk"],
            "forecast_headroom": risk["forecast_headroom"],
            "forecast_headroom_pct": risk["forecast_headroom_pct"],
        }
    )

    # --------------------------------------------------
    # MONTE CARLO
    # --------------------------------------------------
    monte_carlo = run_monte_carlo_forecast(
        actual_revenue=actual_revenue,
        budget_revenue=budget_revenue,
        committed_backlog=committed_backlog,
        weighted_pipeline=weighted_pipeline,
        utilization_adjustment=utilization_adjustment,
        risk_adjustment=risk_adjustment,
        iterations=5000,
        random_seed=42,
    )

    # --------------------------------------------------
    # STAFFING
    # --------------------------------------------------
    staffing = calculate_staffing_position(db)
    staffing_insights = generate_staffing_insights(staffing)
    staffing_recommendations = generate_staffing_recommendations(
        staffing,
        staffing_insights,
    )

    # --------------------------------------------------
    # INSIGHTS
    # --------------------------------------------------
    insights = generate_insights(
        reasoning=reasoning,
        risk=risk,
        monte_carlo=monte_carlo,
        staffing=staffing,
    )

    # --------------------------------------------------
    # RECOMMENDATIONS
    # --------------------------------------------------
    recommendations = generate_recommendations(
        reasoning=reasoning,
        insights=insights,
        risk=risk,
        monte_carlo=monte_carlo,
    )

    # Add staffing actions only when they are not already represented.
    existing_categories = {
        item.get("category") for item in recommendations
    }
    for item in staffing_recommendations:
        if item.get("category") not in existing_categories:
            recommendations.append(item)
            existing_categories.add(item.get("category"))

    priority_rank = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    recommendations.sort(
        key=lambda item: priority_rank.get(
            str(item.get("priority", "LOW")).upper(), 3
        )
    )

    # --------------------------------------------------
    # DATA QUALITY
    # --------------------------------------------------
    data_quality_flags = []

    if staffing.get("utilization_data_quality") == "review_required":
        data_quality_flags.append(
            {
                "severity": "HIGH",
                "area": "staffing",
                "message": (
                    "Staffing utilization cannot be treated as a "
                    "true utilization rate because the available "
                    "schema provides hours budget rather than a "
                    "capacity-hours denominator."
                ),
            }
        )

    if canonical_forecast <= 0 and budget_revenue > 0:
        data_quality_flags.append(
            {
                "severity": "HIGH",
                "area": "forecast",
                "message": "Canonical forecast is non-positive.",
            }
        )

    # --------------------------------------------------
    # RESPONSE
    # --------------------------------------------------
    return _round_dict(
        {
            "status": "healthy",
            "canonical_forecast_revenue": canonical_forecast,
            "reasoning": reasoning,
            "risk": risk,
            "monte_carlo": monte_carlo,
            "staffing": staffing,
            "insights": insights,
            "recommendations": recommendations,
            "staffing_insights": staffing_insights,
            "staffing_recommendations": staffing_recommendations,
            "data_quality": {
                "status": "review_required"
                if data_quality_flags
                else "ok",
                "flags": data_quality_flags,
            },
            "source_metrics": {
                "actual_revenue": actual_revenue,
                "actual_cost": actual_cost,
                "budget_revenue": budget_revenue,
                "budget_utilization": budget_utilization,
                "pipeline_value": pipeline_value,
                "weighted_pipeline": weighted_pipeline,
                "committed_backlog": committed_backlog,
                "uncommitted_pipeline": uncommitted_pipeline,
            },
            "forecast": {
                "committed_backlog": forecast_result.committed_backlog,
                "weighted_pipeline": forecast_result.weighted_pipeline,
                "utilization_adjustment": utilization_adjustment,
                "risk_adjustment": -risk_adjustment,
                "forecast_revenue": canonical_forecast,
            },
            "forecast_decomposition": forecast_decomposition,
        }
    )
