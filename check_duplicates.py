import csv
from collections import Counter
import sys
import os

def analyze_column(input_csv, column_name, output_csv='duplicates_report.csv'):
    values = []

    # Read the CSV file
    with open(input_csv, newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        if column_name not in reader.fieldnames:
            raise ValueError(f"Column '{column_name}' not found in CSV headers: {reader.fieldnames}")

        for i, row in enumerate(reader, start=1):
            value = row.get(column_name, '').strip()
            if value:
                values.append(value)
            else:
                print(f"[Row {i}] Warning: Empty value in '{column_name}' column.")

    # Count duplicates
    counter = Counter(values)
    duplicate_values = {val: count for val, count in counter.items() if count > 1}
    unique_count = sum(1 for count in counter.values() if count == 1)

    # Write duplicates to CSV
    with open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow([column_name, 'Count'])
        for val, count in sorted(duplicate_values.items(), key=lambda x: x[1], reverse=True):
            writer.writerow([val, count])

    # Console summary
    print("\n--- Duplicate Analysis Report ---")
    print(f"Total non-empty values: {len(values)}")
    print(f"Unique values:          {unique_count}")
    print(f"Duplicate values:       {len(duplicate_values)}")
    print(f"Duplicate report saved to: {os.path.abspath(output_csv)}\n")

    if duplicate_values:
        print("Top duplicates:")
        for val, count in sorted(duplicate_values.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  '{val}': {count} times")
    else:
        print("No duplicates found.\n")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python check_duplicates.py <input_csv> <column_name>")
    else:
        input_csv = sys.argv[1]
        column_name = sys.argv[2]
        try:
            analyze_column(input_csv, column_name)
        except Exception as e:
            print(f"Error: {e}")
