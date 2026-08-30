"""
Standalone X-Fin Intelligence Dashboard
"""

from __future__ import annotations

import pandas as pd
import streamlit as st
import plotly.graph_objects as go

from dashboard.api import (
    get_intelligence,
    get_executive_briefing,
)
from dashboard.charts import (
    executive_risk_chart,
)


st.set_page_config(
    page_title="X-Fin Intelligence",
    page_icon="X",
    layout="wide",
)


def money(value):
    try:
        value = float(value or 0)
    except (TypeError, ValueError):
        value = 0.0

    if abs(value) >= 1_000_000_000:
        return (
            f"₹{value / 1_000_000_000:.2f}B"
        )

    if abs(value) >= 1_000_000:
        return (
            f"₹{value / 1_000_000:.1f}M"
        )

    if abs(value) >= 1_000:
        return (
            f"₹{value / 1_000:.1f}K"
        )

    return f"₹{value:,.0f}"


def pct(value):
    try:
        return f"{float(value or 0):.1f}%"
    except (TypeError, ValueError):
        return "0.0%"


def title_case(value):
    return (
        str(value or "unknown")
        .replace("_", " ")
        .title()
    )


st.title(
    "X-Fin Intelligence"
)

st.caption(
    "Executive finance intelligence and "
    "decision support."
)

st.divider()


try:
    intelligence = get_intelligence()
except Exception as exc:
    st.error(
        "Unable to connect to the X-Fin API."
    )
    st.exception(exc)
    st.stop()


reasoning = intelligence.get(
    "reasoning",
    {},
)

risk = intelligence.get(
    "risk",
    {},
)

forecast = intelligence.get(
    "forecast",
    {},
)

monte_carlo = intelligence.get(
    "monte_carlo",
    {},
)

insights = intelligence.get(
    "insights",
    [],
)

recommendations = intelligence.get(
    "recommendations",
    [],
)

source_metrics = intelligence.get(
    "source_metrics",
    {},
)

revenue_leakage = intelligence.get(
    "revenue_leakage",
    {},
)

pipeline_intelligence = intelligence.get(
    "pipeline_intelligence",
    {},
)

margin_risk = intelligence.get(
    "margin_risk",
    {},
)

portfolio_risk = intelligence.get(
    "portfolio_risk",
    {},
)


# ------------------------------------------------------------
# Executive briefing
# ------------------------------------------------------------

try:
    executive_response = (
        get_executive_briefing()
    )

    briefing = executive_response.get(
        "briefing",
        {},
    )

except Exception:
    briefing = {}


if briefing:
    st.subheader(
        "Executive Briefing"
    )

    st.info(
        briefing.get(
            "headline",
            "No executive headline available.",
        )
    )

    st.write(
        briefing.get(
            "management_summary",
            "",
        )
    )


# ------------------------------------------------------------
# Core status
# ------------------------------------------------------------

performance = reasoning.get(
    "performance",
    "unknown",
)

overall_risk = portfolio_risk.get(
    "risk_level",
    risk.get(
        "overall_risk",
        "unknown",
    ),
)

if performance == "ahead_of_plan":
    st.success(
        "PERFORMANCE STATUS: AHEAD OF PLAN"
    )
elif performance == "below_plan":
    st.error(
        "PERFORMANCE STATUS: BELOW PLAN"
    )
else:
    st.warning(
        f"PERFORMANCE STATUS: "
        f"{title_case(performance)}"
    )


# ------------------------------------------------------------
# Core KPIs
# ------------------------------------------------------------

cols = st.columns(6)

with cols[0]:
    st.metric(
        "Actual Revenue",
        money(
            reasoning.get(
                "actual_revenue"
            )
        ),
    )

with cols[1]:
    st.metric(
        "Budget",
        money(
            reasoning.get(
                "budget_revenue"
            )
        ),
    )

with cols[2]:
    st.metric(
        "Forecast",
        money(
            reasoning.get(
                "forecast_revenue",
                forecast.get(
                    "forecast_revenue"
                ),
            )
        ),
    )

with cols[3]:
    st.metric(
        "Weighted Pipeline",
        money(
            pipeline_intelligence.get(
                "weighted_pipeline",
                reasoning.get(
                    "weighted_pipeline",
                    0,
                ),
            )
        ),
    )

with cols[4]:
    st.metric(
        "Revenue Leakage",
        money(
            revenue_leakage.get(
                "total_potential_leakage",
                0,
            )
        ),
    )

with cols[5]:
    st.metric(
        "Portfolio Risk",
        f"{float(portfolio_risk.get('portfolio_risk_score', risk.get('risk_score', 0))):.1f}/100",
    )


st.divider()


# ------------------------------------------------------------
# New intelligence layer
# ------------------------------------------------------------

st.subheader(
    "Strategic Intelligence"
)

cols = st.columns(4)

with cols[0]:
    st.metric(
        "Pipeline Quality",
        f"{float(pipeline_intelligence.get('pipeline_quality_score', 0)):.1f}/100",
    )

    st.caption(
        title_case(
            pipeline_intelligence.get(
                "pipeline_quality_band"
            )
        )
    )

with cols[1]:
    st.metric(
        "Potential Leakage",
        money(
            revenue_leakage.get(
                "total_potential_leakage",
                0,
            )
        ),
    )

    st.caption(
        f"{revenue_leakage.get('projects_with_leakage', 0)} projects affected"
    )

with cols[2]:
    st.metric(
        "Margin at Risk",
        money(
            margin_risk.get(
                "margin_at_risk",
                0,
            )
        ),
    )

    st.caption(
        f"{margin_risk.get('high_risk_projects', 0)} high-risk projects"
    )

with cols[3]:
    st.metric(
        "Revenue at Risk",
        money(
            portfolio_risk.get(
                "revenue_at_risk",
                0,
            )
        ),
    )

    st.caption(
        f"Risk level: {title_case(overall_risk)}"
    )


# ------------------------------------------------------------
# Portfolio risk
# ------------------------------------------------------------

st.subheader(
    "Portfolio Risk"
)

risk_cols = st.columns(2)

with risk_cols[0]:
    st.plotly_chart(
        executive_risk_chart(
            portfolio_risk
        ),
        width="stretch",
    )

with risk_cols[1]:
    drivers = portfolio_risk.get(
        "risk_drivers",
        [],
    )

    if drivers:
        st.markdown(
            "### Risk Drivers"
        )

        for driver in drivers:
            st.warning(
                title_case(driver)
            )

    else:
        st.success(
            "No material portfolio risk drivers detected."
        )


# ------------------------------------------------------------
# Revenue leakage
# ------------------------------------------------------------

st.subheader(
    "Revenue Leakage"
)

leakage_findings = revenue_leakage.get(
    "top_leakage_projects",
    [],
)

if leakage_findings:
    leakage_df = pd.DataFrame(
        leakage_findings
    )

    display_columns = [
        "project_id",
        "project_name",
        "business_unit",
        "revenue_gap",
        "cost_overrun",
        "potential_leakage",
        "severity",
    ]

    available = [
        column
        for column in display_columns
        if column in leakage_df.columns
    ]

    st.dataframe(
        leakage_df[available],
        width="stretch",
        hide_index=True,
    )
else:
    st.success(
        "No material revenue leakage detected."
    )


# ------------------------------------------------------------
# Pipeline intelligence
# ------------------------------------------------------------

st.subheader(
    "Pipeline Intelligence"
)

pipeline_findings = (
    pipeline_intelligence.get(
        "top_attention_opportunities",
        [],
    )
)

if pipeline_findings:
    pipeline_df = pd.DataFrame(
        pipeline_findings
    )

    display_columns = [
        "opportunity_id",
        "opportunity_name",
        "stage",
        "value",
        "probability",
        "adjusted_weighted_value",
        "freshness",
        "risk",
    ]

    available = [
        column
        for column in display_columns
        if column in pipeline_df.columns
    ]

    st.dataframe(
        pipeline_df[available],
        width="stretch",
        hide_index=True,
    )
else:
    st.info(
        "No pipeline opportunities require immediate attention."
    )


# ------------------------------------------------------------
# Margin risk
# ------------------------------------------------------------

st.subheader(
    "Margin Risk"

)

margin_findings = margin_risk.get(
    "top_margin_risks",
    [],
)

if margin_findings:
    margin_df = pd.DataFrame(
        margin_findings
    )

    display_columns = [
        "project_id",
        "project_name",
        "business_unit",
        "revenue",
        "cost",
        "actual_margin_pct",
        "target_margin_pct",
        "margin_gap_pct",
        "risk",
    ]

    available = [
        column
        for column in display_columns
        if column in margin_df.columns
    ]

    st.dataframe(
        margin_df[available],
        width="stretch",
        hide_index=True,
    )
else:
    st.success(
        "No material margin risks detected."
    )


# ------------------------------------------------------------
# Existing insights
# ------------------------------------------------------------

st.subheader(
    "Financial Insights"
)

if insights:
    for insight in insights:
        severity = str(
            insight.get(
                "severity",
                "LOW",
            )
        ).upper()

        message = (
            f"**{insight.get('category', 'Finance')}** — "
            f"{insight.get('message', '')}"
        )

        if severity == "HIGH":
            st.error(message)
        elif severity == "MEDIUM":
            st.warning(message)
        else:
            st.info(message)
else:
    st.info(
        "No material insights detected."
    )


# ------------------------------------------------------------
# Recommendations
# ------------------------------------------------------------

st.subheader(
    "Recommended Actions"
)

recommended_actions = briefing.get(
    "recommended_actions",
    recommendations,
)

if recommended_actions:
    for recommendation in recommended_actions:
        priority = str(
            recommendation.get(
                "priority",
                "LOW",
            )
        ).upper()

        action = recommendation.get(
            "action",
            "",
        )

        rationale = recommendation.get(
            "rationale",
            "",
        )

        impact = recommendation.get(
            "financial_impact"
        )

        content = (
            f"**{recommendation.get('category', 'Action')}**\n\n"
            f"{action}\n\n"
            f"*{rationale}*"
        )

        if priority == "HIGH":
            st.error(content)
        elif priority == "MEDIUM":
            st.warning(content)
        else:
            st.success(content)

        if impact is not None:
            st.caption(
                f"Financial value: {money(impact)}"
            )
else:
    st.info(
        "No recommendations generated."
    )


# ------------------------------------------------------------
# Forecast
# ------------------------------------------------------------

st.subheader(
    "Forecast Construction"
)

forecast_rows = {
    "Committed Backlog": forecast.get(
        "committed_backlog",
        0,
    ),
    "Weighted Pipeline": forecast.get(
        "weighted_pipeline",
        0,
    ),
    "Utilization Adjustment": forecast.get(
        "utilization_adjustment",
        0,
    ),
    "Risk Adjustment": forecast.get(
        "risk_adjustment",
        0,
    ),
    "Final Forecast": forecast.get(
        "forecast_revenue",
        0,
    ),
}

forecast_df = pd.DataFrame(
    [
        {
            "Component": key,
            "Value": money(value),
        }
        for key, value
        in forecast_rows.items()
    ]
)

st.dataframe(
    forecast_df,
    width="stretch",
    hide_index=True,
)


# ------------------------------------------------------------
# Source metrics
# ------------------------------------------------------------

with st.expander(
    "Canonical Source Metrics"
):
    source_df = pd.DataFrame(
        [
            {
                "Metric": key,
                "Value": value,
            }
            for key, value
            in source_metrics.items()
        ]
    )

    st.dataframe(
        source_df,
        width="stretch",
        hide_index=True,
    )


st.divider()

st.caption(
    "X-Fin | Delivery Finance Intelligence"
)