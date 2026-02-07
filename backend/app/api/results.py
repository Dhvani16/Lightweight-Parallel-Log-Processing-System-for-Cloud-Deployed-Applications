from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.result import Result
from app.models.user import User
from app.api.auth import get_current_user
from app.schemas.result import ResultOut
router = APIRouter(prefix="/results", tags=["results"])


@router.get("/{job_id}", response_model=ResultOut)
def get_results(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = (
        db.query(Result)
        .join(Job)
        .filter(
            Job.id == job_id,
            Job.user_id == current_user.id,
        )
        .first()
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Result not found",
        )

    return result