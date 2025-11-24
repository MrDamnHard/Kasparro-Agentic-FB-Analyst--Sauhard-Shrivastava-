import json
from src.utils.llm import LLM


class InsightAgent:
    """
    Uses LLM (Ollama) to generate hypotheses about ROAS, CTR, CPC etc.
    """

    def __init__(self):
        self.llm = LLM()
        # Load prompt template
        with open("prompts/insight_prompt.md", "r") as f:
            self.base_prompt = f.read()

    def generate(self, metric_summary: dict):
        """
        Generate hypotheses using the LLM, based only on the metric summary.
        """

        prompt = (
            self.base_prompt
            + "\n\n"
            + "## Metric Summary (last 7 vs previous 7)\n"
            + json.dumps(metric_summary, indent=2)
        )

        # LLM outputs structured hypotheses
        output = self.llm.generate_json(prompt)
        return output
