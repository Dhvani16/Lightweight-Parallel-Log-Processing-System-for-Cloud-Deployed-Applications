from concurrent.futures import ProcessPoolExecutor
from typing import Dict, Tuple
import os

def process_chunk_from_file_args(args: Tuple[str, int, int]) -> Dict[str, int]:
    """Top-level helper for multiprocessing (pickleable)."""
    file_path, start, end = args
    total = errors = warnings = 0
    with open(file_path, "r", errors="ignore") as f:
        f.seek(start)
        while f.tell() < end:
            line = f.readline()
            if not line:
                break
            total += 1
            l = line.lower()
            if "error" in l:
                errors += 1
            if "warning" in l:
                warnings += 1
    return {
        "total_lines": total, 
        "error_count": errors, 
        "warning_count": warnings
    }

def process_log_parallel(file_path: str, workers: int, progress_cb) -> Dict[str, int]:
    file_size = os.path.getsize(file_path)
    chunk_size = file_size // workers
    offsets = [(file_path, i * chunk_size, (i + 1) * chunk_size if i < workers - 1 else file_size)
               for i in range(workers)]

    results = []
    bytes_done = 0

    # Map using the top-level helper (no lambdass)
    with ProcessPoolExecutor(max_workers=workers) as executor:
        for r in executor.map(process_chunk_from_file_args, offsets):
            results.append(r)
            bytes_done += chunk_size
            percent = min(100, int((bytes_done / file_size) * 100))
            progress_cb(percent)

    return {
        "total_lines": sum(r["total_lines"] for r in results),
        "error_count": sum(r["error_count"] for r in results),
        "warning_count": sum(r["warning_count"] for r in results),
    }