import pandas as pd

# Load dataset
df = pd.read_csv("data/sales.csv")

print("First 5 rows:")
print(df.head())


print("\nDataset Info:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())

# Convert date column
df["Date"] = pd.to_datetime(df["Date"])

# Make column names lowercase
df.columns = df.columns.str.lower()

# Save cleaned dataset
df.to_csv("data/clean_sales.csv", index=False)

print("\nCleaned dataset saved successfully!")