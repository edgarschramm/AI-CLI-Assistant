import os
import sys
from rich.console import Console
from enum import Enum

console = Console()

class CommandMode(Enum):
    ALWAYS_ASK = 'ask'
    ALWAYS_CONFIRM = 'yes'
    WHITELIST = 'whitelist'

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    MODEL_NAME = 'gemini-2.0-flash-exp'
    STORAGE_DIR = "storage"
    HISTORY_FILE_PREFIX = "history_"
    WHITELIST_FILE = "whitelist"
    DEFAULT_COMMAND_MODE = CommandMode.ALWAYS_ASK
    
    @classmethod
    def validate(cls):
        if not cls.GEMINI_API_KEY:
            console.print("Error: GEMINI_API_KEY environment variable not set.", style="red")
            sys.exit(1)
        os.makedirs(cls.STORAGE_DIR, exist_ok=True)
        # Create whitelist file if it doesn't exist
        if not os.path.exists(cls.WHITELIST_FILE):
            with open(cls.WHITELIST_FILE, 'w') as f:
                f.write("# Add commands to whitelist (one per line)\n")
                f.write("# You can use exact commands or patterns with *\n")
                f.write("# Example:\n")
                f.write("# ls *\n")
                f.write("# git status\n")