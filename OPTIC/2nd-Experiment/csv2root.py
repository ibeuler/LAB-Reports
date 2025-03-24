import pandas as pd
import uproot
import numpy as np

"""
USAGE: 
... LAB-Reports/OPTIC/2nd-Experiment$ python3

Python 3.10.12 (main, Feb  4 2025, 14:57:36) [GCC 11.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.

>>> import csv2root
>>> csv2root.csv2ROOT(FileRelativePath="DATA/Table_Data.csv")
ROOT file saved as DATA/Table_Data.root
>>> quit()

"""

def csv2ROOT(FileRelativePath="data.csv"):
	# Step 1: Read CSV file
	csv_file = FileRelativePath  # Replace with your CSV file path
	df = pd.read_csv(csv_file)

	# Step 2: Convert DataFrame to a NumPy structured array
	array = np.core.records.fromarrays(df.to_numpy().T, names=",".join(df.columns))

	# Step 3: Save to ROOT file
	root_file = FileRelativePath[:-3]+"root"
	with uproot.recreate(root_file) as f:
	    f["tree"] = array  # Create a tree named "tree"

	print(f"ROOT file saved as {root_file}")
