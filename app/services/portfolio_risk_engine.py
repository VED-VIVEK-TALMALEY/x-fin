"""
Portfolio Risk Engine
---------------------

Combines revenue leakage, pipeline, margin, forecast and concentration
signals into a single portfolio risk view.

This engine does not replace the existing risk_engine.py.

Instead it creates a higher-level portfolio risk layer.
"""

from __future__ import annotations

from typing import Any, Dict


def _float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _clamp(value: float, low: float = 0.0, high: float = 100.0):
    return max(low, min(high, value))


def build_portfolio_risk(
    *,
    leakage: Dict[str, Any] | None = None,
    pipeline: Dict[str, Any] | None = None,
    margin: Dict[str, Any] | None = None,
    forecast: Dict[str, Any] | None = None,
    risk: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    leakage = leakage or {}
    pipeline = pipeline or {}
    margin = margin or {}
    forecast = forecast or {}
    risk = risk or {}

    existing_risk_score = _float(
        risk.get("risk_score"),
        0.0,
    )

    pipeline_quality = _float(
        pipeline.get("pipeline_quality_score"),
        100.0,
    )

    concentration = _float(
        pipeline.get("concentration_pct"),
        0.0,
    )

    leakage_rate = _float(
        leakage.get("leakage_rate_pct"),
        0.0,
    )

    margin_status = str(
        margin.get("status", "LOW")
    ).upper()

    margin_penalty = {
        "HIGH": 25.0,
        "MEDIUM": 12.0,
        "LOW": 0.0,
    }.get(
        margin_status,
        0.0,
    )

    # Pipeline weakness.
    pipeline_penalty = (
        100.0 - pipeline_quality
    ) * 0.25

    concentration_penalty = min(
        concentration * 0.20,
        20.0,
    )

    leakage_penalty = min(
        leakage_rate * 0.25,
        20.0,
    )

    margin_penalty = min(
        margin_penalty,
        25.0,
    )

    # Existing risk engine gets the strongest weighting because it is
    # already part of the canonical X-Fin forecast architecture.
    portfolio_score = (
        existing_risk_score * 0.40
        + pipeline_penalty
        + concentration_penalty
        + leakage_penalty
        + margin_penalty
    )

    portfolio_score = _clamp(
        portfolio_score
    )

    if portfolio_score >= 70:
        risk_level = "HIGH"
    elif portfolio_score >= 40:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    forecast_revenue = _float(
        forecast.get(
            "forecast_revenue",
            forecast.get("canonical_forecast_revenue"),
        )
    )

    forecast_gap = _float(
        forecast.get(
            "forecast_gap",
            forecast.get("forecast_vs_budget"),
        )
    )

    total_leakage = _float(
        leakage.get("total_potential_leakage")
    )

    margin_at_risk = _float(
        margin.get("margin_at_risk")
    )

    revenue_at_risk = (
        total_leakage
        + margin_at_risk
    )

    drivers = []

    if leakage_rate > 0:
        drivers.append(
            "revenue leakage"
        )

    if pipeline_quality < 60:
        drivers.append(
            "weak pipeline quality"
        )

    if concentration >= 30:
        drivers.append(
            "pipeline concentration"
        )

    if margin_status in {"HIGH", "MEDIUM"}:
        drivers.append(
            "margin deterioration"
        )

    if existing_risk_score >= 60:
        drivers.append(
            "forecast execution risk"
        )

    return {
        "portfolio_risk_score": round(
            portfolio_score,
            2,
        ),
        "risk_level": risk_level,
        "revenue_at_risk": revenue_at_risk,
        "forecast_revenue": forecast_revenue,
        "forecast_gap": forecast_gap,
        "existing_risk_score": existing_risk_score,
        "pipeline_quality_score": pipeline_quality,
        "pipeline_concentration_pct": concentration,
        "leakage_rate_pct": leakage_rate,
        "margin_status": margin_status,
        "risk_drivers": drivers,
    }


def analyze_portfolio_risk(
    intelligence: Dict[str, Any],
) -> Dict[str, Any]:
    return build_portfolio_risk(
        leakage=intelligence.get("revenue_leakage"),
        pipeline=intelligence.get("pipeline_intelligence"),
        margin=intelligence.get("margin_risk"),
        forecast=intelligence.get("forecast"),
        risk=intelligence.get("risk"),
    )