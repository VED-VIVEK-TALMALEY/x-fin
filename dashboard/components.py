import html

import streamlit as st


def metric_card(
    label,
    value,
    delta=None,
    help_text=None,
):

    st.metric(
        label=label,
        value=value,
        delta=delta,
        help=help_text,
    )


def section_title(title, help_text=None):
    description = help_text or (
        f"{title}: Key dashboard section showing the most relevant "
        "finance and operating metrics for this view."
    )

    st.markdown(
        f"""
        <h2 title="{description}" style="
            margin-top: 2rem;
            margin-bottom: 0.5rem;
            color: #f8fafc;
            letter-spacing: 0.01em;
            font-weight: 700;
        ">
        {title}
        </h2>
        """,
        unsafe_allow_html=True,
    )


def insight_card(category, metric, message, severity="INFO"):
    severity = str(severity or "INFO").upper()
    accent = {
        "HIGH": "#f87171",
        "MEDIUM": "#fbbf24",
        "LOW": "#34d399",
    }.get(severity, "#60a5fa")

    st.markdown(
        f"""
        <article class="decision-card" style="--card-accent: {accent};">
            <div class="card-kicker">{html.escape(severity)} · INSIGHT</div>
            <h3>{html.escape(str(category))}</h3>
            <div class="card-label">{html.escape(str(metric))}</div>
            <p>{html.escape(str(message))}</p>
        </article>
        """,
        unsafe_allow_html=True,
    )


def recommendation_card(category, priority, action, rationale="", impact=None):
    priority = str(priority or "LOW").upper()
    accent = {
        "HIGH": "#f87171",
        "MEDIUM": "#fbbf24",
        "LOW": "#34d399",
    }.get(priority, "#60a5fa")
    impact_text = ""
    if impact is not None:
        impact_text = (
            f'<div class="card-impact">Financial impact: '
            f'{html.escape(format_currency(impact))}</div>'
        )

    rationale_text = ""
    if rationale:
        rationale_text = (
            f'<div class="card-rationale">{html.escape(str(rationale))}</div>'
        )

    st.markdown(
        f"""
        <article class="decision-card" style="--card-accent: {accent};">
            <div class="card-kicker">{html.escape(priority)} · ACTION</div>
            <h3>{html.escape(str(category))}</h3>
            <p class="card-action">{html.escape(str(action))}</p>
            {rationale_text}
            {impact_text}
        </article>
        """,
        unsafe_allow_html=True,
    )

def format_currency(
    value,
    decimals=1,
):

    if value is None:
        return "—"

    value = float(value)

    absolute = abs(value)

    if absolute >= 1_000_000_000:

        return (
            f"₹{value / 1_000_000_000:.{decimals}f}B"
        )

    if absolute >= 1_000_000:

        return (
            f"₹{value / 1_000_000:.{decimals}f}M"
        )

    if absolute >= 1_000:

        return (
            f"₹{value / 1_000:.{decimals}f}K"
        )

    return f"₹{value:,.0f}"


def format_percentage(value):

    if value is None:
        return "—"

    return f"{float(value):.1f}%"


def show_error(message):

    st.error(message)


def show_success(message):

    st.success(message)