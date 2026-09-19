# X-Fin System Reference & Architecture Manual

## Document Overview

This document provides a consolidated technical and operational reference for the **X-Fin Delivery Finance Operating System**. It describes the core architectural layers, computational pipelines, relational data models, REST endpoints, and diagnostic heuristic frameworks.

---

## 1. End-to-End System Architecture

```
+-----------------------------------------------------------------------------------------------------------------------------------------+
|                                                      1. PRESENTATION TIER (STREAMLIT :8501)                                              |
|                                                                                                                                         |
|  +-------------------------------------+  +-------------------------------------+  +-------------------------------------------------+  |
|  |       app.py (Executive View)       |  |     intelligence.py (Action Hub)    |  |               charts.py & components.py         |  |
|  |  * Metric Summary KPI Banners       |  |  * 9 Rule-Based Diagnostic Cards    |  |  * Waterfall Forecast Visualizer                |  |
|  |  * Revenue & Margin Realization     |  |  * 10 Prioritized Action Cards      |  |  * Monte Carlo Distribution Density Plots       |  |
|  |  * Business Unit Performance Matrix |  |  * Headroom & VaR Impact Metrics    |  |  * Scenario Sensitivity Sliders                 |  |
|  +-------------------------------------+  +-------------------------------------+  +-------------------------------------------------+  |
|                                                     |                                                                                   |
|                                                     v (Internal Python Requests Client)                                                 |
|                                     +---------------------------------------------------+                                               |
|                                     |    api.py (Resilient REST Connector with Timeout) |                                               |
|                                     +---------------------------------------------------+                                               |
+-----------------------------------------------------------------|-----------------------------------------------------------------------+
                                                                  | HTTP REST (JSON / Port 8000)
                                                                  v
+-----------------------------------------------------------------------------------------------------------------------------------------+
|                                                       2. API GATEWAY TIER (FASTAPI :8000)                                               |
|                                                                                                                                         |
|  +------------------------------------+  +-------------------------------------+  +--------------------------------------------------+  |
|  |        /forecast/current           |  |          /analytics/*               |  |           /intelligence/* & /executive/*         |  |
|  |  * 5-Step Net Deliverable Baseline  |  |  * /summary, /monthly-revenue       |  |  * /overview (Unified Diagnostic Bundle)         |  |
|  |  * Backlog vs Pipeline Allocation  |  |  * /backlog (Stage Breakdown)       |  |  * /briefing (Strategic Status & Health)         |  |
|  |  * Haircut & Utilization Adjust    |  |  * /variance (Budget vs Actual)     |  |  * /decisions/overview & /scenarios/run          |  |
|  +------------------------------------+  +-------------------------------------+  +--------------------------------------------------+  |
+-----------------------------------------------------------------|-----------------------------------------------------------------------+
                                                                  |
                                                                  v
+-----------------------------------------------------------------------------------------------------------------------------------------+
|                                                   3. COMPUTATION & REASONING ENGINES                                                    |
|                                                                                                                                         |
|  +----------------------------------------------------+   +--------------------------------------------------------------------------+  |
|  |               Deterministic Engines                |   |                       Stochastic & Variance Engines                      |  |
|  |  * forecast_engine.py (5-Step Deterministic Model) |   |  * monte_carlo_engine.py (5,000 Stochastic Iterations: P10, P50, P90)    |  |
|  |  * backlog_engine.py (Contract Realization)        |   |  * variance_engine.py (Revenue & Margin Bridges vs Operating Budget)     |  |
|  |  * forecast_decomposition.py (Additive Waterfall)  |   |  * scenario_engine.py (Multi-Parameter Parametric Sensitivity Model)     |  |
|  +----------------------------------------------------+   +--------------------------------------------------------------------------+  |
|                                                                                                                                         |
|  +-----------------------------------------------------------------------------------------------------------------------------------+  |
|  |                                                 Diagnostic & Decision Engines                                                     |  |
|  |  * finance_reasoning.py (Calculates 20+ Financial Ratios, Forward Coverage, Pipeline Risk, and Operational Health)               |  |
|  |  * insight_engine.py (Evaluates 9 Diagnostic Rules, Classifying Severity into High, Medium, and Low Alert Badges)                 |  |
|  |  * recommendation_engine.py (Evaluates 10 Prescriptive Action Playbooks and Computes Quantified Financial Impact)                 |  |
|  |  * staffing_engine.py & staffing_insight_engine.py (Analyzes Delivery Hours vs Budgeted Demand and Flags Data Review State)       |  |
|  +-----------------------------------------------------------------------------------------------------------------------------------+  |
+-----------------------------------------------------------------|-----------------------------------------------------------------------+
                                                                  | SQLAlchemy Core / Raw SQL Queries
                                                                  v
+-----------------------------------------------------------------------------------------------------------------------------------------+
|                                                  4. PERSISTENCE LAYER (POSTGRESQL / SQLITE)                                             |
|                                                                                                                                         |
|  +-------------------------+  +-------------------------+  +--------------------------+  +---------------------------------------+  |
|  |     business_units      |  |        projects         |  |     project_pipeline     |  |            project_actuals            |  |
|  |  * business_unit_id(PK) |  |  * project_id (PK)      |  |  * pipeline_id (PK)      |  |  * actual_id (PK)                     |  |
|  |  * name                 |  |  * business_unit_id(FK) |  |  * project_id (FK)       |  |  * project_id (FK)                    |  |
|  |                         |  |  * stage, contract_val  |  |  * probability, stage    |  |  * actual_revenue, actual_cost, hours |  |
|  +-------------------------+  +-------------------------+  +--------------------------+  +---------------------------------------+  |
|                                                                                                                                         |
|  +------------------------------------------------------+  +-------------------------------------------------------------------------+  |
|  |                        budgets                       |  |                   forecast_versions & forecast_values                   |  |
|  |  * budget_id (PK)                                    |  |  * forecast_id (PK)                                                     |  |
|  |  * business_unit_id (FK)                             |  |  * forecast_month, forecast_method                                       |  |
|  |  * revenue_budget, hours_budget, utilization_budget  |  |  * forecast_value_id (PK), project_id (FK), forecast_revenue             |  |
|  +------------------------------------------------------+  +-------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------------------------------------------------------------+
```

---

## 2. Telemetry Ingestion & Forecast Pipeline

```
+---------------------------------------------------------------------------------------------------------------------------------------+
|                                                        STAGE 1: INPUT EXTRACTION                                                      |
|                                                                                                                                       |
|  [Committed Backlog Ingestion]            [Weighted Pipeline Ingestion]           [Utilization Tracking]                              |
|  SUM(contract_value) for:                 SUM(contract_value * win_probability)   Current Practice Utilization: 74.0%                 |
|  'In Delivery' & 'Closed Won'             for 'Prospect' & 'Qualified'            Target Benchmark Standard:    75.0%                 |
|  Value: INR 100,000.00                    Value: INR 50,000.00                    Delta Ratio: 0.74 / 0.75 = 0.9867                   |
+---------------------------------------------------|-----------------------------------------------------------------------------------+
                                                    |
                                                    v
+---------------------------------------------------------------------------------------------------------------------------------------+
|                                                    STAGE 2: UTILIZATION ADJUSTMENT                                                    |
|                                                                                                                                       |
|  Utilization Factor     = actual_utilization / target_utilization                                                                     |
|  Utilization Adjustment = committed_backlog * (utilization_factor - 1.0)                                                              |
|                                                                                                                                       |
|  At Standard Parity (75% / 75%):                                                                                                      |
|  Utilization Adjustment = INR 100,000.00 * (1.0 - 1.0) = INR 0.00                                                                     |
+---------------------------------------------------|-----------------------------------------------------------------------------------+
                                                    |
                                                    v
+---------------------------------------------------------------------------------------------------------------------------------------+
|                                                    STAGE 3: GROSS FORECAST SYNTHESIS                                                  |
|                                                                                                                                       |
|  Gross Forecast Revenue = Committed Backlog + Weighted Pipeline + Utilization Adjustment                                              |
|  Gross Forecast Revenue = INR 100,000.00 + INR 50,000.00 + INR 0.00 = INR 150,000.00                                                 |
+---------------------------------------------------|-----------------------------------------------------------------------------------+
                                                    |
                                                    v
+---------------------------------------------------------------------------------------------------------------------------------------+
|                                                    STAGE 4: EXECUTION RISK HAIRCUT                                                    |
|                                                                                                                                       |
|  Risk Adjustment Rate = 5.0% (Execution Buffer for Project Delay & Commercial Slippage)                                               |
|  Risk Haircut Amount  = Gross Forecast Revenue * 0.05                                                                                 |
|  Risk Haircut Amount  = INR 150,000.00 * 0.05 = INR 7,500.00                                                                          |
+---------------------------------------------------|-----------------------------------------------------------------------------------+
                                                    |
                                                    v
+---------------------------------------------------------------------------------------------------------------------------------------+
|                                                    STAGE 5: NET DELIVERABLE FORECAST                                                  |
|                                                                                                                                       |
|  Net Forecast Revenue = Gross Forecast Revenue - Risk Haircut Amount                                                                  |
|  Net Forecast Revenue = INR 150,000.00 - INR 7,500.00 = INR 142,500.00                                                                |
+---------------------------------------------------------------------------------------------------------------------------------------+
```

---

## 3. Monte Carlo Simulation Engine

```
+---------------------------------------------------------------------------------------------------------------------------------------+
|                                                     1. PARAMETRIC DISTRIBUTIONS                                                       |
|                                                                                                                                       |
|  +-----------------------------------+  +------------------------------------+  +--------------------------------------------------+  |
|  |     Pipeline Win Probabilities    |  |     Staffing Utilization Rate      |  |             Delivery Project Slippage            |  |
|  |  * Modeled via Beta Distribution  |  |  * Normal Distribution             |  |  * Log-Normal Distribution                       |  |
|  |  * Reflects historical win rates  |  |  * Mean = 0.75, StdDev = 0.035     |  |  * Right-skewed delay factor (0% to 15%)         |  |
|  +-----------------------------------+  +------------------------------------+  +--------------------------------------------------+  |
+-------------------------------------------------------------------|-------------------------------------------------------------------+
                                                                    |
                                                                    v
+---------------------------------------------------------------------------------------------------------------------------------------+
|                                                     2. STOCHASTIC SIMULATION RUN                                                      |
|                                                                                                                                       |
|  Number of Iterations : 5,000 Independent Trials                                                                                      |
|  Random Number Seed   : 42 (Guarantees Reproducibility across Test Environments)                                                      |
|  Trial Execution Logic: Evaluates Gross Synthesis, Slippage Drag, and Risk Haircut across each trial                                  |
+-------------------------------------------------------------------|-------------------------------------------------------------------+
                                                                    |
                                                                    v
+---------------------------------------------------------------------------------------------------------------------------------------+
|                                                     3. OUTPUT DISTRIBUTION & RISK METRICS                                             |
|                                                                                                                                       |
|  +-------------------------------+  +--------------------------------+  +--------------------------------+  +----------------------+  |
|  |         P10 (Floor)           |  |          P50 (Median)          |  |          P90 (Upside)          |  | Value-at-Risk (VaR)  |  |
|  |  * 10th Percentile Outcome    |  |  * 50th Percentile Outcome     |  |  * 90th Percentile Outcome     |  |  * Net Forecast - P10|  |
|  |  * Conservative 90% floor     |  |  * Probabilistic central value |  |  * Optimistic target capture   |  |  * Downside risk amt |  |
|  |  * Capital protection anchor  |  |  * Benchmarked against Net     |  |  * Resource surge indicator    |  |  * Risk exposure     |  |
|  +-------------------------------+  +--------------------------------+  +--------------------------------+  +----------------------+  |
+---------------------------------------------------------------------------------------------------------------------------------------+
```

---

## 4. Diagnostic & Recommendation Playbook Pipeline

```
+---------------------------------------------------------------------------------------------------------------------------------------+
|                                                       STEP 1: TELEMETRY EXTRACTION                                                    |
|                                                                                                                                       |
|  Actual Revenue       : Recognized delivery fees from project_actuals                                                                 |
|  Operating Budget     : Revenue and hours targets from budgets                                                                        |
|  Committed Backlog    : Contract value for 'In Delivery' and 'Closed Won' engagements                                                 |
|  Weighted Pipeline    : Probability-discounted commercial pipeline value                                                              |
|  Net Forecast Revenue : 5-step risk-adjusted deliverable projection                                                                   |
+---------------------------------------------------|-----------------------------------------------------------------------------------+
                                                    |
                                                    v
+---------------------------------------------------------------------------------------------------------------------------------------+
|                                                   STEP 2: FINANCIAL REASONING ENGINE                                                  |
|                                                                                                                                       |
|  Variance Ratios     : budget_gap, budget_gap_pct, forecast_gap, forecast_gap_pct, forecast_headroom                                  |
|  Coverage Ratios     : forward_revenue, forward_coverage, committed_forecast_coverage                                                 |
|  Composition Ratios  : pipeline_dependency, committed_revenue_mix                                                                     |
|  Health Indicators   : forecast_risk, pipeline_risk, forward_position, headroom_status                                                |
+---------------------------------------------------|-----------------------------------------------------------------------------------+
                                                    |
                                                    v
+---------------------------------------------------------------------------------------------------------------------------------------+
|                                                   STEP 3: DIAGNOSTIC INSIGHT ENGINE                                                   |
|                                                                                                                                       |
|  Evaluates 9 Heuristic Severity Rules:                                                                                                |
|  * Rule 1: Revenue Realization Gap vs Operating Budget                                                                                |
|  * Rule 2: Net Forecast Headroom Gap vs Operating Budget                                                                              |
|  * Rule 3: Forward Coverage Depth vs Target Baseline                                                                                  |
|  * Rule 4: Committed Backlog Coverage of Net Forecast                                                                                 |
|  * Rule 5: Commercial Pipeline Dependency Ratio                                                                                       |
|  * Rule 6: Committed Revenue Mix across Forward Book                                                                                  |
|  * Rule 7: Aggregate Delivery Forecast Risk Rating                                                                                    |
|  * Rule 8: Comprehensive Practice Forward Market Stance                                                                               |
|  * Rule 9: Absolute Forecast Headroom Buffer Status                                                                                   |
+---------------------------------------------------|-----------------------------------------------------------------------------------+
                                                    |
                                                    v
+---------------------------------------------------------------------------------------------------------------------------------------+
|                                                 STEP 4: ACTION RECOMMENDATION ENGINE                                                  |
|                                                                                                                                       |
|  Maps Operational Shortfalls to 10 Prioritized Action Items with Quantified Financial Impact (INR):                                  |
|  * Priority 1 [HIGH]   : Partner Revenue Recovery Mobilization     (Impact: abs(budget_gap))                                          |
|  * Priority 2 [HIGH]   : Forecast Protection & SOW Lock-in         (Impact: abs(forecast_gap))                                        |
|  * Priority 3 [HIGH]   : Pipeline Origination Surge                (Impact: budget - forward_revenue)                                 |
|  * Priority 4 [MEDIUM] : Forward Coverage Buffer Preservation      (Impact: forward_revenue - budget)                                 |
|  * Priority 5 [HIGH]   : Executive Closing Surge on Qualified Deals(Impact: weighted_pipeline)                                        |
|  * Priority 6 [MEDIUM] : Stage-Gate Proposal Velocity Acceleration (Impact: weighted_pipeline)                                        |
|  * Priority 7 [HIGH]   : Fast-Track MSA/SOW Legal Review           (Impact: forecast - backlog)                                       |
|  * Priority 8 [MEDIUM] : Backlog Hardening via Milestone Sign-off  (Impact: forecast - backlog)                                       |
|  * Priority 9 [HIGH]   : Portfolio Deliverable Slippage Audit      (Impact: forecast_revenue)                                         |
|  * Priority 10 [LOW]   : Premium-Rate Margin Optimization          (Impact: forecast_gap)                                             |
+---------------------------------------------------------------------------------------------------------------------------------------+
```

---

## 5. Summary Reference Tables

### Core Financial Telemetry Formulas

| Metric Identifier | Mathematical Formula | Target Benchmark | Strategic Purpose |
|:------------------|:---------------------|:----------------:|:------------------|
| **Actual Revenue** | `SUM(project_actuals.actual_revenue)` | `>= Budget Target` | Recognized delivery fees to date |
| **Budget Target** | `SUM(budgets.revenue_budget)` | Operating Baseline | Annual operating plan revenue target |
| **Committed Backlog** | `SUM(pipeline_value) [In Delivery, Closed Won]` | Maximum | Contractually locked engagement value |
| **Weighted Pipeline** | `SUM(pipeline_value * win_probability)` | Conversion Dependent | Probability-weighted open proposal value |
| **Gross Forecast** | `Committed Backlog + Weighted Pipeline + Util Adj` | N/A | Total unadjusted projected revenue |
| **Risk Haircut** | `Gross Forecast * 0.05` | 5.0% Haircut | Execution slippage contingency buffer |
| **Net Forecast** | `Gross Forecast - Risk Haircut` | `>= Budget Target` | Risk-adjusted deliverable forecast |
| **Forecast Headroom** | `Net Forecast - Budget Target` | `> 0.0` | Net buffer above operating target |
| **Forward Coverage** | `((Backlog + Weighted Pipeline) / Budget) * 100` | `>= 120.0%` | Multiple of forward book relative to budget |
| **Pipeline Dependency** | `(Weighted Pipeline / Forward Revenue) * 100` | `<= 40.0%` | Vulnerability of forward plan to deal losses |

### Practice Health Classification Boundaries

| Health Dimension | Healthy (Green) | Watch (Amber) | Critical Action (Red) |
|:-----------------|:---------------:|:-------------:|:---------------------:|
| **Forecast Risk** | Committed Coverage `>= 70%` | `50% <= Coverage < 70%` | Committed Coverage `< 50%` |
| **Pipeline Risk** | Pipeline Dependency `<= 30%` | `30% < Dependency <= 50%` | Pipeline Dependency `> 50%` |
| **Forward Position** | Forward Coverage `>= 120%` | `100% <= Coverage < 120%` | Forward Coverage `< 100%` |
| **Headroom Buffer** | Headroom `% >= 10.0%` | `0.0% <= Headroom % < 10.0%` | Headroom `% < 0.0%` |
| **Revenue Realization**| Budget Gap `>= 0.0` | `-10.0% <= Budget Gap % < 0.0%`| Budget Gap `% < -10.0%` |

