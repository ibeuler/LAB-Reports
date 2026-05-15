import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import re

# Suppress warnings
import warnings
warnings.filterwarnings('ignore')

print("=" * 70)
print("LAB REPORT UPDATE SCRIPT - Heat Insulation and Conduction (Exp 5)")
print("=" * 70)

# Setup paths
EXP_DIR = Path(".")
ANALYSIS_DIR = EXP_DIR / "Analysis"
PLOTS_DIR = EXP_DIR / "plots"
REPORT_DIR = EXP_DIR / "report"
TABLES_DIR = REPORT_DIR / "tables"
DATA_DIR = EXP_DIR / "DATA"

TABLES_DIR.mkdir(parents=True, exist_ok=True)

print(f"\nCurrent directory: {EXP_DIR.resolve()}")
print(f"Plots directory exists: {PLOTS_DIR.exists()}")
print(f"Data directory exists: {DATA_DIR.exists()}")
print(f"Tables directory exists: {TABLES_DIR.exists()}")

# Load the notebook
nb_path = ANALYSIS_DIR / "calculations.ipynb"
print(f"\nReading notebook: {nb_path}")
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

print(f"Notebook has {len(nb['cells'])} cells")

# Helper function for 3 significant figures
def format_3sf(value):
    """Format a number to 3 significant figures"""
    if isinstance(value, str):
        return value
    if pd.isna(value) or value == 0:
        return value
    return float(f'{float(value):.3g}')

# Read DATA CSVs
print("\n" + "=" * 70)
print("LOADING DATA FILES")
print("=" * 70)

df_table1 = pd.read_csv(DATA_DIR / "table1.csv")
df_table2 = pd.read_csv(DATA_DIR / "table2.csv")
df_table3 = pd.read_csv(DATA_DIR / "table3.csv")

print(f"\nTable 1 shape: {df_table1.shape}")
print(f"Table 1 columns: {list(df_table1.columns)}")
print(df_table1.head(2))

print(f"\nTable 2 shape: {df_table2.shape}")
print(f"Table 2 columns: {list(df_table2.columns)}")
print(df_table2.head(2))

print(f"\nTable 3 shape: {df_table3.shape}")
print(f"Table 3 columns: {list(df_table3.columns)}")
print(df_table3.head(2))

# Format all numeric columns to 3 sig figs
for df in [df_table1, df_table2, df_table3]:
    for col in df.columns:
        if df[col].dtype in ['float64', 'int64']:
            df[col] = df[col].apply(format_3sf)

# Save formatted CSV tables
table1_path = TABLES_DIR / "table1_formatted.csv"
table2_path = TABLES_DIR / "table2_formatted.csv"
table3_path = TABLES_DIR / "table3_formatted.csv"

df_table1.to_csv(table1_path, index=False)
df_table2.to_csv(table2_path, index=False)
df_table3.to_csv(table3_path, index=False)

print(f"\nSaved formatted tables:")
print(f"  - {table1_path}")
print(f"  - {table2_path}")
print(f"  - {table3_path}")

print("\n" + "=" * 70)
print("SCRIPT COMPLETED")
print("=" * 70)
