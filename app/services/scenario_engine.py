from decimal import Decimal


def run_scenario(
    base_revenue: float,
    pipeline_revenue: float,
    utilization: float,
    pipeline_conversion_change: float = 0.0,
    utilization_change: float = 0.0,
    billing_rate_change: float = 0.0,
    slippage_rate: float = 0.0,
):

    adjusted_pipeline = (
        pipeline_revenue
        * (1 + pipeline_conversion_change)
    )

    adjusted_utilization = (
        utilization + utilization_change
    )

    utilization_factor = (
        adjusted_utilization / utilization
        if utilization
        else 1
    )

    adjusted_revenue = (
        base_revenue
        * utilization_factor
        * (1 + billing_rate_change)
    )

    adjusted_revenue += adjusted_pipeline

    adjusted_revenue *= (
        1 - slippage_rate
    )

    return {
        "base_revenue": round(
            base_revenue,
            2,
        ),
        "adjusted_pipeline": round(
            adjusted_pipeline,
            2,
        ),
        "adjusted_utilization": round(
            adjusted_utilization,
            4,
        ),
        "scenario_revenue": round(
            adjusted_revenue,
            2,
        ),
        "revenue_change": round(
            adjusted_revenue - base_revenue,
            2,
        ),
        "revenue_change_pct": round(
            (
                (
                    adjusted_revenue
                    - base_revenue
                )
                / base_revenue
                * 100
            )
            if base_revenue
            else 0,
            2,
        ),
    }