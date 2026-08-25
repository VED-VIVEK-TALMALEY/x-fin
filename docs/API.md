# X-Fin — API Reference

> **Base URL** `http://127.0.0.1:8000` · **Framework** FastAPI 0.115+ · **Format** JSON

---

## Endpoint Map

```
GET  /                              Root health check
GET  /health                        Service health

GET  /forecast/current              Current revenue forecast

GET  /analytics/summary             Finance + budget + backlog summary
GET  /analytics/monthly-revenue     Month-by-month revenue time series
GET  /analytics/backlog             Backlog summary + waterfall
GET  /analytics/variance            Actual vs budget variance
GET  /analytics/forecast-accuracy   Monthly forecast accuracy history
GET  /analytics/business-units      Per-BU performance breakdown

GET  /intelligence/health           Intelligence service health
GET  /intelligence/overview         Full intelligence package

POST /scenarios/run                 What-if scenario simulation
```

---

## Root

### `GET /`

Returns service identity and health status.

**Response**

| Field | Type | Example |
|-------|------|---------|
| `name` | string | `"X-Fin"` |
| `version` | string | `"1.0.0"` |
| `description` | string | `"Intelligent Delivery Finance Operating System"` |
| `status` | string | `"healthy"` |

---

### `GET /health`

| Field | Type | Example |
|-------|------|---------|
| `status` | string | `"healthy"` |
| `service` | string | `"x-fin"` |

---

## Forecast

### `GET /forecast/current`

Builds the current period revenue forecast from live database data.

**Response**

```
{
  "forecast": {
    "committed_backlog":       float,   // ₹ value of In Delivery + Closed Won
    "weighted_pipeline":       float,   // probability-weighted pipeline
    "utilization_adjustment":  float,   // delta from actual vs target utilization
    "risk_adjustment":         float,   // 5% gross forecast haircut
    "forecast_revenue":        float    // net forecast revenue
  },
  "pipeline": {
    "opportunities":       int,
    "pipeline_value":      float,   // raw pipeline (no probability weighting)
    "weighted_pipeline":   float    // probability-weighted pipeline
  },
  "backlog": {
    "committed_backlog":     float,
    "uncommitted_pipeline":  float,
    "total_coverage":        float
  }
}
```

**Forecast formula:**

```
gross_forecast = committed_backlog
               + weighted_pipeline
               + utilization_adjustment

utilization_adjustment = committed_backlog
                       * (actual_utilization / target_utilization - 1)

risk_adjustment = gross_forecast * 0.05

forecast_revenue = gross_forecast - risk_adjustment
```

---

## Analytics

### `GET /analytics/summary`

Aggregate finance, budget and backlog summary across all projects and BUs.

**Response**

| Key | Sub-fields |
|-----|------------|
| `finance` | `actual_revenue`, `actual_cost`, `contract_value`, `planned_hours` |
| `budget` | `budget_revenue`, `budget_hours`, `budget_utilization` |
| `backlog` | `committed_backlog`, `uncommitted_pipeline`, `total_coverage` |

---

### `GET /analytics/monthly-revenue`

Time series of monthly revenue, hours and cost.

**Response** — array of objects:

| Field | Type | Description |
|-------|------|-------------|
| `month` | date | Month start date (YYYY-MM-DD) |
| `revenue` | float | Sum of actual revenue |
| `hours` | float | Sum of actual hours |
| `cost` | float | Sum of actual cost |

---

### `GET /analytics/backlog`

Backlog summary and simplified waterfall.

**Response**

```
{
  "summary": {
    "committed_backlog":    float,
    "uncommitted_pipeline": float,
    "total_coverage":       float
  },
  "waterfall": {
    "opening_backlog":    float,    // In Delivery stage value
    "new_wins":           float,    // Closed Won stage value
    "revenue_recognized": null,     // requires period schedules
    "closing_backlog":    float,    // opening + new_wins
    "methodology":        string
  }
}
```

---

### `GET /analytics/variance`

Budget variance analysis.

**Response** — `VarianceResult` fields:

| Field | Type | Description |
|-------|------|-------------|
| `actual` | decimal | Actual revenue |
| `budget` | decimal | Budget revenue |
| `forecast` | decimal | Current forecast |
| `actual_vs_budget` | decimal | Actual - Budget (absolute) |
| `actual_vs_budget_pct` | decimal | As % of budget |
| `forecast_vs_budget` | decimal | Forecast - Budget (absolute) |
| `forecast_vs_budget_pct` | decimal | As % of budget |

---

### `GET /analytics/forecast-accuracy`

Monthly comparison of actual vs. budget revenue with variance %.

**Response** — array of objects:

| Field | Type | Description |
|-------|------|-------------|
| `month` | date | Month start |
| `actual_revenue` | float | Actuals for month |
| `budget_revenue` | float | Budget for month |
| `variance_pct` | float | (actual - budget) / budget * 100 |

---

### `GET /analytics/business-units`

Per-business-unit revenue and margin performance, sorted descending by actual revenue.

**Response** — array of objects:

| Field | Type | Description |
|-------|------|-------------|
| `business_unit` | string | BU name |
| `actual_revenue` | float | Total actual revenue |
| `budget_revenue` | float | Total budget |
| `variance` | float | actual - budget |
| `variance_pct` | float | % variance |
| `actual_cost` | float | Total actual cost |
| `gross_margin` | float | Revenue - cost |
| `gross_margin_pct` | float | Margin as % of revenue |
| `actual_hours` | float | Total actual hours |
| `budget_hours` | float | Total budgeted hours |

---

## Intelligence

### `GET /intelligence/overview`

Full intelligence package: reasoning, insights and recommendations.

**Response**

```
{
  "status": "healthy" | "error",

  "reasoning": {
    // Core financial values
    "actual_revenue":       float,
    "budget_revenue":       float,
    "forecast_revenue":     float,
    "committed_backlog":    float,
    "weighted_pipeline":    float,

    // Variances
    "budget_gap":           float,    // actual - budget
    "budget_gap_pct":       float,
    "forecast_gap":         float,    // forecast - budget
    "forecast_gap_pct":     float,

    // Forward position
    "forward_revenue":      float,    // committed + weighted
    "forward_coverage":     float,    // forward / budget * 100
    "forward_position":     "strong" | "adequate" | "watch" | "weak",

    // Forecast composition
    "committed_forecast_coverage": float,  // committed / forecast * 100
    "committed_revenue_mix":       float,  // committed / forward * 100
    "pipeline_dependency":         float,  // weighted / forward * 100

    // Risk classification
    "forecast_risk":  "low" | "moderate" | "high",
    "pipeline_risk":  "low" | "moderate" | "high",

    // Statuses
    "performance":      "ahead_of_plan" | "on_plan" | "below_plan",
    "forecast_status":  "on_or_above_plan" | "on_plan" | "below_plan",

    // Headroom
    "forecast_headroom":     float,
    "forecast_headroom_pct": float,

    // Backward-compat alias for committed_forecast_coverage
    "forecast_confidence_base": float
  },

  "insights": [
    {
      "severity":  "HIGH" | "MEDIUM" | "LOW",
      "category":  string,
      "metric":    string,
      "message":   string,
      "value":     float
    }
  ],

  "recommendations": [
    {
      "priority":         "HIGH" | "MEDIUM" | "LOW",
      "category":         string,
      "action":           string,
      "rationale":        string,
      "financial_impact": float
    }
  ],

  "source_metrics": {
    "actual_revenue":       float,
    "budget_revenue":       float,
    "budget_utilization":   float,
    "pipeline_value":       float,
    "weighted_pipeline":    float,
    "committed_backlog":    float,
    "uncommitted_pipeline": float
  },

  "forecast": {
    "committed_backlog":      float,
    "weighted_pipeline":      float,
    "utilization_adjustment": float,
    "risk_adjustment":        float,
    "forecast_revenue":       float
  }
}
```

---

## Scenarios

### `POST /scenarios/run`

Run a parameterised what-if scenario on revenue.

**Request body**

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `base_revenue` | float | Yes | — | Current committed / actual revenue base |
| `pipeline_revenue` | float | Yes | — | Pipeline revenue before adjustments |
| `utilization` | float | Yes | — | Current utilization rate (0–1) |
| `pipeline_conversion_change` | float | No | `0.0` | Delta on pipeline conversion (e.g. +0.10 = +10%) |
| `utilization_change` | float | No | `0.0` | Delta on utilization rate |
| `billing_rate_change` | float | No | `0.0` | Delta on billing rate (e.g. +0.05 = +5%) |
| `slippage_rate` | float | No | `0.0` | Revenue slippage haircut (0–1) |

**Response**

| Field | Type | Description |
|-------|------|-------------|
| `base_revenue` | float | Input base revenue |
| `adjusted_pipeline` | float | Pipeline after conversion delta |
| `adjusted_utilization` | float | Utilization after delta |
| `scenario_revenue` | float | Total scenario revenue |
| `revenue_change` | float | Delta vs base |
| `revenue_change_pct` | float | % delta vs base |

**Example**

```json
// Request
{
  "base_revenue": 5000000,
  "pipeline_revenue": 2000000,
  "utilization": 0.74,
  "pipeline_conversion_change": 0.10,
  "utilization_change": 0.02,
  "billing_rate_change": 0.05,
  "slippage_rate": 0.03
}

// Response
{
  "base_revenue": 5000000.0,
  "adjusted_pipeline": 2200000.0,
  "adjusted_utilization": 0.76,
  "scenario_revenue": 7451200.0,
  "revenue_change": 2451200.0,
  "revenue_change_pct": 49.02
}
```

---

## Error Handling

All endpoints return standard HTTP status codes.

| Code | Meaning |
|------|---------|
| `200` | Success |
| `422` | Validation error (Pydantic) |
| `500` | Internal server error |

For `/intelligence/overview`, failures return a `200` with `"status": "error"` and `"error"` / `"error_type"` fields — this preserves dashboard connectivity even during partial failures.
