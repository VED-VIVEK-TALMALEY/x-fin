"""
X-Fin Dashboard API Client
"""

from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests
import streamlit as st


def _get_secret(name: str) -> Optional[str]:
    try:
        value = st.secrets.get(name)
        if value:
            return str(value)
    except Exception:
        pass

    return os.getenv(name)


BASE_URL = _get_secret(
    "API_BASE_URL"
)

if not BASE_URL:
    raise RuntimeError(
        "API_BASE_URL is not configured. "
        "Set it in Streamlit Cloud Secrets or the environment."
    )

BASE_URL = BASE_URL.rstrip("/")


SESSION = requests.Session()

SESSION.headers.update(
    {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
)


class APIError(RuntimeError):
    """Raised when the X-Fin API cannot be reached successfully."""


def _request(
    method: str,
    endpoint: str,
    payload: Optional[Dict[str, Any]] = None,
) -> Any:
    url = f"{BASE_URL}/{endpoint.lstrip('/')}"

    try:
        response = SESSION.request(
            method=method.upper(),
            url=url,
            json=payload,
            timeout=30,
        )
    except requests.RequestException as exc:
        raise APIError(
            f"Unable to connect to X-Fin API: {exc}"
        ) from exc

    if not response.ok:
        try:
            detail = response.json()
        except ValueError:
            detail = response.text

        raise APIError(
            f"X-Fin API returned HTTP "
            f"{response.status_code}: {detail}"
        )

    try:
        return response.json()
    except ValueError as exc:
        raise APIError(
            "X-Fin API returned a non-JSON response."
        ) from exc


def get(endpoint: str) -> Any:
    return _request(
        "GET",
        endpoint,
    )


def post(
    endpoint: str,
    payload: Dict[str, Any],
) -> Any:
    return _request(
        "POST",
        endpoint,
        payload,
    )


def get_summary():
    return get(
        "/analytics/summary"
    )


def get_monthly_revenue():
    return get(
        "/analytics/monthly-revenue"
    )


def get_backlog():
    return get(
        "/analytics/backlog"
    )


def get_variance():
    return get(
        "/analytics/variance"
    )


def get_forecast():
    return get(
        "/forecast/current"
    )


def get_forecast_accuracy():
    return get(
        "/analytics/forecast-accuracy"
    )


def get_business_units():
    return get(
        "/analytics/business-units"
    )


def get_intelligence():
    return get(
        "/intelligence/overview"
    )


def get_executive_briefing():
    return get(
        "/executive/briefing"
    )


def run_scenario(
    payload: Dict[str, Any],
):
    return post(
        "/scenarios/run",
        payload,
    )