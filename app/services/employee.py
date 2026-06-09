# employee.py
# Service for the employee_master table.
# Shows how to use BaseService helpers to run raw SQL safely.

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from typing import Any

from app.services.base import BaseService


# The SELECT part that all employee queries share.
# We reuse this to avoid writing the same 15 columns in every method.
_EMPLOYEE_SELECT = """
    SELECT
        e.id, e.keycloak_user_id, e.user_name, e.user_email,
        e.designation, e.employee_id, e.work_location_status,
        e.work_address, e.home_address, e.contact_number, e.country,
        e.created_at, e.location_id,
        l.name AS location_name
    FROM employee_master e
    LEFT JOIN locations l ON l.id = e.location_id
"""


# A simple container for one employee row.
# _fetch_one returns a dict; EmployeeData(**dict) converts it to this object.
@dataclass
class EmployeeData:
    id: UUID
    keycloak_user_id: str
    user_name: str
    user_email: str
    designation: str | None
    employee_id: str | None
    work_location_status: str
    work_address: str | None
    home_address: str | None
    contact_number: str | None
    country: str | None
    created_at: datetime
    location_id: UUID | None
    location_name: str | None


class EmployeeService(BaseService):

    def get_by_id(self, employee_id: UUID) -> EmployeeData | None:
        # :id is a placeholder; {"id": employee_id} fills it safely
        row = self._fetch_one(
            _EMPLOYEE_SELECT + " WHERE e.id = :id",
            {"id": employee_id},
        )
        return EmployeeData(**row) if row else None

    def get_all(self) -> list[EmployeeData]:
        rows = self._fetch_all(
            _EMPLOYEE_SELECT + " ORDER BY e.user_name"
        )
        return [EmployeeData(**row) for row in rows]

    def search_by_name(self, query: str) -> list[EmployeeData]:
        # ILIKE = case-insensitive search
        # f"%{query}%" is safe because query is still sent as a bound parameter
        rows = self._fetch_all(
            _EMPLOYEE_SELECT + " WHERE e.user_name ILIKE :pattern",
            {"pattern": f"%{query}%"},
        )
        return [EmployeeData(**row) for row in rows]

    def get_by_location(self, location_id: UUID) -> list[EmployeeData]:
        rows = self._fetch_all(
            _EMPLOYEE_SELECT + " WHERE e.location_id = :loc_id",
            {"loc_id": location_id},
        )
        return [EmployeeData(**row) for row in rows]

    def create(self, data: dict[str, Any]) -> UUID:
        # INSERT ... RETURNING id gives back the new row's ID
        row = self.db.execute(
            text("""
                INSERT INTO employee_master
                    (keycloak_user_id, user_name, user_email, designation,
                     employee_id, work_location_status, work_address,
                     home_address, contact_number, country, location_id)
                VALUES
                    (:keycloak_user_id, :user_name, :user_email, :designation,
                     :employee_id, :work_location_status, :work_address,
                     :home_address, :contact_number, :country, :location_id)
                RETURNING id
            """),
            data,
        ).mappings().one()

        self.db.commit()
        return row["id"]
