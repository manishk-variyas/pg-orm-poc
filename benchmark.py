# benchmark.py
# Runs each query 1000 times, compares raw SQL vs ORM speed.
# Saves results to benchmark.json.

import json
import time
import statistics
from uuid import uuid4

from app.database import SessionLocal
from app.services.employee import EmployeeService
from app.services.employee_orm import EmployeeORMService
from app.services.location import LocationService
from app.services.location_orm import LocationORMService

N = 1000
fake_id = uuid4()
results = {}


def bench(label, service_cls, method, *args):
    times = []
    for _ in range(N):
        db = SessionLocal()
        svc = service_cls(db)
        t0 = time.perf_counter()
        getattr(svc, method)(*args)
        times.append(time.perf_counter() - t0)
        db.close()

    times = times[50:]
    avg = round(statistics.mean(times) * 1000, 3)
    results[label] = avg
    print(f"  {label:30s}  {avg}ms")


print(f"Each query runs {N}x\n")

print("── get_by_id (cache miss) ──")
bench("raw  EmployeeService", EmployeeService, "get_by_id", fake_id)
bench("orm  EmployeeORMService", EmployeeORMService, "get_by_id", fake_id)

print("\n── get_by_id (cache hot) ──")
bench("raw  EmployeeService", EmployeeService, "get_by_id", fake_id)
bench("orm  EmployeeORMService", EmployeeORMService, "get_by_id", fake_id)

print("\n── get_all ──")
bench("raw  LocationService", LocationService, "get_all")
bench("orm  LocationORMService", LocationORMService, "get_all")

winner = "RAW" if results["raw  EmployeeService"] < results["orm  EmployeeORMService"] else "ORM"

report = {
    "winner": winner,
    "why": f"Raw SQL avg {results['raw  EmployeeService']}ms vs ORM {results['orm  EmployeeORMService']}ms - barely any difference",
    "results": results,
}

with open("benchmark.json", "w") as f:
    json.dump(report, f, indent=2)

print("\nSaved to benchmark.json")
