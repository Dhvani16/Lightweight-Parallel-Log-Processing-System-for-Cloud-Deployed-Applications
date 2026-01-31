from pydantic import BaseModel


class JobCreate(BaseModel):
    mode: str          # sequential | parallel
    workers: int       # 1, 2, 4


class JobStatus(BaseModel):
    id: int
    status: str
    duration_ms: float | None