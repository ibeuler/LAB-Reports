import csv
import os
import re

tables_dir = "report/tables"
# Absolute path logic if needed, but relative should work in cwd
tables_dir = r"c:\Users\Pc\Drive’ım (ibrahim.hamed2701@gmail.com)\Academic Archive\Archive & Resources\Academic material\İÜ - Cource Contents\Physics\LAB\ALL\THERMODYNAMICS_AND_STATISTICAL_PHYSICS\2nd_Heat_Capacity_of_Metals\report\tables"

def clean_value(val):
    # Match number at start of string (integer or float)
    # Handle cases like "0.359" or "1046.75"
    # Ignore " degree_Celsius" etc.
    # Be careful with "Brass" (no number at start)
    m = re.match(r"^(-?[\d\.]+)", val)
    if m:
        # Check if it's purely a number followed by space or end
        # "Brass" won't match. "14 degree" will match "14"
        return m.group(1)
    return val

for filename in os.listdir(tables_dir):
    if filename.endswith(".csv"):
        filepath = os.path.join(tables_dir, filename)
        print(f"Cleaning {filename}...")
        rows = []
        with open(filepath, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            try:
                header = next(reader)
            except StopIteration:
                continue
            rows.append(header)
            for row in reader:
                cleaned_row = []
                for i, c in enumerate(row):
                    # Heuristic: if header suggests it is Material, don't clean?
                    # But "Brass" won't match the regex anyway.
                    # Be careful if a material name starts with a number. unlikely.
                    cleaned_row.append(clean_value(c.strip()))
                rows.append(cleaned_row)
        
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(rows)

print("Done.")
