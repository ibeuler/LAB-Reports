"""Calculate Millikan Table 2 values from Table 1 measurements."""

import csv
import math
from pathlib import Path


C1 = 2.73e-11
C2 = 6.37e-5


def calculate_row(row: dict[str, str]) -> dict[str, str]:
    voltage = float(row["voltage_V"])
    ascent_time = float(row["ascent_time_s"])
    descent_time = float(row["descent_time_s"])
    ascent_distance = float(row["ascent_distance_m"])
    descent_distance = float(row["descent_distance_m"])

    # Report: v1 is the falling velocity, v1 = s2 / t2.
    v1 = descent_distance / descent_time
    # Report: v2 is the rising velocity, v2 = s1 / t1.
    v2 = ascent_distance / ascent_time
    # Report: r = C2 * sqrt(|v1 - v2|).
    velocity_difference = abs(v1 - v2)
    # Report: Q = C1 * (v1 + v2) / U * sqrt(|v1 - v2|).
    charge = C1 * (v1 + v2) / voltage * math.sqrt(velocity_difference)
    radius = C2 * math.sqrt(velocity_difference)

    return {
        "voltage_V": f"{voltage:.0f}",
        "v1_m_per_s": f"{v1:.1e}",
        "v2_m_per_s": f"{v2:.1e}",
        "charge_C": f"{charge:.1e}",
        "radius_m": f"{radius:.1e}",
    }


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    input_path = project_root / "data" / "raw" / "table1_measurements.csv"
    output_path = project_root / "data" / "processed" / "table2_calculations.csv"

    with input_path.open(newline="") as input_file:
        rows = csv.DictReader(input_file)
        results = [calculate_row(row) for row in rows]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)


if __name__ == "__main__":
    main()