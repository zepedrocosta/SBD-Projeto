# sys_usage analysis with time-based analysis
import glob
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime


def extract_database_from_filename(filename):
    """Extract database name from sys_usage filename"""
    basename = os.path.basename(filename)
    if "mysql" in basename.lower():
        return "MySQL"
    elif "postgresql" in basename.lower() or "postgres" in basename.lower():
        return "PostgreSQL"
    elif "mariadb" in basename.lower():
        return "MariaDB"
    else:
        return "Unknown"


def divide_into_time_ranges(df, num_ranges=4):
    """Divide dataframe into time ranges based on timestamps"""
    total_rows = len(df)
    rows_per_range = total_rows // num_ranges

    ranges = []
    for i in range(num_ranges):
        start_idx = i * rows_per_range
        if i == num_ranges - 1:  # Last range gets remaining rows
            end_idx = total_rows
        else:
            end_idx = (i + 1) * rows_per_range

        range_data = df.iloc[start_idx:end_idx]
        ranges.append(
            {
                "data": range_data,
                "label": f"Time Range {i+1}",
                "start_time": (
                    range_data["Timestamp"].iloc[0] if len(range_data) > 0 else "N/A"
                ),
                "end_time": (
                    range_data["Timestamp"].iloc[-1] if len(range_data) > 0 else "N/A"
                ),
            }
        )

    return ranges


# Define paths for sys_usage files
base_paths = [
    os.path.join("Results", "Rodrigo", "res_desktop", "csv"),  # PC 1
    os.path.join("Results", "Silva", "csv"),  # PC 2
    os.path.join("Results", "Ze", "csv"),  # PC 3
    os.path.join("Results", "Rodrigo", "res_macos", "csv"),  # PC 4
]

pc_labels = ["PC 1", "PC 2", "PC 3", "PC 4"]
pc_ram_gb = [16, 16, 32, 16]

# Dictionary to store data for each database and time range
database_time_data = {}

for i, (base_path, pc_label, ram_gb) in enumerate(
    zip(base_paths, pc_labels, pc_ram_gb)
):
    pattern = os.path.join(base_path, "sys_usage_*.csv")
    sys_files = glob.glob(pattern)

    for file_path in sys_files:
        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
                df.columns = df.columns.str.strip()

                database = extract_database_from_filename(file_path)

                # Clean CPU data
                df["CPU_Usage_Percent"] = pd.to_numeric(
                    df["CPU_Usage_Percent"], errors="coerce"
                )

                # For PC 1, divide into 5 ranges but only use first 4
                if pc_label == "PC 1":
                    time_ranges = divide_into_time_ranges(df, num_ranges=5)
                    time_ranges = time_ranges[:4]  # Only use first 4 ranges
                else:
                    time_ranges = divide_into_time_ranges(df, num_ranges=4)

                # Initialize database entry if not exists
                if database not in database_time_data:
                    database_time_data[database] = {
                        "time_ranges": {
                            f"range_{j+1}": {"cpu": [], "ram": [], "pc_labels": []}
                            for j in range(4)
                        },
                        "pc_labels": [],
                    }

                # Process each time range
                for j, time_range in enumerate(time_ranges):
                    range_df = time_range["data"]

                    if len(range_df) > 0:
                        # Filter CPU values >= 10% before calculating average
                        cpu_filtered = range_df[range_df["CPU_Usage_Percent"] >= 10][
                            "CPU_Usage_Percent"
                        ]

                        if len(cpu_filtered) > 0:
                            avg_cpu = cpu_filtered.mean()
                        else:
                            # If no values >= 10%, use all available values
                            avg_cpu = range_df["CPU_Usage_Percent"].mean()

                        # RAM calculation remains the same (no filtering)
                        avg_ram_mb = range_df["RAM_Used_MB"].mean()
                        total_ram_mb = ram_gb * 1024
                        avg_ram_percent = (avg_ram_mb / total_ram_mb) * 100

                        range_key = f"range_{j+1}"
                        database_time_data[database]["time_ranges"][range_key][
                            "cpu"
                        ].append(avg_cpu)
                        database_time_data[database]["time_ranges"][range_key][
                            "ram"
                        ].append(avg_ram_percent)
                        database_time_data[database]["time_ranges"][range_key][
                            "pc_labels"
                        ].append(pc_label)

            except Exception as e:
                print(f"Error reading {file_path}: {e}")

# Create Graphs directory if it doesn't exist
os.makedirs("Graphs", exist_ok=True)

# Create time-based comparison graphs for each database
for database, data in database_time_data.items():
    if not any(data["time_ranges"][f"range_{i}"]["cpu"] for i in range(1, 5)):
        continue

    # Create a 2x2 subplot for the 4 time ranges
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle(
        f"{database} - CPU & RAM Usage Across Time Ranges",
        fontsize=16,
    )

    for i in range(4):
        row = i // 2
        col = i % 2
        ax = axes[row, col]

        range_key = f"range_{i+1}"
        range_data = data["time_ranges"][range_key]

        if range_data["cpu"]:
            x_pos = np.arange(len(range_data["pc_labels"]))
            width = 0.35

            # Create bars for CPU and RAM
            bars1 = ax.bar(
                x_pos - width / 2,
                range_data["cpu"],
                width,
                label="CPU %",
                color="skyblue",
                alpha=0.7,
            )
            bars2 = ax.bar(
                x_pos + width / 2,
                range_data["ram"],
                width,
                label="RAM %",
                color="lightcoral",
                alpha=0.7,
            )

            # Add value labels
            for bar, value in zip(bars1, range_data["cpu"]):
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 1,
                    f"{value:.1f}%",
                    ha="center",
                    va="bottom",
                    fontsize=8,
                )

            for bar, value in zip(bars2, range_data["ram"]):
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 1,
                    f"{value:.1f}%",
                    ha="center",
                    va="bottom",
                    fontsize=8,
                )

            ax.set_ylabel("Usage (%)")
            ax.set_xlabel("Machine")
            ax.set_xticks(x_pos)
            ax.set_xticklabels(range_data["pc_labels"])
            ax.legend()
            ax.grid(axis="y", linestyle="--", alpha=0.7)
            ax.set_ylim(0, 100)

    plt.tight_layout()
    output_path = os.path.join(
        "Graphs", f"sys_usage_{database.lower()}_time_ranges_filtered.png"
    )
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()

# Create combined comparison across all databases for each time range
for i in range(1, 5):
    if not database_time_data:
        continue

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

    databases = list(database_time_data.keys())
    x_positions = range(len(pc_labels))
    bar_width = 0.25

    range_key = f"range_{i}"

    # CPU Usage Comparison for this time range
    for j, database in enumerate(databases):
        cpu_values = []
        for pc in pc_labels:
            range_data = database_time_data[database]["time_ranges"][range_key]
            if pc in range_data["pc_labels"]:
                idx = range_data["pc_labels"].index(pc)
                cpu_values.append(range_data["cpu"][idx])
            else:
                cpu_values.append(0)

        x_pos = [x + j * bar_width for x in x_positions]
        ax1.bar(x_pos, cpu_values, bar_width, label=database, alpha=0.8)

    ax1.set_xlabel("Machine")
    ax1.set_ylabel("CPU Usage (%)")
    ax1.set_xticks([x + bar_width * (len(databases) - 1) / 2 for x in x_positions])
    ax1.set_xticklabels(pc_labels)
    ax1.legend()
    ax1.grid(axis="y", linestyle="--", alpha=0.7)

    # RAM Usage Comparison for this time range
    for j, database in enumerate(databases):
        ram_values = []
        for pc in pc_labels:
            range_data = database_time_data[database]["time_ranges"][range_key]
            if pc in range_data["pc_labels"]:
                idx = range_data["pc_labels"].index(pc)
                ram_values.append(range_data["ram"][idx])
            else:
                ram_values.append(0)

        x_pos = [x + j * bar_width for x in x_positions]
        ax2.bar(x_pos, ram_values, bar_width, label=database, alpha=0.8)

    ax2.set_xlabel("Machine")
    ax2.set_ylabel("RAM Usage (%)")
    ax2.set_xticks([x + bar_width * (len(databases) - 1) / 2 for x in x_positions])
    ax2.set_xticklabels(pc_labels)
    ax2.legend()
    ax2.grid(axis="y", linestyle="--", alpha=0.7)

    plt.tight_layout()
    output_path = os.path.join(
        "Graphs", f"sys_usage_all_databases_time_range_{i}_filtered.png"
    )
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()

print("Time-based system usage graphs generated successfully!!!")
print("Generated graphs with CPU filtering:")
print("- PC 1 data divided into 5 ranges, using first 4 for comparison")
print("- Other PCs divided into 4 ranges as usual")
print("- Individual database time range comparisons (2x2 subplots)")
print("- Cross-database comparisons for each time range")
