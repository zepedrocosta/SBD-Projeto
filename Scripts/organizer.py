import os
import re
from datetime import datetime
from pathlib import Path


def parse_log_file(file_path):
    """
    Parse a log file to extract database type, timestamp, and log type.
    Returns a tuple: (log_type, database, timestamp_str, datetime_obj)
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Determine log type based on content
        filename = file_path.name.lower()
        if filename.startswith("hdbtcount"):
            log_type = "hdbtcount"
        elif filename.startswith("hammerdb"):
            log_type = "hammerdb"
        else:
            return None

        # Extract database type
        database = None
        db_patterns = [
            r"(\w+)\s+tpm\s+@",  # MariaDB tpm @
            r"(\w+)\s+TPM",  # PostgreSQL TPM
            r"PostgreSQL",
            r"MySQL",
            r"MariaDB",
        ]

        for pattern in db_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                if pattern in [r"(\w+)\s+tpm\s+@", r"(\w+)\s+TPM"]:
                    database = match.group(1)
                else:
                    database = match.group(0)
                break

        if not database:
            return None

        # Extract timestamp from first line
        first_line = content.split("\n")[0]

        # Look for the specific timestamp pattern: @ Fri Jun 06 16:52:43 UTC 2025
        timestamp_pattern = (
            r"@\s+([A-Za-z]{3}\s+[A-Za-z]{3}\s+\d{2}\s+\d{2}:\d{2}:\d{2}\s+UTC\s+\d{4})"
        )

        match = re.search(timestamp_pattern, first_line)
        if match:
            timestamp_str = match.group(1)
            try:
                datetime_obj = datetime.strptime(
                    timestamp_str, "%a %b %d %H:%M:%S UTC %Y"
                )
            except ValueError:
                return None
        else:
            return None

        return (log_type, database, timestamp_str, datetime_obj)

    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return None


def organize_log_files(directory_path):
    """
    Organize log files in the specified directory.
    """
    directory = Path(directory_path)

    if not directory.exists():
        print(f"Directory {directory_path} does not exist.")
        return

    # Find all log files
    log_files = []
    for ext in ["*.log", "*.txt"]:
        log_files.extend(directory.glob(ext))

    if not log_files:
        print("No log files found in the directory.")
        return

    print(f"Found {len(log_files)} log files to process.")

    # Parse and organize files
    file_info = []

    for file_path in log_files:
        print(f"Processing: {file_path.name}")
        parsed = parse_log_file(file_path)

        if parsed:
            log_type, database, timestamp_str, datetime_obj = parsed
            file_info.append(
                (file_path, log_type, database, timestamp_str, datetime_obj)
            )
            print(f"  -> Type: {log_type}, Database: {database}, Time: {timestamp_str}")
        else:
            print(f"  -> Could not parse file")

        # Sort by timestamp
    file_info.sort(key=lambda x: x[4])  # Sort by datetime_obj

    # Group files by type and database, then assign sequential numbers
    print("\nRenaming files:")

    # Create a dictionary to track counters for each type-database combination
    counters = {}

    for file_path, log_type, database, timestamp_str, datetime_obj in file_info:
        # Create a key for this type-database combination
        key = f"{log_type}_{database}"

        # Initialize or increment counter for this combination
        if key not in counters:
            counters[key] = 0  # Start at 0 to track position

        counters[key] += 1

        # Create sequence: 2, 4, 8, 12, 16, 20, 24, 28...
        position = counters[key]
        if position <= 2:
            sequence_number = position * 2  # 2, 4
        else:
            sequence_number = 4 + (position - 2) * 4  # 8, 12, 16, 20...

        # Create new filename with sequential number
        new_name = f"{log_type}_{database}_{sequence_number}{file_path.suffix}"
        new_path = file_path.parent / new_name

        # Handle duplicate names (shouldn't happen with this logic, but keeping as safety)
        counter = 1
        while new_path.exists() and new_path != file_path:
            name_parts = new_name.rsplit(".", 1)
            if len(name_parts) == 2:
                new_name = f"{name_parts[0]}_{counter}.{name_parts[1]}"
            else:
                new_name = f"{new_name}_{counter}"
            new_path = file_path.parent / new_name
            counter += 1

        if new_path != file_path:
            try:
                file_path.rename(new_path)
                print(f"  {file_path.name} -> {new_name}")
            except Exception as e:
                print(f"  Error renaming {file_path.name}: {e}")
        else:
            print(f"  {file_path.name} (no change needed)")


if __name__ == "__main__":
    # Use current directory or specify a different path
    directory_path = "."

    print(f"Organizing log files in: {directory_path}")
    organize_log_files(directory_path)
    print("\nDone!")
