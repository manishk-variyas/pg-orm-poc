# base.py
# A reusable parent class for all services.
# Child classes (EmployeeService, LocationService) inherit these helpers
# so they don't have to repeat the same code.

from sqlalchemy import text
from sqlalchemy.orm import Session


class BaseService:
    # Takes a database session when created.
    # The session = your open connection to the database.
    def __init__(self, db: Session):
        self.db = db

    # Fetch one row (or None if no match).
    # sql = your query with :param placeholders.
    # params = dict of values for those placeholders.
    # NEVER put user input directly in sql — always use :param.
    def _fetch_one(self, sql: str, params: dict | None = None) -> dict | None:
        return self.db.execute(text(sql), params or {}).mappings().first()

    # Fetch many rows (always returns a list, even if empty).
    def _fetch_all(self, sql: str, params: dict | None = None) -> list[dict]:
        return self.db.execute(text(sql), params or {}).mappings().all()

    # Run INSERT / UPDATE / DELETE, then save (commit).
    # Returns how many rows were changed.
    def _execute(self, sql: str, params: dict | None = None) -> int:
        result = self.db.execute(text(sql), params or {})
        self.db.commit()
        return result.rowcount
