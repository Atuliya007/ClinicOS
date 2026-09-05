from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.modules.doctors.api import router as doctor_router
from app.modules.patients.api import router as patient_router
from app.modules.receptionists.api import router as receptionist_router
from app.modules.appointments.api import router as appointment_router
from app.modules.departments.api import router as department_router
from app.modules.laboratory.api import router as laboratory_router
from app.modules.pharmacy.api import router as pharmacy_router
from app.modules.billing.api import router as billing_router

app = FastAPI(
    title="ClinicOS API",
    version="0.1.0",
)

# The frontend is a separately served static application in development.
# Keep this limited to local origins; deployment should configure its own origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500", "http://127.0.0.1:8080", "http://localhost:8080"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(patient_router)
app.include_router(doctor_router)
app.include_router(receptionist_router)
app.include_router(appointment_router)
app.include_router(department_router)
app.include_router(laboratory_router)
app.include_router(pharmacy_router)
app.include_router(billing_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to ClinicOS 🚀"
    }
