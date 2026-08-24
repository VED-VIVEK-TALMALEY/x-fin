from dataclasses import dataclass
from decimal import Decimal


@dataclass
class ForecastResult:
    backlog_revenue: Decimal
    pipeline_revenue: Decimal
    capacity_adjustment: Decimal
    risk_adjustment: Decimal
    total_forecast: Decimal


def calculate_forecast(
    backlog_revenue: Decimal,
    pipeline_revenue: Decimal,
    utilization: Decimal = Decimal("0.75"),
    target_utilization: Decimal = Decimal("0.75"),
    risk_rate: Decimal = Decimal("0.05"),
) -> ForecastResult:

    utilization_factor = (
        utilization / target_utilization
        if target_utilization > 0
        else Decimal("1")
    )

    capacity_adjustment = (
        backlog_revenue * (utilization_factor - Decimal("1"))
    )

    gross_forecast = (
        backlog_revenue
        + pipeline_revenue
        + capacity_adjustment
    )

    risk_adjustment = (
        gross_forecast * risk_rate
    )

    total_forecast = gross_forecast - risk_adjustment

    return ForecastResult(
        backlog_revenue=backlog_revenue.quantize(Decimal("0.01")),
        pipeline_revenue=pipeline_revenue.quantize(Decimal("0.01")),
        capacity_adjustment=capacity_adjustment.quantize(Decimal("0.01")),
        risk_adjustment=risk_adjustment.quantize(Decimal("0.01")),
        total_forecast=total_forecast.quantize(Decimal("0.01")),
    )