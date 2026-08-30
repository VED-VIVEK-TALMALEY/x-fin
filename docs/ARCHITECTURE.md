# X-Fin Architecture Overview

> **Version:** 1.0.0 · **Target Environment:** Python 3.10+ / FastAPI / PostgreSQL 14+ (with SQLite Fallback) / Streamlit

---

## Architectural Topology

```mermaid
flowchart TB
    subgraph Client["CLIENT TIER"]
        BROWSER["Web Browser / Leadership User (Port 8501)"]
    end

    subgraph PresentationTier["PRESENTATION TIER (Streamlit :8501)"]
        direction TB
        UI_MAIN["<b>dashboard/app.py</b><br/>• Performance Overview<br/>• Waterfall & Monte Carlo Charts<br/>• Scenario Sensitivity Planners"]
        UI_INTEL["<b>dashboard/intelligence.py</b><br/>• 9 Diagnostic Insight Cards<br/>• 10 Action Recommendation Cards"]
        UI_API["<b>dashboard/api.py</b><br/>HTTP REST Client with 10s Timeout & Resilience"]
        UI_MAIN & UI_INTEL --> UI_API
    end

    subgraph APITier["API GATEWAY (FastAPI :8000)"]
        direction TB
        MAIN["<b>app/main.py</b> (ASGI Application)"]
        R_ALL["<b>APIRouters:</b><br/>/forecast/current · /analytics/* · /intelligence/*<br/>/executive/* · /decisions/* · /scenarios/run"]
        MAIN --> R_ALL
    end

    subgraph ServiceTier["CALCULATION ENGINES (app/services)"]
        direction TB
        S_CORE["<b>Core Engines:</b><br/>• forecast_engine.py (5-Step Deterministic Model)<br/>• monte_carlo_engine.py (5,000 Iteration Simulator)<br/>• variance_engine.py & backlog_engine.py"]
        S_INTEL["<b>Intelligence & Reasoning:</b><br/>• finance_reasoning.py (20+ Ratios)<br/>• insight_engine.py (9 Diagnostic Rules)<br/>• recommendation_engine.py (10 Action Triggers)"]
    end

    subgraph DataTier["PERSISTENCE (PostgreSQL 14+ / SQLite)"]
        DB_CONN[("<b>Relational Schema</b><br/>business_units, projects, project_pipeline,<br/>project_actuals, budgets, forecast_versions")]
    end

    BROWSER --> PresentationTier
    UI_API -->|HTTP REST JSON| APITier
    APITier --> ServiceTier
    ServiceTier --> DataTier

    style Client fill:#F1F5F9,stroke:#475569,stroke-width:2px,color:#0F172A
    style PresentationTier fill:#EFF6FF,stroke:#2563EB,stroke-width:2px,color:#1E40AF
    style APITier fill:#F0FDF4,stroke:#16A34A,stroke-width:2px,color:#15803D
    style ServiceTier fill:#FAF5FF,stroke:#9333EA,stroke-width:2px,color:#6B21A8
    style DataTier fill:#F8FAFC,stroke:#334155,stroke-width:2px,color:#1E293B

    style BROWSER fill:#E2E8F0,stroke:#475569,stroke-width:1px,color:#0F172A
    style UI_MAIN fill:#DBEAFE,stroke:#1D4ED8,stroke-width:1px,color:#1E3A8A
    style UI_INTEL fill:#DBEAFE,stroke:#1D4ED8,stroke-width:1px,color:#1E3A8A
    style UI_API fill:#BFDBFE,stroke:#1D4ED8,stroke-width:1px,color:#1E3A8A
    style MAIN fill:#DCFCE7,stroke:#15803D,stroke-width:1px,color:#166534
    style R_ALL fill:#BBF7D0,stroke:#15803D,stroke-width:1px,color:#166534
    style S_CORE fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87
    style S_INTEL fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87
    style DB_CONN fill:#E2E8F0,stroke:#334155,stroke-width:1px,color:#1E293B
```

---

## Canonical Intelligence Data Flow Pipeline

```mermaid
flowchart TD
    subgraph Ingestion["1. DATABASE QUERY INGESTION"]
        DB[(PostgreSQL / SQLite)]
        Q_ALL["<b>finance_queries & backlog_engine</b><br/>Fetch actuals, budgets, pipeline snapshots, and staffing hours"]
        DB --> Q_ALL
    end

    subgraph Processing["2. FORECAST & STOCHASTIC ENGINES"]
        direction TB
        F1["<b>forecast_engine.py</b>: 5-step deterministic forecast calculation"]
        MC1["<b>monte_carlo_engine.py</b>: 5,000 iterations for P10, P50, P90, and VaR"]
        Q_ALL --> F1 & MC1
    end

    subgraph Reasoning["3. REASONING & DIAGNOSTICS"]
        direction TB
        R1["<b>finance_reasoning.py</b>: 20+ derived ratios & health classifications"]
        I1["<b>insight_engine.py</b>: 9 severity diagnostic rules"]
        REC1["<b>recommendation_engine.py</b>: 10 prioritized remediation playbooks"]
        F1 & MC1 --> R1 --> I1 --> REC1
    end

    subgraph DeliveryStage["4. API DISPATCH & UI"]
        EP["<b>GET /intelligence/overview & /executive/briefing</b><br/>Streamlit UI renders executive banners, charts & playbooks"]
        REC1 --> EP
    end

    Ingestion --> Processing --> Reasoning --> DeliveryStage

    style Ingestion fill:#F8FAFC,stroke:#475569,stroke-width:2px,color:#1E293B
    style Processing fill:#EFF6FF,stroke:#2563EB,stroke-width:2px,color:#1E40AF
    style Reasoning fill:#FAF5FF,stroke:#9333EA,stroke-width:2px,color:#6B21A8
    style DeliveryStage fill:#ECFDF5,stroke:#059669,stroke-width:2px,color:#065F46
```

---

## Architectural Component Responsibilities

| Layer | Component Module | Primary Functionality | Dependencies | Output Interface |
|:------|:-----------------|:----------------------|:-------------|:-----------------|
| **Presentation** | `dashboard/app.py` | Multi-tab executive decision dashboard | `streamlit`, `plotly`, `api.py` | Browser UI (:8501) |
| **Presentation** | `dashboard/intelligence.py` | Scored insight cards & action trigger lists | `streamlit`, `components.py` | Browser UI Subview |
| **Presentation** | `dashboard/charts.py` | Themed Plotly chart factory functions | `plotly.graph_objects`, `plotly.express` | Plotly Figure objects |
| **Presentation** | `dashboard/api.py` | Resilient REST client with retry/error handling | `requests` | Python dictionaries |
| **API Gateway** | `app/main.py` | FastAPI application initialization & middleware | `fastapi`, `uvicorn` | ASGI HTTP Server (:8000) |
| **API Gateway** | `app/routers/*` | Endpoint routing, dependency injection, auth | `fastapi.APIRouter`, `get_db` | JSON REST responses |
| **Service Engine**| `forecast_engine.py` | Deterministic 5-step deliverable forecast | Pure Python / `dataclasses` | `ForecastResult` |
| **Service Engine**| `monte_carlo_engine.py`| 5,000-iteration stochastic simulation | `random`, `math` | Distribution & VaR quantiles |
| **Service Engine**| `finance_reasoning.py`| 20+ derived practice ratios & classifications | Pure Python | Ratios dictionary |
| **Service Engine**| `insight_engine.py` | 9 diagnostic severity evaluators | `finance_reasoning` | Scored insights array |
| **Service Engine**| `recommendation_engine.py`| 10 prioritized remediation playbooks | `insight_engine`, `finance_reasoning` | Action recommendations |
| **Service Engine**| `staffing_engine.py` | Hours budget vs actuals & data quality flag | `SQLAlchemy` | Staffing position dict |
| **Persistence** | `app/db/connection.py`| Connection pooling with SQLite fallback | `SQLAlchemy` | `Session` generator |

---

## Architectural Decision Records (ADRs)

| # | Architecture Decision | Chosen Implementation | Technical & Business Rationale | Trade-offs & Alternatives |
|:--:|:----------------------|:----------------------|:-------------------------------|:--------------------------|
| **ADR-001** | **Deterministic Baseline** | 5-Step Rule Formulation | Consulting leadership requires 100% auditable mathematics with transparent haircut rules. | Black-box ML models (ARIMA/Prophet) were rejected due to lack of explainability. |
| **ADR-002** | **Stochastic Complement** | Monte Carlo (5,000 runs) | Provides empirical confidence intervals (P10/P50/P90) and VaR without obfuscating deterministic baseline. | Static sensitivity scenarios alone fail to capture multi-variable co-variance. |
| **ADR-003** | **Data Persistence** | Dual PostgreSQL / SQLite | Enables zero-config local evaluation out-of-the-box while maintaining production PostgreSQL compatibility. | Pure PostgreSQL requires local server daemon installation. |
| **ADR-004** | **Query Strategy** | Raw SQL via SQLAlchemy `text()` | Complex multi-table joins and window aggregations execute with zero ORM overhead. | Full ORM querysets introduce query generation latency. |
| **ADR-005** | **Decoupled Architecture** | Pure Python Services | Logic in `app/services` has zero coupling to HTTP frameworks, enabling fast pytest unit execution. | Embedding calculations directly in router handlers creates tightly coupled code. |

---

## Deployment & Production Topology

```mermaid
flowchart LR
    subgraph DeploymentNode["Host / Render Deployment Node"]
        direction TB
        ST_APP["<b>Streamlit Dashboard (:8501)</b><br/>streamlit run dashboard/app.py"]
        UV["<b>FastAPI ASGI Service (:8000)</b><br/>uvicorn app.main:app --port 8000"]
        PG["<b>PostgreSQL 14+ / SQLite</b><br/>Database Persistence"]
        ST_APP -->|Internal REST Calls| UV -->|Connection Pool| PG
    end

    User(["Practice Leader / Partner"]) -->|HTTPS Web Traffic| ST_APP

    style DeploymentNode fill:#F8FAFC,stroke:#334155,stroke-width:2px,color:#0F172A
    style User fill:#FEF3CD,stroke:#D97706,stroke-width:2px,color:#92400E
    style ST_APP fill:#DBEAFE,stroke:#1D4ED8,stroke-width:1px,color:#1E3A8A
    style UV fill:#DCFCE7,stroke:#15803D,stroke-width:1px,color:#166534
    style PG fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87
```
