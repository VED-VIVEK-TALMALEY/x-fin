# X-Fin — Forecast Engine

> **Module** `app/services/forecast_engine.py` · **Router** `app/routers/forecast.py`

---

## Overview

The forecast engine produces a single deterministic revenue number for the current planning period. It takes three financial signals — committed backlog, probability-weighted pipeline, and utilization — and applies two adjustments to arrive at net forecast revenue.

---

## Formula

```
Step 1 — Utilization factor
─────────────────────────────
utilization_factor = actual_utilization / target_utilization


Step 2 — Utilization adjustment
────────────────────────────────
utilization_adjustment = committed_backlog
                       * (utilization_factor - 1)

  > Positive when actual > target: upside
  > Negative when actual < target: downside


Step 3 — Gross forecast
────────────────────────
gross_forecast = committed_backlog
               + weighted_pipeline
               + utilization_adjustment


Step 4 — Risk adjustment (haircut)
────────────────────────────────────
risk_adjustment = gross_forecast * risk_rate   (default 5%)


Step 5 — Net forecast
──────────────────────
forecast_revenue = gross_forecast - risk_adjustment
```

---

## Inputs

| Input | Source | Default | Description |
|-------|--------|---------|-------------|
| `committed_backlog` | `backlog_engine.calculate_backlog()` | — | Sum of pipeline_value where stage IN ('In Delivery', 'Closed Won') at latest snapshot |
| `weighted_pipeline` | `finance_queries.get_pipeline_summary()` | — | SUM(pipeline_value * probability) at latest snapshot |
| `utilization` | `finance_queries.get_budget_summary()` → `budget_utilization` | 0.74 | Average utilization_budget across all BU/month budget records |
| `target_utilization` | Hard-coded | **0.75** | Target utilization rate; raises ValueError if <= 0 |
| `risk_rate` | Hard-coded | **0.05** | 5% gross forecast haircut |

---

## Outputs (`ForecastResult` dataclass)

| Field | Type | Description |
|-------|------|-------------|
| `committed_backlog` | float | Input committed backlog (rounded to 2dp) |
| `weighted_pipeline` | float | Input weighted pipeline (rounded to 2dp) |
| `utilization_adjustment` | float | Upside or downside from utilization delta |
| `risk_adjustment` | float | 5% gross forecast haircut |
| `forecast_revenue` | float | **Net forecast revenue** |

---

## Numerical Example

| Input | Value |
|-------|-------|
| Committed Backlog | ₹100,000 |
| Weighted Pipeline | ₹50,000 |
| Actual Utilization | 0.75 |
| Target Utilization | 0.75 |
| Risk Rate | 5% |

```
utilization_factor    = 0.75 / 0.75 = 1.0
utilization_adjustment = 100,000 * (1.0 - 1) = 0

gross_forecast = 100,000 + 50,000 + 0 = 150,000

risk_adjustment = 150,000 * 0.05 = 7,500

forecast_revenue = 150,000 - 7,500 = 142,500
```

> **Test assertion:** `test_forecast.py` confirms `forecast_revenue == 142500.00`

---

## Utilization Sensitivity

```
Actual Utilization vs Target 0.75 | Adjustment Direction
─────────────────────────────────────────────────────────
0.80 (above target)               | Positive (upside)
0.75 (at target)                  | Zero (neutral)
0.70 (below target)               | Negative (downside)
0.60 (well below target)          | Larger negative
```

---

## Usage in Intelligence

When called from `/intelligence/overview`, the forecast engine receives:

- `committed_backlog` from `backlog_engine`
- `weighted_pipeline` from `finance_queries`
- `utilization` = `budget_utilization` from `finance_queries.get_budget_summary()`
- `target_utilization` = 0.75
- `risk_rate` = 0.05

When called from `/forecast/current`, `utilization` is hard-coded to **0.74** (legacy default).

---

## Variance Engine

`app/services/variance_engine.py` provides two functions:

### `calculate_variance(actual, budget, forecast)`

Returns a `VarianceResult` dataclass:

| Field | Formula |
|-------|---------|
| `actual_vs_budget` | `actual - budget` |
| `actual_vs_budget_pct` | `(actual - budget) / budget * 100` |
| `forecast_vs_budget` | `forecast - budget` |
| `forecast_vs_budget_pct` | `(forecast - budget) / budget * 100` |

All values use `Decimal` for precision. Rounded to 2dp.

### `variance_bridge(budget, actual, project_slippage, pipeline_change, utilization_change, rate_change)`

Decomposes the variance between budget and actual into explained components:

```
total_explained = project_slippage
                + pipeline_change
                + utilization_change
                + rate_change

unexplained = actual - budget - total_explained
```

Returns a bridge dictionary with all components and `unexplained`.

---

## Scenario Engine

`app/services/scenario_engine.py` — `run_scenario()`:

```
adjusted_pipeline  = pipeline_revenue * (1 + pipeline_conversion_change)

utilization_factor = (utilization + utilization_change) / utilization
                     [capped: if utilization == 0, factor = 1]

adjusted_revenue   = base_revenue
                   * utilization_factor
                   * (1 + billing_rate_change)
                   + adjusted_pipeline

scenario_revenue   = adjusted_revenue * (1 - slippage_rate)

revenue_change     = scenario_revenue - base_revenue
revenue_change_pct = revenue_change / base_revenue * 100
```
