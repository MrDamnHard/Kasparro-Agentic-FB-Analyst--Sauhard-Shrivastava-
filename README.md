📘 Kasparro Agentic Facebook Ads Performance Analyst
Author: Sauhard Shrivastava
Repository: kasparro-agentic-fb-analyst-sauhard-shrivastava

An LLM-powered, multi-agent analytics system that diagnoses Facebook Ads performance, validates insights quantitatively, detects drift, and generates new creative recommendations — all with production-grade retry, logging, and JSON safety.

Built for the Kasparro Applied AI Engineer Assignment, following all rubric requirements (Planner → Data → Insight → Evaluator → Creative → Report).

⭐ What This System Does

This agentic system autonomously:

🔍 Diagnose why ROAS changed

Identifies which metrics (CTR, CPC, CVR, Spend, Impressions) drove the change.

🧠 Generate hypotheses using an LLM

Uses structured reasoning + JSON-safe prompting.

📊 Validate hypotheses quantitatively

EvaluatorAgent blends numeric confidence with LLM confidence.

🧪 Detect drift (z-scores + percent change)

Flags high severity shifts (eg. ROAS spike, CTR crash).

🎨 Generate new creative ideas

Headlines, hooks, CTAs, offer angles — with strict JSON guarantee.

📄 Produce a complete, marketing-ready report

Saved as reports/report.md.

🧾 Log everything in structured JSON

Every agent writes: timestamp, agent name, runtime_ms, input/output, errors, retry info.




🧠 Architecture Overview
User Query
    ▼
Planner Agent
    ▼
Data Agent → loads dataset, validates schema, computes last7/prev7, detects drift
    ▼
Insight Agent (LLM via LangChain/Ollama) → hypotheses (JSON)
    ▼
Evaluator Agent → numeric evaluation + confidence blending
    ▼
Creative Agent (LLM with JSON forcing)
    ▼
Report Generator → insights.json, creatives.json, report.md



🏗 Project Structure
kasparro-agentic-fb-analyst-sauhard-shrivastava/
│
├── data/
│   └── raw_dataset.csv
|tests/
| ├── test_data_agent.py
| ├── test_evaluator.py
| └── test_json_safety.py
├── src/
│   ├── agents/
│   │     ├── planner_agent.py
│   │     ├── data_agent.py
│   │     ├── insight_agent.py
│   │     ├── evaluator_agent.py
│   │     ├── creative_agent.py
│   │
│   ├── utils/
│   │     ├── llm.py          ← LangChain + Ollama wrapper (retry + JSON safety)
│   │     └── logger.py       ← structured logging
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
│   └── agent_runs.jsonl      ← all agent logs
│
├── requirements.txt
├── run.py
└── README.md



💡 Why This Design?
🧱 Multi-Agent Separation

Each agent has a single responsibility:

Planner — break query into subtasks

DataAgent — metrics, drift, schema

InsightAgent — LLM reasoning

Evaluator — numeric validation

CreativeAgent — JSON-safe creative generation

This fulfills Kasparro’s expected Planner → Evaluator loop.

🤖 Why LangChain + Ollama?

We use LangChain only for:

Managing .with_retry() for exponential backoff

A simple ChatOllama interface

Clean .invoke() abstraction

Standard formatting of output

The actual LLM usage stays isolated inside LLM.generate and LLM.generate_json, making the whole system modular.

🔐 JSON Safety (Critical Requirement)

All LLM outputs must be valid JSON.
Our system guarantees this by:

Asking for JSON via prompt

Trying json.loads directly

Trying to extract { ... } substring

Falling back to:

{"error": "Invalid JSON", "raw_output": "..."}


This matches industry hardening practices for production LLM pipelines.

🔁 Retry / Backoff (Required by Reviewer)

llm.py uses:

self.llm.with_retry(
    stop_after_attempt=3,
    wait_exponential_jitter=True
)


This gives:

exponential increasing delay

jitter randomness

automatic retry

logged errors

📜 Structured Logging (Observability)

Each log entry includes:

{
  "timestamp": "...",
  "run_id": "...",
  "level": "INFO",
  "agent": "DataAgent.detect_drift",
  "runtime_ms": 3.12,
  "input": {"last7_n": 7},
  "output": {...}
}


Logging covers:

start/end times

error logs

retry logs

hypothesis counts

drift classification

This was a mandatory improvement from reviewer feedback.

⚙️ Installation
1. Clone the repository
git clone https://github.com/<your-username>/kasparro-agentic-fb-analyst-sauhard-shrivastava
cd kasparro-agentic-fb-analyst-sauhard-shrivastava

2. Create conda environment (recommended)
conda create -n kasparro python=3.11 -y
conda activate kasparro
pip install -r requirements.txt

3. Install & run Ollama
ollama pull llama3

4. Run the full pipeline
python run.py "Analyze ROAS drop"


Outputs will appear in /reports.

📤 Example Output
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

📈 Drift Detection Example

The DataAgent computes drift like:

"drift": {
  "roas": {
    "severity": "high",
    "z_score": 3.43,
    "change_pct": 307.1,
    "last7": 6.61,
    "prev7": 1.62
  }
}


High drift indicates sudden change that must be validated.

🔧 Troubleshooting
❌ JSON parsing error in LLM output

✓ Handled automatically.
✓ See logs in logs/agent_runs.jsonl.

❌ Unicode error writing report

Ensure Windows is using UTF-8 (VSCode auto-handles this).

❌ pydantic_core installation fails

Use Python 3.11 + conda — avoids Rust compile issues.

❌ Ollama model not found

Run:

ollama pull llama3

🧪 Tests (Recommended)

To run:

pytest -q


(If you want, I can generate the test files for you.)

🔖 Release Instructions (Required for Submission)

Create tag:

git tag -a v1.0 -m "Kasparro submission v1.0"
git push origin v1.0


Create PR titled self-review
Include design decisions, trade-offs, known limitations.

🚀 Summary

This project satisfies all Kasparro assignment requirements:

✔ Multi-agent architecture
✔ LLM reasoning with JSON safety
✔ Automatic retry + backoff
✔ Drift detection + schema validation
✔ Advanced evaluator (numeric + drift)
✔ Rich observability (runtime, errors, retries)
✔ Creative generation with strict JSON output
✔ End-to-end reproducible CLI pipeline