from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.connection import get_db

from app.services.finance_queries import (
    get_finance_summary,
    get_budget_summary,
    get_pipeline_summary,
)

from app.services.backlog_engine import (
    calculate_backlog,
)

from app.services.forecast_engine import (
    build_forecast,
)

from app.services.finance_reasoning import (
    explain_financial_position,
)

from app.services.insight_engine import (
    generate_insights,
)

from app.services.recommendation_engine import (
    generate_recommendations,
)


router = APIRouter(
    prefix="/intelligence",
    tags=["Intelligence"],
)


@router.get("/health")
def intelligence_health():
    return {
        "status": "ok",
        "service": "finance-intelligence",
    }


@router.get("/overview")
def intelligence_overview(
    db: Session = Depends(get_db),
):
    try:
        # -----------------------------------------
        # SOURCE DATA
        # -----------------------------------------

        finance = get_finance_summary(db)

        budget = get_budget_summary(db)

        pipeline = get_pipeline_summary(db)

        backlog = calculate_backlog(db)

        # -----------------------------------------
        # NORMALIZATION
        # -----------------------------------------

        actual_revenue = float(
            finance.get("actual_revenue", 0) or 0
        )

        budget_revenue = float(
            budget.get("budget_revenue", 0) or 0
        )

        budget_utilization = float(
            budget.get("budget_utilization", 0) or 0
        )

        pipeline_value = float(
            pipeline.get("pipeline_value", 0) or 0
        )

        weighted_pipeline = float(
            pipeline.get("weighted_pipeline", 0) or 0
        )

        committed_backlog = float(
            backlog.get("committed_backlog", 0) or 0
        )

        uncommitted_pipeline = float(
            backlog.get("uncommitted_pipeline", 0) or 0
        )

        # -----------------------------------------
        # FORECAST
        # -----------------------------------------

        forecast_result = build_forecast(
            committed_backlog=committed_backlog,
            weighted_pipeline=weighted_pipeline,
            utilization=budget_utilization,
            target_utilization=0.75,
            risk_rate=0.05,
        )

        forecast_revenue = float(
            forecast_result.forecast_revenue
        )

        # -----------------------------------------
        # REASONING
        # -----------------------------------------

        reasoning = explain_financial_position(
            actual_revenue=actual_revenue,
            budget_revenue=budget_revenue,
            forecast_revenue=forecast_revenue,
            committed_backlog=committed_backlog,
            weighted_pipeline=weighted_pipeline,
        )

        # -----------------------------------------
        # INSIGHTS
        # -----------------------------------------

        insights = generate_insights(
            reasoning
        )

        # -----------------------------------------
        # RECOMMENDATIONS
        # -----------------------------------------

        recommendations = generate_recommendations(
            reasoning=reasoning,
            insights=insights,
        )

        # -----------------------------------------
        # RESPONSE
        # -----------------------------------------

        return {
            "status": "healthy",

            "reasoning": reasoning,

            "insights": insights,

            "recommendations": recommendations,

            "source_metrics": {
                "actual_revenue": actual_revenue,
                "budget_revenue": budget_revenue,
                "budget_utilization": budget_utilization,
                "pipeline_value": pipeline_value,
                "weighted_pipeline": weighted_pipeline,
                "committed_backlog": committed_backlog,
                "uncommitted_pipeline": uncommitted_pipeline,
            },

            "forecast": {
                "committed_backlog": (
                    forecast_result.committed_backlog
                ),

                "weighted_pipeline": (
                    forecast_result.weighted_pipeline
                ),

                "utilization_adjustment": (
                    forecast_result.utilization_adjustment
                ),

                "risk_adjustment": (
                    forecast_result.risk_adjustment
                ),

                "forecast_revenue": (
                    forecast_result.forecast_revenue
                ),
            },
        }

    except Exception as exc:

        return {
            "status": "error",
            "error_type": type(exc).__name__,
            "error": str(exc),
        }