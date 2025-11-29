import json
import uuid
import time
from datetime import datetime

class AgentLogger:
    def __init__(self, logfile="logs/agent_runs.jsonl"):
        self.logfile = logfile
        self.run_id = str(uuid.uuid4())  # correlation ID

    def log(self, agent: str, input_data: dict, output_data: dict, level="INFO"):        
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "run_id": self.run_id,
            "level": level,
            "agent": agent,
            "input": input_data,
            "output": output_data,
        }
        with open(self.logfile, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")

    def log_runtime(self, agent: str, start_time: float, extra=None):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "run_id": self.run_id,
            "level": "INFO",
            "agent": agent,
            "runtime_ms": round((time.time() - start_time) * 1000, 3),
            "extra": extra
        }
        with open(self.logfile, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")

    def log_error(self, agent: str, message: str, context=None):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "run_id": self.run_id,
            "level": "ERROR",
            "agent": agent,
            "error": message,
            "context": context,
        }
        with open(self.logfile, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
