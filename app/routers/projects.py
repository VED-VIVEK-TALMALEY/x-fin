from fastapi import APIRouter

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("/health")
def projects_health():
    return {"status": "ok", "service": "projects"}