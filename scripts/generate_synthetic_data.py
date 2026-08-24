import os
from datetime import date, timedelta

import numpy as np
import pandas as pd


np.random.seed(42)

os.makedirs("data", exist_ok=True)

N_PROJECTS = 750

business_units = [
    "X Build",
    "X Design",
    "Digital Ventures",
]

stages = [
    "Prospect",
    "Qualified",
    "In Delivery",
    "Closed Won",
    "Closed Lost",
]

rows = []

for i in range(N_PROJECTS):

    stage = np.random.choice(
        stages,
        p=[0.20, 0.25, 0.25, 0.25, 0.05],
    )

    planned_hours = np.random.randint(
        200,
        5000,
    )

    billing_rate = np.random.choice(
        [150, 200, 250, 300, 350, 400]
    )

    contract_value = (
        planned_hours * billing_rate
    )

    start_date = date.today() - timedelta(
        days=int(np.random.randint(0, 720))
    )

    end_date = start_date + timedelta(
        days=int(np.random.randint(60, 360))
    )

    rows.append({
        "project_name": f"Project {i + 1:04d}",
        "client_name": f"Client {np.random.randint(1, 101):03d}",
        "business_unit": np.random.choice(
            business_units
        ),
        "stage": stage,
        "status": (
            "Completed"
            if stage == "Closed Won"
            else "Active"
        ),
        "start_date": start_date,
        "end_date": end_date,
        "contract_value": round(
            contract_value,
            2,
        ),
        "billing_rate": billing_rate,
        "planned_hours": planned_hours,
    })


projects = pd.DataFrame(rows)

projects.to_csv(
    "data/projects.csv",
    index=False,
)

# ---------------------------
# Pipeline
# ---------------------------

pipeline = []

probabilities = {
    "Prospect": 0.15,
    "Qualified": 0.35,
    "In Delivery": 0.75,
    "Closed Won": 1.00,
    "Closed Lost": 0.00,
}

for _, project in projects.iterrows():

    for month_offset in range(6):

        snapshot = (
            pd.Timestamp.today()
            - pd.DateOffset(
                months=month_offset
            )
        ).date()

        probability = probabilities[
            project["stage"]
        ]

        pipeline.append({
            "project_name": project["project_name"],
            "snapshot_date": snapshot,
            "stage": project["stage"],
            "probability": probability,
            "expected_close_date": project["end_date"],
            "pipeline_value": project[
                "contract_value"
            ],
        })


pipeline = pd.DataFrame(pipeline)

pipeline.to_csv(
    "data/pipeline.csv",
    index=False,
)

# ---------------------------
# Monthly actuals
# ---------------------------

actuals = []

months = pd.date_range(
    end=pd.Timestamp.today().replace(
        day=1
    ),
    periods=24,
    freq="MS",
)

for _, project in projects.iterrows():

    monthly_value = (
        project["contract_value"] / 12
    )

    for month in months:

        if project["stage"] in [
            "Prospect",
            "Qualified",
        ]:
            probability = 0.30
        else:
            probability = 0.85

        revenue = (
            monthly_value
            * probability
            * np.random.uniform(
                0.80,
                1.15,
            )
        )

        hours = (
            project["planned_hours"]
            / 12
            * np.random.uniform(
                0.70,
                1.10,
            )
        )

        cost = (
            revenue
            * np.random.uniform(
                0.55,
                0.75,
            )
        )

        actuals.append({
            "project_name": project[
                "project_name"
            ],
            "month": month.date(),
            "actual_hours": round(
                hours,
                2,
            ),
            "actual_revenue": round(
                revenue,
                2,
            ),
            "actual_cost": round(
                cost,
                2,
            ),
        })


actuals = pd.DataFrame(actuals)

actuals.to_csv(
    "data/actuals.csv",
    index=False,
)

# ---------------------------
# Business-unit budget
# ---------------------------

budgets = []

for business_unit in business_units:

    for month in months:

        revenue_budget = np.random.uniform(
            4_000_000,
            10_000_000,
        )

        budgets.append({
            "business_unit": business_unit,
            "month": month.date(),
            "revenue_budget": round(
                revenue_budget,
                2,
            ),
            "hours_budget": round(
                revenue_budget / 250,
                2,
            ),
            "utilization_budget": round(
                np.random.uniform(
                    0.70,
                    0.82,
                ),
                4,
            ),
        })


budgets = pd.DataFrame(budgets)

budgets.to_csv(
    "data/budgets.csv",
    index=False,
)

print("Synthetic finance dataset generated.")
print(f"Projects: {len(projects):,}")
print(f"Pipeline records: {len(pipeline):,}")
print(f"Actual records: {len(actuals):,}")
print(f"Budget records: {len(budgets):,}")