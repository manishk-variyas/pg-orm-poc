# models.py
# Defines what each table looks like in Python.
# Each class = one table. Each attribute = one column.
# SQLAlchemy uses these to create/read/update tables.

from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime, Text, Float, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
import uuid


class Base(DeclarativeBase):
    pass


class EmployeeMaster(Base):
    __tablename__ = "employee_master"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    keycloak_user_id: Mapped[str] = mapped_column(String(255))
    redmine_user_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    user_name: Mapped[str] = mapped_column(String(255))
    user_email: Mapped[str] = mapped_column(String(255))

    designation: Mapped[str | None] = mapped_column(String(255), nullable=True)
    employee_id: Mapped[str | None] = mapped_column(String(100), nullable=True)

    work_location_status: Mapped[str] = mapped_column(String(6))
    work_address: Mapped[str | None] = mapped_column(String(500), nullable=True)
    home_address: Mapped[str | None] = mapped_column(String(500), nullable=True)

    contact_number: Mapped[str | None] = mapped_column(String(50), nullable=True)
    alt_contact_number: Mapped[str | None] = mapped_column(String(50), nullable=True)

    country: Mapped[str | None] = mapped_column(String(10), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Foreign key to locations table
    location_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("locations.id"),
        nullable=True,
    )

    # Relationship lets you do emp.location to get the Location object
    location: Mapped["Location | None"] = relationship(
        back_populates="employees"
    )


class Location(Base):
    __tablename__ = "locations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)

    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)

    radius_meters: Mapped[int] = mapped_column(Integer)

    is_active: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    created_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Back-reference: loc.employees gives all EmployeeMaster rows with this location_id
    employees: Mapped[list["EmployeeMaster"]] = relationship(
        back_populates="location"
    )
