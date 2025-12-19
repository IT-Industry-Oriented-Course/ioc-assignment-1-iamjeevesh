"""
Audit logger for compliance and tracking
Every action must be logged for healthcare compliance
"""

import json
import os
from datetime import datetime
from typing import Any, Dict

class AuditLogger:
    """Logger for tracking all agent actions"""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self.log_file = os.path.join(log_dir, f"audit_{datetime.now().strftime('%Y%m%d')}.jsonl")
    
    def log_action(
        self, 
        action_type: str, 
        function_name: str, 
        parameters: Dict[str, Any],
        result: Any,
        success: bool = True,
        error: str = None
    ):
        """Log a function call action"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action_type": action_type,
            "function_name": function_name,
            "parameters": parameters,
            "result": str(result) if result else None,
            "success": success,
            "error": error
        }
        
        with open(self.log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
        
        # Also print to console for visibility
        status = "✓" if success else "✗"
        print(f"[{status}] {action_type}: {function_name}({parameters})")
    
    def log_user_request(self, request: str):
        """Log the original user request"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "user_request",
            "request": request
        }
        
        with open(self.log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
        
        print(f"\n[USER REQUEST] {request}\n")
    
    def log_agent_response(self, response: str):
        """Log the agent's final response"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "agent_response",
            "response": response
        }
        
        with open(self.log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
        
        print(f"\n[AGENT RESPONSE]\n{response}\n")
    
    def get_logs(self, limit: int = 10) -> list:
        """Retrieve recent log entries"""
        if not os.path.exists(self.log_file):
            return []
        
        with open(self.log_file, "r") as f:
            lines = f.readlines()
        
        return [json.loads(line) for line in lines[-limit:]]