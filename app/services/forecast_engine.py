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
) -> ForecastResult:
    """
    Build the X-Fin deterministic revenue forecast.

    Forecast construction:

        Forecast
        =
        Committed Backlog
        + Weighted Pipeline
        + Utilization Adjustment
        - Execution Risk Adjustment

    All monetary values are expected to be in the same currency
    and units as the source financial data.
    """

    committed_backlog = float(committed_backlog or 0.0)
    weighted_pipeline = float(weighted_pipeline or 0.0)
    utilization = float(utilization or 0.0)
    target_utilization = float(target_utilization or 0.0)
    risk_rate = float(risk_rate or 0.0)

    # --------------------------------------------------
    # UTILIZATION ADJUSTMENT
    # --------------------------------------------------
    #
    # Positive utilization variance produces upside.
    # Negative utilization variance produces downside.
    #
    # We apply the utilization delta to the weighted
    # pipeline because pipeline realization is the
    # component most exposed to delivery capacity.
    #
    utilization_delta = utilization - target_utilization

    utilization_adjustment = (
        weighted_pipeline * utilization_delta
    )

    # --------------------------------------------------
    # EXECUTION RISK
    # --------------------------------------------------
    #
    # Risk is applied to the forward revenue base.
    #
    forward_revenue = (
        committed_backlog
        + weighted_pipeline
    )

    risk_adjustment = (
        forward_revenue * risk_rate
    )

    # --------------------------------------------------
    # FINAL FORECAST
    # --------------------------------------------------

    forecast_revenue = (
        committed_backlog
        + weighted_pipeline
        + utilization_adjustment
        - risk_adjustment
    )

    # Prevent pathological negative forecasts.
    forecast_revenue = max(
        forecast_revenue,
        0.0,
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
            forecast_revenue,
            2,
        ),
    )