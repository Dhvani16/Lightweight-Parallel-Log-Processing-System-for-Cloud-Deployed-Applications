from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.result import Result

router = APIRouter(prefix="/results", tags=["results"])


@router.get("/{job_id}")
def get_result(job_id: int, db: Session = Depends(get_db)):
    result = db.query(Result).filter(Result.job_id == job_id).first()
    return result