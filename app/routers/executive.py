"""
Executive API Router
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.connection import get_db
from app.services.intelligence_engine import (
    build_intelligence_overview,
)
from app.services.executive_briefing_engine import (
    build_executive_briefing,
)


router = APIRouter(
    prefix="/executive",
    tags=["Executive"],
)


@router.get("/health")
def executive_health():
    return {
        "status": "ok",
        "service": "executive-intelligence",
    }


@router.get("/briefing")
def executive_briefing(
    db: Session = Depends(get_db),
):
    intelligence = build_intelligence_overview(db)

    briefing = build_executive_briefing(
        intelligence
    )

    return {
        "status": "ok",
        "briefing": briefing,
    }