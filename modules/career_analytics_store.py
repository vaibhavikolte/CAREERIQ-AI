
import sqlite3
import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_DIR = BASE_DIR / "database"
DATABASE_PATH = DATABASE_DIR / "career_analytics.db"

DATABASE_DIR.mkdir(parents=True, exist_ok=True)


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_analytics_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS analytics_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT NOT NULL,
            score REAL,
            details TEXT,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_analytics_event(event_type, score=None, details=None):

    if not event_type:
        raise ValueError("Event type is required.")

    if score is not None:
        score = float(score)
        if not 0 <= score <= 100:
            raise ValueError("Score must be between 0 and 100.")

    if details is None:
        details = {}

    connection = get_connection()

    connection.execute("""
        INSERT INTO analytics_history
        (event_type, score, details, created_at)
        VALUES (?, ?, ?, ?)
    """, (
        str(event_type),
        score,
        json.dumps(details, ensure_ascii=False),
        datetime.now().isoformat(timespec="seconds")
    ))

    connection.commit()
    connection.close()


def get_analytics_data():

    initialize_analytics_database()

    connection = get_connection()

    rows = connection.execute("""
        SELECT *
        FROM analytics_history
        ORDER BY created_at ASC
    """).fetchall()

    connection.close()

    records = []

    for row in rows:
        try:
            details = json.loads(row["details"]) if row["details"] else {}
        except (json.JSONDecodeError, TypeError):
            details = {}

        records.append({
            "id": row["id"],
            "event_type": row["event_type"],
            "score": row["score"],
            "details": details,
            "created_at": row["created_at"]
        })

    return records


def get_analytics_by_type(event_type):

    records = get_analytics_data()

    return [
        record for record in records
        if record["event_type"].lower() == event_type.lower()
    ]


def clear_analytics_history():

    connection = get_connection()
    connection.execute("DELETE FROM analytics_history")
    connection.commit()
    connection.close()


initialize_analytics_database()
