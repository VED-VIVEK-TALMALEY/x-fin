"""
Intelligence Router
-------------------

Canonical API surface for X-Fin intelligence.

The existing intelligence_engine remains responsible for constructing
the canonical intelligence object.

This router deliberately does not duplicate business logic.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.connection import get_db
from app.services.intelligence_engine import (
    build_intelligence_overview,
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
    """
    Canonical executive intelligence endpoint.

    Existing intelligence_engine remains the source of truth.
    """
    result = build_intelligence_overview(db)

    if result is None:
        return {
            "status": "ok",
            "reasoning": {},
            "risk": {},
            "forecast": {},
            "forecast_decomposition": {},
            "monte_carlo": {},
            "staffing": {},
            "insights": [],
            "recommendations": [],
            "data_quality": {},
            "source_metrics": {},
        }

    return result