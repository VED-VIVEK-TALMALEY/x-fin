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
    # =========================================================
    # SOURCE DATA
    # =========================================================

    finance = get_finance_summary(db)

    budget = get_budget_summary(db)

    pipeline = get_pipeline_summary(db)

    backlog = calculate_backlog(db)

    # =========================================================
    # NORMALIZATION
    # =========================================================

    actual_revenue = float(
        finance.get(
            "actual_revenue",
            0,
        )
        or 0
    )

    budget_revenue = float(
        budget.get(
            "budget_revenue",
            0,
        )
        or 0
    )

    budget_utilization = float(
        budget.get(
            "budget_utilization",
            0,
        )
        or 0
    )

    pipeline_value = float(
        pipeline.get(
            "pipeline_value",
            0,
        )
        or 0
    )

    weighted_pipeline = float(
        pipeline.get(
            "weighted_pipeline",
            0,
        )
        or 0
    )

    committed_backlog = float(
        backlog.get(
            "committed_backlog",
            0,
        )
        or 0
    )

    uncommitted_pipeline = float(
        backlog.get(
            "uncommitted_pipeline",
            0,
        )
        or 0
    )

    # =========================================================
    # FORECAST
    # =========================================================

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

    # =========================================================
    # FORECAST DECOMPOSITION
    # =========================================================

    forecast_decomposition = {
        "committed_backlog": round(
            forecast_result.committed_backlog,
            2,
        ),
        "weighted_pipeline": round(
            forecast_result.weighted_pipeline,
            2,
        ),
        "utilization_adjustment": round(
            forecast_result.utilization_adjustment,
            2,
        ),
        "risk_adjustment": round(
            forecast_result.risk_adjustment,
            2,
        ),
        "forecast_revenue": round(
            forecast_result.forecast_revenue,
            2,
        ),
    }

    # =========================================================
    # REASONING
    # =========================================================

    reasoning = explain_financial_position(
        actual_revenue=actual_revenue,
        budget_revenue=budget_revenue,
        forecast_revenue=forecast_revenue,
        committed_backlog=committed_backlog,
        weighted_pipeline=weighted_pipeline,
    )

    # =========================================================
    # INSIGHTS
    # =========================================================

    insights = generate_insights(
        reasoning
    )

    # =========================================================
    # RECOMMENDATIONS
    # =========================================================

    recommendations = generate_recommendations(
        reasoning=reasoning,
        insights=insights,
    )

    # =========================================================
    # RESPONSE
    # =========================================================

    return {
        "status": "healthy",

        # -----------------------------------------------------
        # Financial reasoning
        # -----------------------------------------------------

        "reasoning": reasoning,

        # -----------------------------------------------------
        # Automated insights
        # -----------------------------------------------------

        "insights": insights,

        # -----------------------------------------------------
        # Prescriptive recommendations
        # -----------------------------------------------------

        "recommendations": recommendations,

        # -----------------------------------------------------
        # Raw source metrics
        # -----------------------------------------------------

        "source_metrics": {
            "actual_revenue": round(
                actual_revenue,
                2,
            ),
            "budget_revenue": round(
                budget_revenue,
                2,
            ),
            "budget_utilization": round(
                budget_utilization,
                6,
            ),
            "pipeline_value": round(
                pipeline_value,
                2,
            ),
            "weighted_pipeline": round(
                weighted_pipeline,
                2,
            ),
            "committed_backlog": round(
                committed_backlog,
                2,
            ),
            "uncommitted_pipeline": round(
                uncommitted_pipeline,
                2,
            ),
        },

        # -----------------------------------------------------
        # Forecast
        # -----------------------------------------------------

        "forecast": {
            "committed_backlog": round(
                forecast_result.committed_backlog,
                2,
            ),
            "weighted_pipeline": round(
                forecast_result.weighted_pipeline,
                2,
            ),
            "utilization_adjustment": round(
                forecast_result.utilization_adjustment,
                2,
            ),
            "risk_adjustment": round(
                forecast_result.risk_adjustment,
                2,
            ),
            "forecast_revenue": round(
                forecast_result.forecast_revenue,
                2,
            ),
        },

        # -----------------------------------------------------
        # Explicit forecast bridge
        # -----------------------------------------------------

        "forecast_decomposition": forecast_decomposition,
    }