# pgorm

FastAPI app that compares raw SQL vs ORM performance.

## setup

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install fastapi sqlalchemy psycopg pydantic-settings fastapi-cli
```

create a `.env` file:

```
database_url=postgresql://user:pass@localhost/dbname
```

## run

```bash
fastapi run app/main.py
```

## switch between raw sql / orm

add `?use_orm=true` to any endpoint. example:

```
http://localhost:8000/employees/some-uuid?use_orm=true
```

without the flag it uses raw SQL.

## benchmark

```bash
python benchmark.py
```

runs each query 1000 times and saves results to `benchmark.json`.

## project layout

```
app/
├── main.py          # FastAPI routes
├── database.py      # database connection
├── models.py        # table definitions
├── settings.py      # config from .env
└── services/
    ├── base.py      # BaseService with helpers
    ├── employee.py  # raw SQL queries
    ├── employee_orm.py  # same queries with ORM
    ├── location.py  # raw SQL queries
    └── location_orm.py  # same queries with ORM
benchmark.py
```
