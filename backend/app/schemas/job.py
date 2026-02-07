from pydantic import BaseModel
from typing import Optional

class JobCreate(BaseModel):
    mode: str          # sequential | parallel
    workers: int       # 1, 2, 4


class JobStatus(BaseModel):
    id: int
    status: str
    duration_ms: Optional[float]
    progress: int

    class Config:
        orm_mode = True