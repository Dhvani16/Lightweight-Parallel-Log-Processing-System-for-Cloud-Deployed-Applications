import os
import re

pattern = re.compile(r"(ERROR|WARNING|CRITICAL):\s+\w+\s+\d+")

def process_log_sequential(file_path: str, cancel_check, progress_cb) -> dict:
    total_lines = 0
    error_count = 0
    warning_count = 0

    file_size = os.path.getsize(file_path)
    bytes_read = 0
    last_reported = -1

    with open(file_path, "r") as f:
        for line in f:

            if cancel_check():
                break

            total_lines += 1
            l = line.lower()

            if "error" in l:
                error_count += 1
            if "warning" in l:
                warning_count += 1

            bytes_read += len(line)

            percent = int((bytes_read / file_size) * 100)
            if percent // 10 != last_reported:
                last_reported = percent // 10
                progress_cb(percent)

    return {
        "total_lines": total_lines,
        "error_count": error_count,
        "warning_count": warning_count,
    }