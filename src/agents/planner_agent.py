class PlannerAgent:
    """
    Simple rule-based planner.
    For now, it creates a fixed sequence of tasks depending on metric asked.
    """

    def plan(self, query: str):
        query = query.lower()

        task_list = []

        # 1. Identify metric
        if "roas" in query:
            metric = "roas"
        elif "ctr" in query:
            metric = "ctr"
        elif "clicks" in query:
            metric = "clicks"
        elif "impressions" in query:
            metric = "impressions"
        else:
            metric = "roas"  # default

        # 2. Identify adset name
        adset = None
        words = query.split()
        for w in words:
            if "adset" in w:
                adset = w.replace("adset", "").strip()

        # 3. Create hardcoded task list
        task_list = [
            {"task": "load_data"},
            {"task": "fetch_timeseries", "metric": metric, "adset": adset},
            {"task": "analyze_trends", "metric": metric},
            {"task": "evaluate_insights"},
            {"task": "generate_recommendations"},
        ]

        return task_list
