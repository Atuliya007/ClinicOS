from fastapi import FastAPI

from app.modules.patients.api import router as patient_router

app = FastAPI(
    title="ClinicOS API",
    version="0.1.0",
)

app.include_router(patient_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to ClinicOS 🚀"
    }