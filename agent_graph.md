🧠 Kasparro Agentic FB Analyst — Agent Graph & Data Flow
🎯 Overview

This document explains the agent architecture, data flow, and reasoning structure of the Kasparro Agentic Facebook Performance Analyst.

The system is built with autonomous components (“agents”) that interact to diagnose Facebook Ads performance and generate optimized creative strategies.

📊 Agent Graph (Mermaid Diagram)
flowchart TD

    A[User Query] --> B[Planner Agent]

    B --> C[Data Agent]

    C --> D[Insight Agent]

    D --> E[Evaluator Agent]

    E --> F[Recommendation Agent]

    C --> G[Creative Agent]

    E --> F
    F --> H[Final Report Generator]
    G --> H

🔍 Agent Responsibilities
1. Planner Agent

Parses the user query

Produces a structured task plan

Ensures downstream agents know what to do

Converts natural language → step-by-step agent workflow

Example output:

[
  {"task": "load_data"},
  {"task": "fetch_timeseries", "metric": "roas"},
  {"task": "analyze_trends"},
  {"task": "evaluate_insights"},
  {"task": "generate_recommendations"}
]

2. Data Agent

Loads & cleans the CSV dataset

Computes last 7 vs previous 7 day summaries

Extracts low CTR creatives

Creates data foundation for insights

Produces:

Time-series metrics

Aggregated KPIs

Creative-level performance

3. Insight Agent (LLM-based)

Takes numeric summary from Data Agent

Generates hypotheses explaining ROAS changes

Structured JSON output with confidence scores

Uses chain-of-thought internally but outputs clean JSON

Example:

{
  "reason": "CTR drop reduced efficiency.",
  "evidence": "CTR -23%, conversions -14%.",
  "confidence": 0.81
}

4. Evaluator Agent

Validates Insight Agent hypotheses numerically

Adjusts confidence based on thresholds

Ensures insights are reliable and not hallucinated

Checks:

CTR % delta

CPC delta

CVR delta

Impression/spend shifts

ROAS change magnitude

5. Recommendation Agent (LLM-based)

Converts metrics + insights → strategic actions

Marketing-focused output

Produces 5–8 actionable steps

Examples:

“Introduce 2 new creatives to counter fatigue”

“Increase budget on high-ROAS adsets”

“Expand 2% lookalike audience”

6. Creative Agent (LLM + JSON Repair Layer)

Analyzes low-performing creatives

Generates:

Headlines

Primary text

Hooks

CTAs

Offer angles

Uses 2-pass generation:

Creative free text (LLM freedom)

Strict JSON reconstruction (no hallucination)

Ensures stable output even if LLM drifts.

7. Final Report Generator

Combines:

Validated hypotheses

Creative recommendations

Strategic recommendations

Outputs a marketing-ready Markdown file:

reports/report.md

🔁 Data Flow Summary

User Query → Planner Agent

Planner → Data Agent

Metrics → Insight Agent

Hypotheses → Evaluator Agent

Validated → Recommendation Agent

Low CTR creatives → Creative Agent

Everything → Final Report

This produces a highly structured, explainable, and marketer-friendly analysis.

🧩 Why This Architecture?

Separates LLM reasoning from numerical logic

Reduces hallucinations with evaluator agent

Enables creative and analytical thinking simultaneously

Fully reproducible across datasets

Follows Kasparro’s assignment structure precisely

Highly extensible (memory, iterations, dashboards)

📦 Files Produced

insights.json – hypotheses + confidence

creatives.json – creative concepts

recommendations.json – next-step strategies

report.md – final report