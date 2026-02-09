from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.core.database import get_db
from app.models.job import Job
from app.models.user import User
from app.processing.runner import run_job
from app.utils.file_handler import save_upload_file
from app.schemas.job import JobStatus

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("/upload", response_model=JobStatus)
def upload_log(
    mode: str,
    workers: int,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if mode not in {"sequential", "parallel"}:
        raise HTTPException(status_code=400, detail="Invalid mode")

    if workers not in {1, 2, 4}:
        raise HTTPException(status_code=400, detail="Invalid worker count")

    job = Job(
        user_id=current_user.id,
        mode=mode,
        workers=workers,
        status="pending",
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    file_path = save_upload_file(file)

    # Run asynchronously
    background_tasks.add_task(run_job, job.id, file_path)

    return {
        "id": job.id,
        "status": job.status,
        "progress": 0,
        "duration_ms": None,
        "error_message": job.error_message,
    }


@router.get("/{job_id}", response_model=JobStatus)
def get_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    job = (
        db.query(Job)
        .filter(Job.id == job_id, Job.user_id == current_user.id)
        .first()
    )

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return {
        "id": job.id,
        "status": job.status,
        "duration_ms": job.duration_ms,
        "progress": job.progress,
        "error_message": job.error_message,
    }

@router.get("", response_model=list[JobStatus])
def list_jobs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    jobs = (
        db.query(Job)
        .filter(Job.user_id == current_user.id)
        .order_by(Job.id.desc())
        .all()
    )

    return jobs

@router.post("/{job_id}/cancel")
def cancel_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    job = (
        db.query(Job)
        .filter(Job.id == job_id, Job.user_id == current_user.id)
        .first()
    )

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if job.status in {"completed", "failed", "cancelled"}:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot cancel job with status '{job.status}'",
        )
    
    if job.mode == "parallel" and job.status == "running":
        raise HTTPException(
            status_code=400,
            detail="Parallel jobs cannot be cancelled once started",
        )

    job.cancel_requested = True
    db.commit()

    return {"message": "Cancellation requested"}