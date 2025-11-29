import json
import time
from typing import Dict, Any
from src.utils.llm import LLM
from src.utils.logger import AgentLogger


class InsightAgent:
    """
    InsightAgent with upgraded logging:
    - logs runtime for each run
    - logs errors when LLM JSON parsing fails
    - logs fallback triggers
    - logs structured output + hypothesis count
    """

    def __init__(self):
        self.llm = LLM()
        self.logger = AgentLogger()

        # Load minimal prompt template
        with open("prompts/insight_prompt.md", "r", encoding="utf-8") as f:
            self.base_prompt = f.read()

    def generate(self, metric_summary: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate hypotheses based on metric_summary using the LLM.
        Includes runtime logging and error logging.
        """
        start = time.time()

        # Build LLM prompt
        payload = {
            "metrics": metric_summary,
            "drift": metric_summary.get("drift", {})
        }

        full_prompt = self.base_prompt + "\n\nMETRICS:\n" + json.dumps(payload, indent=2)

        # -------------------------------------------------------------
        # 1) Primary attempt: JSON-aware LLM call
        # -------------------------------------------------------------
        output = self.llm.generate_json(full_prompt)

        # -------------------------------------------------------------
        # 2) Fallback: Try to salvage JSON substring manually
        # -------------------------------------------------------------
        if not isinstance(output, dict) or "hypotheses" not in output:
            self.logger.log_error(
                "InsightAgent.generate",
                "Primary JSON parse failed. Trying raw parse fallback.",
                {"raw_sample": str(output)[:200]}
            )

            raw = self.llm.generate(full_prompt)

            # Try JSON substring extraction
            try:
                start_idx = raw.index("{")
                end_idx = raw.rindex("}") + 1
                cleaned = json.loads(raw[start_idx:end_idx])
                output = cleaned
            except Exception as e:
                # -----------------------------------------------------
                # 3) Final fallback: deterministic rule-based hypothesis
                # -----------------------------------------------------
                self.logger.log_error(
                    "InsightAgent.generate",
                    f"Fallback JSON extraction failed: {str(e)}"
                )

                output = {
                    "hypotheses": [
                        {
                            "reason": "Unable to parse model output.",
                            "evidence": "Model returned non-JSON response.",
                            "confidence": 0.4,
                            "recommended_action": "Re-run the pipeline or inspect LLM raw logs."
                        }
                    ]
                }

        # -------------------------------------------------------------
        # 4) Normalize structure into clean, safe output
        # -------------------------------------------------------------
        normalized = self._normalize(output)

        # Log successful generation (INFO level)
        self.logger.log(
            "InsightAgent.generate",
            {"hypotheses_requested": True},
            {"n_hypotheses": len(normalized.get("hypotheses", []))}
        )

        # Log runtime
        self.logger.log_runtime(
            "InsightAgent.generate",
            start,
            {"success": True}
        )

        return normalized

    # -------------------------------------------------------------
    # Structure normalization
    # -------------------------------------------------------------
    def _normalize(self, parsed: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ensures standardized structure:
        - hypotheses list exists
        - confidence is numeric
        - strip whitespace
        """
        if not isinstance(parsed, dict) or "hypotheses" not in parsed:
            return {"hypotheses": []}

        cleaned = []

        for h in parsed["hypotheses"]:
            try:
                reason = str(h.get("reason", "")).strip()
                evidence = str(h.get("evidence", "")).strip()
                action = str(h.get("recommended_action", "")).strip()

                try:
                    conf = float(h.get("confidence", 0.5))
                except:
                    conf = 0.5

                conf = max(0.0, min(1.0, conf))  # clamp 0..1

                cleaned.append({
                    "reason": reason,
                    "evidence": evidence,
                    "confidence": conf,
                    "recommended_action": action
                })

            except Exception as e:
                # Log malformed hypothesis but continue
                self.logger.log_error(
                    "InsightAgent._normalize",
                    f"Malformed hypothesis skipped: {str(e)}",
                    {"raw": h}
                )
                continue

        # Final fallback if list is empty
        if not cleaned:
            self.logger.log_error(
                "InsightAgent._normalize",
                "No valid hypotheses after normalization."
            )

            cleaned = [
                {
                    "reason": "Unable to produce structured insights.",
                    "evidence": "Fallback triggered.",
                    "confidence": 0.5,
                    "recommended_action": "Review data quality or adjust prompt."
                }
            ]

        return {"hypotheses": cleaned}
