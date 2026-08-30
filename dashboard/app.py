from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# X-FIN IMPORTS
# ============================================================

from dashboard.api import (
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
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="X-Fin | Delivery Finance OS",
    page_icon="X",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       GLOBAL
       ====================================================== */

    .stApp {
        background:
            linear-gradient(
                180deg,
                #241421 0%,
                #111827 38%,
                #0f172a 100%
            );
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 4rem;
        max-width: 1600px;
    }

    /* ======================================================
       HEADER
       ====================================================== */

    .brand-title {
        color: #f3f4f6;
        font-size: 2.8rem;
        font-weight: 750;
        letter-spacing: -0.03em;
        line-height: 1.15;
        margin: 0;
    }

    .brand-accent {
        color: #f3f453;
    }

    .brand-subtitle {
        color: #9ca3af;
        font-size: 1rem;
        margin-top: 0.35rem;
        margin-bottom: 1.5rem;
    }

    /* ======================================================
       METRICS
       ====================================================== */

    div[data-testid="stMetric"] {
        background:
            rgba(31, 41, 55, 0.88);

        border:
            1px solid
            rgba(148, 163, 184, 0.20);

        border-radius:
            0.85rem;

        padding:
            0.8rem 0.9rem;

        box-shadow:
            0 4px 16px
            rgba(0, 0, 0, 0.16);
    }

    div[data-testid="stMetricLabel"] p {
        color: #9ca3af !important;
        font-weight: 500;
    }

    div[data-testid="stMetricValue"] {
        color: #f9fafb !important;
    }

    /* ======================================================
       TEXT
       ====================================================== */

    .stMarkdown,
    .stMarkdown p,
    label {
        color: #e5e7eb;
    }

    .stCaption,
    [data-testid="stCaptionContainer"] {
        color: #9ca3af;
    }

    /* ======================================================
       TABLES
       ====================================================== */

    [data-testid="stDataFrame"] {
        border:
            1px solid
            rgba(148, 163, 184, 0.20);

        border-radius:
            0.75rem;

        overflow: hidden;
    }

    /* ======================================================
       TABS
       ====================================================== */

    button[data-baseweb="tab"] {
        font-weight: 600;
    }

    /* ======================================================
       EXPANDERS
       ====================================================== */

    .streamlit-expanderHeader {
        color: #e5e7eb;
        font-weight: 600;
    }

    /* ======================================================
       DIVIDERS
       ====================================================== */

    hr {
        border-color: rgba(148, 163, 184, 0.18);
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
        <span class="brand-accent">X-Fin</span> — Delivery Finance OS
    </h1>
    <div class="brand-subtitle">
        Finance performance, forecasting, backlog and strategic intelligence
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HELPERS
# ============================================================

def safe_float(value: Any, default: float = 0.0) -> float:
    """Safely convert values to float."""
    try:
        if value is None:
            return default

        if isinstance(value, str):
            value = value.replace(",", "").replace("$", "").strip()

        result = float(value)

        if pd.isna(result):
            return default

        return result

    except (TypeError, ValueError):
        return default


def money(value: Any) -> str:
    """Format financial values safely."""
    return format_currency(safe_float(value))


def pct(value: Any) -> str:
    """Format percentage values safely."""
    return format_percentage(safe_float(value))


def percentage_point(value: Any) -> str:
    """Format percentage-point values."""
    return f"{safe_float(value):.1f}%"


def title_case(value: Any) -> str:
    """Human-readable label."""
    if value is None:
        return "Unknown"

    text = str(value).strip()

    if not text:
        return "Unknown"

    return text.replace("_", " ").title()


def normalize_percentage(value: Any) -> float:
    """
    Normalize percentage values.

    Examples:
        0.85 -> 85
        85   -> 85
    """
    value = safe_float(value)

    if 0 <= value <= 1:
        return value * 100

    return value


def format_dataframe(
    df: pd.DataFrame,
    currency_columns: list[str] | None = None,
    percentage_columns: list[str] | None = None,
) -> pd.DataFrame:
    """
    Create a display-safe copy of a dataframe.
    """
    output = df.copy()

    currency_columns = currency_columns or []
    percentage_columns = percentage_columns or []

    for column in currency_columns:
        if column in output.columns:
            output[column] = output[column].apply(money)

    for column in percentage_columns:
        if column in output.columns:
            output[column] = output[column].apply(
                lambda value: f"{safe_float(value):.1f}%"
            )

    return output


def render_table(
    data: list[dict[str, Any]] | pd.DataFrame,
    columns: list[str],
    currency_columns: list[str] | None = None,
    percentage_columns: list[str] | None = None,
) -> None:
    """
    Render a safe, formatted dataframe.
    """
    if isinstance(data, pd.DataFrame):
        df = data.copy()
    else:
        df = pd.DataFrame(data)

    if df.empty:
        return

    available = [
        column
        for column in columns
        if column in df.columns
    ]

    if not available:
        return

    df = df[available]

    df = format_dataframe(
        df,
        currency_columns=currency_columns,
        percentage_columns=percentage_columns,
    )

    st.dataframe(
        df,
        width="stretch",
        hide_index=True,
    )


# ============================================================
# LOAD DASHBOARD DATA
# ============================================================

@st.cache_data(
    ttl=60,
    show_spinner=False,
)
def load_dashboard_data() -> dict[str, Any]:
    """
    Load the complete dashboard snapshot.

    Cached for 60 seconds so Streamlit widget interactions
    do not repeatedly hit the Finance API.
    """

    return {
        "monthly_revenue": get_monthly_revenue(),
        "backlog": get_backlog(),
        "variance": get_variance(),
        "forecast_accuracy": get_forecast_accuracy(),
        "business_units": get_business_units(),
        "intelligence": get_intelligence(),
        "executive": get_executive_briefing(),
    }


# ============================================================
# API LOAD
# ============================================================

try:
    dashboard_data = load_dashboard_data()

except Exception as exc:
    show_error(
        f"Unable to connect to the Finance API: {exc}"
    )
    st.stop()


# ============================================================
# EXTRACT DATA
# ============================================================

monthly_revenue = dashboard_data.get(
    "monthly_revenue",
    [],
)

backlog = dashboard_data.get(
    "backlog",
    [],
)

variance = dashboard_data.get(
    "variance",
    [],
)

forecast_accuracy = dashboard_data.get(
    "forecast_accuracy",
    [],
)

business_units = dashboard_data.get(
    "business_units",
    [],
)

intelligence = dashboard_data.get(
    "intelligence",
    {},
)

executive_response = dashboard_data.get(
    "executive",
    {},
)


# ============================================================
# INTELLIGENCE LAYERS
# ============================================================

reasoning = intelligence.get(
    "reasoning",
    {},
) or {}

risk = intelligence.get(
    "risk",
    {},
) or {}

forecast = intelligence.get(
    "forecast",
    {},
) or {}

decomposition = intelligence.get(
    "forecast_decomposition",
    {},
) or {}

monte_carlo = intelligence.get(
    "monte_carlo",
    {},
) or {}

staffing = intelligence.get(
    "staffing",
    {},
) or {}

insights = intelligence.get(
    "insights",
    [],
) or []

recommendations = intelligence.get(
    "recommendations",
    [],
) or []

data_quality = intelligence.get(
    "data_quality",
    {},
) or {}

source_metrics = intelligence.get(
    "source_metrics",
    {},
) or {}


# ============================================================
# STRATEGIC INTELLIGENCE
# ============================================================

revenue_leakage = intelligence.get(
    "revenue_leakage",
    {},
) or {}

pipeline_intelligence = intelligence.get(
    "pipeline_intelligence",
    {},
) or {}

margin_risk = intelligence.get(
    "margin_risk",
    {},
) or {}

portfolio_risk = intelligence.get(
    "portfolio_risk",
    {},
) or {}


briefing = executive_response.get(
    "briefing",
    {},
) or {}


# ============================================================
# CANONICAL VALUES
# ============================================================

actual_revenue = safe_float(
    reasoning.get(
        "actual_revenue",
        0,
    )
)

budget_revenue = safe_float(
    reasoning.get(
        "budget_revenue",
        0,
    )
)

canonical_forecast = safe_float(
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
)

committed_backlog = safe_float(
    reasoning.get(
        "committed_backlog",
        0,
    )
)

weighted_pipeline = safe_float(
    reasoning.get(
        "weighted_pipeline",
        pipeline_intelligence.get(
            "weighted_pipeline",
            0,
        ),
    )
)

pipeline_value = safe_float(
    source_metrics.get(
        "pipeline_value",
        pipeline_intelligence.get(
            "pipeline_value",
            0,
        ),
    )
)

actual_cost = safe_float(
    source_metrics.get(
        "actual_cost",
        0,
    )
)

gross_margin = (
    actual_revenue - actual_cost
)

gross_margin_pct = (
    gross_margin
    / actual_revenue
    * 100
    if actual_revenue
    else 0
)

portfolio_risk_score = safe_float(
    portfolio_risk.get(
        "portfolio_risk_score",
        risk.get(
            "risk_score",
            0,
        ),
    )
)

revenue_at_risk = safe_float(
    portfolio_risk.get(
        "revenue_at_risk",
        0,
    )
)

leakage_value = safe_float(
    revenue_leakage.get(
        "total_potential_leakage",
        0,
    )
)

margin_at_risk = safe_float(
    margin_risk.get(
        "margin_at_risk",
        0,
    )
)

pipeline_quality = safe_float(
    pipeline_intelligence.get(
        "pipeline_quality_score",
        0,
    )
)


# ============================================================
# TABS
# ============================================================

tab_executive, tab_financials, tab_risk, tab_scenarios = st.tabs(
    [
        "Executive",
        "Financials",
        "Risk & Forecast",
        "Scenarios",
    ]
)


# ============================================================
# EXECUTIVE TAB
# ============================================================

with tab_executive:

    # ========================================================
    # EXECUTIVE BRIEFING
    # ========================================================

    section_title(
        "Executive Briefing",
        (
            "Management-level synthesis of revenue performance, "
            "forecast quality, portfolio risk and financial exposure."
        ),
    )

    if briefing:

        headline = briefing.get(
            "headline",
            "Current financial position requires management attention.",
        )

        management_summary = briefing.get(
            "management_summary",
            "",
        )

        st.info(
            f"**{headline}**"
        )

        if management_summary:
            st.caption(
                management_summary
            )

    else:
        st.warning(
            "Executive briefing is currently unavailable."
        )


    # ========================================================
    # DECISION SNAPSHOT
    # ========================================================

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


    # ========================================================
    # CORE PERFORMANCE
    # ========================================================

    section_title(
        "Core Performance",
        "Current revenue, forecast, backlog, pipeline and margin position.",
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


    # ========================================================
    # STRATEGIC INTELLIGENCE
    # ========================================================

    section_title(
        "Strategic Intelligence",
        (
            "Higher-order signals derived from leakage, "
            "pipeline quality, margin performance and portfolio exposure."
        ),
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
            f"Risk level: "
            f"{title_case(portfolio_risk.get('risk_level', 'unknown'))}"
        )


    # ========================================================
    # PORTFOLIO RISK
    # ========================================================

    section_title(
        "Portfolio Risk",
        (
            "Composite risk across forecast quality, pipeline dependency, "
            "revenue leakage and margin pressure."
        ),
    )

    risk_cols = st.columns(2)

    with risk_cols[0]:

        try:

            st.plotly_chart(
                executive_risk_chart(
                    portfolio_risk
                ),
                width="stretch",
            )

        except Exception as exc:

            st.warning(
                f"Unable to render portfolio risk chart: {exc}"
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


    # ========================================================
    # INSIGHTS
    # ========================================================

    section_title(
        "Key Insights",
        "Findings generated by the X-Fin intelligence stack.",
    )

    if insights:

        insight_columns = st.columns(3)

        for index, insight in enumerate(insights):

            if not isinstance(insight, dict):
                continue

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


    # ========================================================
    # RECOMMENDATIONS
    # ========================================================

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

            if not isinstance(recommendation, dict):
                continue

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
# FINANCIALS TAB
# ============================================================

with tab_financials:

    # ========================================================
    # FINANCIAL POSITION
    # ========================================================

    section_title(
        "Financial Position",
        "Actual, budget and forecast revenue gaps.",
    )

    fcols = st.columns(4)

    with fcols[0]:

        st.metric(
            "Actual Revenue",
            money(actual_revenue),
        )

    with fcols[1]:

        st.metric(
            "Actual vs Budget",
            money(
                reasoning.get(
                    "budget_gap",
                    0,
                )
            ),
        )

    with fcols[2]:

        st.metric(
            "Forecast",
            money(canonical_forecast),
        )

    with fcols[3]:

        st.metric(
            "Forecast vs Budget",
            money(
                reasoning.get(
                    "forecast_gap",
                    0,
                )
            ),
        )


    # ========================================================
    # REVENUE PERFORMANCE
    # ========================================================

    section_title(
        "Revenue Performance",
        "Historical monthly revenue trend.",
    )

    if monthly_revenue:

        try:

            st.plotly_chart(
                revenue_chart(
                    monthly_revenue
                ),
                width="stretch",
            )

        except Exception as exc:

            st.warning(
                f"Unable to render revenue chart: {exc}"
            )

    else:

        st.info(
            "No monthly revenue data available."
        )


    # ========================================================
    # FORECAST / BACKLOG
    # ========================================================

    left, right = st.columns(2)

    with left:

        section_title(
            "Forecast Position",
            "Canonical forecast compared with backlog and pipeline.",
        )

        forecast_metrics = st.columns(3)

        with forecast_metrics[0]:

            st.metric(
                "Forecast",
                money(canonical_forecast),
            )

        with forecast_metrics[1]:

            st.metric(
                "Backlog",
                money(committed_backlog),
            )

        with forecast_metrics[2]:

            st.metric(
                "Weighted Pipeline",
                money(weighted_pipeline),
            )

        try:

            st.plotly_chart(
                variance_chart(
                    variance
                ),
                width="stretch",
            )

        except Exception as exc:

            st.warning(
                f"Unable to render variance chart: {exc}"
            )


    with right:

        section_title(
            "Backlog Position",
            "Current committed backlog profile.",
        )

        try:

            st.plotly_chart(
                backlog_chart(
                    backlog
                ),
                width="stretch",
            )

        except Exception as exc:

            st.warning(
                f"Unable to render backlog chart: {exc}"
            )


    # ========================================================
    # BUSINESS UNITS
    # ========================================================

    section_title(
        "Business Unit Performance",
        "Revenue and margin comparison across business units.",
    )

    if business_units:

        bu_df = pd.DataFrame(
            business_units
        )

        render_table(
            bu_df,
            columns=[
                "business_unit",
                "actual_revenue",
                "budget_revenue",
                "variance",
                "variance_pct",
                "gross_margin_pct",
            ],
            currency_columns=[
                "actual_revenue",
                "budget_revenue",
                "variance",
            ],
            percentage_columns=[
                "variance_pct",
                "gross_margin_pct",
            ],
        )

        chart_cols = st.columns(2)

        with chart_cols[0]:

            try:

                st.plotly_chart(
                    business_unit_chart(
                        business_units
                    ),
                    width="stretch",
                )

            except Exception as exc:

                st.warning(
                    f"Unable to render business unit chart: {exc}"
                )

        with chart_cols[1]:

            try:

                st.plotly_chart(
                    business_unit_heatmap(
                        business_units
                    ),
                    width="stretch",
                )

            except Exception as exc:

                st.warning(
                    f"Unable to render business unit heatmap: {exc}"
                )

    else:

        st.info(
            "No business-unit data available."
        )


    # ========================================================
    # FORECAST ACCURACY
    # ========================================================

    section_title(
        "Historical Forecast / Budget Accuracy",
        "Historical reliability of forecasting and budgeting.",
    )

    if forecast_accuracy:

        try:

            st.plotly_chart(
                accuracy_chart(
                    forecast_accuracy
                ),
                width="stretch",
            )

        except Exception as exc:

            st.warning(
                f"Unable to render accuracy chart: {exc}"
            )

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


# ============================================================
# RISK & FORECAST TAB
# ============================================================

with tab_risk:

    # ========================================================
    # REVENUE LEAKAGE
    # ========================================================

    section_title(
        "Revenue Leakage",
        (
            "Potential value loss caused by revenue realization gaps, "
            "cost overruns and delivery/revenue mismatches."
        ),
    )

    leakage_projects = revenue_leakage.get(
        "top_leakage_projects",
        [],
    )

    if leakage_projects:

        render_table(
            leakage_projects,
            columns=[
                "project_id",
                "project_name",
                "business_unit",
                "revenue_gap",
                "cost_overrun",
                "potential_leakage",
                "severity",
            ],
            currency_columns=[
                "revenue_gap",
                "cost_overrun",
                "potential_leakage",
            ],
        )

    else:

        st.success(
            "No material revenue leakage detected."
        )


    # ========================================================
    # PIPELINE INTELLIGENCE
    # ========================================================

    section_title(
        "Pipeline Intelligence",
        (
            "Conversion probability, opportunity aging and "
            "concentration risk."
        ),
    )

    pipeline_projects = pipeline_intelligence.get(
        "top_attention_opportunities",
        [],
    )

    if pipeline_projects:

        render_table(
            pipeline_projects,
            columns=[
                "opportunity_id",
                "opportunity_name",
                "stage",
                "value",
                "probability",
                "adjusted_weighted_value",
                "freshness",
                "risk",
            ],
            currency_columns=[
                "value",
                "adjusted_weighted_value",
            ],
            percentage_columns=[
                "probability",
            ],
        )

        st.caption(
            "Pipeline concentration: "
            f"{safe_float(pipeline_intelligence.get('concentration_pct', 0)):.1f}%"
        )

    else:

        st.info(
            "No pipeline opportunities require immediate attention."
        )


    # ========================================================
    # MARGIN RISK
    # ========================================================

    section_title(
        "Margin Risk",
        "Project-level margin deterioration and cost-overrun exposure.",
    )

    margin_projects = margin_risk.get(
        "top_margin_risks",
        [],
    )

    if margin_projects:

        render_table(
            margin_projects,
            columns=[
                "project_id",
                "project_name",
                "business_unit",
                "revenue",
                "cost",
                "actual_margin_pct",
                "target_margin_pct",
                "margin_gap_pct",
                "risk",
            ],
            currency_columns=[
                "revenue",
                "cost",
            ],
            percentage_columns=[
                "actual_margin_pct",
                "target_margin_pct",
                "margin_gap_pct",
            ],
        )

    else:

        st.success(
            "No material margin risks detected."
        )


    # ========================================================
    # FORECAST DECOMPOSITION
    # ========================================================

    section_title(
        "Forecast Decomposition",
        (
            "How committed backlog, weighted pipeline, utilization "
            "and execution risk combine into the forecast."
        ),
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

    try:

        st.plotly_chart(
            forecast_decomposition_chart(
                decomposition
            ),
            width="stretch",
        )

    except Exception as exc:

        st.warning(
            f"Unable to render forecast decomposition: {exc}"
        )


    # ========================================================
    # FORECAST RISK
    # ========================================================

    section_title(
        "Forecast Risk & Revenue Quality",
        (
            "Coverage, dependency and forecast-headroom indicators."
        ),
    )

    risk_metrics = st.columns(5)

    with risk_metrics[0]:

        st.metric(
            "Risk Score",
            f"{safe_float(risk.get('risk_score', 0)):.1f}/100",
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

        try:

            st.plotly_chart(
                risk_driver_chart(
                    risk
                ),
                width="stretch",
            )

        except Exception as exc:

            st.warning(
                f"Unable to render risk driver chart: {exc}"
            )

    with chart_cols[1]:

        try:

            st.plotly_chart(
                forecast_confidence_chart(
                    monte_carlo,
                    budget_revenue,
                ),
                width="stretch",
            )

        except Exception as exc:

            st.warning(
                f"Unable to render forecast confidence chart: {exc}"
            )


    # ========================================================
    # MONTE CARLO
    # ========================================================

    section_title(
        "Monte Carlo Forecast",
        (
            "Simulated revenue distribution and probability "
            "of achieving budget."
        ),
    )

    if monte_carlo:

        distribution = monte_carlo.get(
            "distribution",
            {},
        ) or {}

        budget_analysis = monte_carlo.get(
            "budget_analysis",
            {},
        ) or {}

        mcols = st.columns(6)

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

        probability = (
            budget_analysis.get(
                "probability_of_achieving_budget",
                budget_analysis.get(
                    "probability",
                    None,
                ),
            )
        )

        with mcols[5]:

            if probability is not None:

                probability_value = safe_float(
                    probability
                )

                if probability_value <= 1:
                    probability_value *= 100

                st.metric(
                    "Budget Probability",
                    f"{probability_value:.1f}%",
                )

            else:

                st.metric(
                    "Budget Probability",
                    "N/A",
                )

        st.caption(
            "Monte Carlo results are generated by the canonical "
            "forecast simulation engine."
        )

    else:

        st.info(
            "Monte Carlo results are not available."
        )


    # ========================================================
    # STAFFING
    # ========================================================

    section_title(
        "Staffing & Capacity",
        "Actual staffing consumption versus planned delivery capacity.",
    )

    scols = st.columns(5)

    with scols[0]:

        st.metric(
            "Actual Hours",
            f"{safe_float(staffing.get('actual_hours', 0)):,.0f}",
        )

    with scols[1]:

        st.metric(
            "Hours Budget",
            f"{safe_float(staffing.get('budget_hours', 0)):,.0f}",
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

    try:

        st.plotly_chart(
            capacity_chart(
                staffing
            ),
            width="stretch",
        )

    except Exception as exc:

        st.warning(
            f"Unable to render capacity chart: {exc}"
        )


# ============================================================
# SCENARIOS TAB
# ============================================================

with tab_scenarios:

    # ========================================================
    # SCENARIO SIMULATOR
    # ========================================================

    section_title(
        "Scenario Simulator",
        (
            "Pressure-test revenue under pipeline conversion, "
            "utilization, billing-rate and delivery-slippage assumptions."
        ),
    )

    scenario_left, scenario_right = st.columns(2)

    with scenario_left:

        base_revenue = st.number_input(
            "Base Revenue",
            min_value=0.0,
            value=float(actual_revenue),
            step=1_000_000.0,
            format="%.0f",
        )

        scenario_pipeline = st.number_input(
            "Pipeline Revenue",
            min_value=0.0,
            value=float(pipeline_value),
            step=1_000_000.0,
            format="%.0f",
        )

        current_utilization = normalize_percentage(
            source_metrics.get(
                "budget_utilization",
                0,
            )
        )

        scenario_utilization = st.slider(
            "Current Utilization",
            min_value=0.0,
            max_value=150.0,
            value=min(
                max(
                    float(current_utilization),
                    0.0,
                ),
                150.0,
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


    # ========================================================
    # SCENARIO SUMMARY
    # ========================================================

    st.divider()

    scenario_summary = st.columns(4)

    with scenario_summary[0]:

        st.metric(
            "Base Revenue",
            money(base_revenue),
        )

    with scenario_summary[1]:

        st.metric(
            "Pipeline",
            money(scenario_pipeline),
        )

    with scenario_summary[2]:

        st.metric(
            "Utilization",
            f"{scenario_utilization:.0f}%",
        )

    with scenario_summary[3]:

        st.metric(
            "Slippage",
            f"{slippage_rate * 100:.0f}%",
        )


    # ========================================================
    # RUN SCENARIO
    # ========================================================

    run_scenario_button = st.button(
        "Run Scenario",
        type="primary",
        width="stretch",
    )

    if run_scenario_button:

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

            with st.spinner(
                "Running scenario simulation..."
            ):

                scenario = run_scenario(
                    payload
                )

            # ----------------------------------------------
            # RESULTS
            # ----------------------------------------------

            result_cols = st.columns(4)

            with result_cols[0]:

                st.metric(
                    "Base Revenue",
                    money(
                        scenario.get(
                            "base_revenue",
                            base_revenue,
                        )
                    ),
                )

            with result_cols[1]:

                st.metric(
                    "Scenario Revenue",
                    money(
                        scenario.get(
                            "scenario_revenue",
                            0,
                        )
                    ),
                )

            with result_cols[2]:

                revenue_change = safe_float(
                    scenario.get(
                        "revenue_change",
                        0,
                    )
                )

                st.metric(
                    "Revenue Impact",
                    money(
                        revenue_change
                    ),
                    delta=money(
                        revenue_change
                    ),
                )

            with result_cols[3]:

                st.metric(
                    "Impact %",
                    pct(
                        scenario.get(
                            "revenue_change_pct",
                            0,
                        )
                    ),
                )

            # ----------------------------------------------
            # BUDGET COMPARISON
            # ----------------------------------------------

            scenario_revenue = safe_float(
                scenario.get(
                    "scenario_revenue",
                    0,
                )
            )

            if budget_revenue:

                scenario_budget_achievement = (
                    scenario_revenue
                    / budget_revenue
                    * 100
                )

                st.subheader(
                    "Budget Impact"
                )

                budget_cols = st.columns(3)

                with budget_cols[0]:

                    st.metric(
                        "Budget",
                        money(
                            budget_revenue
                        ),
                    )

                with budget_cols[1]:

                    st.metric(
                        "Scenario Revenue",
                        money(
                            scenario_revenue
                        ),
                    )

                with budget_cols[2]:

                    st.metric(
                        "Budget Achievement",
                        f"{scenario_budget_achievement:.1f}%",
                    )

            # ----------------------------------------------
            # ASSUMPTIONS
            # ----------------------------------------------

            with st.expander(
                "Scenario Assumptions",
                expanded=False,
            ):

                assumption_df = pd.DataFrame(
                    [
                        {
                            "Assumption": "Pipeline conversion change",
                            "Value": f"{pipeline_conversion_change * 100:.1f}%",
                        },
                        {
                            "Assumption": "Utilization change",
                            "Value": f"{utilization_change * 100:.1f}%",
                        },
                        {
                            "Assumption": "Billing rate change",
                            "Value": f"{billing_rate_change * 100:.1f}%",
                        },
                        {
                            "Assumption": "Project slippage",
                            "Value": f"{slippage_rate * 100:.1f}%",
                        },
                    ]
                )

                st.dataframe(
                    assumption_df,
                    width="stretch",
                    hide_index=True,
                )

        except Exception as exc:

            show_error(
                f"Scenario calculation failed: {exc}"
            )


# ============================================================
# DATA QUALITY
# ============================================================

if data_quality.get(
    "flags"
):

    st.divider()

    section_title(
        "Data Quality",
        (
            "Flags that may affect interpretation "
            "of the financial model."
        ),
    )

    for flag in data_quality.get(
        "flags",
        [],
    ):

        severity = str(
            flag.get(
                "severity",
                "",
            )
        ).upper()

        area = title_case(
            flag.get(
                "area",
                "Data",
            )
        )

        message = flag.get(
            "message",
            "",
        )

        formatted_message = (
            f"**{area}** — {message}"
        )

        if severity == "HIGH":

            st.error(
                formatted_message
            )

        elif severity == "MEDIUM":

            st.warning(
                formatted_message
            )

        else:

            st.info(
                formatted_message
            )


# ============================================================
# CANONICAL SOURCE METRICS
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
            for key, value in source_metrics.items()
        ]
    )

    if source_df.empty:

        st.info(
            "No source metrics available."
        )

    else:

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