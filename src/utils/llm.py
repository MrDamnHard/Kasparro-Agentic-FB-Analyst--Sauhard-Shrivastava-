import json
import time
from langchain_ollama import ChatOllama
from src.utils.logger import AgentLogger


class LLM:
    """
    Unified LLM wrapper using LangChain + Ollama with:
    - Automatic retry (exponential backoff)
    - Text + JSON-safe extraction
    - Full observability: retry logs, error logs, runtime logs
    """

    def __init__(self, model: str = "llama3", temperature: float = 0.2):
        self.model = model
        self.temperature = temperature
        self.logger = AgentLogger()

        # Base LLM
        self.llm = ChatOllama(
            model=self.model,
            temperature=self.temperature,
        )

        # Retry-enabled wrapper
        self.llm_with_retry = self.llm.with_retry(
            stop_after_attempt=3,                 # total attempts
            wait_exponential_jitter=True,         # exponential backoff with jitter
        )

    # ------------------------------------------------------------------
    # TEXT GENERATION WITH LOGGING
    # ------------------------------------------------------------------
    def generate(self, prompt: str) -> str:
        """
        Generate plain text using retry-enabled LLM.
        Logs: runtime + retry attempts + errors.
        """
        start = time.time()

        try:
            response = self.llm_with_retry.invoke(prompt)
            text = response.content

            # Runtime log
            self.logger.log_runtime(
                "LLM.generate",
                start,
                {"chars": len(text)}
            )
            return text

        except Exception as e:
            # ERROR log
            self.logger.log_error(
                "LLM.generate",
                f"LLM invocation failed after retries: {str(e)}",
                {"prompt_sample": prompt[:200]}
            )
            return f"LLM Error: {str(e)}"

    # ------------------------------------------------------------------
    # JSON GENERATION WITH FALLBACKS + LOGGING
    # ------------------------------------------------------------------
    def generate_json(self, prompt: str) -> dict:
        """
        Generate structured JSON using:
        1) direct JSON attempt
        2) substring JSON extraction
        3) final fallback safe error structure

        Fully logged (runtime + errors).
        """

        start = time.time()

        raw = self.generate(prompt)

        # Try direct JSON
        try:
            parsed = json.loads(raw)
            self.logger.log_runtime(
                "LLM.generate_json",
                start,
                {"method": "direct_json"}
            )
            return parsed

        except Exception:
            pass

        # Try substring extraction
        try:
            s = raw.index("{")
            e = raw.rindex("}") + 1
            cleaned = raw[s:e]
            parsed = json.loads(cleaned)

            self.logger.log(
                "LLM.generate_json",
                {"attempt": "substring_extract"},
                {"success": True}
            )
            self.logger.log_runtime("LLM.generate_json", start)
            return parsed

        except Exception as e:
            # Log that substring parsing also failed
            self.logger.log_error(
                "LLM.generate_json",
                f"JSON parsing failed: {str(e)}",
                {"raw_sample": raw[:200]}
            )

        # Final fallback – never break pipeline
        fallback = {
            "error": "Invalid JSON",
            "raw_output": raw
        }

        self.logger.log_runtime(
            "LLM.generate_json",
            start,
            {"fallback_used": True}
        )

        return fallback
