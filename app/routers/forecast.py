from decimal import Decimal

from fastapi import APIRouter

from app.services.forecast_engine import calculate_forecast

router = APIRouter(prefix="/forecast", tags=["Forecast"])


@router.get("/demo")
def demo_forecast():

    result = calculate_forecast(
        backlog_revenue=Decimal("28000000"),
        pipeline_revenue=Decimal("12000000"),
        utilization=Decimal("0.74"),
        target_utilization=Decimal("0.75"),
        risk_rate=Decimal("0.05"),
    )

    return {
        "backlog_revenue": float(result.backlog_revenue),
        "pipeline_revenue": float(result.pipeline_revenue),
        "capacity_adjustment": float(result.capacity_adjustment),
        "risk_adjustment": float(result.risk_adjustment),
        "total_forecast": float(result.total_forecast),
    }   