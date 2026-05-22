"""Database access layer for the car rental system."""

import sqlite3
from pathlib import Path


class DatabaseManager:
    """Simple wrapper around a SQLite connection."""

    def __init__(self, db_path: Path) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row

    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        return cursor

    def executescript(self, script: str) -> None:
        self.connection.executescript(script)
        self.connection.commit()

    def close(self) -> None:
        self.connection.close()
