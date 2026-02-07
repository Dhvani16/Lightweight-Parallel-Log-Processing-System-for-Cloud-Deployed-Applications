from concurrent.futures import ProcessPoolExecutor
from typing import Dict, List
import math

def process_chunk(lines: List[str]) -> Dict[str, int]:
    total = 0
    errors = 0
    warnings = 0

    for line in lines:
        total += 1
        l = line.lower()
        if "error" in l:
            errors += 1
        if "warning" in l:
            warnings += 1

    return {
        "total_lines": total,
        "error_count": errors,
        "warning_count": warnings,
    }

def process_log_parallel(file_path: str, workers: int, progress_cb) -> Dict[str, int]:
    with open(file_path, "r", errors="ignore") as f:
        lines = f.readlines()

    chunk_size = max(1, len(lines) // workers)
    chunks = [
        lines[i:i + chunk_size]
        for i in range(0, len(lines), chunk_size)
    ]

    completed = 0
    results = []

    with ProcessPoolExecutor(max_workers=workers) as executor:
        for partial in executor.map(process_chunk, chunks):
            results.append(partial)
            completed += 1
            percent = int((completed / len(chunks)) * 100)
            progress_cb(percent)

    return {
        "total_lines": sum(r["total_lines"] for r in results),
        "error_count": sum(r["error_count"] for r in results),
        "warning_count": sum(r["warning_count"] for r in results),
    }