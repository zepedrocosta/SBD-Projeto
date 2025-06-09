import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


def load_data():
    """Load data from both directories"""
    base_path = (
        "/Users/rodrigoalbuquerque/Desktop/SBD-Projeto/Results/Rodrigo/res_desktop/csv"
    )

    # Directory 1: base csv files
    dir1_summary = pd.read_csv(f"{base_path}/hammerdb_summary.csv")

    # Directory 2: csv_all_wh files
    dir2_summary = pd.read_csv(f"{base_path}/csv_all_wh/hammerdb_summary.csv")

    # Load count data for each database
    databases = ["MySQL", "PostgreSQL", "MariaDB"]
    dir1_counts = {}
    dir2_counts = {}

    for db in databases:
        try:
            dir1_counts[db] = pd.read_csv(f"{base_path}/hdbtcount_{db}_12.csv")
            dir2_counts[db] = pd.read_csv(
                f"{base_path}/csv_all_wh/hdbtcount_{db}_12a.csv"
            )
        except FileNotFoundError:
            print(f"Warning: Could not find files for {db}")
            continue

    return dir1_summary, dir2_summary, dir1_counts, dir2_counts


def create_summary_chart(dir1_summary, dir2_summary, output_path):
    """Create bar chart comparing summary data by database for VU=12 only"""
    fig, ax = plt.subplots(figsize=(10, 6))

    databases = ["MySQL", "PostgreSQL", "MariaDB"]
    colors = {"MySQL": "blue", "PostgreSQL": "green", "MariaDB": "red"}

    # Filter data for VU = 12 only
    dir1_vu12 = dir1_summary[dir1_summary["VU"] == 12]
    dir2_vu12 = dir2_summary[dir2_summary["VU"] == 12]

    # Get NOPM values for each database at VU=12
    dir1_values = []
    dir2_values = []

    for db in databases:
        dir1_val = dir1_vu12[dir1_vu12["Database"] == db]["NOPM"].values
        dir2_val = dir2_vu12[dir2_vu12["Database"] == db]["NOPM"].values

        dir1_values.append(dir1_val[0] if len(dir1_val) > 0 else 0)
        dir2_values.append(dir2_val[0] if len(dir2_val) > 0 else 0)

    x_pos = np.arange(len(databases))
    width = 0.35

    bars1 = ax.bar(
        x_pos - width / 2,
        dir1_values,
        width,
        label="Base",
        alpha=0.8,
        color=[colors[db] for db in databases],
    )
    bars2 = ax.bar(
        x_pos + width / 2,
        dir2_values,
        width,
        label="Use all Warehouses",
        alpha=0.8,
        color=[colors[db] for db in databases],
        hatch="///",
    )

    # Add value labels
    for bar in bars1:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            height,
            f"{height:.0f}",
            ha="center",
            va="bottom",
            fontsize=12,
        )

    for bar in bars2:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            height,
            f"{height:.0f}",
            ha="center",
            va="bottom",
            fontsize=12,
        )

    ax.set_xlabel("Database")
    ax.set_ylabel("NOPM (New Orders Per Minute)")
    ax.set_xticks(x_pos)
    ax.set_xticklabels(databases)
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    # Save to specified path
    summary_path = os.path.join(output_path, "hammerdb_summary_comparison_vu12.png")
    plt.savefig(summary_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Summary chart saved as '{summary_path}'")


def create_count_charts(dir1_counts, dir2_counts, output_path):
    """Create separate line charts for each database comparing TPM over time"""
    colors = {"MySQL": "blue", "PostgreSQL": "green", "MariaDB": "red"}

    for db in dir1_counts.keys():
        if db in dir2_counts and len(dir1_counts[db]) > 0 and len(dir2_counts[db]) > 0:
            fig, ax = plt.subplots(figsize=(12, 6))

            # Process dir1 data (base directory)
            dir1_data = dir1_counts[db]["tpm"].values
            dir1_time = np.linspace(0, 10, len(dir1_data))  # 0 to 10 minutes

            ax.plot(
                dir1_time,
                dir1_data,
                "--",
                color=colors[db],
                label=f"{db} Base",
                alpha=0.8,
                linewidth=2,
            )

            # Process dir2 data (all WH directory)
            dir2_data = dir2_counts[db]["tpm"].values
            dir2_time = np.linspace(0, 10, len(dir2_data))  # 0 to 10 minutes

            ax.plot(
                dir2_time,
                dir2_data,
                "-",
                color=colors[db],
                label=f"{db} (Use all Warehouses)",
                linewidth=2,
            )

            # Customize chart
            ax.set_xlabel("Time (minutes)")
            ax.set_ylabel("Transactions Per Minute (TPM)")
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 600000)
            ax.legend()
            ax.grid(True, alpha=0.3)

            plt.tight_layout()

            # Save to specified path
            count_path = os.path.join(
                output_path, f"database_count_comparison_{db}.png"
            )
            plt.savefig(count_path, dpi=300, bbox_inches="tight")
            plt.close()

            print(f"{db} count chart saved as '{count_path}'")


def main():
    """Main function to execute the script"""
    try:
        # Define output path
        output_path = "/Users/rodrigoalbuquerque/Desktop/SBD-Projeto/Graphs"

        # Create output directory if it doesn't exist
        os.makedirs(output_path, exist_ok=True)

        print("Loading data...")
        dir1_summary, dir2_summary, dir1_counts, dir2_counts = load_data()

        print(f"Dir1 summary shape: {dir1_summary.shape}")
        print(f"Dir2 summary shape: {dir2_summary.shape}")
        print(f"Available databases in counts: {list(dir1_counts.keys())}")

        print("Creating summary chart for VU=12...")
        create_summary_chart(dir1_summary, dir2_summary, output_path)

        print("Creating individual count charts...")
        create_count_charts(dir1_counts, dir2_counts, output_path)

        print("Charts created successfully!")

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
