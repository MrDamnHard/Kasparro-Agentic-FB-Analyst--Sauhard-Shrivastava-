from src.agents.evaluator_agent import EvaluatorAgent

def test_numeric_evaluation_alignment():
    evaluator = EvaluatorAgent()

    hypothesis = {
        "reason": "CTR improved which increased ROAS",
        "evidence": "CTR up, ROAS up",
        "confidence": 0.7
    }

    metrics = {
        "ctr": {"change": 0.01},
        "roas": {"change": 1.0},
        "cpc": {"change": -0.1},
        "conversion_rate": {"change": 0.0},
        "impressions": {"change": 2000},
        "spend": {"change": 30},
        "drift": {}
    }

    drift = {
        "ctr": {"z_score": 3.1},
        "roas": {"z_score": 2.0}
    }

    score = evaluator._evaluate_numeric_alignment(hypothesis, metrics, drift)
    assert 0.3 <= score <= 1.0  # should be boosted by CTR alignment


def test_evaluator_validation():
    evaluator = EvaluatorAgent()

    metrics = {
        "ctr": {"change": 0.01},
        "roas": {"change": 1.0},
        "cpc": {"change": -0.05},
        "conversion_rate": {"change": 0.02},
        "impressions": {"change": 10000},
        "spend": {"change": 20},
        "drift": {}
    }

    insights = {
        "hypotheses": [
            {
                "reason": "CTR improved",
                "evidence": "CTR increase was observed",
                "confidence": 0.8
            }
        ]
    }

    validated = evaluator.validate(metrics, insights)
    assert len(validated["validated_hypotheses"]) == 1
    assert validated["validated_hypotheses"][0]["validated"] is True
