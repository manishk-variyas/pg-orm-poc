from __future__ import annotations

from uuid import UUID
from typing import Any
from sqlalchemy import text
from app.services.base import BaseService
from dataclasses import dataclass

_LOCATION_SELECT = """
select id,name,address,latitude,longitude,radius_meters,is_active from locations
"""


@dataclass
class LocationData:
    id: UUID
    name: str | None
    address: str | None
    latitude: float
    longitude: float
    radius_meters: int
    is_active: bool | None

class LocationService(BaseService):
    def get_by_id(self,location_id:UUID) -> LocationData | None:
        row = self._fetch_one(_LOCATION_SELECT + " Where id = :id",{"id":location_id})
        return LocationData(**row) if row else None
    def get_all(self) ->list[LocationData]:
        rows = self._fetch_all(_LOCATION_SELECT+ " ORDER BY name NULLS LAST")
        return [LocationData(**row) for row in rows]