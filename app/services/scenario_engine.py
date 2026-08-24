from decimal import Decimal


def run_scenario(
    base_revenue: Decimal,
    pipeline_revenue: Decimal,
    utilization: Decimal,
    billing_rate_change: Decimal = Decimal("0"),
    pipeline_conversion_change: Decimal = Decimal("0"),
    utilization_change: Decimal = Decimal("0"),
    slippage_rate: Decimal = Decimal("0"),
):

    adjusted_pipeline = (
        pipeline_revenue
        * (Decimal("1") + pipeline_conversion_change)
    )

    adjusted_utilization = (
        utilization + utilization_change
    )

    utilization_factor = (
        adjusted_utilization / utilization
        if utilization > 0
        else Decimal("1")
    )

    adjusted_revenue = (
        base_revenue
        * utilization_factor
        * (Decimal("1") + billing_rate_change)
    )

    adjusted_revenue += adjusted_pipeline

    adjusted_revenue *= (
        Decimal("1") - slippage_rate
    )

    return {
        "base_revenue": base_revenue.quantize(Decimal("0.01")),
        "adjusted_pipeline": adjusted_pipeline.quantize(Decimal("0.01")),
        "adjusted_utilization": adjusted_utilization.quantize(Decimal("0.01")),
        "scenario_revenue": adjusted_revenue.quantize(Decimal("0.01")),
        "revenue_change": (
            adjusted_revenue - base_revenue
        ).quantize(Decimal("0.01")),
    }