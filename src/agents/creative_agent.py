import json
from src.utils.llm import LLM


class CreativeAgent:
    """
    Production-grade Creative Agent using:
    - Two-pass generation
    - Strict schema validation
    - Auto-fill defaults
    - Improved prompts
    - Safe fallbacks
    """

    def __init__(self):
        self.llm = LLM()

        # Base creative prompt
        with open("prompts/creative_prompt.md", "r") as f:
            self.base_prompt = f.read()

        # Second pass → convert ideas to JSON
        self.converter_prompt = """
You are a JSON formatting engine.
Convert the text into STRICT JSON following this schema ONLY:

{
  "analysis": "string, 1-3 sentences analyzing the issues with low-performing creatives.",
  "new_creatives": {
    "headlines": ["5-10 punchy ad headlines"],
    "primary_text": ["3-6 primary messages"],
    "hooks": ["3-6 thumb-stopping opening lines"],
    "ctas": ["3-6 call-to-actions"],
    "offer_angles": [
      {"name": "angle title", "description": "1 sentence description"},
      {"name": "angle title", "description": "1 sentence description"}
    ]
  }
}

RULES:
- Output ONLY JSON. No markdown. No text around it.
- Lists must NOT be empty. Fill them with your best suggestions.
- Values MUST be strings.
- You MUST derive improvements from the provided low CTR creatives.

TEXT TO CONVERT:
"""

    def generate(self, low_ctr_creatives: list):

        # -------- PASS 1: Generate ideas (messy OK) --------
        prompt = (
            self.base_prompt
            + "\n\n### LOW CTR CREATIVES\n"
            + json.dumps(low_ctr_creatives, indent=2)
        )

        raw_output = self.llm.generate(prompt)

        # -------- PASS 2: Convert to strict JSON --------
        convert_prompt = self.converter_prompt + "\n\n" + raw_output
        json_output = self.llm.generate_json(convert_prompt)

        # Validate JSON
        validated = self._validate_json(json_output)

        return validated

    # ----------------------- JSON VALIDATION -------------------------

    def _validate_json(self, data):
        """Ensures required fields exist and are non-empty."""

        if not isinstance(data, dict):
            return self.empty_output("Invalid JSON response")

        if "new_creatives" not in data:
            return self.empty_output("Missing new_creatives")

        nc = data["new_creatives"]

        # Auto-fill all missing buckets
        defaults = {
            "headlines": ["Fresh Deal Just Dropped!", "You’ll Love This Upgrade"],
            "primary_text": ["Discover what your feed was missing."],
            "hooks": ["Stop scrolling — look at this!"],
            "ctas": ["Shop Now", "Learn More"],
            "offer_angles": [
                {"name": "Limited Time", "description": "Create urgency to act now."}
            ]
        }

        for key in defaults:
            if key not in nc or not isinstance(nc[key], list) or len(nc[key]) == 0:
                nc[key] = defaults[key]

        # Ensure analysis exists
        if "analysis" not in data or not isinstance(data["analysis"], str):
            data["analysis"] = "Creative analysis missing."

        return data

    # ----------------------- FALLBACK -------------------------

    def empty_output(self, reason):
        return {
            "analysis": reason,
            "new_creatives": {
                "headlines": ["Fresh Deal Just Dropped!"],
                "primary_text": ["Discover what your feed was missing."],
                "hooks": ["Stop scrolling — look at this!"],
                "ctas": ["Shop Now"],
                "offer_angles": [
                    {"name": "Limited Time", "description": "Create urgency to act now."}
                ]
            }
        }
