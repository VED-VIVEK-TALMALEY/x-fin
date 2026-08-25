from typing import Dict


def explain_financial_position(
    actual_revenue: float,
    budget_revenue: float,
    forecast_revenue: float,
    committed_backlog: float,
    weighted_pipeline: float,
) -> Dict:

    actual_revenue = float(actual_revenue or 0)
    budget_revenue = float(budget_revenue or 0)
    forecast_revenue = float(forecast_revenue or 0)
    committed_backlog = float(committed_backlog or 0)
    weighted_pipeline = float(weighted_pipeline or 0)

    # --------------------------------------------------
    # ACTUAL VS BUDGET
    # --------------------------------------------------

    budget_gap = actual_revenue - budget_revenue

    if budget_revenue:
        budget_gap_pct = (
            budget_gap / budget_revenue
        ) * 100
    else:
        budget_gap_pct = 0.0

    # --------------------------------------------------
    # FORECAST VS BUDGET
    # --------------------------------------------------

    forecast_gap = forecast_revenue - budget_revenue

    if budget_revenue:
        forecast_gap_pct = (
            forecast_gap / budget_revenue
        ) * 100
    else:
        forecast_gap_pct = 0.0

    # --------------------------------------------------
    # FORWARD REVENUE
    #
    # Forward revenue consists of:
    #   1. Committed backlog
    #   2. Probability-weighted pipeline
    # --------------------------------------------------

    forward_revenue = (
        committed_backlog
        + weighted_pipeline
    )

    if budget_revenue:
        forward_coverage = (
            forward_revenue / budget_revenue
        ) * 100
    else:
        forward_coverage = 0.0

    # --------------------------------------------------
    # PERFORMANCE STATUS
    # --------------------------------------------------

    if budget_gap > 0:
        performance = "ahead_of_plan"

    elif budget_gap < 0:
        performance = "below_plan"

    else:
        performance = "on_plan"

    # --------------------------------------------------
    # FORECAST STATUS
    # --------------------------------------------------

    if forecast_gap > 0:
        forecast_status = "on_or_above_plan"

    elif forecast_gap < 0:
        forecast_status = "below_plan"

    else:
        forecast_status = "on_plan"

    # --------------------------------------------------
    # FORECAST COMMITTED COVERAGE
    #
    # IMPORTANT:
    # This is NOT statistical forecast confidence.
    #
    # It measures how much of the forecast is supported
    # by committed backlog.
    # --------------------------------------------------

    if forecast_revenue > 0:
        committed_forecast_coverage = (
            committed_backlog
            / forecast_revenue
        ) * 100
    else:
        committed_forecast_coverage = 0.0

    # --------------------------------------------------
    # PIPELINE DEPENDENCY
    #
    # Measures how much forward revenue depends on
    # weighted pipeline rather than committed backlog.
    # --------------------------------------------------

    if forward_revenue > 0:
        pipeline_dependency = (
            weighted_pipeline
            / forward_revenue
        ) * 100
    else:
        pipeline_dependency = 0.0

    # --------------------------------------------------
    # COMMITTED REVENUE MIX
    # --------------------------------------------------

    if forward_revenue > 0:
        committed_revenue_mix = (
            committed_backlog
            / forward_revenue
        ) * 100
    else:
        committed_revenue_mix = 0.0

    # --------------------------------------------------
    # FORECAST HEADROOM
    #
    # Positive = forecast above budget
    # Negative = forecast below budget
    # --------------------------------------------------

    forecast_headroom = forecast_gap

    if budget_revenue > 0:
        forecast_headroom_pct = (
            forecast_headroom
            / budget_revenue
        ) * 100
    else:
        forecast_headroom_pct = 0.0

    # --------------------------------------------------
    # FORECAST RISK CLASSIFICATION
    #
    # This is a deterministic business-risk indicator,
    # not a probabilistic/statistical confidence score.
    # --------------------------------------------------

    if committed_forecast_coverage >= 70:
        forecast_risk = "low"

    elif committed_forecast_coverage >= 50:
        forecast_risk = "moderate"

    else:
        forecast_risk = "high"

    # --------------------------------------------------
    # PIPELINE RISK CLASSIFICATION
    # --------------------------------------------------

    if pipeline_dependency <= 30:
        pipeline_risk = "low"

    elif pipeline_dependency <= 50:
        pipeline_risk = "moderate"

    else:
        pipeline_risk = "high"

    # --------------------------------------------------
    # OVERALL FORWARD POSITION
    # --------------------------------------------------

    if forward_coverage >= 120:
        forward_position = "strong"

    elif forward_coverage >= 100:
        forward_position = "adequate"

    elif forward_coverage >= 80:
        forward_position = "watch"

    else:
        forward_position = "weak"

    # --------------------------------------------------
    # RETURN
    # --------------------------------------------------

    return {
        # Core statuses
        "performance": performance,
        "forecast_status": forecast_status,

        # Core financial values
        "actual_revenue": round(
            actual_revenue,
            2,
        ),

        "budget_revenue": round(
            budget_revenue,
            2,
        ),

        "forecast_revenue": round(
            forecast_revenue,
            2,
        ),

        "committed_backlog": round(
            committed_backlog,
            2,
        ),

        "weighted_pipeline": round(
            weighted_pipeline,
            2,
        ),

        # Actual vs budget
        "budget_gap": round(
            budget_gap,
            2,
        ),

        "budget_gap_pct": round(
            budget_gap_pct,
            2,
        ),

        # Forecast vs budget
        "forecast_gap": round(
            forecast_gap,
            2,
        ),

        "forecast_gap_pct": round(
            forecast_gap_pct,
            2,
        ),

        # Forward position
        "forward_revenue": round(
            forward_revenue,
            2,
        ),

        "forward_coverage": round(
            forward_coverage,
            2,
        ),

        "forward_position": forward_position,

        # Forecast composition
        "committed_forecast_coverage": round(
            committed_forecast_coverage,
            2,
        ),

        "committed_revenue_mix": round(
            committed_revenue_mix,
            2,
        ),

        "pipeline_dependency": round(
            pipeline_dependency,
            2,
        ),

        # Risk
        "forecast_risk": forecast_risk,
        "pipeline_risk": pipeline_risk,

        # Forecast headroom
        "forecast_headroom": round(
            forecast_headroom,
            2,
        ),

        "forecast_headroom_pct": round(
            forecast_headroom_pct,
            2,
        ),

        # Backward-compatible field.
        #
        # Existing app.py uses this field.
        # It now explicitly represents committed
        # forecast coverage rather than claiming to
        # be statistical confidence.
        "forecast_confidence_base": round(
            committed_forecast_coverage,
            2,
        ),
    }