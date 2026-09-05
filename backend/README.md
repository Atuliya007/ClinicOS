# ClinicOS backend

ClinicOS is a FastAPI hospital workflow API using SQLAlchemy 2.x, PostgreSQL, and Alembic. Requests flow through API routes, services, repositories, and database models.

## Setup and run

Copy `.env.example` to `.env` and set `DATABASE_URL` to a PostgreSQL database, for example `postgresql+psycopg://user:password@localhost:5432/clinicos`.

```powershell
cd backend
poetry install
poetry run alembic upgrade head
poetry run uvicorn app.main:app --reload
```

Swagger is available at `http://127.0.0.1:8000/docs`; OpenAPI is at `/openapi.json`. Run tests with `poetry run pytest`.

## Modules and workflow

- Patients, Doctors, Receptionists, Departments: registration/catalogue data. Patient, doctor, and receptionist records are deactivated rather than deleted.
- Appointments: validates active linked entities, future times, doctor double-booking, and lifecycle transitions (`PENDING → WAITING → IN_PROCESS → COMPLETED`, with allowed cancellation/no-show branches).
- Laboratory: test catalogue and patient test orders with result completion.
- Pharmacy: medicine inventory and prescriptions. Prescription creation atomically checks and decrements stock.
- Billing: invoices use `Numeric/Decimal`, calculated item totals, and payments that cannot exceed the balance.

Typical workflow: register a patient, create an active receptionist and doctor, book an appointment, complete the consultation, optionally create lab orders or a prescription, then create an invoice and record payments.

## Important routes

`/patients`, `/doctors`, `/receptionists`, `/departments`, `/appointments`, `/laboratory/tests`, `/laboratory/orders`, `/pharmacy/medicines`, `/pharmacy/prescriptions`, `/billing/invoices`.

Use `PATCH` for partial updates. Create endpoints return 201; conflicts such as duplicate contact details or double booking return 409.
