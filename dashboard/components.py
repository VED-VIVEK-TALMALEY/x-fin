import streamlit as st


def metric_card(
    label,
    value,
    delta=None,
):

    st.metric(
        label=label,
        value=value,
        delta=delta,
    )


def section_title(title):

    st.markdown(
        f"""
        <h2 style="
            margin-top: 1.5rem;
            margin-bottom: 0.5rem;
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