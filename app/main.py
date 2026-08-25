from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

from app.routers import (
    projects,
    forecast,
    analytics,
    scenarios,
    intelligence,
)


app = FastAPI(
    title="X-Fin Finance API",
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


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():
    return {
        "name": "X-Fin",
        "version": "1.0.0",
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