from fastapi import APIRouter

from app.services.decision_engine import generate_decisions

router = APIRouter(
    prefix="/decisions",
    tags=["decisions"],
)


@router.get("/overview")
def decisions_overview():
    return generate_decisions(
        forecast_risk="low",
        confidence_band="moderate",
        pipeline_dependency=25.0,
        forecast_headroom_pct=8.0,
        variance_pct=2.0,
        staffing_gap=0.0,
    )