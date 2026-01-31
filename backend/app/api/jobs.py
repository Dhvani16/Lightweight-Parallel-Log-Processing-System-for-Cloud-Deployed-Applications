import time
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.job import Job
from app.models.result import Result
from app.processing.sequential import process_log_sequential
from app.processing.parallel import process_log_parallel
from app.utils.file_handler import save_upload_file
from app.schemas.job import JobStatus

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("/upload", response_model=JobStatus)
def upload_log(
    mode: str,
    workers: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if mode not in {"sequential", "parallel"}:
        raise HTTPException(status_code=400, detail="Invalid mode")

    if workers not in {1, 2, 4}:
        raise HTTPException(status_code=400, detail="Invalid worker count")

    job = Job(
        user_id=1,  # TEMP: auth integration later
        mode=mode,
        workers=workers,
        status="pending",
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    file_path = save_upload_file(file)

    job.status = "running"
    db.commit()

    start = time.perf_counter()

    if mode == "sequential":
        metrics = process_log_sequential(file_path)
    else:
        metrics = process_log_parallel(file_path, workers)

    duration = (time.perf_counter() - start) * 1000

    result = Result(job_id=job.id, **metrics)
    db.add(result)

    job.status = "completed"
    job.duration_ms = duration
    db.commit()

    return {
        "id": job.id,
        "status": job.status,
        "duration_ms": job.duration_ms,
    }

@router.get("/{job_id}", response_model=JobStatus)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return {
        "id": job.id,
        "status": job.status,
        "duration_ms": job.duration_ms,
    }