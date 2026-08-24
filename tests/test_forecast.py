from app.services.forecast_engine import build_forecast


def test_forecast():

    result = build_forecast(
        committed_backlog=100000,
        weighted_pipeline=50000,
        utilization=0.75,
        target_utilization=0.75,
        risk_rate=0.05,
    )

    assert result.forecast_revenue == 142500.00