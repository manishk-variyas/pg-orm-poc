# main.py
# FastAPI app entry point.
# Each function = one API endpoint.
# use_orm=true on the URL switches to ORM version for benchmarking.

from uuid import UUID
import time

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.employee import EmployeeService
from app.services.employee_orm import EmployeeORMService
from app.services.location import LocationService
from app.services.location_orm import LocationORMService


# Helper: show time nicely
def _fmt(elapsed: float) -> str:
    if elapsed >= 1:
        return f"{elapsed:.2f}s"
    return f"{round(elapsed * 1000, 1)}ms"


app = FastAPI()


@app.get("/")
def root():
    return {"message": "ok"}


@app.get("/employees")
def list_employees(
    db: Session = Depends(get_db),
    use_orm: bool = False,
):
    # Pick which service to use based on the ?use_orm= flag
    svc = EmployeeORMService(db) if use_orm else EmployeeService(db)
    start = time.perf_counter()
    emps = svc.get_all()
    elapsed = time.perf_counter() - start
    return {
        "data": emps,
        "execution_time": _fmt(elapsed),
        "method": "orm" if use_orm else "raw",
    }


@app.get("/employees/{employee_id}")
def get_employee(
    employee_id: UUID,
    db: Session = Depends(get_db),
    use_orm: bool = False,
):
    svc = EmployeeORMService(db) if use_orm else EmployeeService(db)
    start = time.perf_counter()
    emp = svc.get_by_id(employee_id)
    elapsed = time.perf_counter() - start
    if emp is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {
        "data": emp,
        "execution_time": _fmt(elapsed),
        "method": "orm" if use_orm else "raw",
    }


@app.get("/locations")
def get_locations(
    db: Session = Depends(get_db),
    use_orm: bool = False,
):
    svc = LocationORMService(db) if use_orm else LocationService(db)
    start = time.perf_counter()
    locs = svc.get_all()
    elapsed = time.perf_counter() - start
    return {
        "data": locs,
        "execution_time": _fmt(elapsed),
        "method": "orm" if use_orm else "raw",
    }


@app.get("/locations/{location_id}")
def get_location(
    location_id: UUID,
    db: Session = Depends(get_db),
    use_orm: bool = False,
):
    svc = LocationORMService(db) if use_orm else LocationService(db)
    start = time.perf_counter()
    loc = svc.get_by_id(location_id)
    elapsed = time.perf_counter() - start
    if loc is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return {
        "data": loc,
        "execution_time": _fmt(elapsed),
        "method": "orm" if use_orm else "raw",
    }
