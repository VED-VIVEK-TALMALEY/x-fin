import streamlit as st
import pandas as pd

from api import (
    get_summary,
    get_monthly_revenue,
    get_backlog,
    get_variance,
    get_forecast_accuracy,
    get_business_units,
    get_intelligence,
    run_scenario,
)

from components import (
    metric_card,
    section_title,
    format_currency,
    format_percentage,
    show_error,
)

from charts import (
    revenue_chart,
    backlog_chart,
    business_unit_chart,
    variance_chart,
)


st.set_page_config(
    page_title="X-Fin | Delivery Finance OS",
    page_icon="X",
    layout="wide",
)

st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(180deg, #111827 0%, #0f172a 100%);
            color: #e5e7eb;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1600px;
        }

        div[data-testid="stMetric"] {
            background: rgba(31, 41, 55, 0.88);
            border: 1px solid rgba(148, 163, 184, 0.24);
            border-radius: 0.85rem;
            padding: 0.75rem 0.9rem;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.22);
        }

        div[data-testid="stMetricLabel"] p,
        div[data-testid="stMetricValue"] {
            color: #f3f4f6;
        }

        .stCaption, [data-testid="stCaptionContainer"] {
            color: #a7b0c0;
        }

        .stMarkdown, .stMarkdown p, label {
            color: #e5e7eb;
        }

        [data-testid="stDataFrame"] {
            border: 1px solid rgba(148, 163, 184, 0.24);
            border-radius: 0.85rem;
            overflow: hidden;
        }

        div[data-testid="stVerticalBlock"] > div {
            gap: 0.85rem;
        }

        .stDataFrame, .stPlotlyChart {
            margin-top: 0.35rem;
        }

        .stAlert {
            border-radius: 0.8rem;
        }

        h1 {
            color: #f8fafc;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("X-Fin — Delivery Finance OS")
st.caption(
    "Finance performance, forecasting, backlog and scenario intelligence"
)


def money(value):
    return format_currency(value)


def pct(value):
    return format_percentage(value)


def title_case(value):
    return str(value or "unknown").replace("_", " ").title()


# ==================================================
# LOAD DATA
# ==================================================

try:
    summary = get_summary()
    monthly_revenue = get_monthly_revenue()
    backlog = get_backlog()
    variance = get_variance()
    forecast_accuracy = get_forecast_accuracy()
    business_units = get_business_units()

    # IMPORTANT:
    # All executive forecast/risk/intelligence KPIs come from this
    # canonical endpoint. Do not recompute them from /forecast/current.
    intelligence = get_intelligence()

except Exception as exc:
    show_error(f"Unable to connect to the Finance API: {exc}")
    st.stop()


reasoning = intelligence.get("reasoning", {})
risk = intelligence.get("risk", {})
forecast = intelligence.get("forecast", {})
decomposition = intelligence.get("forecast_decomposition", {})
monte_carlo = intelligence.get("monte_carlo", {})
staffing = intelligence.get("staffing", {})
insights = intelligence.get("insights", [])
recommendations = intelligence.get("recommendations", [])
data_quality = intelligence.get("data_quality", {})

source_metrics = intelligence.get("source_metrics", {})

# Canonical values
actual_revenue = float(reasoning.get("actual_revenue", 0) or 0)
budget_revenue = float(reasoning.get("budget_revenue", 0) or 0)
canonical_forecast = float(
    intelligence.get("canonical_forecast_revenue", 0) or 0
)
committed_backlog = float(
    reasoning.get("committed_backlog", 0) or 0
)
weighted_pipeline = float(
    reasoning.get("weighted_pipeline", 0) or 0
)
pipeline_value = float(
    source_metrics.get("pipeline_value", 0) or 0
)
actual_cost = float(
    source_metrics.get("actual_cost", 0) or 0
)

gross_margin = actual_revenue - actual_cost
gross_margin_pct = (
    gross_margin / actual_revenue * 100
    if actual_revenue
    else 0
)


# ==================================================
# EXECUTIVE PERFORMANCE
# ==================================================

section_title(
    "Executive Performance",
    "Core operating view of actual revenue, budget variance, forecast, backlog, utilization, and margin performance.",
)

cols = st.columns(8)

with cols[0]:
    metric_card(
        "Actual Revenue",
        money(actual_revenue),
        help_text="Recognized revenue delivered to date across the practice.",
    )

with cols[1]:
    metric_card(
        "vs Budget",
        pct(reasoning.get("budget_gap_pct", 0)),
        help_text="Actual performance versus budget, expressed as a percent variance.",
    )

with cols[2]:
    metric_card(
        "Forecast Revenue",
        money(canonical_forecast),
        help_text="The current risk-adjusted revenue forecast after backlog, pipeline, utilization, and execution-risk effects.",
    )

with cols[3]:
    metric_card(
        "Committed Backlog",
        money(committed_backlog),
        help_text="Revenue already locked in through active delivery or closed-won work.",
    )

with cols[4]:
    metric_card(
        "Pipeline",
        money(pipeline_value),
        help_text="Total value of the active pipeline before probability weighting.",
    )

with cols[5]:
    metric_card(
        "Weighted Pipeline",
        money(weighted_pipeline),
        help_text="Probability-adjusted pipeline value, reflecting the likely conversion contribution.",
    )

with cols[6]:
    metric_card(
        "Budget Utilization",
        pct(
            float(
                source_metrics.get(
                    "budget_utilization", 0
                )
                or 0
            )
            * 100
            if float(
                source_metrics.get(
                    "budget_utilization", 0
                )
                or 0
            ) <= 1
            else float(
                source_metrics.get(
                    "budget_utilization", 0
                )
                or 0
            )
        ),
        help_text="Planned utilization target used in the forecast model and delivery-capacity assumptions.",
    )

with cols[7]:
    metric_card(
        "Gross Margin",
        pct(gross_margin_pct),
        help_text="Actual gross margin percentage based on delivered revenue less direct delivery cost.",
    )


# ==================================================
# EXECUTIVE INTELLIGENCE
# ==================================================

section_title(
    "Executive Intelligence",
    "Summary of performance, risk status, forecast health, and coverage signals used by leadership.",
)

cols = st.columns(6)

with cols[0]:
    st.metric(
        "Performance",
        title_case(reasoning.get("performance")),
        help="Overall operating health based on actual revenue, pipeline, and risk posture.",
    )

with cols[1]:
    st.metric(
        "Forecast Status",
        title_case(reasoning.get("forecast_status")),
        help="Current forecast quality signal showing whether the forecast is tracking to plan.",
    )

with cols[2]:
    st.metric(
        "Committed Coverage",
        pct(risk.get("committed_forecast_coverage")),
        help="Share of forecast covered by committed backlog versus the total forecast value.",
    )

with cols[3]:
    st.metric(
        "Forward Coverage",
        pct(reasoning.get("forward_coverage")),
        help="Forward-looking coverage of remaining revenue against the upcoming period demand.",
    )

with cols[4]:
    st.metric(
        "Composite Risk Score",
        f"{float(risk.get('risk_score', 0)):.1f}/100",
        help="A blended quantitative risk score from forecast, coverage, and pipeline dependency inputs.",
    )

with cols[5]:
    st.metric(
        "Overall Risk",
        title_case(risk.get("overall_risk")),
        help="Qualitative classification of overall risk based on the operating and forecast signals.",
    )

st.caption(
    "Composite risk score and qualitative risk classification are "
    "separate measures: the score is continuous; qualitative risk "
    "is driven by forecast commitment and pipeline dependency."
)


# ==================================================
# FORECAST DECOMPOSITION
# ==================================================

section_title(
    "Forecast Decomposition",
    "Breakdown of how committed backlog, weighted pipeline, utilization, and execution risk combine into the final forecast.",
)

dcols = st.columns(5)

with dcols[0]:
    st.metric(
        "Committed Backlog",
        money(decomposition.get("committed_backlog")),
        help="Revenue that is already contractually or operationally committed to delivery.",
    )

with dcols[1]:
    st.metric(
        "Weighted Pipeline",
        money(decomposition.get("weighted_pipeline")),
        help="Probability-adjusted pipeline contribution. This is the pipeline after conversion weighting.",
    )

with dcols[2]:
    st.metric(
        "Utilization Adjustment",
        money(decomposition.get("utilization_adjustment")),
        help="Adjustment for expected utilization or capacity conversion impact on forecast performance.",
    )

with dcols[3]:
    st.metric(
        "Execution Risk",
        money(decomposition.get("risk_adjustment")),
        help="Risk adjustment representing execution uncertainty or downside probability in the forecast.",
    )

with dcols[4]:
    st.metric(
        "Final Forecast",
        money(decomposition.get("forecast_revenue")),
        help="Final forecast after all decomposition components are combined into one operating number.",
    )

st.caption(
    "Forecast = committed backlog + weighted pipeline + utilization "
    "adjustment + execution-risk contribution. The execution-risk "
    "contribution is displayed as a negative amount."
)


# ==================================================
# FORECAST RISK
# ==================================================

section_title(
    "Forecast Risk & Revenue Quality",
    "Measures of forecast confidence, coverage, dependency, and headroom used to judge revenue quality.",
)

rcols = st.columns(6)

with rcols[0]:
    st.metric(
        "Risk Score",
        f"{float(risk.get('risk_score', 0)):.1f}/100",
        help="Continuous risk score used to compare the forecast quality against the operating baseline.",
    )

with rcols[1]:
    st.metric(
        "Score Band",
        title_case(risk.get("risk_score_status")),
        help="Categorized risk band based on the underlying numeric risk score.",
    )

with rcols[2]:
    st.metric(
        "Committed Coverage",
        pct(risk.get("committed_forecast_coverage")),
        help="Coverage of the forecast by committed backlog. Higher values indicate stronger delivery certainty.",
    )

with rcols[3]:
    st.metric(
        "Pipeline Dependency",
        pct(risk.get("pipeline_dependency")),
        help="Share of the forecast depending on pipeline conversion versus already committed work.",
    )

with rcols[4]:
    st.metric(
        "Forecast Headroom",
        money(risk.get("forecast_headroom")),
        help="How much cushion remains between current forecast and the plan or risk threshold.",
    )

with rcols[5]:
    st.metric(
        "Headroom %",
        pct(risk.get("forecast_headroom_pct")),
        help="Percentage cushion compared with the forecast or plan threshold.",
    )

detail = st.columns(3)

with detail[0]:
    st.write("**Overall Risk**")
    st.write(title_case(risk.get("overall_risk")))

with detail[1]:
    st.write("**Forecast Risk**")
    st.write(title_case(risk.get("forecast_risk")))

with detail[2]:
    st.write("**Pipeline Risk**")
    st.write(title_case(risk.get("pipeline_risk")))


# ==================================================
# MONTE CARLO
# ==================================================

section_title(
    "Monte Carlo Forecast",
    "Probability distribution of outcomes across thousands of simulations to estimate revenue confidence bands.",
)

if monte_carlo:
    distribution = monte_carlo.get("distribution", {})
    budget_analysis = monte_carlo.get("budget_analysis", {})

    mcols = st.columns(6)

    with mcols[0]:
        st.metric(
            "P10",
            money(distribution.get("p10")),
            help="Lower-bound forecast outcome at the 10th percentile of simulated results.",
        )

    with mcols[1]:
        st.metric(
            "P50",
            money(distribution.get("p50")),
            help="Median simulated revenue outcome, representing the most balanced scenario.",
        )

    with mcols[2]:
        st.metric(
            "P90",
            money(distribution.get("p90")),
            help="Upper-bound forecast outcome at the 90th percentile of simulated results.",
        )

    with mcols[3]:
        st.metric(
            "Probability ≥ Budget",
            pct(budget_analysis.get("probability_above_budget")),
            help="Likelihood that the forecast exceeds budget under simulation assumptions.",
        )

    with mcols[4]:
        st.metric(
            "Probability < Budget",
            pct(budget_analysis.get("probability_below_budget")),
            help="Likelihood that the forecast lands below budget under simulation assumptions.",
        )

    with mcols[5]:
        st.metric(
            "Simulation Risk",
            title_case(monte_carlo.get("risk", {}).get("risk_level")),
            help="Overall risk classification derived from the simulation distribution and budget sensitivity.",
        )

    st.caption(
        f"5,000 deterministic-seed simulations using backlog, pipeline, "
        f"utilization and execution-risk volatility."
    )

else:
    st.info("Monte Carlo results are not available.")


# ==================================================
# STAFFING
# ==================================================

section_title(
    "Staffing & Capacity",
    "Actual and planned staffing hours, cost, and capacity health used to validate delivery assumptions.",
)

scols = st.columns(5)

with scols[0]:
    st.metric(
        "Actual Hours",
        f"{float(staffing.get('actual_hours', 0) or 0):,.0f}",
        help="Actual staffed hours consumed in the current period for delivery capacity tracking.",
    )

with scols[1]:
    st.metric(
        "Hours Budget",
        f"{float(staffing.get('budget_hours', 0) or 0):,.0f}",
        help="Planned staffing-hours budget used as the baseline for capacity comparisons.",
    )

with scols[2]:
    st.metric(
        "Hours vs Budget",
        pct(staffing.get("hours_attainment_pct")),
        help="Actual hours relative to budget, indicating whether staffing is under or over plan.",
    )

with scols[3]:
    st.metric(
        "Blended Cost / Hour",
        money(staffing.get("blended_cost_per_hour")),
        help="Average cost per staffed hour, including mix of labor classes and rate assumptions.",
    )

with scols[4]:
    st.metric(
        "Capacity Status",
        title_case(staffing.get("capacity_status")),
        help="Overall staffing capacity classification for the current operating pattern.",
    )

st.warning(
    staffing.get(
        "capacity_measurement_note",
        "Capacity measurement note unavailable.",
    )
)


# ==================================================
# FINANCIAL POSITION
# ==================================================

section_title(
    "Financial Position",
    "Gap between actual, forecast, and budget performance to understand operating shortfall or upside.",
)

fcols = st.columns(4)

with fcols[0]:
    st.metric(
        "Actual vs Budget",
        money(reasoning.get("budget_gap")),
        help="Difference between actual revenue and budget as a dollar gap.",
    )

with fcols[1]:
    st.metric(
        "Budget Gap %",
        pct(reasoning.get("budget_gap_pct")),
        help="Variance between actual and budget performance as a percentage of plan.",
    )

with fcols[2]:
    st.metric(
        "Forecast vs Budget",
        money(reasoning.get("forecast_gap")),
        help="Difference between forecast revenue and the original budget position.",
    )

with fcols[3]:
    st.metric(
        "Forecast Gap %",
        pct(reasoning.get("forecast_gap_pct")),
        help="Forecast-to-budget gap expressed as a percentage, highlighting material upside or downside.",
    )


# ==================================================
# INSIGHTS
# ==================================================

section_title(
    "Key Insights",
    "Priority findings surfaced from the finance and forecast analysis, including operational risk and performance deviations.",
)

if insights:
    for insight in insights:
        severity = str(
            insight.get("severity", "INFO")
        ).upper()
        content = (
            f"**{insight.get('category', 'General')} — "
            f"{insight.get('metric', '')}**\n\n"
            f"{insight.get('message', '')}"
        )

        if severity == "HIGH":
            st.error(content)
        elif severity == "MEDIUM":
            st.warning(content)
        else:
            st.info(content)
else:
    st.info("No material insights detected.")


# ==================================================
# RECOMMENDATIONS
# ==================================================

section_title(
    "Recommended Actions",
    "Suggested next steps to address risk, improve forecast quality, and act on the current operating conditions.",
)

if recommendations:
    for recommendation in recommendations:
        priority = str(
            recommendation.get("priority", "LOW")
        ).upper()

        category = recommendation.get("category", "Action")
        action = recommendation.get("action", "")
        rationale = recommendation.get("rationale", "")
        impact = recommendation.get("financial_impact")

        st.markdown(f"### {category}")
        st.write(f"**Priority:** {priority}")
        st.write(f"**Action:** {action}")

        if rationale:
            st.write(f"**Rationale:** {rationale}")

        if impact is not None:
            st.write(
                "**Financial Impact:** "
                + money(impact)
            )
else:
    st.info("No recommendations generated.")


# ==================================================
# REVENUE PERFORMANCE
# ==================================================

section_title(
    "Revenue Performance",
    "Trend of monthly revenue performance used to validate the operating forecast and business momentum.",
)

if monthly_revenue:
    st.plotly_chart(
        revenue_chart(monthly_revenue),
        width="stretch",
    )
else:
    st.info("No monthly revenue data available.")


# ==================================================
# FORECAST + BACKLOG
# ==================================================

left, right = st.columns(2)

with left:
    section_title(
        "Forecast Position",
        "Current revenue forecast compared to backlog and pipeline to understand deliverability and coverage.",
    )

    st.metric(
        "Canonical Forecast Revenue",
        money(canonical_forecast),
        help="The single canonical revenue forecast used in the executive scorecard and dashboard summary.",
    )
    st.metric(
        "Committed Backlog",
        money(committed_backlog),
        help="Backlog already committed to delivery and contributing to the forecast base.",
    )
    st.metric(
        "Weighted Pipeline",
        money(weighted_pipeline),
        help="Consideration of pipeline value after probability adjustment and conversion weighting.",
    )

    st.plotly_chart(
        variance_chart(variance),
        width="stretch",
    )

with right:
    section_title(
        "Backlog Position",
        "Backlog profile and delivery mix across the current book of work and committed demand.",
    )

    st.plotly_chart(
        backlog_chart(backlog),
        width="stretch",
    )


# ==================================================
# BUSINESS UNIT PERFORMANCE
# ==================================================

section_title(
    "Business Unit Performance",
    "Revenue, variance, and margin performance by business unit to compare operating outcomes across the portfolio.",
)

if business_units:
    bu_df = pd.DataFrame(business_units)

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
            bu_df[available_columns],
            width="stretch",
            hide_index=True,
        )

    st.plotly_chart(
        business_unit_chart(business_units),
        width="stretch",
    )
else:
    st.info("No business-unit data available.")


# ==================================================
# FORECAST ACCURACY
# ==================================================

section_title(
    "Historical Forecast / Budget Accuracy",
    "Recent forecast and budget accuracy history to understand performance consistency and model reliability.",
)

if forecast_accuracy:
    st.dataframe(
        pd.DataFrame(forecast_accuracy),
        width="stretch",
        hide_index=True,
    )
else:
    st.info("No historical forecast data available.")


# ==================================================
# SCENARIO SIMULATOR
# ==================================================

section_title("Scenario Simulator")

st.caption(
    "Pressure-test revenue under pipeline, utilization, pricing "
    "and delivery-slippage assumptions."
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

    current_budget_utilization = float(
        source_metrics.get("budget_utilization", 0) or 0
    )
    if current_budget_utilization <= 1:
        current_budget_utilization *= 100

    scenario_utilization = st.slider(
        "Current Utilization",
        min_value=0.0,
        max_value=150.0,
        value=float(current_budget_utilization),
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

if st.button("Run Scenario", type="primary"):
    payload = {
        "base_revenue": base_revenue,
        "pipeline_revenue": scenario_pipeline,
        "utilization": scenario_utilization / 100,
        "pipeline_conversion_change": pipeline_conversion_change,
        "utilization_change": utilization_change,
        "billing_rate_change": billing_rate_change,
        "slippage_rate": slippage_rate,
    }

    try:
        scenario = run_scenario(payload)

        result_cols = st.columns(4)

        with result_cols[0]:
            st.metric(
                "Base Revenue",
                money(scenario.get("base_revenue")),
            )

        with result_cols[1]:
            st.metric(
                "Scenario Revenue",
                money(scenario.get("scenario_revenue")),
            )

        with result_cols[2]:
            st.metric(
                "Revenue Impact",
                money(scenario.get("revenue_change")),
            )

        with result_cols[3]:
            st.metric(
                "Impact %",
                pct(scenario.get("revenue_change_pct")),
            )

    except Exception as exc:
        show_error(f"Scenario calculation failed: {exc}")


# ==================================================
# DATA QUALITY
# ==================================================

if data_quality.get("flags"):
    section_title("Data Quality")

    for flag in data_quality["flags"]:
        message = (
            f"**{flag.get('area', 'data').title()}** — "
            f"{flag.get('message', '')}"
        )
        if str(flag.get("severity", "")).upper() == "HIGH":
            st.error(message)
        else:
            st.warning(message)


# ==================================================
# SOURCE DATA
# ==================================================

with st.expander("Canonical Source Metrics"):
    source_df = pd.DataFrame(
        [
            {"Metric": key, "Value": value}
            for key, value in source_metrics.items()
        ]
    )
    st.dataframe(
        source_df,
        width="stretch",
        hide_index=True,
    )


st.divider()
st.caption("X-Fin | Delivery Finance Intelligence")
