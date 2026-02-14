import time
from app.core.database import SessionLocal
from app.models.job import Job
from app.models.result import Result
from app.processing.sequential import process_log_sequential
from app.processing.parallel import process_log_parallel
from app.processing.progress import update_progress

def run_job(job_id: int, file_path: str):
    db = SessionLocal()
    try:
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            return

        job.status = "running"
        job.progress = 0
        db.commit()

        def cancel_check():
            db.refresh(job)
            return job.cancel_requested is True

        def progress_cb(p: int):
            update_progress(job.id, p)

        start = time.perf_counter()

        if job.mode == "sequential":
            metrics = process_log_sequential(
                file_path,
                cancel_check,
                progress_cb,
            )
        else:
            # Parallel jobs are NOT cancellable mid-run
            metrics = process_log_parallel(
                file_path,
                job.workers,
                progress_cb,
            )
            update_progress(job.id, 100)

        if job.cancel_requested:
            job.status = "cancelled"
            job.progress = progress_cb
            db.commit()
            return

        job.status = "completed"
        job.progress = 100
        job.duration_ms = (time.perf_counter() - start) * 1000

        db.add(Result(job_id=job.id, **metrics))
        db.commit()

    except Exception:
        job.status = "failed"
        job.error_message = str(e)
        job.progress = 0
        db.commit()
        raise
    finally:
        db.close()