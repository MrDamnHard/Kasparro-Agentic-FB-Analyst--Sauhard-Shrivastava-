📘 Kasparro Agentic Facebook Ads Performance Analyst

Author: Sauhard Shrivastava
Repository: kasparro-agentic-fb-analyst-sauhard-shrivastava

⭐ Overview

This project implements a multi-agent, LLM-powered Facebook Ads analytics system.
It autonomously:

Diagnoses why ROAS changed over time

Identifies performance drivers (CTR, CPC, CVR, Spend, Impressions)

Generates hypotheses using LLM reasoning

Validates hypotheses with quantitative checks

Recommends strategic next steps

Produces new creative ideas for low-CTR ads

Outputs everything into a clean report.md

This follows the Kasparro Applied AI Engineer Assignment structure and evaluation rubric.

🧠 System Architecture
               ┌─────────────────┐
               │  User Query     │
               └────────┬────────┘
                        │
                        ▼
               ┌─────────────────┐
               │ Planner Agent   │
               └───────┬─────────┘
                       │ Creates task plan
                       ▼
     ┌───────────────────────────────────────────┐
     │ Data Agent                                │
     │ - Load dataset                            │
     │ - Compute last7 vs prev7                  │
     │ - Extract low CTR creatives               │
     └───────────────────────────────────────────┘
                       ▼
               ┌─────────────────┐
               │ Insight Agent   │
               │ (LLM reasoning) │
               └───────┬─────────┘
                       ▼
           ┌───────────────────────────┐
           │ Evaluator Agent           │
           │ Numeric validation        │
           └─────────┬─────────────────┘
                     ▼
         ┌──────────────────────────────┐
         │ Recommendation Agent         │
         │ Strategic optimization steps │
         └───────────┬──────────────────┘
                     ▼
         ┌──────────────────────────────┐
         │ Creative Agent (LLM)         │
         │ New creatives for low CTR    │
         └───────────┬──────────────────┘
                     ▼
         ┌──────────────────────────────┐
         │ Final Report (report.md)     │
         └──────────────────────────────┘

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
│   │     └── recommendation_agent.py
│   │
│   ├── utils/
│   │     └── llm.py
│   │
│   └── __init__.py
│
├── prompts/
│   ├── planner_prompt.md
│   ├── creative_prompt.md
│   └── insight_prompt.md
│
├── reports/
│   ├── insights.json
│   ├── creatives.json
│   ├── recommendations.json
│   └── report.md
│
├── logs/
│   └── agent_runs.jsonl
│
├── config/
│   └── config.yaml
│
├── tests/
│   ├── test_evaluator.py
│   ├── test_data_agent.py
│   └── test_json_safety.py
│
├── run.py
├── requirements.txt
└── Makefile

🔧 Installation
1. Clone the repository
git clone https://github.com/<your-username>/kasparro-agentic-fb-analyst-sauhard-shrivastava
cd kasparro-agentic-fb-analyst-sauhard-shrivastava

2. Install requirements
pip install -r requirements.txt

3. Install & run Ollama locally (Required)

Download Ollama:
https://ollama.com/download

Pull llama3 (or any chosen model):

ollama pull llama3

🚀 Running the System

Run a full analysis:

python run.py "Analyze ROAS drop"


This will automatically generate:

reports/insights.json

reports/creatives.json

reports/recommendations.json

reports/report.md

🤖 Agents — Detailed Explanation
📌 Planner Agent

Breaks the user query into a structured plan such as:

[
  {"task": "load_data"},
  {"task": "fetch_timeseries", "metric": "roas"},
  {"task": "analyze_trends"},
  {"task": "evaluate_insights"},
  {"task": "generate_recommendations"}
]

📌 Data Agent

Responsible for:

Loading the dataset

Cleaning + preprocessing

Computing last 7 days vs previous 7 days metrics

Detecting low CTR creatives

Returning everything to other agents

📌 Insight Agent (LLM)

Uses structured LLM reasoning to generate hypotheses:

{
  "reason": "ROAS dropped due to CTR decline and CPC increase.",
  "evidence": "CTR declined 23%. CPC increased 17%.",
  "confidence": 0.82
}


Includes:

JSON-guaranteed output

Step-by-step reasoning

Confidence scoring

📌 Evaluator Agent

Quantitatively validates LLM hypotheses using:

CTR delta

CPC delta

CVR delta

Spend/Impression changes

ROAS shift

Produces validated and confidence-adjusted insights.

📌 Recommendation Agent (LLM)

Converts insights + metrics into 5–8 strategic recommendations, e.g.:

Expand 2% LAL audience

Introduce 2–3 new creatives

Shift budget toward high-ROAS adsets

Pause fatigued segments

📌 Creative Agent (LLM)

Generates structured creative directions using 2-pass JSON conversion:

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


This ensures valid JSON even if the LLM drifts.

📊 Example Outputs
insights.json
{
  "hypotheses": [
    {
      "reason": "ROAS increased due to CTR improvement and CPC reduction.",
      "evidence": "CTR increased by 0.0009; CPC reduced by 17.6%.",
      "confidence": 0.81
    }
  ]
}

creatives.json
{
  "analysis": "Underperforming creatives show fatigue.",
  "new_creatives": {
    "headlines": ["Feel the confidence", "Unlock comfort"],
    "primary_text": ["Experience all-day comfort"],
    "hooks": ["What’s holding you back?"],
    "ctas": ["Shop Now"],
    "offer_angles": [{"name": "Limited time", "description": "Ends soon!"}]
  }
}

recommendations.json
{
  "recommendations": [
    "Expand lookalike audience from 1% → 2%",
    "Introduce 3 new creatives to counter fatigue",
    "Increase spend on high-ROAS adsets"
  ]
}

report.md

The system generates a clean marketing-ready Markdown report containing:

Performance diagnosis

Validated insights

Creative recommendations

Strategic next steps

⚙️ config.yaml
data_path: data/raw_dataset.csv
low_ctr_threshold: 0.01
model_name: llama3
temperature: 0.2
seed: 42

📜 Logging

All runs are tracked in:

logs/agent_runs.jsonl


Containing:

agent name

timestamps

input

output

error recovery (if any)

🧪 Tests

Minimal tests included in tests/:

evaluator logic

data agent summary

JSON safety conversion

basic pipeline check

Run tests using:

pytest tests/