from app.services.forecast_confidence_engine import (
    calculate_forecast_confidence,
)


def test_strong_committed_coverage_has_high_confidence():

    result = calculate_forecast_confidence(
        forecast_revenue=10_000_000,
        budget_revenue=9_000_000,
        committed_backlog=8_000_000,
        weighted_pipeline=1_000_000,
    )

    assert result["confidence_score"] >= 80
    assert result["confidence_band"] == "high"


def test_zero_forecast_returns_insufficient_data():

    result = calculate_forecast_confidence(
        forecast_revenue=0,
        budget_revenue=1_000_000,
        committed_backlog=0,
        weighted_pipeline=0,
    )

    assert result["confidence_band"] == "insufficient_data"