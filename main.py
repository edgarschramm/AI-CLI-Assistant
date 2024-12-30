import signal
import sys
from rich.console import Console
from src.config import Config, CommandMode
from src.history_manager import HistoryManager
from src.command_processor import CommandProcessor
from src.chat_manager import ChatManager
from src.cli import CLI
from src.prompt import get_system_prompt

console = Console()
chat = None

def signal_handler(sig, frame):
    """Handle Ctrl+C by saving history before exit"""
    console.print("\n\nCaught Ctrl+C, saving history before exit...")
    if chat and hasattr(chat, 'history'):
        HistoryManager.save_history(chat.history)
    console.print("Goodbye!")
    sys.exit(0)

def main():
    global chat
    
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        Config.validate()
        args = CLI.parse_arguments()
        
        # Set command mode
        command_mode = CommandMode(args.command_mode)
        
        initial_history = []
        if not args.new:
            history_file = args.history if args.history else HistoryManager.get_latest_history_file()
            if history_file:
                console.print(f"Loading history from {history_file}")
                initial_history = HistoryManager.load_history(history_file)
                if initial_history:
                    console.print(f"Loaded {len(initial_history)} messages from history")
                else:
                    console.print("Starting fresh chat (no history loaded)")
        
        chat = ChatManager.initialize_chat(get_system_prompt(), initial_history)
        command_processor = CommandProcessor(command_mode)
        
        # Print current mode
        console.print(f"[yellow]Command mode: {command_mode.value}[/yellow]")
        if command_mode == CommandMode.WHITELIST:
            console.print(f"[yellow]Whitelist file: {Config.WHITELIST_FILE}[/yellow]")
        
        CLI.run_chat_loop(chat, command_processor, HistoryManager)
        
    except Exception as e:
        console.print(f"\n[red]Error: {str(e)}[/red]")
        if chat and hasattr(chat, 'history'):
            console.print("Saving history before exit due to error...")
            HistoryManager.save_history(chat.history)
        raise

if __name__ == "__main__":
    main()
