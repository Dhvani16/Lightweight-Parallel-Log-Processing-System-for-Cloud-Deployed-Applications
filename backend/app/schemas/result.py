from pydantic import BaseModel


class ResultOut(BaseModel):
    total_lines: int
    error_count: int
    warning_count: int