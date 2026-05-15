# Report Update Summary

## File Status
echo "=== REPORT FILES ==="
dir report/ | where {$_.Name -match "report\.(tex|pdf|log)$"} | format-table Name, Length, LastWriteTime -AutoSize

echo "`n=== CSV TABLES ==="
dir report/tables/*.csv -Name

echo "`n=== REGRESSION PLOTS ==="
dir plots/*regression*.png -Name

echo "`n=== ORIGINAL ANALYSIS PLOTS ==="
dir plots/*temperatures*.png, plots/*heat*.png -Name | where {$_ -notmatch "regression"}

