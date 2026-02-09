import pandas as pd
from pathlib import Path

# anchor paths to project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]
csv_path = PROJECT_ROOT / "data" / "raw"

file_name = "appearances.csv"  # <-- change this
df = pd.read_csv(csv_path / file_name, nrows=0)
print("Columns:")
for c in df.columns:
    print("-", repr(c))
