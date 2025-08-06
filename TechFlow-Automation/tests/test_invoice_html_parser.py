import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.parsers.invoice_parser import parse_html_invoice

import pandas as pd

file = 'data/invoice_TF-2024-001.html'
data = parse_html_invoice(file)

print("\n--- Extracted Invoice Data ---")
for k, v in data.items():
    print(f"{k}: {v}")

# Export to Excel
df = pd.DataFrame([data])
df.to_excel("invoice_html_export.xlsx", index=False)
print("\nExported to invoice_html_export.xlsx")
