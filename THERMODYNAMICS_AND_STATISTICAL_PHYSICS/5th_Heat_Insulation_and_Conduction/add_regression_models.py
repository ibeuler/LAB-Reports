import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from pathlib import Path

# Read the existing notebook
with open("Analysis/calculations.ipynb", 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Create a new code cell with regression model enhancements
regression_code = '''# ENHANCED: Add regression models to all plots
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from pathlib import Path

# Create regression plots
def plot_with_regression(x_data, y_data, title, xlabel, ylabel, savepath, alpha_reg=0.7):
    """Plot data with regression line and equation"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Remove NaN values
    mask = ~(np.isnan(x_data) | np.isnan(y_data))
    x_clean = x_data[mask]
    y_clean = y_data[mask]
    
    if len(x_clean) < 2:
        ax.scatter(x_data, y_data)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.grid(True, alpha=0.3)
        fig.savefig(savepath, dpi=120, bbox_inches='tight')
        plt.close(fig)
        return
    
    # Perform linear regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(x_clean, y_clean)
    x_line = np.array([x_clean.min(), x_clean.max()])
    y_line = slope * x_line + intercept
    
    # Plot
    ax.scatter(x_clean, y_clean, s=100, alpha=0.6, label='Data', color='#1f77b4')
    ax.plot(x_line, y_line, 'r-', linewidth=2, alpha=alpha_reg, label='Linear fit')
    
    # Add equation and R²
    eq_text = f'y = {slope:.4g}x + {intercept:.4g}\nR² = {r_value**2:.4f}'
    ax.text(0.05, 0.95, eq_text, transform=ax.transAxes, 
            fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.legend(loc='lower right')
    
    fig.savefig(savepath, dpi=120, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved: {savepath}")

# Format to 3 sig figs
def fmt3sf(val):
    if isinstance(val, str) or pd.isna(val):
        return val
    if val == 0:
        return 0
    return float(f'{float(val):.3g}')

# Read measurement data for regression plots
heating_data = pd.read_csv("../report/tables/heating_measurements_table2.csv")
illum_w_data = pd.read_csv("../report/tables/illumination_w_measurements_table4.csv")
illum_g_data = pd.read_csv("../report/tables/illumination_g_measurements_table4.csv")

# Create regression plots for key parameters
PLOTS_DIR = Path("../plots")

# Heating phase: time vs air inside temperature
plot_with_regression(
    heating_data["time_min"].values,
    heating_data["air_in_C"].values,
    "Heating Phase: Indoor Air Temperature vs Time",
    "Time (min)",
    "Temperature (°C)",
    PLOTS_DIR / "heating_air_temp_regression.png"
)

# Illumination Wood: time vs inside temperature
plot_with_regression(
    illum_w_data["time_min"].values,
    illum_w_data["wood_in_C"].values,
    "Illumination (Wood): Inside Surface Temp vs Time",
    "Time (min)",
    "Temperature (°C)",
    PLOTS_DIR / "illumination_w_temp_regression.png"
)

# Illumination Glass: time vs inside temperature  
glass_data_clean = illum_g_data[illum_g_data["glass_in_C"].notna()]
if len(glass_data_clean) > 1:
    plot_with_regression(
        glass_data_clean["time_min"].values,
        glass_data_clean["glass_in_C"].values,
        "Illumination (Glass): Inside Surface Temp vs Time",
        "Time (min)",
        "Temperature (°C)",
        PLOTS_DIR / "illumination_g_temp_regression.png"
    )

print("\\nRegression model plots created successfully!")
'''

# Add this as a new cell at the end
new_cell = {
    "cell_type": "code",
    "execution_count": None,
    "id": "regression_models",
    "metadata": {},
    "outputs": [],
    "source": regression_code.split('\n')
}

nb['cells'].append(new_cell)

# Save the modified notebook
with open("Analysis/calculations_updated.ipynb", 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("✓ Created enhanced notebook with regression models")
print(f"✓ Total cells: {len(nb['cells'])}")
print("✓ New regression plot cell added")
print("\nNotebook saved to: Analysis/calculations_updated.ipynb")

