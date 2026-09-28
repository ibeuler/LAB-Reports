import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

if not os.path.exists('plots'):
    os.makedirs('plots')
if not os.path.exists('report/tables'):
    os.makedirs('report/tables')

# Given constants and data
d = 430  # distance to screen in mm
g = 1671  # grating constant in nm (1.671 um)
central_max = 560  # mm

# Measured positions on ruler (mm)
pos_red = 740     # turuncu (orange/red)
pos_green = 730   # yeşil (green)
pos_blue = 700    # mavi (blue)

l_red = abs(pos_red - central_max)
l_green = abs(pos_green - central_max)
l_blue = abs(pos_blue - central_max)

def calc_wavelength(l, d, g):
    return g * l / np.sqrt(d**2 + l**2)

lambda_exp_red = calc_wavelength(l_red, d, g)
lambda_exp_green = calc_wavelength(l_green, d, g)
lambda_exp_blue = calc_wavelength(l_blue, d, g)

data = {
    'Line': ['H_alpha', 'H_beta', 'H_gamma'],
    '2l (m)': [2 * l_red / 1000, 2 * l_green / 1000, 2 * l_blue / 1000],  # 2l in meters
    'n1': [2, 2, 2],
    'n2': [3, 4, 5],
    'lambda_exp (nm)': [lambda_exp_red, lambda_exp_green, lambda_exp_blue],
    'lambda_lit (nm)': [656.28, 486.13, 434.05]
}

df1 = pd.DataFrame(data)
df1['R_exp (m^-1)'] = 1 / ((df1['lambda_exp (nm)'] * 1e-9) * (1/(df1['n1']**2) - 1/(df1['n2']**2)))

df1_export = df1.copy()
df1_export['lambda_exp (nm)'] = df1_export['lambda_exp (nm)'].map('{:.2f}'.format)
df1_export['R_exp (m^-1)'] = df1_export['R_exp (m^-1)'].map('{:.3e}'.format)

df1_export.to_csv('report/tables/table1.csv', index=False)

plt.figure(figsize=(8, 6))
plt.scatter(df1['lambda_lit (nm)'], df1['lambda_exp (nm)'], color='blue', label='Data Points', s=100)

min_val = min(df1['lambda_lit (nm)'].min(), df1['lambda_exp (nm)'].min()) - 20
max_val = max(df1['lambda_lit (nm)'].max(), df1['lambda_exp (nm)'].max()) + 20
plt.plot([min_val, max_val], [min_val, max_val], 'r--', label='Ideal Match')

plt.title('Experimental vs Literature Wavelengths for Hydrogen')
plt.xlabel('Literature Wavelength (nm)')
plt.ylabel('Experimental Wavelength (nm)')
plt.grid(True)
plt.legend()
plt.savefig('plots/wavelength_comparison.png', dpi=300)
