from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import DATABASE_URL


# ============================================================
# DATABASE ENGINE
# ============================================================

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=1800,
    connect_args={
        "connect_timeout": 10,
    },
)


# ============================================================
# SESSION
# ============================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# ============================================================
# BASE
# ============================================================

Base = declarative_base()


# ============================================================
# DATABASE DEPENDENCY
# ============================================================

def get_db():
    """
    FastAPI database dependency.

    Opens a SQLAlchemy session for the request
    and guarantees that it is closed afterwards.
    """

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# ============================================================
# CONNECTION TEST
# ============================================================

def test_connection():
    """
    Test database connectivity.

    Returns:
        True  -> database reachable
        False -> connection failed
    """

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        print("Database connection successful")
        return True

    except Exception as exc:
        print(
            f"Database connection failed: {exc}"
        )
        return False


# ============================================================
# LOCAL EXECUTION
# ============================================================

if __name__ == "__main__":
    test_connection()