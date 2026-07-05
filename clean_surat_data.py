import pandas as pd

# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv("surat_uncleaned.csv")

print("Original Shape:", df.shape)

# -----------------------------
# Remove Duplicate Rows
# -----------------------------
df = df.drop_duplicates()

# -----------------------------
# Handle Missing Values
# -----------------------------

# Fill transaction with most frequent value
df["transaction"] = df["transaction"].fillna(df["transaction"].mode()[0])

# Fill status with most frequent value
df["status"] = df["status"].fillna(df["status"].mode()[0])

# Fill floor with "Unknown"
df["floor"] = df["floor"].fillna("Unknown")

# Fill furnishing with "Unknown"
df["furnishing"] = df["furnishing"].fillna("Unknown")

# Fill facing with "Unknown"
df["facing"] = df["facing"].fillna("Unknown")

# Fill description with "Not Available"
df["description"] = df["description"].fillna("Not Available")

# Fill price_per_sqft with its median
df["price_per_sqft"] = pd.to_numeric(
    df["price_per_sqft"].astype(str).str.replace(r"[^\d.]", "", regex=True),
    errors="coerce"
)

df["price_per_sqft"] = df["price_per_sqft"].fillna(
    df["price_per_sqft"].median()
)

# -----------------------------
# Clean Text Columns
# -----------------------------
text_columns = [
    "property_name",
    "areaWithType",
    "transaction",
    "status",
    "floor",
    "furnishing",
    "facing",
    "description"
]

for col in text_columns:
    df[col] = df[col].astype(str).str.strip()

# -----------------------------
# Standardize Text
# -----------------------------
for col in text_columns:
    df[col] = df[col].str.title()

# -----------------------------
# Convert Numeric Columns
# -----------------------------

# Convert square_feet to numeric
df["square_feet"] = df["square_feet"].astype(str).str.strip()
# Remove Remaining Missing Values
# -----------------------------

# -----------------------------
# Reset Index
# -----------------------------
df = df.reset_index(drop=True)

# -----------------------------
# Round Numeric Columns
# -----------------------------
numeric_columns = [
    "square_feet",
    "price_per_sqft"
]

df[numeric_columns] = df[numeric_columns].round(2)

# -----------------------------
# Save Clean Dataset
# -----------------------------
df.to_csv(
    "surat_cleaned.csv",
    index=False,
    encoding="utf-8"
)

print("\nCleaning Completed Successfully!")
print("Final Shape:", df.shape)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nFirst 5 Rows:")
print(df.head())

print("\nData Types:")
print(df.dtypes)

print("\nDataset Information:")
df.info()