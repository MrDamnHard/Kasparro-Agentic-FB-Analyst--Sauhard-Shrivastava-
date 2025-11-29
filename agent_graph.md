agent_graph.md — Kasparro Agentic Facebook Ads Analyst Architecture

Author: Sauhard Shrivastava
Project: kasparro-agentic-fb-analyst-sauhard-shrivastava

🧠 High-Level Multi-Agent Architecture
                         ┌──────────────────────────────┐
                         │          User Query           │
                         └───────────────┬───────────────┘
                                         │
                                         ▼
                             ┌────────────────────────┐
                             │     Planner Agent      │
                             │  (task decomposition)  │
                             └────────────┬───────────┘
                                          │ plan
                                          ▼
       ┌───────────────────────────────────────────────────────────────┐
       │                        Data Agent                              │
       │  load_data → schema check → preprocess → metrics → drift        │
       │  get_summary_metrics → get_low_ctr_creatives                   │
       └──────────────────────────────┬────────────────────────────────┘
                                      ▼
                           ┌─────────────────────────┐
                           │     Insight Agent       │
                           │     (LLM hypotheses)    │
                           └──────────────┬──────────┘
                                          │ raw insights (JSON)
                                          ▼
                          ┌────────────────────────────────┐
                          │        Evaluator Agent         │
                          │  quantitative validation +     │
                          │  blended confidence scoring    │
                          └──────────────┬─────────────────┘
                                         ▼
                          ┌────────────────────────────────┐
                          │        Creative Agent          │
                          │  (LLM creative generation)     │
                          │    json-safe via 2-pass LLM    │
                          └──────────────┬─────────────────┘
                                         ▼
                          ┌────────────────────────────────┐
                          │     Report Generator (run.py)   │
                          │ insights.json + creatives.json  │
                          │        → final report.md        │
                          └─────────────────────────────────┘

🗂 Agent Responsibilities (Detailed)
1️⃣ Planner Agent

Reads the user query (“Analyze ROAS drop”)

Identifies the metric to analyze

Produces a simple ordered task plan:

[
  {"task": "load_data"},
  {"task": "fetch_timeseries", "metric": "roas"},
  {"task": "analyze_trends"},
  {"task": "evaluate_insights"},
  {"task": "generate_recommendations"}
]


LLM not used here (simple rule-based logic)

2️⃣ Data Agent

Core responsibilities:

Load CSV and normalize schema

Validate schema against REQUIRED_COLUMNS

Compute derived metrics:

CPC

Conversion Rate

Compute last 7 days vs previous 7 days

Drift detection using:

Z-scores

Percent change

Severity classification (low / moderate / high)

Extract low-CTR creatives

Features added for production reliability:

Safe NA filling

Division-by-zero guards (EPS = 1e-6)

ERROR logs on missing columns

Runtime logs for all methods

3️⃣ Insight Agent (LLM)

Input: Metric summary + drift signals.
Output:

{
  "hypotheses": [
    {
      "reason": "...",
      "evidence": "...",
      "confidence": 0.83,
      "recommended_action": "..."
    }
  ]
}


Why LangChain + Ollama?

.with_retry() gives exponential backoff

Ensures robustness when LLM server is slow or fails

JSON Safety Pipeline:

Ask LLM for JSON

Try json.loads

Try extracting { ... } substring

Fallback hypothesis if still invalid

Nothing crashes the pipeline.

Logs:

hypothesis count

raw parse failures

runtime

4️⃣ Evaluator Agent

This agent combines:

ROAS / CTR / CPC / CVR deltas

Drift z-scores

Spend & impression relationships

Hypothesis keywords (“CTR”, “fatigue”, “conversion”)

Produces:

numeric confidence (0–1)

final blended confidence

validated vs rejected hypotheses

Example:

{
  "reason": "...",
  "llm_confidence": 0.8,
  "quant_confidence": 0.85,
  "final_confidence": 0.82,
  "validated": true
}


Logs:

runtime for entire validation

numeric scoring time per hypothesis

number of validated/rejected

5️⃣ Creative Agent (LLM)

Receives low-CTR creatives (< threshold).
Two-step process ensures valid JSON:

Pass 1: Ask model to generate creative ideas
Pass 2: Ask model to convert output into strict JSON schema

If even that fails → inject safe empty structure.

Final Output:

{
  "analysis": "...",
  "new_creatives": {
    "headlines": [...],
    "primary_text": [...],
    "hooks": [...],
    "ctas": [...],
    "offer_angles": [...]
  }
}

🔄 End-to-End Data Flow
raw_dataset.csv
    │
    ▼
DataAgent → {metrics, deltas, drift, low_ctr_creatives}
    │
    ▼
InsightAgent (LLM)
    → hypotheses.json
    │
    ▼
EvaluatorAgent
    → validated_hypotheses.json
    │
    ▼
CreativeAgent (LLM)
    → creatives.json
    │
    ▼
ReportGenerator (run.py)
    → report.md

🔐 Error Handling & Retry Flow
LLM Errors

If LLM fails:

retried 3 times with exponential backoff

logged with ERROR log level

fallback safe JSON returned

Schema Errors

If dataset is missing columns:

ERROR logged

DataAgent returns None

Orchestrator handles gracefully

JSON Parse Errors

InsightAgent and CreativeAgent:

substring extraction → fallback JSON

pipeline never crashes

📜 Observability Layer

Every agent logs via AgentLogger to:

logs/agent_runs.jsonl


Each log line includes:

{
  "timestamp": "2025-11-29T14:32:41Z",
  "run_id": "5b9a844f-2fbe-4e93-9fa8-381e33caa8fa",
  "level": "INFO",
  "agent": "DataAgent.detect_drift",
  "runtime_ms": 3.12,
  "input": {"last7_n": 7},
  "output": {"spend": {...}, "ctr": {...}}
}

📄 Final Outputs

Generated inside /reports:

File	Description
insights.json	Validated + rejected hypotheses
creatives.json	Structured creative ideas
report.md	Final marketer-friendly report
🎯 Summary

This system fulfills all Kasparro assignment requirements:

✔ Multi-agent architecture
✔ LLM reasoning with JSON safety
✔ Retry + backoff
✔ Full observability
✔ Schema validation
✔ Drift detection
✔ Hypothesis validation
✔ Creative generation
✔ Final report generation
✔ Reproducible CLI pipeline