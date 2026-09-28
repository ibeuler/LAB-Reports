import nbformat as nbf

nb = nbf.v4.new_notebook()

code1 = """import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# Create output directories
if not os.path.exists('../plots'):
    os.makedirs('../plots')
if not os.path.exists('../report/tables'):
    os.makedirs('../report/tables')
"""

code2 = """# Given constants and data
d = 430  # distance to screen in mm
g = 1671  # grating constant in nm (1.671 um)
central_max = 560  # mm

# Measured positions on ruler (mm)
pos_red = 740     # turuncu (orange/red)
pos_green = 730   # yeşil (green)
pos_blue = 700    # mavi (blue)

# Calculate 2l (distance from central maximum)
# Note: The manual says 'read the length 2l on the ruler' which implies measuring between the two first-order maxima.
# But the data provided is the absolute position on the ruler. 
# l is the distance from the central maximum.
l_red = abs(pos_red - central_max)
l_green = abs(pos_green - central_max)
l_blue = abs(pos_blue - central_max)

print(f"l_red: {l_red} mm")
print(f"l_green: {l_green} mm")
print(f"l_blue: {l_blue} mm")
"""

code3 = """# Calculate experimental wavelengths
def calc_wavelength(l, d, g):
    return g * l / np.sqrt(d**2 + l**2)

lambda_exp_red = calc_wavelength(l_red, d, g)
lambda_exp_green = calc_wavelength(l_green, d, g)
lambda_exp_blue = calc_wavelength(l_blue, d, g)

print(f"Experimental Wavelength (Red/H_alpha): {lambda_exp_red:.2f} nm")
print(f"Experimental Wavelength (Green/H_beta): {lambda_exp_green:.2f} nm")
print(f"Experimental Wavelength (Blue/H_gamma): {lambda_exp_blue:.2f} nm")
"""

code4 = """# Table 1 data preparation
# For Hydrogen lines:
# H_alpha: n1=2, n2=3, lambda_lit = 656.28 nm
# H_beta: n1=2, n2=4, lambda_lit = 486.13 nm
# H_gamma: n1=2, n2=5, lambda_lit = 434.05 nm

data = {
    'Line': ['H_alpha', 'H_beta', 'H_gamma'],
    '2l (m)': [2 * l_red / 1000, 2 * l_green / 1000, 2 * l_blue / 1000],  # 2l in meters
    'n1': [2, 2, 2],
    'n2': [3, 4, 5],
    'lambda_exp (nm)': [lambda_exp_red, lambda_exp_green, lambda_exp_blue],
    'lambda_lit (nm)': [656.28, 486.13, 434.05]
}

df1 = pd.DataFrame(data)

# Calculate Rydberg constant for each line
# 1/lambda = R_th * (1/n1^2 - 1/n2^2)
# R_exp = 1 / (lambda_exp * (1/n1^2 - 1/n2^2))
# Note: lambda must be in meters to get R_exp in m^-1
df1['R_exp (m^-1)'] = 1 / ((df1['lambda_exp (nm)'] * 1e-9) * (1/(df1['n1']**2) - 1/(df1['n2']**2)))

# Calculate average Rydberg constant
R_ave = df1['R_exp (m^-1)'].mean()
R_std = df1['R_exp (m^-1)'].std()

print(df1)
print(f"\\nAverage Rydberg Constant: {R_ave:.2e} m^-1 +/- {R_std:.2e} m^-1")

# Export Table 1 to CSV for LaTeX
df1_export = df1.copy()
# Format the columns nicely
df1_export['lambda_exp (nm)'] = df1_export['lambda_exp (nm)'].map('{:.2f}'.format)
df1_export['R_exp (m^-1)'] = df1_export['R_exp (m^-1)'].map('{:.3e}'.format)

df1_export.to_csv('../report/tables/table1.csv', index=False)
"""

code5 = """# Plot experimental vs literature wavelengths
plt.figure(figsize=(8, 6))
plt.scatter(df1['lambda_lit (nm)'], df1['lambda_exp (nm)'], color='blue', label='Data Points', s=100)

# 1:1 line for ideal match
min_val = min(df1['lambda_lit (nm)'].min(), df1['lambda_exp (nm)'].min()) - 20
max_val = max(df1['lambda_lit (nm)'].max(), df1['lambda_exp (nm)'].max()) + 20
plt.plot([min_val, max_val], [min_val, max_val], 'r--', label='Ideal Match')

plt.title('Experimental vs Literature Wavelengths for Hydrogen')
plt.xlabel('Literature Wavelength (nm)')
plt.ylabel('Experimental Wavelength (nm)')
plt.grid(True)
plt.legend()
plt.savefig('../plots/wavelength_comparison.png', dpi=300)
plt.show()
"""

nb['cells'] = [
    nbf.v4.new_markdown_cell("# Importing Requirements"),
    nbf.v4.new_code_cell(code1),
    nbf.v4.new_markdown_cell("# Data Input"),
    nbf.v4.new_code_cell(code2),
    nbf.v4.new_markdown_cell("# Calculations"),
    nbf.v4.new_code_cell(code3),
    nbf.v4.new_code_cell(code4),
    nbf.v4.new_markdown_cell("# Plots"),
    nbf.v4.new_code_cell(code5)
]

with open('Analysis/calculations.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)
