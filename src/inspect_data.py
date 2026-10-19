
from pathlib import Path
import pandas as pd

project_root = Path(__file__).resolve().parent.parent
raw_dir = project_root / "data" / "raw"

# read the FBref file using its two-row header
players = pd.read_excel(
    raw_dir / "player_stats_2024_25.xlsx",
    header=[0, 1]
)

# display the column names
print("PLAYER STATISTICS COLUMNS:")
for column in players.columns:
    print(column)

print("\nFIRST FIVE ROWS:")
print(players.head())