# X-Fin Developer & Operations Manual

> **Technology Stack:** Python 3.10+ · FastAPI · PostgreSQL 14+ · Streamlit · SQLAlchemy · Plotly

---

## Local Development Lifecycle

```mermaid
flowchart LR
    subgraph S1["1. ENVIRONMENT"]
        V["Create Virtualenv<br/><code>python -m venv .venv</code>"]
        I["Install Dependencies<br/><code>pip install -r requirements.txt</code>"]
        V --> I
    end

    subgraph S2["2. DATABASE SETUP"]
        D["Execute Schema DDL<br/><code>psql -f app/db/schema.sql</code>"]
        G["Generate Synthetic Data<br/><code>python scripts/generate_synthetic_data.py</code>"]
        L["Load Database Tables<br/><code>python scripts/load_data.py</code>"]
        D --> G --> L
    end

    subgraph S3["3. APPLICATION RUNTIME"]
        API["Launch FastAPI Server<br/><code>uvicorn app.main:app --port 8000</code>"]
        UI["Launch Streamlit UI<br/><code>streamlit run dashboard/app.py</code>"]
    end

    subgraph S4["4. AUTOMATED VERIFICATION"]
        T["Execute Pytest Suite<br/><code>pytest tests/ -v</code>"]
    end

    S1 --> S2 --> S3 --> S4
```

---

## Automated Verification Suite

```mermaid
graph TD
    subgraph Suite["Automated Pytest Framework"]
        T1["tests/test_forecast.py"]
        T2["tests/test_variance.py"]
    end

    subgraph Trace["Test Verification Logic"]
        C1["<b>test_forecast:</b><br/>• Committed Backlog = INR 100,000.00<br/>• Weighted Pipeline = INR 50,000.00<br/>• Actual Util = 0.75, Target Util = 0.75<br/>• Risk Haircut = 5% (0.05)<br/>Result: Asserts forecast_revenue == INR 142,500.00"]
        C2["<b>test_variance:</b><br/>• Actual = 90.00, Budget = 100.00, Forecast = 95.00<br/>Result: Asserts Actual Variance == -10.00 (-10.00%)<br/>Result: Asserts Forecast Variance == -5.00 (-5.00%)"]
    end

    T1 --> C1
    T2 --> C2
```

Run test suite:
```bash
pytest tests/ -v
```

---

## Dependency Matrix

```mermaid
pie title Dependencies by Architecture Layer
    "API & Web Framework (FastAPI, Uvicorn, Pydantic, Requests)" : 30
    "Database & ORM (SQLAlchemy, psycopg2-binary)" : 20
    "Data & Numerical Ops (Pandas, Numpy)" : 20
    "Visualization & UI (Streamlit, Plotly)" : 20
    "Testing & Quality (Pytest, HTTPX, Black, Flake8)" : 10
```

| Package Name | Minimum Version | Architectural Role | Layer Categorization |
|:-------------|:---------------:|:-------------------|:---------------------|
| `fastapi` | `0.115.0+` | Asynchronous REST API framework | API Gateway |
| `uvicorn` | `0.30.0+` | Production ASGI web server | API Gateway |
| `sqlalchemy` | `2.0.0+` | Database abstraction and raw SQL engine | Persistence |
| `psycopg2-binary` | `2.9.9+` | PostgreSQL database driver adapter | Persistence |
| `pydantic` | `2.8.0+` | Data schema validation and serialisation | API Gateway |
| `pandas` | `2.2.0+` | Tabular data transformations | Analytics & Logic |
| `numpy` | `1.26.0+` | Mathematical operations & distributions | Analytics & Logic |
| `plotly` | `5.22.0+` | Interactive visual charting engine | Presentation |
| `streamlit` | `1.36.0+` | Reactive executive dashboard frontend | Presentation |
| `pytest` | `8.2.0+` | Test execution runner | Quality & Testing |
| `httpx` | `0.27.0+` | Asynchronous test HTTP client | Quality & Testing |
| `requests` | `2.32.0+` | HTTP client for Streamlit UI connector | Presentation |

---

## New Endpoint Development Workflow

```mermaid
sequenceDiagram
    autonumber
    participant S as app/services/
    participant R as app/routers/
    participant M as app/main.py
    participant D as dashboard/api.py
    participant UI as dashboard/app.py
    participant T as tests/

    Note over S: 1. Write pure calculation function in services/
    Note over R: 2. Expose endpoint in routers/ with Pydantic model
    Note over M: 3. Register router in app/main.py
    Note over D: 4. Add HTTP request wrapper in dashboard/api.py
    Note over UI: 5. Build Streamlit metric cards and Plotly charts
    Note over T: 6. Add automated regression unit test in tests/
```
