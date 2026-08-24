from app.services.variance_engine import calculate_variance


def test_variance():

    result = calculate_variance(
        actual=90,
        budget=100,
        forecast=95,
    )

    assert result.actual_vs_budget == -10
    assert result.actual_vs_budget_pct == -10
    assert result.forecast_vs_budget == -5
    assert result.forecast_vs_budget_pct == -5