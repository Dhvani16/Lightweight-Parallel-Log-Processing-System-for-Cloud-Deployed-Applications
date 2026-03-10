from sqlalchemy.orm import Session
from app.models.job import Job

def is_cancelled(db: Session, job_id: int) -> bool:
    job = db.query(Job).filter(Job.id == job_id).first()
    return job is None or job.status == "cancelled"