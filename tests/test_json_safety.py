from src.utils.llm import LLM
from src.agents.insight_agent import InsightAgent
from src.agents.creative_agent import CreativeAgent

def test_llm_json_fallback():
    llm = LLLMWrapperFakeResponse("{not json")
    res = llm.generate_json("ignored prompt")
    assert "error" in res


class LLLMWrapperFakeResponse(LLM):
    """Mocks LLM.generate to return non-JSON."""
    def generate(self, prompt: str) -> str:
        return "THIS IS NOT JSON"


def test_insight_agent_normalization():
    agent = InsightAgent()
    bad_data = {"hypotheses": [{}]}

    norm = agent._normalize(bad_data)
    assert len(norm["hypotheses"]) >= 1
    assert "reason" in norm["hypotheses"][0]


def test_creative_agent_safe_output():
    agent = CreativeAgent()
    result = agent.generate([])

    # must contain safe JSON structure
    assert "new_creatives" in result
    assert isinstance(result["new_creatives"], dict)
    assert "headlines" in result["new_creatives"]
