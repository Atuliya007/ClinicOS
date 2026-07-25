from fastapi import FastAPI

app = FastAPI(
    title="ClinicOS API",
    version="0.1.0",
)


@app.get("/")
def root():
    return {"message": "Welcome to ClinicOS 🚀"}