# CLI Assistant

A command-line chat interface powered by Google's Gemini AI model, with support for executing shell commands, persistent chat history, and command whitelisting.

## Features

- Interactive chat interface with Gemini AI
- Execute shell commands through chat interactions
- Persistent chat history with automatic loading/saving
- Command execution safety features

## Installation

1. Clone the repository:
```bash
git clone https://github.com/edgarschramm/AI-CLI-Assistant.git
cd cli-assistant
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your Gemini API key:
```bash
export GEMINI_API_KEY='your-api-key-here'
```

## Usage

### Basic Usage
```bash
python main.py
```

### Command Line Arguments
- `--new`: Start a new chat without loading history
- `--history <filename>`: Load a specific history file
- `--command-mode <mode>`: Set command confirmation mode
  - `ask`: Always ask for confirmation (default)
  - `yes`: Always confirm commands
  - `whitelist`: Use whitelist to determine confirmation


### Chat Commands
- `exit`: Save history and exit
- `save_history`: Save current chat history


### Command Whitelisting

Edit `whitelist` to add trusted commands. Supports exact matches and wildcards:
```
# Example whitelist entries
ls *
git status
git pull
echo *
```


## License

GNU GPLv3 