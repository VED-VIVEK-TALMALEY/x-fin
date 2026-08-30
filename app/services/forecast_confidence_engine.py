from __future__ import annotations

from typing import Dict


def calculate_forecast_confidence(
    forecast_revenue: float,
    budget_revenue: float,
    committed_backlog: float,
    weighted_pipeline: float,
    forecast_accuracy: float | None = None,
) -> Dict:
    """
    Estimate forecast confidence from observable revenue support.

    This is an explainable confidence framework, not a statistical
    probability claim.

    Confidence is primarily driven by:
    1. Committed backlog coverage
    2. Pipeline support
    3. Position versus budget
    4. Historical forecast accuracy, when available
    """

    forecast_revenue = float(forecast_revenue or 0)
    budget_revenue = float(budget_revenue or 0)
    committed_backlog = float(committed_backlog or 0)
    weighted_pipeline = float(weighted_pipeline or 0)

    # ---------------------------------------------------------
    # Insufficient data
    # ---------------------------------------------------------

    if forecast_revenue <= 0:
        return {
            "confidence_score": 0.0,
            "confidence_band": "insufficient_data",
            "confidence_drivers": [
                "Forecast revenue is zero or unavailable."
            ],
        }

    # ---------------------------------------------------------
    # Coverage calculations
    # ---------------------------------------------------------

    committed_coverage = committed_backlog / forecast_revenue

    pipeline_coverage = weighted_pipeline / forecast_revenue

    budget_support = (
        forecast_revenue / budget_revenue
        if budget_revenue > 0
        else 1.0
    )

    # ---------------------------------------------------------
    # Confidence scoring
    #
    # Maximum base score = 100
    #
    # Committed revenue: 65
    # Pipeline support: 15
    # Budget position: 20
    # ---------------------------------------------------------

    score = 0.0
    drivers = []

    # ---------------------------------------------------------
    # 1. Committed revenue
    # ---------------------------------------------------------
    # Committed backlog is the strongest confidence signal.
    # Once >=80% of forecast revenue is committed, the forecast
    # receives the maximum commitment-confidence contribution.

    if committed_coverage >= 0.80:
        commitment_score = 65

    else:
        commitment_score = (
            min(committed_coverage, 1.0) / 0.80
        ) * 65

    score += commitment_score

    if committed_coverage >= 0.80:
        drivers.append(
            "Very strong committed-revenue coverage."
        )
    elif committed_coverage >= 0.70:
        drivers.append(
            "Strong committed-revenue coverage."
        )
    elif committed_coverage >= 0.50:
        drivers.append(
            "Moderate committed-revenue coverage."
        )
    else:
        drivers.append(
            "Low committed-revenue coverage."
        )

    # ---------------------------------------------------------
    # 2. Pipeline support
    # ---------------------------------------------------------

    pipeline_score = min(pipeline_coverage, 1.0) * 15

    score += pipeline_score

    if pipeline_coverage > 0.50:
        drivers.append(
            "Forecast has significant pipeline dependency."
        )
    elif pipeline_coverage > 0.30:
        drivers.append(
            "Forecast has moderate pipeline dependency."
        )
    else:
        drivers.append(
            "Pipeline dependency is limited."
        )

    # ---------------------------------------------------------
    # 3. Budget position
    # ---------------------------------------------------------

    if budget_support >= 1.05:
        score += 20
        drivers.append(
            "Forecast is materially above budget."
        )

    elif budget_support >= 1.00:
        score += 15
        drivers.append(
            "Forecast is at or above budget."
        )

    elif budget_support >= 0.95:
        score += 8
        drivers.append(
            "Forecast is slightly below budget."
        )

    else:
        drivers.append(
            "Forecast is materially below budget."
        )

    # ---------------------------------------------------------
    # 4. Historical forecast accuracy
    # ---------------------------------------------------------

    if forecast_accuracy is not None:

        accuracy = max(
            0.0,
            min(float(forecast_accuracy), 1.0),
        )

        score = (
            score * 0.85
            + (accuracy * 100 * 0.15)
        )

        if accuracy >= 0.90:
            drivers.append(
                "Historical forecast accuracy is strong."
            )

        elif accuracy < 0.75:
            drivers.append(
                "Historical forecast accuracy is weak."
            )

    # ---------------------------------------------------------
    # Normalize score
    # ---------------------------------------------------------

    score = round(
        max(0.0, min(score, 100.0)),
        2,
    )

    # ---------------------------------------------------------
    # Confidence band
    # ---------------------------------------------------------

    if score >= 80:
        band = "high"

    elif score >= 60:
        band = "moderate"

    elif score >= 40:
        band = "low"

    else:
        band = "very_low"

    return {
        "confidence_score": score,
        "confidence_band": band,
        "confidence_drivers": drivers,
    }