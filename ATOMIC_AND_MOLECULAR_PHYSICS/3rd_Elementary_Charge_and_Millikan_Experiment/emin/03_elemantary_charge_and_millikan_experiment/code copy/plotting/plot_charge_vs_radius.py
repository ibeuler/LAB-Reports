"""Create the Millikan charge-versus-radius plot from Table 1 data.

The script uses the same equations and constants as the report.  It reads the
measured times and distances from the raw CSV, keeps full precision for the
plot, and saves a PNG that can be included by LaTeX.
"""

import csv
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


# Constants from the report: Q = C1*(v1 + v2)/U*sqrt(|v1 - v2|)
# and r = C2*sqrt(|v1 - v2|).
C1 = 2.73e-11
C2 = 6.37e-5


def read_measurements(input_path: Path) -> list[dict[str, float]]:
    """Calculate unrounded charge and radius values from Table 1."""
    points = []
    with input_path.open(newline="") as input_file:
        for row in csv.DictReader(input_file):
            voltage = float(row["voltage_V"])
            ascent_velocity = float(row["ascent_distance_m"]) / float(row["ascent_time_s"])
            descent_velocity = float(row["descent_distance_m"]) / float(row["descent_time_s"])

            # Report notation: v1 is falling and v2 is rising.
            v1 = descent_velocity
            v2 = ascent_velocity
            velocity_difference = abs(v1 - v2)
            charge = C1 * (v1 + v2) / voltage * math.sqrt(velocity_difference)
            radius = C2 * math.sqrt(velocity_difference)
            points.append({"voltage": voltage, "charge": charge, "radius": radius})
    return points


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    input_path = project_root / "data" / "raw" / "table1_measurements.csv"
    output_path = project_root / "figures" / "plots" / "charge_vs_radius.png"
    points = read_measurements(input_path)

    width, height = 1100, 750
    left, top, right, bottom = 190, 70, 85, 105
    plot_width = width - left - right
    plot_height = height - top - bottom
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    bold_font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    title_font = ImageFont.truetype(bold_font_path, 28)
    axis_font = ImageFont.truetype(bold_font_path, 23)
    tick_font = ImageFont.truetype(font_path, 19)

    # Use fixed 0, 2, 4, 6, 8, 10 ticks in the scaled axis units.
    max_radius = 10e-7
    max_charge = 10e-19

    def coordinates(point: dict[str, float]) -> tuple[float, float]:
        x = left + point["radius"] / max_radius * plot_width
        y = top + plot_height - point["charge"] / max_charge * plot_height
        return x, y

    # Axes and labels.
    draw.line((left, top, left, top + plot_height), fill="black", width=3)
    draw.line((left, top + plot_height, left + plot_width, top + plot_height), fill="black", width=3)
    draw.text((width // 2 - 180, 20), "Millikan charge versus radius", fill="black", font=title_font)
    draw.text((width // 2 - 135, height - 55), "Radius r (10^-7 m)", fill="black", font=axis_font)

    # Rotate the vertical label so the quantity and symbol remain clear.
    y_label = Image.new("RGBA", (300, 45), (255, 255, 255, 0))
    ImageDraw.Draw(y_label).text((0, 0), "Charge Q (10^-19 C)", fill="black", font=axis_font)
    y_label = y_label.rotate(90, expand=True)
    image.paste(y_label, (8, height // 2 - y_label.height // 2), y_label)

    # These guides mark the measured Q values; they are not voltage-specific levels.
    for point in points:
        _, y = coordinates(point)
        dash_length, gap_length = 10, 6
        x = left
        while x < left + plot_width:
            draw.line((x, y, min(x + dash_length, left + plot_width), y),
                      fill="#555555", width=1)
            x += dash_length + gap_length

    # Use one marker style because the manual does not separate points by voltage.
    for point in points:
        x, y = coordinates(point)
        draw.ellipse((x - 8, y - 8, x + 8, y + 8), fill="black", outline="black")

    # Show the fixed scaled ticks on both axes.
    for tick_value in range(0, 11, 2):
        fraction = tick_value / 10
        x = left + fraction * plot_width
        y = top + plot_height - fraction * plot_height
        draw.line((x, top + plot_height, x, top + plot_height + 8), fill="black", width=2)
        draw.line((left - 8, y, left, y), fill="black", width=2)
        draw.text((x - 10, top + plot_height + 12), str(tick_value), fill="black", font=tick_font)
        draw.text((left - 35, y - 11), str(tick_value), fill="black", font=tick_font)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path, dpi=(150, 150))


if __name__ == "__main__":
    main()