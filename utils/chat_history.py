import json
import os

CHAT_HISTORY_FILE = "chat_history.json"

def load_chat_history():
    """Load chat history from a JSON file and ensure it's a list."""
    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
                if isinstance(data, list):  # Ensure it's a list
                    return data
                return []  # Return empty list if it's not a valid list
            except json.JSONDecodeError:
                return []  # Return empty list if JSON is invalid
    return []

def save_chat_history(chat_history):
    """Save chat history to a JSON file."""
    with open(CHAT_HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(chat_history, file, indent=4)
