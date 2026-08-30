"""
Pipeline Intelligence Engine
----------------------------

Transforms raw pipeline opportunities into:
- weighted pipeline
- conversion-adjusted pipeline
- concentration risk
- stale opportunity risk
- stage risk
- pipeline quality score
- top opportunities requiring management attention
"""

from __future__ import annotations

from typing import Any, Dict, List


DEFAULT_STAGE_PROBABILITIES = {
    "lead": 0.10,
    "prospect": 0.20,
    "qualification": 0.30,
    "qualified": 0.35,
    "proposal": 0.50,
    "negotiation": 0.70,
    "contract": 0.85,
    "committed": 0.95,
    "closed_won": 1.00,
    "won": 1.00,
    "closed_lost": 0.00,
    "lost": 0.00,
}


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
        for key in ("pipeline", "opportunities", "records", "data", "items"):
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


def _stage_probability(record: Dict[str, Any]) -> float:
    explicit = _first(
        record,
        "probability",
        "win_probability",
        "conversion_probability",
    )

    if explicit is not None:
        probability = _float(explicit)

        if probability > 1:
            probability /= 100

        return max(0.0, min(probability, 1.0))

    stage = str(
        _first(record, "stage", "pipeline_stage", default="")
    ).strip().lower()

    return DEFAULT_STAGE_PROBABILITIES.get(stage, 0.25)


def analyze_opportunity(
    opportunity: Dict[str, Any],
) -> Dict[str, Any]:
    value = _float(
        _first(
            opportunity,
            "pipeline_value",
            "opportunity_value",
            "deal_value",
            "value",
            "revenue",
        )
    )

    probability = _stage_probability(opportunity)

    weighted_value = value * probability

    age_days = _float(
        _first(
            opportunity,
            "age_days",
            "days_open",
            "opportunity_age_days",
        )
    )

    if age_days >= 180:
        freshness = "STALE"
        stale_penalty = 0.25
    elif age_days >= 90:
        freshness = "AGING"
        stale_penalty = 0.10
    else:
        freshness = "FRESH"
        stale_penalty = 0.0

    adjusted_probability = max(
        0.0,
        probability * (1.0 - stale_penalty),
    )

    adjusted_weighted_value = (
        value * adjusted_probability
    )

    risk_score = (
        (1.0 - probability) * 60
        + min(age_days / 180, 1.0) * 40
    )

    if risk_score >= 65:
        risk = "HIGH"
    elif risk_score >= 35:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    opportunity_id = _first(
        opportunity,
        "opportunity_id",
        "deal_id",
        "id",
        default="unknown",
    )

    return {
        "opportunity_id": opportunity_id,
        "opportunity_name": _first(
            opportunity,
            "opportunity_name",
            "name",
            "deal_name",
            default=str(opportunity_id),
        ),
        "business_unit": _first(
            opportunity,
            "business_unit",
            "unit",
            default="Unknown",
        ),
        "stage": _first(
            opportunity,
            "stage",
            "pipeline_stage",
            default="Unknown",
        ),
        "value": value,
        "probability": probability,
        "weighted_value": weighted_value,
        "adjusted_probability": adjusted_probability,
        "adjusted_weighted_value": adjusted_weighted_value,
        "age_days": age_days,
        "freshness": freshness,
        "risk_score": risk_score,
        "risk": risk,
    }


def analyze_pipeline(data: Any) -> Dict[str, Any]:
    opportunities = _records(data)

    analyzed = [
        analyze_opportunity(item)
        for item in opportunities
    ]

    total_value = sum(x["value"] for x in analyzed)
    weighted_value = sum(x["weighted_value"] for x in analyzed)
    adjusted_value = sum(
        x["adjusted_weighted_value"]
        for x in analyzed
    )

    high_risk = [
        x
        for x in analyzed
        if x["risk"] == "HIGH"
    ]

    stale = [
        x
        for x in analyzed
        if x["freshness"] == "STALE"
    ]

    # Concentration is measured as the share represented by the
    # largest opportunity.
    largest_opportunity = max(
        (x["value"] for x in analyzed),
        default=0.0,
    )

    concentration_pct = (
        largest_opportunity / total_value * 100
        if total_value
        else 0.0
    )

    average_probability = (
        sum(x["probability"] for x in analyzed)
        / len(analyzed)
        if analyzed
        else 0.0
    )

    conversion_gap = max(
        total_value - adjusted_value,
        0.0,
    )

    # 100 = excellent pipeline quality.
    quality_score = 100.0

    quality_score -= min(
        concentration_pct * 0.40,
        30,
    )

    quality_score -= min(
        len(stale) / len(analyzed) * 30
        if analyzed
        else 0,
        30,
    )

    quality_score -= (
        (1.0 - average_probability) * 30
    )

    quality_score = max(
        0.0,
        min(100.0, quality_score),
    )

    if quality_score >= 70:
        quality_band = "STRONG"
    elif quality_score >= 45:
        quality_band = "MODERATE"
    else:
        quality_band = "WEAK"

    attention = sorted(
        analyzed,
        key=lambda x: (
            x["risk_score"],
            x["value"],
        ),
        reverse=True,
    )

    return {
        "pipeline_value": total_value,
        "weighted_pipeline": weighted_value,
        "risk_adjusted_pipeline": adjusted_value,
        "conversion_gap": conversion_gap,
        "opportunity_count": len(analyzed),
        "average_probability_pct": average_probability * 100,
        "pipeline_quality_score": quality_score,
        "pipeline_quality_band": quality_band,
        "largest_opportunity_value": largest_opportunity,
        "concentration_pct": concentration_pct,
        "stale_opportunities": len(stale),
        "high_risk_opportunities": len(high_risk),
        "top_attention_opportunities": attention[:10],
        "opportunities": analyzed,
    }


def build_pipeline_intelligence(
    data: Any,
) -> Dict[str, Any]:
    return analyze_pipeline(data)