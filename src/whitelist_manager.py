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
        # Split the compound command and strip whitespace
        individual_commands = [cmd.strip() for cmd in command.split('&&')]
        
        # Check each command separately
        for cmd in individual_commands:
            if not any(fnmatch.fnmatch(cmd.strip(), pattern) for pattern in self.whitelist):
                return False
        
        # Only return True if all commands matched
        return True
