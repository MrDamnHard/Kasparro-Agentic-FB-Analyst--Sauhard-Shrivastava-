<!--
KASPARRO AGENTIC ANALYST - HIGH-BAR V2 README
Layout: "Canvas" / Dashboard Style for Senior Engineering Projects
-->

<!-- HEADER / BANNER -->

<div align="center">
<img src="https://www.google.com/search?q=https://capsule-render.vercel.app/api%3Ftype%3Dwaving%26color%3D0:2a2a72,100:009ffd%26height%3D220%26section%3Dheader%26text%3DKasparro%2520Agentic%2520Analyst%26fontSize%3D50%26animation%3DfadeIn%26fontAlignY%3D38%26desc%3DProduction-Grade%2520Multi-Agent%2520LLM%2520System%2520for%2520Ad%2520Performance%26descAlignY%3D55%26descAlign%3D50" width="100%" alt="Kasparro Header" />

<!-- BADGES -->

<p>
<img src="https://www.google.com/search?q=https://img.shields.io/badge/Status-Production%2520Grade-success%3Fstyle%3Dfor-the-badge%26logo%3Dstatuspage" />
<img src="https://www.google.com/search?q=https://img.shields.io/badge/LLM-Llama%25203-blue%3Fstyle%3Dfor-the-badge%26logo%3Dmeta" />
<img src="https://www.google.com/search?q=https://img.shields.io/badge/Architecture-Multi--Agent-orange%3Fstyle%3Dfor-the-badge%26logo%3Dhive" />
<img src="https://www.google.com/search?q=https://img.shields.io/badge/License-MIT-lightgrey%3Fstyle%3Dfor-the-badge" />
</p>
</div>

<br />

<!--
MAIN CANVAS: ARCHITECTURE & STANDARDS
Left: System Diagram & Core Logic
Right: Engineering Principles (The "High-Bar" Requirements)
-->

<table>
<tr>
<!-- LEFT COLUMN: ARCHITECTURE (60%) -->
<td valign="top" width="60%">
<h2>🧠 System Architecture</h2>
<p>
<b>Kasparro V2</b> is not an academic prototype; it is a resilient, autonomous loop designed to diagnose ROAS fluctuations, validate hypotheses numerically, and generate upgraded creatives.
</p>

  <h3>Agent Workflow</h3>
  <!-- MERMAID DIAGRAM -->
  <pre>


graph TD
    Start(User Query) --> Planner[📅 Planner Agent]
    Planner -->|Task Graph| Data[💾 Data Agent]
    Data -->|Metrics & Drift| Insight[💡 Insight Agent]
    Insight -->|Hypothesis| Eval[⚖️ Evaluator Agent]
    Eval -->|Validated Score| Creative[🎨 Creative Agent]
    Eval -->|Validated Score| Recs[🚀 Recs Agent]
    Creative --> Report[📝 Final Report]
    Recs --> Report


  </pre>
  <blockquote>
    <i>"The system features self-healing reflection loops. If an LLM outputs malformed JSON, the Insight Agent reflects, repairs, and retries automatically."</i>
  </blockquote>
</td>

<!-- RIGHT COLUMN: ENGINEERING STANDARDS (40%) -->
<td valign="top" width="40%">
  <h2>🛡️ Engineering Standards</h2>
  <p>Implementation of "High-Bar" reliability patterns:</p>
  
  <table>
    <tr>
      <td width="30">✅</td>
      <td>
        <b>Resilience</b><br/>
        <sub>Exponential backoff + Jitter + Deterministic fallbacks for every agent.</sub>
      </td>
    </tr>
    <tr>
      <td width="30">👁️</td>
      <td>
        <b>Observability</b><br/>
        <sub>Structured JSONL logs with <code>trace_id</code>, <code>run_id</code>, and <code>execution_id</code>.</sub>
      </td>
    </tr>
    <tr>
      <td width="30">🔒</td>
      <td>
        <b>Schema Governance</b><br/>
        <sub>Strict Z-score drift detection and Pydantic-style schema validation.</sub>
      </td>
    </tr>
    <tr>
      <td width="30">⚖️</td>
      <td>
        <b>Weighted Scoring</b><br/>
        <sub>Confidence = <code>0.4 * numeric</code> + <code>0.6 * llm_reasoning</code>.</sub>
      </td>
    </tr>
  </table>
  
  <br/>
  
  <div align="center">
    <b>Testing Strategy</b><br/>
    <img src="https://img.shields.io/badge/Coverage-Core%20Logic-success?style=flat-square" />
    <img src="https://img.shields.io/badge/Tests-Pytest-blue?style=flat-square" />
  </div>
</td>


</tr>
</table>

<!-- TECH STACK SECTION -->

<h2>🛠️ Technology Stack</h2>
<table>
<tr>
<td align="center" width="120"><b>Core</b></td>
<td>
<img src="https://www.google.com/search?q=https://skillicons.dev/icons%3Fi%3Dpython,pytorch,docker" />
</td>
<td align="center" width="120"><b>LLM Ops</b></td>
<td>
<img src="https://www.google.com/search?q=https://img.shields.io/badge/Ollama-White%3Fstyle%3Dflat-square%26logo%3Dollama%26logoColor%3Dblack" />
<img src="https://www.google.com/search?q=https://img.shields.io/badge/Llama_3-0467DF%3Fstyle%3Dflat-square%26logo%3Dmeta%26logoColor%3Dwhite" />
</td>
</tr>
</table>

<!-- AGENT CAPABILITIES TABLE -->

<h2>🤖 Agent Capabilities</h2>
<table>
<thead align="center">
<tr>
<td width="20%"><b>Agent</b></td>
<td width="50%"><b>Responsibility</b></td>
<td width="30%"><b>Key Output</b></td>
</tr>
</thead>
<tbody>
<tr>
<td><b>Data Agent</b></td>
<td>Ingests raw ads data, validates schema consistency, calculates derived metrics, and detects statistical drift.</td>
<td><code>drift_report.json</code></td>
</tr>
<tr>
<td><b>Insight Agent</b></td>
<td>Generates causal hypotheses for performance changes (e.g., "Low CTR caused ROAS drop"). Includes auto-repair reflection.</td>
<td><code>hypotheses.json</code></td>
</tr>
<tr>
<td><b>Evaluator Agent</b></td>
<td>Numerically validates hypotheses against data using weighted scoring logic (ROAS/CTR/CPC deltas).</td>
<td><code>validation_scores</code></td>
</tr>
<tr>
<td><b>Creative Agent</b></td>
<td>Synthesizes new ad copy, headlines, and hooks based on performance data of underperforming assets.</td>
<td><code>new_creatives.json</code></td>
</tr>
</tbody>
</table>

<!-- INSTALLATION & USAGE -->

<h2>🚀 Getting Started</h2>

<table>
<tr>
<td>

<b>1. Installation</b>

git clone [https://github.com/your-repo/kasparro-analyst.git](https://github.com/your-repo/kasparro-analyst.git)
pip install -r requirements.txt
ollama pull llama3


<b>2. Run Analysis</b>

# Execute the full pipeline
python run.py "Diagnose ROAS drop for Campaign A"


<b>3. Check Outputs</b>

# Structured reports generated in /reports
cat reports/report.md
cat reports/insights.json


</td>
</tr>
</table>

<!-- DIRECTORY STRUCTURE TREE -->

<details>
<summary><b>📂 Project Structure (Click to Expand)</b></summary>

kasparro-agentic-fb-analyst/
│
├── src/
│   ├── agents/             # Core logic for Planner, Data, Insight, etc.
│   ├── utils/              # LLM wrappers & Structured Logger
│   └── errors/             # Custom error handling & Recovery
│
├── prompts/                # Reasoning scaffolds & System prompts
├── logs/                   # Structured JSONL logs (trace_id tagged)
├── reports/                # Final artifacts (MD + JSON)
├── tests/                  # Unit tests for drift & schema validation
└── run.py                  # Entry point


</details>

<div align="center">
<sub><i>Built with ❤️ by Sauhard Shrivastava. Maintained for High-Bar Reliability.</i></sub>
</div>
