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

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)

@router.get("/forecast-accuracy")
def forecast_accuracy(
    db: Session = Depends(get_db),
):

    return calculate_forecast_accuracy(db)


@router.get("/business-units")
def business_units(
    db: Session = Depends(get_db),
):

    return business_unit_performance(db)
@router.get("/summary")
def summary(
    db: Session = Depends(get_db),
):

    finance = get_finance_summary(db)
    budget = get_budget_summary(db)
    backlog = calculate_backlog(db)

    return {
        "finance": finance,
        "budget": budget,
        "backlog": backlog,
    }


@router.get("/monthly-revenue")
def monthly_revenue(
    db: Session = Depends(get_db),
):

    return get_monthly_revenue(db)


@router.get("/backlog")
def backlog(
    db: Session = Depends(get_db),
):

    return {
        "summary": calculate_backlog(db),
        "waterfall": backlog_waterfall(db),
    }


@router.get("/variance")
def variance(
    db: Session = Depends(get_db),
):

    finance = get_finance_summary(db)
    budget = get_budget_summary(db)

    actual = float(
        finance["actual_revenue"]
    )

    budget_value = float(
        budget["budget_revenue"]
    )

    # Current forecast is intentionally based on
    # actual performance rather than an arbitrary
    # hard-coded multiplier.
    forecast = actual

    return calculate_variance(
        actual=actual,
        budget=budget_value,
        forecast=forecast,
    )