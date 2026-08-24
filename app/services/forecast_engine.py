from dataclasses import dataclass


@dataclass
class ForecastResult:
    committed_backlog: float
    weighted_pipeline: float
    utilization_adjustment: float
    risk_adjustment: float
    forecast_revenue: float


def build_forecast(
    committed_backlog: float,
    weighted_pipeline: float,
    utilization: float,
    target_utilization: float = 0.75,
    risk_rate: float = 0.05,
):

    if target_utilization <= 0:
        raise ValueError(
            "target_utilization must be positive"
        )

    utilization_factor = (
        utilization / target_utilization
    )

    utilization_adjustment = (
        committed_backlog
        * (utilization_factor - 1)
    )

    gross_forecast = (
        committed_backlog
        + weighted_pipeline
        + utilization_adjustment
    )

    risk_adjustment = (
        gross_forecast * risk_rate
    )

    forecast = (
        gross_forecast - risk_adjustment
    )

    return ForecastResult(
        committed_backlog=round(
            committed_backlog,
            2,
        ),
        weighted_pipeline=round(
            weighted_pipeline,
            2,
        ),
        utilization_adjustment=round(
            utilization_adjustment,
            2,
        ),
        risk_adjustment=round(
            risk_adjustment,
            2,
        ),
        forecast_revenue=round(
            forecast,
            2,
        ),
    )