# X-Fin REST API Reference

> **Base URL:** `http://127.0.0.1:8000` · **Framework:** FastAPI 0.115+ · **Specification:** OpenAPI 3.1.0 / JSON

---

## API Route Architecture

```mermaid
flowchart TB
    API["<b>FastAPI Gateway (:8000)</b>"]

    subgraph CoreRoutes["Core Analytics & Forecast"]
        A1["/analytics/* (/summary, /monthly-revenue, /backlog, /variance, /forecast-accuracy, /business-units)"]
        F1["/forecast/current"]
    end

    subgraph DecisionRoutes["Intelligence & Decision Routes"]
        I1["/intelligence/* (/health, /overview)"]
        E1["/executive/* (/health, /briefing)"]
        D1["/decisions/overview"]
        S1["/scenarios/run"]
        P1["/projects"]
    end

    API --> CoreRoutes & DecisionRoutes

    style API fill:#1E293B,stroke:#0F172A,stroke-width:2px,color:#FFFFFF
    style CoreRoutes fill:#EFF6FF,stroke:#2563EB,stroke-width:2px,color:#1E40AF
    style DecisionRoutes fill:#FAF5FF,stroke:#9333EA,stroke-width:2px,color:#6B21A8
    style A1 fill:#DBEAFE,stroke:#1D4ED8,stroke-width:1px,color:#1E3A8A
    style F1 fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87
    style I1 fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87
    style E1 fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87
    style D1 fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87
    style S1 fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87
    style P1 fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87
```

---

## Canonical Intelligence Request & Response Sequence

```mermaid
sequenceDiagram
    autonumber
    actor Dashboard as Streamlit UI (dashboard/api.py)
    participant Gateway as FastAPI Router (/intelligence/overview)
    participant DB as Database (PostgreSQL / SQLite)
    participant EngFC as forecast_engine.py
    participant EngMC as monte_carlo_engine.py
    participant EngRS as finance_reasoning.py
    participant EngIN as insight_engine.py
    participant EngRC as recommendation_engine.py

    Dashboard->>Gateway: GET /intelligence/overview
    Gateway->>DB: Query actuals, budgets, pipeline snapshots, staffing hours
    DB-->>Gateway: Raw financial records
    Gateway->>EngFC: build_forecast(backlog, weighted_pipe, util, target=0.75, haircut=0.05)
    EngFC-->>Gateway: ForecastResult (forecast_revenue, utilization_adj, risk_adj)
    Gateway->>EngMC: run_monte_carlo_forecast(5000 iterations, seed=42)
    EngMC-->>Gateway: Stochastic quantiles (P10, P50, P90, VaR)
    Gateway->>EngRS: explain_financial_position() + calculate_forecast_risk()
    EngRS-->>Gateway: 20+ derived ratios & health classifications
    Gateway->>EngIN: generate_insights(reasoning, risk, monte_carlo, staffing)
    EngIN-->>Gateway: 9 scored diagnostic insights
    Gateway->>EngRC: generate_recommendations() + staffing actions
    EngRC-->>Gateway: Priority-sorted remediation playbooks (HIGH/MEDIUM/LOW)
    Gateway-->>Dashboard: 200 OK Complete Intelligence Package JSON
    Dashboard->>Dashboard: Render KPI Cards, Monte Carlo Plots, and Action Banners
```

---

## Complete API Route Catalog

| Method | Route Endpoint | Request Body | Response Schema | Description |
|:------:|:---------------|:-------------|:----------------|:------------|
| `GET` | `/` | None | `Dict[str, str]` | Application metadata, name, version, and status |
| `GET` | `/health` | None | `HealthStatus` | System health check probe |
| `GET` | `/health/db` | None | `Dict[str, str]` | Database connection health status |
| `GET` | `/forecast/current` | None | `ForecastResponse` | Current period deliverable forecast with backlog & pipeline split |
| `GET` | `/analytics/summary` | None | `FinanceSummary` | Aggregated recognized actuals, operating budgets, and backlog |
| `GET` | `/analytics/monthly-revenue` | None | `List[MonthlyRevenue]` | Monthly recognized delivery fees, hours, and direct costs |
| `GET` | `/analytics/backlog` | None | `BacklogResponse` | Committed vs uncommitted backlog and stage waterfall |
| `GET` | `/analytics/variance` | None | `VarianceResult` | Actual vs budget and forecast vs budget variance bridges |
| `GET` | `/analytics/forecast-accuracy`| None | `List[AccuracyItem]` | Historical month-by-month actual vs budget accuracy |
| `GET` | `/analytics/business-units` | None | `List[BUPerformance]` | BU-level revenue, gross margin, hours, and project count |
| `GET` | `/intelligence/health` | None | `HealthStatus` | Intelligence subsystem health status |
| `GET` | `/intelligence/overview` | None | `IntelligencePackage` | Full 360° financial intelligence bundle |
| `GET` | `/executive/health` | None | `Dict[str, str]` | Executive briefing subsystem health check |
| `GET` | `/executive/briefing` | None | `Dict[str, Any]` | High-level leadership decision briefing with critical actions |
| `GET` | `/decisions/overview` | None | `Dict[str, Any]` | Standardized decision triggers and recommendations |
| `POST` | `/scenarios/run` | `ScenarioRequest` | `ScenarioResult` | Multi-parameter what-if sensitivity simulation |
| `GET` | `/projects` | None | `List[Dict[str, Any]]` | Project directory with stage, contract value, and billing rate |

---

## Scenario Simulation Schema (`POST /scenarios/run`)

### Request JSON Payload

```json
{
  "base_revenue": 100000.0,
  "pipeline_revenue": 50000.0,
  "utilization": 0.74,
  "pipeline_conversion_change": 0.10,
  "utilization_change": 0.02,
  "billing_rate_change": 0.05,
  "slippage_rate": 0.03
}
```

### Response JSON Payload

```json
{
  "scenario_revenue": 147825.0,
  "revenue_change": 47825.0,
  "revenue_change_pct": 47.83,
  "parameters": {
    "pipeline_conversion_change": 0.10,
    "utilization_change": 0.02,
    "billing_rate_change": 0.05,
    "slippage_rate": 0.03
  }
}
```
