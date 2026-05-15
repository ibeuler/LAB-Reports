import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("COMPREHENSIVE LAB REPORT UPDATE")
print("Heat Insulation and Conduction - Experiment 5")
print("=" * 80)

# Paths
EXP_DIR = Path(".")
TABLES_DIR = EXP_DIR / "report" / "tables"
PLOTS_DIR = EXP_DIR / "plots"
DATA_DIR = EXP_DIR / "DATA"

# 3 sig figs formatter
def fmt3sf(val):
    if isinstance(val, str) or pd.isna(val):
        return val
    if val == 0:
        return 0
    return float(f'{float(val):.3g}')

# List existing table CSVs
print("\n" + "=" * 80)
print("STEP 1: INVENTORY EXISTING TABLES")
print("=" * 80)
table_files = sorted(TABLES_DIR.glob("*.csv"))
for tf in table_files:
    df = pd.read_csv(tf)
    print(f"\n{tf.name}:")
    print(f"  Shape: {df.shape}")
    print(f"  Columns: {list(df.columns)[:5]}...")

# Read and format derived parameters
print("\n" + "=" * 80)
print("STEP 2: READ AND FORMAT DERIVED PARAMETERS")
print("=" * 80)

heating_derived = pd.read_csv(TABLES_DIR / "heating_derived_table3.csv")
illum_derived = pd.read_csv(TABLES_DIR / "illumination_derived_table5.csv")

print(f"\nHeating derived (Table 3):")
print(heating_derived)

print(f"\nIllumination derived (Table 5):")
print(illum_derived)

# Format to 3 sig figs
for col in heating_derived.columns:
    if heating_derived[col].dtype in ['float64', 'float32', 'int64', 'int32']:
        heating_derived[col] = heating_derived[col].apply(fmt3sf)

for col in illum_derived.columns:
    if illum_derived[col].dtype in ['float64', 'float32', 'int64', 'int32']:
        illum_derived[col] = illum_derived[col].apply(fmt3sf)

# Save back
heating_derived.to_csv(TABLES_DIR / "heating_derived_table3.csv", index=False)
illum_derived.to_csv(TABLES_DIR / "illumination_derived_table5.csv", index=False)
print("\nFormatted and saved derived parameter tables to 3 sig figs")

# Read and format measurement tables
print("\n" + "=" * 80)
print("STEP 3: FORMAT MEASUREMENT TABLES TO 3 SIG FIGS")
print("=" * 80)

measure_files = [
    "heating_measurements_table2.csv",
    "illumination_w_measurements_table4.csv",
    "illumination_g_measurements_table4.csv"
]

for fname in measure_files:
    fpath = TABLES_DIR / fname
    if fpath.exists():
        df = pd.read_csv(fpath)
        for col in df.columns:
            if df[col].dtype in ['float64', 'float32', 'int64', 'int32']:
                df[col] = df[col].apply(fmt3sf)
        df.to_csv(fpath, index=False)
        print(f"Formatted: {fname}")

# List plots and check for regression
print("\n" + "=" * 80)
print("STEP 4: ANALYZE EXISTING PLOTS")
print("=" * 80)

plot_files = sorted(PLOTS_DIR.glob("*.png"))
print(f"\nFound {len(plot_files)} plot files:")
for pf in plot_files:
    size_kb = pf.stat().st_size / 1024
    print(f"  - {pf.name} ({size_kb:.1f} KB)")

# Read notebook to understand analysis
print("\n" + "=" * 80)
print("STEP 5: EXTRACT NOTEBOOK ANALYSIS")
print("=" * 80)

with open("Analysis/calculations.ipynb", 'r', encoding='utf-8') as f:
    nb = json.load(f)

for i, cell in enumerate(nb['cells']):
    src = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']
    if 'plot_temperatures' in src or 'savefig' in src:
        print(f"\nCell {i} contains plotting code")
        # Show first 200 chars
        print(f"  {src[:200]}...")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print("✓ Inventory of tables complete")
print("✓ Derived parameters formatted to 3 sig figs")
print("✓ Measurement tables formatted to 3 sig figs")
print("✓ Plots identified for regression model addition")
print("✓ Notebook structure analyzed")
print("\nNEXT STEPS:")
print("1. Update plots with regression models and equations")
print("2. Regenerate plots using modified notebook")
print("3. Update report.tex with new content")

