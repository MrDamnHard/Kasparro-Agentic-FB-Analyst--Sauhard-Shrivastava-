import json
from src.utils.llm import LLM

class RecommendationAgent:
    """
    Converts insights + metrics into actionable next steps.
    """

    def __init__(self):
        self.llm = LLM()

        self.prompt = """
You are a senior Growth Marketing Strategist.

Based on the insights and metrics below, generate 5–8 clear,
actionable recommendations for improving ROAS and CTR.

### INPUT METRICS
{METRICS}

### INSIGHTS
{INSIGHTS}

---

### OUTPUT FORMAT (STRICT JSON)
{
  "recommendations": [
    ""
  ]
}

Return ONLY valid JSON.
"""

    def generate(self, metrics, insights):
        prompt = (
            self.prompt
            .replace("{METRICS}", json.dumps(metrics, indent=2))
            .replace("{INSIGHTS}", json.dumps(insights, indent=2))
        )

        result = self.llm.generate_json(prompt)

        if not isinstance(result, dict) or "recommendations" not in result:
            return {
                "recommendations": [
                    "Introduce 2 new creatives to counter possible fatigue.",
                    "Increase budget on high-ROAS adsets.",
                    "Lower spend on low-performing audiences.",
                ]
            }

        return result
