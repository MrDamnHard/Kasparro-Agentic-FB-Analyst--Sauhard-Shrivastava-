import json
import ollama

class LLM:
    def __init__(self, model="llama3", temperature=0.2):
        self.model = model
        self.temperature = temperature

    def generate(self, prompt: str) -> str:
        response = ollama.generate(
            model=self.model,
            prompt=prompt,
            options={
                "temperature": self.temperature,
                "format": "json"  # <--- FORCE JSON OUTPUT
            }
        )
        return response["response"]
    def generate_json(self, prompt: str) -> dict:
        """
        Ensures response is valid JSON.
        Forces JSON output and cleans malformed text.
        """
        response = self.generate(prompt)

    # 1. Try direct JSON decode
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            pass

    # 2. Try extracting JSON substring
        try:
            start = response.index("{")
            end = response.rindex("}") + 1
            cleaned = response[start:end]
            return json.loads(cleaned)
        except:
            pass

    # 3. Hard fallback
        return {
            "error": "Invalid JSON",
            "raw": response
        }
