import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL"
)

engine = create_engine(
    DATABASE_URL
)


def load():

    projects = pd.read_csv(
        "data/projects.csv"
    )

    pipeline = pd.read_csv(
        "data/pipeline.csv"
    )

    actuals = pd.read_csv(
        "data/actuals.csv"
    )

    budgets = pd.read_csv(
        "data/budgets.csv"
    )

    # Business units
    business_units = pd.DataFrame({
        "name": projects[
            "business_unit"
        ].unique()
    })

    business_units.to_sql(
        "business_units",
        engine,
        if_exists="append",
        index=False,
    )

    units = pd.read_sql(
        "SELECT business_unit_id, name FROM business_units",
        engine,
    )

    projects = projects.merge(
        units,
        left_on="business_unit",
        right_on="name",
    )

    project_columns = [
        "project_name",
        "client_name",
        "business_unit_id",
        "stage",
        "status",
        "start_date",
        "end_date",
        "contract_value",
        "billing_rate",
        "planned_hours",
    ]

    projects[
        project_columns
    ].to_sql(
        "projects",
        engine,
        if_exists="append",
        index=False,
    )

    db_projects = pd.read_sql(
        """
        SELECT
            project_id,
            project_name
        FROM projects
        """,
        engine,
    )

    pipeline = pipeline.merge(
        db_projects,
        on="project_name",
    )

    pipeline_columns = [
        "project_id",
        "snapshot_date",
        "stage",
        "probability",
        "expected_close_date",
        "pipeline_value",
    ]

    pipeline[
        pipeline_columns
    ].to_sql(
        "project_pipeline",
        engine,
        if_exists="append",
        index=False,
    )

    actuals = actuals.merge(
        db_projects,
        on="project_name",
    )

    actual_columns = [
        "project_id",
        "month",
        "actual_hours",
        "actual_revenue",
        "actual_cost",
    ]

    actuals[
        actual_columns
    ].to_sql(
        "project_actuals",
        engine,
        if_exists="append",
        index=False,
    )

    budgets = budgets.merge(
        units,
        left_on="business_unit",
        right_on="name",
    )

    budget_columns = [
        "business_unit_id",
        "month",
        "revenue_budget",
        "hours_budget",
        "utilization_budget",
    ]

    budgets[
        budget_columns
    ].to_sql(
        "budgets",
        engine,
        if_exists="append",
        index=False,
    )

    with engine.connect() as conn:

        for table in [
            "business_units",
            "projects",
            "project_pipeline",
            "project_actuals",
            "budgets",
        ]:

            result = conn.execute(
                text(
                    f"SELECT COUNT(*) FROM {table}"
                )
            )

            print(
                f"{table}: {result.scalar():,}"
            )


if __name__ == "__main__":
    load()