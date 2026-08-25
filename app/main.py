from fastapi import FastAPI

from app.routers import (
    projects,
    forecast,
    analytics,
    scenarios,
    intelligence,
)


app = FastAPI(
    title="X-Fin",
    version="1.0.0",
    description="Intelligent Delivery Finance Operating System",
)


# --------------------------------------------------
# ROUTERS
# --------------------------------------------------

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


# --------------------------------------------------
# ROOT
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "name": "X-Fin",
        "version": "1.0.0",
        "description": "Intelligent Delivery Finance Operating System",
        "status": "healthy",
    }


# --------------------------------------------------
# HEALTH
# --------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "x-fin",
    }