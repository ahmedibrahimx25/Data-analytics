
# Exploring the NYC Airbnb Market: Data Cleaning and Preparation

import pandas as pd
from datetime import datetime

# 1. Data Loading
# ----------------
df = pd.read_csv('Airbnb_Open_Data.csv')

# 2. Initial Exploration
# ----------------------
print('Data shape:', df.shape)
print('Columns:', df.columns.tolist())
print(df.head())
print(df.info())

# 3. Cleaning Price and Service Fee Columns
# -----------------------------------------
def clean_currency(col):
    """Remove $ and commas, convert to float."""
    return pd.to_numeric(df[col].astype(str).str.replace(r'[$,]', '', regex=True), errors='coerce')

df['price_clean'] = clean_currency('price')
df['service_fee_clean'] = clean_currency('service fee')

# 4. Parsing Last Review Date
# ---------------------------
df['last_review_parsed'] = pd.to_datetime(df['last review'], errors='coerce')

# 5. Remove/Flag Future Dates in Last Review
# ------------------------------------------
now = pd.Timestamp(datetime.now())
df['last_review_valid'] = df['last_review_parsed'].where(df['last_review_parsed'] <= now, pd.NaT)

# 6. Clean String Columns
# -----------------------
def clean_string(col):
    """Trim whitespace and standardize to title case."""
    return df[col].astype(str).str.strip().str.title()

for col in ['neighbourhood group', 'neighbourhood', 'host name']:
    df[col + '_clean'] = clean_string(col)

# 7. Summary Statistics
# ---------------------
print(df[['price_clean', 'service_fee_clean', 'last_review_valid']].describe())
print('Missing values:', df[['price_clean', 'service_fee_clean', 'last_review_valid']].isna().sum())

# 8. Sample of Cleaned Data
# -------------------------
print(df[[
    'NAME', 'host name_clean', 'neighbourhood group_clean', 'neighbourhood_clean',
    'price_clean', 'service_fee_clean', 'last_review_valid'
]].head(10))
