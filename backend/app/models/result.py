from sqlalchemy import Column, Integer, ForeignKey
from app.core.database import Base


class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)

    total_lines = Column(Integer, nullable=False)
    error_count = Column(Integer, nullable=False)
    warning_count = Column(Integer, nullable=False)