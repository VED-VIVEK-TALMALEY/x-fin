from typing import Dict


def build_forecast_decomposition(
    committed_backlog: float,
    weighted_pipeline: float,
    utilization_adjustment: float,
    risk_adjustment: float,
) -> Dict:
    """
    Build an explainable decomposition of the revenue forecast.

    The forecast is constructed from:

        Committed Backlog
        + Weighted Pipeline
        + Utilization Adjustment
        - Risk Adjustment
        = Forecast Revenue

    All monetary values are returned as floats rounded to 2 decimals.
    """

    committed_backlog = float(
        committed_backlog or 0
    )

    weighted_pipeline = float(
        weighted_pipeline or 0
    )

    utilization_adjustment = float(
        utilization_adjustment or 0
    )

    risk_adjustment = float(
        risk_adjustment or 0
    )

    forecast_revenue = (
        committed_backlog
        + weighted_pipeline
        + utilization_adjustment
        - risk_adjustment
    )

    return {
        "committed_backlog": round(
            committed_backlog,
            2,
        ),
        "weighted_pipeline": round(
            weighted_pipeline,
            2,
        ),
        "utilization_adjustment": round(
            utilization_adjustment,
            2,
        ),
        "risk_adjustment": round(
            risk_adjustment,
            2,
        ),
        "forecast_revenue": round(
            forecast_revenue,
            2,
        ),
    }