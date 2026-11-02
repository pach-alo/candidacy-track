from fastapi import FastAPI
from sqlalchemy import text
from schemas import ApplicationStatus, ApplicationCreate
from db import engine

app = FastAPI()
@app.get("/")
@app.post("/applications/")
def create_application(application: ApplicationCreate):
    query = text("""
    INSERT INTO applications(
    job_title, job_url, date_applied, status, notes, company_id
    )
    VALUES (:job_title, :job_url, :date_applied, :status, :notes, :company_id))
    RETURNING id, job_title, job_url, date_applied, status, notes, company_id
    """)

    with engine.connect() as connection:
        result = connection.execute(query, {
            "job_title": application.job_title,
            "job_url": application.job_url,
            "date_applied": application.date_applied,
            "status": application.status,
            "notes": application.notes,
            "company_id": application.company_id
        })
        created_application = result.fetchone()

    return created_application

@app.get("/applications")
def get_applications():
    query = text("""
    SELECT
        a.id,
        c.name AS company,
        a.job_title,
        a.job_url,
        a.status,
        a.date_applied,
        a.notes,
        a.created_at,
        a.updated_at
    FROM applications AS a
    JOIN companies AS c 
        ON a.company_id = c.id
    ORDER BY a.created_at DESC
    """)

    with engine.connect() as connection:
        result = connection.execute(query)
        applications = [dict(row) for row in result.mappings()]

    return applications