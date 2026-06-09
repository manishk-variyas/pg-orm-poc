from __future__ import annotations

from uuid import UUID
from sqlalchemy.orm import Session
from app.models import Location


class LocationORMService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, location_id: UUID) -> dict | None:
        loc = self.db.query(Location).filter(
            Location.id == location_id
        ).first()
        if loc is None:
            return None
        return {
            "id": loc.id,
            "name": loc.name,
            "address": loc.address,
            "latitude": loc.latitude,
            "longitude": loc.longitude,
            "radius_meters": loc.radius_meters,
            "is_active": loc.is_active,
        }

    def get_all(self) -> list[dict]:
        locs = self.db.query(Location).order_by(Location.name).all()
        return [
            {
                "id": loc.id,
                "name": loc.name,
                "address": loc.address,
                "latitude": loc.latitude,
                "longitude": loc.longitude,
                "radius_meters": loc.radius_meters,
                "is_active": loc.is_active,
            }
            for loc in locs
        ]
