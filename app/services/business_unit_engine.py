from sqlalchemy import text


def business_unit_performance(db):

    query = text("""
    WITH actuals AS (
        SELECT
            p.business_unit_id,

            COALESCE(
                SUM(a.actual_revenue),
                0
            ) AS actual_revenue,

            COALESCE(
                SUM(a.actual_cost),
                0
            ) AS actual_cost,

            COALESCE(
                SUM(a.actual_hours),
                0
            ) AS actual_hours

        FROM projects p

        LEFT JOIN project_actuals a
            ON a.project_id = p.project_id

        GROUP BY p.business_unit_id
    ),

    budgets AS (
        SELECT
            business_unit_id,

            COALESCE(
                SUM(revenue_budget),
                0
            ) AS budget_revenue,

            COALESCE(
                SUM(hours_budget),
                0
            ) AS budget_hours

        FROM budgets

        GROUP BY business_unit_id
    )

    SELECT
        bu.name AS business_unit,

        COALESCE(
            actuals.actual_revenue,
            0
        ) AS actual_revenue,

        COALESCE(
            budgets.budget_revenue,
            0
        ) AS budget_revenue,

        COALESCE(
            actuals.actual_cost,
            0
        ) AS actual_cost,

        COALESCE(
            actuals.actual_hours,
            0
        ) AS actual_hours,

        COALESCE(
            budgets.budget_hours,
            0
        ) AS budget_hours

    FROM business_units bu

    LEFT JOIN actuals
        ON actuals.business_unit_id =
           bu.business_unit_id

    LEFT JOIN budgets
        ON budgets.business_unit_id =
           bu.business_unit_id

    ORDER BY actual_revenue DESC
""")
    rows = db.execute(query).mappings().all()

    results = []

    for row in rows:

        actual = float(
            row["actual_revenue"] or 0
        )

        budget = float(
            row["budget_revenue"] or 0
        )

        cost = float(
            row["actual_cost"] or 0
        )

        variance = actual - budget

        variance_pct = (
            variance / budget * 100
            if budget
            else 0
        )

        gross_margin = actual - cost

        gross_margin_pct = (
            gross_margin / actual * 100
            if actual
            else 0
        )

        results.append({
            "business_unit": row["business_unit"],
            "actual_revenue": round(actual, 2),
            "budget_revenue": round(budget, 2),
            "variance": round(variance, 2),
            "variance_pct": round(
                variance_pct,
                2,
            ),
            "actual_cost": round(cost, 2),
            "gross_margin": round(
                gross_margin,
                2,
            ),
            "gross_margin_pct": round(
                gross_margin_pct,
                2,
            ),
            "actual_hours": round(
                float(row["actual_hours"] or 0),
                2,
            ),
            "budget_hours": round(
                float(row["budget_hours"] or 0),
                2,
            ),
        })

    return results