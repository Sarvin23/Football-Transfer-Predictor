from pathlib import Path
import pandas as pd

project_root = Path(__file__).resolve().parent.parent
processed_dir = project_root / "data" / "processed"

# Load the saved datasets
players_combined = pd.read_csv(
    processed_dir / "player_stats_combined.csv"
)

matched_transfers_unique = pd.read_csv(
    processed_dir / "matched_transfers_clean.csv"
)

# Selecting the transfer columns to include
transfer_columns = [
    "player_name",
    "club",
    "window",
    "movement",
    "position",
    "pos",
    "market_value",
    "dealing_club",
    "dealing_country",
    "fee",
    "is_loan"
]

transfer_selected = matched_transfers_unique[transfer_columns]

# merging the data
merged_data = players_combined.merge(
    transfer_selected,
    left_on="player",
    right_on="player_name",
    how="inner",
    validate="one_to_one"
)

print("Merged dataset shape:", merged_data.shape)

# saving the data to Excel file
# merged_data.to_csv(
#     processed_dir / "player_transfer_dataset.csv",
#     index=False
# )