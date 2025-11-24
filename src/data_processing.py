import pandas as pd

def load_and_clean_data(path="data/raw_dataset.csv"):
    # 1. Load dataset
    df = pd.read_csv(path)

    # 2. Normalize column names
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # 3. Convert date column to datetime
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # 4. Sort values
    df = df.sort_values(by=["adset_name", "date"])

    # 5. Fill missing values
    num_cols = ["spend", "impressions", "clicks", "ctr", "purchases", "revenue", "roas"]
    for col in num_cols:
        if col in df.columns:
            df[col] = df[col].fillna(0)

    # 6. Remove impossible values (negative spend, negative ROAS, etc.)
    for col in num_cols:
        df = df[df[col] >= 0]

    # 7. Basic derived metrics
    df["cpc"] = df["spend"] / df["clicks"].replace(0, 1)
    df["cpm"] = df["spend"] / (df["impressions"].replace(0, 1) / 1000)
    df["conversion_rate"] = df["purchases"] / df["clicks"].replace(0, 1)
    df["profit"] = df["revenue"] - df["spend"]

    return df
