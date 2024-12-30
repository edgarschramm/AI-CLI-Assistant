import argparse
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from .config import CommandMode

console = Console()

class CLI:
    @staticmethod
    def parse_arguments():
        """Parse command line arguments."""
        parser = argparse.ArgumentParser(description='Chat CLI with history management')
        parser.add_argument('--new', action='store_true', 
                          help='Start a new chat without loading history')
        parser.add_argument('--history', type=str, 
                          help='Load a specific history file')
        parser.add_argument('--command-mode', type=str,
                          choices=[mode.value for mode in CommandMode],
                          default=CommandMode.ALWAYS_ASK.value,
                          help='Command confirmation mode: ask (default), yes (always confirm), or whitelist')
        return parser.parse_args()

    @staticmethod
    def run_chat_loop(chat, command_processor, history_manager):
        """Run the main chat loop."""
        while True:
            user_input = Prompt.ask(">")
            if user_input.lower() == 'exit':
                history_manager.save_history(chat.history)
                break
            if user_input == "save_history":
                history_manager.save_history(chat.history)
                continue
            
            response = chat.send_message(user_input + " ")
            console.print(Markdown(response.text), style="green")
            command_processor.process_response(response, chat)