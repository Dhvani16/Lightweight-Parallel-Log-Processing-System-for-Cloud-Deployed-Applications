from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    mode = Column(String, nullable=False)          # sequential | parallel
    workers = Column(Integer, nullable=False)      # 1, 2, 4

    status = Column(String, nullable=False)        # pending | running | completed | failed

    start_time = Column(DateTime(timezone=True))
    end_time = Column(DateTime(timezone=True))
    duration_ms = Column(Float)