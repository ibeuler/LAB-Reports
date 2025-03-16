import pandas as pd
import ROOT
from array import array

df = pd.read_csv("data_part_1.csv")


f = ROOT.TFile("data.root", "RECREATE")
tree = ROOT.TTree("tree", "Data from Pandas")


branches = {col: array('f', [0]) for col in df.columns}  
for col in df.columns:
    tree.Branch(col, branches[col], f"{col}/F")  

for _, row in df.iterrows():
    for col in df.columns:
        branches[col][0] = row[col]
    tree.Fill()

tree.Write()
f.Close()

