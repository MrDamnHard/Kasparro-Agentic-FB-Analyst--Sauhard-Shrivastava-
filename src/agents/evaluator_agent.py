import time
from typing import Any, Dict, List
from src.utils.logger import AgentLogger


class EvaluatorAgent:
    """
    Production-grade EvaluatorAgent with advanced logging:
    - runtime logging
    - structured INFO logs
    - ERROR logs for numeric evaluation failures
    - blended confidence (numeric + LLM)
    - drift-aware numeric scoring
    """

    def __init__(self):
        self.logger = AgentLogger()

    # --------------------------------------------------------
    # Main entrypoint
    # --------------------------------------------------------
    def validate(self, metrics: Dict[str, Any], insights: Dict[str, Any]) -> Dict[str, Any]:
        start = time.time()

        drift = metrics.get("drift", {})
        hypotheses = insights.get("hypotheses", [])

        validated = []
        rejected = []

        for h in hypotheses:
            try:
                numeric = self._evaluate_numeric_alignment(h, metrics, drift)
            except Exception as e:
                # Log numeric evaluation failure but continue pipeline
                self.logger.log_error(
                    "EvaluatorAgent.validate",
                    f"Numeric evaluation failed: {str(e)}",
                    {"hypothesis": h}
                )
                numeric = 0.3  # safe fallback so pipeline continues

            llm_conf = float(h.get("confidence", 0.5))

            # final confidence
            final_conf = round(0.4 * numeric + 0.6 * llm_conf, 2)

            result = {
                "reason": h.get("reason", ""),
                "evidence": h.get("evidence", ""),
                "llm_confidence": llm_conf,
                "quant_confidence": numeric,
                "final_confidence": final_conf,
                "recommended_action": h.get("recommended_action", "")
            }

            if final_conf >= 0.5:
                result["validated"] = True
                validated.append(result)
            else:
                result["validated"] = False
                rejected.append(result)

        out = {
            "validated_hypotheses": validated,
            "rejected_hypotheses": rejected
        }

        # INFO log for final evaluation output
        self.logger.log(
            "EvaluatorAgent.validate",
            {"n_hypotheses": len(hypotheses)},
            {
                "validated": len(validated),
                "rejected": len(rejected)
            }
        )

        # Add runtime log
        self.logger.log_runtime(
            "EvaluatorAgent.validate",
            start,
            {"validated_count": len(validated)}
        )

        return out

    # --------------------------------------------------------
    # Numeric scoring logic
    # --------------------------------------------------------
    def _evaluate_numeric_alignment(
        self,
        hypothesis: Dict[str, Any],
        metrics: Dict[str, Any],
        drift: Dict[str, Any]
    ) -> float:

        start = time.time()  # runtime for numeric scoring

        reason = hypothesis.get("reason", "").lower()
        evidence = hypothesis.get("evidence", "").lower()

        # Safe extract helpers
        def safe_metric(col: str, key: str):
            try:
                return float(metrics.get(col, {}).get(key, 0))
            except Exception:
                return 0.0

        def safe_drift(col: str, key: str):
            try:
                return drift.get(col, {}).get(key, None)
            except Exception:
                return None

        # Extract deltas
        roas_change = safe_metric("roas", "change")
        ctr_change = safe_metric("ctr", "change")
        cpc_change = safe_metric("cpc", "change")
        conv_change = safe_metric("conversion_rate", "change")
        impressions_change = safe_metric("impressions", "change")
        spend_change = safe_metric("spend", "change")

        # Extract drift z-scores
        ctr_z = safe_drift("ctr", "z_score")
        cpc_z = safe_drift("cpc", "z_score")
        spend_z = safe_drift("spend", "z_score")
        roas_z = safe_drift("roas", "z_score")

        score = 0.2  # baseline — avoids ever being zero

        # ----------------------------- 
        # ROAS alignment
        # -----------------------------
        if "roas" in reason or "roas" in evidence:
            if roas_change > 0:
                score += 0.25
            elif roas_change < 0:
                score += 0.15

        # -----------------------------
        # CTR alignment
        # -----------------------------
        if "ctr" in reason or "ctr" in evidence:
            if ctr_change > 0:
                score += 0.20
            if ctr_z and abs(ctr_z) > 2:
                score += 0.10

        # -----------------------------
        # CPC alignment
        # -----------------------------
        if "cpc" in reason or "cost" in reason:
            if cpc_change < 0:
                score += 0.15
            if cpc_z and abs(cpc_z) > 2:
                score += 0.10

        # -----------------------------
        # Conversion rate alignment
        # -----------------------------
        if "conversion" in reason or "cvr" in reason:
            if conv_change > 0:
                score += 0.20
            if conv_change < 0:
                score += 0.10

        # -----------------------------
        # Spend / Impressions alignment
        # -----------------------------
        if "spend" in reason and spend_change > 0:
            score += 0.10

        if "impressions" in reason and impressions_change > 0:
            score += 0.10

        # -----------------------------
        # Drift alignment
        # -----------------------------
        if "fatigue" in reason:
            if ctr_z and ctr_z < -2:
                score += 0.15

        if "volatility" in reason or "unstable" in reason:
            if spend_z and abs(spend_z) > 2:
                score += 0.15

        # Cap at 1.0
        score = float(min(1.0, score))

        # Log numeric scoring runtime
        self.logger.log_runtime(
            "EvaluatorAgent._evaluate_numeric_alignment",
            start,
            {"numeric_score": score}
        )

        return score
