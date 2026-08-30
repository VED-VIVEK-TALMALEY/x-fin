# X-Fin: Enterprise Delivery Finance Operating System

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI Framework](https://img.shields.io/badge/FastAPI-0.115%2B-teal.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL Engine](https://img.shields.io/badge/PostgreSQL-14%2B-navy.svg)](https://www.postgresql.org/)
[![SQLite Fallback](https://img.shields.io/badge/SQLite-Zero--Config-lightgrey.svg)](https://www.sqlite.org/)
[![Streamlit UI](https://img.shields.io/badge/Streamlit-1.40%2B-red.svg)](https://streamlit.io/)
[![Plotly Engine](https://img.shields.io/badge/Plotly-Interactive-slate.svg)](https://plotly.com/)
[![Test Suite](https://img.shields.io/badge/Pytest-Passing-brightgreen.svg)](https://docs.pytest.org/)

---

## Executive Summary & System Overview

**X-Fin** is an enterprise-grade delivery finance operating system engineered as a functional portfolio showcase modeled on modern technology consulting delivery practices (such as **X Build**, **X Design**, and **Digital Ventures**). 

The platform automates the synthesis of commercial pipeline telemetry, contracted project backlogs, consultant staffing hours, and financial actuals into real-time, risk-adjusted revenue forecasts and executive decision intelligence.

```mermaid
flowchart TB
    subgraph S_INGEST["1. TELEMETRY INGESTION & DATA FOUNDATION"]
        direction TB
        D_ACT["<b>Delivered Actuals</b><br/>• Monthly Billable Hours<br/>• Recognized Fee Revenue<br/>• Direct Consulting Costs"]
        D_PIP["<b>Pipeline Opportunities</b><br/>• Stage Win Probabilities<br/>• Deal Contract Value<br/>• Target Close Timelines"]
        D_BDG["<b>Practice Operating Plan</b><br/>• Revenue Budgets by BU<br/>• Staffing Hours Targets<br/>• Benchmark Utilization (75%)"]
    end

    subgraph S_ENGINES["2. MULTI-ENGINE PROCESSING TIER"]
        direction TB
        E_FC["<b>Forecast Engine</b><br/>Deterministic 5-step model with 5% haircut"]
        E_MC["<b>Monte Carlo Simulator</b><br/>5,000-iteration stochastic distribution (P10/P50/P90)"]
        E_INT["<b>Intelligence & Reasoning</b><br/>20+ derived metrics, 9 insights, 10 action triggers"]
    end

    subgraph S_OUTPUT["3. EXECUTIVE DECISION SURFACES"]
        direction TB
        O_DASH["<b>Streamlit Decision Portal (:8501)</b><br/>Executive KPI banner, waterfalls, heatmaps, scenario sliders"]
        O_API["<b>FastAPI REST Gateway (:8000)</b><br/>12+ endpoints with Pydantic validation & OpenAPI docs"]
        O_BRIEF["<b>Executive Decision Readout</b><br/>Prioritized remediation playbooks with quantified INR impact"]
    end

    S_INGEST --> S_ENGINES --> S_OUTPUT

    style S_INGEST fill:#EFF6FF,stroke:#2563EB,stroke-width:2px,color:#1E40AF
    style S_ENGINES fill:#FAF5FF,stroke:#9333EA,stroke-width:2px,color:#6B21A8
    style S_OUTPUT fill:#ECFDF5,stroke:#059669,stroke-width:2px,color:#065F46

    style D_ACT fill:#DBEAFE,stroke:#1D4ED8,stroke-width:1px,color:#1E3A8A
    style D_PIP fill:#DBEAFE,stroke:#1D4ED8,stroke-width:1px,color:#1E3A8A
    style D_BDG fill:#DBEAFE,stroke:#1D4ED8,stroke-width:1px,color:#1E3A8A

    style E_FC fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87
    style E_MC fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87
    style E_INT fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87

    style O_DASH fill:#D1FAE5,stroke:#047857,stroke-width:1px,color:#064E3B
    style O_API fill:#D1FAE5,stroke:#047857,stroke-width:1px,color:#064E3B
    style O_BRIEF fill:#D1FAE5,stroke:#047857,stroke-width:1px,color:#064E3B
```

---

## Core Financial Pillars & Executive KPI Definitions

| Pillar | Metric Name | Formula / Calculation | Target Benchmark | Strategic & Operating Purpose |
|:-------|:------------|:----------------------|:----------------:|:------------------------------|
| **Revenue** | **Actual Revenue** | `SUM(project_actuals.actual_revenue)` | `>= Budget Target` | Recognized delivery fees to date across billing cycles |
| **Revenue** | **Revenue Budget** | `SUM(budgets.revenue_budget)` | Plan Baseline | Approved annual/quarterly operating plan revenue target |
| **Forecast** | **Net Forecast Revenue** | `Gross Forecast * (1 - 0.05)` | `>= Budget Target` | Primary deliverable forecast after 5% execution risk haircut |
| **Forecast** | **Forecast Headroom** | `Net Forecast - Budget Target` | `> 0` (Surplus) | Absolute buffer above baseline plan (negative = budget deficit) |
| **Coverage** | **Forward Coverage** | `((Backlog + Weighted Pipeline) / Budget) * 100` | `>= 120.0%` | Total forward book depth supporting target attainment |
| **Quality** | **Committed Revenue Mix** | `(Committed Backlog / Forward Revenue) * 100` | `>= 60.0%` | Share of forward plan secured by executed SOWs/contracts |
| **Risk** | **Pipeline Dependency** | `(Weighted Pipeline / Forward Revenue) * 100` | `<= 40.0%` | Vulnerability of forward plan to commercial conversion slippage |
| **Staffing** | **Consultant Utilization** | `(Delivered Hours / Capacity Hours) * 100` | `75.0%` Baseline | Billable staffing efficiency vs target operational capacity |
| **Stochastic**| **P50 Expected Value** | 50th Percentile of 5,000 Monte Carlo Iterations | `~ Net Forecast` | Median probabilistic outcome under stochastic volatility |
| **Stochastic**| **Value-at-Risk (VaR P10)** | `Deterministic Forecast - P10 Outcome` | Minimize | Quantified downside revenue exposure under adverse conditions |

---

## End-to-End System Architecture

```mermaid
flowchart TB
    subgraph UI_TIER["PRESENTATION TIER (Streamlit :8501)"]
        direction TB
        UI_MAIN["<b>dashboard/app.py</b><br/>• Executive Performance Overview & KPI Banner<br/>• Waterfall & Monte Carlo Confidence Charts<br/>• Risk Driver & Staffing Capacity View<br/>• BU Margins Heatmap & Sensitivity Planners"]
        UI_INTEL["<b>dashboard/intelligence.py</b><br/>• 9 Diagnostic Insight Cards<br/>• 10 Actionable Remediation Cards"]
        UI_API["<b>dashboard/api.py</b> (Requests Client with 10s Timeout)"]
        UI_MAIN & UI_INTEL --> UI_API
    end

    subgraph API_TIER["API GATEWAY (FastAPI :8000)"]
        direction TB
        APP["<b>app.main:app</b> (FastAPI ASGI Factory)"]
        R_ALL["<b>Route Handlers:</b><br/>/forecast/current · /analytics/* · /intelligence/* · /executive/* · /decisions/* · /scenarios/run"]
        APP --> R_ALL
    end

    subgraph SERVICE_TIER["SERVICE & CALCULATION ENGINES (app/services)"]
        direction TB
        S_FC["<b>forecast_engine.py</b>: 5-Step Deterministic Model"]
        S_MC["<b>monte_carlo_engine.py</b>: 5,000 Iteration Simulator"]
        S_VR["<b>variance_engine.py</b>: Budget Variance Bridges"]
        S_RS["<b>finance_reasoning.py</b>: 20+ Operating Ratios"]
        S_IN["<b>insight_engine.py</b>: 9 Severity Diagnostic Rules"]
        S_RC["<b>recommendation_engine.py</b>: 10 Action Rules"]
        S_STF["<b>staffing_engine.py</b>: Capacity & Utilization"]
    end

    subgraph DB_TIER["DATABASE PERSISTENCE (PostgreSQL 14+ / SQLite)"]
        DB_CONN[("<b>Relational Tables:</b><br/>business_units, projects, project_pipeline,<br/>project_actuals, budgets, forecast_versions")]
    end

    UI_TIER -->|HTTP REST JSON| API_TIER
    API_TIER --> SERVICE_TIER
    SERVICE_TIER --> DB_CONN

    style UI_TIER fill:#EFF6FF,stroke:#2563EB,stroke-width:2px,color:#1E40AF
    style API_TIER fill:#F0FDF4,stroke:#16A34A,stroke-width:2px,color:#15803D
    style SERVICE_TIER fill:#FAF5FF,stroke:#9333EA,stroke-width:2px,color:#6B21A8
    style DB_TIER fill:#F8FAFC,stroke:#334155,stroke-width:2px,color:#1E293B

    style UI_MAIN fill:#DBEAFE,stroke:#1D4ED8,stroke-width:1px,color:#1E3A8A
    style UI_INTEL fill:#DBEAFE,stroke:#1D4ED8,stroke-width:1px,color:#1E3A8A
    style UI_API fill:#BFDBFE,stroke:#1D4ED8,stroke-width:1px,color:#1E3A8A

    style APP fill:#DCFCE7,stroke:#15803D,stroke-width:1px,color:#166534
    style R_ALL fill:#BBF7D0,stroke:#15803D,stroke-width:1px,color:#166534

    style S_FC fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87
    style S_MC fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87
    style S_VR fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87
    style S_RS fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87
    style S_IN fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87
    style S_RC fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87
    style S_STF fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87

    style DB_CONN fill:#E2E8F0,stroke:#334155,stroke-width:1px,color:#1E293B
```

---

## Deterministic Forecast Engine (5 Steps)

```mermaid
flowchart TD
    subgraph ST1["STEP 1: INGESTION & UTILIZATION FACTOR"]
        I_CB["<b>Committed Backlog</b><br/>SUM(pipeline_value) for In Delivery & Closed Won"]
        I_WP["<b>Weighted Pipeline</b><br/>SUM(pipeline_value * win_probability)"]
        I_UT["<b>Staffing Utilization</b><br/>Delivered rate vs 75% target benchmark"]
        F_FAC["<b>Utilization Factor</b><br/><code>factor = actual_utilization / 0.75</code>"]
        I_UT --> F_FAC
    end

    subgraph ST2["STEP 2: UTILIZATION ADJUSTMENT"]
        F_ADJ["<b>Utilization Adjustment</b><br/><code>adj_util = committed_backlog * (factor - 1.0)</code>"]
        I_CB & F_FAC --> F_ADJ
    end

    subgraph ST3["STEP 3: GROSS FORECAST SYNTHESIS"]
        F_GROSS["<b>Gross Forecast Revenue</b><br/><code>gross_forecast = committed_backlog + weighted_pipeline + adj_util</code>"]
        I_CB & I_WP & F_ADJ --> F_GROSS
    end

    subgraph ST4["STEP 4: EXECUTION RISK HAIRCUT"]
        F_RISK["<b>Risk Adjustment (5%)</b><br/><code>adj_risk = gross_forecast * 0.05</code>"]
        F_GROSS --> F_RISK
    end

    subgraph ST5["STEP 5: NET DELIVERABLE FORECAST"]
        F_NET["<b>Net Forecast Revenue</b><br/><code>forecast_revenue = round(gross_forecast - adj_risk, 2)</code>"]
        F_GROSS & F_RISK --> F_NET
    end

    ST1 --> ST2 --> ST3 --> ST4 --> ST5

    style ST1 fill:#EFF6FF,stroke:#2563EB,stroke-width:2px,color:#1E40AF
    style ST2 fill:#FDF4FF,stroke:#C026D3,stroke-width:2px,color:#86198F
    style ST3 fill:#FAF5FF,stroke:#9333EA,stroke-width:2px,color:#6B21A8
    style ST4 fill:#FEF2F2,stroke:#DC2626,stroke-width:2px,color:#991B1B
    style ST5 fill:#ECFDF5,stroke:#059669,stroke-width:2px,color:#065F46
```

### Deterministic Calculation Trace Matrix

| Step | Engine Component | Mathematical Operation | Sample Input Value | Resulting Output Value |
|:----:|:-----------------|:-----------------------|:-------------------|:----------------------|
| **1** | Committed Backlog | `SUM(pipeline_value)` | Baseline Ingestion | **INR 100,000.00** |
| **2** | Weighted Pipeline | `SUM(value * prob)` | Baseline Ingestion | **INR 50,000.00** |
| **3** | Utilization Adjustment | `100,000 * (0.75 / 0.75 - 1.0)` | Target Util (75.0%) | **INR 0.00** |
| **4** | Gross Forecast | `100,000 + 50,000 + 0` | Combined Components | **INR 150,000.00** |
| **5** | Execution Haircut (5%) | `150,000 * 0.05` | 5% Delivery Discount | **INR -7,500.00** |
| **6** | **Net Deliverable Forecast** | `150,000 - 7,500` | **Net Deliverable Revenue** | **INR 142,500.00** |

---

## Monte Carlo Stochastic Simulation Engine

In addition to deterministic calculations, `app/services/monte_carlo_engine.py` executes a **5,000-iteration Monte Carlo simulation** to quantify uncertainty across pipeline conversion, utilization variance, and deliverable slippage:

```mermaid
flowchart LR
    subgraph PARAMS["1. DISTRIBUTIONS"]
        P_CONV["<b>Pipeline Win Rate</b><br/>Beta Distribution"]
        P_UTIL["<b>Staffing Util</b><br/>Normal (mean=0.75, std=0.04)"]
        P_SLIP["<b>Delivery Slippage</b><br/>Log-Normal (0% - 15%)"]
    end

    subgraph SIM["2. SIMULATION ENGINE"]
        S_ITER["<b>5,000 Iterations</b><br/>(Random Seed = 42)<br/>Calculate gross, haircuts & net"]
    end

    subgraph METRICS["3. QUANTILES & VaR"]
        Q10["<b>P10 Downside</b> (Floor)"]
        Q50["<b>P50 Median</b> (Expected)"]
        Q90["<b>P90 Upside</b> (Target)"]
        VAR["<b>Value-at-Risk (VaR)</b>"]
    end

    PARAMS --> SIM --> METRICS

    style PARAMS fill:#EFF6FF,stroke:#2563EB,stroke-width:2px,color:#1E40AF
    style SIM fill:#FAF5FF,stroke:#9333EA,stroke-width:2px,color:#6B21A8
    style METRICS fill:#ECFDF5,stroke:#059669,stroke-width:2px,color:#065F46
```

### Monte Carlo Confidence Band Interpretation

| Quantile Metric | Statistical Confidence | Strategic Interpretation | Leadership Decision Trigger |
|:----------------|:----------------------:|:-------------------------|:----------------------------|
| **P10 (Downside)** | 90% Confidence Floor | Minimum revenue expected even if deals slip | Establish baseline cost controls & staffing floor |
| **P50 (Median)** | 50th Percentile Outcome | Central tendency of stochastic revenue realization | Primary comparison point for deterministic forecast |
| **P90 (Upside)** | 10% Exceedance Rate | High-conversion scenario where major proposals close early | Reserve commercial bandwidth and contractor pool |
| **VaR (P10)** | `Net Forecast - P10` | Quantified downside exposure under market shocks | Monitor top 3 accounts for early warning signs |

---

## Intelligence & Financial Reasoning Engine

`app/services/finance_reasoning.py` and `app/services/intelligence_engine.py` derive 20+ financial telemetry indicators to classify practice health:

```mermaid
flowchart TD
    subgraph IN["FINANCIAL TELEMETRY"]
        T1["actual_revenue · budget_revenue · forecast_revenue · committed_backlog · weighted_pipeline"]
    end

    subgraph R1["1. VARIANCE & TRAJECTORY"]
        V1["<b>budget_gap</b> = actual_revenue - budget_revenue<br/><b>budget_gap_pct</b> = (budget_gap / budget_revenue) * 100<br/><b>forecast_gap</b> = forecast_revenue - budget_revenue<br/><b>forecast_gap_pct</b> = (forecast_gap / budget_revenue) * 100"]
    end

    subgraph R2["2. COVERAGE & REVENUE COMPOSITION"]
        C1["<b>forward_revenue</b> = committed_backlog + weighted_pipeline<br/><b>forward_coverage</b> = (forward_revenue / budget_revenue) * 100<br/><b>committed_forecast_coverage</b> = (committed_backlog / forecast_revenue) * 100<br/><b>committed_revenue_mix</b> = (committed_backlog / forward_revenue) * 100<br/><b>pipeline_dependency</b> = (weighted_pipeline / forward_revenue) * 100"]
    end

    subgraph R3["3. HEALTH CLASSIFICATIONS"]
        H1["<b>forecast_risk</b>: 'low' (>=70%), 'moderate' (50-69%), 'high' (<50%)<br/><b>pipeline_risk</b>: 'low' (<=30%), 'moderate' (31-50%), 'high' (>50%)<br/><b>forward_position</b>: 'strong' (>=120%), 'adequate' (100-119%), 'watch' (80-99%), 'weak' (<80%)"]
    end

    IN --> R1 --> R2 --> R3

    style IN fill:#F8FAFC,stroke:#475569,stroke-width:2px,color:#1E293B
    style R1 fill:#EFF6FF,stroke:#2563EB,stroke-width:2px,color:#1E40AF
    style R2 fill:#FAF5FF,stroke:#9333EA,stroke-width:2px,color:#6B21A8
    style R3 fill:#ECFDF5,stroke:#059669,stroke-width:2px,color:#065F46
```

---

## Practice Lead Diagnostic Matrix (9 Heuristic Rules)

| # | Diagnostic Dimension | Telemetry Metric | [HIGH] Severity Trigger | [MEDIUM] Severity Trigger | [LOW] Severity Trigger | Management Playbook |
|:--:|:---------------------|:-----------------|:------------------------|:--------------------------|:-----------------------|:--------------------|
| **1** | Revenue Performance | `budget_gap_pct` | `<= -10.0%` | `-10.0% < gap < 0.0%` | `>= 0.0%` | Investigate billable hours recognition across active cases |
| **2** | Forecast Trajectory | `forecast_gap_pct` | `<= -10.0%` | `-10.0% < gap < 0.0%` | `>= 0.0%` | Partner intervention required to accelerate late-stage pipeline |
| **3** | Forward Coverage | `forward_coverage` | `< 100.0%` | `100.0% <= cov < 120.0%` | `>= 120.0%` | Originate new proposals in priority client accounts |
| **4** | Forecast Quality | `committed_forecast_coverage` | `< 50.0%` | `50.0% <= cov < 70.0%` | `>= 70.0%` | Expedite signature of pending Statements of Work (SOWs) |
| **5** | Pipeline Dependency | `pipeline_dependency` | `>= 60.0%` | `40.0% <= dep < 60.0%` | `< 40.0%` | De-risk plan by closing top 3 opportunities |
| **6** | Committed Revenue Mix| `committed_revenue_mix` | `< 40.0%` | `40.0% <= mix < 60.0%` | `>= 60.0%` | Harden backlog to ensure staffing certainty |
| **7** | Forecast Risk Profile| `forecast_risk` | `== "high"` | `== "moderate"` | `== "low"` | Implement weekly case milestone health checks |
| **8** | Market Stance | `forward_position` | `in ("watch", "weak")` | `== "adequate"` | `== "strong"` | Align practice staffing and hiring to pipeline reality |
| **9** | Headroom Buffer | `forecast_headroom` | `< 0.0` | — | `> 0.0` | Dedicate partner commercial capacity to bridge shortfall |

---

## Action Recommendation Engine (10 Rules)

| Priority | Operational Domain | Activation Condition | Prescriptive Action Item | Quantified Financial Impact (INR) |
|:---------|:-------------------|:---------------------|:-------------------------|:----------------------------------|
| **[HIGH]** | Revenue Recovery | `budget_gap < 0` | Mobilize partner-led revenue recovery plan on lagging accounts | `abs(budget_gap)` |
| **[HIGH]** | Forecast Protection | `forecast_gap < 0` | Lock in pending contract extensions and prevent scope reduction | `abs(forecast_gap)` |
| **[HIGH]** | Pipeline Coverage | `forward_coverage < 100%` | Fast-track high-probability proposals to achieve baseline budget | `budget_revenue - forward_revenue` |
| **[MEDIUM]** | Coverage Buffer | `100% <= forward_coverage < 120%` | Maintain business development momentum to preserve safety buffer | `forward_revenue - budget_revenue` |
| **[HIGH]** | Deal Closure Surge | `pipeline_dependency >= 60%` | Conduct executive closing sessions on all deals in Qualified stage | `weighted_pipeline` |
| **[MEDIUM]** | Velocity Management | `40% <= pipeline_dependency < 60%` | Review stage-gate progression weekly with client teams | `weighted_pipeline` |
| **[HIGH]** | Backlog Fortification| `committed_forecast_coverage < 50%` | Prioritize execution of MSAs and SOWs currently under legal review | `forecast_revenue - committed_backlog` |
| **[MEDIUM]** | Backlog Hardening | `50% <= committed_forecast_coverage < 70%` | Expedite client sign-offs on milestone deliverables | `forecast_revenue - committed_backlog` |
| **[HIGH]** | Delivery Audit | `forecast_risk == "high"` | Conduct portfolio-wide review to prevent deliverable slippage | `forecast_revenue` |
| **[LOW]** | Margin Optimization | `forward_coverage >= 120%` & `pipeline < 60%` | Prioritize higher-margin, premium-rate engagements | `forecast_gap` |

---

## Engagement Lifecycle & Backlog Transition Model

```mermaid
stateDiagram-v2
    [*] --> Prospect : Win Prob = 15% (Uncommitted)
    Prospect --> Qualified : Win Prob = 35% (Uncommitted)
    Qualified --> In_Delivery : Win Prob = 75% (Committed)
    Qualified --> Closed_Lost : Win Prob = 0%
    In_Delivery --> Closed_Won : Win Prob = 100% (Committed)
    In_Delivery --> Closed_Lost : Win Prob = 0%
```

---

## Relational Database Architecture

```mermaid
erDiagram
    BUSINESS_UNITS ||--o{ PROJECTS : manages
    BUSINESS_UNITS ||--o{ BUDGETS : targets
    PROJECTS ||--o{ PROJECT_PIPELINE : snapshots
    PROJECTS ||--o{ PROJECT_ACTUALS : recognizes

    BUSINESS_UNITS {
        int id PK
        string name "X Build, X Design, Digital Ventures"
    }

    PROJECTS {
        int id PK
        int business_unit_id FK
        string name
        string stage
        numeric contract_value
        numeric billing_rate
    }

    PROJECT_PIPELINE {
        int id PK
        int project_id FK
        date snapshot_date
        string stage
        numeric pipeline_value
        numeric win_probability
    }

    PROJECT_ACTUALS {
        int id PK
        int project_id FK
        date month
        int actual_hours
        numeric actual_revenue
        numeric actual_cost
    }

    BUDGETS {
        int id PK
        int business_unit_id FK
        date month
        numeric revenue_budget
        numeric utilization_budget
    }
```

---

## Complete API Route Specifications

| Method | Endpoint Path | Return Schema | Function / Module | Operational Description |
|:------:|:--------------|:--------------|:------------------|:------------------------|
| `GET` | `/` | `Dict[str, str]` | `app.main` | Application name, version, status, description |
| `GET` | `/health` | `HealthStatus` | `app.main` | System health check probe |
| `GET` | `/health/db` | `Dict[str, str]` | `app.main` | Database connection status |
| `GET` | `/forecast/current` | `ForecastResponse` | `forecast_engine.build_forecast()` | Current period forecast, pipeline & backlog summary |
| `GET` | `/analytics/summary` | `FinanceSummary` | `finance_queries.get_finance_summary()` | Aggregated actuals, budgets, and backlog summary |
| `GET` | `/analytics/monthly-revenue` | `List[MonthlyRevenue]` | `finance_queries.get_monthly_revenue()` | Historical monthly recognized revenue, hours, cost |
| `GET` | `/analytics/backlog` | `BacklogResponse` | `backlog_engine.calculate_backlog()` | Committed vs uncommitted backlog and waterfall |
| `GET` | `/analytics/variance` | `VarianceResult` | `variance_engine.calculate_variance()` | Absolute and % actual vs budget and forecast vs budget |
| `GET` | `/analytics/forecast-accuracy`| `List[AccuracyItem]` | `forecast_accuracy.get_forecast_accuracy()` | Month-by-month historical forecast accuracy |
| `GET` | `/analytics/business-units` | `List[BUPerformance]` | `business_unit_engine.get_bu_performance()` | Practice-level revenue, margin, and hours breakdown |
| `GET` | `/intelligence/health` | `HealthStatus` | `routers.intelligence` | Intelligence subsystem health check |
| `GET` | `/intelligence/overview` | `IntelligencePackage` | `intelligence_engine.build_intelligence_overview()` | Full reasoning metrics, insights, recommendations |
| `GET` | `/executive/briefing` | `Dict[str, Any]` | `executive_briefing_engine` | Leadership executive briefing synthesis |
| `GET` | `/decisions/overview` | `Dict[str, Any]` | `decision_engine` | Standardized decision triggers |
| `POST` | `/scenarios/run` | `ScenarioResult` | `scenario_engine.run_scenario()` | Multi-parameter what-if revenue simulation |
| `GET` | `/projects` | `List[Dict[str, Any]]` | `routers.projects` | Project directory |

---

## Scenario Simulation Engine

`app/services/scenario_engine.py` models the revenue impact of commercial and operational shocks:

```mermaid
flowchart LR
    subgraph Inputs["1. Scenario Inputs"]
        B["Base Revenue"]
        P["Pipeline Revenue"]
        U["Utilization"]
        C_CHG["Conversion Delta"]
        U_CHG["Util Delta"]
        R_CHG["Rate Delta"]
        S_CHG["Slippage Rate"]
    end

    subgraph Adjustments["2. Adjustments"]
        P_ADJ["Adjusted Pipe = Pipe * (1 + delta_conv)"]
        U_FAC["Util Factor = (Util + delta_util) / Util"]
        B_ADJ["Adjusted Base = Base * Util_Fac * (1 + delta_rate)"]
        P & C_CHG --> P_ADJ
        U & U_CHG --> U_FAC
        B & U_FAC & R_CHG --> B_ADJ
    end

    subgraph Output["3. Output"]
        COMB["Pre-Slippage = Base_Adj + Pipe_Adj"]
        SCEN["Scenario Revenue = Pre_Slippage * (1 - slippage)"]
        DELT["Delta = Scenario - Base"]
        P_ADJ & B_ADJ --> COMB --> SCEN --> DELT
    end

    style Inputs fill:#F8FAFC,stroke:#475569,stroke-width:2px,color:#1E293B
    style Adjustments fill:#FFFBEB,stroke:#D97706,stroke-width:2px,color:#92400E
    style Output fill:#ECFDF5,stroke:#059669,stroke-width:2px,color:#065F46
```

---


<<<<<<< HEAD
```bash
# 1. Enter x-fin directory
cd consulting-forecast-engine/x-fin

# 2. Virtual Environment Setup
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# 3. Start FastAPI Service
uvicorn app.main:app --reload --port 8000

# 4. Start Executive Dashboard
cd dashboard
streamlit run app.py

# 5. Automated Testing
pytest tests/ -v
```

---
=======
>>>>>>> 2cf98977284ac948c626d1271915ba23dd008caa

## Technical Documentation Directory

| Document Path | Description |
|:--------------|:------------|
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Component architecture, deployment topology, and data flow pipelines |
| [docs/API.md](docs/API.md) | REST API endpoints, JSON schemas, payload examples, and status codes |
| [docs/DATA_MODEL.md](docs/DATA_MODEL.md) | PostgreSQL relational schema, column definitions, constraints, and ERD |
| [docs/FORECAST_ENGINE.md](docs/FORECAST_ENGINE.md) | Mathematical formulation, parameter sensitivities, and haircut rules |
| [docs/INTELLIGENCE.md](docs/INTELLIGENCE.md) | Reasoning specifications, 9 insight evaluators, and 10 action triggers |
| [docs/DASHBOARD.md](docs/DASHBOARD.md) | Streamlit user workflows, executive tabs, charts, and sensitivity controls |
| [docs/METRICS.md](docs/METRICS.md) | Standard metric glossary, formulas, and data quality caveats |
| [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) | Setup walkthrough, test suite executions, conventions, and dependencies |
| [docs/PRODUCTION.md](docs/PRODUCTION.md) | Render deployment, Docker, logging, health checks, and runbooks |

---

## Project Attribution

Personal Portfolio Project · Delivery Finance Operating System Showcase
