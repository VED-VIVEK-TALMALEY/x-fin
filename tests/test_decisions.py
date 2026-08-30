from app.services.decision_engine import generate_decisions


def test_high_pipeline_dependency_creates_action():

    result = generate_decisions(
        forecast_risk="low",
        confidence_band="moderate",
        pipeline_dependency=60,
        forecast_headroom_pct=10,
        variance_pct=2,
    )

    assert result["decision_count"] >= 1

    assert any(
        decision["area"] == "pipeline"
        for decision in result["decisions"]
    )


def test_negative_budget_headroom_creates_action():

    result = generate_decisions(
        forecast_risk="low",
        confidence_band="moderate",
        pipeline_dependency=20,
        forecast_headroom_pct=-5,
        variance_pct=2,
    )

    assert any(
        decision["area"] == "budget"
        for decision in result["decisions"]
    )