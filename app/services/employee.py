from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from typing import Any

from app.services.base import BaseService


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
        row = self._fetch_one(
            _EMPLOYEE_SELECT + " WHERE e.id = :id",
            {"id": employee_id},
        )
        return EmployeeData(**row) if row else None

    def get_all(self) -> list[EmployeeData]:
        rows = self._fetch_all(_EMPLOYEE_SELECT + " ORDER BY e.user_name")
        return [EmployeeData(**row) for row in rows]

   