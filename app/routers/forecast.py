from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.connection import get_db
from app.services.backlog_engine import calculate_backlog
from app.services.finance_queries import (
    get_pipeline_summary,
)
from app.services.forecast_engine import build_forecast

router = APIRouter(
    prefix="/forecast",
    tags=["Forecast"],
)


@router.get("/current")
def current_forecast(
    db: Session = Depends(get_db),
):

    backlog = calculate_backlog(db)

    pipeline = get_pipeline_summary(db)

    utilization = 0.74

    result = build_forecast(
        committed_backlog=backlog[
            "committed_backlog"
        ],
        weighted_pipeline=float(
            pipeline["weighted_pipeline"]
        ),
        utilization=utilization,
    )

    return {
        "forecast": result.__dict__,
        "pipeline": pipeline,
        "backlog": backlog,
    }