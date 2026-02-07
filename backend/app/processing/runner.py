import time
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.job import Job
from app.models.result import Result
from app.processing.sequential import process_log_sequential
from app.processing.parallel import process_log_parallel
from app.processing.progress import update_progress

def run_job(job_id: int, file_path: str):
    db = SessionLocal()
    job = db.query(Job).get(job_id)

    job.status = "running"
    job.progress = 0
    db.commit()

    def cancel_check():
        db.refresh(job)
        return job.status == "cancelled"

    def progress_cb(p):
        update_progress(job_id, p)

    start = time.perf_counter()

    if job.mode == "sequential":
        metrics = process_log_sequential(file_path, cancel_check, progress_cb)
    else:
        metrics = process_log_parallel(file_path, job.workers, progress_cb)

    job.status = "completed"
    job.progress = 100
    job.duration_ms = (time.perf_counter() - start) * 1000

    db.add(Result(job_id=job.id, **metrics))
    db.commit()
    db.close()

def is_cancelled(db: Session, job_id: int) -> bool:
    return (
        db.query(Job.cancel_requested)
        .filter(Job.id == job_id)
        .scalar()
    )