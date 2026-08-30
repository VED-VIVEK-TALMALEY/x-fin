from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

from app.config import APP_NAME, APP_VERSION
from app.routers import (
    analytics,
    executive,
    forecast,
    intelligence,
    projects,
    scenarios,
)


# ============================================================
# APPLICATION
# ============================================================

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="Intelligent Delivery Finance Operating System",
)


# ============================================================
# GLOBAL EXCEPTION HANDLER
# ============================================================

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception,
):
    import traceback

    traceback.print_exc()

    return PlainTextResponse(
        f"{type(exc).__name__}: {exc}",
        status_code=500,
    )


# ============================================================
# ROUTERS
# ============================================================

app.include_router(
    projects.router,
)

app.include_router(
    forecast.router,
)

app.include_router(
    analytics.router,
)

app.include_router(
    scenarios.router,
)

app.include_router(
    intelligence.router,
)

# IMPORTANT:
# Register the executive router.
app.include_router(
    executive.router,
)


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():
    return {
        "name": "X-Fin",
        "version": APP_VERSION,
        "description": (
            "Intelligent Delivery Finance "
            "Operating System"
        ),
        "status": "healthy",
    }


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "x-fin",
    }


# ============================================================
# DATABASE HEALTH
# ============================================================

@app.get("/health/db")
def database_health():
    from app.db.connection import test_connection

    if test_connection():
        return {
            "status": "healthy",
            "database": "connected",
        }

    return {
        "status": "unhealthy",
        "database": "unreachable",
    }