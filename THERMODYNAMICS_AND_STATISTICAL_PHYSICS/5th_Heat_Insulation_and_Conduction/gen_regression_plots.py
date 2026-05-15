import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from pathlib import Path

print("Generating regression analysis plots...")
print("="*70)

# Create regression plots
def plot_with_regression(x_data, y_data, title, xlabel, ylabel, savepath, alpha_reg=0.7):
    """Plot data with regression line and equation"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Convert to numpy arrays and numeric types
    x_data = pd.to_numeric(x_data, errors='coerce').values
    y_data = pd.to_numeric(y_data, errors='coerce').values
    
    # Remove NaN values
    mask = ~(np.isnan(x_data) | np.isnan(y_data))
    x_clean = x_data[mask]
    y_clean = y_data[mask]
    
    if len(x_clean) < 2:
        ax.scatter(x_data[~np.isnan(x_data)], y_data[~np.isnan(y_data)])
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.grid(True, alpha=0.3)
        fig.savefig(savepath, dpi=120, bbox_inches='tight')
        plt.close(fig)
        print(f"  (Insufficient data)")
        return None
    
    # Perform linear regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(x_clean, y_clean)
    x_line = np.array([x_clean.min(), x_clean.max()])
    y_line = slope * x_line + intercept
    
    # Plot
    ax.scatter(x_clean, y_clean, s=100, alpha=0.6, label='Data', color='#1f77b4')
    ax.plot(x_line, y_line, 'r-', linewidth=2.5, alpha=alpha_reg, label='Linear fit')
    
    # Add equation and R²
    eq_text = f'y = {slope:.3g}x + {intercept:.3g}\nR² = {r_value**2:.3f}'
    ax.text(0.05, 0.95, eq_text, transform=ax.transAxes, 
            fontsize=11, verticalalignment='top', family='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.9))
    
    ax.set_title(title, fontsize=13, fontweight='bold')
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='lower right', fontsize=10)
    
    fig.savefig(savepath, dpi=120, bbox_inches='tight')
    plt.close(fig)
    
    return {'slope': f'{slope:.3g}', 'intercept': f'{intercept:.3g}', 'r2': f'{r_value**2:.3f}'}

# Read measurement data for regression plots
heating_data = pd.read_csv("report/tables/heating_measurements_table2.csv")
illum_w_data = pd.read_csv("report/tables/illumination_w_measurements_table4.csv")
illum_g_data = pd.read_csv("report/tables/illumination_g_measurements_table4.csv")

print(f"Heating data columns: {list(heating_data.columns)}")
print(f"Illum W data columns: {list(illum_w_data.columns)}")
print(f"Illum G data columns: {list(illum_g_data.columns)}")

PLOTS_DIR = Path("plots")
PLOTS_DIR.mkdir(exist_ok=True)

# Plot 1: Heating phase - air inside temperature vs time
print("\n1. Heating air temperature vs time")
stats_heating_air = plot_with_regression(
    heating_data["time_min"],
    heating_data["air_in_C"],
    "Heating Phase: Indoor Air Temperature vs Time",
    "Time (min)",
    "Temperature (°C)",
    PLOTS_DIR / "heating_air_temp_regression.png"
)
print(f"   → {stats_heating_air}")

# Plot 2: Heating phase - wood inside temperature vs time
print("\n2. Heating wood temperature vs time")
stats_heating_wood = plot_with_regression(
    heating_data["time_min"],
    heating_data["wood_in_C"],
    "Heating Phase: Wood Surface (Inside) Temperature vs Time",
    "Time (min)",
    "Temperature (°C)",
    PLOTS_DIR / "heating_w_temp_regression.png"
)
print(f"   → {stats_heating_wood}")

# Plot 3: Heating phase - glass inside temperature vs time
print("\n3. Heating glass temperature vs time")
stats_heating_glass = plot_with_regression(
    heating_data["time_min"],
    heating_data["glass_in_C"],
    "Heating Phase: Glass Surface (Inside) Temperature vs Time",
    "Time (min)",
    "Temperature (°C)",
    PLOTS_DIR / "heating_g_temp_regression.png"
)
print(f"   → {stats_heating_glass}")

# Plot 4: Illumination Wood - inside temperature vs time
print("\n4. Illumination wood temperature vs time")
stats_illum_w = plot_with_regression(
    illum_w_data["time_min"],
    illum_w_data["wood_in_C"],
    "Illumination (Wood): Inside Surface Temperature vs Time",
    "Time (min)",
    "Temperature (°C)",
    PLOTS_DIR / "illumination_w_temp_regression.png"
)
print(f"   → {stats_illum_w}")

# Plot 5: Illumination Glass - inside temperature vs time (exclude NaN)
print("\n5. Illumination glass temperature vs time")
glass_data_clean = illum_g_data[illum_g_data["glass_in_C"].notna()]
if len(glass_data_clean) > 1:
    stats_illum_g = plot_with_regression(
        glass_data_clean["time_min"],
        glass_data_clean["glass_in_C"],
        "Illumination (Glass): Inside Surface Temperature vs Time",
        "Time (min)",
        "Temperature (°C)",
        PLOTS_DIR / "illumination_g_temp_regression.png"
    )
    print(f"   → {stats_illum_g}")

print("\n" + "="*70)
print("✓ All regression plots generated successfully!")
print("="*70)

