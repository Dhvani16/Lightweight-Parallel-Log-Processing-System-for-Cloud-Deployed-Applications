import time
from app.core.database import SessionLocal
from app.models.job import Job
from app.models.result import Result
from app.processing.sequential import process_log_sequential
from app.processing.parallel import process_log_parallel

def run_job(job_id: int, file_path: str):
    db = SessionLocal()
    try:
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            return

        job.status = "running"
        job.progress = 0
        db.commit()

        start = time.perf_counter()

        if job.mode == "sequential":
            last_cancel_check = 0

            def cancel_check():
                nonlocal last_cancel_check
                now = time.perf_counter()
                if now - last_cancel_check > 1:
                    db.refresh(job)
                    last_cancel_check = now
                return job.cancel_requested is True

            def progress_cb(p: int):
                job.progress = min(p, 100)
                db.flush()

            metrics = process_log_sequential(file_path, cancel_check, progress_cb)

        else:
            # Parallel processing
            metrics = process_log_parallel(
                file_path,
                job.workers,
                lambda p: None  # avoid DB in worker processes
            )
            job.progress = 100
            db.flush()

        db.refresh(job)
        if job.cancel_requested:
            job.status = "cancelled"
            db.commit()
            return

        # Mark completion
        job.status = "completed"
        job.progress = 100
        job.duration_ms = (time.perf_counter() - start) * 1000

        db.add(Result(job_id=job.id, **metrics))
        db.commit()

    except Exception as e:
        job.status = "failed"
        job.error_message = str(e)
        job.progress = 0
        db.commit()
        raise

    finally:
        db.close()