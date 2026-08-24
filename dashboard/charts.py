import pandas as pd
import plotly.graph_objects as go


def revenue_chart(data):

    if not data:
        return go.Figure()

    df = pd.DataFrame(data)

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

    actual = pd.DataFrame(actual_data)
    budget = pd.DataFrame(budget_data)

    if actual.empty:
        return go.Figure()

    actual["month"] = pd.to_datetime(
        actual["month"]
    )

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


def backlog_chart(backlog):

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
        )
    )

    fig.update_layout(
        title="Backlog Position",
        template="plotly_white",
        height=400,
    )

    return fig


def business_unit_chart(data):

    if not data:
        return go.Figure()

    df = pd.DataFrame(data)

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


def variance_chart(data):

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
        )
    )

    fig.update_layout(
        title="Revenue Variance",
        template="plotly_white",
        height=350,
    )

    return fig