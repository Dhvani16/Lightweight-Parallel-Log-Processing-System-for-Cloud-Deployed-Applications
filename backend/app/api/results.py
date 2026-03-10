from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.result import Result
from app.models.job import Job
from app.models.user import User
from app.schemas.result import ResultOut
router = APIRouter(prefix="/results", tags=["results"])


@router.get("/{job_id}", response_model=ResultOut)
def get_results(
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

    result = db.query(Result).filter(Result.job_id == job_id).first()

    if not result:
        raise HTTPException(status_code=404, detail="Result not ready")

    return result