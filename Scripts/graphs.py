import os
import pandas as pd
import matplotlib.pyplot as plt

# hdbtcount

# File name (easy to change)
filenames = [
    'hdbtcount_MySQL_2.csv',
    'hdbtcount_MySQL_4.csv',
    'hdbtcount_MySQL_8.csv',
    'hdbtcount_MySQL_12.csv',
    'hdbtcount_PostgreSQL_2.csv',
    'hdbtcount_PostgreSQL_4.csv',
    'hdbtcount_PostgreSQL_8.csv',
    'hdbtcount_PostgreSQL_12.csv',
    'hdbtcount_MariaDB_2.csv',
    'hdbtcount_MariaDB_4.csv',
    'hdbtcount_MariaDB_8.csv',
    'hdbtcount_MariaDB_12.csv',
]
for filename in filenames:

    csv_files = [
        rf'Results\Rodrigo\res_desktop\csv\{filename}',  # 1
        rf'Results\Silva\csv\{filename}',                # 2
        rf'Results\Ze\csv\{filename}',                 # 3
        rf'Results\Rodrigo\res_macos\csv\{filename}'     # 4
    ]
    labels = ['PC 1', 'PC 2', 'PC 3', 'PC 4']

    plt.figure(figsize=(14, 7))

    for file, label in zip(csv_files, labels):
        df = pd.read_csv(file)
        tpm_values = df['tpm'].head(61).reset_index(drop=True)
        x_values = [i * 10 / 60 for i in range(len(tpm_values))]  # Scale 0-60 points to 0-10
        plt.plot(x_values, tpm_values, label=label, marker='o', linestyle='-')

    plt.xlabel('Time (minutes)')
    plt.ylabel('TPM')
    plt.legend()
    plt.grid(True)
    plt.xticks(ticks=[i for i in range(11)])
    plt.tight_layout()

    output_path = os.path.join('Graphs', f'{filename.replace(".csv", ".png")}')
    plt.savefig(output_path)

# summary

paths = [
    r'Results\Rodrigo\res_desktop\csv\hammerdb_summary.csv',
    r'Results\Silva\csv\hammerdb_summary.csv',
    r'Results\Ze\csv\hammerdb_summary.csv',
    r'Results\Rodrigo\res_macos\csv\hammerdb_summary.csv'
]

for csv_path in paths:

    # Read the CSV file
    data = pd.read_csv(csv_path)

    # Pivot the data to have VU as x-axis and Database as columns with NOPM as values
    pivot_df = data.pivot(index='VU', columns='Database', values='NOPM')

    # Plot grouped bar chart
    pivot_df.plot(kind='bar', figsize=(10, 6))

    plt.title('NOPM Comparison Across Databases by VU')
    plt.xlabel('Virtual Users (VU)')
    plt.ylabel('New Orders Per Minute (NOPM)')
    plt.legend(title='Database')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=0)
    plt.tight_layout()

    # Save the plot
    parts = csv_path.split(os.sep)
    user = parts[1]  
    if len(parts) > 3:
        subfolder = parts[2]
        user = f"{user}_{subfolder}"
    base = os.path.basename(csv_path).replace(".csv", ".png")
    output_path = os.path.join('Graphs', f'{user}_{base}')
    plt.savefig(output_path)

print("Graphs generated successfully!!!")