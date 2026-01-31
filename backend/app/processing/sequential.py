def process_log_sequential(file_path: str) -> dict:
    total_lines = 0
    error_count = 0
    warning_count = 0

    with open(file_path, "r", errors="ignore") as f:
        for line in f:
            total_lines += 1
            line_lower = line.lower()
            if "error" in line_lower:
                error_count += 1
            if "warning" in line_lower:
                warning_count += 1

    return {
        "total_lines": total_lines,
        "error_count": error_count,
        "warning_count": warning_count,
    }