import streamlit as st
import pandas as pd
import plotly.graph_objects as go


st.set_page_config(
    page_title="X-Fin",
    page_icon="📊",
    layout="wide",
)

st.title("X-Fin")
st.caption("Intelligent Delivery Finance Operating System")

st.divider()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Revenue Forecast",
    "₹42.7M",
    "-5.1%",
)

col2.metric(
    "Budget",
    "₹45.0M",
)

col3.metric(
    "Backlog",
    "₹28.4M",
    "+4.2%",
)

col4.metric(
    "Pipeline",
    "₹63.7M",
    "+8.7%",
)

st.divider()

left, right = st.columns(2)

with left:

    st.subheader("Revenue Outlook")

    df = pd.DataFrame({
        "Month": [
            "Jul", "Aug", "Sep", "Oct",
            "Nov", "Dec"
        ],
        "Actual": [
            6.8, 7.2, 7.5, None, None, None
        ],
        "Budget": [
            7.0, 7.4, 7.6, 7.8, 7.9, 8.1
        ],
        "Forecast": [
            6.8, 7.2, 7.5, 7.4, 7.3, 7.6
        ],
    })

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["Month"],
            y=df["Budget"],
            name="Budget",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["Month"],
            y=df["Forecast"],
            name="Forecast",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["Month"],
            y=df["Actual"],
            name="Actual",
        )
    )

    fig.update_layout(
        yaxis_title="Revenue (₹M)",
        hovermode="x unified",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


with right:

    st.subheader("Forecast Drivers")

    drivers = pd.DataFrame({
        "Driver": [
            "Project Slippage",
            "Pipeline Conversion",
            "Utilization",
            "Billing Rate",
        ],
        "Impact (₹M)": [
            -1.8,
            -0.9,
            -0.4,
            0.3,
        ],
    })

    fig = go.Figure(
        go.Bar(
            x=drivers["Impact (₹M)"],
            y=drivers["Driver"],
            orientation="h",
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

st.divider()

st.subheader("Management Signals")

signals = pd.DataFrame({
    "Area": [
        "Revenue",
        "Pipeline",
        "Utilization",
        "Backlog",
    ],
    "Status": [
        "Below Plan",
        "Watch",
        "Stable",
        "Healthy",
    ],
    "Comment": [
        "Forecast 5.1% below budget",
        "Conversion declining",
        "Within target range",
        "Strong coverage for next quarter",
    ],
})

st.dataframe(
    signals,
    use_container_width=True,
    hide_index=True,
)