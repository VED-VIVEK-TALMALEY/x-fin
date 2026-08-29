# X-Fin Production Runbook

## Production topology

X-Fin uses a two-service deployment:

- **Frontend:** Streamlit Community Cloud
- **Backend:** FastAPI on Render
- **Database:** PostgreSQL managed by Render

Production API:

`https://x-fin-api.onrender.com`

Frontend:

`https://x-finance.streamlit.app/`

The Streamlit frontend must use `API_BASE_URL` pointing to the Render API. It must not fall back to `127.0.0.1:8000` in production.

## Render API configuration

Required environment variables:

```text
DATABASE_URL=<Render PostgreSQL connection string>
ENVIRONMENT=production
```

`DATABASE_URL` must be the current Render PostgreSQL connection string. Do not commit the database URL to Git.

The application normalizes `postgres://` and `postgresql://` URLs to the SQLAlchemy `postgresql+psycopg2://` form.

## Streamlit configuration

In Streamlit Community Cloud, configure:

```toml
API_BASE_URL = "https://x-fin-api.onrender.com"
```

Keep this value in Streamlit Secrets rather than hard-coding the production URL into application code.

## Deployment checks

After deploying the API:

```text
GET /
GET /health
GET /health/db
GET /intelligence/health
GET /analytics/summary
GET /analytics/monthly-revenue
GET /analytics/backlog
GET /analytics/variance
GET /analytics/forecast-accuracy
GET /analytics/business-units
GET /forecast/current
GET /intelligence/overview
```

The core endpoints should return HTTP 200.

After deploying the Streamlit frontend, verify that the dashboard no longer reports:

```text
127.0.0.1:8000
```

If it does, check that `API_BASE_URL` exists in Streamlit Secrets and that the latest frontend commit has been pushed.

## Data loading

The production startup command runs:

```bash
python scripts/bootstrap_db.py
```

followed by Uvicorn.

Do not run the full synthetic data loader automatically on every deployment unless replacing the production dataset is intentional.

## Git hygiene

The repository ignores:

- virtual environments
- `.env` files
- Streamlit secrets
- local databases
- logs
- Python caches
- build artifacts

If a secret or virtual environment was committed previously, `.gitignore` alone is not sufficient. Remove the tracked files and rewrite Git history if the sensitive material must disappear from repository history.

## Staffing-model limitation

The current schema contains `hours_budget` and `utilization_budget`, but not a true capacity-hours denominator.

Therefore:

- `actual_hours / budget_hours` is **hours attainment**, not utilization.
- `actual_utilization` remains unavailable.
- bench hours and bench percentage remain unavailable.
- management-facing staffing conclusions should explicitly carry the data-quality limitation.

This is intentional model governance: the system does not fabricate utilization from an invalid denominator.

## Pre-release validation

Run:

```bash
pytest tests/ -v
```

Then perform a production smoke test against:

```text
https://x-fin-api.onrender.com/health
https://x-fin-api.onrender.com/intelligence/overview
```

Finally open the Streamlit application and verify KPI cards, forecast, risk, scenarios, charts, and intelligence panels.
