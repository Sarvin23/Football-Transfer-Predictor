from pathlib import Path
import pandas as pd

project_root = Path(__file__).resolve().parent.parent
raw_dir = project_root / "data" / "raw"

players = pd.read_excel(
    raw_dir / "player_stats_2024_25.xlsx",
    header= [0,1],
    engine= "openpyxl"
)

# inspecting raw data
print("Shape:", players.shape)
print("\nMissing values per column:")
print(players.isnull().sum())

# checking for duplicates
print("\nDuplicated rows:", players.duplicated().sum())
print(players.dtypes)

# detecting any missing values
missing_rows = players[players.isnull().any(axis=1)]

print("\nRows with missing values:")
print(missing_rows)

# flatten and rename the columns
players.columns = [
    "rank", "player", "nation", "position", "squad",
    "age", "birth_year", "matches_played", "starts",
    "minutes_played", "minutes_per_90",
    "goals", "assists", "goals_assists",
    "non_penalty_goals", "penalty_goals",
    "penalties_attempted", "yellow_cards", "red_cards",
    "goals_per_90", "assists_per_90",
    "goals_assists_per_90", "non_penalty_goals_per_90",
    "goals_assists_minus_penalties_per_90", "matches"
]

# dropping the matches column since it do not giving anything
players_clean = players.drop(columns=["matches"])

# saving cleaned data
# processed_dir = project_root / "data" / "processed"
# players_clean.to_excel(processed_dir / "player_stats_clean.xlsx")

# cleaned data types
print(players.dtypes)

# summary stats of chosen attributes
summary_table = players[
    ["age", "minutes_played", "matches_played", "goals", "assists", "goals_assists"]
].describe()

# adding range to the table
range_values = summary_table.loc["max"] - summary_table.loc["min"]
summary_table.loc["range"] = range_values
print(summary_table)

# saving as an Excel file
# summary_table.to_excel(processed_dir / "player_stats_summary.xlsx")

# check for any duplicated players
print(players["player"].duplicated())
print(players["player"].nunique())

# check for position and number of players in that pos
print(players["position"].value_counts())