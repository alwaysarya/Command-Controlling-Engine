"""
CMD ENGINE - Memory
Stores command history, user preferences, and session context.
Simple JSON file storage. No database needed.
"""

import json
import os
from datetime import datetime
from pathlib import Path


# Where memory lives
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")
PREFS_FILE = os.path.join(DATA_DIR, "preferences.json")
CONTEXT_FILE = os.path.join(DATA_DIR, "context.json")

MAX_HISTORY = 50


def _ensure_data_dir():
    """Make sure the data folder exists."""
    Path(DATA_DIR).mkdir(parents=True, exist_ok=True)


def _load(filepath, default):
    """Safely load a JSON file."""
    _ensure_data_dir()
    if not os.path.exists(filepath):
        return default
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return default


def _save(filepath, data):
    """Safely save data to JSON."""
    _ensure_data_dir()
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ════════════════════════
#  COMMAND HISTORY
# ════════════════════════

def remember_command(user_input, response, action=None):
    """Save a command to history."""
    history = _load(HISTORY_FILE, [])

    entry = {
        "timestamp": datetime.now().isoformat(),
        "user": user_input,
        "response": response,
        "action": action
    }

    history.append(entry)

    if len(history) > MAX_HISTORY:
        history = history[-MAX_HISTORY:]

    _save(HISTORY_FILE, history)


def get_recent_commands(count=5):
    """Return the last N commands."""
    history = _load(HISTORY_FILE, [])
    return history[-count:] if history else []


def get_last_command():
    """Return the most recent command, or None."""
    history = _load(HISTORY_FILE, [])
    return history[-1] if history else None


def repeat_last_command():
    """Return the text of the last command."""
    last = get_last_command()
    if last:
        return last.get("user", "")
    return "No previous command to repeat."


def clear_history():
    """Wipe all history."""
    _save(HISTORY_FILE, [])
    return "History cleared."


def search_history(keyword):
    """Search through command history."""
    history = _load(HISTORY_FILE, [])
    keyword = keyword.lower()
    matches = []
    for entry in history:
        user = entry.get("user", "").lower()
        response = entry.get("response", "").lower()
        if keyword in user or keyword in response:
            matches.append(entry)
    return matches


# ════════════════════════
#  USER PREFERENCES
# ════════════════════════

def set_preference(key, value):
    """Save a user preference."""
    prefs = _load(PREFS_FILE, {})
    prefs[key] = value
    _save(PREFS_FILE, prefs)


def get_preference(key, default=None):
    """Get a preference value."""
    prefs = _load(PREFS_FILE, {})
    return prefs.get(key, default)


def get_all_preferences():
    """Return all preferences."""
    return _load(PREFS_FILE, {})


def delete_preference(key):
    """Remove a preference."""
    prefs = _load(PREFS_FILE, {})
    if key in prefs:
        del prefs[key]
        _save(PREFS_FILE, prefs)
        return True
    return False


# ════════════════════════
#  SESSION CONTEXT
# ════════════════════════

def set_context(key, value):
    """Store temporary session context."""
    ctx = _load(CONTEXT_FILE, {})
    ctx[key] = value
    _save(CONTEXT_FILE, ctx)


def get_context(key, default=None):
    """Get a context value."""
    ctx = _load(CONTEXT_FILE, {})
    return ctx.get(key, default)


def clear_context():
    """Wipe all session context."""
    _save(CONTEXT_FILE, {})


def get_full_context():
    """Return the entire context dict."""
    return _load(CONTEXT_FILE, {})


# ════════════════════════
#  HELPERS
# ════════════════════════

def get_conversation_summary():
    """Return a summary of recent commands for AI context."""
    recent = get_recent_commands(10)
    if not recent:
        return "No recent commands."

    lines = []
    for entry in recent:
        user = entry.get("user", "")
        response = entry.get("response", "")
        lines.append(f"User: {user} | Response: {response}")

    return "\n".join(lines)


# Test
if __name__ == "__main__":
    print("Memory test\n")

    remember_command("open notepad", "Opened Notepad", {"action": "open_app"})
    remember_command("volume up", "Volume up", {"action": "volume:up"})

    print("Recent commands:")
    for cmd in get_recent_commands(3):
        print(f"  {cmd['user']} -> {cmd['response']}")

    set_preference("voice_speed", "fast")
    print(f"Preference: {get_preference('voice_speed')}")

    set_context("current_app", "notepad")
    print(f"Context: {get_context('current_app')}")

    # Clean up test data
    clear_history()
    delete_preference("voice_speed")
    clear_context()
    print("Test complete.")