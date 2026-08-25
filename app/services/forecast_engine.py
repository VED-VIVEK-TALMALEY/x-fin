from dataclasses import dataclass


@dataclass
class ForecastResult:
    committed_backlog: float
    weighted_pipeline: float
    utilization_adjustment: float
    risk_adjustment: float
    forecast_revenue: float

    @property
    def decomposition(self):
        return {
            "committed_backlog": round(
                self.committed_backlog,
                2,
            ),
            "weighted_pipeline": round(
                self.weighted_pipeline,
                2,
            ),
            "utilization_adjustment": round(
                self.utilization_adjustment,
                2,
            ),
            "risk_adjustment": round(
                self.risk_adjustment,
                2,
            ),
            "forecast_revenue": round(
                self.forecast_revenue,
                2,
            ),
        }


def build_forecast(
    committed_backlog: float,
    weighted_pipeline: float,
    utilization: float,
    target_utilization: float = 0.75,
    risk_rate: float = 0.05,
) -> ForecastResult:
    """
    Build the deterministic revenue forecast.

    Forecast logic:

        Forward Revenue
        = Committed Backlog
        + Weighted Pipeline

        Utilization Adjustment
        = Forward Revenue
        * (Utilization - Target Utilization)

        Risk Adjustment
        = Forward Revenue
        * Risk Rate

        Forecast Revenue
        = Forward Revenue
        + Utilization Adjustment
        - Risk Adjustment

    All monetary values are expected in the same currency/unit.
    Utilization values are decimal percentages:
        0.75 = 75%
    """

    committed_backlog = float(
        committed_backlog or 0
    )

    weighted_pipeline = float(
        weighted_pipeline or 0
    )

    utilization = float(
        utilization or 0
    )

    target_utilization = float(
        target_utilization or 0
    )

    risk_rate = float(
        risk_rate or 0
    )

    forward_revenue = (
        committed_backlog
        + weighted_pipeline
    )

    utilization_delta = (
        utilization
        - target_utilization
    )

    utilization_adjustment = (
        forward_revenue
        * utilization_delta
    )

    risk_adjustment = (
        forward_revenue
        * risk_rate
    )

    forecast_revenue = (
        forward_revenue
        + utilization_adjustment
        - risk_adjustment
    )

    return ForecastResult(
        committed_backlog=committed_backlog,
        weighted_pipeline=weighted_pipeline,
        utilization_adjustment=utilization_adjustment,
        risk_adjustment=risk_adjustment,
        forecast_revenue=forecast_revenue,
    )


def calculate_forecast_accuracy(db):
    """
    Calculate historical actual-vs-budget performance by month.

    Kept here for compatibility with the existing dashboard/API.
    """

    from sqlalchemy import text

    query = text(
        """
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
        """
    )

    rows = db.execute(
        query
    ).mappings().all()

    results = []

    for row in rows:
        results.append(
            {
                "month": row["month"],
                "actual_revenue": float(
                    row["actual_revenue"] or 0
                ),
                "budget_revenue": float(
                    row["budget_revenue"] or 0
                ),
                "variance_pct": round(
                    float(
                        row["variance_pct"] or 0
                    ),
                    2,
                ),
            }
        )

    return results