import json
import numpy as np

class EvaluatorAgent:
    """
    Evaluates hypotheses from the InsightAgent using numeric validation.
    """

    def __init__(self):
        pass

    def validate(self, metric_summary: dict, llm_hypotheses: dict):
        validated = []
        rejected = []

        # Expand metric summary
        roas_last = metric_summary["roas"]["last7"]
        roas_prev = metric_summary["roas"]["prev7"]
        ctr_last = metric_summary["ctr"]["last7"]
        ctr_prev = metric_summary["ctr"]["prev7"]
        cpc_last = metric_summary["cpc"]["last7"]
        cpc_prev = metric_summary["cpc"]["prev7"]
        conv_last = metric_summary["conversion_rate"]["last7"]
        conv_prev = metric_summary["conversion_rate"]["prev7"]

        for h in llm_hypotheses.get("hypotheses", []):

            reason = h.get("reason", "")
            evidence = h.get("evidence", "")
            llm_conf = float(h.get("confidence", 0.5))

            quant_score = 0.0
            checks = 0

            # ------------------------------
            # 1. Validate CTR drop claims
            # ------------------------------
            if "ctr" in reason.lower() or "ctr" in evidence.lower():
                checks += 1
                if ctr_last < ctr_prev:
                    quant_score += 1

            # ------------------------------
            # 2. Validate CPC increase claims
            # ------------------------------
            if "cpc" in reason.lower() or "cpc" in evidence.lower():
                checks += 1
                if cpc_last > cpc_prev:
                    quant_score += 1

            # ------------------------------
            # 3. Validate Conversion Rate drop claims
            # ------------------------------
            if "conversion" in reason.lower() or "conversion" in evidence.lower():
                checks += 1
                if conv_last < conv_prev:
                    quant_score += 1

            # ------------------------------
            # 4. Validate ROAS drop claims
            # ------------------------------
            if "roas" in reason.lower() or "roas" in evidence.lower():
                checks += 1
                if roas_last < roas_prev:
                    quant_score += 1

            # Avoid division by zero
            if checks == 0:
                final = {
                    "reason": reason,
                    "evidence": evidence,
                    "llm_confidence": llm_conf,
                    "quant_confidence": 0.0,
                    "final_confidence": round(llm_conf * 0.6, 2),
                    "validated": False,
                }
                rejected.append(final)
                continue

            quant_conf = quant_score / checks

            final_conf = round((llm_conf * 0.5) + (quant_conf * 0.5), 2)

            result = {
                "reason": reason,
                "evidence": evidence,
                "llm_confidence": llm_conf,
                "quant_confidence": round(quant_conf, 2),
                "final_confidence": final_conf,
                "validated": quant_conf >= 0.5,
            }

            # Decide whether to accept the hypothesis
            if result["validated"]:
                validated.append(result)
            else:
                rejected.append(result)

        return {
            "validated_hypotheses": validated,
            "rejected_hypotheses": rejected
        }
