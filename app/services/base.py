from __future__ import annotations

"""
BaseService — reusable layer for running raw SQL safely.

All services (EmployeeService, LocationService, etc.) will inherit from this
to avoid repeating the same boilerplate in every file.
"""

from sqlalchemy import text
from sqlalchemy.orm import Session


class BaseService:
    """
    Accepts a database session at initialization.
    Provides three helpers that child classes use for all SQL operations.
    """

    def __init__(self, db: Session):
        # The session is the connection to the database.
        # It is passed in by whoever creates the service (e.g. a FastAPI route).
        self.db = db

    def _fetch_one(self, sql: str, params: dict | None = None) -> dict | None:
        """
        Run a SELECT that returns at most one row.
        Returns a dictionary (column_name -> value), or None if no row found.

        sql    — raw SQL with :param placeholders, e.g. "SELECT * FROM users WHERE id = :id"
        params — dictionary of values for those placeholders, e.g. {"id": 1}

        SAFETY: values are sent separately from the SQL, so malicious input
        cannot hijack the query (SQL injection is prevented).
        """
        return self.db.execute(text(sql), params or {}).mappings().first()

    def _fetch_all(self, sql: str, params: dict | None = None) -> list[dict]:
        """
        Run a SELECT that can return many rows.
        Returns a list of dictionaries (empty list if no rows).
        """
        return self.db.execute(text(sql), params or {}).mappings().all()

    def _execute(self, sql: str, params: dict | None = None) -> int:
        """
        Run an INSERT, UPDATE, or DELETE.
        Commits the transaction automatically.
        Returns the number of rows that were changed.
        """
        result = self.db.execute(text(sql), params or {})
        self.db.commit()
        return result.rowcount
