from sqlalchemy import text


def get_finance_summary(db):

    query = text("""
        SELECT
            COALESCE(SUM(a.actual_revenue), 0) AS actual_revenue,
            COALESCE(SUM(a.actual_cost), 0) AS actual_cost,
            COALESCE(SUM(p.contract_value), 0) AS contract_value,
            COALESCE(SUM(p.planned_hours), 0) AS planned_hours
        FROM projects p
        LEFT JOIN project_actuals a
            ON p.project_id = a.project_id
    """)

    row = db.execute(query).mappings().first()

    return dict(row)


def get_pipeline_summary(db):

    query = text("""
        SELECT
            COUNT(*) AS opportunities,
            COALESCE(SUM(pipeline_value), 0) AS pipeline_value,
            COALESCE(
                SUM(pipeline_value * probability),
                0
            ) AS weighted_pipeline
        FROM project_pipeline
        WHERE snapshot_date = (
            SELECT MAX(snapshot_date)
            FROM project_pipeline
        )
    """)

    row = db.execute(query).mappings().first()

    return dict(row)


def get_budget_summary(db):

    query = text("""
        SELECT
            COALESCE(SUM(revenue_budget), 0) AS budget_revenue,
            COALESCE(SUM(hours_budget), 0) AS budget_hours,
            COALESCE(AVG(utilization_budget), 0)
                AS budget_utilization
        FROM budgets
    """)

    row = db.execute(query).mappings().first()

    return dict(row)


def get_monthly_revenue(db):

    query = text("""
        SELECT
            DATE_TRUNC('month', month) AS month,
            SUM(actual_revenue) AS revenue,
            SUM(actual_hours) AS hours,
            SUM(actual_cost) AS cost
        FROM project_actuals
        GROUP BY DATE_TRUNC('month', month)
        ORDER BY month
    """)

    return [
        dict(row)
        for row in db.execute(query).mappings().all()
    ]