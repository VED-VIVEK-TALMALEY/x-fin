CREATE EXTENSION IF NOT EXISTS pgcrypto;

DROP TABLE IF EXISTS forecast_values CASCADE;
DROP TABLE IF EXISTS forecast_versions CASCADE;
DROP TABLE IF EXISTS budgets CASCADE;
DROP TABLE IF EXISTS project_actuals CASCADE;
DROP TABLE IF EXISTS project_pipeline CASCADE;
DROP TABLE IF EXISTS projects CASCADE;
DROP TABLE IF EXISTS business_units CASCADE;

CREATE TABLE business_units (
    business_unit_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE projects (
    project_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_name VARCHAR(255) NOT NULL,
    client_name VARCHAR(255) NOT NULL,
    business_unit_id UUID REFERENCES business_units(business_unit_id),
    stage VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'Active',
    start_date DATE NOT NULL,
    end_date DATE,
    contract_value NUMERIC(15,2) NOT NULL,
    billing_rate NUMERIC(10,2) NOT NULL,
    planned_hours NUMERIC(12,2) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE project_pipeline (
    pipeline_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(project_id) ON DELETE CASCADE,
    snapshot_date DATE NOT NULL,
    stage VARCHAR(50) NOT NULL,
    probability NUMERIC(5,4) NOT NULL,
    expected_close_date DATE,
    pipeline_value NUMERIC(15,2) NOT NULL
);

CREATE TABLE project_actuals (
    actual_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(project_id) ON DELETE CASCADE,
    month DATE NOT NULL,
    actual_hours NUMERIC(12,2) NOT NULL,
    actual_revenue NUMERIC(15,2) NOT NULL,
    actual_cost NUMERIC(15,2) NOT NULL,
    UNIQUE(project_id, month)
);

CREATE TABLE budgets (
    budget_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    business_unit_id UUID REFERENCES business_units(business_unit_id),
    month DATE NOT NULL,
    revenue_budget NUMERIC(15,2) NOT NULL,
    hours_budget NUMERIC(12,2) NOT NULL,
    utilization_budget NUMERIC(5,2) NOT NULL,
    UNIQUE(business_unit_id, month)
);

CREATE TABLE forecast_versions (
    forecast_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    forecast_date DATE NOT NULL,
    forecast_month DATE NOT NULL,
    forecast_method VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE forecast_values (
    forecast_value_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    forecast_id UUID REFERENCES forecast_versions(forecast_id) ON DELETE CASCADE,
    project_id UUID REFERENCES projects(project_id),
    forecast_revenue NUMERIC(15,2) NOT NULL,
    confidence NUMERIC(5,4),
    UNIQUE(forecast_id, project_id)
);

CREATE INDEX idx_actuals_month ON project_actuals(month);
CREATE INDEX idx_pipeline_snapshot ON project_pipeline(snapshot_date);
CREATE INDEX idx_forecast_month ON forecast_versions(forecast_month);