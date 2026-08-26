import os

from dotenv import load_dotenv


load_dotenv()


def get_database_url() -> str:
    """
    Read and normalize the database URL for SQLAlchemy.

    Render may provide:
        postgres://...
    or:
        postgresql://...

    SQLAlchemy with psycopg2 uses:
        postgresql+psycopg2://...
    """

    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError(
            "DATABASE_URL is not configured. "
            "Set DATABASE_URL in the environment."
        )

    if database_url.startswith("postgres://"):
        database_url = database_url.replace(
            "postgres://",
            "postgresql+psycopg2://",
            1,
        )

    elif database_url.startswith("postgresql://"):
        database_url = database_url.replace(
            "postgresql://",
            "postgresql+psycopg2://",
            1,
        )

    return database_url


DATABASE_URL = get_database_url()

ENVIRONMENT = os.getenv(
    "ENVIRONMENT",
    "development",
)

APP_NAME = os.getenv(
    "APP_NAME",
    "X-Fin Finance API",
)

APP_VERSION = os.getenv(
    "APP_VERSION",
    "1.0.0",
)