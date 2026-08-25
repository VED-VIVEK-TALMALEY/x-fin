import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from dashboard.api import get_intelligence


st.set_page_config(
    page_title="X-Fin Intelligence",
    page_icon="X",
    layout="wide",
)


# ============================================================
# Helpers
# ============================================================

def money(value):

    value = float(value or 0)

    if abs(value) >= 1_000_000_000:
        return f"₹{value / 1_000_000_000:.2f}B"

    if abs(value) >= 1_000_000:
        return f"₹{value / 1_000_000:.1f}M"

    if abs(value) >= 1_000:
        return f"₹{value / 1_000:.1f}K"

    return f"₹{value:,.0f}"


def pct(value):

    return f"{float(value or 0):.1f}%"


# ============================================================
# Header
# ============================================================

st.title("X-Fin")
st.caption(
    "Intelligent Delivery Finance Operating System"
)

st.divider()


# ============================================================
# Load intelligence
# ============================================================

try:

    data = get_intelligence()

except Exception as exc:

    st.error(
        "Unable to connect to the X-Fin API."
    )

    st.code(str(exc))

    st.stop()


reasoning = data.get(
    "reasoning",
    {},
)

source_metrics = data.get(
    "source_metrics",
    {},
)

forecast = data.get(
    "forecast",
    {},
)

insights = data.get(
    "insights",
    [],
)

recommendations = data.get(
    "recommendations",
    [],
)


# ============================================================
# Executive status
# ============================================================

performance = reasoning.get(
    "performance",
    "unknown",
)

forecast_status = reasoning.get(
    "forecast_status",
    "unknown",
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
        f"PERFORMANCE STATUS: {performance}"
    )


# ============================================================
# KPI cards
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Actual Revenue",
        money(
            reasoning.get(
                "actual_revenue"
            )
        ),
        f"{pct(reasoning.get('budget_gap_pct'))} vs budget",
    )


with col2:

    st.metric(
        "Budget",
        money(
            reasoning.get(
                "budget_revenue"
            )
        ),
    )


with col3:

    st.metric(
        "Forecast",
        money(
            reasoning.get(
                "forecast_revenue"
            )
        ),
        f"{pct(reasoning.get('forecast_gap_pct'))} vs budget",
    )


with col4:

    st.metric(
        "Forward Coverage",
        pct(
            reasoning.get(
                "forward_coverage"
            )
        ),
    )


st.divider()


# ============================================================
# Revenue outlook
# ============================================================

left, right = st.columns(
    [1.5, 1]
)


with left:

    st.subheader(
        "Revenue Outlook"
    )

    labels = [
        "Budget",
        "Forecast",
        "Actual",
    ]

    values = [
        reasoning.get(
            "budget_revenue",
            0,
        ),
        reasoning.get(
            "forecast_revenue",
            0,
        ),
        reasoning.get(
            "actual_revenue",
            0,
        ),
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=labels,
            y=values,
            text=[
                money(value)
                for value in values
            ],
            textposition="auto",
        )
    )

    fig.update_layout(
        height=400,
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20,
        ),
        yaxis_title="Revenue",
        showlegend=False,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


with right:

    st.subheader(
        "Forward Revenue"
    )

    committed = reasoning.get(
        "committed_backlog",
        0,
    )

    weighted = reasoning.get(
        "weighted_pipeline",
        0,
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=[
                "Committed Backlog",
                "Weighted Pipeline",
            ],
            y=[
                committed,
                weighted,
            ],
            text=[
                money(committed),
                money(weighted),
            ],
            textposition="auto",
        )
    )

    fig.update_layout(
        height=400,
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20,
        ),
        yaxis_title="Revenue",
        showlegend=False,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


# ============================================================
# Forecast bridge
# ============================================================

st.subheader(
    "Forecast Construction"
)

forecast_df = pd.DataFrame(
    {
        "Component": [
            "Committed Backlog",
            "Weighted Pipeline",
            "Utilization Adjustment",
            "Risk Adjustment",
            "Final Forecast",
        ],
        "Value": [
            forecast.get(
                "committed_backlog",
                0,
            ),
            forecast.get(
                "weighted_pipeline",
                0,
            ),
            forecast.get(
                "utilization_adjustment",
                0,
            ),
            -forecast.get(
                "risk_adjustment",
                0,
            ),
            forecast.get(
                "forecast_revenue",
                0,
            ),
        ],
    }
)

st.dataframe(
    forecast_df.assign(
        Value=forecast_df["Value"].apply(
            money
        )
    ),
    use_container_width=True,
    hide_index=True,
)


# ============================================================
# Insights + recommendations
# ============================================================

left, right = st.columns(2)


with left:

    st.subheader(
        "Financial Insights"
    )

    if not insights:

        st.info(
            "No material insights detected."
        )

    for insight in insights:

        severity = insight.get(
            "severity",
            "LOW",
        )

        category = insight.get(
            "category",
            "Finance",
        )

        message = insight.get(
            "message",
            "",
        )

        if severity == "HIGH":

            st.error(
                f"**{category}** — {message}"
            )

        elif severity == "MEDIUM":

            st.warning(
                f"**{category}** — {message}"
            )

        else:

            st.info(
                f"**{category}** — {message}"
            )


with right:

    st.subheader(
        "Recommended Actions"
    )

    if not recommendations:

        st.info(
            "No recommendations generated."
        )

    for recommendation in recommendations:

        priority = recommendation.get(
            "priority",
            "LOW",
        )

        category = recommendation.get(
            "category",
            "Finance",
        )

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

        if priority == "HIGH":

            st.error(
                f"**{category}**\n\n"
                f"{action}\n\n"
                f"*{rationale}*"
            )

        elif priority == "MEDIUM":

            st.warning(
                f"**{category}**\n\n"
                f"{action}\n\n"
                f"*{rationale}*"
            )

        else:

            st.success(
                f"**{category}**\n\n"
                f"{action}\n\n"
                f"*{rationale}*"
            )

        if impact is not None:

            st.caption(
                f"Associated financial value: "
                f"{money(impact)}"
            )


# ============================================================
# Source metrics
# ============================================================

with st.expander(
    "Source Financial Metrics"
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
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# Footer
# ============================================================

st.divider()

st.caption(
    "X-Fin | Delivery Finance Intelligence"
)