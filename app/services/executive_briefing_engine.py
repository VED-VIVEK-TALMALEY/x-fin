"""
Executive Briefing Engine
-------------------------

Converts the X-Fin analytical outputs into a concise leadership briefing.

Output sections:
- headline
- financial position
- key risks
- opportunities
- management actions
- financial exposure
"""

from __future__ import annotations

from typing import Any, Dict, List


def _float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _money(value: Any) -> str:
    value = _float(value)

    absolute = abs(value)

    if absolute >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"

    if absolute >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"

    if absolute >= 1_000:
        return f"{value / 1_000:.1f}K"

    return f"{value:,.0f}"


def _pct(value: Any) -> str:
    return f"{_float(value):.1f}%"


def _priority(
    score: float,
) -> str:
    if score >= 70:
        return "HIGH"
    if score >= 40:
        return "MEDIUM"
    return "LOW"


def build_executive_briefing(
    intelligence: Dict[str, Any],
) -> Dict[str, Any]:
    reasoning = intelligence.get(
        "reasoning",
        {},
    )

    risk = intelligence.get(
        "risk",
        {},
    )

    forecast = intelligence.get(
        "forecast",
        {},
    )

    leakage = intelligence.get(
        "revenue_leakage",
        {},
    )

    pipeline = intelligence.get(
        "pipeline_intelligence",
        {},
    )

    margin = intelligence.get(
        "margin_risk",
        {},
    )

    portfolio = intelligence.get(
        "portfolio_risk",
        {},
    )

    actual_revenue = _float(
        reasoning.get("actual_revenue")
    )

    budget_revenue = _float(
        reasoning.get("budget_revenue")
    )

    forecast_revenue = _float(
        reasoning.get(
            "forecast_revenue",
            forecast.get("forecast_revenue"),
        )
    )

    budget_gap_pct = _float(
        reasoning.get("budget_gap_pct")
    )

    forecast_gap_pct = _float(
        reasoning.get("forecast_gap_pct")
    )

    portfolio_score = _float(
        portfolio.get(
            "portfolio_risk_score",
            risk.get("risk_score"),
        )
    )

    risk_level = portfolio.get(
        "risk_level",
        risk.get("overall_risk", "LOW"),
    )

    pipeline_quality = _float(
        pipeline.get("pipeline_quality_score")
    )

    weighted_pipeline = _float(
        pipeline.get("weighted_pipeline")
    )

    leakage_value = _float(
        leakage.get("total_potential_leakage")
    )

    margin_at_risk = _float(
        margin.get("margin_at_risk")
    )

    if budget_gap_pct >= 0:
        headline = (
            f"Revenue is {_pct(budget_gap_pct)} above budget."
        )
    else:
        headline = (
            f"Revenue is {_pct(abs(budget_gap_pct))} below budget."
        )

    if risk_level:
        headline += (
            f" Portfolio risk is "
            f"{str(risk_level).upper()}."
        )

    financial_position = {
        "actual_revenue": actual_revenue,
        "budget_revenue": budget_revenue,
        "forecast_revenue": forecast_revenue,
        "budget_gap_pct": budget_gap_pct,
        "forecast_gap_pct": forecast_gap_pct,
    }

    risks: List[Dict[str, Any]] = []

    if leakage_value > 0:
        risks.append(
            {
                "category": "Revenue Leakage",
                "severity": _priority(
                    min(
                        leakage_value /
                        max(actual_revenue, 1)
                        * 100,
                        100,
                    )
                ),
                "message": (
                    f"Potential revenue leakage of "
                    f"{_money(leakage_value)} identified."
                ),
                "financial_impact": leakage_value,
            }
        )

    if pipeline_quality < 60:
        risks.append(
            {
                "category": "Pipeline Quality",
                "severity": "HIGH",
                "message": (
                    f"Pipeline quality score is "
                    f"{pipeline_quality:.1f}/100."
                ),
                "financial_impact": weighted_pipeline,
            }
        )

    if margin_at_risk > 0:
        risks.append(
            {
                "category": "Margin Risk",
                "severity": "MEDIUM",
                "message": (
                    f"Estimated margin exposure is "
                    f"{_money(margin_at_risk)}."
                ),
                "financial_impact": margin_at_risk,
            }
        )

    if portfolio_score >= 70:
        risks.append(
            {
                "category": "Portfolio Risk",
                "severity": "HIGH",
                "message": (
                    f"Composite portfolio risk score is "
                    f"{portfolio_score:.1f}/100."
                ),
                "financial_impact": portfolio.get(
                    "revenue_at_risk",
                    0,
                ),
            }
        )

    actions: List[Dict[str, Any]] = []

    if leakage_value > 0:
        actions.append(
            {
                "priority": "HIGH",
                "category": "Revenue Recovery",
                "action": (
                    "Review the highest-value leakage cases "
                    "and reconcile delivered work against "
                    "billing and revenue recognition."
                ),
                "rationale": (
                    "Recovering existing delivery value has "
                    "lower execution risk than creating new demand."
                ),
                "financial_impact": leakage_value,
            }
        )

    if pipeline_quality < 60:
        actions.append(
            {
                "priority": "HIGH",
                "category": "Pipeline",
                "action": (
                    "Prioritize high-value opportunities with "
                    "strong conversion probability and remove "
                    "stale opportunities from the forecast."
                ),
                "rationale": (
                    "Weak pipeline quality increases dependence "
                    "on uncertain future conversion."
                ),
                "financial_impact": weighted_pipeline,
            }
        )

    if margin_at_risk > 0:
        actions.append(
            {
                "priority": "MEDIUM",
                "category": "Margin Protection",
                "action": (
                    "Review cost overruns and margin compression "
                    "across the highest-risk projects."
                ),
                "rationale": (
                    "Cost control protects profitability without "
                    "requiring additional revenue."
                ),
                "financial_impact": margin_at_risk,
            }
        )

    if not actions:
        actions.append(
            {
                "priority": "LOW",
                "category": "Monitoring",
                "action": (
                    "Continue monitoring forecast coverage, "
                    "pipeline quality and project margins."
                ),
                "rationale": (
                    "No material management intervention "
                    "was detected by the current signals."
                ),
                "financial_impact": 0,
            }
        )

    return {
        "headline": headline,
        "financial_position": financial_position,
        "portfolio_risk": portfolio,
        "key_risks": risks,
        "recommended_actions": actions,
        "financial_exposure": {
            "revenue_leakage": leakage_value,
            "margin_at_risk": margin_at_risk,
            "weighted_pipeline": weighted_pipeline,
            "total_identified_exposure": (
                leakage_value
                + margin_at_risk
            ),
        },
        "management_summary": (
            f"Actual revenue is {_money(actual_revenue)} "
            f"against a budget of {_money(budget_revenue)}, "
            f"with forecast revenue of "
            f"{_money(forecast_revenue)}. "
            f"Portfolio risk is "
            f"{str(risk_level).upper()}."
        ),
    }


def build_briefing(
    intelligence: Dict[str, Any],
) -> Dict[str, Any]:
    return build_executive_briefing(intelligence)