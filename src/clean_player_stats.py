from pathlib import Path
import pandas as pd

project_root = Path(__file__).resolve().parent.parent
raw_dir = project_root / "data" / "raw"

players = pd.read_excel(
    raw_dir / "player_stats_2024_25.xlsx",
    header= [0,1],
    engine= "openpyxl"
)

print("Dataset shape :", players.shape)
print("\nMissing values per column:")
print(players.isnull().sum())

print("\nDuplicate rows:", players.duplicated().sum())
print("\nData types:")
print(players.dtypes)


# Show rows with at least one missing value
missing_rows = players[players.isnull().any(axis=1)]

print("\nRows with missing values:")
print(missing_rows)