# X-Fin Production Deployment & Runbook

> **Target Environment:** Render Web Services & PostgreSQL / Streamlit Community Cloud

---

## Production Deployment Topology

```mermaid
graph LR
    subgraph StreamlitCloud["Streamlit Community Cloud"]
        ST_APP["<b>Frontend Application</b><br/>https://x-finance.streamlit.app/"]
    end

    subgraph RenderPlatform["Render Cloud Infrastructure"]
        subgraph WebService["FastAPI Web Service"]
            FAST_API["<b>FastAPI ASGI Service</b><br/>https://x-fin-api.onrender.com"]
        end

        subgraph ManagedDB["Managed PostgreSQL"]
            PG_DB[("PostgreSQL 14+ Instance")]
        end
    end

    User(["Practice Leadership / Partner"]) -->|HTTPS Web Traffic| ST_APP
    ST_APP -->|Secure REST Calls (API_BASE_URL)| FAST_API
    FAST_API -->|TCP SSL :5432| PG_DB

    style StreamlitCloud fill:#EFF6FF,stroke:#2563EB,stroke-width:2px,color:#1E40AF
    style RenderPlatform fill:#F0FDF4,stroke:#16A34A,stroke-width:2px,color:#15803D
    style WebService fill:#DCFCE7,stroke:#15803D,stroke-width:1px,color:#166534
    style ManagedDB fill:#FAF5FF,stroke:#9333EA,stroke-width:1px,color:#6B21A8
    style User fill:#FEF3CD,stroke:#D97706,stroke-width:2px,color:#92400E
```

---

## Environment Configuration Matrix

| Variable Name | Environment | Sample Value | Security Level | Purpose |
|:--------------|:-----------:|:-------------|:--------------:|:--------|
| `DATABASE_URL` | Render / Backend | `postgresql://user:pass@host:5432/dbname` | **Secret** | Connection string for PostgreSQL database |
| `ENVIRONMENT` | Render / Backend | `production` | Public | Toggles production logging and strict error handling |
| `API_PORT` | Render / Backend | `8000` | Public | Target internal port for Uvicorn ASGI server |
| `API_BASE_URL` | Streamlit Cloud | `https://x-fin-api.onrender.com` | **Secret** | Base URL for frontend REST connector |

---

## Production Health Check Verification Runbook

```mermaid
flowchart TD
    subgraph Checks["HEALTH CHECK VERIFICATION PIPELINE"]
        C1["<b>1. Root & Base Health</b><br/><code>GET /</code> & <code>GET /health</code><br/>Expected: 200 OK {'status': 'healthy'}"]
        C2["<b>2. Database Connectivity</b><br/><code>GET /health/db</code><br/>Expected: 200 OK {'database': 'connected'}"]
        C3["<b>3. Financial Intelligence</b><br/><code>GET /intelligence/health</code> & <code>GET /intelligence/overview</code><br/>Expected: 200 OK with full reasoning bundle"]
        C4["<b>4. Executive Briefing</b><br/><code>GET /executive/briefing</code><br/>Expected: 200 OK with decision summary"]
    end

    C1 --> C2 --> C3 --> C4

    style Checks fill:#EFF6FF,stroke:#2563EB,stroke-width:2px,color:#1E40AF
```

### Verification Command Sequence

```bash
# Verify API service is reachable
curl -f https://x-fin-api.onrender.com/health

# Verify PostgreSQL connection pool
curl -f https://x-fin-api.onrender.com/health/db

# Verify intelligence pipeline returns status ok
curl -f https://x-fin-api.onrender.com/intelligence/health

# Verify executive briefing endpoint
curl -f https://x-fin-api.onrender.com/executive/health
```

---

## Production Data Loading & Bootstrapping

The production startup command automatically runs:

```bash
python scripts/bootstrap_db.py && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

> [!CAUTION]
> **Production Data Safety:** Do NOT execute `scripts/load_data.py` or `scripts/generate_synthetic_data.py` in production unless you intend to completely replace the active database dataset.
