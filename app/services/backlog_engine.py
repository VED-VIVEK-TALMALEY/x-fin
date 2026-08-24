from sqlalchemy import text


def calculate_backlog(db):

    query = text("""
        SELECT
            COALESCE(
                SUM(
                    CASE
                        WHEN stage IN ('In Delivery', 'Closed Won')
                        THEN pipeline_value
                        ELSE 0
                    END
                ),
                0
            ) AS committed_backlog,

            COALESCE(
                SUM(
                    CASE
                        WHEN stage IN ('Prospect', 'Qualified')
                        THEN pipeline_value
                        ELSE 0
                    END
                ),
                0
            ) AS uncommitted_pipeline

        FROM project_pipeline
        WHERE snapshot_date = (
            SELECT MAX(snapshot_date)
            FROM project_pipeline
        )
    """)

    row = db.execute(query).mappings().first()

    committed = float(row["committed_backlog"])
    uncommitted = float(row["uncommitted_pipeline"])

    return {
        "committed_backlog": round(committed, 2),
        "uncommitted_pipeline": round(uncommitted, 2),
        "total_coverage": round(
            committed + uncommitted,
            2,
        ),
    }


def backlog_waterfall(db):

    query = text("""
        SELECT
            COALESCE(
                SUM(
                    CASE
                        WHEN stage = 'In Delivery'
                        THEN pipeline_value
                        ELSE 0
                    END
                ),
                0
            ) AS opening_backlog,

            COALESCE(
                SUM(
                    CASE
                        WHEN stage = 'Closed Won'
                        THEN pipeline_value
                        ELSE 0
                    END
                ),
                0
            ) AS new_wins

        FROM project_pipeline
        WHERE snapshot_date = (
            SELECT MAX(snapshot_date)
            FROM project_pipeline
        )
    """)

    row = db.execute(query).mappings().first()

    opening = float(row["opening_backlog"])
    wins = float(row["new_wins"])

    # This is deliberately NOT subtracting all historical revenue.
    # We currently do not have a period-specific backlog consumption
    # schedule, so we avoid manufacturing a false closing balance.

    return {
        "opening_backlog": round(opening, 2),
        "new_wins": round(wins, 2),
        "revenue_recognized": None,
        "closing_backlog": round(
            opening + wins,
            2,
        ),
        "methodology": (
            "Snapshot backlog plus current-period wins; "
            "revenue consumption requires period-specific "
            "backlog schedules."
        ),
    }