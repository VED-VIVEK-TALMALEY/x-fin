from typing import Dict, List


def generate_insights(
    reasoning: Dict,
) -> List[Dict]:

    insights: List[Dict] = []

    # --------------------------------------------------
    # CORE METRICS
    # --------------------------------------------------

    budget_gap = float(
        reasoning.get("budget_gap", 0.0) or 0.0
    )

    budget_gap_pct = float(
        reasoning.get("budget_gap_pct", 0.0) or 0.0
    )

    forecast_gap = float(
        reasoning.get("forecast_gap", 0.0) or 0.0
    )

    forecast_gap_pct = float(
        reasoning.get("forecast_gap_pct", 0.0) or 0.0
    )

    forward_coverage = float(
        reasoning.get("forward_coverage", 0.0) or 0.0
    )

    committed_backlog = float(
        reasoning.get("committed_backlog", 0.0) or 0.0
    )

    weighted_pipeline = float(
        reasoning.get("weighted_pipeline", 0.0) or 0.0
    )

    committed_forecast_coverage = float(
        reasoning.get(
            "committed_forecast_coverage",
            reasoning.get(
                "forecast_confidence_base",
                0.0,
            ),
        )
        or 0.0
    )

    committed_revenue_mix = float(
        reasoning.get(
            "committed_revenue_mix",
            0.0,
        )
        or 0.0
    )

    pipeline_dependency = float(
        reasoning.get(
            "pipeline_dependency",
            0.0,
        )
        or 0.0
    )

    forecast_headroom = float(
        reasoning.get(
            "forecast_headroom",
            forecast_gap,
        )
        or 0.0
    )

    forecast_headroom_pct = float(
        reasoning.get(
            "forecast_headroom_pct",
            forecast_gap_pct,
        )
        or 0.0
    )

    forecast_risk = str(
        reasoning.get(
            "forecast_risk",
            "unknown",
        )
    ).lower()

    pipeline_risk = str(
        reasoning.get(
            "pipeline_risk",
            "unknown",
        )
    ).lower()

    forward_position = str(
        reasoning.get(
            "forward_position",
            "unknown",
        )
    ).lower()

    # --------------------------------------------------
    # 1. REVENUE PERFORMANCE
    # --------------------------------------------------

    if budget_gap > 0:

        insights.append({
            "severity": "LOW",
            "category": "Revenue",
            "metric": "Actual vs Budget",
            "message": (
                "Actual revenue is "
                f"{budget_gap_pct:.1f}% above budget."
            ),
            "value": round(
                budget_gap,
                2,
            ),
        })

    elif budget_gap < 0:

        severity = (
            "HIGH"
            if budget_gap_pct <= -10
            else "MEDIUM"
        )

        insights.append({
            "severity": severity,
            "category": "Revenue",
            "metric": "Actual vs Budget",
            "message": (
                "Actual revenue is "
                f"{abs(budget_gap_pct):.1f}% below budget."
            ),
            "value": round(
                budget_gap,
                2,
            ),
        })

    else:

        insights.append({
            "severity": "LOW",
            "category": "Revenue",
            "metric": "Actual vs Budget",
            "message": (
                "Actual revenue is broadly in line "
                "with budget."
            ),
            "value": 0.0,
        })

    # --------------------------------------------------
    # 2. FORECAST POSITION
    # --------------------------------------------------

    if forecast_gap > 0:

        insights.append({
            "severity": "LOW",
            "category": "Forecast",
            "metric": "Forecast vs Budget",
            "message": (
                "Current forecast is "
                f"{forecast_gap_pct:.1f}% above budget."
            ),
            "value": round(
                forecast_gap,
                2,
            ),
        })

    elif forecast_gap < 0:

        severity = (
            "HIGH"
            if forecast_gap_pct <= -10
            else "MEDIUM"
        )

        insights.append({
            "severity": severity,
            "category": "Forecast",
            "metric": "Forecast vs Budget",
            "message": (
                "Current forecast is "
                f"{abs(forecast_gap_pct):.1f}% below budget."
            ),
            "value": round(
                forecast_gap,
                2,
            ),
        })

    else:

        insights.append({
            "severity": "LOW",
            "category": "Forecast",
            "metric": "Forecast vs Budget",
            "message": (
                "Current forecast is broadly "
                "in line with budget."
            ),
            "value": 0.0,
        })

    # --------------------------------------------------
    # 3. FORWARD COVERAGE
    # --------------------------------------------------

    if forward_coverage >= 120:

        coverage_severity = "LOW"

        coverage_message = (
            "Forward revenue coverage is "
            f"{forward_coverage:.1f}% of budget, "
            "providing a strong coverage position."
        )

    elif forward_coverage >= 100:

        coverage_severity = "MEDIUM"

        coverage_message = (
            "Forward revenue coverage is "
            f"{forward_coverage:.1f}% of budget. "
            "The position is covered but has limited "
            "buffer against execution risk."
        )

    else:

        coverage_severity = "HIGH"

        coverage_message = (
            "Forward revenue coverage is only "
            f"{forward_coverage:.1f}% of budget, "
            "indicating a potential revenue coverage gap."
        )

    insights.append({
        "severity": coverage_severity,
        "category": "Coverage",
        "metric": "Forward Revenue Coverage",
        "message": coverage_message,
        "value": round(
            forward_coverage,
            2,
        ),
    })

    # --------------------------------------------------
    # 4. FORECAST COMMITMENT
    # --------------------------------------------------

    if committed_forecast_coverage >= 70:

        severity = "LOW"

        message = (
            f"{committed_forecast_coverage:.1f}% of forecast "
            "revenue is supported by committed backlog, "
            "providing relatively strong delivery visibility."
        )

    elif committed_forecast_coverage >= 50:

        severity = "MEDIUM"

        message = (
            f"{committed_forecast_coverage:.1f}% of forecast "
            "revenue is supported by committed backlog, "
            "with the remaining forecast dependent on "
            "pipeline conversion and execution."
        )

    else:

        severity = "HIGH"

        message = (
            f"Only {committed_forecast_coverage:.1f}% of "
            "forecast revenue is supported by committed "
            "backlog, creating meaningful execution risk."
        )

    insights.append({
        "severity": severity,
        "category": "Forecast Quality",
        "metric": "Committed Forecast Coverage",
        "message": message,
        "value": round(
            committed_forecast_coverage,
            2,
        ),
    })

    # --------------------------------------------------
    # 5. PIPELINE DEPENDENCY
    # --------------------------------------------------

    if pipeline_dependency >= 60:

        severity = "HIGH"

        message = (
            f"{pipeline_dependency:.1f}% of forward revenue "
            "depends on weighted pipeline, creating high "
            "conversion dependency."
        )

    elif pipeline_dependency >= 40:

        severity = "MEDIUM"

        message = (
            f"{pipeline_dependency:.1f}% of forward revenue "
            "depends on weighted pipeline, creating "
            "moderate conversion dependency."
        )

    else:

        severity = "LOW"

        message = (
            f"{pipeline_dependency:.1f}% of forward revenue "
            "depends on weighted pipeline, indicating "
            "relatively low pipeline dependency."
        )

    insights.append({
        "severity": severity,
        "category": "Pipeline Risk",
        "metric": "Pipeline Dependency",
        "message": message,
        "value": round(
            pipeline_dependency,
            2,
        ),
    })

    # --------------------------------------------------
    # 6. COMMITTED REVENUE MIX
    # --------------------------------------------------

    if committed_revenue_mix >= 60:

        severity = "LOW"

    elif committed_revenue_mix >= 40:

        severity = "MEDIUM"

    else:

        severity = "HIGH"

    insights.append({
        "severity": severity,
        "category": "Revenue Quality",
        "metric": "Committed Revenue Mix",
        "message": (
            f"{committed_revenue_mix:.1f}% of forward "
            "revenue is supported by committed backlog, "
            f"while {pipeline_dependency:.1f}% depends "
            "on weighted pipeline."
        ),
        "value": round(
            committed_revenue_mix,
            2,
        ),
    })

    # --------------------------------------------------
    # 7. FORECAST RISK
    # --------------------------------------------------

    if forecast_risk == "high":

        insights.append({
            "severity": "HIGH",
            "category": "Forecast Risk",
            "metric": "Forecast Risk",
            "message": (
                "Forecast risk is high because a relatively "
                "small portion of forecast revenue is backed "
                "by committed backlog."
            ),
            "value": round(
                committed_forecast_coverage,
                2,
            ),
        })

    elif forecast_risk == "moderate":

        insights.append({
            "severity": "MEDIUM",
            "category": "Forecast Risk",
            "metric": "Forecast Risk",
            "message": (
                "Forecast risk is moderate. A meaningful "
                "portion of forecast revenue remains dependent "
                "on pipeline conversion."
            ),
            "value": round(
                committed_forecast_coverage,
                2,
            ),
        })

    elif forecast_risk == "low":

        insights.append({
            "severity": "LOW",
            "category": "Forecast Risk",
            "metric": "Forecast Risk",
            "message": (
                "Forecast risk is relatively low because "
                "most forecast revenue is supported by "
                "committed backlog."
            ),
            "value": round(
                committed_forecast_coverage,
                2,
            ),
        })

    # --------------------------------------------------
    # 8. FORWARD POSITION
    # --------------------------------------------------

    if forward_position == "strong":

        insights.append({
            "severity": "LOW",
            "category": "Forward Position",
            "metric": "Forward Revenue Position",
            "message": (
                f"Forward revenue coverage of "
                f"{forward_coverage:.1f}% indicates "
                "a strong forward position."
            ),
            "value": round(
                forward_coverage,
                2,
            ),
        })

    elif forward_position == "adequate":

        insights.append({
            "severity": "MEDIUM",
            "category": "Forward Position",
            "metric": "Forward Revenue Position",
            "message": (
                f"Forward revenue coverage of "
                f"{forward_coverage:.1f}% is adequate, "
                "but the business has limited buffer."
            ),
            "value": round(
                forward_coverage,
                2,
            ),
        })

    elif forward_position in {
        "watch",
        "weak",
    }:

        insights.append({
            "severity": "HIGH",
            "category": "Forward Position",
            "metric": "Forward Revenue Position",
            "message": (
                f"Forward revenue coverage of "
                f"{forward_coverage:.1f}% requires "
                "management attention."
            ),
            "value": round(
                forward_coverage,
                2,
            ),
        })

    # --------------------------------------------------
    # 9. FORECAST HEADROOM
    # --------------------------------------------------

    if forecast_headroom > 0:

        insights.append({
            "severity": "LOW",
            "category": "Forecast Headroom",
            "metric": "Forecast Buffer",
            "message": (
                f"Forecast has ₹{forecast_headroom:,.0f} "
                f"of headroom above budget "
                f"({forecast_headroom_pct:.1f}%)."
            ),
            "value": round(
                forecast_headroom,
                2,
            ),
        })

    elif forecast_headroom < 0:

        insights.append({
            "severity": "HIGH",
            "category": "Forecast Headroom",
            "metric": "Forecast Shortfall",
            "message": (
                f"Forecast is ₹{abs(forecast_headroom):,.0f} "
                f"below budget "
                f"({abs(forecast_headroom_pct):.1f}%)."
            ),
            "value": round(
                forecast_headroom,
                2,
            ),
        })

    return insights