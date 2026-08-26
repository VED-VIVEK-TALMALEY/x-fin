from typing import Dict, Optional

import numpy as np


def run_monte_carlo_forecast(
    *,
    actual_revenue: float,
    budget_revenue: float,
    committed_backlog: float,
    weighted_pipeline: float,
    utilization_adjustment: float = 0.0,
    risk_adjustment: float = 0.0,
    iterations: int = 5000,
    random_seed: int = 42,
    pipeline_volatility: float = 0.15,
    backlog_volatility: float = 0.05,
    utilization_volatility: float = 0.05,
    risk_volatility: float = 0.20,
) -> Dict:
    """
    Monte Carlo forecast engine for X-Fin.

    The model starts from the deterministic forecast structure:

        Forecast =
            Committed Backlog
            + Weighted Pipeline
            + Utilization Adjustment
            - Risk Adjustment

    Each simulation introduces controlled uncertainty around:

        1. Committed backlog realization
        2. Weighted pipeline realization
        3. Utilization adjustment
        4. Execution / delivery risk

    Outputs:

        P10
        P25
        P50
        P75
        P90
        mean
        standard deviation
        probability of beating budget
        probability of missing budget
        downside vs budget
        upside vs budget
    """

    # --------------------------------------------------
    # INPUT NORMALIZATION
    # --------------------------------------------------

    actual_revenue = float(actual_revenue or 0.0)
    budget_revenue = float(budget_revenue or 0.0)
    committed_backlog = float(committed_backlog or 0.0)
    weighted_pipeline = float(weighted_pipeline or 0.0)
    utilization_adjustment = float(
        utilization_adjustment or 0.0
    )
    risk_adjustment = float(
        risk_adjustment or 0.0
    )

    iterations = int(iterations)

    if iterations < 100:
        raise ValueError(
            "iterations must be at least 100"
        )

    if iterations > 100_000:
        raise ValueError(
            "iterations cannot exceed 100000"
        )

    # --------------------------------------------------
    # VALIDATE VOLATILITY
    # --------------------------------------------------

    volatility_values = {
        "pipeline_volatility": pipeline_volatility,
        "backlog_volatility": backlog_volatility,
        "utilization_volatility": utilization_volatility,
        "risk_volatility": risk_volatility,
    }

    for name, value in volatility_values.items():

        if value < 0:
            raise ValueError(
                f"{name} cannot be negative"
            )

    # --------------------------------------------------
    # RANDOM GENERATOR
    # --------------------------------------------------

    rng = np.random.default_rng(
        random_seed
    )

    # --------------------------------------------------
    # 1. COMMITTED BACKLOG
    # --------------------------------------------------

    # Committed backlog has relatively low volatility.
    #
    # Example:
    #
    # ₹274M committed backlog
    # ±5% uncertainty
    #
    # The result is clipped at zero because revenue
    # cannot become negative.

    backlog_factor = rng.normal(
        loc=1.0,
        scale=backlog_volatility,
        size=iterations,
    )

    backlog_factor = np.clip(
        backlog_factor,
        0.0,
        None,
    )

    simulated_backlog = (
        committed_backlog
        * backlog_factor
    )

    # --------------------------------------------------
    # 2. WEIGHTED PIPELINE
    # --------------------------------------------------

    # Pipeline is inherently more uncertain than
    # committed backlog.

    pipeline_factor = rng.normal(
        loc=1.0,
        scale=pipeline_volatility,
        size=iterations,
    )

    pipeline_factor = np.clip(
        pipeline_factor,
        0.0,
        None,
    )

    simulated_pipeline = (
        weighted_pipeline
        * pipeline_factor
    )

    # --------------------------------------------------
    # 3. UTILIZATION ADJUSTMENT
    # --------------------------------------------------

    utilization_noise = rng.normal(
        loc=0.0,
        scale=abs(
            utilization_adjustment
            * utilization_volatility
        ),
        size=iterations,
    )

    simulated_utilization = (
        utilization_adjustment
        + utilization_noise
    )

    # --------------------------------------------------
    # 4. EXECUTION / DELIVERY RISK
    # --------------------------------------------------

    # Risk adjustment is treated as a negative
    # contribution to forecast revenue.

    risk_noise = rng.normal(
        loc=0.0,
        scale=abs(
            risk_adjustment
            * risk_volatility
        ),
        size=iterations,
    )

    simulated_risk = (
        risk_adjustment
        + risk_noise
    )

    # Risk cannot become negative.

    simulated_risk = np.clip(
        simulated_risk,
        0.0,
        None,
    )

    # --------------------------------------------------
    # 5. TOTAL SIMULATED FORECAST
    # --------------------------------------------------

    simulated_forecast = (
        simulated_backlog
        + simulated_pipeline
        + simulated_utilization
        - simulated_risk
    )

    simulated_forecast = np.maximum(
        simulated_forecast,
        0.0,
    )

    # --------------------------------------------------
    # DISTRIBUTION STATISTICS
    # --------------------------------------------------

    p10 = float(
        np.percentile(
            simulated_forecast,
            10,
        )
    )

    p25 = float(
        np.percentile(
            simulated_forecast,
            25,
        )
    )

    p50 = float(
        np.percentile(
            simulated_forecast,
            50,
        )
    )

    p75 = float(
        np.percentile(
            simulated_forecast,
            75,
        )
    )

    p90 = float(
        np.percentile(
            simulated_forecast,
            90,
        )
    )

    mean_forecast = float(
        np.mean(
            simulated_forecast
        )
    )

    std_forecast = float(
        np.std(
            simulated_forecast
        )
    )

    # --------------------------------------------------
    # BUDGET PROBABILITIES
    # --------------------------------------------------

    if budget_revenue > 0:

        probability_above_budget = float(
            np.mean(
                simulated_forecast
                >= budget_revenue
            )
            * 100
        )

        probability_below_budget = float(
            np.mean(
                simulated_forecast
                < budget_revenue
            )
            * 100
        )

    else:

        probability_above_budget = 0.0
        probability_below_budget = 0.0

    # --------------------------------------------------
    # UPSIDE / DOWNSIDE
    # --------------------------------------------------

    if budget_revenue > 0:

        downside_vs_budget = (
            p10
            - budget_revenue
        )

        upside_vs_budget = (
            p90
            - budget_revenue
        )

        median_vs_budget = (
            p50
            - budget_revenue
        )

    else:

        downside_vs_budget = 0.0
        upside_vs_budget = 0.0
        median_vs_budget = 0.0

    # --------------------------------------------------
    # RISK CLASSIFICATION
    # --------------------------------------------------

    if budget_revenue <= 0:

        risk_level = "UNKNOWN"

    elif probability_below_budget >= 50:

        risk_level = "HIGH"

    elif probability_below_budget >= 25:

        risk_level = "MEDIUM"

    else:

        risk_level = "LOW"

    # --------------------------------------------------
    # FORECAST RANGE
    # --------------------------------------------------

    forecast_range = (
        p90 - p10
    )

    # --------------------------------------------------
    # RETURN
    # --------------------------------------------------

    return {
        "iterations": iterations,

        "random_seed": random_seed,

        "deterministic_inputs": {
            "actual_revenue": round(
                actual_revenue,
                2,
            ),
            "budget_revenue": round(
                budget_revenue,
                2,
            ),
            "committed_backlog": round(
                committed_backlog,
                2,
            ),
            "weighted_pipeline": round(
                weighted_pipeline,
                2,
            ),
            "utilization_adjustment": round(
                utilization_adjustment,
                2,
            ),
            "risk_adjustment": round(
                risk_adjustment,
                2,
            ),
        },

        "distribution": {
            "p10": round(
                p10,
                2,
            ),
            "p25": round(
                p25,
                2,
            ),
            "p50": round(
                p50,
                2,
            ),
            "p75": round(
                p75,
                2,
            ),
            "p90": round(
                p90,
                2,
            ),
            "mean": round(
                mean_forecast,
                2,
            ),
            "standard_deviation": round(
                std_forecast,
                2,
            ),
            "range_p10_p90": round(
                forecast_range,
                2,
            ),
        },

        "budget_analysis": {
            "probability_above_budget": round(
                probability_above_budget,
                2,
            ),
            "probability_below_budget": round(
                probability_below_budget,
                2,
            ),
            "p10_vs_budget": round(
                downside_vs_budget,
                2,
            ),
            "p50_vs_budget": round(
                median_vs_budget,
                2,
            ),
            "p90_vs_budget": round(
                upside_vs_budget,
                2,
            ),
        },

        "risk": {
            "risk_level": risk_level,
            "downside_at_p10": round(
                downside_vs_budget,
                2,
            ),
            "forecast_range": round(
                forecast_range,
                2,
            ),
        },
    }