from dataclasses import dataclass
from decimal import Decimal


@dataclass
class VarianceResult:
    actual: Decimal
    budget: Decimal
    forecast: Decimal
    actual_vs_budget: Decimal
    actual_vs_budget_pct: Decimal
    forecast_vs_budget: Decimal
    forecast_vs_budget_pct: Decimal


def calculate_variance(
    actual: float,
    budget: float,
    forecast: float,
):
    d_actual = Decimal(str(actual))
    d_budget = Decimal(str(budget))
    d_forecast = Decimal(str(forecast))

    actual_variance = d_actual - d_budget
    forecast_variance = d_forecast - d_budget

    actual_variance_pct = (
        (actual_variance / d_budget * Decimal("100"))
        if d_budget
        else Decimal("0")
    )

    forecast_variance_pct = (
        (forecast_variance / d_budget * Decimal("100"))
        if d_budget
        else Decimal("0")
    )

    # Returning both dict format (from original function logic) AND dataclass support if needed,
    # or returning the exact structure requested by the snippet combination without discarding metrics:
    return VarianceResult(
        actual=d_actual.quantize(Decimal("0.01")),
        budget=d_budget.quantize(Decimal("0.01")),
        forecast=d_forecast.quantize(Decimal("0.01")),
        actual_vs_budget=actual_variance.quantize(Decimal("0.01")),
        actual_vs_budget_pct=actual_variance_pct.quantize(Decimal("0.01")),
        forecast_vs_budget=forecast_variance.quantize(Decimal("0.01")),
        forecast_vs_budget_pct=forecast_variance_pct.quantize(Decimal("0.01")),
    )


def variance_bridge(
    budget: float,
    actual: float,
    project_slippage: float,
    pipeline_change: float,
    utilization_change: float,
    rate_change: float,
):
    total_explained = (
        project_slippage
        + pipeline_change
        + utilization_change
        + rate_change
    )

    unexplained = actual - budget - total_explained

    return {
        "budget": round(budget, 2),
        "project_slippage": round(project_slippage, 2),
        "pipeline_change": round(pipeline_change, 2),
        "utilization_change": round(utilization_change, 2),
        "rate_change": round(rate_change, 2),
        "unexplained": round(unexplained, 2),
        "actual": round(actual, 2),
    }