from fastapi import FastAPI

from api import application

app = FastAPI(
    title="candidacy-tracker",
    description="API for managing job applications and companies",
)

app.include_router(application.router)

@app.get("/")
def root():
    return {"message": "candidacy tracker is running"}