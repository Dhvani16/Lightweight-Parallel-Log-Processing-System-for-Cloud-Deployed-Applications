from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from app.core.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    mode = Column(String, nullable=False)          # sequential | parallel
    workers = Column(Integer, nullable=False)      # 1, 2, 4

    status = Column(String, default="pending")        # pending | running | completed | failed

    duration_ms = Column(Float, nullable=True)
    cancel_requested = Column(Boolean, default=False)

    progress = Column(Integer, default=0)