from fastapi import APIRouter
from pydantic import BaseModel

from app.services.scenario_engine import run_scenario


router = APIRouter(
    prefix="/scenarios",
    tags=["Scenarios"],
)


class ScenarioRequest(BaseModel):

    base_revenue: float
    pipeline_revenue: float
    utilization: float

    pipeline_conversion_change: float = 0.0
    utilization_change: float = 0.0
    billing_rate_change: float = 0.0
    slippage_rate: float = 0.0


@router.post("/run")
def run(request: ScenarioRequest):

    return run_scenario(
        base_revenue=request.base_revenue,
        pipeline_revenue=request.pipeline_revenue,
        utilization=request.utilization,
        pipeline_conversion_change=(
            request.pipeline_conversion_change
        ),
        utilization_change=(
            request.utilization_change
        ),
        billing_rate_change=(
            request.billing_rate_change
        ),
        slippage_rate=(
            request.slippage_rate
        ),
    )