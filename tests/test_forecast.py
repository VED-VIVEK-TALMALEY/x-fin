from decimal import Decimal

from app.services.forecast_engine import calculate_forecast


def test_forecast():

    result = calculate_forecast(
        backlog_revenue=Decimal("100000"),
        pipeline_revenue=Decimal("50000"),
        utilization=Decimal("0.75"),
        target_utilization=Decimal("0.75"),
        risk_rate=Decimal("0.05"),
    )

    assert result.total_forecast == Decimal(
        "142500.00"
    )