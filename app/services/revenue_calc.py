from decimal import Decimal


STAGE_PROBABILITY = {
    "Prospect": Decimal("0.15"),
    "Qualified": Decimal("0.35"),
    "In Delivery": Decimal("0.75"),
    "Closed Won": Decimal("1.00"),
    "Closed Lost": Decimal("0.00"),
}


def probability_for_stage(stage: str) -> Decimal:
    return STAGE_PROBABILITY.get(stage, Decimal("0.00"))


def calculate_project_value(
    planned_hours: Decimal,
    billing_rate: Decimal,
) -> Decimal:
    return (
        planned_hours * billing_rate
    ).quantize(Decimal("0.01"))


def probability_weighted_value(
    project_value: Decimal,
    stage: str,
    probability: Decimal | None = None,
) -> Decimal:

    effective_probability = (
        probability
        if probability is not None
        else probability_for_stage(stage)
    )

    return (
        project_value * effective_probability
    ).quantize(Decimal("0.01"))


def monthly_revenue(
    contract_value: Decimal,
    months: int,
) -> Decimal:

    if months <= 0:
        raise ValueError("months must be greater than zero")

    return (
        contract_value / Decimal(months)
    ).quantize(Decimal("0.01"))