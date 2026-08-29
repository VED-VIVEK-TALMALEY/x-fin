import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


# ============================================================
# CONFIG
# ============================================================

load_dotenv(override=True)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not configured")

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

PROJECTS_FILE = DATA_DIR / "projects.csv"
PIPELINE_FILE = DATA_DIR / "pipeline.csv"
ACTUALS_FILE = DATA_DIR / "actuals.csv"
BUDGETS_FILE = DATA_DIR / "budgets.csv"

BATCH_SIZE = 1000


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={"connect_timeout": 10},
)


# ============================================================
# HELPERS
# ============================================================

def clean_value(value):
    """Convert pandas NaN/NaT values to Python None."""
    if pd.isna(value):
        return None
    return value


def load_csv(path):
    if not path.exists():
        raise FileNotFoundError(f"Missing data file: {path}")

    return pd.read_csv(path)


def execute_batches(conn, statement, records, batch_size=BATCH_SIZE):
    """
    Execute parameterized INSERT statements in batches.

    This avoids thousands of individual network round trips
    when connecting through Supabase's connection pooler.
    """

    total = len(records)

    for start in range(0, total, batch_size):
        batch = records[start:start + batch_size]

        conn.execute(statement, batch)

        end = min(start + batch_size, total)

        print(
            f"    inserted {end:,}/{total:,}",
            flush=True,
        )


# ============================================================
# BUSINESS UNITS
# ============================================================

def load_business_units(conn, projects_df, budgets_df):

    project_units = set(
        projects_df["business_unit"]
        .dropna()
        .astype(str)
        .str.strip()
    )

    budget_units = set(
        budgets_df["business_unit"]
        .dropna()
        .astype(str)
        .str.strip()
    )

    business_units = sorted(project_units | budget_units)

    print(
        f"Business units discovered: {len(business_units)}",
        flush=True,
    )

    statement = text(
        """
        INSERT INTO business_units (name)
        VALUES (:name)
        ON CONFLICT (name) DO NOTHING
        """
    )

    records = [
        {"name": name}
        for name in business_units
    ]

    execute_batches(conn, statement, records)

    rows = conn.execute(
        text(
            """
            SELECT business_unit_id, name
            FROM business_units
            """
        )
    ).mappings().all()

    return {
        row["name"]: row["business_unit_id"]
        for row in rows
    }


# ============================================================
# PROJECTS
# ============================================================

def load_projects(conn, projects_df, business_unit_map):

    projects_df = projects_df.drop_duplicates(
        subset=["project_name"],
        keep="first",
    )

    print(
        f"Projects to load: {len(projects_df)}",
        flush=True,
    )

    records = []

    for _, row in projects_df.iterrows():

        project_name = str(
            row["project_name"]
        ).strip()

        business_unit = str(
            row["business_unit"]
        ).strip()

        business_unit_id = business_unit_map.get(
            business_unit
        )

        if business_unit_id is None:
            raise ValueError(
                f"Business unit not found for project "
                f"{project_name}: {business_unit}"
            )

        records.append(
            {
                "project_name": clean_value(
                    row["project_name"]
                ),
                "client_name": clean_value(
                    row["client_name"]
                ),
                "business_unit_id": business_unit_id,
                "stage": clean_value(
                    row["stage"]
                ),
                "status": clean_value(
                    row["status"]
                ) or "Active",
                "start_date": clean_value(
                    row["start_date"]
                ),
                "end_date": clean_value(
                    row["end_date"]
                ),
                "contract_value": clean_value(
                    row["contract_value"]
                ),
                "billing_rate": clean_value(
                    row["billing_rate"]
                ),
                "planned_hours": clean_value(
                    row["planned_hours"]
                ),
            }
        )

    statement = text(
        """
        INSERT INTO projects (
            project_name,
            client_name,
            business_unit_id,
            stage,
            status,
            start_date,
            end_date,
            contract_value,
            billing_rate,
            planned_hours
        )
        VALUES (
            :project_name,
            :client_name,
            :business_unit_id,
            :stage,
            :status,
            :start_date,
            :end_date,
            :contract_value,
            :billing_rate,
            :planned_hours
        )
        """
    )

    execute_batches(conn, statement, records)

    rows = conn.execute(
        text(
            """
            SELECT project_id, project_name
            FROM projects
            """
        )
    ).mappings().all()

    return {
        row["project_name"]: row["project_id"]
        for row in rows
    }


# ============================================================
# PIPELINE
# ============================================================

def load_pipeline(conn, pipeline_df, project_map):

    print(
        f"Pipeline records to load: {len(pipeline_df)}",
        flush=True,
    )

    records = []

    for _, row in pipeline_df.iterrows():

        project_name = str(
            row["project_name"]
        ).strip()

        project_id = project_map.get(
            project_name
        )

        if project_id is None:
            raise ValueError(
                f"Pipeline references unknown project: "
                f"{project_name}"
            )

        records.append(
            {
                "project_id": project_id,
                "snapshot_date": clean_value(
                    row["snapshot_date"]
                ),
                "stage": clean_value(
                    row["stage"]
                ),
                "probability": clean_value(
                    row["probability"]
                ),
                "expected_close_date": clean_value(
                    row["expected_close_date"]
                ),
                "pipeline_value": clean_value(
                    row["pipeline_value"]
                ),
            }
        )

    statement = text(
        """
        INSERT INTO project_pipeline (
            project_id,
            snapshot_date,
            stage,
            probability,
            expected_close_date,
            pipeline_value
        )
        VALUES (
            :project_id,
            :snapshot_date,
            :stage,
            :probability,
            :expected_close_date,
            :pipeline_value
        )
        """
    )

    execute_batches(conn, statement, records)


# ============================================================
# ACTUALS
# ============================================================

def load_actuals(conn, actuals_df, project_map):

    print(
        f"Actual records to load: {len(actuals_df)}",
        flush=True,
    )

    records = []

    for _, row in actuals_df.iterrows():

        project_name = str(
            row["project_name"]
        ).strip()

        project_id = project_map.get(
            project_name
        )

        if project_id is None:
            raise ValueError(
                f"Actuals reference unknown project: "
                f"{project_name}"
            )

        records.append(
            {
                "project_id": project_id,
                "month": clean_value(
                    row["month"]
                ),
                "actual_hours": clean_value(
                    row["actual_hours"]
                ),
                "actual_revenue": clean_value(
                    row["actual_revenue"]
                ),
                "actual_cost": clean_value(
                    row["actual_cost"]
                ),
            }
        )

    statement = text(
        """
        INSERT INTO project_actuals (
            project_id,
            month,
            actual_hours,
            actual_revenue,
            actual_cost
        )
        VALUES (
            :project_id,
            :month,
            :actual_hours,
            :actual_revenue,
            :actual_cost
        )
        ON CONFLICT (project_id, month) DO UPDATE
        SET
            actual_hours = EXCLUDED.actual_hours,
            actual_revenue = EXCLUDED.actual_revenue,
            actual_cost = EXCLUDED.actual_cost
        """
    )

    execute_batches(conn, statement, records)


# ============================================================
# BUDGETS
# ============================================================

def load_budgets(conn, budgets_df, business_unit_map):

    print(
        f"Budget records to load: {len(budgets_df)}",
        flush=True,
    )

    records = []

    for _, row in budgets_df.iterrows():

        business_unit = str(
            row["business_unit"]
        ).strip()

        business_unit_id = business_unit_map.get(
            business_unit
        )

        if business_unit_id is None:
            raise ValueError(
                f"Budget references unknown business unit: "
                f"{business_unit}"
            )

        records.append(
            {
                "business_unit_id": business_unit_id,
                "month": clean_value(
                    row["month"]
                ),
                "revenue_budget": clean_value(
                    row["revenue_budget"]
                ),
                "hours_budget": clean_value(
                    row["hours_budget"]
                ),
                "utilization_budget": clean_value(
                    row["utilization_budget"]
                ),
            }
        )

    statement = text(
        """
        INSERT INTO budgets (
            business_unit_id,
            month,
            revenue_budget,
            hours_budget,
            utilization_budget
        )
        VALUES (
            :business_unit_id,
            :month,
            :revenue_budget,
            :hours_budget,
            :utilization_budget
        )
        ON CONFLICT (business_unit_id, month) DO UPDATE
        SET
            revenue_budget = EXCLUDED.revenue_budget,
            hours_budget = EXCLUDED.hours_budget,
            utilization_budget = EXCLUDED.utilization_budget
        """
    )

    execute_batches(conn, statement, records)


# ============================================================
# VALIDATION
# ============================================================

def validate_counts(conn):

    tables = [
        "business_units",
        "projects",
        "project_pipeline",
        "project_actuals",
        "budgets",
        "forecast_versions",
        "forecast_values",
    ]

    print()
    print("DATABASE COUNTS")
    print("=" * 50)

    for table in tables:

        count = conn.execute(
            text(
                f"SELECT COUNT(*) FROM {table}"
            )
        ).scalar()

        print(
            f"{table:25} {count:,}",
            flush=True,
        )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("X-FIN DATA LOADER")
    print("=" * 60)

    print(
        f"Data directory: {DATA_DIR}",
        flush=True,
    )

    print()

    # --------------------------------------------------------
    # LOAD CSV FILES
    # --------------------------------------------------------

    projects_df = load_csv(
        PROJECTS_FILE
    )

    pipeline_df = load_csv(
        PIPELINE_FILE
    )

    actuals_df = load_csv(
        ACTUALS_FILE
    )

    budgets_df = load_csv(
        BUDGETS_FILE
    )

    print(
        f"projects.csv:  {len(projects_df):,} rows"
    )

    print(
        f"pipeline.csv:  {len(pipeline_df):,} rows"
    )

    print(
        f"actuals.csv:   {len(actuals_df):,} rows"
    )

    print(
        f"budgets.csv:   {len(budgets_df):,} rows"
    )

    print()

    # --------------------------------------------------------
    # SINGLE TRANSACTION
    # --------------------------------------------------------

    with engine.begin() as conn:

        print(
            "Loading business units...",
            flush=True,
        )

        business_unit_map = load_business_units(
            conn,
            projects_df,
            budgets_df,
        )

        print(
            "Loading projects...",
            flush=True,
        )

        project_map = load_projects(
            conn,
            projects_df,
            business_unit_map,
        )

        print(
            "Loading pipeline...",
            flush=True,
        )

        load_pipeline(
            conn,
            pipeline_df,
            project_map,
        )

        print(
            "Loading actuals...",
            flush=True,
        )

        load_actuals(
            conn,
            actuals_df,
            project_map,
        )

        print(
            "Loading budgets...",
            flush=True,
        )

        load_budgets(
            conn,
            budgets_df,
            business_unit_map,
        )

        print()
        print(
            "Validating...",
            flush=True,
        )

        validate_counts(conn)

    print()
    print("=" * 60)
    print("X-FIN DATA LOAD COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()