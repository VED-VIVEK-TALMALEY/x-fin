# X-Fin — Delivery Finance Operating System

> **v1.0.0** · FastAPI · PostgreSQL · Streamlit · Python 3.10+

```
╔══════════════════════════════════════════════════════════════╗
║   X-FIN  |  INTELLIGENT DELIVERY FINANCE OPERATING SYSTEM   ║
║                                                              ║
║   Revenue  ·  Forecast  ·  Backlog  ·  Variance             ║
║   Insights  ·  Recommendations  ·  Scenarios                 ║
╚══════════════════════════════════════════════════════════════╝
```

---

## What X-Fin Does

X-Fin is a **rule-based financial intelligence platform** for consulting delivery organisations. It ingests project actuals, pipeline snapshots and budgets from PostgreSQL and produces:

| Output | Description |
|--------|-------------|
| Revenue Forecast | Deterministic model: backlog + pipeline + utilization adjustment − risk haircut |
| Variance Analysis | Actual vs budget and forecast vs budget, absolute and % |
| Backlog Waterfall | Committed backlog, new wins, closing balance |
| Business Unit Performance | Per-BU revenue, margin, hours vs budget |
| Forecast Accuracy | Month-by-month actual vs budget accuracy history |
| Financial Insights | 9-rule severity-scored assessment (HIGH / MEDIUM / LOW) |
| Recommendations | 10-rule priority-sorted action list with ₹ impact |
| Scenario Simulation | What-if: pipeline conversion, utilization, billing rate, slippage |

---

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                  PRESENTATION (Streamlit)                 │
│                                                          │
│    dashboard/app.py ──────────── dashboard/intelligence.py│
│    (Executive Dashboard)         (Intelligence Page)      │
└──────────────────────┬───────────────────────────────────┘
                       │  HTTP GET/POST  (requests library)
                       ▼
┌──────────────────────────────────────────────────────────┐
│                  API LAYER (FastAPI)                      │
│               http://127.0.0.1:8000                      │
│                                                          │
│  /forecast/*    /analytics/*    /intelligence/*          │
│  /scenarios/*   /projects/*                              │
└──────────────────────┬───────────────────────────────────┘
                       │  SQLAlchemy Sessions
                       ▼
┌──────────────────────────────────────────────────────────┐
│                  SERVICE LAYER (Python)                   │
│                                                          │
│  forecast_engine    backlog_engine    variance_engine     │
│  finance_reasoning  insight_engine   recommendation_engine│
│  scenario_engine    business_unit_engine                  │
└──────────────────────┬───────────────────────────────────┘
                       │  Raw SQL (text())
                       ▼
┌──────────────────────────────────────────────────────────┐
│               DATA LAYER (PostgreSQL >= 14)              │
│                                                          │
│  business_units · projects · project_pipeline            │
│  project_actuals · budgets · forecast_versions           │
└──────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
x-fin/
├── app/                         FastAPI backend
│   ├── main.py                  App factory; 5 routers registered
│   ├── config.py                dotenv loader
│   ├── __init__.py              Package init (DATABASE_URL, ENVIRONMENT, API_PORT)
│   ├── db/
│   │   ├── connection.py        SQLAlchemy engine + get_db() dependency
│   │   └── schema.sql           PostgreSQL DDL
│   ├── models/
│   │   └── project.py           ORM model
│   ├── routers/
│   │   ├── analytics.py         6 analytics endpoints
│   │   ├── forecast.py          /forecast/current
│   │   ├── intelligence.py      /intelligence/health + /intelligence/overview
│   │   ├── projects.py          Project CRUD
│   │   └── scenarios.py         POST /scenarios/run
│   └── services/
│       ├── backlog_engine.py    Backlog + waterfall calculation
│       ├── business_unit_engine.py  Per-BU performance
│       ├── finance_queries.py   SQL: finance, pipeline, budget, monthly revenue
│       ├── finance_reasoning.py 20+ derived metrics + risk classifications
│       ├── forecast_accuracy.py Monthly accuracy time series
│       ├── forecast_engine.py   Deterministic forecast (ForecastResult)
│       ├── insight_engine.py    9-rule insight scorer
│       ├── recommendation_engine.py  10-rule recommendation generator
│       ├── revenue_calc.py      Revenue helpers
│       ├── scenario_engine.py   What-if scenario calculator
│       └── variance_engine.py   VarianceResult + bridge
│
├── dashboard/                   Streamlit front-end
│   ├── app.py                   Executive dashboard (8 KPIs, charts, intelligence)
│   ├── intelligence.py          Intelligence deep-dive page
│   ├── api.py                   HTTP client (9 functions)
│   ├── charts.py                Plotly chart builders
│   └── components.py            metric_card, section_title, format helpers
│
├── data/
│   ├── actuals.csv              ~18,000 rows (750 projects x 24 months)
│   ├── budgets.csv              72 rows (3 BUs x 24 months)
│   ├── pipeline.csv             ~4,500 rows (750 projects x 6 snapshots)
│   ├── projects.csv             750 rows
│   └── synthetic_projects.csv   Legacy synthetic file
│
├── scripts/
│   ├── generate_synthetic_data.py  Generates 4 CSV files
│   └── load_data.py                Loads CSVs into PostgreSQL
│
├── tests/
│   ├── test_forecast.py         Unit test: forecast_engine
│   └── test_variance.py         Unit test: variance_engine
│
├── .env                         Local environment variables
├── requirements.txt             16 Python dependencies
└── gen_tree.py                  Utility: prints directory tree
```

---

## Quick Start

### Prerequisites

| Requirement | Version | Role |
|-------------|---------|------|
| Python | >= 3.10 | Runtime |
| PostgreSQL | >= 14 | Database |
| pip | latest | Package manager |

### Step-by-step

```bash
# 1. Create virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
# Edit .env:
#   DATABASE_URL=postgresql://postgres:forecast@localhost:5432/consulting_forecast
#   ENVIRONMENT=development

# 4. Apply database schema
psql -U postgres -d consulting_forecast -f app/db/schema.sql

# 5. Generate and load synthetic data
python scripts/generate_synthetic_data.py
python scripts/load_data.py

# 6. Start the API
uvicorn app.main:app --reload --port 8000

# 7. Start the dashboard (in a second terminal)
cd dashboard
streamlit run app.py
```

---

## API Endpoints

### Route Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Service identity + health |
| GET | `/health` | Health check |
| GET | `/forecast/current` | Current revenue forecast |
| GET | `/analytics/summary` | Finance + budget + backlog aggregate |
| GET | `/analytics/monthly-revenue` | Monthly revenue time series |
| GET | `/analytics/backlog` | Backlog summary + waterfall |
| GET | `/analytics/variance` | Actual vs budget variance |
| GET | `/analytics/forecast-accuracy` | Monthly forecast accuracy history |
| GET | `/analytics/business-units` | Per-BU performance |
| GET | `/intelligence/health` | Intelligence service health |
| GET | `/intelligence/overview` | Full intelligence package |
| POST | `/scenarios/run` | What-if scenario simulation |

### Auto-generated API docs

| URL | Interface |
|-----|-----------|
| `http://127.0.0.1:8000/docs` | Swagger UI |
| `http://127.0.0.1:8000/redoc` | ReDoc |

---

## Database Tables

| Table | Purpose | Key Columns |
|-------|---------|-------------|
| `business_units` | Master BU list | `business_unit_id`, `name` |
| `projects` | Project master | `project_id`, `stage`, `contract_value`, `billing_rate` |
| `project_pipeline` | Snapshot pipeline | `snapshot_date`, `stage`, `probability`, `pipeline_value` |
| `project_actuals` | Monthly actuals | `month`, `actual_hours`, `actual_revenue`, `actual_cost` |
| `budgets` | Monthly BU budgets | `month`, `revenue_budget`, `utilization_budget` |
| `forecast_versions` | Forecast audit trail | `forecast_date`, `forecast_month` |
| `forecast_values` | Per-project forecasts | `forecast_revenue`, `confidence` |

---

## Forecast Engine

```
Inputs
──────
  committed_backlog  = SUM(pipeline_value)  stage IN ('In Delivery', 'Closed Won')
  weighted_pipeline  = SUM(pipeline_value * probability)
  utilization        = AVG(utilization_budget)   from budgets table
  target_utilization = 0.75   (hard-coded)
  risk_rate          = 0.05   (hard-coded, 5%)

Formula
───────
  utilization_adjustment = committed_backlog * (utilization / target_utilization - 1)
  gross_forecast         = committed_backlog + weighted_pipeline + utilization_adjustment
  risk_adjustment        = gross_forecast * risk_rate
  forecast_revenue       = gross_forecast - risk_adjustment

Numerical Example  (utilization = target = 0.75)
────────────────────────────────────────────────
  committed_backlog = 100,000
  weighted_pipeline =  50,000
  utilization_adj   =       0   (neutral)
  gross_forecast    = 150,000
  risk_adjustment   =   7,500
  forecast_revenue  = 142,500   ✓ (matches test_forecast.py)
```

---

## Intelligence Pipeline

```
  actual_revenue
  budget_revenue            ┌─────────────────────┐
  forecast_revenue    ─────►│  finance_reasoning  │
  committed_backlog         │  explain_financial_ │
  weighted_pipeline         │  position()         │
                            └─────────┬───────────┘
                                      │  20+ metrics
                                      ▼
                            ┌─────────────────────┐
                            │   insight_engine    │
                            │   generate_insights │
                            │   9 rules           │
                            └─────────┬───────────┘
                                      │  scored insights[]
                                      ▼
                            ┌─────────────────────┐
                            │ recommendation_engine│
                            │ generate_            │
                            │ recommendations()   │
                            │ 10 rules            │
                            └─────────┬───────────┘
                                      │  priority-sorted recs[]
                                      ▼
                             /intelligence/overview
```

### Insight Severity Rules

| Insight Category | HIGH | MEDIUM | LOW |
|-----------------|------|--------|-----|
| Revenue vs Budget | gap <= -10% | -10% to 0 | >= 0 |
| Forecast vs Budget | gap <= -10% | -10% to 0 | >= 0 |
| Forward Coverage | < 100% | 100–119% | >= 120% |
| Committed Forecast Coverage | < 50% | 50–69% | >= 70% |
| Pipeline Dependency | >= 60% | 40–59% | < 40% |
| Committed Revenue Mix | < 40% | 40–59% | >= 60% |
| Forecast Risk | "high" | "moderate" | "low" |
| Forward Position | "watch"/"weak" | "adequate" | "strong" |
| Forecast Headroom | negative | — | positive |

### Risk Classification

```
forecast_risk classification (committed_forecast_coverage):
  >= 70%  →  low
  >= 50%  →  moderate
  <  50%  →  high

pipeline_risk classification (pipeline_dependency):
  <= 30%  →  low
  <= 50%  →  moderate
  >  50%  →  high

forward_position (forward_coverage = (committed + weighted) / budget * 100):
  >= 120%  →  strong
  >= 100%  →  adequate
  >=  80%  →  watch
  <   80%  →  weak
```

---

## Dashboard Pages

### `dashboard/app.py` — Executive Dashboard

| Section | Data Source | Visualisation |
|---------|-------------|---------------|
| Executive Performance (8 metrics) | analytics/summary + forecast/current | Metric cards |
| Executive Intelligence | intelligence/overview | Status + 4 KPIs |
| Key Insights | intelligence/overview | Colour-coded alerts (HIGH=red, MEDIUM=amber, LOW=blue) |
| Recommended Actions | intelligence/overview | Priority-sorted alert cards |
| Forecast Engine Detail | intelligence/overview | 5 expandable metric cards |
| Revenue Performance | analytics/monthly-revenue | Plotly line chart |
| Backlog | analytics/backlog | Bar chart |
| Business Units | analytics/business-units | Grouped bar chart |
| Forecast Accuracy | analytics/forecast-accuracy | Line + bar chart |
| Variance | analytics/variance | Summary metrics |
| Scenario Planner | scenarios/run | Interactive sliders + result card |

### `dashboard/intelligence.py` — Intelligence Deep-Dive

| Section | Visualisation |
|---------|---------------|
| Performance status banner | Success / Error / Warning |
| KPI row: Actual · Budget · Forecast · Forward Coverage | st.metric cards |
| Revenue Outlook | Plotly bar (Budget vs Forecast vs Actual) |
| Forward Revenue | Plotly bar (Committed vs Weighted) |
| Forecast Construction | Dataframe table (5 components) |
| Financial Insights | Colour-coded alert cards |
| Recommended Actions | Priority-sorted alert cards |
| Source Financial Metrics | Expandable dataframe |

---

## Synthetic Data

| Dataset | Rows | Generation |
|---------|------|-----------|
| Projects | 750 | Random BU, stage, billing rate (150–400 ₹/hr), hours (200–5000) |
| Pipeline | ~4,500 | 6 monthly snapshots per project |
| Actuals | ~18,000 | 24 monthly records per project |
| Budgets | 72 | 3 BUs × 24 months, ₹4M–₹10M/month |

Business units: **X Build** · **X Design** · **Digital Ventures**

---

## Testing

```bash
pytest tests/ -v
```

| Test | Input | Expected |
|------|-------|----------|
| `test_forecast` | backlog=100K, pipeline=50K, util=0.75, target=0.75, risk=5% | `forecast_revenue == 142500.00` |
| `test_variance` | actual=90, budget=100, forecast=95 | `actual_vs_budget == -10`, `actual_vs_budget_pct == -10`, `forecast_vs_budget == -5` |

---

## Dependencies

| Package | Role |
|---------|------|
| `fastapi` | REST API framework |
| `uvicorn` | ASGI server |
| `sqlalchemy` | Database ORM + raw SQL |
| `psycopg2-binary` | PostgreSQL driver |
| `pydantic` | Data validation |
| `python-dotenv` | `.env` loader |
| `pandas` | Data manipulation |
| `numpy` | Numerical ops |
| `plotly` | Interactive charts |
| `streamlit` | Dashboard UI |
| `pytest` | Test runner |
| `httpx` | Async HTTP (tests) |
| `pytest-asyncio` | Async test support |
| `black` | Code formatter |
| `flake8` | Linter |
| `requests` | HTTP client (dashboard) |

---

## Documentation

| Document | Link |
|----------|------|
| Architecture & Data Flow | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| API Reference | [docs/API.md](docs/API.md) |
| Database Schema | [docs/DATA_MODEL.md](docs/DATA_MODEL.md) |
| Forecast & Variance Engine | [docs/FORECAST_ENGINE.md](docs/FORECAST_ENGINE.md) |
| Intelligence Layer | [docs/INTELLIGENCE.md](docs/INTELLIGENCE.md) |
| Development Guide | [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) |

---

## Known Limitations

| Area | Detail |
|------|--------|
| Backlog waterfall | `revenue_recognized` always `null` — period schedules not implemented |
| `/forecast/current` | Uses hard-coded utilization 0.74 (not live budget utilization) |
| Risk rate | Hard-coded at 5%; not environment-configurable |
| `forecast_versions` | Schema present but not populated by any v1.0.0 endpoint |
| Currency | INR-only; not internationalised |
| `dashboard/api.py` | `get_intelligence()` defined twice; second definition takes precedence |
