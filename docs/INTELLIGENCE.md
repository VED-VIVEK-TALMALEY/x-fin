# X-Fin Intelligence & Reasoning Subsystem

> **Module Paths:** `app/services/finance_reasoning.py`, `app/services/insight_engine.py`, `app/services/recommendation_engine.py`, `app/services/intelligence_engine.py`, `app/services/executive_briefing_engine.py`

---

## Intelligence Subsystem Workflow

```mermaid
flowchart TD
    subgraph S1["1. TELEMETRY EXTRACTION"]
        T1["actual_revenue"]
        T2["budget_revenue"]
        T3["forecast_revenue"]
        T4["committed_backlog"]
        T5["weighted_pipeline"]
    end

    subgraph S2["2. FINANCIAL REASONING ENGINE (finance_reasoning.py)"]
        direction TB
        R1["<b>Variance & Gap Ratios:</b><br/>• budget_gap = actual_revenue - budget_revenue<br/>• budget_gap_pct = (budget_gap / budget_revenue) * 100<br/>• forecast_gap = forecast_revenue - budget_revenue<br/>• forecast_gap_pct = (forecast_gap / budget_revenue) * 100"]
        R2["<b>Coverage & Composition Ratios:</b><br/>• forward_revenue = committed_backlog + weighted_pipeline<br/>• forward_coverage = (forward_revenue / budget_revenue) * 100<br/>• committed_forecast_coverage = (committed_backlog / forecast_revenue) * 100<br/>• pipeline_dependency = (weighted_pipeline / forward_revenue) * 100<br/>• committed_revenue_mix = (committed_backlog / forward_revenue) * 100"]
        R3["<b>Operational Health Classifications:</b><br/>• forecast_risk ('low'|'moderate'|'high')<br/>• pipeline_risk ('low'|'moderate'|'high')<br/>• forward_position ('strong'|'adequate'|'watch'|'weak')"]
        R1 --> R2 --> R3
    end

    subgraph S3["3. DIAGNOSTIC INSIGHT ENGINE (insight_engine.py)"]
        I_EVAL["Evaluate 9 Severity Heuristic Rules Across Performance, Coverage, Quality, and Risk"]
        I_SCORED["<b>Array of Scored Diagnostic Insights:</b><br/>[{severity: 'HIGH'|'MEDIUM'|'LOW', category, metric, message, value}]"]
        I_EVAL --> I_SCORED
    end

    subgraph S4["4. ACTION RECOMMENDATION ENGINE (recommendation_engine.py)"]
        A_EVAL["Evaluate 10 Prescriptive Action Rules Mapping Deficits to Remediation Tasks with Quantified INR Impact"]
        A_MERGE["Merge Staffing Guardrail Actions & Sort by Priority (HIGH -> MEDIUM -> LOW)"]
        A_EVAL --> A_MERGE
    end

    subgraph S5["5. EXECUTIVE BRIEFING SYNTHESIS (executive_briefing_engine.py)"]
        B_GEN["Generate Strategic Status Summary, Headroom Stance, Critical Interventions, and Leadership Takeaways"]
    end

    S1 --> S2 --> S3 --> S4 --> S5

    style S1 fill:#F8FAFC,stroke:#475569,stroke-width:2px,color:#1E293B
    style S2 fill:#EFF6FF,stroke:#2563EB,stroke-width:2px,color:#1E40AF
    style S3 fill:#FFFBEB,stroke:#D97706,stroke-width:2px,color:#92400E
    style S4 fill:#ECFDF5,stroke:#059669,stroke-width:2px,color:#065F46
    style S5 fill:#FAF5FF,stroke:#9333EA,stroke-width:2px,color:#6B21A8
```

---

## Complete Financial Reasoning Metric Catalog (20+ Ratios)

| Metric Key | Category | Formula / Definition | Healthy Benchmark | Strategic Operational Meaning |
|:-----------|:---------|:---------------------|:-----------------:|:------------------------------|
| `budget_gap` | Variance | $\text{actual\_revenue} - \text{budget\_revenue}$ | $\ge 0.0$ | Recognized fee surplus or deficit vs approved operating budget |
| `budget_gap_pct` | Variance | $(\text{budget\_gap} / \text{budget\_revenue}) \times 100$ | $\ge 0.0\%$ | Relative percentage variance of actual revenue to budget |
| `forecast_gap` | Variance | $\text{forecast\_revenue} - \text{budget\_revenue}$ | $\ge 0.0$ | Expected net deliverable surplus or deficit vs target budget |
| `forecast_gap_pct` | Variance | $(\text{forecast\_gap} / \text{budget\_revenue}) \times 100$ | $\ge 0.0\%$ | Relative headroom percentage above approved plan |
| `forecast_headroom` | Forecast | $\text{forecast\_revenue} - \text{budget\_revenue}$ | $> 0.0$ | Absolute buffer above target revenue baseline |
| `forecast_headroom_pct` | Forecast | $(\text{forecast\_headroom} / \text{budget\_revenue}) \times 100$ | $\ge 10.0\%$ | Relative headroom buffer above budget |
| `forward_revenue` | Coverage | $\text{committed\_backlog} + \text{weighted\_pipeline}$ | $\ge \text{budget}$ | Total forward book of business supporting future revenue |
| `forward_coverage` | Coverage | $(\text{forward\_revenue} / \text{budget\_revenue}) \times 100$ | $\ge 120.0\%$ | Multiple of forward revenue available relative to budget target |
| `committed_forecast_coverage` | Quality | $(\text{committed\_backlog} / \text{forecast\_revenue}) \times 100$ | $\ge 70.0\%$ | Proportion of period forecast secured by executed contracts |
| `committed_revenue_mix` | Quality | $(\text{committed\_backlog} / \text{forward\_revenue}) \times 100$ | $\ge 60.0\%$ | Proportion of total forward book secured by signed SOWs |
| `pipeline_dependency` | Risk | $(\text{weighted\_pipeline} / \text{forward\_revenue}) \times 100$ | $\le 40.0\%$ | Share of forward book dependent on open proposal wins |
| `forecast_risk` | Classification | Evaluates `committed_forecast_coverage` | `"low"` ($\ge 70\%$) | Qualitative confidence in forecast delivery attainment |
| `pipeline_risk` | Classification | Evaluates `pipeline_dependency` | `"low"` ($\le 30\%$) | Qualitative exposure to commercial pipeline conversion |
| `forward_position` | Classification | Evaluates `forward_coverage` | `"strong"` ($\ge 120\%$) | Comprehensive market stance and capacity health |
| `performance` | Classification | Evaluates `budget_gap` | `"ahead_of_plan"` ($>0$) | Current period revenue realization performance |
| `forecast_status` | Classification | Evaluates `forecast_gap` | `"on_or_above_plan"` | Projected year-end delivery target attainment |
| `headroom_status` | Classification | Evaluates `forecast_headroom_pct` | `"strong"` ($\ge 10\%$) | Practice buffer rating above operating plan |
| `p10_revenue` | Stochastic | Monte Carlo 10th percentile outcome | $\approx 0.90 \times \text{Net}$ | Downside revenue floor under adverse market conditions |
| `p50_revenue` | Stochastic | Monte Carlo 50th percentile outcome | $\approx \text{Net Forecast}$ | Median expected probabilistic outcome |
| `p90_revenue` | Stochastic | Monte Carlo 90th percentile outcome | $\approx 1.10 \times \text{Net}$ | High-conversion upside revenue potential |
| `var_p10` | Stochastic | $\text{Deterministic Net} - \text{P10 Outcome}$ | Minimize | Downside value-at-risk exposure |

---

## Practice Lead Diagnostic Insights Matrix (9 Rules)

| # | Diagnostic Dimension | Telemetry Metric | [HIGH] Severity Condition | [MEDIUM] Severity Condition | [LOW] Severity Condition | Management Diagnostic Action |
|:--:|:---------------------|:-----------------|:--------------------------|:----------------------------|:-------------------------|:-----------------------------|
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

## Action Recommendation Engine (10 Rules + Staffing Actions)

```mermaid
flowchart LR
    subgraph TriggerMatrix["TRIGGER CONDITIONS"]
        T1["budget_gap < 0"]
        T2["forecast_gap < 0"]
        T3["forward_coverage < 100%"]
        T4["100% <= forward_coverage < 120%"]
        T5["pipeline_dependency >= 60%"]
        T6["40% <= pipeline_dependency < 60%"]
        T7["committed_forecast_coverage < 50%"]
        T8["50% <= committed_forecast_coverage < 70%"]
        T9["forecast_risk == 'high'"]
        T10["forward_coverage >= 120% & pipeline < 60%"]
    end

    subgraph Actions["PRESCRIPTIVE ACTION ITEMS"]
        A1["Partner Revenue Recovery Mobilization"]
        A2["Forecast Protection & Extension Lock-in"]
        A3["Fast-Track Proposal Origination"]
        A4["Coverage Buffer Momentum Maintenance"]
        A5["Executive Closing Surge on Qualified Deals"]
        A6["Weekly Stage-Gate Velocity Reviews"]
        A7["Priority Legal Hardening of MSAs/SOWs"]
        A8["Milestone Sign-Off Acceleration"]
        A9["Portfolio-Wide Deliverable Slippage Audit"]
        A10["High-Margin Premium Rate Prioritization"]
    end

    T1 --> A1
    T2 --> A2
    T3 --> A3
    T4 --> A4
    T5 --> A5
    T6 --> A6
    T7 --> A7
    T8 --> A8
    T9 --> A9
    T10 --> A10

    style TriggerMatrix fill:#EFF6FF,stroke:#2563EB,stroke-width:2px,color:#1E40AF
    style Actions fill:#ECFDF5,stroke:#059669,stroke-width:2px,color:#065F46
```

### Action Recommendation Catalog & Financial Valuation

| Priority | Strategy Category | Activation Rule | Action Description | Quantified Financial Impact (INR) |
|:---------|:------------------|:----------------|:-------------------|:----------------------------------|
| **[HIGH]** | Revenue Recovery | `budget_gap < 0` | Mobilize partner-led revenue recovery plan on lagging accounts | $\text{abs}(\text{budget\_gap})$ |
| **[HIGH]** | Forecast Protection | `forecast_gap < 0` | Lock in pending contract extensions and prevent scope reduction | $\text{abs}(\text{forecast\_gap})$ |
| **[HIGH]** | Pipeline Coverage | `forward_coverage < 100%` | Fast-track high-probability proposals to achieve baseline budget | $\text{budget} - \text{forward\_revenue}$ |
| **[MEDIUM]** | Coverage Buffer | `100% <= forward_coverage < 120%` | Maintain business development momentum to preserve safety buffer | $\text{forward\_revenue} - \text{budget}$ |
| **[HIGH]** | Deal Closure Surge | `pipeline_dependency >= 60%` | Conduct executive closing sessions on all deals in Qualified stage | $\text{weighted\_pipeline}$ |
| **[MEDIUM]** | Velocity Management| `40% <= pipeline_dependency < 60%` | Review stage-gate progression weekly with client teams | $\text{weighted\_pipeline}$ |
| **[HIGH]** | Backlog Fortification| `committed_forecast_coverage < 50%`| Prioritize execution of MSAs and SOWs currently under legal review | $\text{forecast} - \text{backlog}$ |
| **[MEDIUM]** | Backlog Hardening | `50% <= committed_forecast_coverage < 70%`| Expedite client sign-offs on milestone deliverables | $\text{forecast} - \text{backlog}$ |
| **[HIGH]** | Delivery Audit | `forecast_risk == "high"` | Conduct portfolio-wide review to prevent deliverable slippage | $\text{forecast\_revenue}$ |
| **[LOW]** | Margin Optimization| `forward_coverage >= 120%` & `pipeline < 60%`| Prioritize higher-margin, premium-rate engagements | $\text{forecast\_gap}$ |

---

## Staffing & Utilization Data-Quality Guardrails

`app/services/staffing_engine.py` and `app/services/staffing_insight_engine.py` evaluate capacity vs hours budget boundaries:

```mermaid
flowchart TD
    subgraph Telemetry["Staffing Telemetry"]
        ACT_HRS["actual_hours (Delivered)"]
        BDG_HRS["hours_budget (Capacity Target)"]
        UTIL_BDG["utilization_budget (75% Baseline)"]
    end

    subgraph Eval["Data Quality Evaluation"]
        CHK["Check: Is hours_budget true consultant capacity or planned billable demand?"]
        FLAG["If schema lacks head-count capacity denominator:<br/><b>utilization_data_quality = 'review_required'</b>"]
        CHK --> FLAG
    end

    subgraph Actions["Staffing Remediations"]
        STF_INS["Surface explicit Data Quality Warning Banner in Streamlit UI"]
        STF_REC["Recommend establishing standard denominator across all delivery hubs"]
    end

    Telemetry --> Eval --> Actions

    style Telemetry fill:#F8FAFC,stroke:#475569,stroke-width:2px,color:#1E293B
    style Eval fill:#FFFBEB,stroke:#D97706,stroke-width:2px,color:#92400E
    style Actions fill:#ECFDF5,stroke:#059669,stroke-width:2px,color:#065F46
```
