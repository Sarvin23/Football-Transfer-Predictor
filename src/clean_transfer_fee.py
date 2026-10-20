from pathlib import Path
import pandas as pd
from openpyxl.utils.datetime import to_excel

from src.clean_player_stats import players_clean

project_root = Path(__file__).resolve().parent.parent
raw_dir = project_root / "data" / "raw"

transfer_fee = pd.read_csv(
    raw_dir / "transfer_fees.csv"
)

# checking the shape of the data
print("Dataset shape :", transfer_fee.shape)
print("\nMissing values per column:")
print(transfer_fee.isnull().sum())

# checking for duplicates
print("\nDuplicate rows:", transfer_fee.duplicated().sum())
print(transfer_fee.dtypes) # initial checking

# checking which player are missing with the market value
print(transfer_fee[transfer_fee["market_value"].isnull()][["player_name", "market_value"]])

# checking which player are missing with the fees
print(transfer_fee[transfer_fee["fee"].isnull()][["player_name", "market_value", "fee", "is_loan", "movement"]])


# dropping the players with missing fees and market values
transfer_fee_clean = transfer_fee[
    (transfer_fee["fee"].notnull()) &
    (transfer_fee["market_value"].notnull())
]

# saving cleaned data
processed_dir = project_root / "data" / "processed"
transfer_fee_clean.to_excel(processed_dir / "transfer_fee_clean.xlsx")

# print(transfer_fee_clean.isnull().sum())
# print(transfer_fee_clean["season"].value_counts())
# print(transfer_fee_clean["window"].value_counts(dropna=False))
# print(transfer_fee_clean["club"].nunique())
# print(transfer_fee_clean["club"].unique())
# print(transfer_fee_clean["player_name"].isin(players_clean["player"]).sum())
# print((~transfer_fee_clean["player_name"].isin(players_clean["player"])).sum())