from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.models.job import Job

router = APIRouter()

@router.get("/")
def get_stats(db: Session = Depends(get_db)):

    seq_avg = (
        db.query(func.avg(Job.duration_ms))
        .filter(Job.mode == "sequential", Job.status == "completed")
        .scalar()
    )

    par_avg = (
        db.query(func.avg(Job.duration_ms))
        .filter(Job.mode == "parallel", Job.status == "completed")
        .scalar()
    )

    speedup = None
    if seq_avg and par_avg and par_avg > 0:
        speedup = seq_avg / par_avg

    return {
        "sequential_avg_ms": seq_avg,
        "parallel_avg_ms": par_avg,
        "speedup": speedup,
    }