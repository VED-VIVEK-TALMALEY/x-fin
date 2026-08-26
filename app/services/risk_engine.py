from typing import Dict


def calculate_forecast_risk(
    forecast_revenue: float,
    committed_backlog: float,
    weighted_pipeline: float,
    budget_revenue: float,
    risk_adjustment: float = 0.0,
) -> Dict:
    """
    Calculate transparent forecast and pipeline risk indicators.

    The model deliberately separates:

    1. Forecast commitment coverage
       How much of the forecast is supported by committed backlog.

    2. Pipeline dependency
       How much forward revenue depends on weighted pipeline.

    3. Forecast headroom
       How far the forecast is above/below budget.

    4. Execution-risk haircut
       The absolute risk adjustment applied by the forecast engine.

    The output is intended for executive finance reporting and
    should remain deterministic and explainable.
    """

    forecast_revenue = float(forecast_revenue or 0)
    committed_backlog = float(committed_backlog or 0)
    weighted_pipeline = float(weighted_pipeline or 0)
    budget_revenue = float(budget_revenue or 0)
    risk_adjustment = float(risk_adjustment or 0)

    # --------------------------------------------------
    # FORWARD REVENUE
    # --------------------------------------------------

    forward_revenue = (
        committed_backlog
        + weighted_pipeline
    )

    # --------------------------------------------------
    # COMMITTED FORECAST COVERAGE
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
    # --------------------------------------------------

    if forward_revenue > 0:
        pipeline_dependency = (
            weighted_pipeline
            / forward_revenue
        ) * 100
    else:
        pipeline_dependency = 0.0

    # --------------------------------------------------
    # FORECAST HEADROOM
    # --------------------------------------------------

    forecast_headroom = (
        forecast_revenue
        - budget_revenue
    )

    if budget_revenue > 0:
        forecast_headroom_pct = (
            forecast_headroom
            / budget_revenue
        ) * 100
    else:
        forecast_headroom_pct = 0.0

    # --------------------------------------------------
    # RISK ADJUSTMENT RATE
    # --------------------------------------------------

    if forecast_revenue > 0:
        risk_adjustment_pct = (
            risk_adjustment
            / forecast_revenue
        ) * 100
    else:
        risk_adjustment_pct = 0.0

    # --------------------------------------------------
    # FORECAST RISK
    #
    # Based primarily on committed coverage.
    #
    # >= 70%  LOW
    # >= 50%  MEDIUM
    # < 50%   HIGH
    # --------------------------------------------------

    if committed_forecast_coverage >= 70:
        forecast_risk = "low"
    elif committed_forecast_coverage >= 50:
        forecast_risk = "medium"
    else:
        forecast_risk = "high"

    # --------------------------------------------------
    # PIPELINE RISK
    #
    # Based on dependency on weighted pipeline.
    #
    # <= 35%  LOW
    # <= 50%  MEDIUM
    # > 50%   HIGH
    # --------------------------------------------------

    if pipeline_dependency <= 35:
        pipeline_risk = "low"
    elif pipeline_dependency <= 50:
        pipeline_risk = "medium"
    else:
        pipeline_risk = "high"

    # --------------------------------------------------
    # HEADROOM STATUS
    # --------------------------------------------------

    if forecast_headroom_pct >= 15:
        headroom_status = "strong"
    elif forecast_headroom_pct >= 5:
        headroom_status = "moderate"
    elif forecast_headroom_pct >= 0:
        headroom_status = "thin"
    else:
        headroom_status = "negative"

    # --------------------------------------------------
    # OVERALL RISK
    # --------------------------------------------------

    risk_levels = {
        "low": 1,
        "medium": 2,
        "high": 3,
    }

    max_risk = max(
        risk_levels.get(
            forecast_risk,
            2,
        ),
        risk_levels.get(
            pipeline_risk,
            2,
        ),
    )

    if max_risk >= 3:
        overall_risk = "high"
    elif max_risk == 2:
        overall_risk = "medium"
    else:
        overall_risk = "low"

    # --------------------------------------------------
    # RISK SCORE
    #
    # 0-33   low
    # 34-66  medium
    # 67-100 high
    #
    # Score is explainable rather than ML-generated.
    # --------------------------------------------------

    commitment_risk = max(
        0.0,
        min(
            100.0,
            100.0
            - committed_forecast_coverage,
        ),
    )

    pipeline_risk_score = max(
        0.0,
        min(
            100.0,
            pipeline_dependency,
        ),
    )

    execution_risk_score = max(
        0.0,
        min(
            100.0,
            risk_adjustment_pct * 5,
        ),
    )

    risk_score = (
        commitment_risk * 0.45
        + pipeline_risk_score * 0.35
        + execution_risk_score * 0.20
    )

    risk_score = max(
        0.0,
        min(
            100.0,
            risk_score,
        ),
    )

    if risk_score < 34:
        risk_score_status = "low"
    elif risk_score < 67:
        risk_score_status = "medium"
    else:
        risk_score_status = "high"

    return {
        "overall_risk": overall_risk,

        "forecast_risk": forecast_risk,

        "pipeline_risk": pipeline_risk,

        "risk_score": round(
            risk_score,
            2,
        ),

        "risk_score_status": risk_score_status,

        "committed_forecast_coverage": round(
            committed_forecast_coverage,
            2,
        ),

        "pipeline_dependency": round(
            pipeline_dependency,
            2,
        ),

        "forecast_headroom": round(
            forecast_headroom,
            2,
        ),

        "forecast_headroom_pct": round(
            forecast_headroom_pct,
            2,
        ),

        "risk_adjustment": round(
            risk_adjustment,
            2,
        ),

        "risk_adjustment_pct": round(
            risk_adjustment_pct,
            2,
        ),

        "headroom_status": headroom_status,
    }