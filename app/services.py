from dataclasses import dataclass, asdict
from datetime import datetime
from uuid import UUID
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session


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


@dataclass
class LocationData:
    id: UUID
    name: str | None
    address: str | None
    latitude: float
    longitude: float
    radius_meters: int
    is_active: bool | None


class EmployeeService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, employee_id: UUID) -> EmployeeData | None:
        row = self.db.execute(
            text("""
                SELECT
                    e.id, e.keycloak_user_id, e.user_name, e.user_email,
                    e.designation, e.employee_id, e.work_location_status,
                    e.work_address, e.home_address, e.contact_number, e.country,
                    e.created_at, e.location_id,
                    l.name AS location_name
                FROM employee_master e
                LEFT JOIN locations l ON l.id = e.location_id
                WHERE e.id = :id
            """),
            {"id": employee_id},
        ).mappings().first()

        return EmployeeData(**row) if row else None

    def get_by_email(self, email: str) -> list[EmployeeData]:
        rows = self.db.execute(
            text("""
                SELECT
                    e.id, e.keycloak_user_id, e.user_name, e.user_email,
                    e.designation, e.employee_id, e.work_location_status,
                    e.work_address, e.home_address, e.contact_number, e.country,
                    e.created_at, e.location_id,
                    l.name AS location_name
                FROM employee_master e
                LEFT JOIN locations l ON l.id = e.location_id
                WHERE e.user_email = :email
            """),
            {"email": email},
        ).mappings().all()

        return [EmployeeData(**row) for row in rows]

    def get_by_location(self, location_id: UUID) -> list[EmployeeData]:
        rows = self.db.execute(
            text("""
                SELECT
                    e.id, e.keycloak_user_id, e.user_name, e.user_email,
                    e.designation, e.employee_id, e.work_location_status,
                    e.work_address, e.home_address, e.contact_number, e.country,
                    e.created_at, e.location_id,
                    l.name AS location_name
                FROM employee_master e
                LEFT JOIN locations l ON l.id = e.location_id
                WHERE e.location_id = :loc_id
            """),
            {"loc_id": location_id},
        ).mappings().all()

        return [EmployeeData(**row) for row in rows]

    def search_by_name(self, query: str) -> list[EmployeeData]:
        rows = self.db.execute(
            text("""
                SELECT
                    e.id, e.keycloak_user_id, e.user_name, e.user_email,
                    e.designation, e.employee_id, e.work_location_status,
                    e.work_address, e.home_address, e.contact_number, e.country,
                    e.created_at, e.location_id,
                    l.name AS location_name
                FROM employee_master e
                LEFT JOIN locations l ON l.id = e.location_id
                WHERE e.user_name ILIKE :pattern
            """),
            {"pattern": f"%{query}%"},
        ).mappings().all()

        return [EmployeeData(**row) for row in rows]

    def create(self, data: dict[str, Any]) -> UUID:
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


class LocationService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, location_id: UUID) -> LocationData | None:
        row = self.db.execute(
            text("""
                SELECT id, name, address, latitude, longitude,
                       radius_meters, is_active
                FROM locations
                WHERE id = :id
            """),
            {"id": location_id},
        ).mappings().first()

        return LocationData(**row) if row else None

    def get_active(self) -> list[LocationData]:
        rows = self.db.execute(
            text("""
                SELECT id, name, address, latitude, longitude,
                       radius_meters, is_active
                FROM locations
                WHERE is_active = true
            """),
        ).mappings().all()

        return [LocationData(**row) for row in rows]

    def get_nearby(
        self, lat: float, lng: float, radius_meters: int
    ) -> list[LocationData]:
        rows = self.db.execute(
            text("""
                SELECT id, name, address, latitude, longitude,
                       radius_meters, is_active
                FROM locations
                WHERE is_active = true
                  AND earth_distance(
                      ll_to_earth(:lat, :lng),
                      ll_to_earth(latitude, longitude)
                  ) <= :radius
            """),
            {"lat": lat, "lng": lng, "radius": radius_meters},
        ).mappings().all()

        return [LocationData(**row) for row in rows]

    def create(self, data: dict[str, Any]) -> UUID:
        row = self.db.execute(
            text("""
                INSERT INTO locations
                    (name, address, latitude, longitude, radius_meters, is_active)
                VALUES
                    (:name, :address, :latitude, :longitude, :radius_meters, :is_active)
                RETURNING id
            """),
            data,
        ).mappings().one()

        self.db.commit()
        return row["id"]

    def update_coordinates(
        self, location_id: UUID, lat: float, lng: float
    ) -> bool:
        result = self.db.execute(
            text("""
                UPDATE locations
                SET latitude = :lat, longitude = :lng
                WHERE id = :id
            """),
            {"id": location_id, "lat": lat, "lng": lng},
        )
        self.db.commit()
        return result.rowcount > 0
