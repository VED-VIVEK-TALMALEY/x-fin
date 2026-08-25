# X-Fin — Intelligence Layer

> **Modules** `finance_reasoning.py` · `insight_engine.py` · `recommendation_engine.py`
> **Router** `app/routers/intelligence.py` · **Endpoint** `GET /intelligence/overview`

---

## Overview

The intelligence layer transforms raw financial data into human-readable assessments and actions. It operates in three sequential stages:

```
Stage 1 — REASONING
  finance_reasoning.explain_financial_position()
  Input:  actual_revenue, budget_revenue, forecast_revenue,
          committed_backlog, weighted_pipeline
  Output: 20+ derived metrics and risk classifications

           │
           ▼

Stage 2 — INSIGHTS
  insight_engine.generate_insights(reasoning)
  Input:  reasoning dict
  Output: list of scored insight objects
          Each has: severity, category, metric, message, value

           │
           ▼

Stage 3 — RECOMMENDATIONS
  recommendation_engine.generate_recommendations(reasoning, insights)
  Input:  reasoning dict + insights list
  Output: priority-sorted list of action items
          Each has: priority, category, action, rationale, financial_impact
```

---

## Stage 1 — Reasoning (`finance_reasoning.py`)

### Input Parameters

| Parameter | Source |
|-----------|--------|
| `actual_revenue` | `get_finance_summary()` |
| `budget_revenue` | `get_budget_summary()` |
| `forecast_revenue` | `build_forecast()` |
| `committed_backlog` | `calculate_backlog()` |
| `weighted_pipeline` | `get_pipeline_summary()` |

### Output Metrics

| Metric | Formula | Description |
|--------|---------|-------------|
| `budget_gap` | `actual - budget` | Positive = ahead of plan |
| `budget_gap_pct` | `budget_gap / budget * 100` | % vs budget |
| `forecast_gap` | `forecast - budget` | Positive = forecast above budget |
| `forecast_gap_pct` | `forecast_gap / budget * 100` | % vs budget |
| `forward_revenue` | `committed + weighted` | Total forward coverage ₹ |
| `forward_coverage` | `forward / budget * 100` | Forward revenue as % of budget |
| `committed_forecast_coverage` | `committed / forecast * 100` | Backlog-backed % of forecast |
| `pipeline_dependency` | `weighted / forward * 100` | % of forward from pipeline |
| `committed_revenue_mix` | `committed / forward * 100` | Complement of pipeline_dependency |
| `forecast_headroom` | `= forecast_gap` | ₹ above or below budget |
| `forecast_headroom_pct` | `headroom / budget * 100` | % headroom |

### Risk Classifications

#### Forecast Risk

> Measures **backlog support** behind the forecast. Not a statistical probability.

| `committed_forecast_coverage` | `forecast_risk` |
|-------------------------------|-----------------|
| >= 70% | `low` |
| 50% – 69% | `moderate` |
| < 50% | `high` |

#### Pipeline Risk

| `pipeline_dependency` | `pipeline_risk` |
|-----------------------|-----------------|
| <= 30% | `low` |
| 31% – 50% | `moderate` |
| > 50% | `high` |

#### Forward Position

| `forward_coverage` | `forward_position` |
|--------------------|-------------------|
| >= 120% | `strong` |
| 100% – 119% | `adequate` |
| 80% – 99% | `watch` |
| < 80% | `weak` |

#### Performance Status

| Condition | `performance` |
|-----------|--------------|
| `budget_gap > 0` | `ahead_of_plan` |
| `budget_gap < 0` | `below_plan` |
| `budget_gap = 0` | `on_plan` |

#### Forecast Status

| Condition | `forecast_status` |
|-----------|-----------------|
| `forecast_gap > 0` | `on_or_above_plan` |
| `forecast_gap < 0` | `below_plan` |
| `forecast_gap = 0` | `on_plan` |

---

## Stage 2 — Insights (`insight_engine.py`)

Nine insight rules, always evaluated in order. Severity: `HIGH` / `MEDIUM` / `LOW`.

### Insight Rules Table

| # | Category | Metric | HIGH condition | MEDIUM condition | LOW condition |
|---|----------|--------|----------------|-----------------|--------------|
| 1 | Revenue | Actual vs Budget | `budget_gap_pct <= -10%` | `-10% < gap < 0` | `gap >= 0` |
| 2 | Forecast | Forecast vs Budget | `forecast_gap_pct <= -10%` | `-10% < gap < 0` | `gap >= 0` |
| 3 | Coverage | Forward Revenue Coverage | `< 100%` | `100% – 119%` | `>= 120%` |
| 4 | Forecast Quality | Committed Forecast Coverage | `< 50%` | `50% – 69%` | `>= 70%` |
| 5 | Pipeline Risk | Pipeline Dependency | `>= 60%` | `40% – 59%` | `< 40%` |
| 6 | Revenue Quality | Committed Revenue Mix | `< 40%` | `40% – 59%` | `>= 60%` |
| 7 | Forecast Risk | Forecast Risk | `forecast_risk = "high"` | `= "moderate"` | `= "low"` |
| 8 | Forward Position | Forward Revenue Position | `"watch"` or `"weak"` | `"adequate"` | `"strong"` |
| 9 | Forecast Headroom | Forecast Buffer/Shortfall | `headroom < 0` | — | `headroom > 0` |

### Insight Object Schema

```
{
  "severity":  "HIGH" | "MEDIUM" | "LOW",
  "category":  string,         // e.g. "Revenue", "Coverage"
  "metric":    string,         // e.g. "Actual vs Budget"
  "message":   string,         // human-readable description
  "value":     float           // underlying metric value
}
```

---

## Stage 3 — Recommendations (`recommendation_engine.py`)

Ten recommendation rules, evaluated independently. Output is priority-sorted (HIGH first).

### Recommendation Rules Table

| # | Category | Priority | Trigger Condition |
|---|----------|----------|-------------------|
| 1 | Revenue Recovery | HIGH | `budget_gap < 0` |
| 2 | Forecast Protection | HIGH | `forecast_gap < 0` |
| 3 | Pipeline Coverage | HIGH | `forward_coverage < 100%` |
| 4 | Coverage Protection | MEDIUM | `100% <= forward_coverage < 120%` |
| 5 | Pipeline Risk | HIGH | `pipeline_dependency >= 60%` |
| 6 | Pipeline Management | MEDIUM | `40% <= pipeline_dependency < 60%` |
| 7 | Forecast Quality (High) | HIGH | `committed_forecast_coverage < 50%` |
| 8 | Forecast Quality (Med) | MEDIUM | `50% <= committed_forecast_coverage < 70%` |
| 9 | Forecast Risk | HIGH | `forecast_risk = "high"` |
| 10 | Performance Protection | LOW | All positive: `budget_gap >= 0` AND `forecast_gap >= 0` AND `coverage >= 100%` AND `pipeline_risk != "high"` |

### Growth Optimization (bonus rule)

Fires when `forward_coverage >= 120%` AND `forecast_gap >= 0` AND `pipeline_dependency < 60%`:

> Use the strong forward position to prioritise higher-margin opportunities.

### Fallback

If no rules fire, a `LOW` / Management Review recommendation is appended to ensure the list is never empty.

### Recommendation Object Schema

```
{
  "priority":         "HIGH" | "MEDIUM" | "LOW",
  "category":         string,
  "action":           string,    // what to do
  "rationale":        string,    // why (includes ₹ values)
  "financial_impact": float      // associated ₹ amount
}
```

---

## Intelligence Response Priority Order

The dashboard presents intelligence data in this order:

```
1. Performance status banner (ahead_of_plan / below_plan)
2. KPI cards: Actual Revenue · Budget · Forecast · Forward Coverage
3. Revenue Outlook bar chart (Budget vs Forecast vs Actual)
4. Forward Revenue split (Committed Backlog vs Weighted Pipeline)
5. Forecast Construction table (waterfall of components)
6. Financial Insights (HIGH first, then MEDIUM, then LOW)
7. Recommended Actions (HIGH first, then MEDIUM, then LOW)
8. Source Financial Metrics (expandable)
```

---

## Important Terminology Note

> **`committed_forecast_coverage`** and **`forecast_confidence_base`** are the same value.
>
> `forecast_confidence_base` is a backward-compatible alias retained for `dashboard/app.py`.
>
> Neither is a **statistical** confidence interval. The value measures:
> _"what percentage of forecast revenue is directly backed by committed backlog."_
>
> This is a **business quality indicator**, not a probability estimate.
