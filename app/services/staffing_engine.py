from typing import Dict

from sqlalchemy import text


def calculate_staffing_position(db) -> Dict:
    """
    Calculate staffing economics using only quantities supported by
    the current database schema.

    Important modeling constraint:
    the schema contains hours_budget and utilization_budget, but it
    does not contain a capacity-hours denominator. Therefore
    actual_hours / budget_hours is reported as HOURS ATTAINMENT,
    not as actual utilization.

    This avoids incorrectly reporting figures such as 181.4% as
    "utilization" when the underlying denominator is not capacity.
    """

    query = text(
        """
        WITH actuals AS (
            SELECT
                COALESCE(SUM(actual_hours), 0) AS actual_hours,
                COALESCE(SUM(actual_cost), 0) AS actual_cost,
                COALESCE(SUM(actual_revenue), 0) AS actual_revenue
            FROM project_actuals
        ),
        budgets AS (
            SELECT
                COALESCE(SUM(hours_budget), 0) AS budget_hours,
                COALESCE(AVG(utilization_budget), 0)
                    AS budget_utilization
            FROM budgets
        )
        SELECT
            actuals.actual_hours,
            actuals.actual_cost,
            actuals.actual_revenue,
            budgets.budget_hours,
            budgets.budget_utilization
        FROM actuals
        CROSS JOIN budgets
        """
    )

    row = db.execute(query).mappings().one()

    actual_hours = float(row["actual_hours"] or 0)
    budget_hours = float(row["budget_hours"] or 0)
    actual_cost = float(row["actual_cost"] or 0)
    actual_revenue = float(row["actual_revenue"] or 0)
    raw_budget_utilization = float(row["budget_utilization"] or 0)

    budget_utilization = (
        raw_budget_utilization * 100
        if raw_budget_utilization <= 1
        else raw_budget_utilization
    )

    # This is NOT utilization. It is hours delivered relative to
    # the hours budget.
    hours_attainment_pct = (
        actual_hours / budget_hours * 100
        if budget_hours > 0
        else 0.0
    )

    hours_variance = actual_hours - budget_hours
    hours_variance_pct = (
        hours_variance / budget_hours * 100
        if budget_hours > 0
        else 0.0
    )

    # Without capacity hours we cannot infer true bench capacity.
    # Keep bench metrics unavailable rather than inventing them.
    bench_hours = None
    bench_percentage = None
    estimated_bench_cost = None
    potential_revenue = None
    bench_margin_exposure = None

    if actual_hours > 0:
        blended_cost_per_hour = actual_cost / actual_hours
        realized_revenue_per_hour = actual_revenue / actual_hours
    else:
        blended_cost_per_hour = 0.0
        realized_revenue_per_hour = 0.0

    # Capacity status is based on hours attainment, with a data-quality
    # qualifier because hours attainment is not utilization.
    if hours_attainment_pct >= 120:
        capacity_status = "hours_above_budget_review_required"
    elif hours_attainment_pct >= 100:
        capacity_status = "hours_at_or_above_budget"
    elif hours_attainment_pct >= 85:
        capacity_status = "hours_near_budget"
    else:
        capacity_status = "hours_below_budget"

    utilization_data_quality = (
        "review_required"
        if budget_hours > 0 and hours_attainment_pct > 120
        else "limited"
        if budget_hours > 0
        else "missing_capacity_denominator"
    )

    return {
        "actual_hours": round(actual_hours, 2),
        "budget_hours": round(budget_hours, 2),
        "hours_attainment_pct": round(hours_attainment_pct, 2),
        "hours_variance": round(hours_variance, 2),
        "hours_variance_pct": round(hours_variance_pct, 2),
        "actual_utilization": None,
        "budget_utilization": round(budget_utilization, 2),
        "utilization_gap": None,
        "bench_hours": bench_hours,
        "bench_percentage": bench_percentage,
        "actual_cost": round(actual_cost, 2),
        "blended_cost_per_hour": round(blended_cost_per_hour, 2),
        "estimated_bench_cost": estimated_bench_cost,
        "actual_revenue": round(actual_revenue, 2),
        "realized_revenue_per_hour": round(
            realized_revenue_per_hour, 2
        ),
        "potential_revenue": potential_revenue,
        "bench_margin_exposure": bench_margin_exposure,
        "capacity_status": capacity_status,
        "bench_risk": "unknown",
        "utilization_data_quality": utilization_data_quality,
        "capacity_measurement_note": (
            "True utilization/bench requires a capacity-hours "
            "denominator that is not currently present in the schema."
        ),
    }
