.

📘 Kasparro Agentic Facebook Ads Performance Analyst

Author: Sauhard Shrivastava
Repository: kasparro-agentic-fb-analyst-sauhard-shrivastava

⭐ Overview

This project implements a multi-agent, LLM-enhanced analytics system for diagnosing Facebook Ads performance.
It autonomously:

Analyzes why ROAS changed

Identifies drivers (CTR, CPC, CVR, Spend, Impressions)

Generates structured LLM hypotheses

Validates them with quantitative checks

Detects drift (z-score, % change, severity)

Produces creative recommendations

Outputs a final marketing-ready report.md

This solution fully aligns with the Kasparro Applied AI Engineer Assignment architecture & evaluation rubric.

🧠 Architecture
                         User Query
                              │
                              ▼
                       Planner Agent
                              │
                              ▼
      ┌─────────────────────────────────────────────┐
      │                Data Agent                   │
      │  - Load & validate dataset                  │
      │  - Compute last7 vs prev7 metrics           │
      │  - Detect drift (z-score, severity)         │
      │  - Extract low CTR creatives                │
      └─────────────────────────────────────────────┘
                              ▼
                       Insight Agent (LLM)
                              ▼
                     Evaluator Agent (Numeric)
                              ▼
                      Creative Agent (LLM)
                              ▼
                     Report Generator (run.py)

📁 Project Structure
kasparro-agentic-fb-analyst-sauhard-shrivastava/
│
├── data/
│   └── raw_dataset.csv
│
├── src/
│   ├── agents/
│   │     ├── planner_agent.py
│   │     ├── data_agent.py
│   │     ├── insight_agent.py
│   │     ├── evaluator_agent.py
│   │     ├── creative_agent.py
│   │
│   ├── utils/
│   │     ├── llm.py
│   │     └── logger.py
│   │
│   └── __init__.py
│
├── prompts/
│   ├── insight_prompt.md
│   ├── creative_prompt.md
│   └── planner_prompt.md
│
├── reports/
│   ├── insights.json
│   ├── creatives.json
│   └── report.md
│
├── logs/
│   └── agent_runs.jsonl
│
├── tests/
│   ├── test_data_agent.py
│   ├── test_evaluator.py
│   └── test_json_safety.py
│
├── run.py
├── requirements.txt
└── README.md

🔧 Installation
1. Clone the repository
git clone https://github.com/<username>/kasparro-agentic-fb-analyst-sauhard-shrivastava
cd kasparro-agentic-fb-analyst-sauhard-shrivastava

2. Create environment (recommended: Python 3.11)
conda create -n kasparro python=3.11 -y
conda activate kasparro
pip install -r requirements.txt

3. Install & start Ollama
ollama pull llama3

4. Run full analysis
python run.py "Analyze ROAS drop"

📊 Example Outputs
insights.json
{
  "validated_hypotheses": [
    {
      "reason": "Increased CTR and Spend led to higher ROAS",
      "evidence": "CTR increased 58% and Spend increased $32.",
      "llm_confidence": 0.8,
      "quant_confidence": 0.85,
      "final_confidence": 0.82
    }
  ]
}

creatives.json
{
  "analysis": "Underperforming creatives show fatigue.",
  "new_creatives": {
    "headlines": ["Feel the confidence"],
    "primary_text": ["Experience all-day comfort"],
    "hooks": ["What's holding you back?"],
    "ctas": ["Shop Now"],
    "offer_angles": []
  }
}

🧪 Testing

Run all tests:

pytest -q


Tests include:

Schema validation

Summary metrics

Drift detection

Evaluator numeric scoring

JSON safety

🔍 Agents — Detailed Behavior
📌 Planner Agent

Creates an execution blueprint based on the user query.

📌 Data Agent

Loads CSV

Validates schema

Computes metrics

Performs drift detection

Identifies low-CTR creatives

📌 Insight Agent (LLM)

Uses structured prompting

Returns guaranteed JSON

Includes fallback/repair logic

📌 Evaluator Agent

Aligns LLM hypotheses with actual metric changes

Computes numeric confidence

Produces validated vs rejected hypotheses

📌 Creative Agent

Generates new creative directions using a 2-pass LLM → JSON pipeline

Guarantees JSON schema compliance

🔐 Observability & Logging

All agents log to:

logs/agent_runs.jsonl


Each log entry includes:

{
  "timestamp": "...",
  "run_id": "...",
  "level": "INFO",
  "agent": "DataAgent.detect_drift",
  "runtime_ms": 3.12
}

📈 Drift Detection Example
"drift": {
  "roas": {
    "severity": "high",
    "z_score": 3.43,
    "change_pct": 307.1
  }
}

🚨 Troubleshooting
Ollama model not found
ollama pull llama3

Invalid JSON from LLM

Handled automatically via fallback parsing.

Unicode write error (Windows)

Ensure UTF-8 encoding in editor.

🏁 Release Instructions (Required for Submission)
Create tag:
git tag -a v1.0 -m "Kasparro submission v1.0"
git push origin v1.0

Create PR titled:
self-review


Paste the PR Self-Review text (already provided).

🎉 Summary

This project meets all assignment requirements:

Multi-agent architecture

Retry/backoff LLM wrapper

Schema validation

Drift detection

Evaluator with numeric alignment

JSON-safe LLM outputs

Fully logged pipeline

Tests included

Final report generation
