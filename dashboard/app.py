import streamlit as st
import pandas as pd

from api import (
    get_summary,
    get_monthly_revenue,
    get_backlog,
    get_variance,
    get_forecast,
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
    forecast_decomposition_chart,
)


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="X-Fin | BCG X Delivery Finance",
    page_icon="",
    layout="wide",
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title(
    "X-Fin — Delivery Finance OS"
)

st.caption(
    "Finance performance, forecasting, backlog and scenario intelligence"
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

try:

    summary = get_summary()

    monthly_revenue = (
        get_monthly_revenue()
    )

    backlog = get_backlog()

    variance = get_variance()

    forecast = get_forecast()

    forecast_accuracy = (
        get_forecast_accuracy()
    )

    business_units = (
        get_business_units()
    )

    intelligence = (
        get_intelligence()
    )

except Exception as e:

    show_error(
        f"Unable to connect to the Finance API: {e}"
    )

    st.stop()


# --------------------------------------------------
# SUMMARY DATA
# --------------------------------------------------

finance = summary.get(
    "finance",
    {},
)

budget = summary.get(
    "budget",
    {},
)

backlog_summary = summary.get(
    "backlog",
    {},
)

forecast_data = forecast.get(
    "forecast",
    {},
)

pipeline = forecast.get(
    "pipeline",
    {},
)


actual_revenue = float(
    finance.get(
        "actual_revenue",
        0,
    )
    or 0
)


budget_revenue = float(
    budget.get(
        "budget_revenue",
        0,
    )
    or 0
)


forecast_revenue = float(
    forecast_data.get(
        "forecast_revenue",
        0,
    )
    or 0
)


committed_backlog = float(
    backlog_summary.get(
        "committed_backlog",
        0,
    )
    or 0
)


pipeline_value = float(
    pipeline.get(
        "pipeline_value",
        0,
    )
    or 0
)


weighted_pipeline = float(
    pipeline.get(
        "weighted_pipeline",
        0,
    )
    or 0
)


# --------------------------------------------------
# DERIVED METRICS
# --------------------------------------------------

actual_cost = float(
    finance.get(
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


revenue_variance_pct = (
    (
        actual_revenue
        - budget_revenue
    )
    / budget_revenue
    * 100
    if budget_revenue
    else 0
)


utilization = 0.74


# --------------------------------------------------
# KPI ROW
# --------------------------------------------------

section_title(
    "Executive Performance"
)

cols = st.columns(8)


with cols[0]:

    metric_card(
        "Actual Revenue",
        format_currency(
            actual_revenue
        ),
    )


with cols[1]:

    metric_card(
        "vs Budget",
        format_percentage(
            revenue_variance_pct
        ),
    )


with cols[2]:

    metric_card(
        "Forecast Revenue",
        format_currency(
            forecast_revenue
        ),
    )


with cols[3]:

    metric_card(
        "Committed Backlog",
        format_currency(
            committed_backlog
        ),
    )


with cols[4]:

    metric_card(
        "Pipeline",
        format_currency(
            pipeline_value
        ),
    )


with cols[5]:

    metric_card(
        "Weighted Pipeline",
        format_currency(
            weighted_pipeline
        ),
    )


with cols[6]:

    metric_card(
        "Utilization",
        format_percentage(
            utilization * 100
        ),
    )


with cols[7]:

    metric_card(
        "Gross Margin",
        format_percentage(
            gross_margin_pct
        ),
    )


# --------------------------------------------------
# EXECUTIVE INTELLIGENCE
# --------------------------------------------------

section_title(
    "Executive Intelligence"
)


reasoning = intelligence.get(
    "reasoning",
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


intelligence_status = (
    intelligence.get(
        "status",
        "unknown",
    )
)


intelligence_cols = st.columns(4)


with intelligence_cols[0]:

    performance = reasoning.get(
        "performance",
        "unknown",
    )

    st.metric(
        "Performance",
        str(
            performance
        ).replace(
            "_",
            " ",
        ).title(),
    )


with intelligence_cols[1]:

    forecast_status = reasoning.get(
        "forecast_status",
        "unknown",
    )

    st.metric(
        "Forecast Status",
        str(
            forecast_status
        ).replace(
            "_",
            " ",
        ).title(),
    )


with intelligence_cols[2]:

    confidence = reasoning.get(
        "forecast_confidence_base",
        None,
    )

    if confidence is not None:

        st.metric(
            "Committed Coverage",
            f"{float(confidence):.1f}%",
        )

    else:

        st.metric(
            "Committed Coverage",
            "N/A",
        )


with intelligence_cols[3]:

    forward_coverage = reasoning.get(
        "forward_coverage",
        None,
    )

    if forward_coverage is not None:

        st.metric(
            "Forward Coverage",
            f"{float(forward_coverage):.1f}%",
        )

    else:

        st.metric(
            "Forward Coverage",
            "N/A",
        )


# --------------------------------------------------
# INTELLIGENCE FINANCIAL POSITION
# --------------------------------------------------

intelligence_fin_cols = st.columns(4)


with intelligence_fin_cols[0]:

    budget_gap = reasoning.get(
        "budget_gap",
        0,
    )

    st.metric(
        "Actual vs Budget",
        format_currency(
            budget_gap
        ),
    )


with intelligence_fin_cols[1]:

    budget_gap_pct = reasoning.get(
        "budget_gap_pct",
        0,
    )

    st.metric(
        "Budget Gap %",
        f"{float(budget_gap_pct):.1f}%",
    )


with intelligence_fin_cols[2]:

    forecast_gap = reasoning.get(
        "forecast_gap",
        0,
    )

    st.metric(
        "Forecast vs Budget",
        format_currency(
            forecast_gap
        ),
    )


with intelligence_fin_cols[3]:

    forecast_gap_pct = reasoning.get(
        "forecast_gap_pct",
        0,
    )

    st.metric(
        "Forecast Gap %",
        f"{float(forecast_gap_pct):.1f}%",
    )


# --------------------------------------------------
# FORECAST DECOMPOSITION
# --------------------------------------------------

section_title(
    "Forecast Decomposition"
)


forecast_decomposition = (
    intelligence.get(
        "forecast_decomposition",
        {},
    )
)


decomposition_cols = st.columns(5)


with decomposition_cols[0]:

    st.metric(
        "Committed Backlog",
        format_currency(
            forecast_decomposition.get(
                "committed_backlog",
                0,
            )
        ),
    )


with decomposition_cols[1]:

    st.metric(
        "Weighted Pipeline",
        format_currency(
            forecast_decomposition.get(
                "weighted_pipeline",
                0,
            )
        ),
    )


with decomposition_cols[2]:

    st.metric(
        "Utilization Adjustment",
        format_currency(
            forecast_decomposition.get(
                "utilization_adjustment",
                0,
            )
        ),
    )


with decomposition_cols[3]:

    st.metric(
        "Risk Adjustment",
        format_currency(
            forecast_decomposition.get(
                "risk_adjustment",
                0,
            )
        ),
    )


with decomposition_cols[4]:

    st.metric(
        "Final Forecast",
        format_currency(
            forecast_decomposition.get(
                "forecast_revenue",
                forecast_revenue,
            )
        ),
    )


if forecast_decomposition:

    st.plotly_chart(
        forecast_decomposition_chart(
            forecast_decomposition
        ),
        width="stretch",
    )

else:

    st.info(
        "Forecast decomposition is not available."
    )


# --------------------------------------------------
# INSIGHTS
# --------------------------------------------------

if insights:

    st.subheader(
        "Key Insights"
    )

    for insight in insights:

        severity = str(
            insight.get(
                "severity",
                "INFO",
            )
        ).upper()

        category = insight.get(
            "category",
            "General",
        )

        metric = insight.get(
            "metric",
            "",
        )

        message = insight.get(
            "message",
            "",
        )

        content = (
            f"**{category} — {metric}**\n\n"
            f"{message}"
        )

        if severity == "HIGH":

            st.error(
                content
            )

        elif severity == "MEDIUM":

            st.warning(
                content
            )

        else:

            st.info(
                content
            )


# --------------------------------------------------
# RECOMMENDATIONS
# --------------------------------------------------

if recommendations:

    st.subheader(
        "Recommended Actions"
    )

    for recommendation in recommendations:

        priority = str(
            recommendation.get(
                "priority",
                "LOW",
            )
        ).upper()

        category = recommendation.get(
            "category",
            "Action",
        )

        action = recommendation.get(
            "action",
            "",
        )

        rationale = recommendation.get(
            "rationale",
            "",
        )

        financial_impact = (
            recommendation.get(
                "financial_impact",
                None,
            )
        )

        st.markdown(
            f"### {category}"
        )

        st.write(
            f"**Priority:** {priority}"
        )

        st.write(
            f"**Action:** {action}"
        )

        if rationale:

            st.write(
                f"**Rationale:** {rationale}"
            )

        if financial_impact is not None:

            st.write(
                "**Financial Impact:** "
                + format_currency(
                    float(
                        financial_impact
                    )
                )
            )


# --------------------------------------------------
# REVENUE PERFORMANCE
# --------------------------------------------------

section_title(
    "Revenue Performance"
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


# --------------------------------------------------
# FORECAST + VARIANCE
# --------------------------------------------------

left, right = st.columns(2)


with left:

    section_title(
        "Forecast Position"
    )

    st.metric(
        "Forecast Revenue",
        format_currency(
            forecast_revenue
        ),
    )

    st.metric(
        "Committed Backlog",
        format_currency(
            committed_backlog
        ),
    )

    st.metric(
        "Weighted Pipeline",
        format_currency(
            weighted_pipeline
        ),
    )

    st.plotly_chart(
        variance_chart(
            variance
        ),
        width="stretch",
    )


with right:

    section_title(
        "Backlog Position"
    )

    st.plotly_chart(
        backlog_chart(
            backlog
        ),
        width="stretch",
    )


# --------------------------------------------------
# BUSINESS UNIT PERFORMANCE
# --------------------------------------------------

section_title(
    "Business Unit Performance"
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

else:

    st.info(
        "No business-unit data available."
    )


# --------------------------------------------------
# FORECAST ACCURACY
# --------------------------------------------------

section_title(
    "Historical Forecast / Budget Accuracy"
)


if forecast_accuracy:

    accuracy_df = pd.DataFrame(
        forecast_accuracy
    )

    st.dataframe(
        accuracy_df,
        width="stretch",
        hide_index=True,
    )

else:

    st.info(
        "No historical forecast data available."
    )


# --------------------------------------------------
# SCENARIO SIMULATOR
# --------------------------------------------------

section_title(
    "Scenario Simulator"
)


st.caption(
    "Pressure-test revenue under pipeline, utilization, "
    "pricing and delivery-slippage assumptions."
)


scenario_left, scenario_right = (
    st.columns(2)
)


with scenario_left:

    base_revenue = st.number_input(
        "Base Revenue",
        min_value=0.0,
        value=float(
            actual_revenue
        ),
        step=1_000_000.0,
    )

    scenario_pipeline = st.number_input(
        "Pipeline Revenue",
        min_value=0.0,
        value=float(
            pipeline_value
        ),
        step=1_000_000.0,
    )

    scenario_utilization = st.slider(
        "Current Utilization",
        min_value=0.0,
        max_value=1.5,
        value=0.74,
        step=0.01,
    )


with scenario_right:

    pipeline_conversion_change = (
        st.slider(
            "Pipeline Conversion Change",
            min_value=-0.50,
            max_value=0.50,
            value=0.0,
            step=0.01,
            format="%.0f%%",
        )
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
        "utilization": scenario_utilization,
        "pipeline_conversion_change": (
            pipeline_conversion_change
        ),
        "utilization_change": (
            utilization_change
        ),
        "billing_rate_change": (
            billing_rate_change
        ),
        "slippage_rate": slippage_rate,
    }

    try:

        scenario = run_scenario(
            payload
        )

        st.subheader(
            "Scenario Result"
        )

        result_cols = st.columns(4)


        with result_cols[0]:

            st.metric(
                "Base Revenue",
                format_currency(
                    scenario[
                        "base_revenue"
                    ]
                ),
            )


        with result_cols[1]:

            st.metric(
                "Scenario Revenue",
                format_currency(
                    scenario[
                        "scenario_revenue"
                    ]
                ),
            )


        with result_cols[2]:

            st.metric(
                "Revenue Impact",
                format_currency(
                    scenario[
                        "revenue_change"
                    ]
                ),
            )


        with result_cols[3]:

            st.metric(
                "Impact %",
                format_percentage(
                    scenario[
                        "revenue_change_pct"
                    ]
                ),
            )

    except Exception as e:

        show_error(
            f"Scenario calculation failed: {e}"
        )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "X-Fin | Finance Analytics & Forecasting Engine"
)