# X-Fin Architecture Overview

> **Version:** 1.0.0 · **Target Environment:** Python 3.10+ / FastAPI / PostgreSQL 14+ / Streamlit

---

## Architectural Topology

```mermaid
graph TB
    subgraph Client["CLIENT TIER"]
        BROWSER["Web Browser (Port 8501)"]
    end

    subgraph PresentationTier["PRESENTATION TIER (Streamlit :8501)"]
        UI_MAIN["<b>dashboard/app.py</b><br/>• Executive Performance Overview<br/>• Revenue Performance Line Chart<br/>• Backlog Waterfall Chart<br/>• Business Unit Margins Grouped Chart<br/>• Forecast Accuracy Time Series<br/>• Scenario Planning Sliders"]
        UI_INTEL["<b>dashboard/intelligence.py</b><br/>• Financial Status Banner<br/>• Revenue Outlook Comparison Bar<br/>• Forward Revenue Split Bar<br/>• Forecast Construction Dataframe<br/>• Scored Insights Cards<br/>• Action Recommendations Cards"]
        UI_CHARTS["<b>dashboard/charts.py</b><br/>Plotly Chart Builders (Line, Bar, Waterfall)"]
        UI_COMP["<b>dashboard/components.py</b><br/>UI Helper Functions & Formatters"]
        UI_API["<b>dashboard/api.py</b><br/>Requests HTTP Client with 10s Timeout"]

        UI_MAIN & UI_INTEL --> UI_CHARTS
        UI_MAIN & UI_INTEL --> UI_COMP
        UI_MAIN & UI_INTEL --> UI_API
    end

    subgraph APITier["API GATEWAY TIER (FastAPI :8000)"]
        MAIN["<b>app/main.py</b><br/>FastAPI Application Factory & CORS Middleware"]
        subgraph Routers["FastAPI APIRouters"]
            R_FORECAST["<b>routers/forecast.py</b><br/>GET /forecast/current"]
            R_ANALYTICS["<b>routers/analytics.py</b><br/>GET /analytics/summary<br/>GET /analytics/monthly-revenue<br/>GET /analytics/backlog<br/>GET /analytics/variance<br/>GET /analytics/forecast-accuracy<br/>GET /analytics/business-units"]
            R_INTEL["<b>routers/intelligence.py</b><br/>GET /intelligence/health<br/>GET /intelligence/overview"]
            R_SCENARIOS["<b>routers/scenarios.py</b><br/>POST /scenarios/run"]
            R_PROJECTS["<b>routers/projects.py</b><br/>GET /projects"]
        end
        MAIN --> Routers
    end

    subgraph ServiceTier["SERVICE & BUSINESS LOGIC TIER (app/services)"]
        S_FC["<b>forecast_engine.py</b><br/>build_forecast()"]
        S_BL["<b>backlog_engine.py</b><br/>calculate_backlog(), calculate_backlog_waterfall()"]
        S_VR["<b>variance_engine.py</b><br/>calculate_variance(), variance_bridge()"]
        S_RS["<b>finance_reasoning.py</b><br/>explain_financial_position()"]
        S_IN["<b>insight_engine.py</b><br/>generate_insights()"]
        S_RC["<b>recommendation_engine.py</b><br/>generate_recommendations()"]
        S_SC["<b>scenario_engine.py</b><br/>run_scenario()"]
        S_BU["<b>business_unit_engine.py</b><br/>get_bu_performance()"]
        S_FA["<b>forecast_accuracy.py</b><br/>get_forecast_accuracy()"]
        S_FQ["<b>finance_queries.py</b><br/>get_finance_summary(), get_pipeline_summary(), get_budget_summary(), get_monthly_revenue()"]
    end

    subgraph DataTier["DATA PERSISTENCE TIER (PostgreSQL 14+)"]
        DB_CONN["<b>app/db/connection.py</b><br/>SQLAlchemy create_engine() & get_db() sessionmaker"]
        subgraph Tables["Relational Tables (app/db/schema.sql)"]
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
```

---

## Intelligence Subsystem Data Flow Pipeline

```mermaid
flowchart TD
    subgraph Ingestion["1. DATABASE QUERY EXECUTION"]
        DB[(PostgreSQL)]
        Q1["<b>finance_queries.get_finance_summary(db)</b><br/>SELECT COALESCE(SUM(actual_revenue),0), COALESCE(SUM(actual_cost),0), COALESCE(SUM(contract_value),0)"]
        Q2["<b>finance_queries.get_budget_summary(db)</b><br/>SELECT COALESCE(SUM(revenue_budget),0), COALESCE(AVG(utilization_budget),0)"]
        Q3["<b>finance_queries.get_pipeline_summary(db)</b><br/>SELECT COUNT(*), SUM(pipeline_value), SUM(pipeline_value * probability) [Latest Snapshot]"]
        Q4["<b>backlog_engine.calculate_backlog(db)</b><br/>SELECT SUM(pipeline_value) WHERE stage IN ('In Delivery', 'Closed Won') vs ('Prospect', 'Qualified')"]

        DB --> Q1 & Q2 & Q3 & Q4
    end

    subgraph ForecastStage["2. FORECAST SYNTHESIS (forecast_engine.py)"]
        F1["<b>forecast_engine.build_forecast()</b><br/>Inputs: committed_backlog, weighted_pipeline, utilization=budget_utilization, target=0.75, risk=0.05<br/>1. Factor = utilization / 0.75<br/>2. Util_Adj = committed_backlog * (Factor - 1.0)<br/>3. Gross = committed_backlog + weighted_pipeline + Util_Adj<br/>4. Risk_Adj = Gross * 0.05<br/>5. Net Forecast = Gross - Risk_Adj"]
        Q3 & Q4 & Q2 --> F1
        F1 --> F_OUT["<b>ForecastResult Dataclass</b><br/>forecast_revenue, committed_backlog, weighted_pipeline, utilization_adjustment, risk_adjustment"]
    end

    subgraph ReasoningStage["3. FINANCE REASONING (finance_reasoning.py)"]
        R1["<b>finance_reasoning.explain_financial_position()</b><br/>Inputs: actual_revenue, budget_revenue, forecast_revenue, committed_backlog, weighted_pipeline<br/>Computes 20+ Financial Ratios & Classifications:<br/>• budget_gap = actual - budget | budget_gap_pct<br/>• forecast_gap = forecast - budget | forecast_gap_pct<br/>• forward_revenue = committed + weighted<br/>• forward_coverage = (forward_revenue / budget) * 100<br/>• committed_forecast_coverage = (committed / forecast) * 100<br/>• pipeline_dependency = (weighted / forward) * 100<br/>• committed_revenue_mix = (committed / forward) * 100<br/>• forecast_risk: 'low' | 'moderate' | 'high'<br/>• pipeline_risk: 'low' | 'moderate' | 'high'<br/>• forward_position: 'strong' | 'adequate' | 'watch' | 'weak'"]
        Q1 & Q2 & F_OUT & Q4 & Q3 --> R1
        R1 --> R_OUT["<b>Reasoning Output Dictionary</b>"]
    end

    subgraph InsightStage["4. INSIGHT SCORING (insight_engine.py)"]
        I1["<b>insight_engine.generate_insights()</b><br/>Evaluates 9 Deterministic Severity Rules:<br/>1. Actual vs Budget<br/>2. Forecast vs Budget<br/>3. Forward Revenue Coverage<br/>4. Committed Forecast Coverage<br/>5. Pipeline Dependency<br/>6. Committed Revenue Mix<br/>7. Forecast Risk Profile<br/>8. Forward Market Stance<br/>9. Forecast Headroom Buffer"]
        R_OUT --> I1
        I1 --> I_OUT["<b>Array of Scored Insight Dictionaries</b><br/>[{severity: 'HIGH'|'MEDIUM'|'LOW', category, metric, message, value}]"]
    end

    subgraph RecommendationStage["5. ACTION RECOMMENDATIONS (recommendation_engine.py)"]
        REC1["<b>recommendation_engine.generate_recommendations()</b><br/>Evaluates 10 Action Rules with Priority Sorting:<br/>1. Revenue Recovery (budget_gap < 0)<br/>2. Forecast Protection (forecast_gap < 0)<br/>3. Pipeline Acceleration (coverage < 100%)<br/>4. Coverage Buffer (100% <= coverage < 120%)<br/>5. Pipeline Risk Surge (dependency >= 60%)<br/>6. Velocity Management (40% <= dependency < 60%)<br/>7. Backlog Fortification (committed_coverage < 50%)<br/>8. Backlog Hardening (50% <= committed_coverage < 70%)<br/>9. Delivery Audit (forecast_risk == 'high')<br/>10. Growth Optimization (coverage >= 120% & pipeline < 60%)"]
        R_OUT & I_OUT --> REC1
        REC1 --> REC_OUT["<b>Array of Action Recommendation Dictionaries</b><br/>[{priority: 'HIGH'|'MEDIUM'|'LOW', category, action, rationale, financial_impact}]"]
    end

    subgraph DeliveryStage["6. API RESPONSE DISPATCH"]
        EP["<b>GET /intelligence/overview</b><br/>JSON Package: status, reasoning, insights, recommendations, source_metrics, forecast"]
        R_OUT & I_OUT & REC_OUT --> EP
        EP --> ST["<b>dashboard/intelligence.py</b><br/>Render Executive Streamlit UI"]
    end

    Ingestion --> ForecastStage --> ReasoningStage --> InsightStage --> RecommendationStage --> DeliveryStage
```

---

## Architectural Decision Records (ADRs)

| Decision Item | Chosen Approach | Rationale | Alternatives Evaluated |
|:--------------|:----------------|:----------|:-----------------------|
| **Forecasting Model** | Deterministic Rule-Based Engine | In enterprise delivery finance, all adjustments must be audit-compliant and mathematically verifiable. | Time-series ML (ARIMA/Prophet) was rejected due to black-box explainability issues in partner reviews. |
| **Data Querying** | Raw SQL with SQLAlchemy `text()` | Complex multi-table financial rollups require explicit `COALESCE`, `DATE_TRUNC`, and window aggregations. | Heavy ORM querysets introduce query latency and serialization overhead. |
| **Pipeline Storage** | Point-in-Time Snapshot Table | Tracking stage conversion and deal velocity requires immutable historical snapshots per snapshot date. | In-place update tables overwrite past states, destroying pipeline velocity analytics. |
| **Decoupled Architecture** | Pure Python Logic in `app/services` | Service modules have zero dependencies on FastAPI request contexts, enabling standalone unit testing. | Embedding calculations directly inside router endpoints creates coupling. |
| **UI Presentation** | Streamlit + Plotly Engine | Enables interactive executive dashboarding with minimal frontend boilerplate. | React / Vue SPA was evaluated but Streamlit provides native Python analytics integration. |

---

## Deployment & Network Topology

```mermaid
graph LR
    subgraph Host["Container / Local Host Environment"]
        subgraph ServiceStreamlit["Streamlit Service (Port 8501)"]
            ST_APP["streamlit run dashboard/app.py"]
        end

        subgraph ServiceFastAPI["FastAPI ASGI Server (Port 8000)"]
            UV["uvicorn app.main:app --port 8000"]
        end

        subgraph ServicePostgres["PostgreSQL Database (Port 5432)"]
            PG["consulting_forecast Database"]
        end
    end

    User(["Executive / Finance Lead"]) -->|HTTP Browser Request| ST_APP
    ST_APP -->|Internal REST API Calls (127.0.0.1:8000)| UV
    UV -->|Connection Pooling / TCP :5432| PG
```
