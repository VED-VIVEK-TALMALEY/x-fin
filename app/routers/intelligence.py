from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.connection import get_db
from app.services.intelligence_engine import build_intelligence_overview


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
    return build_intelligence_overview(db)
