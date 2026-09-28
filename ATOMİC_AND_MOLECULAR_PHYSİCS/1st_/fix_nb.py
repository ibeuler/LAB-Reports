import nbformat as nbf
with open('Analysis/calculations.ipynb', 'r', encoding='utf-8') as f:
    nb = nbf.read(f, as_version=4)
for cell in nb.cells:
    if cell.cell_type == 'code' and 'df1_export.to_csv' in cell.source:
        cell.source = cell.source.replace("df1_export.to_csv('../report/tables/table1.csv', index=False)", "df1_export.columns = ['Line', '2l', 'n1', 'n2', 'lambdaExp', 'lambdaLit', 'Rexp']\ndf1_export.to_csv('../report/tables/table1.csv', index=False)")
with open('Analysis/calculations.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)
