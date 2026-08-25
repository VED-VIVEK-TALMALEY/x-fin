# X-Fin — Architecture Overview

> **Version 1.0.0** · Last updated: August 2026

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER                           │
│                                                                     │
│   ┌─────────────────────┐        ┌────────────────────────────┐    │
│   │   dashboard/app.py  │        │  dashboard/intelligence.py  │    │
│   │   (Main Dashboard)  │        │  (Intelligence Deep-Dive)   │    │
│   └──────────┬──────────┘        └──────────────┬─────────────┘    │
│              │  HTTP (requests)                  │                  │
└──────────────┼───────────────────────────────────┼──────────────────┘
               │                                   │
               ▼                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                          API LAYER  (FastAPI)                       │
│                        http://127.0.0.1:8000                        │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │
│  │  /forecast/* │  │ /analytics/* │  │    /intelligence/*        │  │
│  └──────┬───────┘  └──────┬───────┘  └────────────┬─────────────┘  │
│         │                 │                        │                │
│  ┌──────┴─────────────────┴────────────────────────┴─────────────┐  │
│  │                    /scenarios/*    /projects/*                 │  │
│  └──────────────────────────────────────────────────────────────-┘  │
└─────────────────────────────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       SERVICE LAYER (Python)                        │
│                                                                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────────┐    │
│  │ forecast_engine │  │  backlog_engine  │  │ variance_engine  │    │
│  └─────────────────┘  └─────────────────┘  └──────────────────┘    │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────────┐    │
│  │finance_reasoning│  │ insight_engine  │  │recommendation_eng│    │
│  └─────────────────┘  └─────────────────┘  └──────────────────┘    │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────────┐    │
│  │ scenario_engine │  │  business_unit  │  │forecast_accuracy │    │
│  └─────────────────┘  └─────────────────┘  └──────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      DATA LAYER (PostgreSQL)                        │
│                                                                     │
│  ┌────────────────┐  ┌───────────────────┐  ┌──────────────────┐   │
│  │ business_units │  │    projects        │  │ project_pipeline │   │
│  └────────────────┘  └───────────────────┘  └──────────────────┘   │
│  ┌────────────────┐  ┌───────────────────┐  ┌──────────────────┐   │
│  │project_actuals │  │    budgets         │  │forecast_versions │   │
│  └────────────────┘  └───────────────────┘  └──────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Component Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Presentation | Streamlit + Plotly | Executive dashboards, KPI cards, charts |
| API | FastAPI + Uvicorn | REST endpoints, request routing, error handling |
| Services | Pure Python | Business logic, financial calculations, rule engines |
| Data | PostgreSQL + SQLAlchemy | Persistence, querying, aggregation |

---

## Data Flow — Intelligence Pipeline

```
PostgreSQL
    │
    ├─ finance_queries.py ──────► actual_revenue, actual_cost, contract_value
    ├─ finance_queries.py ──────► budget_revenue, budget_hours, budget_utilization
    ├─ finance_queries.py ──────► pipeline_value, weighted_pipeline
    └─ backlog_engine.py  ──────► committed_backlog, uncommitted_pipeline
                                         │
                                         ▼
                              forecast_engine.py
                              ─────────────────
                              Inputs:
                                committed_backlog
                                weighted_pipeline
                                budget_utilization
                              Adjustments:
                                utilization_adjustment
                                risk_adjustment (5%)
                              Output:
                                forecast_revenue
                                         │
                                         ▼
                             finance_reasoning.py
                             ──────────────────────
                             Computes 15+ derived metrics:
                               budget_gap, budget_gap_pct
                               forecast_gap, forecast_gap_pct
                               forward_coverage
                               committed_forecast_coverage
                               pipeline_dependency
                               committed_revenue_mix
                               forecast_risk (low/moderate/high)
                               pipeline_risk (low/moderate/high)
                               forward_position (strong/adequate/watch/weak)
                                         │
                                         ▼
                              insight_engine.py
                              ─────────────────
                              9 insight categories:
                                Revenue Performance
                                Forecast Position
                                Forward Coverage
                                Forecast Commitment
                                Pipeline Dependency
                                Committed Revenue Mix
                                Forecast Risk
                                Forward Position
                                Forecast Headroom
                              Severity: HIGH / MEDIUM / LOW
                                         │
                                         ▼
                          recommendation_engine.py
                          ─────────────────────────
                          10 recommendation rules:
                            Priority-sorted output
                            Financial impact quantified
                                         │
                                         ▼
                            /intelligence/overview
                              (REST response)
                                         │
                                         ▼
                           Streamlit Dashboard
```

---

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Deterministic rules only — no ML | Auditability and explainability are critical in consulting finance |
| `committed_forecast_coverage` is not statistical confidence | Named accurately: measures backlog support, not probability |
| Snapshot-based backlog | Period-specific schedules unavailable; avoids manufacturing false data |
| Risk rate hard-coded at 5% | Starting calibration; intended to be configurable per environment |
| INR (₹) currency notation | System currently calibrated for Indian consulting context |
| Utilization from budget data | Budget utilization (avg across BUs) used as the forecast input signal |

---

## Deployment Topology

```
┌──────────────────────────────────────────────────┐
│  Local / Single-Server Deployment                 │
│                                                   │
│  ┌──────────────┐   ┌────────────────────────┐   │
│  │ PostgreSQL   │   │  uvicorn (port 8000)    │   │
│  │ :5432        │   │  FastAPI app            │   │
│  └──────────────┘   └────────────────────────┘   │
│                                                   │
│  ┌────────────────────────────────────────────┐   │
│  │  streamlit run app.py (port 8501)           │   │
│  │  dashboard/app.py → calls :8000             │   │
│  └────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────┘
```
