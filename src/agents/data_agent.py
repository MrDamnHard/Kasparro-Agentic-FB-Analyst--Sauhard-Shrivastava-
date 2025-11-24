import pandas as pd

class DataAgent:
    """
    Loads dataset and produces summary metrics used by the rest of the agents.
    """

    def __init__(self, path="data/raw_dataset.csv"):
        self.path = path

    def load_data(self):
        df = pd.read_csv(self.path)

        # Normalize
        df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.sort_values(by=["adset_name", "date"])

        # Fill numeric NaNs
        num_cols = ["spend", "impressions", "clicks", "ctr", "purchases", "revenue", "roas"]
        for col in num_cols:
            if col in df.columns:
                df[col] = df[col].fillna(0)

        # Derived metrics
        df["cpc"] = df["spend"] / df["clicks"].replace(0, 1)
        df["cpm"] = df["spend"] / (df["impressions"].replace(0, 1) / 1000)
        df["conversion_rate"] = df["purchases"] / df["clicks"].replace(0, 1)
        df["profit"] = df["revenue"] - df["spend"]

        return df

    # -----------------------------------------------------
    # NEW FUNCTION → REQUIRED BY run.py
    # -----------------------------------------------------
    def get_summary_metrics(self, df):
        """Calculate last 7 days vs previous 7 days performance."""
        df = df.sort_values("date")

        if len(df) < 14:
            raise ValueError("Dataset must contain at least 14 days of data.")

        last7 = df.tail(7)
        prev7 = df.tail(14).head(7)

        def summarize(col):
            return {
                "last7": round(last7[col].mean(), 6),
                "prev7": round(prev7[col].mean(), 6),
                "change": round(last7[col].mean() - prev7[col].mean(), 6)
            }

        summary = {
            "spend": summarize("spend"),
            "impressions": summarize("impressions"),
            "clicks": summarize("clicks"),
            "ctr": summarize("ctr"),
            "cpc": summarize("cpc"),
            "conversion_rate": summarize("conversion_rate"),
            "roas": summarize("roas"),
            "profit": summarize("profit")
        }

        return summary

    # -----------------------------------------------------
    # Low CTR creative finder (used by CreativeAgent)
    # -----------------------------------------------------
    def get_low_ctr_creatives(self, df, threshold=0.01):
        return df[df["ctr"] < threshold][[
            "campaign_name",
            "adset_name",
            "creative_message",
            "ctr",
            "creative_type"
        ]].to_dict(orient="records")
