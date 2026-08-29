from app.services.monte_carlo_engine import run_monte_carlo_forecast


def test_monte_carlo_is_deterministic():
    kwargs = dict(
        actual_revenue=600000,
        budget_revenue=500000,
        committed_backlog=300000,
        weighted_pipeline=250000,
        utilization_adjustment=10000,
        risk_adjustment=20000,
        iterations=5000,
        random_seed=42,
    )

    first = run_monte_carlo_forecast(**kwargs)
    second = run_monte_carlo_forecast(**kwargs)

    assert first == second
    assert first["distribution"]["p10"] <= first["distribution"]["p50"]
    assert first["distribution"]["p50"] <= first["distribution"]["p90"]
    assert (
        first["budget_analysis"]["probability_above_budget"]
        + first["budget_analysis"]["probability_below_budget"]
        == 100
    )


def test_monte_carlo_rejects_invalid_iterations():
    try:
        run_monte_carlo_forecast(
            actual_revenue=100,
            budget_revenue=100,
            committed_backlog=100,
            weighted_pipeline=100,
            iterations=99,
        )
    except ValueError as exc:
        assert "at least 100" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
