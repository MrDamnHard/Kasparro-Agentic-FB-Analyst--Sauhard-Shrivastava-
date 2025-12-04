<!--
KASPARRO AGENTIC ANALYST - HIGH-BAR V2 README
Layout: "Canvas" / Dashboard Style for Senior Engineering Projects
-->

<!-- HEADER / BANNER -->

<div align="center">
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:2a2a72,100:009ffd&height=220&section=header&text=Kasparro%20Agentic%20Analyst&fontSize=50&animation=fadeIn&fontAlignY=38&desc=Production-Grade%20Multi-Agent%20LLM%20System%20for%20Ad%20Performance&descAlignY=55&descAlign=50" width="100%" alt="Kasparro Header" />

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
<h2>🧠 System Architecture & Flow</h2>
<p>
<b>Kasparro V2</b> is a resilient, autonomous loop designed to diagnose ROAS fluctuations, validate hypotheses numerically, and generate actionable strategic and creative outputs.
</p>

<h3>Agent Workflow</h3>
<pre>

graph TD
    Start(User Query) --&gt; Planner[📅 Planner Agent]
    Planner --&gt;|Task Graph| Data[💾 Data Agent]
    Data --&gt;|Metrics &amp; Drift| Insight[💡 Insight Agent]
    Insight --&gt;|Hypothesis| Eval[⚖️ Evaluator Agent]
    Eval --&gt;|Validated Score| Creative[🎨 Creative Agent]
    Eval --&gt;|Validated Score| Recs[🚀 Recs Agent]
    Creative --&gt; Report[📝 Final Report Builder]
    Recs --&gt; Report


</pre>
<blockquote>
<i>"The system features self-healing reflection loops. If an LLM outputs malformed JSON, the Insight Agent attempts auto-repair via reflection, substring extraction, and re-parsing."</i>
</blockquote>
</td>

<!-- RIGHT COLUMN: ENGINEERING STANDARDS (40%) -->

<td valign="top" width="40%">
<h2>🛡️ Engineering Standards (High-Bar V2)</h2>
<p>Implementation of production-grade reliability patterns for LLM systems:</p>

<table>
<tr>
<td width="30">✅</td>
<td>
<b>Reliability & Resilience</b>




<sub>All external (LLM) or I/O operations are wrapped in a <code>retry_policy</code> with <b>Exponential Backoff + Jitter</b> (Max attempts: 3). Guaranteed non-blocking operation.</sub>
</td>
</tr>
<tr>
<td width="30">👁️</td>
<td>
<b>Observability & Tracing</b>




<sub>Structured JSONL logging tracks <code>run_id</code> (pipeline trace), <code>trace_id</code> (event), and <code>execution_id</code> (per agent call/retry). Supports real-time monitoring.</sub>
</td>
</tr>
<tr>
<td width="30">🔒</td>
<td>
<b>Schema Governance</b>




<sub>The Data Agent performs initial schema validation (required fields) and Z-score based <b>Drift Detection</b> on core metrics using previous 7-day data.</sub>
</td>
</tr>
<tr>
<td width="30">⚖️</td>
<td>
<b>Validation & Weighted Scoring</b>




<sub>Hypotheses are validated numerically. Final confidence is a weighted score: <code>0.4 * numeric_score + 0.6 * llm_confidence</code>.</sub>
</td>
</tr>
</table>

<div align="center">
<b>Testing Strategy</b>




<img src="https://img.shields.io/badge/Coverage-Core%20Logic-success?style=flat-square" />
<img src="https://img.shields.io/badge/Tests-Pytest-blue?style=flat-square" />
<img src="https://www.google.com/search?q=https://img.shields.io/badge/Drift%2520Logic-Tested-informational%3Fstyle%3Dflat-square" />
</div>
</td>
</tr>
</table>

<!-- DETAILED AGENT CAPABILITIES TABLE -->

<h2>🤖 Detailed Agent Breakdown</h2>
<p>Each agent operates with strict I/O contracts and deterministic fallbacks to maintain pipeline stability.</p>
<table>
<thead align="center">
<tr>
<td width="15%"><b>Agent</b></td>
<td width="15%"><b>Input</b></td>
<td width="40%"><b>Core Logic & Functions</b></td>
<td width="15%"><b>Output</b></td>
<td width="15%"><b>Fallback Strategy</b></td>
</tr>
</thead>
<tbody>
<tr>
<td><b>Planner Agent</b></td>
<td><code>User Query (str)</code></td>
<td>Parses query intent. Builds a sequential or parallel <b>Task Graph (DAG)</b> to guide execution.</td>
<td><code>ExecutionTaskGraph (list)</code></td>
<td>Returns a default, comprehensive 5-step analysis plan.</td>
</tr>
<tr>
<td><b>Data Agent</b></td>
<td><code>Raw Ads Data (CSV/DB)</code></td>
<td>1. <b>Schema Validation:</b> Checks for required columns. 2. <b>Derived Metrics:</b> Calculates eCPM, eCPC, etc. 3. <b>Drift Detection:</b> Z-score based statistical anomaly detection.</td>
<td><code>Metrics_Dict (dict)</code>, <code>Drift_Report (json)</code></td>
<td>Logs validation error. Returns <code>Metrics_Dict</code> with <code>NULL</code> values; subsequent agents proceed with warnings.</td>
</tr>
<tr>
<td><b>Insight Agent</b></td>
<td><code>Metrics_Dict</code>, <code>Drift_Report</code></td>
<td>Uses Llama 3 with structured reasoning prompt to generate 3-5 causal hypotheses. Features <b>LLM Reflection Loop</b> for auto-repairing malformed JSON output.</td>
<td><code>Hypotheses_List (json)</code></td>
<td>Fails to Reflection/Repair. On final failure, extracts JSON substring or returns list with <code>confidence: 0.0</code>.</td>
</tr>
<tr>
<td><b>Evaluator Agent</b></td>
<td><code>Hypotheses_List</code>, <code>Metrics_Dict</code></td>
<td><b>Numeric Validation:</b> Scores each hypothesis by correlating metric deltas (e.g., if ROAS is down, a hypothesis citing "CTR drop" gets a higher numeric score if CTR also dropped).</td>
<td><code>Validated_Hypotheses (json)</code></td>
<td>Logs scoring error. Returns raw hypotheses with <code>final_confidence: 0.0</code>.</td>
</tr>
<tr>
<td><b>Creative Agent</b></td>
<td><code>Validated_Hypotheses</code></td>
<td>Generates new copy/visual ideas based on the most confident validated hypothesis (e.g., if "Hook fatigue" is high-confidence, generates new hooks/CTAs).</td>
<td><code>New_Creatives_JSON (json)</code></td>
<td>Returns generic, high-performing creative templates based on hardcoded best practices.</td>
</tr>
<tr>
<td><b>Recommendation Agent</b></td>
<td><code>Validated_Hypotheses</code></td>
<td>Generates strategic actions (e.g., Scale, Pause, Test) based on the combined output of validation and drift analysis.</td>
<td><code>Recommendations_List (list)</code></td>
<td>Returns non-critical advice: "Monitor all core metrics daily."</td>
</tr>
</tbody>
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

<!-- EXAMPLE OUTPUTS -->

<h2>📊 Example Artifacts</h2>
<p>The system generates three structured JSON artifacts and one final report Markdown file.</p>

<details>
<summary><b>Example: <code>reports/insights.json</code></b></summary>

{
  "validated_hypotheses": [
    {
      "reason": "CPC volatility strongly reduced ROAS, despite a steady CVR.",
      "evidence": "CPC +45% (High Drift) & ROAS -22%",
      "final_confidence": 0.91,
      "numeric_score": 0.85
    },
    {
      "reason": "Creative fatigue in Ad Set X caused a mild CTR drop.",
      "evidence": "Ad Set X CTR -15%",
      "final_confidence": 0.78,
      "numeric_score": 0.60
    }
  ]
}


</details>

<details>
<summary><b>Example: <code>reports/creatives.json</code></b></summary>

{
  "analysis": "Hypothesis: CPC volatility is driven by auction competition. Focus new creatives on high-intent, low-cost audiences.",
  "new_creatives": {
    "headlines": ["Stop Overpaying for Leads: Get 3X ROI Now", "The Secret to <Product> Success"],
    "primary_text": ["Avoid the 4 common mistakes marketers make. Read our guide.", "..."],
    "hooks": ["Are you wasting 50% of your budget?", "Watch this 60s demo"],
    "ctas": ["Download Case Study", "Calculate Your ROI"],
    "offer_angles": ["Urgency: Limited Time Offer", "Value: 100% Money-Back Guarantee"]
  }
}


</details>

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

# Execute the full pipeline with a specific query
python run.py "Diagnose ROAS drop for Campaign A in the last 7 days vs previous 7 days"


<b>3. Check Outputs</b>

# Structured reports generated in /reports
cat reports/report.md
cat reports/insights.json
cat logs/agent_runs.jsonl


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
