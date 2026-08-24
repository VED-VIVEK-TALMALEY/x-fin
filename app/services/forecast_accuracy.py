from sqlalchemy import text


def calculate_forecast_accuracy(db):

    query = text("""
        WITH monthly_actuals AS (
            SELECT
                DATE_TRUNC('month', month) AS month,
                SUM(actual_revenue) AS actual_revenue
            FROM project_actuals
            GROUP BY DATE_TRUNC('month', month)
        ),

        monthly_budgets AS (
            SELECT
                DATE_TRUNC('month', month) AS month,
                SUM(revenue_budget) AS budget_revenue
            FROM budgets
            GROUP BY DATE_TRUNC('month', month)
        )

        SELECT
            a.month,
            a.actual_revenue,
            b.budget_revenue,

            CASE
                WHEN b.budget_revenue = 0
                THEN 0

                ELSE
                    (
                        a.actual_revenue
                        - b.budget_revenue
                    )
                    / b.budget_revenue
                    * 100
            END AS variance_pct

        FROM monthly_actuals a

        LEFT JOIN monthly_budgets b
            ON a.month = b.month

        ORDER BY a.month
    """)

    rows = db.execute(
        query
    ).mappings().all()

    results = []

    for row in rows:

        results.append({
            "month": row["month"],
            "actual_revenue": float(
                row["actual_revenue"] or 0
            ),
            "budget_revenue": float(
                row["budget_revenue"] or 0
            ),
            "variance_pct": round(
                float(row["variance_pct"] or 0),
                2,
            ),
        })

    return results