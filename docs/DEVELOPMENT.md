# X-Fin Developer & Operations Manual

> **Technology Stack:** Python 3.10+ · FastAPI · PostgreSQL 14+ / SQLite Fallback · Streamlit · SQLAlchemy · Plotly · Pytest

---

## Local Development Lifecycle

```mermaid
flowchart LR
    subgraph S1["1. ENVIRONMENT INITIALIZATION"]
        V["Create Virtualenv<br/><code>python -m venv .venv</code>"]
        I["Install Dependencies<br/><code>pip install -r requirements.txt</code>"]
        V --> I
    end

    subgraph S2["2. DATA FOUNDATION"]
        D["Apply PostgreSQL DDL (Optional)<br/><code>psql -f app/db/schema.sql</code>"]
        G["Generate Synthetic Data<br/><code>python scripts/generate_synthetic_data.py</code>"]
        L["Load Database Tables<br/><code>python scripts/load_data.py</code>"]
        D --> G --> L
    end

    subgraph S3["3. APPLICATION RUNTIME"]
        API["Launch FastAPI Server<br/><code>uvicorn app.main:app --port 8000</code>"]
        UI["Launch Streamlit Decision UI<br/><code>streamlit run dashboard/app.py</code>"]
    end

    subgraph S4["4. AUTOMATED VERIFICATION"]
        T["Execute Pytest Suite<br/><code>pytest tests/ -v</code>"]
    end

    S1 --> S2 --> S3 --> S4

    style S1 fill:#EFF6FF,stroke:#2563EB,stroke-width:2px,color:#1E40AF
    style S2 fill:#FDF4FF,stroke:#C026D3,stroke-width:2px,color:#86198F
    style S3 fill:#F0FDF4,stroke:#16A34A,stroke-width:2px,color:#15803D
    style S4 fill:#ECFDF5,stroke:#059669,stroke-width:2px,color:#065F46
```

---

## Automated Pytest Suite Specification

```mermaid
graph TD
    subgraph Suite["Automated Pytest Framework"]
        T1["tests/test_forecast.py"]
        T2["tests/test_variance.py"]
    end

    subgraph Trace["Test Verification Assertions"]
        C1["<b>test_forecast:</b><br/>• Committed Backlog = INR 100,000.00<br/>• Weighted Pipeline = INR 50,000.00<br/>• Actual Util = 0.75, Target Util = 0.75<br/>• Risk Haircut = 5% (0.05)<br/>Asserts: forecast_revenue == INR 142,500.00"]
        C2["<b>test_variance:</b><br/>• Actual = 90.00, Budget = 100.00, Forecast = 95.00<br/>Asserts: Actual Variance == -10.00 (-10.00%)<br/>Asserts: Forecast Variance == -5.00 (-5.00%)"]
    end

    T1 --> C1
    T2 --> C2

    style Suite fill:#EFF6FF,stroke:#2563EB,stroke-width:2px,color:#1E40AF
    style Trace fill:#ECFDF5,stroke:#059669,stroke-width:2px,color:#065F46
```

### Run Test Suite

```bash
# Run all unit and integration tests with verbose output
python -m pytest tests/ -v
```

---

## Dependency Specification Matrix

| Package Name | Minimum Version | Architectural Role | Layer Categorization |
|:-------------|:---------------:|:-------------------|:---------------------|
| `fastapi` | `0.115.0+` | ASGI Web Framework & Routing | API Gateway |
| `uvicorn` | `0.30.0+` | High-performance ASGI Web Server | Infrastructure |
| `pydantic` | `2.8.0+` | Request / Response Schema Validation | Core Type Safety |
| `sqlalchemy` | `2.0.0+` | Database Connection Pooling & Queries | Data Persistence |
| `psycopg2-binary` | `2.9.9+` | PostgreSQL Database Adapter | Data Persistence |
| `streamlit` | `1.40.0+` | Executive Decision Surface & UI | Presentation |
| `plotly` | `5.24.0+` | Interactive Visualizations & Charts | Presentation |
| `pandas` | `2.2.0+` | Table & Matrix Data Manipulations | Analytics Engine |
| `pytest` | `8.3.0+` | Automated Test Runner & Assertions | Quality Assurance |
| `requests` | `2.32.0+` | Internal HTTP Client for Dashboard | Presentation Client |

---

## Code Quality & Contribution Standards

1. **Pure Python Engines:** All calculation logic in `app/services` must remain pure Python with zero dependencies on FastAPI HTTP request contexts.
2. **Deterministic Reproducibility:** Monte Carlo simulations and stochastic routines must use explicit random seeds (`seed=42`) for testing reproducibility.
3. **Data Quality Awareness:** Never present proxy calculations as authoritative metrics without explicit warning flags.
