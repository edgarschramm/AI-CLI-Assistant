import subprocess
import re
from rich.console import Console
from rich.prompt import Prompt
from .config import CommandMode, Config
from .whitelist_manager import WhitelistManager

console = Console()

class CommandProcessor:
    def __init__(self, command_mode=Config.DEFAULT_COMMAND_MODE):
        self.command_mode = command_mode
        self.whitelist_manager = WhitelistManager()

    def should_confirm_command(self, command):
        """Determine if command needs confirmation based on mode and whitelist."""
        if self.command_mode == CommandMode.ALWAYS_CONFIRM:
            return False
        elif self.command_mode == CommandMode.ALWAYS_ASK:
            return True
        elif self.command_mode == CommandMode.WHITELIST:
            return not self.whitelist_manager.is_whitelisted(command)
        return True

    def execute_command(self, command):
        """Execute a shell command with confirmation based on mode and whitelist."""
        if self.should_confirm_command(command):
            confirmed = Prompt.ask(f"Execute command?(y/n)", default="n").lower()
            if not confirmed in ["yes", "y", "true", "1"]:
                return "Command denied by user with the reason: " + confirmed
        else:
            if self.command_mode == CommandMode.WHITELIST:
                console.print(f"[green]Command whitelisted, executing: {command}[/green]")
            else:
                console.print(f"[yellow]Auto-confirming command: {command}[/yellow]")
        
        output = subprocess.run(command, shell=True, text=True, capture_output=True)
        return output.stdout + output.stderr + " "

    def process_response(self, response, chat):
        """Process a response containing commands."""
        while "CMD" in response.text and "CMD_END" in response.text:
            commands = re.findall(r'CMD(.*?)CMD_END', response.text, re.DOTALL)
            compound_command = " && ".join(command.strip() for command in commands)
            console.print(f"[red]$ {compound_command}[/red]")
            output = self.execute_command(compound_command)
            console.print(f"[blue]{output}[/blue]")
            response = chat.send_message(output)
            console.print(f"[green]{response.text}[/green]")