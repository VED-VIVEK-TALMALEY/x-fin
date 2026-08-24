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
    actual: Decimal,
    budget: Decimal,
    forecast: Decimal,
) -> VarianceResult:

    actual_vs_budget = actual - budget
    forecast_vs_budget = forecast - budget

    actual_pct = (
        actual_vs_budget / budget * Decimal("100")
        if budget != 0
        else Decimal("0")
    )

    forecast_pct = (
        forecast_vs_budget / budget * Decimal("100")
        if budget != 0
        else Decimal("0")
    )

    return VarianceResult(
        actual=actual,
        budget=budget,
        forecast=forecast,
        actual_vs_budget=actual_vs_budget.quantize(Decimal("0.01")),
        actual_vs_budget_pct=actual_pct.quantize(Decimal("0.01")),
        forecast_vs_budget=forecast_vs_budget.quantize(Decimal("0.01")),
        forecast_vs_budget_pct=forecast_pct.quantize(Decimal("0.01")),
    )