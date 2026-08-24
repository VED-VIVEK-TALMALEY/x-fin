from decimal import Decimal

from app.services.variance_engine import calculate_variance


def test_variance():

    result = calculate_variance(
        actual=Decimal("90"),
        budget=Decimal("100"),
        forecast=Decimal("95"),
    )

    assert result.actual_vs_budget == Decimal("-10.00")
    assert result.actual_vs_budget_pct == Decimal("-10.00")