import requests


BASE_URL = "http://127.0.0.1:8000"


def get(
    endpoint: str,
):
    response = requests.get(
        f"{BASE_URL}{endpoint}",
        timeout=10,
    )

    response.raise_for_status()

    return response.json()


def post(
    endpoint: str,
    payload: dict,
):
    response = requests.post(
        f"{BASE_URL}{endpoint}",
        json=payload,
        timeout=10,
    )

    response.raise_for_status()

    return response.json()


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


def run_scenario(
    payload: dict,
):
    return post(
        "/scenarios/run",
        payload,
    )