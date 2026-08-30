"""
X-Fin | Delivery Finance Operating System
------------------------------------------

Main Streamlit dashboard.

Architecture:

API
 ↓
Canonical Intelligence
 ↓
Executive Intelligence
 ↓
Forecast / Risk / Pipeline / Leakage / Margin
 ↓
Management Actions
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from dashboard.api import (
    get_summary,
    get_monthly_revenue,
    get_backlog,
    get_variance,
    get_forecast_accuracy,
    get_business_units,
    get_intelligence,
    get_executive_briefing,
    run_scenario,
)

from dashboard.components import (
    metric_card,
    section_title,
    insight_card,
    recommendation_card,
    format_currency,
    format_percentage,
    show_error,
)

from dashboard.charts import (
    revenue_chart,
    backlog_chart,
    business_unit_chart,
    variance_chart,
    forecast_decomposition_chart,
    business_unit_heatmap,
    capacity_chart,
    risk_driver_chart,
    forecast_confidence_chart,
    accuracy_chart,
    executive_risk_chart,
)


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="X-Fin | Delivery Finance OS",
    page_icon="X",
    layout="wide",
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            linear-gradient(
                180deg,
                #311827 0%,
                #0f172a 100%
            );
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1600px;
    }

    div[data-testid="stMetric"] {
        background:
            rgba(31, 41, 55, 0.88);
        border:
            1px solid
            rgba(148, 163, 184, 0.24);
        border-radius:
            0.85rem;
        padding:
            0.75rem 0.9rem;
        box-shadow:
            0 2px 10px
            rgba(0, 0, 0, 0.22);
    }

    div[data-testid="stMetricLabel"] p,
    div[data-testid="stMetricValue"] {
        color: #f3f4f6;
    }

    .stCaption,
    [data-testid="stCaptionContainer"] {
        color: #a7b0c0;
    }

    .stMarkdown,
    .stMarkdown p,
    label {
        color: #e5e7eb;
    }

    [data-testid="stDataFrame"] {
        border:
            1px solid
            rgba(148, 163, 184, 0.24);
        border-radius:
            0.85rem;
        overflow: hidden;
    }

    .brand-title {
        color: #f3f453;
        font-size: 3rem;
        font-weight: 700;
        line-height: 1.2;
        margin: 0;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <h1 class="brand-title">
        X-Fin — Delivery Finance OS
    </h1>
    """,
    unsafe_allow_html=True,
)

st.caption(
    "Finance performance, forecasting, "
    "backlog and strategic intelligence"
)


# ============================================================
# HELPERS
# ============================================================

def money(value):
    return format_currency(value)


def pct(value):
    return format_percentage(value)


def title_case(value):
    return (
        str(value or "unknown")
        .replace("_", " ")
        .title()
    )


# ============================================================
# LOAD API DATA
# ============================================================

try:
    summary = get_summary()
    monthly_revenue = get_monthly_revenue()
    backlog = get_backlog()
    variance = get_variance()
    forecast_accuracy = get_forecast_accuracy()
    business_units = get_business_units()

    # Canonical intelligence endpoint.
    intelligence = get_intelligence()

    # New executive briefing layer.
    executive_response = get_executive_briefing()

except Exception as exc:
    show_error(
        f"Unable to connect to the Finance API: {exc}"
    )
    st.stop()


# ============================================================
# CANONICAL INTELLIGENCE
# ============================================================

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

decomposition = intelligence.get(
    "forecast_decomposition",
    {},
)

monte_carlo = intelligence.get(
    "monte_carlo",
    {},
)

staffing = intelligence.get(
    "staffing",
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

data_quality = intelligence.get(
    "data_quality",
    {},
)

source_metrics = intelligence.get(
    "source_metrics",
    {},
)


# ============================================================
# NEW STRATEGIC INTELLIGENCE
# ============================================================

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

briefing = executive_response.get(
    "briefing",
    {},
)


# ============================================================
# CANONICAL VALUES
# ============================================================

actual_revenue = float(
    reasoning.get(
        "actual_revenue",
        0,
    )
    or 0
)

budget_revenue = float(
    reasoning.get(
        "budget_revenue",
        0,
    )
    or 0
)

canonical_forecast = float(
    intelligence.get(
        "canonical_forecast_revenue",
        reasoning.get(
            "forecast_revenue",
            forecast.get(
                "forecast_revenue",
                0,
            ),
        ),
    )
    or 0
)

committed_backlog = float(
    reasoning.get(
        "committed_backlog",
        0,
    )
    or 0
)

weighted_pipeline = float(
    reasoning.get(
        "weighted_pipeline",
        pipeline_intelligence.get(
            "weighted_pipeline",
            0,
        ),
    )
    or 0
)

pipeline_value = float(
    source_metrics.get(
        "pipeline_value",
        pipeline_intelligence.get(
            "pipeline_value",
            0,
        ),
    )
    or 0
)

actual_cost = float(
    source_metrics.get(
        "actual_cost",
        0,
    )
    or 0
)

gross_margin = (
    actual_revenue
    - actual_cost
)

gross_margin_pct = (
    gross_margin
    / actual_revenue
    * 100
    if actual_revenue
    else 0
)

portfolio_risk_score = float(
    portfolio_risk.get(
        "portfolio_risk_score",
        risk.get(
            "risk_score",
            0,
        ),
    )
    or 0
)

revenue_at_risk = float(
    portfolio_risk.get(
        "revenue_at_risk",
        0,
    )
    or 0
)

leakage_value = float(
    revenue_leakage.get(
        "total_potential_leakage",
        0,
    )
    or 0
)

margin_at_risk = float(
    margin_risk.get(
        "margin_at_risk",
        0,
    )
    or 0
)

pipeline_quality = float(
    pipeline_intelligence.get(
        "pipeline_quality_score",
        0,
    )
    or 0
)


# ============================================================
# EXECUTIVE BRIEFING
# ============================================================

section_title(
    "Executive Briefing",
    "A management-level synthesis of revenue performance, "
    "forecast quality, portfolio risk and financial exposure.",
)

if briefing:
    st.info(
        f"**{briefing.get('headline', '')}**"
    )

    st.caption(
        briefing.get(
            "management_summary",
            "",
        )
    )

    briefing_cols = st.columns(4)

    with briefing_cols[0]:
        st.metric(
            "Revenue Leakage",
            money(leakage_value),
        )

    with briefing_cols[1]:
        st.metric(
            "Margin at Risk",
            money(margin_at_risk),
        )

    with briefing_cols[2]:
        st.metric(
            "Revenue at Risk",
            money(revenue_at_risk),
        )

    with briefing_cols[3]:
        st.metric(
            "Portfolio Risk",
            f"{portfolio_risk_score:.1f}/100",
        )


# ============================================================
# DECISION SNAPSHOT
# ============================================================

section_title(
    "Decision Snapshot",
    "The four signals management should inspect first.",
)

snapshot = st.columns(4)

with snapshot[0]:
    st.metric(
        "Actual vs Budget",
        pct(
            reasoning.get(
                "budget_gap_pct",
                0,
            )
        ),
    )

with snapshot[1]:
    st.metric(
        "Forecast vs Budget",
        pct(
            reasoning.get(
                "forecast_gap_pct",
                0,
            )
        ),
    )

with snapshot[2]:
    st.metric(
        "Pipeline Quality",
        f"{pipeline_quality:.1f}/100",
    )

with snapshot[3]:
    st.metric(
        "Portfolio Risk",
        f"{portfolio_risk_score:.1f}/100",
    )


# ============================================================
# CORE PERFORMANCE
# ============================================================

section_title(
    "Executive Performance",
    "Core revenue, backlog, pipeline and margin metrics.",
)

cols = st.columns(8)

with cols[0]:
    metric_card(
        "Actual Revenue",
        money(actual_revenue),
    )

with cols[1]:
    metric_card(
        "vs Budget",
        pct(
            reasoning.get(
                "budget_gap_pct",
                0,
            )
        ),
    )

with cols[2]:
    metric_card(
        "Forecast",
        money(canonical_forecast),
    )

with cols[3]:
    metric_card(
        "Committed Backlog",
        money(committed_backlog),
    )

with cols[4]:
    metric_card(
        "Pipeline",
        money(pipeline_value),
    )

with cols[5]:
    metric_card(
        "Weighted Pipeline",
        money(weighted_pipeline),
    )

with cols[6]:
    metric_card(
        "Gross Margin",
        pct(gross_margin_pct),
    )

with cols[7]:
    metric_card(
        "Portfolio Risk",
        f"{portfolio_risk_score:.1f}/100",
    )


# ============================================================
# STRATEGIC INTELLIGENCE
# ============================================================

section_title(
    "Strategic Intelligence",
    "Higher-order signals derived from project leakage, "
    "pipeline quality and margin performance.",
)

strategic = st.columns(4)

with strategic[0]:
    st.metric(
        "Potential Leakage",
        money(leakage_value),
    )

    st.caption(
        f"{revenue_leakage.get('projects_with_leakage', 0)} "
        "projects with leakage signals"
    )

with strategic[1]:
    st.metric(
        "Pipeline Quality",
        f"{pipeline_quality:.1f}/100",
    )

    st.caption(
        title_case(
            pipeline_intelligence.get(
                "pipeline_quality_band",
                "unknown",
            )
        )
    )

with strategic[2]:
    st.metric(
        "Margin at Risk",
        money(margin_at_risk),
    )

    st.caption(
        f"{margin_risk.get('high_risk_projects', 0)} "
        "high-risk projects"
    )

with strategic[3]:
    st.metric(
        "Revenue at Risk",
        money(revenue_at_risk),
    )

    st.caption(
        f"Portfolio risk: "
        f"{title_case(portfolio_risk.get('risk_level', 'unknown'))}"
    )


# ============================================================
# PORTFOLIO RISK
# ============================================================

section_title(
    "Portfolio Risk",
    "Composite risk across forecast quality, pipeline dependency, "
    "revenue leakage and margin pressure.",
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
    st.subheader(
        "Risk Drivers"
    )

    drivers = portfolio_risk.get(
        "risk_drivers",
        [],
    )

    if drivers:
        for driver in drivers:
            st.warning(
                title_case(driver)
            )
    else:
        st.success(
            "No material portfolio risk drivers detected."
        )


# ============================================================
# REVENUE LEAKAGE
# ============================================================

section_title(
    "Revenue Leakage",
    "Potential value loss caused by revenue realization gaps, "
    "cost overruns and delivery/revenue mismatches.",
)

leakage_projects = revenue_leakage.get(
    "top_leakage_projects",
    [],
)

if leakage_projects:
    leakage_df = pd.DataFrame(
        leakage_projects
    )

    columns = [
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
        for column in columns
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


# ============================================================
# PIPELINE INTELLIGENCE
# ============================================================

section_title(
    "Pipeline Intelligence",
    "Conversion probability, opportunity aging and "
    "concentration risk.",
)

pipeline_projects = pipeline_intelligence.get(
    "top_attention_opportunities",
    [],
)

if pipeline_projects:
    pipeline_df = pd.DataFrame(
        pipeline_projects
    )

    columns = [
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
        for column in columns
        if column in pipeline_df.columns
    ]

    st.dataframe(
        pipeline_df[available],
        width="stretch",
        hide_index=True,
    )

    st.caption(
        f"Pipeline concentration: "
        f"{float(pipeline_intelligence.get('concentration_pct', 0)):.1f}%"
    )

else:
    st.info(
        "No pipeline opportunities require immediate attention."
    )


# ============================================================
# MARGIN RISK
# ============================================================

section_title(
    "Margin Risk",
    "Project-level margin deterioration and cost-overrun exposure.",
)

margin_projects = margin_risk.get(
    "top_margin_risks",
    [],
)

if margin_projects:
    margin_df = pd.DataFrame(
        margin_projects
    )

    columns = [
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
        for column in columns
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


# ============================================================
# FORECAST DECOMPOSITION
# ============================================================

section_title(
    "Forecast Decomposition",
    "How committed backlog, weighted pipeline, utilization "
    "and execution risk combine into the forecast.",
)

dcols = st.columns(5)

with dcols[0]:
    st.metric(
        "Committed Backlog",
        money(
            decomposition.get(
                "committed_backlog",
                0,
            )
        ),
    )

with dcols[1]:
    st.metric(
        "Weighted Pipeline",
        money(
            decomposition.get(
                "weighted_pipeline",
                0,
            )
        ),
    )

with dcols[2]:
    st.metric(
        "Utilization Adjustment",
        money(
            decomposition.get(
                "utilization_adjustment",
                0,
            )
        ),
    )

with dcols[3]:
    st.metric(
        "Risk Adjustment",
        money(
            decomposition.get(
                "risk_adjustment",
                0,
            )
        ),
    )

with dcols[4]:
    st.metric(
        "Final Forecast",
        money(
            decomposition.get(
                "forecast_revenue",
                canonical_forecast,
            )
        ),
    )

st.plotly_chart(
    forecast_decomposition_chart(
        decomposition
    ),
    width="stretch",
)


# ============================================================
# FORECAST RISK
# ============================================================

section_title(
    "Forecast Risk & Revenue Quality",
    "Coverage, dependency and forecast-headroom indicators.",
)

risk_metrics = st.columns(5)

with risk_metrics[0]:
    st.metric(
        "Risk Score",
        f"{float(risk.get('risk_score', 0)):.1f}/100",
    )

with risk_metrics[1]:
    st.metric(
        "Committed Coverage",
        pct(
            risk.get(
                "committed_forecast_coverage",
                0,
            )
        ),
    )

with risk_metrics[2]:
    st.metric(
        "Pipeline Dependency",
        pct(
            risk.get(
                "pipeline_dependency",
                0,
            )
        ),
    )

with risk_metrics[3]:
    st.metric(
        "Forecast Headroom",
        money(
            risk.get(
                "forecast_headroom",
                0,
            )
        ),
    )

with risk_metrics[4]:
    st.metric(
        "Overall Risk",
        title_case(
            risk.get(
                "overall_risk",
                "unknown",
            )
        ),
    )

chart_cols = st.columns(2)

with chart_cols[0]:
    st.plotly_chart(
        risk_driver_chart(risk),
        width="stretch",
    )

with chart_cols[1]:
    st.plotly_chart(
        forecast_confidence_chart(
            monte_carlo,
            budget_revenue,
        ),
        width="stretch",
    )


# ============================================================
# MONTE CARLO
# ============================================================

section_title(
    "Monte Carlo Forecast",
    "Simulated revenue distribution and probability of achieving budget.",
)

if monte_carlo:
    distribution = monte_carlo.get(
        "distribution",
        {},
    )

    budget_analysis = monte_carlo.get(
        "budget_analysis",
        {},
    )

    mcols = st.columns(5)

    with mcols[0]:
        st.metric(
            "P10",
            money(
                distribution.get(
                    "p10",
                    0,
                )
            ),
        )

    with mcols[1]:
        st.metric(
            "P25",
            money(
                distribution.get(
                    "p25",
                    0,
                )
            ),
        )

    with mcols[2]:
        st.metric(
            "P50",
            money(
                distribution.get(
                    "p50",
                    0,
                )
            ),
        )

    with mcols[3]:
        st.metric(
            "P75",
            money(
                distribution.get(
                    "p75",
                    0,
                )
            ),
        )

    with mcols[4]:
        st.metric(
            "P90",
            money(
                distribution.get(
                    "p90",
                    0,
                )
            ),
        )

    st.caption(
        "Monte Carlo results are generated by the canonical "
        "forecast simulation engine."
    )

else:
    st.info(
        "Monte Carlo results are not available."
    )


# ============================================================
# STAFFING
# ============================================================

section_title(
    "Staffing & Capacity",
    "Actual staffing consumption versus planned delivery capacity.",
)

scols = st.columns(5)

with scols[0]:
    st.metric(
        "Actual Hours",
        f"{float(staffing.get('actual_hours', 0) or 0):,.0f}",
    )

with scols[1]:
    st.metric(
        "Hours Budget",
        f"{float(staffing.get('budget_hours', 0) or 0):,.0f}",
    )

with scols[2]:
    st.metric(
        "Hours vs Budget",
        pct(
            staffing.get(
                "hours_attainment_pct",
                0,
            )
        ),
    )

with scols[3]:
    st.metric(
        "Blended Cost / Hour",
        money(
            staffing.get(
                "blended_cost_per_hour",
                0,
            )
        ),
    )

with scols[4]:
    st.metric(
        "Capacity Status",
        title_case(
            staffing.get(
                "capacity_status",
                "unknown",
            )
        ),
    )

st.plotly_chart(
    capacity_chart(staffing),
    width="stretch",
)


# ============================================================
# FINANCIAL POSITION
# ============================================================

section_title(
    "Financial Position",
    "Actual, budget and forecast revenue gaps.",
)

fcols = st.columns(4)

with fcols[0]:
    st.metric(
        "Actual vs Budget",
        money(
            reasoning.get(
                "budget_gap",
                0,
            )
        ),
    )

with fcols[1]:
    st.metric(
        "Budget Gap %",
        pct(
            reasoning.get(
                "budget_gap_pct",
                0,
            )
        ),
    )

with fcols[2]:
    st.metric(
        "Forecast vs Budget",
        money(
            reasoning.get(
                "forecast_gap",
                0,
            )
        ),
    )

with fcols[3]:
    st.metric(
        "Forecast Gap %",
        pct(
            reasoning.get(
                "forecast_gap_pct",
                0,
            )
        ),
    )


# ============================================================
# INSIGHTS
# ============================================================

section_title(
    "Key Insights",
    "Findings generated by the existing X-Fin intelligence stack.",
)

if insights:
    insight_columns = st.columns(3)

    for index, insight in enumerate(insights):
        with insight_columns[index % 3]:
            insight_card(
                insight.get(
                    "category",
                    "General",
                ),
                insight.get(
                    "metric",
                    "",
                ),
                insight.get(
                    "message",
                    "",
                ),
                insight.get(
                    "severity",
                    "INFO",
                ),
            )
else:
    st.info(
        "No material insights detected."
    )


# ============================================================
# RECOMMENDATIONS
# ============================================================

section_title(
    "Recommended Actions",
    "Management actions generated from current financial signals.",
)

actions = briefing.get(
    "recommended_actions",
    recommendations,
)

if actions:
    recommendation_columns = st.columns(3)

    for index, recommendation in enumerate(actions):
        with recommendation_columns[index % 3]:
            recommendation_card(
                recommendation.get(
                    "category",
                    "Action",
                ),
                recommendation.get(
                    "priority",
                    "LOW",
                ),
                recommendation.get(
                    "action",
                    "",
                ),
                recommendation.get(
                    "rationale",
                    "",
                ),
                recommendation.get(
                    "financial_impact",
                ),
            )
else:
    st.info(
        "No recommendations generated."
    )


# ============================================================
# REVENUE PERFORMANCE
# ============================================================

section_title(
    "Revenue Performance",
    "Historical monthly revenue trend.",
)

if monthly_revenue:
    st.plotly_chart(
        revenue_chart(
            monthly_revenue
        ),
        width="stretch",
    )
else:
    st.info(
        "No monthly revenue data available."
    )


# ============================================================
# FORECAST / BACKLOG
# ============================================================

left, right = st.columns(2)

with left:
    section_title(
        "Forecast Position",
        "Canonical forecast compared with backlog and pipeline.",
    )

    st.metric(
        "Canonical Forecast",
        money(canonical_forecast),
    )

    st.metric(
        "Committed Backlog",
        money(committed_backlog),
    )

    st.metric(
        "Weighted Pipeline",
        money(weighted_pipeline),
    )

    st.plotly_chart(
        variance_chart(
            variance
        ),
        width="stretch",
    )


with right:
    section_title(
        "Backlog Position",
        "Current backlog profile.",
    )

    st.plotly_chart(
        backlog_chart(
            backlog
        ),
        width="stretch",
    )


# ============================================================
# BUSINESS UNITS
# ============================================================

section_title(
    "Business Unit Performance",
    "Revenue and margin comparison across business units.",
)

if business_units:
    bu_df = pd.DataFrame(
        business_units
    )

    display_columns = [
        "business_unit",
        "actual_revenue",
        "budget_revenue",
        "variance",
        "variance_pct",
        "gross_margin_pct",
    ]

    available_columns = [
        column
        for column in display_columns
        if column in bu_df.columns
    ]

    if available_columns:
        st.dataframe(
            bu_df[
                available_columns
            ],
            width="stretch",
            hide_index=True,
        )

    st.plotly_chart(
        business_unit_chart(
            business_units
        ),
        width="stretch",
    )

    st.plotly_chart(
        business_unit_heatmap(
            business_units
        ),
        width="stretch",
    )

else:
    st.info(
        "No business-unit data available."
    )


# ============================================================
# FORECAST ACCURACY
# ============================================================

section_title(
    "Historical Forecast / Budget Accuracy",
    "Historical forecast reliability.",
)

if forecast_accuracy:
    st.plotly_chart(
        accuracy_chart(
            forecast_accuracy
        ),
        width="stretch",
    )

    st.dataframe(
        pd.DataFrame(
            forecast_accuracy
        ),
        width="stretch",
        hide_index=True,
    )
else:
    st.info(
        "No historical forecast data available."
    )


# ============================================================
# SCENARIO SIMULATOR
# ============================================================

section_title(
    "Scenario Simulator",
    "Pressure-test revenue under pipeline, utilization, "
    "billing-rate and delivery-slippage assumptions.",
)

scenario_left, scenario_right = st.columns(2)

with scenario_left:

    base_revenue = st.number_input(
        "Base Revenue",
        min_value=0.0,
        value=float(actual_revenue),
        step=1_000_000.0,
    )

    scenario_pipeline = st.number_input(
        "Pipeline Revenue",
        min_value=0.0,
        value=float(pipeline_value),
        step=1_000_000.0,
    )

    current_utilization = float(
        source_metrics.get(
            "budget_utilization",
            0,
        )
        or 0
    )

    if current_utilization <= 1:
        current_utilization *= 100

    scenario_utilization = st.slider(
        "Current Utilization",
        min_value=0.0,
        max_value=150.0,
        value=float(
            current_utilization
        ),
        step=1.0,
        format="%.0f%%",
    )


with scenario_right:

    pipeline_conversion_change = st.slider(
        "Pipeline Conversion Change",
        min_value=-0.50,
        max_value=0.50,
        value=0.0,
        step=0.01,
        format="%.0f%%",
    )

    utilization_change = st.slider(
        "Utilization Change",
        min_value=-0.30,
        max_value=0.30,
        value=0.0,
        step=0.01,
        format="%.0f%%",
    )

    billing_rate_change = st.slider(
        "Billing Rate Change",
        min_value=-0.30,
        max_value=0.30,
        value=0.0,
        step=0.01,
        format="%.0f%%",
    )

    slippage_rate = st.slider(
        "Project Slippage",
        min_value=0.0,
        max_value=0.50,
        value=0.0,
        step=0.01,
        format="%.0f%%",
    )


if st.button(
    "Run Scenario",
    type="primary",
):

    payload = {
        "base_revenue": base_revenue,
        "pipeline_revenue": scenario_pipeline,
        "utilization": (
            scenario_utilization / 100
        ),
        "pipeline_conversion_change": (
            pipeline_conversion_change
        ),
        "utilization_change": (
            utilization_change
        ),
        "billing_rate_change": (
            billing_rate_change
        ),
        "slippage_rate": (
            slippage_rate
        ),
    }

    try:

        scenario = run_scenario(
            payload
        )

        result_cols = st.columns(4)

        with result_cols[0]:
            st.metric(
                "Base Revenue",
                money(
                    scenario.get(
                        "base_revenue"
                    )
                ),
            )

        with result_cols[1]:
            st.metric(
                "Scenario Revenue",
                money(
                    scenario.get(
                        "scenario_revenue"
                    )
                ),
            )

        with result_cols[2]:
            st.metric(
                "Revenue Impact",
                money(
                    scenario.get(
                        "revenue_change"
                    )
                ),
            )

        with result_cols[3]:
            st.metric(
                "Impact %",
                pct(
                    scenario.get(
                        "revenue_change_pct"
                    )
                ),
            )

    except Exception as exc:
        show_error(
            f"Scenario calculation failed: {exc}"
        )


# ============================================================
# DATA QUALITY
# ============================================================

if data_quality.get("flags"):

    section_title(
        "Data Quality",
        "Flags that may affect interpretation of the financial model.",
    )

    for flag in data_quality["flags"]:

        message = (
            f"**{flag.get('area', 'data').title()}** — "
            f"{flag.get('message', '')}"
        )

        if (
            str(
                flag.get(
                    "severity",
                    "",
                )
            ).upper()
            == "HIGH"
        ):
            st.error(message)
        else:
            st.warning(message)


# ============================================================
# SOURCE DATA
# ============================================================

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


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "X-Fin | Delivery Finance Intelligence"
)