import pytest
from app.services.scenario_engine import run_scenario


def test_scenario_applies_pipeline_and_slippage():
    result = run_scenario(
        base_revenue=5_000_000,
        pipeline_revenue=2_000_000,
        utilization=0.74,
        pipeline_conversion_change=0.10,
        utilization_change=0.02,
        billing_rate_change=0.05,
        slippage_rate=0.03,
    )

    assert result["adjusted_pipeline"] == 2_200_000
    assert result["adjusted_utilization"] == 0.76
    assert result["scenario_revenue"] == pytest.approx(
    7_364_135.14,
    abs=0.01,
)
    assert result["revenue_change"] == pytest.approx(
    2_364_135.14,
    abs=0.01,
)
    assert result["revenue_change_pct"] == pytest.approx(
    47.28,
    abs=0.01,
)

def test_zero_base_revenue_does_not_divide_by_zero():
    result = run_scenario(
        base_revenue=0,
        pipeline_revenue=1000,
        utilization=0,
    )

    assert result["revenue_change_pct"] == 0
