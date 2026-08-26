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