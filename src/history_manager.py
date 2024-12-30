import json
import glob
import os
from datetime import datetime
from rich.console import Console
from .config import Config

console = Console()

class HistoryManager:
    @staticmethod
    def get_latest_history_file():
        """Get the most recent history file from the storage directory."""
        history_files = glob.glob(f"{Config.STORAGE_DIR}/{Config.HISTORY_FILE_PREFIX}*.json")
        return max(history_files, key=os.path.getctime) if history_files else None

    @staticmethod
    def deserialize_chat_history(history_data):
        """Convert JSON history data back into a format suitable for the chat."""
        return [
            {
                "role": item["role"],
                "parts": item["parts"]
            }
            for item in history_data
        ]

    @staticmethod
    def serialize_chat_history(history):
        """Convert chat history to JSON-serializable format."""
        serialized_history = []
        for item in history:
            if hasattr(item, 'role') and hasattr(item, 'parts'):
                serialized_item = {
                    'role': item.role,
                    'parts': [
                        str(part) if hasattr(part, 'text') else part
                        for part in item.parts
                    ]
                }
                serialized_history.append(serialized_item)
        return serialized_history

    @classmethod
    def load_history(cls, filename):
        """Load chat history from a JSON file."""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                history_data = json.load(f)
            return cls.deserialize_chat_history(history_data)
        except Exception as e:
            console.print(f"[red]Error loading history from {filename}: {str(e)}[/red]")
            return []

    @staticmethod
    def save_history(chat_history):
        """Save chat history to a JSON file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{Config.STORAGE_DIR}/{Config.HISTORY_FILE_PREFIX}{timestamp}.json"
        
        serialized_history = HistoryManager.serialize_chat_history(chat_history)
        
        with open(filename, "w", encoding='utf-8') as f:
            json.dump(serialized_history, f, indent=2, ensure_ascii=False)
        console.print(f"History saved to {filename}")