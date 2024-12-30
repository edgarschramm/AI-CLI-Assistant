import os
import fnmatch
from .config import Config

class WhitelistManager:
    def __init__(self):
        self.whitelist = self.load_whitelist()
    
    def load_whitelist(self):
        """Load whitelist patterns from file."""
        if not os.path.exists(Config.WHITELIST_FILE):
            return []
        
        with open(Config.WHITELIST_FILE, 'r') as f:
            return [
                line.strip()
                for line in f
                if line.strip() and not line.startswith('#')
            ]
    
    def is_whitelisted(self, command):
        """Check if a command matches any whitelist pattern."""
        return any(
            fnmatch.fnmatch(command.strip(), pattern)
            for pattern in self.whitelist
        )
