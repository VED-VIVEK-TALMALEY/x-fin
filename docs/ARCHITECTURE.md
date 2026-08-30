# X-Fin Architecture Overview

> **Version:** 1.0.0 · **Target Environment:** Python 3.10+ / FastAPI / PostgreSQL 14+ (with SQLite Fallback) / Streamlit

---

## Architectural Topology

```mermaid
graph TB
    subgraph Client["CLIENT TIER"]
        BROWSER["Web Browser / Leadership User (Port 8501)"]
    end

    subgraph PresentationTier["PRESENTATION TIER (Streamlit :8501)"]
        UI_MAIN["<b>dashboard/app.py</b><br/>• Executive Performance Overview<br/>• Forecast Waterfall & Monte Carlo Distribution<br/>• Risk Driver & Staffing Capacity Charts<br/>• BU Performance Heatmap & Historical Accuracy<br/>• What-If Sensitivity Simulator"]
        UI_INTEL["<b>dashboard/intelligence.py</b><br/>• Financial Status Banner<br/>• Revenue Outlook Comparison Bar<br/>• Forward Revenue Split Bar<br/>• 5-Component Forecast Construction Table<br/>• 9 Diagnostic Insight Cards<br/>• 10 Action Recommendation Cards"]
        UI_CHARTS["<b>dashboard/charts.py</b><br/>Themed Plotly Chart Factory (Waterfall, Density, Heatmap, Gauges)"]
        UI_COMP["<b>dashboard/components.py</b><br/>UI Formatters, Cards, Badges, Alert Containers"]
        UI_API["<b>dashboard/api.py</b><br/>HTTP REST Client with 10s Timeout & Resilience Handling"]

        UI_MAIN & UI_INTEL --> UI_CHARTS
        UI_MAIN & UI_INTEL --> UI_COMP
        UI_MAIN & UI_INTEL --> UI_API
    end

    subgraph APITier["API GATEWAY TIER (FastAPI :8000)"]
        MAIN["<b>app/main.py</b><br/>FastAPI Application Factory, Global Error Handler & CORS"]
        subgraph Routers["FastAPI APIRouters"]
            R_FORECAST["<b>routers/forecast.py</b><br/>GET /forecast/current"]
            R_ANALYTICS["<b>routers/analytics.py</b><br/>GET /analytics/summary<br/>GET /analytics/monthly-revenue<br/>GET /analytics/backlog<br/>GET /analytics/variance<br/>GET /analytics/forecast-accuracy<br/>GET /analytics/business-units"]
            R_INTEL["<b>routers/intelligence.py</b><br/>GET /intelligence/health<br/>GET /intelligence/overview"]
            R_EXEC["<b>routers/executive.py</b><br/>GET /executive/health<br/>GET /executive/briefing"]
            R_DEC["<b>routers/decisions.py</b><br/>GET /decisions/overview"]
            R_SCENARIOS["<b>routers/scenarios.py</b><br/>POST /scenarios/run"]
            R_PROJECTS["<b>routers/projects.py</b><br/>GET /projects"]
        end
        MAIN --> Routers
    end

    subgraph ServiceTier["SERVICE & BUSINESS LOGIC TIER (app/services)"]
        S_FC["<b>forecast_engine.py</b><br/>Deterministic 5-step forecast calculation"]
        S_DEC["<b>forecast_decomposition.py</b><br/>Forecast bridge decomposition"]
        S_MC["<b>monte_carlo_engine.py</b><br/>5,000-iteration stochastic simulation & VaR"]
        S_BL["<b>backlog_engine.py</b><br/>Committed vs. uncommitted backlog waterfall"]
        S_VR["<b>variance_engine.py</b><br/>Multi-factor budget variance bridge"]
        S_RS["<b>finance_reasoning.py</b><br/>20+ derived practice ratios & health status"]
        S_IN["<b>insight_engine.py</b><br/>9 diagnostic severity evaluators"]
        S_RC["<b>recommendation_engine.py</b><br/>10 prioritized operational remediation rules"]
        S_STF["<b>staffing_engine.py</b><br/>Staffing capacity & utilization validator"]
        S_STI["<b>staffing_insight_engine.py</b><br/>Staffing insights & quality guardrails"]
        S_STR["<b>staffing_recommendation_engine.py</b><br/>Staffing data quality recommendations"]
        S_RSK["<b>risk_engine.py & margin_risk_engine.py</b><br/>Forecast headroom & margin risk"]
        S_EXB["<b>executive_briefing_engine.py</b><br/>Synthesized executive briefing builder"]
        S_BU["<b>business_unit_engine.py</b><br/>Practice-level BU aggregations"]
        S_SC["<b>scenario_engine.py</b><br/>Multi-parameter sensitivity simulator"]
        S_FQ["<b>finance_queries.py</b><br/>Optimized raw SQL queries"]
    end

    subgraph DataTier["DATA PERSISTENCE TIER (PostgreSQL 14+ / SQLite Fallback)"]
        DB_CONN["<b>app/db/connection.py</b><br/>SQLAlchemy create_engine() with SQLite fallback & session pooling"]
        subgraph Tables["Relational Schema (app/db/schema.sql)"]
            T_BU[("business_units")]
            T_PR[("projects")]
            T_PL[("project_pipeline")]
            T_AC[("project_actuals")]
            T_BG[("budgets")]
            T_FV[("forecast_versions")]
            T_VL[("forecast_values")]
        end
        DB_CONN --> Tables
    end

    BROWSER --> PresentationTier
    UI_API -->|HTTP REST JSON| APITier
    Routers --> ServiceTier
    ServiceTier --> DB_CONN

    style Client fill:#F1F5F9,stroke:#475569,stroke-width:2px,color:#0F172A
    style PresentationTier fill:#EFF6FF,stroke:#2563EB,stroke-width:2px,color:#1E40AF
    style APITier fill:#F0FDF4,stroke:#16A34A,stroke-width:2px,color:#15803D
    style ServiceTier fill:#FAF5FF,stroke:#9333EA,stroke-width:2px,color:#6B21A8
    style DataTier fill:#F8FAFC,stroke:#334155,stroke-width:2px,color:#1E293B

    style BROWSER fill:#E2E8F0,stroke:#475569,stroke-width:1px,color:#0F172A

    style UI_MAIN fill:#DBEAFE,stroke:#1D4ED8,stroke-width:1px,color:#1E3A8A
    style UI_INTEL fill:#DBEAFE,stroke:#1D4ED8,stroke-width:1px,color:#1E3A8A
    style UI_CHARTS fill:#BFDBFE,stroke:#1D4ED8,stroke-width:1px,color:#1E3A8A
    style UI_COMP fill:#BFDBFE,stroke:#1D4ED8,stroke-width:1px,color:#1E3A8A
    style UI_API fill:#93C5FD,stroke:#1D4ED8,stroke-width:1px,color:#1E3A8A

    style MAIN fill:#DCFCE7,stroke:#15803D,stroke-width:1px,color:#166534
    style Routers fill:#BBF7D0,stroke:#15803D,stroke-width:1px,color:#166534

    style S_FC fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87
    style S_DEC fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87
    style S_MC fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87
    style S_BL fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87
    style S_VR fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87
    style S_RS fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87
    style S_IN fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87
    style S_RC fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87
    style S_STF fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87
    style S_STI fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87
    style S_STR fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87
    style S_RSK fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87
    style S_EXB fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87
    style S_BU fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87
    style S_SC fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87
    style S_FQ fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87

    style DB_CONN fill:#E2E8F0,stroke:#334155,stroke-width:1px,color:#0F172A
    style Tables fill:#CBD5E1,stroke:#334155,stroke-width:1px,color:#0F172A
```

---

## Canonical Intelligence Data Flow Pipeline

```mermaid
flowchart TD
    subgraph Ingestion["1. DATABASE QUERY INGESTION"]
        DB[(PostgreSQL / SQLite)]
        Q1["<b>finance_queries.get_finance_summary(db)</b><br/>SUM(actual_revenue), SUM(actual_cost), SUM(contract_value)"]
        Q2["<b>finance_queries.get_budget_summary(db)</b><br/>SUM(revenue_budget), AVG(utilization_budget)"]
        Q3["<b>finance_queries.get_pipeline_summary(db)</b><br/>COUNT(*), SUM(pipeline_value), SUM(pipeline_value * probability)"]
        Q4["<b>backlog_engine.calculate_backlog(db)</b><br/>Committed Backlog vs Uncommitted Pipeline Split"]
        Q5["<b>staffing_engine.calculate_staffing_position(db)</b><br/>Actual Delivered Hours vs Capacity Hours Budget"]

        DB --> Q1 & Q2 & Q3 & Q4 & Q5
    end

    subgraph Deterministic["2. DETERMINISTIC ENGINE (forecast_engine.py)"]
        F1["<b>forecast_engine.build_forecast()</b><br/>• Utilization Factor = actual_utilization / 0.75<br/>• Utilization Adjustment = committed_backlog * (Factor - 1.0)<br/>• Gross Forecast = committed + weighted + Util_Adj<br/>• Risk Haircut = Gross * 0.05<br/>• Net Forecast = Gross - Risk Haircut"]
        Q2 & Q3 & Q4 --> F1
        F1 --> F_OUT["<b>ForecastResult Dataclass</b><br/>forecast_revenue: round(net, 2)"]
    end

    subgraph Stochastic["3. STOCHASTIC SIMULATION (monte_carlo_engine.py)"]
        MC1["<b>monte_carlo_engine.run_monte_carlo_forecast()</b><br/>• 5,000 Iterations (Seed = 42)<br/>• Beta Pipeline Conversions<br/>• Normal Utilization Volatility<br/>• P10 (Downside), P50 (Median), P90 (Upside)<br/>• Value-at-Risk (VaR)"]
        Q1 & Q2 & Q4 & F_OUT --> MC1
        MC1 --> MC_OUT["<b>Monte Carlo Output Bundle</b>"]
    end

    subgraph ReasoningStage["4. FINANCE REASONING (finance_reasoning.py & risk_engine.py)"]
        R1["<b>finance_reasoning.explain_financial_position()</b><br/>• Budget Gap & Gap %<br/>• Forecast Gap & Headroom %<br/>• Forward Revenue & Forward Coverage %<br/>• Committed Forecast Coverage %<br/>• Pipeline Dependency %<br/>• Risk Classifications ('low', 'moderate', 'high')"]
        Q1 & Q2 & F_OUT & Q4 & Q3 --> R1
        R1 --> R_OUT["<b>Reasoning Metrics Dictionary</b>"]
    end

    subgraph Diagnostics["5. DIAGNOSTICS & ACTIONS (insight_engine.py & recommendation_engine.py)"]
        I1["<b>insight_engine.generate_insights()</b><br/>Evaluates 9 Deterministic Severity Rules across Performance, Coverage, Quality, and Risk"]
        REC1["<b>recommendation_engine.generate_recommendations()</b><br/>Evaluates 10 Decision Action Rules with Quantified INR Financial Impact"]
        STF_REC["<b>staffing engines</b><br/>staffing_insight_engine & staffing_recommendation_engine"]
        
        R_OUT & MC_OUT --> I1 --> REC1
        Q5 --> STF_REC --> REC1
        REC1 --> REC_OUT["<b>Priority-Sorted Remediation Playbook</b>"]
    end

    subgraph DeliveryStage["6. DISPATCH & PRESENTATION"]
        INTEL_PKG["<b>Canonical Intelligence Package</b><br/>Consolidated Overview Object"]
        R_OUT & MC_OUT & I1 & REC_OUT --> INTEL_PKG
        INTEL_PKG --> EP_INT["GET /intelligence/overview"]
        INTEL_PKG --> EP_EX["GET /executive/briefing"]
        EP_INT & EP_EX --> UI["Streamlit Executive Dashboard (:8501)"]
    end

    Ingestion --> Deterministic --> Stochastic --> ReasoningStage --> Diagnostics --> DeliveryStage

    style Ingestion fill:#F8FAFC,stroke:#475569,stroke-width:2px,color:#1E293B
    style Deterministic fill:#EFF6FF,stroke:#2563EB,stroke-width:2px,color:#1E40AF
    style Stochastic fill:#FAF5FF,stroke:#9333EA,stroke-width:2px,color:#6B21A8
    style ReasoningStage fill:#FDF4FF,stroke:#C026D3,stroke-width:2px,color:#86198F
    style Diagnostics fill:#FFFBEB,stroke:#D97706,stroke-width:2px,color:#92400E
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

| # | Architecture Decision | Chosen Implementation | Technical & Business Rationale | Trade-offs & Rejected Alternatives |
|:--:|:----------------------|:----------------------|:-------------------------------|:-----------------------------------|
| **ADR-001** | **Deterministic Baseline** | 5-Step Rule Formulation | Consulting executive committees require 100% auditable mathematics with transparent haircut rules. | Machine Learning time-series models (e.g. ARIMA, Prophet) were rejected due to lack of explainability. |
| **ADR-002** | **Stochastic Complement** | Monte Carlo (5,000 runs) | Provides empirical confidence intervals (P10/P50/P90) and VaR without obfuscating the deterministic baseline. | Static sensitivity scenarios alone fail to capture multi-variable probabilistic co-variance. |
| **ADR-003** | **Data Persistence** | Dual PostgreSQL / SQLite | Enables zero-config local evaluation out-of-the-box while maintaining production PostgreSQL compatibility. | Pure PostgreSQL requires local server daemon installation for quick evaluations. |
| **ADR-004** | **Query Strategy** | Raw SQL via SQLAlchemy `text()` | Complex multi-table joins, point-in-time snapshots, and window aggregations execute with zero ORM overhead. | Full ORM querysets introduce query generation latency and memory serialization overhead. |
| **ADR-005** | **Decoupled Architecture** | Pure Python Services | Logic in `app/services` has zero coupling to HTTP frameworks, enabling rapid pytest unit execution. | Embedding calculations directly in router handlers creates tightly coupled, brittle code. |

---

## Deployment & Production Topology

```mermaid
graph LR
    subgraph Host["Host / Render Deployment Node"]
        subgraph StreamlitSvc["Streamlit Dashboard (Port 8501)"]
            ST_APP["streamlit run dashboard/app.py"]
        end

        subgraph FastAPISvc["FastAPI Service (Port 8000)"]
            UV["uvicorn app.main:app --port 8000"]
        end

        subgraph DatabaseSvc["Database Engine"]
            PG["PostgreSQL 14+ (or SQLite Fallback)"]
        end
    end

    User(["Practice Leader / Partner"]) -->|HTTPS Web Traffic| ST_APP
    ST_APP -->|Internal HTTP REST (127.0.0.1:8000)| UV
    UV -->|Connection Pool (TCP :5432)| PG

    style Host fill:#F8FAFC,stroke:#334155,stroke-width:2px,color:#0F172A
    style StreamlitSvc fill:#EFF6FF,stroke:#2563EB,stroke-width:2px,color:#1E40AF
    style FastAPISvc fill:#F0FDF4,stroke:#16A34A,stroke-width:2px,color:#15803D
    style DatabaseSvc fill:#FAF5FF,stroke:#9333EA,stroke-width:2px,color:#6B21A8

    style User fill:#FEF3CD,stroke:#D97706,stroke-width:2px,color:#92400E
    style ST_APP fill:#DBEAFE,stroke:#1D4ED8,stroke-width:1px,color:#1E3A8A
    style UV fill:#DCFCE7,stroke:#15803D,stroke-width:1px,color:#166534
    style PG fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87
```
