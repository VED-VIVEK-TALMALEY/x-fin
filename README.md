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

    subgraph S_ENGINES["2. MULTI-ENGINE FINANCIAL PROCESSING TIER"]
        direction TB
        E_FC["<b>Forecast Engine</b><br/>Deterministic 5-step model with 5% haircut"]
        E_MC["<b>Monte Carlo Engine</b><br/>5,000-iteration stochastic distribution (P10/P50/P90)"]
        E_RSK["<b>Risk & Leakage Engines</b><br/>Headroom, margin erosion, portfolio concentration"]
        E_STF["<b>Staffing & Utilization Engine</b><br/>Capacity checks & data quality guardrails"]
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
    style E_RSK fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87
    style E_STF fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87
    style E_INT fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87

    style O_DASH fill:#D1FAE5,stroke:#047857,stroke-width:1px,color:#064E3B
    style O_API fill:#D1FAE5,stroke:#047857,stroke-width:1px,color:#064E3B
    style O_BRIEF fill:#D1FAE5,stroke:#047857,stroke-width:1px,color:#064E3B
```

---

## Core Financial Pillars & Executive KPI Definitions

| Pillar | Metric Name | Mathematical Definition | Target Benchmark | Strategic & Operating Purpose |
|:-------|:------------|:------------------------|:----------------:|:------------------------------|
| **Revenue** | **Actual Revenue** | $\sum \text{project\_actuals.actual\_revenue}$ | $\ge \text{Budget Target}$ | Recognized delivery fees to date across billing cycles |
| **Revenue** | **Revenue Budget** | $\sum \text{budgets.revenue\_budget}$ | Plan Baseline | Approved annual/quarterly operating plan revenue target |
| **Forecast** | **Net Forecast Revenue** | $\text{Gross Forecast} \times (1 - 0.05)$ | $\ge \text{Budget Target}$ | Primary deliverable forecast after 5% execution risk haircut |
| **Forecast** | **Forecast Headroom** | $\text{Net Forecast} - \text{Budget Target}$ | $> 0$ (Surplus) | Absolute buffer above baseline plan (negative = budget deficit) |
| **Coverage** | **Forward Coverage** | $\frac{\text{Backlog}_{\text{committed}} + \text{Pipeline}_{\text{weighted}}}{\text{Budget}} \times 100$ | $\ge 120.0\%$ | Total forward book depth supporting target attainment |
| **Quality** | **Committed Revenue Mix** | $\frac{\text{Backlog}_{\text{committed}}}{\text{Forward Revenue}} \times 100$ | $\ge 60.0\%$ | Share of forward plan secured by executed SOWs/contracts |
| **Risk** | **Pipeline Dependency** | $\frac{\text{Pipeline}_{\text{weighted}}}{\text{Forward Revenue}} \times 100$ | $\le 40.0\%$ | Vulnerability of forward plan to commercial conversion slippage |
| **Staffing** | **Consultant Utilization** | $\frac{\text{Billable Delivered Hours}}{\text{Available Capacity Hours}} \times 100$ | $75.0\%$ Baseline | Billable staffing efficiency vs target operational capacity |
| **Stochastic**| **P50 Expected Value** | 50th Percentile of 5,000 Monte Carlo Iterations | $\approx \text{Net Forecast}$ | Median probabilistic outcome under stochastic volatility |
| **Stochastic**| **Value-at-Risk (VaR P10)** | $\text{Deterministic Forecast} - \text{P10 Outcome}$ | Minimize | Quantified downside revenue exposure under adverse market conditions |

---

## End-to-End System Architecture

```mermaid
graph TB
    subgraph Client["CLIENT INTERFACE"]
        BROWSER["Web Browser / Executive User"]
    end

    subgraph Presentation["PRESENTATION TIER (Streamlit :8501)"]
        UI_MAIN["<b>dashboard/app.py</b><br/>• Executive Performance Overview & KPI Banner<br/>• Waterfall & Monte Carlo Confidence Charts<br/>• Risk Driver & Staffing Capacity View<br/>• BU Margins Heatmap & Historical Accuracy<br/>• Interactive Scenario Sensitivity Planners"]
        UI_INTEL["<b>dashboard/intelligence.py</b><br/>• Strategic Positioning Diagnostics<br/>• 9 Diagnostic Insight Cards<br/>• 10 Actionable Remediation Cards<br/>• Staffing Data-Quality Validation"]
        UI_CHARTS["<b>dashboard/charts.py</b> (Themed Plotly Builders)"]
        UI_API["<b>dashboard/api.py</b> (Requests Client with 10s Timeout)"]
        UI_MAIN & UI_INTEL --> UI_CHARTS
        UI_MAIN & UI_INTEL --> UI_API
    end

    subgraph Gateway["API GATEWAY TIER (FastAPI :8000)"]
        APP["<b>app/main.py</b> (FastAPI ASGI Factory)"]
        subgraph Routers["FastAPI Route Handlers"]
            R_FC["/forecast/current"]
            R_AN["/analytics/* (/summary, /monthly-revenue, /backlog, /variance, /forecast-accuracy, /business-units)"]
            R_IN["/intelligence/* (/health, /overview)"]
            R_EX["/executive/* (/health, /briefing)"]
            R_DC["/decisions/overview"]
            R_SC["/scenarios/run"]
            R_PR["/projects"]
        end
        APP --> Routers
    end

    subgraph Services["SERVICE & BUSINESS LOGIC TIER (app/services)"]
        direction TB
        S_FC["<b>forecast_engine.py</b><br/>5-Step Deterministic Model"]
        S_DEC["<b>forecast_decomposition.py</b><br/>Bridge Decomposition"]
        S_MC["<b>monte_carlo_engine.py</b><br/>5,000 Iteration Simulation"]
        S_BL["<b>backlog_engine.py</b><br/>Backlog Waterfall & Stages"]
        S_VR["<b>variance_engine.py</b><br/>Variance Bridge & Gap Analysis"]
        S_RS["<b>finance_reasoning.py</b><br/>20+ Operating Ratios"]
        S_IN["<b>insight_engine.py</b><br/>9 Severity Diagnostic Rules"]
        S_RC["<b>recommendation_engine.py</b><br/>10 Prescriptive Action Rules"]
        S_STF["<b>staffing_engine.py</b><br/>Staffing Capacity & Utilization"]
        S_RSK["<b>risk_engine.py & margin_risk_engine.py</b><br/>Portfolio & Revenue Leakage"]
        S_BU["<b>business_unit_engine.py</b><br/>Practice Aggregations"]
        S_SC["<b>scenario_engine.py</b><br/>What-If Sensitivity Simulation"]
    end

    subgraph Data["DATA PERSISTENCE TIER"]
        DB_CONN["<b>app/db/connection.py</b><br/>SQLAlchemy Engine (PostgreSQL 14+ with SQLite Fallback)"]
        subgraph Tables["Relational Database Tables"]
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

    BROWSER --> Presentation
    UI_API -->|HTTP REST JSON| Gateway
    Routers --> Services
    Services --> DB_CONN

    style Client fill:#F1F5F9,stroke:#475569,stroke-width:2px,color:#0F172A
    style Presentation fill:#EFF6FF,stroke:#2563EB,stroke-width:2px,color:#1E40AF
    style Gateway fill:#F0FDF4,stroke:#16A34A,stroke-width:2px,color:#15803D
    style Services fill:#FAF5FF,stroke:#9333EA,stroke-width:2px,color:#6B21A8
    style Data fill:#F8FAFC,stroke:#334155,stroke-width:2px,color:#1E293B

    style BROWSER fill:#E2E8F0,stroke:#475569,stroke-width:1px,color:#0F172A
    style UI_MAIN fill:#DBEAFE,stroke:#1D4ED8,stroke-width:1px,color:#1E3A8A
    style UI_INTEL fill:#DBEAFE,stroke:#1D4ED8,stroke-width:1px,color:#1E3A8A
    style UI_CHARTS fill:#BFDBFE,stroke:#1D4ED8,stroke-width:1px,color:#1E3A8A
    style UI_API fill:#93C5FD,stroke:#1D4ED8,stroke-width:1px,color:#1E3A8A

    style APP fill:#DCFCE7,stroke:#15803D,stroke-width:1px,color:#166534
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
    style S_RSK fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87
    style S_BU fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87
    style S_SC fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87

    style DB_CONN fill:#E2E8F0,stroke:#475569,stroke-width:1px,color:#1E293B
    style Tables fill:#CBD5E1,stroke:#475569,stroke-width:1px,color:#1E293B
```

---

## Deterministic Forecast Engine (5-Step Formulation)

The forecast engine (`app/services/forecast_engine.py`) models delivery revenue deterministically through a 5-step formulation:

```mermaid
flowchart TD
    subgraph ST1["STEP 1: INGESTION & UTILIZATION FACTOR"]
        I_CB["<b>Committed Backlog ($B_{comm}$)</b><br/>SUM(pipeline_value) for 'In Delivery' + 'Closed Won'"]
        I_WP["<b>Weighted Pipeline ($P_{wt}$)</b><br/>SUM(pipeline_value * win_probability)"]
        I_UT["<b>Actual Utilization ($U_{act}$)</b><br/>Current delivered billable staffing rate"]
        I_TU["<b>Target Utilization ($U_{tgt}$)</b><br/>Fixed practice benchmark = 0.75 (75%)"]

        F_FAC["<b>Utilization Factor ($F_{util}$)</b><br/><code>factor = actual_utilization / 0.75</code>"]
        I_UT & I_TU --> F_FAC
    end

    subgraph ST2["STEP 2: UTILIZATION ADJUSTMENT"]
        F_ADJ["<b>Utilization Adjustment ($A_{util}$)</b><br/><code>adj_util = committed_backlog * (factor - 1.0)</code><br/><i>(Over-utilization = revenue upside; Under-utilization = capacity drag)</i>"]
        I_CB & F_FAC --> F_ADJ
    end

    subgraph ST3["STEP 3: GROSS FORECAST SYNTHESIS"]
        F_GROSS["<b>Gross Forecast ($R_{gross}$)</b><br/><code>gross_forecast = committed_backlog + weighted_pipeline + adj_util</code>"]
        I_CB & I_WP & F_ADJ --> F_GROSS
    end

    subgraph ST4["STEP 4: EXECUTION RISK HAIRCUT"]
        F_RISK["<b>Risk Adjustment ($A_{risk}$)</b><br/><code>adj_risk = gross_forecast * 0.05</code><br/><i>(Standard 5% delivery execution haircut)</i>"]
        F_GROSS --> F_RISK
    end

    subgraph ST5["STEP 5: NET DELIVERABLE FORECAST"]
        F_NET["<b>Net Forecast Revenue ($R_{net}$)</b><br/><code>forecast_revenue = round(gross_forecast - adj_risk, 2)</code>"]
        F_GROSS & F_RISK --> F_NET
    end

    ST1 --> ST2 --> ST3 --> ST4 --> ST5

    style ST1 fill:#EFF6FF,stroke:#2563EB,stroke-width:2px,color:#1E40AF
    style ST2 fill:#FDF4FF,stroke:#C026D3,stroke-width:2px,color:#86198F
    style ST3 fill:#FAF5FF,stroke:#9333EA,stroke-width:2px,color:#6B21A8
    style ST4 fill:#FEF2F2,stroke:#DC2626,stroke-width:2px,color:#991B1B
    style ST5 fill:#ECFDF5,stroke:#059669,stroke-width:2px,color:#065F46

    style I_CB fill:#DBEAFE,stroke:#1D4ED8,stroke-width:1px,color:#1E3A8A
    style I_WP fill:#DBEAFE,stroke:#1D4ED8,stroke-width:1px,color:#1E3A8A
    style I_UT fill:#DBEAFE,stroke:#1D4ED8,stroke-width:1px,color:#1E3A8A
    style I_TU fill:#DBEAFE,stroke:#1D4ED8,stroke-width:1px,color:#1E3A8A
    style F_FAC fill:#BFDBFE,stroke:#1D4ED8,stroke-width:1px,color:#1E3A8A

    style F_ADJ fill:#F5D0FE,stroke:#A21CAF,stroke-width:1px,color:#701A75
    style F_GROSS fill:#E9D5FF,stroke:#7E22CE,stroke-width:1px,color:#581C87
    style F_RISK fill:#FECACA,stroke:#B91C1C,stroke-width:1px,color:#7F1D1D
    style F_NET fill:#A7F3D0,stroke:#047857,stroke-width:2px,color:#064E3B
```

### Deterministic Calculation Trace Matrix

| Step | Engine Component | Mathematical Equation | Sample Input Value | Resulting Output Value |
|:----:|:-----------------|:----------------------|:-------------------|:----------------------|
| **1** | Committed Backlog | $\sum \text{Value}_{\text{Signed/In-Delivery}}$ | Baseline Ingestion | INR 100,000.00 |
| **2** | Weighted Pipeline | $\sum (\text{Value} \times \text{Prob})$ | Baseline Ingestion | INR 50,000.00 |
| **3** | Utilization Adjustment | $\text{Backlog} \times \left(\frac{U_{\text{act}}}{0.75} - 1.0\right)$ | $U_{\text{act}} = 75.0\%$ | INR 0.00 |
| **4** | Gross Forecast | $\text{Backlog} + \text{Pipeline} + \text{Adj}_{\text{util}}$ | $100,000 + 50,000 + 0$ | INR 150,000.00 |
| **5** | Execution Haircut (5%) | $\text{Gross Forecast} \times 0.05$ | $150,000 \times 0.05$ | INR -7,500.00 |
| **6** | **Net Deliverable Forecast** | $\mathbf{\text{Gross Forecast} - \text{Haircut}}$ | **$150,000 - 7,500$** | **INR 142,500.00** |

---

## Monte Carlo Stochastic Simulation Engine

In addition to deterministic calculations, `app/services/monte_carlo_engine.py` executes a **5,000-iteration Monte Carlo simulation** to quantify uncertainty across pipeline conversion, utilization variance, and deliverable slippage:

```mermaid
flowchart LR
    subgraph PARAMS["Stochastic Distributions"]
        P_CONV["<b>Pipeline Conversion</b><br/>Beta Distribution<br/>Mean = Win Prob"]
        P_UTIL["<b>Utilization Shock</b><br/>Normal Distribution<br/>$\mu = 0, \sigma = 0.04$"]
        P_SLIP["<b>Delivery Slippage</b><br/>Log-Normal Distribution<br/>Range: 0% to 15%"]
    end

    subgraph SIM["5,000 Iteration Loop (Seed = 42)"]
        S_ITER["Generate 5,000 synthetic outcomes for gross revenue, haircuts, and net revenue"]
    end

    subgraph METRICS["Quantile Outputs & VaR"]
        Q10["<b>P10 (Downside)</b><br/>Conservative 90% confidence lower bound"]
        Q50["<b>P50 (Median)</b><br/>Stochastic expected baseline"]
        Q90["<b>P90 (Upside)</b><br/>Optimistic conversion trajectory"]
        VAR["<b>Value-at-Risk (VaR)</b><br/>$\text{Deterministic} - \text{P10}$"]
    end

    PARAMS --> SIM --> METRICS

    style PARAMS fill:#EFF6FF,stroke:#2563EB,stroke-width:2px,color:#1E40AF
    style SIM fill:#FAF5FF,stroke:#9333EA,stroke-width:2px,color:#6B21A8
    style METRICS fill:#ECFDF5,stroke:#059669,stroke-width:2px,color:#065F46

    style P_CONV fill:#DBEAFE,stroke:#1D4ED8,stroke-width:1px,color:#1E3A8A
    style P_UTIL fill:#DBEAFE,stroke:#1D4ED8,stroke-width:1px,color:#1E3A8A
    style P_SLIP fill:#DBEAFE,stroke:#1D4ED8,stroke-width:1px,color:#1E3A8A

    style S_ITER fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87

    style Q10 fill:#FEE2E2,stroke:#DC2626,stroke-width:1px,color:#991B1B
    style Q50 fill:#DBEAFE,stroke:#1D4ED8,stroke-width:1px,color:#1E3A8A
    style Q90 fill:#DCFCE7,stroke:#15803D,stroke-width:1px,color:#166534
    style VAR fill:#FEF3C7,stroke:#D97706,stroke-width:1px,color:#92400E
```

### Monte Carlo Confidence Band Interpretation

| Quantile Metric | Statistical Confidence | Strategic Interpretation | Leadership Decision Trigger |
|:----------------|:----------------------:|:-------------------------|:----------------------------|
| **P10 (Downside)** | $90\%$ Confidence Lower Bound | Minimum revenue expected even if deals slip and utilization softens | Establish baseline cost controls & staffing floor |
| **P50 (Median)** | $50\%$ Percentile Outcome | Central tendency of stochastic revenue realization | Primary comparison point for deterministic forecast |
| **P90 (Upside)** | $10\%$ Probability Exceedance | High-conversion scenario where major proposals close early | Reserve commercial bandwidth and contractor pool |
| **Confidence Band Width** | $(P90 - P10) / P50$ | Measurement of practice revenue volatility and uncertainty | $> 25\%$ implies elevated forward forecast instability |

---

## Intelligence & Financial Reasoning Engine

`app/services/finance_reasoning.py` and `app/services/intelligence_engine.py` derive 20+ financial telemetry indicators to classify practice health:

```mermaid
flowchart TD
    subgraph IN["FINANCIAL TELEMETRY"]
        T1["actual_revenue"]
        T2["budget_revenue"]
        T3["forecast_revenue"]
        T4["committed_backlog"]
        T5["weighted_pipeline"]
    end

    subgraph R1["1. VARIANCE & TRAJECTORY"]
        V1["<b>budget_gap</b> = actual_revenue - budget_revenue"]
        V2["<b>budget_gap_pct</b> = (budget_gap / budget_revenue) * 100"]
        V3["<b>forecast_gap</b> = forecast_revenue - budget_revenue"]
        V4["<b>forecast_gap_pct</b> = (forecast_gap / budget_revenue) * 100"]
    end

    subgraph R2["2. COVERAGE & REVENUE COMPOSITION"]
        C1["<b>forward_revenue</b> = committed_backlog + weighted_pipeline"]
        C2["<b>forward_coverage</b> = (forward_revenue / budget_revenue) * 100"]
        C3["<b>committed_forecast_coverage</b> = (committed_backlog / forecast_revenue) * 100"]
        C4["<b>committed_revenue_mix</b> = (committed_backlog / forward_revenue) * 100"]
        C5["<b>pipeline_dependency</b> = (weighted_pipeline / forward_revenue) * 100"]
    end

    subgraph R3["3. HEALTH CLASSIFICATION ENGINE"]
        H1["<b>forecast_risk</b>: 'low' (>=70%), 'moderate' (50-69%), 'high' (<50%)"]
        H2["<b>pipeline_risk</b>: 'low' (<=30%), 'moderate' (31-50%), 'high' (>50%)"]
        H3["<b>forward_position</b>: 'strong' (>=120%), 'adequate' (100-119%), 'watch' (80-99%), 'weak' (<80%)"]
        H4["<b>headroom_status</b>: 'strong' (>=10%), 'moderate' (0-9.9%), 'deficit' (<0%)"]
    end

    IN --> R1 --> R2 --> R3

    style IN fill:#F8FAFC,stroke:#475569,stroke-width:2px,color:#1E293B
    style R1 fill:#EFF6FF,stroke:#2563EB,stroke-width:2px,color:#1E40AF
    style R2 fill:#FAF5FF,stroke:#9333EA,stroke-width:2px,color:#6B21A8
    style R3 fill:#ECFDF5,stroke:#059669,stroke-width:2px,color:#065F46

    style T1 fill:#E2E8F0,stroke:#334155,stroke-width:1px,color:#0F172A
    style T2 fill:#E2E8F0,stroke:#334155,stroke-width:1px,color:#0F172A
    style T3 fill:#E2E8F0,stroke:#334155,stroke-width:1px,color:#0F172A
    style T4 fill:#E2E8F0,stroke:#334155,stroke-width:1px,color:#0F172A
    style T5 fill:#E2E8F0,stroke:#334155,stroke-width:1px,color:#0F172A

    style V1 fill:#DBEAFE,stroke:#1D4ED8,stroke-width:1px,color:#1E3A8A
    style V2 fill:#DBEAFE,stroke:#1D4ED8,stroke-width:1px,color:#1E3A8A
    style V3 fill:#DBEAFE,stroke:#1D4ED8,stroke-width:1px,color:#1E3A8A
    style V4 fill:#DBEAFE,stroke:#1D4ED8,stroke-width:1px,color:#1E3A8A

    style C1 fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87
    style C2 fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87
    style C3 fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87
    style C4 fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87
    style C5 fill:#F3E8FF,stroke:#7E22CE,stroke-width:1px,color:#581C87

    style H1 fill:#D1FAE5,stroke:#047857,stroke-width:1px,color:#064E3B
    style H2 fill:#D1FAE5,stroke:#047857,stroke-width:1px,color:#064E3B
    style H3 fill:#D1FAE5,stroke:#047857,stroke-width:1px,color:#064E3B
    style H4 fill:#D1FAE5,stroke:#047857,stroke-width:1px,color:#064E3B
```

---

## Practice Lead Diagnostic Matrix (9 Evaluators)

`app/services/insight_engine.py` evaluates 9 heuristic severity rules to surface operational vulnerabilities:

| # | Diagnostic Dimension | Telemetry Metric | [HIGH] Severity Condition | [MEDIUM] Severity Condition | [LOW] Severity Condition | Management Action |
|:--:|:---------------------|:-----------------|:--------------------------|:----------------------------|:-------------------------|:------------------|
| **1** | Revenue Performance | `budget_gap_pct` | $\le -10.0\%$ | $-10.0\% < \text{gap} < 0.0\%$ | $\ge 0.0\%$ | Audit billable hours recognition & scope creep on active cases |
| **2** | Forecast Trajectory | `forecast_gap_pct` | $\le -10.0\%$ | $-10.0\% < \text{gap} < 0.0\%$ | $\ge 0.0\%$ | Mobilize partner commercial bandwidth to accelerate deals |
| **3** | Forward Coverage | `forward_coverage` | $< 100.0\%$ | $100.0\% \le \text{cov} < 120.0\%$ | $\ge 120.0\%$ | Originate new proposals in tier-1 client accounts |
| **4** | Forecast Quality | `committed_forecast_coverage` | $< 50.0\%$ | $50.0\% \le \text{cov} < 70.0\%$ | $\ge 70.0\%$ | Expedite client execution of pending Statements of Work (SOWs) |
| **5** | Pipeline Dependency | `pipeline_dependency` | $\ge 60.0\%$ | $40.0\% \le \text{dep} < 60.0\%$ | $< 40.0\%$ | Mitigate risk by securing firm commitments on top 3 opportunities |
| **6** | Committed Revenue Mix| `committed_revenue_mix` | $< 40.0\%$ | $40.0\% \le \text{mix} < 60.0\%$ | $\ge 60.0\%$ | Convert verbal client confirmations into binding commitments |
| **7** | Forecast Risk Profile| `forecast_risk` | $== \text{"high"}$ | $== \text{"moderate"}$ | $== \text{"low"}$ | Institute weekly milestone health checks with delivery leads |
| **8** | Market Stance | `forward_position` | $\in \{\text{"watch"}, \text{"weak"}\}$ | $== \text{"adequate"}$ | $== \text{"strong"}$ | Align practice hiring and bench models with pipeline demand |
| **9** | Headroom Buffer | `forecast_headroom` | $< 0.0$ | — | $> 0.0$ | Allocate partner commercial capacity to bridge revenue deficit |

---

## Action Recommendation Engine (10 Rules + Staffing Remediations)

`app/services/recommendation_engine.py` converts diagnostic deficits into prioritized operational remediation playbooks:

```mermaid
flowchart TD
    subgraph TRIG["RULE ACTIVATION LAYER"]
        R1["budget_gap < 0"]
        R2["forecast_gap < 0"]
        R3["forward_coverage < 100%"]
        R4["100% <= forward_coverage < 120%"]
        R5["pipeline_dependency >= 60%"]
        R6["40% <= pipeline_dependency < 60%"]
        R7["committed_forecast_coverage < 50%"]
        R8["50% <= committed_forecast_coverage < 70%"]
        R9["forecast_risk == 'high'"]
        R10["forward_coverage >= 120% & pipeline < 60%"]
    end

    subgraph ACT["PRESCRIPTIVE ACTIONS & FINANCIAL IMPACT"]
        A1["<b>[HIGH] Partner Revenue Recovery</b><br/>Impact: abs(budget_gap)"]
        A2["<b>[HIGH] Forecast Protection Plan</b><br/>Impact: abs(forecast_gap)"]
        A3["<b>[HIGH] Fast-Track Proposal Origination</b><br/>Impact: budget - forward_revenue"]
        A4["<b>[MEDIUM] Coverage Buffer Maintenance</b><br/>Impact: forward_revenue - budget"]
        A5["<b>[HIGH] Executive Closing Surge</b><br/>Impact: weighted_pipeline"]
        A6["<b>[MEDIUM] Stage-Gate Velocity Review</b><br/>Impact: weighted_pipeline"]
        A7["<b>[HIGH] MSA & SOW Legal Hardening</b><br/>Impact: forecast - backlog"]
        A8["<b>[MEDIUM] Milestone Deliverable Sign-Off</b><br/>Impact: forecast - backlog"]
        A9["<b>[HIGH] Portfolio Slippage Audit</b><br/>Impact: forecast_revenue"]
        A10["<b>[LOW] Premium Margin Optimization</b><br/>Impact: forecast_gap"]
    end

    R1 --> A1
    R2 --> A2
    R3 --> A3
    R4 --> A4
    R5 --> A5
    R6 --> A6
    R7 --> A7
    R8 --> A8
    R9 --> A9
    R10 --> A10

    style TRIG fill:#EFF6FF,stroke:#2563EB,stroke-width:2px,color:#1E40AF
    style ACT fill:#ECFDF5,stroke:#059669,stroke-width:2px,color:#065F46
```

### Action Recommendation Catalog

| Priority | Strategy Domain | Activation Condition | Prescriptive Action Item | Quantified Financial Impact (INR) |
|:---------|:----------------|:---------------------|:-------------------------|:----------------------------------|
| **[HIGH]** | Revenue Recovery | `budget_gap < 0` | Mobilize partner-led revenue recovery plan on lagging accounts | $\text{abs}(\text{budget\_gap})$ |
| **[HIGH]** | Forecast Protection | `forecast_gap < 0` | Lock in pending contract extensions and prevent scope reduction | $\text{abs}(\text{forecast\_gap})$ |
| **[HIGH]** | Pipeline Coverage | `forward_coverage < 100%` | Fast-track high-probability proposals to achieve baseline budget | $\text{budget} - \text{forward\_revenue}$ |
| **[MEDIUM]** | Coverage Buffer | `100% <= forward_coverage < 120%` | Maintain commercial business development momentum | $\text{forward\_revenue} - \text{budget}$ |
| **[HIGH]** | Deal Closure Surge | `pipeline_dependency >= 60%` | Conduct executive closing sessions on all deals in Qualified stage | $\text{weighted\_pipeline}$ |
| **[MEDIUM]** | Velocity Management| `40% <= pipeline_dependency < 60%` | Review stage-gate progression weekly with client teams | $\text{weighted\_pipeline}$ |
| **[HIGH]** | Backlog Fortification| `committed_forecast_coverage < 50%`| Prioritize execution of MSAs and SOWs under legal review | $\text{forecast} - \text{backlog}$ |
| **[MEDIUM]** | Backlog Hardening | `50% <= committed_forecast_coverage < 70%`| Expedite client milestone deliverable acceptances | $\text{forecast} - \text{backlog}$ |
| **[HIGH]** | Delivery Audit | `forecast_risk == "high"` | Conduct portfolio-wide review to prevent deliverable slippage | $\text{forecast\_revenue}$ |
| **[LOW]** | Margin Optimization| `forward_coverage >= 120%` & `pipeline < 60%`| Prioritize higher-margin, premium-rate engagements | $\text{forecast\_gap}$ |

---

## Engagement Lifecycle & Backlog Transition Model

```mermaid
stateDiagram-v2
    [*] --> Prospect : Win Probability = 15%
    Prospect --> Qualified : Win Probability = 35%
    Qualified --> In_Delivery : Win Probability = 75%
    Qualified --> Closed_Lost : Win Probability = 0%
    In_Delivery --> Closed_Won : Win Probability = 100%
    In_Delivery --> Closed_Lost : Win Probability = 0%

    note right of Prospect
        <b>UNCOMMITTED PIPELINE</b>
        • Stage: Prospect
        • Backlog Category: Uncommitted (15%)
    end note

    note right of Qualified
        <b>UNCOMMITTED PIPELINE</b>
        • Stage: Qualified
        • Backlog Category: Uncommitted (35%)
    end note

    note right of In_Delivery
        <b>COMMITTED BACKLOG</b>
        • Stage: In Delivery
        • Backlog Category: Committed (75%)
    end note

    note right of Closed_Won
        <b>COMMITTED BACKLOG</b>
        • Stage: Closed Won
        • Backlog Category: Committed (100%)
    end note
```

---

## Database Architecture & Relational Schema

```mermaid
erDiagram
    BUSINESS_UNITS ||--o{ PROJECTS : manages
    BUSINESS_UNITS ||--o{ BUDGETS : targets
    PROJECTS ||--o{ PROJECT_PIPELINE : snapshots
    PROJECTS ||--o{ PROJECT_ACTUALS : recognizes
    FORECAST_VERSIONS ||--o{ FORECAST_VALUES : records

    BUSINESS_UNITS {
        int id PK
        string name "X Build, X Design, Digital Ventures"
        string code UK "XB, XD, DV"
        timestamp created_at
    }

    PROJECTS {
        int id PK
        int business_unit_id FK
        string name
        string client
        string stage "Prospect, Qualified, In Delivery, Closed Won, Closed Lost"
        numeric total_contract_value
        numeric billing_rate
        int planned_hours
        date start_date
        date end_date
    }

    PROJECT_PIPELINE {
        int id PK
        int project_id FK
        date snapshot_date
        string stage
        numeric pipeline_value
        numeric win_probability "0.00 to 1.00"
        numeric weighted_value
    }

    PROJECT_ACTUALS {
        int id PK
        int project_id FK
        date month "YYYY-MM-01"
        int actual_hours
        numeric actual_revenue
        numeric actual_cost
    }

    BUDGETS {
        int id PK
        int business_unit_id FK
        date month "YYYY-MM-01"
        numeric revenue_budget
        int hours_budget
        numeric utilization_budget "0.75 Baseline"
    }

    FORECAST_VERSIONS {
        int id PK
        string version_name
        timestamp created_at
        string methodology
    }

    FORECAST_VALUES {
        int id PK
        int version_id FK
        int project_id FK
        date month
        numeric forecasted_revenue
    }
```

---

## Complete API Route Specifications

| HTTP Method | Route Endpoint | Response Schema | Service Module & Function | Purpose & Description |
|:-----------:|:---------------|:----------------|:--------------------------|:----------------------|
| `GET` | `/` | `Dict[str, str]` | `app.main:root` | Service name, version, health status |
| `GET` | `/health` | `HealthStatus` | `app.main:health` | Application health probe |
| `GET` | `/health/db` | `Dict[str, str]` | `app.main:database_health` | Database connection test probe |
| `GET` | `/forecast/current` | `ForecastResponse` | `forecast_engine.build_forecast()` | Current period forecast with backlog & pipeline split |
| `GET` | `/analytics/summary` | `FinanceSummary` | `finance_queries.get_finance_summary()` | Aggregated actuals, budgets, and backlog overview |
| `GET` | `/analytics/monthly-revenue` | `List[MonthlyRevenue]` | `finance_queries.get_monthly_revenue()` | Historical monthly recognized revenue, hours, cost |
| `GET` | `/analytics/backlog` | `BacklogResponse` | `backlog_engine.calculate_backlog()` | Committed vs uncommitted backlog and waterfall |
| `GET` | `/analytics/variance` | `VarianceResult` | `variance_engine.calculate_variance()` | Actual vs budget and forecast vs budget bridges |
| `GET` | `/analytics/forecast-accuracy`| `List[AccuracyItem]` | `forecast_accuracy.get_forecast_accuracy()` | Month-by-month historical forecast accuracy series |
| `GET` | `/analytics/business-units` | `List[BUPerformance]` | `business_unit_engine.get_bu_performance()` | Practice-level revenue, margin, and hours breakdown |
| `GET` | `/intelligence/health` | `HealthStatus` | `routers.intelligence:health` | Intelligence subsystem health check |
| `GET` | `/intelligence/overview` | `IntelligencePackage` | `intelligence_engine.build_intelligence_overview()` | Canonical 360° financial intelligence bundle |
| `GET` | `/executive/briefing` | `Dict[str, Any]` | `executive_briefing_engine.build_executive_briefing()` | Synthesized executive briefing with decision summary |
| `GET` | `/decisions/overview` | `Dict[str, Any]` | `decision_engine.generate_decisions()` | Standardized decision triggers and recommendations |
| `POST` | `/scenarios/run` | `ScenarioResult` | `scenario_engine.run_scenario()` | Multi-variable what-if revenue simulation |
| `GET` | `/projects` | `List[Dict[str, Any]]` | `routers.projects:get_projects` | Project directory with stage and contract metadata |

---

## Scenario Simulation Engine

`app/services/scenario_engine.py` simulates sensitivity to commercial conversion, utilization, billing rates, and delivery slippage:

```mermaid
flowchart LR
    subgraph Inputs["1. SCENARIO INPUTS"]
        B["Base Revenue ($R_{base}$)"]
        P["Pipeline Revenue ($R_{pipe}$)"]
        U["Utilization ($U_{base}$)"]
        C_CHG["Conversion Delta ($\Delta_{conv}$)"]
        U_CHG["Utilization Delta ($\Delta_{util}$)"]
        R_CHG["Billing Rate Delta ($\Delta_{rate}$)"]
        S_CHG["Slippage Rate ($S_{slip}$)"]
    end

    subgraph Adjustments["2. PARAMETRIC ADJUSTMENTS"]
        P_ADJ["Adjusted Pipeline<br/><code>= R_pipe * (1 + delta_conv)</code>"]
        U_FAC["Utilization Factor<br/><code>= (U_base + delta_util) / U_base</code>"]
        B_ADJ["Adjusted Delivery Base<br/><code>= R_base * U_fac * (1 + delta_rate)</code>"]
        P & C_CHG --> P_ADJ
        U & U_CHG --> U_FAC
        B & U_FAC & R_CHG --> B_ADJ
    end

    subgraph Output["3. OUTPUT SYNTHESIS"]
        COMB["Pre-Slippage Revenue<br/><code>= base_adj + pipeline_adj</code>"]
        SCEN["Scenario Revenue<br/><code>= combined * (1 - slippage_rate)</code>"]
        DELT["Revenue Delta & %<br/><code>= scenario_revenue - base_revenue</code>"]

        P_ADJ & B_ADJ --> COMB
        COMB & S_CHG --> SCEN
        SCEN & B --> DELT
    end

    style Inputs fill:#F8FAFC,stroke:#475569,stroke-width:2px,color:#1E293B
    style Adjustments fill:#FFFBEB,stroke:#D97706,stroke-width:2px,color:#92400E
    style Output fill:#ECFDF5,stroke:#059669,stroke-width:2px,color:#065F46
```

---



## Comprehensive Documentation Index

| Documentation File | Target Audience | Primary Focus |
|:-------------------|:----------------|:--------------|
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Technical Architects & Leads | Component topologies, data pipelines, and architectural design decisions |
| [docs/FORECAST_ENGINE.md](docs/FORECAST_ENGINE.md) | Finance Analysts & Quant Engineers | 5-step deterministic formulas, haircut rules, and Monte Carlo stochastic mechanics |
| [docs/INTELLIGENCE.md](docs/INTELLIGENCE.md) | Engagement Managers & Practice Leads | 20+ financial reasoning metrics, 9 insight evaluators, and 10 action remediation rules |
| [docs/DATA_MODEL.md](docs/DATA_MODEL.md) | Data Engineers & DBAs | PostgreSQL relational schema, constraints, ERD, and table schemas |
| [docs/API.md](docs/API.md) | Integration Engineers | Complete REST API endpoint catalog, JSON payloads, and schemas |
| [docs/DASHBOARD.md](docs/DASHBOARD.md) | Delivery Leaders & Analysts | Streamlit user workflows, executive tabs, charts, and sensitivity controls |
| [docs/METRICS.md](docs/METRICS.md) | Practice Finance Officers | Standard metric glossary, mathematical formulas, and data quality caveats |
| [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) | Software Engineers | Local developer workflows, pytest executions, and contribution standards |
| [docs/PRODUCTION.md](docs/PRODUCTION.md) | DevOps & SREs | Production hardening, Render deployment, logging, and security |

---

## Project Attribution

Personal Portfolio Project · Delivery Finance Operating System Showcase
