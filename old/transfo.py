import pandas as pd



df = pd.read_excel("data/sales.xlsx")

# numériques
num_cols = [
    "Sales_Amount",
    "Quantity_Sold",
    "Unit_Cost",
    "Unit_Price",
    "Discount"
]
print(df.columns.tolist())

df[num_cols] = df[num_cols].apply(
    pd.to_numeric,
    errors="coerce"
)

df.to_parquet(
    "data/sales.parquet",
    index=False
)


