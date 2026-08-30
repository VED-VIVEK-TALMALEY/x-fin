from __future__ import annotations

from typing import Dict


def build_revenue_waterfall(
    base_revenue: float,
    committed_backlog: float,
    weighted_pipeline: float,
    slippage: float = 0.0,
    risk_adjustment: float = 0.0,
) -> Dict:
    base_revenue = float(base_revenue or 0)
    committed_backlog = float(committed_backlog or 0)
    weighted_pipeline = float(weighted_pipeline or 0)
    slippage = float(slippage or 0)
    risk_adjustment = float(risk_adjustment or 0)

    gross_forecast = (
        base_revenue
        + committed_backlog
        + weighted_pipeline
    )

    net_forecast = (
        gross_forecast
        - slippage
        - risk_adjustment
    )

    return {
        "base_revenue": round(base_revenue, 2),
        "committed_backlog": round(committed_backlog, 2),
        "weighted_pipeline": round(weighted_pipeline, 2),
        "gross_forecast": round(gross_forecast, 2),
        "slippage": round(slippage, 2),
        "risk_adjustment": round(risk_adjustment, 2),
        "net_forecast": round(max(net_forecast, 0), 2),
    }