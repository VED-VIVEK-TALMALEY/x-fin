import pandas as pd
import plotly.graph_objects as go


def revenue_chart(data):

    if not data:
        return go.Figure()

    df = pd.DataFrame(data)

    if "month" not in df.columns:
        return go.Figure()

    if "revenue" not in df.columns:
        return go.Figure()

    df["month"] = pd.to_datetime(
        df["month"]
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["month"],
            y=df["revenue"],
            mode="lines+markers",
            name="Actual Revenue",
        )
    )

    fig.update_layout(
        title="Monthly Revenue",
        xaxis_title="Month",
        yaxis_title="Revenue",
        hovermode="x unified",
        template="plotly_white",
        height=400,
    )

    return fig


def revenue_vs_budget_chart(
    actual_data,
    budget_data,
):

    actual = pd.DataFrame(
        actual_data or []
    )

    budget = pd.DataFrame(
        budget_data or []
    )

    if actual.empty:
        return go.Figure()

    if "month" not in actual.columns:
        return go.Figure()

    if "revenue" not in actual.columns:
        return go.Figure()

    actual["month"] = pd.to_datetime(
        actual["month"]
    )

    if not budget.empty and "month" in budget.columns:
        budget["month"] = pd.to_datetime(
            budget["month"]
        )

    merged = actual.merge(
        budget,
        on="month",
        how="left",
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=merged["month"],
            y=merged["revenue"],
            name="Actual",
        )
    )

    if "budget_revenue" in merged.columns:

        fig.add_trace(
            go.Bar(
                x=merged["month"],
                y=merged["budget_revenue"],
                name="Budget",
            )
        )

    fig.update_layout(
        title="Actual vs Budget Revenue",
        barmode="group",
        template="plotly_white",
        height=400,
    )

    return fig


def backlog_chart(
    backlog,
):

    backlog = backlog or {}

    waterfall = backlog.get(
        "waterfall",
        {},
    )

    labels = [
        "Opening Backlog",
        "New Wins",
        "Closing Backlog",
    ]

    values = [
        waterfall.get(
            "opening_backlog",
            0,
        ),
        waterfall.get(
            "new_wins",
            0,
        ),
        waterfall.get(
            "closing_backlog",
            0,
        ),
    ]

    fig = go.Figure(
        go.Bar(
            x=labels,
            y=values,
            name="Backlog",
        )
    )

    fig.update_layout(
        title="Backlog Position",
        template="plotly_white",
        height=400,
    )

    return fig


def business_unit_chart(
    data,
):

    if not data:
        return go.Figure()

    df = pd.DataFrame(data)

    required = {
        "actual_revenue",
        "business_unit",
    }

    if not required.issubset(
        df.columns
    ):
        return go.Figure()

    df = df.sort_values(
        "actual_revenue",
        ascending=True,
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df["actual_revenue"],
            y=df["business_unit"],
            orientation="h",
            name="Actual Revenue",
        )
    )

    fig.update_layout(
        title="Revenue by Business Unit",
        xaxis_title="Revenue",
        yaxis_title="Business Unit",
        template="plotly_white",
        height=450,
    )

    return fig


def variance_chart(
    data,
):

    data = data or {}

    labels = [
        "Actual vs Budget",
        "Forecast vs Budget",
    ]

    values = [
        data.get(
            "actual_vs_budget",
            0,
        ),
        data.get(
            "forecast_vs_budget",
            0,
        ),
    ]

    fig = go.Figure(
        go.Bar(
            x=labels,
            y=values,
            name="Variance",
        )
    )

    fig.update_layout(
        title="Revenue Variance",
        template="plotly_white",
        height=350,
    )

    return fig


def forecast_decomposition_chart(
    decomposition,
):

    decomposition = (
        decomposition or {}
    )

    committed_backlog = float(
        decomposition.get(
            "committed_backlog",
            0,
        )
        or 0
    )

    weighted_pipeline = float(
        decomposition.get(
            "weighted_pipeline",
            0,
        )
        or 0
    )

    utilization_adjustment = float(
        decomposition.get(
            "utilization_adjustment",
            0,
        )
        or 0
    )

    # API stores execution-risk contribution as a negative amount.
    risk_adjustment = float(
        decomposition.get(
            "risk_adjustment",
            0,
        )
        or 0
    )

    forecast_revenue = float(
        decomposition.get(
            "forecast_revenue",
            0,
        )
        or 0
    )

    fig = go.Figure(
        go.Waterfall(
            name="Forecast",
            orientation="v",
            measure=[
                "relative",
                "relative",
                "relative",
                "relative",
                "total",
            ],
            x=[
                "Committed Backlog",
                "Weighted Pipeline",
                "Utilization Adjustment",
                "Risk Adjustment",
                "Forecast Revenue",
            ],
            y=[
                committed_backlog,
                weighted_pipeline,
                utilization_adjustment,
                risk_adjustment,
                forecast_revenue,
            ],
            connector={
                "line": {
                    "width": 1,
                }
            },
        )
    )

    fig.update_layout(
        title="Forecast Revenue Decomposition",
        yaxis_title="Revenue",
        template="plotly_white",
        height=450,
        showlegend=False,
    )

    return fig