import json
import time
from datetime import datetime
import os

class AgentLogger:
    def __init__(self, log_path="logs/agent_runs.jsonl"):
        self.log_path = log_path
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

    def log(self, agent_name: str, input_data, output_data, extra=None):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "agent": agent_name,
            "input": input_data,
            "output": output_data,
            "extra": extra,
            "runtime_ms": int(time.time() * 1000)
        }

        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
