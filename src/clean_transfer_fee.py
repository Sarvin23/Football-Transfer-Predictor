from pathlib import Path
import pandas as pd

from src.clean_player_stats import players_clean

project_root = Path(__file__).resolve().parent.parent
raw_dir = project_root / "data" / "raw"

transfer_fee = pd.read_csv(
    raw_dir / "transfer_fees.csv"
)

# inspecting raw data
print("Shape:", transfer_fee.shape)
print("\nMissing values per column:")
print(transfer_fee.isnull().sum())

# checking for duplicates
print("\nDuplicate rows:", transfer_fee.duplicated().sum())
print(transfer_fee.dtypes)

# checking which player are missing with the market value
print(transfer_fee[transfer_fee["market_value"].isnull()][["player_name", "market_value"]])

# checking which player are missing with the fees
print(transfer_fee[transfer_fee["fee"].isnull()]
      [["player_name", "market_value", "fee", "is_loan", "movement"]])

# dropping the players with missing fees and market values
transfer_fee_clean = transfer_fee[
    transfer_fee["fee"].notna() &
    (transfer_fee["fee"] != 0)
].copy()

# checking the cleaned row
print("Rows remaining:", len(transfer_fee_clean))

# saving cleaned data
# processed_dir = project_root / "data" / "processed"
# processed_dir.mkdir(parents=True, exist_ok=True)
# transfer_fee_clean.to_excel(processed_dir / "transfer_fee_clean.xlsx",
#                            index=False
#                            )

# checking which season and the window
print(transfer_fee_clean["season"].value_counts()) # summer 2025
print(transfer_fee_clean["window"].value_counts(dropna=False))

# number of different clubs and names
print(transfer_fee_clean["club"].nunique()) # 20
print(transfer_fee_clean["club"].unique())

# checking how many players are in the both datasets
# (transfer fee and player stats) (84 players)
print(transfer_fee_clean["player_name"].isin(players_clean["player"]).sum())

# counts how many times player occured in the data
print(transfer_fee_clean["player_name"].value_counts().head(20))

# checking movement of the duplicated player
print(
    transfer_fee_clean[
        transfer_fee_clean["player_name"].duplicated(keep=False)
    ][["player_name", "club", "movement", "fee"]]
    .sort_values("player_name")
)

matched_transfers = transfer_fee_clean[
    transfer_fee_clean["player_name"].isin(players_clean["player"])
].copy()

# there are 63 unrepeated players
print("Unique matched players:", matched_transfers["player_name"].nunique())

# checking the counts of movements
print(matched_transfers["movement"].value_counts())

matched_in = matched_transfers[
    matched_transfers["movement"] == "in"
]

matched_out = matched_transfers[
    matched_transfers["movement"] == "out"
]

incoming_players = set(matched_in["player_name"])
outgoing_players = set(matched_out["player_name"])

print("Incoming players with matching outgoing records:")
print(sorted(incoming_players & outgoing_players))

print("\nIncoming players without matching outgoing records:")
print(sorted(incoming_players - outgoing_players))

# removing redundant incoming and outgoing players
incoming = matched_transfers[
    matched_transfers["movement"] == "in"
]

outgoing = matched_transfers[
    matched_transfers["movement"] == "out"
]

incoming_only_players = incoming_players - outgoing_players

matched_transfers_unique = matched_transfers[
    (matched_transfers["movement"] == "out") |
    (
        (matched_transfers["movement"] == "in") &
        (matched_transfers["player_name"].isin(incoming_only_players))
    )
].copy()

print("length:", len(matched_transfers_unique))

# 63 players in total
print("\nMovement counts:")
print(matched_transfers_unique["movement"].value_counts())

# saving the data
#
# processed_dir = project_root / "data" / "processed"
# matched_transfers_unique.to_csv(
#     processed_dir / "matched_transfers_clean.csv",
#     index=False
# )
