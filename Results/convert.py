import json
import csv
import os


def convert_json_to_csv(json_file, csv_file):
    with open(json_file, "r") as jf:
        data = json.load(jf)

    csv_data = []
    for timestamp, tpm_value in data.items():
        csv_data.append({"Time": timestamp, "TPM": tpm_value})

    with open(csv_file, "w", newline="") as cf:
        writer = csv.DictWriter(cf, fieldnames=["Time", "TPM"])
        writer.writeheader()
        writer.writerows(csv_data)


def convert_all():
    user_dir = ["Rodrigo", "Silva", "Zé"]
    for user in user_dir:
        input_dir = f"Results/{user}/json"
        output_dir = f"Results/{user}/csv"

        if not os.path.exists(input_dir):
            print(f"Input directory does not exist. Skipping {user}.")
            print()
            continue

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for filename in os.listdir(input_dir):
            if filename.endswith(".json"):
                json_file = os.path.join(input_dir, filename)
                csv_file = os.path.join(output_dir, filename.replace(".json", ".csv"))
                convert_json_to_csv(json_file, csv_file)
                print(f"Converted {user} - {filename} to CSV format.")
        print()


if __name__ == "__main__":
    convert_all()
