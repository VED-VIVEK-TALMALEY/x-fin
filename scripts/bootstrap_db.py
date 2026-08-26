"""Bootstrap the Render PostgreSQL database on first startup.

This script is intentionally idempotent:
- creates the schema only when the database is empty/uninitialized
- loads the bundled synthetic dataset only once
- does not drop or reload production data on subsequent deploys/restarts
"""

from pathlib import Path

from sqlalchemy import create_engine, inspect, text
from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "app" / "db" / "schema.sql"

load_dotenv(ROOT / ".env")

import os

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not configured")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={"connect_timeout": 10},
)


REQUIRED_TABLES = {
    "business_units",
    "projects",
    "project_pipeline",
    "project_actuals",
    "budgets",
    "forecast_versions",
    "forecast_values",
}


def _database_initialized() -> bool:
    tables = set(inspect(engine).get_table_names())
    return REQUIRED_TABLES.issubset(tables)


def _has_data() -> bool:
    if not _database_initialized():
        return False

    with engine.connect() as conn:
        count = conn.execute(
            text("SELECT COUNT(*) FROM business_units")
        ).scalar_one()

    return int(count) > 0


def _create_schema() -> None:
    sql = SCHEMA_PATH.read_text(encoding="utf-8-sig")

    # The development schema contains DROP TABLE statements so that a
    # developer can reset a local database. Never execute those on Render.
    statements = []
    for statement in sql.split(";"):
        statement = statement.strip()
        if not statement:
            continue
        if statement.upper().startswith("DROP TABLE"):
            continue
        statements.append(statement)

    with engine.begin() as conn:
        for statement in statements:
            conn.execute(text(statement))


def main() -> None:
    if not _database_initialized():
        print("X-Fin database schema not found. Creating schema...")
        _create_schema()
    else:
        print("X-Fin database schema already exists.")

    if not _has_data():
        print("X-Fin database is empty. Loading bundled synthetic data...")
        from scripts.load_data import load

        load()
        print("X-Fin data load completed.")
    else:
        print("X-Fin database already contains data. Skipping data load.")

    print("X-Fin database bootstrap complete.")


if __name__ == "__main__":
    main()
