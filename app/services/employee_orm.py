from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.models import EmployeeMaster, Location


class EmployeeORMService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, employee_id: UUID) -> dict | None:
        emp = self.db.query(EmployeeMaster).filter(EmployeeMaster.id==employee_id).first()
        if emp is None:
            return None
        
        return {
            "id": emp.id,
            "keycloak_user_id":emp.keycloak_user_id,
            "user_name":emp.user_name,
            "user_email":emp.user_email,
            "designation":emp.designation,
            "employee_id":emp.employee_id,
            "work_location_status":emp.work_location_status,
            "contact_number":emp.contact_number,
            "country":emp.country,
            "created_at":emp.created_at,
            "location_id":emp.location_id,
            "location_name": emp.location.name if emp.location else None
        }

    def get_all(self) -> list[dict]:
        emps = self.db.query(EmployeeMaster).order_by(EmployeeMaster.user_name).all()
        return [
            {
                "id": emp.id,
                "keycloak_user_id": emp.keycloak_user_id,
                "user_name": emp.user_name,
                "user_email": emp.user_email,
                "designation": emp.designation,
                "employee_id": emp.employee_id,
                "work_location_status": emp.work_location_status,
                "work_address": emp.work_address,
                "home_address": emp.home_address,
                "contact_number": emp.contact_number,
                "country": emp.country,
                "created_at": emp.created_at,
                "location_id": emp.location_id,
                "location_name": emp.location.name if emp.location else None,
            }
            for emp in emps
        ]