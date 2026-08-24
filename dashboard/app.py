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

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="X-Fin | BCG X Delivery Finance",
    page_icon="📊",
    layout="wide",
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title(
    "X-Fin — BCG X Delivery Finance"
)

st.caption(
    "Finance performance, forecasting, backlog and scenario intelligence"
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

try:

    summary = get_summary()
    monthly_revenue = get_monthly_revenue()
    backlog = get_backlog()
    variance = get_variance()
    forecast = get_forecast()
    forecast_accuracy = get_forecast_accuracy()
    business_units = get_business_units()

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
)

budget_revenue = float(
    budget.get(
        "budget_revenue",
        0,
    )
)

forecast_revenue = float(
    forecast_data.get(
        "forecast_revenue",
        0,
    )
)

committed_backlog = float(
    backlog_summary.get(
        "committed_backlog",
        0,
    )
)

pipeline_value = float(
    pipeline.get(
        "pipeline_value",
        0,
    )
)

weighted_pipeline = float(
    pipeline.get(
        "weighted_pipeline",
        0,
    )
)

utilization = 0.74

gross_margin = (
    actual_revenue
    - float(
        finance.get(
            "actual_cost",
            0,
        )
    )
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
        use_container_width=True,
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
        use_container_width=True,
    )


with right:

    section_title(
        "Backlog Position"
    )

    st.plotly_chart(
        backlog_chart(
            backlog
        ),
        use_container_width=True,
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
        use_container_width=True,
        hide_index=True,
    )

    st.plotly_chart(
        business_unit_chart(
            business_units
        ),
        use_container_width=True,
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
        use_container_width=True,
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

scenario_left, scenario_right = st.columns(
    2
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

        "base_revenue":
            base_revenue,

        "pipeline_revenue":
            scenario_pipeline,

        "utilization":
            scenario_utilization,

        "pipeline_conversion_change":
            pipeline_conversion_change,

        "utilization_change":
            utilization_change,

        "billing_rate_change":
            billing_rate_change,

        "slippage_rate":
            slippage_rate,
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