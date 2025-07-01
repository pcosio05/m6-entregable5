import os
from datetime import datetime
import json

class LogService:
    """
    Service for logging token usage in daily JSON files.
    Each day gets its own file in the format: token_usage_YYYY-MM-DD.json
    """
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = log_dir
        self._ensure_log_directory()

    def _ensure_log_directory(self):
        """Ensure the log directory exists"""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def _get_daily_log_file(self) -> str:
        """
        Get the path for today's log file.
        Format: logs/token_usage_YYYY-MM-DD.json
        Example: logs/token_usage_2024-03-21.json
        """
        today = datetime.now().strftime("%Y-%m-%d")
        return os.path.join(self.log_dir, f"token_usage_{today}.json")

    def log_token_usage(self, endpoint: str, input_tokens_used: int, output_tokens_used: int, model: str):
        """
        Log token usage to today's log file.
        Creates a new file for each day if it doesn't exist.
        
        Args:
            endpoint: The API endpoint that was called
            input_tokens_used: Number of tokens used in the input
            output_tokens_used: Number of tokens used in the output
            model: The AI model used
        """
        log_file = self._get_daily_log_file()
        timestamp = datetime.now().isoformat()
        
        log_entry = {
            "timestamp": timestamp,
            "endpoint": endpoint,
            "input_tokens_used": input_tokens_used,
            "output_tokens_used": output_tokens_used,
            "total_tokens_used": input_tokens_used + output_tokens_used,
            "model": model
        }

        # Read existing logs or create new list
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                try:
                    logs = json.load(f)
                except json.JSONDecodeError:
                    logs = []
        else:
            logs = []

        # Append new log entry
        logs.append(log_entry)

        # Write back to file
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2) 