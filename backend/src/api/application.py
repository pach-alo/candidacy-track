from fastapi import APIRouter, HTTPException
from sqlalchemy import text

from db.db import engine
from schemas.application import ApplicationCreate

router = APIRouter(
    prefix="/applications",
    tags=["Applications"]
)

@router.post("/")
def create_application(application: ApplicationCreate):

    with engine.begin() as connection:

        company_query = text("""
            SELECT id
            FROM companies
            WHERE id = :company_id
        """)

        company = connection.execute(
            company_query,
            {"company_id": application.company_id}
        ).first()

        if company is None:
            raise HTTPException(
                status_code=404,
                detail=f"Company with ID {application.company_id} not found"
            )

        query = text("""
            INSERT INTO applications(
                job_title, job_url, date_applied, status, notes, company_id
            )
            VALUES (
                :job_title, :job_url, :date_applied,
                :status, :notes, :company_id
            )
            RETURNING id, job_title, job_url, date_applied,
                      status, notes, company_id
        """)

        result = connection.execute(query, {
            "job_title": application.job_title,
            "job_url": str(application.job_url) if application.job_url else None,
            "date_applied": application.date_applied,
            "status": application.status.value,
            "notes": application.notes,
            "company_id": application.company_id
        })

        created_application = result.mappings().first()

    return dict(created_application)


@router.get("/")
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