from uuid import UUID
import time

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db


from app.services.employee import EmployeeService
from app.services.employee_orm import EmployeeORMService
from app.services.location import LocationService
from app.services.location_orm import LocationORMService


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
    start = time.perf_counter()
    svc = EmployeeORMService(db) if use_orm else EmployeeService(db)
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
    start = time.perf_counter()
    svc = EmployeeORMService(db) if use_orm else EmployeeService(db)
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
    start = time.perf_counter()
    svc = LocationORMService(db) if use_orm else LocationService(db)
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
    start = time.perf_counter()
    svc = LocationORMService(db) if use_orm else LocationService(db)
    loc = svc.get_by_id(location_id)
    elapsed = time.perf_counter() - start
    if loc is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return {
        "data": loc,
        "execution_time": _fmt(elapsed),
        "method": "orm" if use_orm else "raw",
    }
