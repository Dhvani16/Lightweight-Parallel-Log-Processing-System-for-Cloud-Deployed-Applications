from pydantic import BaseModel
from typing import Optional

class JobCreate(BaseModel):
    mode: str          # sequential | parallel
    workers: int       # 1, 2, 4


class JobStatus(BaseModel):
    id: int
    status: str
    progress: Optional[int]
    duration_ms: Optional[float]
    error_message: Optional[str] = None

    class Config:
        from_attributes = True