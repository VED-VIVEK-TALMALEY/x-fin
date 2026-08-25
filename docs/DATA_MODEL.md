# X-Fin — Data Model

> **Database** PostgreSQL >= 14 · **ORM** SQLAlchemy · **Schema** `app/db/schema.sql`

---

## Entity Relationship Diagram

```
business_units
┌──────────────────────────────┐
│ business_unit_id  UUID  PK   │
│ name              VARCHAR    │
└──────────┬───────────────────┘
           │  1
           │  *
           ▼
       projects
┌────────────────────────────────────────┐
│ project_id       UUID  PK              │
│ project_name     VARCHAR               │
│ client_name      VARCHAR               │
│ business_unit_id UUID  FK              │
│ stage            VARCHAR               │
│ status           VARCHAR  default=Active│
│ start_date       DATE                  │
│ end_date         DATE                  │
│ contract_value   NUMERIC(15,2)         │
│ billing_rate     NUMERIC(10,2)         │
│ planned_hours    NUMERIC(12,2)         │
│ created_at       TIMESTAMP             │
└────┬─────────────────────┬─────────────┘
     │                     │
     │ 1                   │ 1
     │ *                   │ *
     ▼                     ▼
project_pipeline       project_actuals
┌────────────────────┐  ┌───────────────────────┐
│ pipeline_id  UUID  │  │ actual_id   UUID  PK   │
│ project_id   UUID  │  │ project_id  UUID  FK   │
│ snapshot_date DATE │  │ month       DATE        │
│ stage        VCHAR │  │ actual_hours  NUM(12,2) │
│ probability  NUM   │  │ actual_revenue NUM(15,2)│
│ expected_close DATE│  │ actual_cost   NUM(15,2) │
│ pipeline_value NUM │  └───────────────────────-┘
└────────────────────┘

business_units
┌──────────────────┐
│ business_unit_id │──────────────────────┐
└──────────────────┘                      │
                                          │ 1
                                          │ *
                                          ▼
                                       budgets
                            ┌────────────────────────────────────┐
                            │ budget_id          UUID  PK         │
                            │ business_unit_id   UUID  FK         │
                            │ month              DATE              │
                            │ revenue_budget     NUMERIC(15,2)    │
                            │ hours_budget       NUMERIC(12,2)    │
                            │ utilization_budget NUMERIC(5,2)     │
                            │ UNIQUE(business_unit_id, month)     │
                            └────────────────────────────────────┘

forecast_versions (1) ──* forecast_values (*) ──1 projects
┌──────────────────────┐   ┌───────────────────────────────┐
│ forecast_id  UUID PK │   │ forecast_value_id UUID PK     │
│ forecast_date DATE   │   │ forecast_id  UUID  FK         │
│ forecast_month DATE  │   │ project_id   UUID  FK         │
│ forecast_method VCHAR│   │ forecast_revenue NUMERIC(15,2)│
│ created_at TIMESTAMP │   │ confidence   NUMERIC(5,4)     │
└──────────────────────┘   └───────────────────────────────┘
```

---

## Tables

### `business_units`

Master table of delivery business units.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `business_unit_id` | UUID | PK, default gen_random_uuid() | Surrogate key |
| `name` | VARCHAR(100) | UNIQUE, NOT NULL | BU display name |

**Seed values:** `X Build`, `X Design`, `Digital Ventures`

---

### `projects`

Core project master, one row per project.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `project_id` | UUID | PK | Surrogate key |
| `project_name` | VARCHAR(255) | NOT NULL | Display name |
| `client_name` | VARCHAR(255) | NOT NULL | Client name |
| `business_unit_id` | UUID | FK → business_units | Parent BU |
| `stage` | VARCHAR(50) | NOT NULL | Pipeline stage |
| `status` | VARCHAR(50) | default=`Active` | Project status |
| `start_date` | DATE | NOT NULL | Engagement start |
| `end_date` | DATE | — | Planned end |
| `contract_value` | NUMERIC(15,2) | NOT NULL | Total contract value |
| `billing_rate` | NUMERIC(10,2) | NOT NULL | ₹/hour billing rate |
| `planned_hours` | NUMERIC(12,2) | NOT NULL | Total planned hours |
| `created_at` | TIMESTAMP | default=NOW() | Record creation |

**Stage values**

| Stage | Meaning | Probability |
|-------|---------|-------------|
| `Prospect` | Early interest | 0.15 |
| `Qualified` | Qualified opportunity | 0.35 |
| `In Delivery` | Active engagement | 0.75 |
| `Closed Won` | Won / completed | 1.00 |
| `Closed Lost` | Lost | 0.00 |

---

### `project_pipeline`

Snapshot-based pipeline register. Each project can have multiple rows — one per snapshot date. The system always reads from the **most recent snapshot**.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `pipeline_id` | UUID | PK | Surrogate key |
| `project_id` | UUID | FK → projects CASCADE | Parent project |
| `snapshot_date` | DATE | NOT NULL | Date of snapshot |
| `stage` | VARCHAR(50) | NOT NULL | Stage at snapshot |
| `probability` | NUMERIC(5,4) | NOT NULL | Win probability (0–1) |
| `expected_close_date` | DATE | — | Predicted close |
| `pipeline_value` | NUMERIC(15,2) | NOT NULL | Contract value at snapshot |

**Index:** `idx_pipeline_snapshot` on `snapshot_date`

**Backlog classification:**

```
committed_backlog    = SUM(pipeline_value) WHERE stage IN ('In Delivery', 'Closed Won')
uncommitted_pipeline = SUM(pipeline_value) WHERE stage IN ('Prospect', 'Qualified')
weighted_pipeline    = SUM(pipeline_value * probability)   -- all stages
```

---

### `project_actuals`

Monthly financial actuals per project. One row per (project, month).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `actual_id` | UUID | PK | Surrogate key |
| `project_id` | UUID | FK → projects CASCADE | Parent project |
| `month` | DATE | NOT NULL | Month start date |
| `actual_hours` | NUMERIC(12,2) | NOT NULL | Hours delivered |
| `actual_revenue` | NUMERIC(15,2) | NOT NULL | Revenue recognised |
| `actual_cost` | NUMERIC(15,2) | NOT NULL | Delivery cost |

**Unique constraint:** `(project_id, month)`

**Index:** `idx_actuals_month` on `month`

---

### `budgets`

Monthly budget targets per business unit.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `budget_id` | UUID | PK | Surrogate key |
| `business_unit_id` | UUID | FK → business_units | Parent BU |
| `month` | DATE | NOT NULL | Month start |
| `revenue_budget` | NUMERIC(15,2) | NOT NULL | Revenue target |
| `hours_budget` | NUMERIC(12,2) | NOT NULL | Hours target |
| `utilization_budget` | NUMERIC(5,2) | NOT NULL | Target utilization rate |

**Unique constraint:** `(business_unit_id, month)`

---

### `forecast_versions`

Audit trail of forecast runs (future extensibility).

| Column | Type | Description |
|--------|------|-------------|
| `forecast_id` | UUID | PK |
| `forecast_date` | DATE | Date forecast was produced |
| `forecast_month` | DATE | Month being forecast |
| `forecast_method` | VARCHAR(100) | Method identifier |
| `created_at` | TIMESTAMP | Creation timestamp |

**Index:** `idx_forecast_month` on `forecast_month`

---

### `forecast_values`

Per-project forecast values linked to a forecast version.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `forecast_value_id` | UUID | PK | Surrogate key |
| `forecast_id` | UUID | FK → forecast_versions CASCADE | Parent forecast |
| `project_id` | UUID | FK → projects | Project |
| `forecast_revenue` | NUMERIC(15,2) | NOT NULL | Projected revenue |
| `confidence` | NUMERIC(5,4) | — | Statistical confidence (0–1) |

**Unique constraint:** `(forecast_id, project_id)`

---

## Synthetic Data Generator

`scripts/generate_synthetic_data.py` creates realistic test data:

| Dataset | Records | Notes |
|---------|---------|-------|
| Projects | 750 | Random BU, stage, billing rate, hours |
| Pipeline | 750 × 6 months | Monthly snapshots per project |
| Actuals | 750 × 24 months | Monthly revenue, hours, cost per project |
| Budgets | 3 BUs × 24 months | Random ₹4M–₹10M monthly budget per BU |

**Stage distribution** (approx)

| Stage | Weight |
|-------|--------|
| Prospect | 20% |
| Qualified | 25% |
| In Delivery | 25% |
| Closed Won | 25% |
| Closed Lost | 5% |

**Billing rates used:** ₹150, ₹200, ₹250, ₹300, ₹350, ₹400 per hour
