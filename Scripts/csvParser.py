import re
import csv
import os
import glob
from datetime import datetime

CURRENT_DIR = os.getcwd()


def parse_hammerdb_result_log(log_file_path):
    """
    Parse HammerDB result log and extract database type, VU count, and NOPM.

    Args:
        log_file_path (str): Path to the input log file

    Returns:
        tuple: (database, vu_count, nopm) or None if not found
    """

    database = None
    vu_count = None
    nopm = None

    # Extract VU count from filename (last number in the filename)
    filename = os.path.basename(log_file_path)
    vu_match = re.search(r"_(\d+)\.log$", filename)
    if vu_match:
        vu_count = int(vu_match.group(1))

    # Pattern to match the test result line
    result_pattern = r"TEST RESULT : System achieved (\d+) NOPM from \d+ (\w+) TPM"

    try:
        with open(log_file_path, "r") as file:
            for line in file:
                line = line.strip()

                # Look for test result
                result_match = re.search(result_pattern, line)
                if result_match:
                    nopm = int(result_match.group(1))
                    database = result_match.group(2)
                    break

        if database and vu_count is not None and nopm is not None:
            return (database, vu_count, nopm)
        else:
            print(
                f"Warning: Could not extract complete data from {os.path.basename(log_file_path)}"
            )
            return None

    except FileNotFoundError:
        print(f"Error: Could not find the file {log_file_path}")
        return None
    except Exception as e:
        print(f"Error processing file {log_file_path}: {e}")
        return None


def process_all_hammerdb_files():
    """
    Process all hammerdb*.log files in the current directory and create a summary CSV
    """

    # Create csv folder if it doesn't exist
    csv_folder = os.path.join(CURRENT_DIR, "csv")
    os.makedirs(csv_folder, exist_ok=True)

    # Find all hammerdb log files
    log_files = glob.glob(os.path.join(CURRENT_DIR, "hammerdb*.log"))

    if not log_files:
        print("No hammerdb*.log files found in the current directory.")
        return

    print(f"Found {len(log_files)} hammerdb log file(s):")

    # Store all results
    results = []

    for log_file in log_files:
        print(f"Processing: {os.path.basename(log_file)}")
        result = parse_hammerdb_result_log(log_file)

        if result:
            database, vu_count, nopm = result
            results.append([database, vu_count, nopm])
            print(f"  -> {database}, VU: {vu_count}, NOPM: {nopm}")
        else:
            print(f"  -> Failed to extract data")

    # Sort results by Database (alphabetically) and then by VU (numerically)
    results.sort(key=lambda x: (x[0], x[1]))

    # Write results to CSV
    if results:
        output_csv = os.path.join(csv_folder, "hammerdb_summary.csv")

        with open(output_csv, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            # Write header
            writer.writerow(["Database", "VU", "NOPM"])
            # Write data
            writer.writerows(results)

        print(
            f"\nSuccessfully created summary with {len(results)} records: {os.path.basename(output_csv)}"
        )
        print(f"CSV file stored in: {csv_folder}")
    else:
        print("\nNo valid results found to write to CSV.")


def parse_hammerdb_log_to_csv(log_file_path, output_csv_path):
    """
    Parse HammerDB transaction counter log and convert to CSV format.
    Works with MariaDB, MySQL, and PostgreSQL logs.

    Args:
        log_file_path (str): Path to the input log file
        output_csv_path (str): Path to the output CSV file
    """

    # Pattern to match lines with TPM data for any database type
    pattern = r"(\d+) (?:MariaDB|MySQL|PostgreSQL) tpm @ .+ (\d{2}:\d{2}:\d{2}) UTC"

    parsed_data = []

    try:
        with open(log_file_path, "r") as file:
            for line in file:
                match = re.search(pattern, line.strip())
                if match:
                    tpm = int(match.group(1))
                    timestamp = match.group(2)

                    # Skip the initial 0 TPM entries (startup/shutdown)
                    if tpm > 0:
                        parsed_data.append([tpm, timestamp])

        # Write to CSV
        with open(output_csv_path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            # Write header
            writer.writerow(["tpm", "timestamp"])
            # Write data
            writer.writerows(parsed_data)

        print(
            f"Successfully parsed {len(parsed_data)} records from {os.path.basename(log_file_path)} to {os.path.basename(output_csv_path)}"
        )

    except FileNotFoundError:
        print(f"Error: Could not find the file {log_file_path}")
    except Exception as e:
        print(f"Error processing file {log_file_path}: {e}")


def process_all_hdbtcount_files():
    """
    Process all hdbtcount*.log files in the current directory
    """

    # Create csv folder if it doesn't exist
    csv_folder = os.path.join(CURRENT_DIR, "csv")
    os.makedirs(csv_folder, exist_ok=True)
    print(f"CSV files will be stored in: {csv_folder}")

    # Find all hdbtcount log files
    log_files = glob.glob(os.path.join(CURRENT_DIR, "hdbtcount*.log"))

    if not log_files:
        print("No hdbtcount*.log files found in the current directory.")
        return

    print(f"Found {len(log_files)} hdbtcount log file(s):")

    for log_file in log_files:
        # Create output CSV filename based on input filename
        base_name = os.path.splitext(os.path.basename(log_file))[0]
        output_csv = os.path.join(csv_folder, f"{base_name}.csv")

        print(f"\nProcessing: {os.path.basename(log_file)}")
        parse_hammerdb_log_to_csv(log_file, output_csv)


# Usage
if __name__ == "__main__":
    process_all_hdbtcount_files()
    process_all_hammerdb_files()
