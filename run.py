import json
import sys
from src.agents.planner_agent import PlannerAgent
from src.agents.data_agent import DataAgent
from src.agents.insight_agent import InsightAgent
from src.agents.evaluator_agent import EvaluatorAgent
from src.agents.creative_agent import CreativeAgent
from src.agents.recommendation_agent import RecommendationAgent


def main(user_query):
    print("\n🔵 Kasparro Agentic FB Analyst Running...\n")

    # 1. Planner Agent
    planner = PlannerAgent()
    plan = planner.plan(user_query)
    print("🧠 Plan:", plan)

    # 2. Data Agent – Load & summarize dataset
    data_agent = DataAgent()
    df = data_agent.load_data()
    metric_summary = data_agent.get_summary_metrics(df)

    # Get low CTR creatives (< 0.01)
    low_ctr = data_agent.get_low_ctr_creatives(df, threshold=0.01)

    print("\n📊 Metrics Summary:")
    print(json.dumps(metric_summary, indent=2))

    # 3. Insight Agent – LLM hypotheses
    insight_agent = InsightAgent()
    hypotheses = insight_agent.generate(metric_summary)

    print("\n💡 Raw Hypotheses:")
    print(json.dumps(hypotheses, indent=2))

    # 4. Evaluator Agent – numeric validation
    evaluator = EvaluatorAgent()
    validated = evaluator.validate(metric_summary, hypotheses)

    # Save insights.json (UTF-8 FIX)
    with open("reports/insights.json", "w", encoding="utf-8") as f:
        json.dump(validated, f, indent=2, ensure_ascii=False)

    print("\n✅ Validated Hypotheses saved → reports/insights.json")

    # 5. Creative Agent – generate new directions
    creative_agent = CreativeAgent()
    creative_output = creative_agent.generate(low_ctr)

    # Save creatives.json (UTF-8 FIX)
    with open("reports/creatives.json", "w", encoding="utf-8") as f:
        json.dump(creative_output, f, indent=2, ensure_ascii=False)

    print("🎨 Generated creatives saved → reports/creatives.json")
    
    recommendation_agent = RecommendationAgent()
    recommendations = recommendation_agent.generate(metric_summary, validated)

    # save
    with open("reports/recommendations.json", "w", encoding="utf-8") as f:
        json.dump(recommendations, f, indent=2)


    # 6. Create final report.md (UTF-8 FIX)
    report_md = build_report(validated, creative_output,recommendations)
    with open("reports/report.md", "w", encoding="utf-8") as f:
        f.write(report_md)

    print("📄 Final report saved → reports/report.md\n")
    print("🎉 Done!")


def build_report(validated, creatives, recommendations):
    md = "# Kasparro Agentic Facebook Ads Report\n\n"

    # -------------------------
    # PERFORMANCE INSIGHTS
    # -------------------------
    md += "## 📈 Validated Performance Insights\n"
    for h in validated["validated_hypotheses"]:
        md += f"- **Reason:** {h['reason']}\n"
        md += f"  - Evidence: {h['evidence']}\n"
        md += f"  - Confidence: {h['final_confidence']}\n\n"

    # -------------------------
    # CREATIVE SUGGESTIONS
    # -------------------------
    md += "\n## 🎨 New Creative Recommendations\n"
    md += "### Headlines\n"
    for h in creatives.get("new_creatives", {}).get("headlines", []):
        md += f"- {h}\n"

    md += "\n### Primary Text Variations\n"
    for t in creatives.get("new_creatives", {}).get("primary_text", []):
        md += f"- {t}\n"

    md += "\n### Hooks\n"
    for h in creatives.get("new_creatives", {}).get("hooks", []):
        md += f"- {h}\n"

    md += "\n### CTAs\n"
    for c in creatives.get("new_creatives", {}).get("ctas", []):
        md += f"- {c}\n"

    md += "\n### Offer Angles\n"
    for o in creatives.get("new_creatives", {}).get("offer_angles", []):
        md += f"- **{o.get('name','')}** — {o.get('description','')}\n"

    # -------------------------
    # ACTIONABLE RECOMMENDATIONS
    # -------------------------
    md += "\n## 🧭 Strategic Recommendations (Next Steps)\n"
    for rec in recommendations.get("recommendations", []):
        md += f"- {rec}\n"

    return md


if __name__ == "__main__":
    user_query = "Diagnose ROAS drop" if len(sys.argv) < 2 else sys.argv[1]
    main(user_query)
