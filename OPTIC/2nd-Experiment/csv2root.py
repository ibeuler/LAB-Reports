import pandas as pd
import uproot
import numpy as np

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
