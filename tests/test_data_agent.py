import pandas as pd
from src.agents.data_agent import DataAgent

def test_schema_validation():
    df = pd.DataFrame({
        "campaign_name": [],
        "adset_name": [],
        "date": [],
        "spend": [],
        "impressions": [],
        "clicks": [],
        "ctr": [],
        "purchases": [],
        "revenue": [],
        "roas": [],
        "creative_type": [],
        "creative_message": [],
        "audience_type": [],
        "platform": [],
        "country": []
    })

    agent = DataAgent()
    missing = agent.validate_schema(df)
    assert missing == []   # should have no missing columns


def test_summary_metrics_basic():
    # 14 rows needed for last7 vs prev7
    df = pd.DataFrame({
        "date": pd.date_range("2024-01-01", periods=14),
        "spend": [10] * 14,
        "impressions": [1000] * 14,
        "clicks": [50] * 14,
        "ctr": [0.05] * 14,
        "purchases": [5] * 14,
        "revenue": [100] * 14,
        "roas": [2.0] * 14,
        "campaign_name": ["A"] * 14,
        "adset_name": ["Test"] * 14,
        "creative_type": ["image"] * 14,
        "creative_message": ["test"] * 14,
        "audience_type": ["broad"] * 14,
        "platform": ["facebook"] * 14,
        "country": ["US"] * 14,
    })

    agent = DataAgent()
    metrics = agent.get_summary_metrics(df)

    assert "spend" in metrics
    assert "drift" in metrics
    assert metrics["spend"]["last7"] == 10.0


def test_summary_metrics_insufficient_data():
    df = pd.DataFrame({"date": pd.date_range("2024-01-01", periods=5)})
    agent = DataAgent()

    metrics = agent.get_summary_metrics(df)
    assert metrics == {}  # not enough rows
