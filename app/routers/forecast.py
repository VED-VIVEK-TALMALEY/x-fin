
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.connection import get_db

from app.services.backlog_engine import (
    calculate_backlog,
)

from app.services.finance_queries import (
    get_pipeline_summary,
)

from app.services.forecast_engine import (
    build_forecast,
)


router = APIRouter(
    prefix="/forecast",
    tags=["Forecast"],
)


# ---------------------------------------------------------
# FORECAST CONFIGURATION
# ---------------------------------------------------------
#
# These are currently explicit model assumptions.
#
# They should eventually move into a configuration/model
# layer or database-backed assumptions table.
#
TARGET_UTILIZATION = 0.75
CURRENT_UTILIZATION = 0.74
EXECUTION_RISK_RATE = 0.05


@router.get("/current")
def current_forecast(
    db: Session = Depends(get_db),
):
    """
    Return the current deterministic X-Fin forecast.

    Forecast model:

        Committed Backlog
        + Weighted Pipeline
        + Utilization Adjustment
        - Execution Risk Adjustment

    The forecast calculation itself lives in
    app.services.forecast_engine.
    """

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
    # FORECAST
    # -----------------------------------------------------

    result = build_forecast(
        committed_backlog=committed_backlog,
        weighted_pipeline=weighted_pipeline,
        utilization=CURRENT_UTILIZATION,
        target_utilization=TARGET_UTILIZATION,
        risk_rate=EXECUTION_RISK_RATE,
    )

    return {
        "forecast": result.__dict__,
        "pipeline": pipeline,
        "backlog": backlog,
        "assumptions": {
            "current_utilization": CURRENT_UTILIZATION,
            "target_utilization": TARGET_UTILIZATION,
            "execution_risk_rate": EXECUTION_RISK_RATE,
        },
    }