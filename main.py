from src.agents.creative_agent import CreativeAgent

sample_low_ctr = [
    {
        "campaign_name": "Winter Sale",
        "adset_name": "Adset A",
        "creative_message": "50% OFF! Free Shipping!",
        "ctr": 0.005,
        "creative_type": "image"
    },
    {
        "campaign_name": "Deals",
        "adset_name": "Adset B",
        "creative_message": "Shop Now! Best Prices!",
        "ctr": 0.004,
        "creative_type": "image"
    }
]

agent = CreativeAgent()
print(agent.generate(sample_low_ctr))
