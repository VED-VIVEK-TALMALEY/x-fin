# X-Fin — Development Guide

> **Stack** Python 3.10+ · FastAPI · SQLAlchemy · PostgreSQL · Streamlit · Plotly

---

## Environment Setup

### 1 — Clone and enter the repo

```bash
cd x-fin
```

### 2 — Create a virtual environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

### 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### 4 — Configure `.env`

```ini
DATABASE_URL=postgresql://postgres:forecast@localhost:5432/consulting_forecast
ENVIRONMENT=development
LOG_LEVEL=INFO
API_PORT=8000
```

### 5 — Set up PostgreSQL

```bash
# Create database
createdb -U postgres consulting_forecast

# Apply schema
psql -U postgres -d consulting_forecast -f app/db/schema.sql
```

### 6 — Seed data

```bash
# Generate synthetic CSV files (750 projects, 24 months)
python scripts/generate_synthetic_data.py

# Load into PostgreSQL
python scripts/load_data.py
```

---

## Running Services

### API (FastAPI)

```bash
uvicorn app.main:app --reload --port 8000
```

- OpenAPI docs: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- Health: http://127.0.0.1:8000/health

### Dashboard (Streamlit)

```bash
cd dashboard
streamlit run app.py
```

Default: http://localhost:8501

### Intelligence page

```bash
cd dashboard
streamlit run intelligence.py
```

---

## Running Tests

```bash
pytest tests/ -v
```

### Test coverage

| Test file | What it tests |
|-----------|--------------|
| `tests/test_forecast.py` | `build_forecast()` with known inputs → asserts `forecast_revenue == 142500.00` |
| `tests/test_variance.py` | `calculate_variance()` → asserts absolute and pct variances |

---

## Project Structure

```
app/
├── main.py            FastAPI application factory, router registration
├── config.py          Environment variable loading (dotenv)
├── __init__.py        Package init; loads DATABASE_URL, ENVIRONMENT, API_PORT
│
├── db/
│   ├── connection.py  SQLAlchemy engine + get_db() dependency
│   └── schema.sql     PostgreSQL DDL (DROP + CREATE)
│
├── models/
│   └── project.py     SQLAlchemy ORM model for projects table
│
├── routers/           FastAPI APIRouter modules
│   ├── analytics.py   /analytics/* (summary, monthly-revenue, backlog, variance, etc.)
│   ├── forecast.py    /forecast/current
│   ├── intelligence.py /intelligence/health + /intelligence/overview
│   ├── projects.py    /projects/*
│   └── scenarios.py   /scenarios/run
│
└── services/          Pure Python business logic (no FastAPI dependencies)
    ├── backlog_engine.py        Backlog + waterfall SQL queries
    ├── business_unit_engine.py  BU performance SQL query + calcs
    ├── finance_queries.py       Finance, pipeline, budget, monthly revenue queries
    ├── finance_reasoning.py     20+ derived metrics from 5 inputs
    ├── forecast_accuracy.py     Monthly actual vs budget accuracy series
    ├── forecast_engine.py       Deterministic forecast formula (ForecastResult dataclass)
    ├── insight_engine.py        9-rule insight scorer
    ├── recommendation_engine.py 10-rule recommendation generator
    ├── revenue_calc.py          Revenue calculation helpers
    ├── scenario_engine.py       What-if scenario calculator
    └── variance_engine.py       VarianceResult + variance_bridge
```

---

## Code Conventions

| Convention | Detail |
|-----------|--------|
| Formatting | `black` (PEP 8) |
| Linting | `flake8` |
| Imports | Absolute imports from `app.*` |
| Type hints | Used in service layer function signatures |
| SQL | Raw SQLAlchemy `text()` — no ORM queries in services |
| Precision | All financial values rounded to 2dp before returning |
| Currency | INR — ₹ symbol used in insight/recommendation messages |
| Null safety | All DB values wrapped in `float(value or 0)` before arithmetic |

---

## Dependency Table

| Package | Version | Role |
|---------|---------|------|
| `fastapi` | latest | REST API framework |
| `uvicorn` | latest | ASGI server |
| `sqlalchemy` | latest | Database ORM + raw SQL |
| `psycopg2-binary` | latest | PostgreSQL adapter |
| `pydantic` | latest | Request/response validation |
| `python-dotenv` | latest | `.env` loader |
| `pandas` | latest | Data manipulation (scripts + dashboard) |
| `numpy` | latest | Numerical operations (scripts) |
| `plotly` | latest | Interactive charts |
| `streamlit` | latest | Dashboard framework |
| `pytest` | latest | Test runner |
| `httpx` | latest | Async HTTP client (test dependency) |
| `pytest-asyncio` | latest | Async test support |
| `black` | latest | Code formatter |
| `flake8` | latest | Linter |
| `requests` | latest | HTTP client (dashboard → API) |

---

## Adding a New Endpoint

1. **Add service logic** in `app/services/`
2. **Create or update a router** in `app/routers/`
3. **Register router** in `app/main.py` via `app.include_router()`
4. **Add dashboard call** in `dashboard/api.py`
5. **Add dashboard section** in `dashboard/app.py` or a new page
6. **Write a test** in `tests/`

---

## Regenerating Synthetic Data

If you need fresh data (e.g. after schema changes):

```bash
# Drop and recreate schema
psql -U postgres -d consulting_forecast -f app/db/schema.sql

# Re-generate CSV files
python scripts/generate_synthetic_data.py

# Reload into PostgreSQL
python scripts/load_data.py
```

> **Note:** `generate_synthetic_data.py` uses `np.random.seed(42)` for reproducibility. Remove the seed for different random data.

---

## Known Limitations

| Area | Limitation |
|------|-----------|
| Backlog waterfall | `revenue_recognized` is always `null` — period-specific backlog consumption schedules are not implemented |
| Forecast current endpoint | Hard-coded utilization of `0.74` vs intelligence endpoint which uses live budget utilization |
| Forecast versions table | Schema exists but no endpoint populates it in v1.0.0 |
| Risk rate | 5% haircut is hard-coded; should be environment-configurable |
| Currency | Hard-coded INR (₹) in message strings; not internationalised |
| `dashboard/api.py` | `get_intelligence()` is defined twice (duplicate function); second definition takes precedence |
