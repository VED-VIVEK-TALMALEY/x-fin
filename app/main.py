from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import scenarios
from app.routers import analytics, forecast, projects
from app.routers import (
    analytics,
    forecast,
    projects,
    scenarios,
)
app = FastAPI(
    title="X-Fin",
    description="Intelligent Delivery Finance Operating System",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projects.router)
app.include_router(forecast.router)
app.include_router(analytics.router)
app.include_router(scenarios.router)
@app.get("/")
def root():
    return {
        "name": "X-Fin",
        "description": "Intelligent Delivery Finance Operating System",
        "version": "1.0.0",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "x-fin",
    }