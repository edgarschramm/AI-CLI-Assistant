import google.generativeai as genai
from rich.console import Console
from .config import Config

console = Console()

class ChatManager:
    @staticmethod
    def initialize_chat(system_prompt, initial_history=None):
        """Initialize the chat with optional history."""
        genai.configure(api_key=Config.GEMINI_API_KEY)
        model = genai.GenerativeModel(
            Config.MODEL_NAME,
            system_instruction=system_prompt
        )
        return model.start_chat(history=initial_history or [])