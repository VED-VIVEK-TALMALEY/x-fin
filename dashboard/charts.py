import pandas as pd
import plotly.graph_objects as go


CHART_TEMPLATE = "plotly_dark"
CHART_PAPER = "rgba(0, 0, 0, 0)"
CHART_GRID = "rgba(148, 163, 184, 0.16)"


def _style_chart(fig, height=400):
    fig.update_layout(
        template=CHART_TEMPLATE,
        paper_bgcolor=CHART_PAPER,
        plot_bgcolor=CHART_PAPER,
        height=height,
        margin=dict(l=24, r=24, t=48, b=28),
        font=dict(color="#e5e7eb"),
        hoverlabel=dict(bgcolor="#1f2937", font_color="#f8fafc"),
    )
    fig.update_xaxes(gridcolor=CHART_GRID, zerolinecolor=CHART_GRID)
    fig.update_yaxes(gridcolor=CHART_GRID, zerolinecolor=CHART_GRID)
    return fig


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
    )

    return _style_chart(fig)


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
    )

    return _style_chart(fig)


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
    )

    return _style_chart(fig)


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
    )

    return _style_chart(fig, height=450)


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
    )

    return _style_chart(fig, height=350)


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
        showlegend=False,
    )

    return _style_chart(fig, height=450)


def business_unit_heatmap(data):
    if not data:
        return go.Figure()

    df = pd.DataFrame(data)
    required = {
        "business_unit",
        "actual_revenue",
        "variance_pct",
        "gross_margin_pct",
    }
    if not required.issubset(df.columns):
        return go.Figure()

    metrics = [
        "actual_revenue",
        "variance_pct",
        "gross_margin_pct",
    ]
    labels = ["Revenue", "Variance %", "Gross Margin %"]
    values = []
    for metric in metrics:
        values.append(pd.to_numeric(df[metric], errors="coerce").fillna(0))

    fig = go.Figure(
        go.Heatmap(
            z=values,
            x=df["business_unit"].tolist(),
            y=labels,
            colorscale="Tealgrn",
            hovertemplate="%{y}<br>%{x}: %{z:.1f}<extra></extra>",
        )
    )
    fig.update_layout(title="Business Unit Performance Map")
    return _style_chart(fig, height=300)


def capacity_chart(staffing):
    staffing = staffing or {}
    labels = ["Actual Hours", "Hours Budget"]
    values = [
        float(staffing.get("actual_hours", 0) or 0),
        float(staffing.get("budget_hours", 0) or 0),
    ]
    fig = go.Figure(
        go.Bar(
            x=labels,
            y=values,
            marker_color=["#38bdf8", "#64748b"] ,
            text=[f"{value:,.0f}" for value in values],
            textposition="auto",
            hovertemplate="%{x}: %{y:,.0f} hours<extra></extra>",
        )
    )
    fig.update_layout(title="Staffing Hours: Actual vs Budget", showlegend=False)
    return _style_chart(fig, height=340)


def risk_driver_chart(risk):
    risk = risk or {}
    labels = ["Committed Coverage", "Pipeline Dependency", "Headroom"]
    values = [
        float(risk.get("committed_forecast_coverage", 0) or 0),
        float(risk.get("pipeline_dependency", 0) or 0),
        float(risk.get("forecast_headroom_pct", 0) or 0),
    ]
    fig = go.Figure(
        go.Bar(
            x=values,
            y=labels,
            orientation="h",
            marker_color=["#34d399", "#f59e0b", "#60a5fa"],
            text=[f"{value:.1f}%" for value in values],
            textposition="auto",
            hovertemplate="%{y}: %{x:.1f}%<extra></extra>",
        )
    )
    fig.update_layout(title="Forecast Risk Drivers", xaxis_title="Percent")
    return _style_chart(fig, height=340)


def forecast_confidence_chart(monte_carlo, budget):
    monte_carlo = monte_carlo or {}
    distribution = monte_carlo.get("distribution", {})
    labels = ["P10", "P25", "P50", "P75", "P90"]
    values = [float(distribution.get(label.lower(), 0) or 0) for label in labels]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=labels,
            y=values,
            mode="lines+markers",
            name="Simulated Revenue",
            line=dict(color="#22d3ee", width=3),
            fill="tozeroy",
            fillcolor="rgba(34, 211, 238, 0.12)",
            hovertemplate="%{x}: ₹%{y:,.0f}<extra></extra>",
        )
    )
    fig.add_hline(
        y=float(budget or 0),
        line_dash="dot",
        line_color="#f59e0b",
        annotation_text="Budget",
    )
    fig.update_layout(title="Forecast Confidence Distribution", yaxis_title="Revenue")
    return _style_chart(fig, height=340)


def accuracy_chart(data):
    if not data:
        return go.Figure()
    df = pd.DataFrame(data)
    date_column = next((column for column in ["month", "period", "date"] if column in df), None)
    value_columns = [column for column in ["actual_revenue", "forecast_revenue", "budget_revenue"] if column in df]
    if not date_column or not value_columns:
        return go.Figure()

    fig = go.Figure()
    for column in value_columns:
        fig.add_trace(
            go.Scatter(
                x=df[date_column],
                y=df[column],
                mode="lines+markers",
                name=column.replace("_", " ").title(),
            )
        )
    fig.update_layout(title="Historical Forecast Accuracy", yaxis_title="Revenue")
    return _style_chart(fig, height=360)