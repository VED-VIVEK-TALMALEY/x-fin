from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.connection import get_db

from app.services.backlog_engine import (
    backlog_waterfall,
    calculate_backlog,
)

from app.services.finance_queries import (
    get_budget_summary,
    get_finance_summary,
    get_monthly_revenue,
    get_pipeline_summary,
)

from app.services.variance_engine import (
    calculate_variance,
)

from app.services.forecast_accuracy import (
    calculate_forecast_accuracy,
)

from app.services.business_unit_engine import (
    business_unit_performance,
)

from app.services.forecast_engine import (
    build_forecast,
)


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


# ---------------------------------------------------------
# FORECAST CONFIGURATION
# ---------------------------------------------------------
#
# Keep these aligned with /forecast/current.
#
# IMPORTANT:
# These are currently model assumptions.
# Eventually they should come from a shared configuration
# or assumptions service rather than being duplicated here.
#

TARGET_UTILIZATION = 0.75
CURRENT_UTILIZATION = 0.74
EXECUTION_RISK_RATE = 0.05


# ---------------------------------------------------------
# FORECAST ACCURACY
# ---------------------------------------------------------

@router.get("/forecast-accuracy")
def forecast_accuracy(
    db: Session = Depends(get_db),
):
    """
    Return historical actual-vs-budget performance.

    NOTE:
    Despite the legacy endpoint name, the underlying data
    currently measures actual revenue against budget revenue.

    It does NOT represent true forecast-vs-actual accuracy
    because historical forecast vintages are not currently
    being compared against realized outcomes.
    """

    return calculate_forecast_accuracy(db)


# ---------------------------------------------------------
# BUSINESS UNITS
# ---------------------------------------------------------

@router.get("/business-units")
def business_units(
    db: Session = Depends(get_db),
):
    """
    Return business-unit performance metrics.

    The business_unit_engine remains responsible for the
    underlying business-unit calculations.
    """

    return business_unit_performance(db)


# ---------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------

@router.get("/summary")
def summary(
    db: Session = Depends(get_db),
):
    """
    Return the core finance, budget and backlog summary.
    """

    finance = get_finance_summary(db)

    budget = get_budget_summary(db)

    backlog = calculate_backlog(db)

    return {
        "finance": finance,
        "budget": budget,
        "backlog": backlog,
    }


# ---------------------------------------------------------
# MONTHLY REVENUE
# ---------------------------------------------------------

@router.get("/monthly-revenue")
def monthly_revenue(
    db: Session = Depends(get_db),
):
    """
    Return historical monthly revenue, hours and cost.
    """

    return get_monthly_revenue(db)


# ---------------------------------------------------------
# BACKLOG
# ---------------------------------------------------------

@router.get("/backlog")
def backlog(
    db: Session = Depends(get_db),
):
    """
    Return backlog summary and waterfall.
    """

    return {
        "summary": calculate_backlog(db),
        "waterfall": backlog_waterfall(db),
    }


# ---------------------------------------------------------
# VARIANCE
# ---------------------------------------------------------

@router.get("/variance")
def variance(
    db: Session = Depends(get_db),
):
    """
    Compare actual and canonical deterministic forecast
    against budget.

    IMPORTANT:
    Forecast is calculated using the same forecast engine
    as /forecast/current.

    It is no longer set equal to actual revenue.
    """

    # -----------------------------------------------------
    # CORE FINANCE DATA
    # -----------------------------------------------------

    finance = get_finance_summary(db)

    budget = get_budget_summary(db)

    actual = float(
        finance.get(
            "actual_revenue",
            0.0,
        )
        or 0.0
    )

    budget_value = float(
        budget.get(
            "budget_revenue",
            0.0,
        )
        or 0.0
    )

    # -----------------------------------------------------
    # BACKLOG
    # -----------------------------------------------------

    backlog = calculate_backlog(db)

    committed_backlog = float(
        backlog.get(
            "committed_backlog",
            0.0,
        )
        or 0.0
    )

    # -----------------------------------------------------
    # PIPELINE
    # -----------------------------------------------------

    pipeline = get_pipeline_summary(db)

    weighted_pipeline = float(
        pipeline.get(
            "weighted_pipeline",
            0.0,
        )
        or 0.0
    )

    # -----------------------------------------------------
    # CANONICAL DETERMINISTIC FORECAST
    # -----------------------------------------------------

    forecast_result = build_forecast(
        committed_backlog=committed_backlog,
        weighted_pipeline=weighted_pipeline,
        utilization=CURRENT_UTILIZATION,
        target_utilization=TARGET_UTILIZATION,
        risk_rate=EXECUTION_RISK_RATE,
    )

    forecast = float(
        forecast_result.forecast_revenue
    )

    result = calculate_variance(
    actual=actual,
    budget=budget_value,
    forecast=forecast,
)

    return {
    **result.__dict__,
    "forecast_method": {
        "model": "deterministic_forecast_engine",
        "current_utilization": CURRENT_UTILIZATION,
        "target_utilization": TARGET_UTILIZATION,
        "execution_risk_rate": EXECUTION_RISK_RATE,
    },
}