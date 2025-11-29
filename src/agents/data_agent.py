import pandas as pd
import numpy as np
import time
from typing import Optional, Dict, Any, List
from src.utils.logger import AgentLogger

REQUIRED_COLUMNS = [
    "campaign_name", "adset_name", "date",
    "spend", "impressions", "clicks",
    "ctr", "purchases", "revenue", "roas",
    "creative_type", "creative_message",
    "audience_type", "platform", "country"
]


class DataAgent:
    """
    Production-grade DataAgent with:
    - schema validation with ERROR logs
    - safe dtype/NA handling
    - derived metrics (CPC, CVR)
    - last7 vs prev7 summary
    - advanced drift detection
    - runtime logging for each operation
    """

    def __init__(self, data_path: str = "data/raw_dataset.csv"):
        self.data_path = data_path
        self.logger = AgentLogger()

    # -----------------------------------------------------
    # Schema validation
    # -----------------------------------------------------
    def validate_schema(self, df: pd.DataFrame) -> List[str]:
        missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        return missing

    # -----------------------------------------------------
    # Load & preprocess
    # -----------------------------------------------------
    def load_data(self) -> Optional[pd.DataFrame]:
        start = time.time()

        try:
            df = pd.read_csv(self.data_path)
        except Exception as e:
            self.logger.log_error(
                "DataAgent.load_data",
                f"CSV read error: {str(e)}",
                {"path": self.data_path}
            )
            return None

        df.columns = [c.lower().strip().replace(" ", "_") for c in df.columns]
        df["date"] = pd.to_datetime(df.get("date"), errors="coerce")

        # Schema validation
        missing = self.validate_schema(df)
        if missing:
            self.logger.log_error(
                "DataAgent.load_data",
                "Missing required columns",
                {"missing": missing}
            )
            return None

        # Fill numeric NA
        fill_defaults = {
            "spend": 0.0, "impressions": 0.0, "clicks": 0.0,
            "purchases": 0.0, "revenue": 0.0, "roas": 0.0, "ctr": 0.0
        }
        df = df.fillna(fill_defaults)

        # Ensure types
        for col in fill_defaults.keys():
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)

        df = df.sort_values("date").reset_index(drop=True)

        # Derived metrics
        EPS = 1e-6
        df["cpc"] = df["spend"] / (df["clicks"] + EPS)
        df["conversion_rate"] = df["purchases"] / (df["clicks"] + EPS)

        self.logger.log_runtime(
            "DataAgent.load_data",
            start,
            {"rows": len(df), "status": "success"}
        )

        return df

    # -----------------------------------------------------
    # Summary metrics (7-day comparison)
    # -----------------------------------------------------
    def get_summary_metrics(self, df: Optional[pd.DataFrame]) -> Dict[str, Any]:
        start = time.time()

        if df is None:
            self.logger.log_error(
                "DataAgent.get_summary_metrics",
                "df is None"
            )
            return {}

        if len(df) < 14:
            self.logger.log_error(
                "DataAgent.get_summary_metrics",
                "Insufficient rows (<14)",
                {"rows": len(df)}
            )
            return {}

        last7 = df.tail(7)
        prev7 = df.tail(14).head(7)

        def extract(col):
            return {
                "last7": float(round(last7[col].mean(), 6)),
                "prev7": float(round(prev7[col].mean(), 6)),
                "change": float(round(last7[col].mean() - prev7[col].mean(), 6)),
            }

        metrics_list = ["spend", "impressions", "clicks", "ctr",
                        "cpc", "conversion_rate", "roas"]

        metrics = {col: extract(col) for col in metrics_list}

        drift = self.detect_drift(last7, prev7)
        metrics["drift"] = drift

        self.logger.log_runtime(
            "DataAgent.get_summary_metrics",
            start,
            {"metrics_computed": True}
        )

        return metrics

    # -----------------------------------------------------
    # Drift detection
    # -----------------------------------------------------
    def detect_drift(self, last7: pd.DataFrame, prev7: pd.DataFrame) -> Dict[str, Any]:
        start = time.time()

        drift_results: Dict[str, Any] = {}
        metrics_for_drift = ["spend", "ctr", "cpc", "impressions", "roas", "conversion_rate"]
        EPS = 1e-6

        for metric in metrics_for_drift:
            m_last = float(last7[metric].mean())
            m_prev = float(prev7[metric].mean())
            sd_prev = float(prev7[metric].std())

            if sd_prev == 0.0:
                z = 0.0 if m_last == m_prev else float("inf")
            else:
                z = (m_last - m_prev) / sd_prev

            pct_change = ((m_last - m_prev) / (m_prev + EPS)) * 100

            if abs(z) == float("inf") or abs(z) > 3.0:
                severity = "high"
            elif abs(z) > 2.0:
                severity = "moderate"
            else:
                severity = "low"

            drift_results[metric] = {
                "severity": severity,
                "z_score": None if z == float("inf") else round(z, 3),
                "change_pct": round(pct_change, 2),
                "last7": round(m_last, 6),
                "prev7": round(m_prev, 6),
            }

        high_drifts = [k for k, v in drift_results.items() if v["severity"] == "high"]
        drift_results["_summary"] = {
            "num_high_drifts": len(high_drifts),
            "high_drifts": high_drifts
        }

        self.logger.log_runtime(
            "DataAgent.detect_drift",
            start,
            {"drift_metrics": len(drift_results)}
        )

        return drift_results

    # -----------------------------------------------------
    # Low-CTR creatives
    # -----------------------------------------------------
    def get_low_ctr_creatives(self, df: Optional[pd.DataFrame], threshold=0.01):
        start = time.time()

        if df is None:
            self.logger.log_error(
                "DataAgent.get_low_ctr_creatives",
                "df is None"
            )
            return []

        df["ctr"] = pd.to_numeric(df["ctr"].fillna(0), errors="coerce").fillna(0)
        low_df = df[df["ctr"] < threshold]
        creatives = low_df[["campaign_name", "adset_name", "creative_message", "ctr"]].to_dict("records")

        self.logger.log_runtime(
            "DataAgent.get_low_ctr_creatives",
            start,
            {"count": len(creatives)}
        )

        return creatives
