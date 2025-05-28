import pandas as pd
import uproot
import numpy as np
import argparse

"""
USAGE: 
$ python3 csv2root.py --file DATA/Table_Data.csv
ROOT file saved as DATA/Table_Data.root
"""

def csv2ROOT(FileRelativePath):
	# Step 1: Read CSV file
	csv_file = FileRelativePath
	df = pd.read_csv(csv_file)

	# Step 2: Convert DataFrame to a NumPy structured array
	array = np.core.records.fromarrays(df.to_numpy().T, names=",".join(df.columns))

	# Step 3: Save to ROOT file
	root_file = FileRelativePath[:-3] + "root"
	with uproot.recreate(root_file) as f:
		f["tree"] = array  # Create a tree named "tree"
	
	print(f"ROOT file saved as {root_file}")

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Convert CSV to ROOT file.")
	parser.add_argument("--file", required=True, help="Path to the input CSV file.")
	args = parser.parse_args()

	csv2ROOT(args.file)
	