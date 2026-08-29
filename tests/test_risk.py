from app.services.risk_engine import calculate_forecast_risk


def test_high_pipeline_dependency_is_high_risk():
    result = calculate_forecast_risk(
        forecast_revenue=1_000_000,
        committed_backlog=400_000,
        weighted_pipeline=600_000,
        budget_revenue=900_000,
        risk_adjustment=50_000,
    )

    assert result["forecast_risk"] == "high"
    assert result["pipeline_risk"] == "high"
    assert result["overall_risk"] == "high"
    assert result["pipeline_dependency"] == 60.0


def test_strong_committed_coverage_is_low_risk():
    result = calculate_forecast_risk(
        forecast_revenue=1_000_000,
        committed_backlog=800_000,
        weighted_pipeline=200_000,
        budget_revenue=900_000,
        risk_adjustment=10_000,
    )

    assert result["forecast_risk"] == "low"
    assert result["pipeline_risk"] == "low"
    assert result["overall_risk"] == "low"
    assert result["headroom_status"] == "moderate"
