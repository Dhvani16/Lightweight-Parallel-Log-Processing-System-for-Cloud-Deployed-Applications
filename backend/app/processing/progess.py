from app.core.database import SessionLocal
from app.models.job import Job

def update_progress(job_id: int, progress: int):
    db = SessionLocal()
    try:
        job = db.query(Job).get(job_id)
        if job:
            job.progress = min(progress, 100)
            db.commit()
    finally:
        db.close()