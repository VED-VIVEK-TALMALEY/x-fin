# X-Fin REST API Reference

> **Base URL:** `http://127.0.0.1:8000` · **Framework:** FastAPI 0.115+ · **Specification:** OpenAPI 3.1.0 / JSON

---

## API Route Architecture

```mermaid
graph LR
    API["FastAPI Gateway (:8000)"]

    subgraph Analytics["/analytics/*"]
        A1["GET /analytics/summary"]
        A2["GET /analytics/monthly-revenue"]
        A3["GET /analytics/backlog"]
        A4["GET /analytics/variance"]
        A5["GET /analytics/forecast-accuracy"]
        A6["GET /analytics/business-units"]
    end

    subgraph Forecast["/forecast/*"]
        F1["GET /forecast/current"]
    end

    subgraph Intelligence["/intelligence/*"]
        I1["GET /intelligence/health"]
        I2["GET /intelligence/overview"]
    end

    subgraph Executive["/executive/*"]
        E1["GET /executive/health"]
        E2["GET /executive/briefing"]
    end

    subgraph Decisions["/decisions/*"]
        D1["GET /decisions/overview"]
    end

    subgraph Scenarios["/scenarios/*"]
        S1["POST /scenarios/run"]
    end

    subgraph Projects["/projects"]
        P1["GET /projects"]
    end

    subgraph System["/"]
        SYS1["GET /"]
        SYS2["GET /health"]
        SYS3["GET /health/db"]
    end

    API --> Analytics & Forecast & Intelligence & Executive & Decisions & Scenarios & Projects & System

    style API fill:#1E293B,stroke:#0F172A,stroke-width:2px,color:#FFFFFF
    style Analytics fill:#EFF6FF,stroke:#2563EB,stroke-width:2px,color:#1E40AF
    style Forecast fill:#FAF5FF,stroke:#9333EA,stroke-width:2px,color:#6B21A8
    style Intelligence fill:#ECFDF5,stroke:#059669,stroke-width:2px,color:#065F46
    style Executive fill:#FDF4FF,stroke:#C026D3,stroke-width:2px,color:#86198F
    style Decisions fill:#FFFBEB,stroke:#D97706,stroke-width:2px,color:#92400E
    style Scenarios fill:#FEF2F2,stroke:#DC2626,stroke-width:2px,color:#991B1B
    style Projects fill:#F0FDF4,stroke:#16A34A,stroke-width:2px,color:#15803D
    style System fill:#F8FAFC,stroke:#475569,stroke-width:2px,color:#1E293B
```

---

## Canonical Intelligence Request & Response Sequence

```mermaid
sequenceDiagram
    autonumber
    actor Dashboard as Streamlit UI (dashboard/api.py)
    participant Gateway as FastAPI Router (/intelligence/overview)
    participant DB as PostgreSQL / SQLite Database
    participant EngFC as forecast_engine.py
    participant EngMC as monte_carlo_engine.py
    participant EngRS as finance_reasoning.py & risk_engine.py
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
