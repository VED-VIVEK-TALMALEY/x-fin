from decimal import Decimal

from fastapi import APIRouter

from app.services.variance_engine import calculate_variance

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/variance/demo")
def demo_variance():

    result = calculate_variance(
        actual=Decimal("42000000"),
        budget=Decimal("45000000"),
        forecast=Decimal("42700000"),
    )

    return {
        "actual": float(result.actual),
        "budget": float(result.budget),
        "forecast": float(result.forecast),
        "actual_vs_budget": float(result.actual_vs_budget),
        "actual_vs_budget_pct": float(result.actual_vs_budget_pct),
        "forecast_vs_budget": float(result.forecast_vs_budget),
        "forecast_vs_budget_pct": float(result.forecast_vs_budget_pct),
    }