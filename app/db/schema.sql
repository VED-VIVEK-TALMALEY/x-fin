CREATE TABLE IF NOT EXISTS projects_backlog (
    project_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_name VARCHAR(255) NOT NULL,
    business_unit VARCHAR(100),
    client_name VARCHAR(255),
    stage VARCHAR(50),
    start_date DATE,
    end_date DATE,
    billable_hours INTEGER,
    bill_rate_per_hour DECIMAL(10, 2),
    utilization_percent DECIMAL(5, 2),
    win_probability DECIMAL(3, 2),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS monthly_actuals (
    actual_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects_backlog(project_id),
    month DATE,
    actual_billable_hours INTEGER,
    actual_revenue DECIMAL(15, 2),
    recorded_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS forecast_versions (
    forecast_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    forecast_date DATE,
    forecast_month DATE,
    project_id UUID REFERENCES projects_backlog(project_id),
    forecast_revenue DECIMAL(15, 2),
    model_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);