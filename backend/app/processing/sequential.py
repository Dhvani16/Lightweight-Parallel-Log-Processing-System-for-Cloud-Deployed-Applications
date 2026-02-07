def process_log_sequential(file_path: str, cancel_check, progress_cb) -> dict:
    total_lines = 0
    error_count = 0
    warning_count = 0

    with open(file_path, "r", errors="ignore") as f:
        lines = f.readlines()

    total = len(lines)

    for i, line in enumerate(lines, start=1):
        if cancel_check():
            break

        total_lines += 1
        l = line.lower()

        if "error" in l:
            error_count += 1
        if "warning" in l:
            warning_count += 1

        if i % 100 == 0 or i == total:
            percent = int((i / total) * 100)
            progress_cb(percent)

    return {
        "total_lines": total_lines,
        "error_count": error_count,
        "warning_count": warning_count,
    }