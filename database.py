import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

import yaml

_config = yaml.safe_load(Path("config.yaml").read_text())
DB_PATH = _config["db"]


@contextmanager
def get_connection() -> Generator[sqlite3.Connection, None, None]:
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> None:
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS competencies (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                import_date   TEXT NOT NULL,
                band          TEXT NOT NULL,
                competency    TEXT NOT NULL,
                sub_competency TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS activities (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                date_added  TEXT NOT NULL,
                start_date  TEXT NOT NULL,
                end_date    TEXT NOT NULL,
                title       TEXT NOT NULL DEFAULT '',
                situation   TEXT NOT NULL,
                task        TEXT NOT NULL,
                action      TEXT NOT NULL,
                result      TEXT NOT NULL,
                reflection  TEXT NOT NULL,
                notes       TEXT NOT NULL DEFAULT ''
            );

            CREATE TABLE IF NOT EXISTS activity_competencies (
                activity_id   INTEGER NOT NULL REFERENCES activities(id),
                competency_id INTEGER NOT NULL REFERENCES competencies(id),
                PRIMARY KEY (activity_id, competency_id)
            );
        """)
        # Migrate existing databases that predate these columns
        for col, definition in [("title", "TEXT NOT NULL DEFAULT ''"), ("notes", "TEXT NOT NULL DEFAULT ''")]:
            try:
                conn.execute(f"ALTER TABLE activities ADD COLUMN {col} {definition}")
            except sqlite3.OperationalError:
                pass  # Column already exists


init_db()
