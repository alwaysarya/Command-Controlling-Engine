"""
CMD ENGINE - Brain
Understands commands. Quick match first, falls back to AI.
Windows version.
"""

import requests
import json
import subprocess
import time


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"


def is_ai_available():
    """Check if Ollama is running and reachable."""
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=2)
        return r.status_code == 200
    except:
        return False


def ensure_ollama():
    """Make sure Ollama is running."""
    if not is_ai_available():
        print("Starting Ollama...")
        subprocess.Popen(["ollama", "serve"],
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL,
                         creationflags=subprocess.CREATE_NO_WINDOW)
        time.sleep(3)


def understand_with_ai(user_input):
    """
    Send command to AI for understanding.
    Returns action dict like {'action': 'open_app', 'params': {'app_name': 'notepad'}}
    """
    ensure_ollama()

    action_list = """
Available actions:
- open_app:app_name (open any app by name)
- close_app:app_name (close an app)
- volume:up
- volume:down
- volume:mute
- volume:level (set volume 0-100)
- brightness:up
- brightness:down
- type_text:text (type the given text)
- press_key:key (press a key like enter, escape, tab)
- press_combo:combo (press combination like ctrl+c, alt+tab)
- screenshot
- lock_screen
- sleep
- shutdown
- restart
- open_url:url
- search_web:query
- search_files:name
- create_file:path
- delete_file:path
- create_folder:path
- play_music
- pause_music
- next_track
- previous_track
- tell_time
- tell_date
- take_note:content
- run_shell:command
"""

    prompt = f"""You control a Windows computer. Convert the user's command into a precise action.

{action_list}

Rules:
- Output ONLY valid JSON. No markdown. No explanation.
- The JSON must be: {{"action": "action_name", "params": {{"key": "value"}}}}
- If nothing matches: {{"action": "unknown", "params": {{}}}}

User command: "{user_input}"

JSON response:"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "temperature": 0.1
            },
            timeout=20
        )

        raw = response.json()["response"].strip()
        raw = raw.replace("```json", "").replace("```", "").strip()

        return json.loads(raw)

    except json.JSONDecodeError:
        print(f"AI returned bad JSON: {raw}")
        return {"action": "unknown", "params": {}}

    except Exception as e:
        print(f"Brain error: {e}")
        return {"action": "error", "params": {"message": str(e)}}


def quick_parse(user_input):
    """
    Fast local match for common commands.
    No AI needed. Instant response.
    Falls back to AI for complex commands.
    """
    text = user_input.lower().strip()

    # Volume
    if any(w in text for w in ["volume up", "louder", "increase volume"]):
        return {"action": "volume:up", "params": {}}
    if any(w in text for w in ["volume down", "quieter", "decrease volume", "lower volume"]):
        return {"action": "volume:down", "params": {}}
    if "mute" in text:
        return {"action": "volume:mute", "params": {}}

    # Brightness
    if any(w in text for w in ["brightness up", "brighter"]):
        return {"action": "brightness:up", "params": {}}
    if any(w in text for w in ["brightness down", "darker", "dim"]):
        return {"action": "brightness:down", "params": {}}

    # Open apps
    if text.startswith("open "):
        app = text.replace("open ", "").strip()
        return {"action": "open_app", "params": {"app_name": app}}
    if text.startswith("close "):
        app = text.replace("close ", "").strip()
        return {"action": "close_app", "params": {"app_name": app}}

    # Screenshot
    if any(w in text for w in ["screenshot", "screen capture", "capture screen"]):
        return {"action": "screenshot", "params": {}}

    # Lock / Sleep / Shutdown
    if any(w in text for w in ["lock", "lock screen", "lock my pc"]):
        return {"action": "lock_screen", "params": {}}
    if any(w in text for w in ["sleep", "put to sleep"]):
        return {"action": "sleep", "params": {}}
    if any(w in text for w in ["shutdown", "shut down", "turn off"]):
        return {"action": "shutdown", "params": {}}
    if any(w in text for w in ["restart", "reboot"]):
        return {"action": "restart", "params": {}}

    # Music
    if any(w in text for w in ["pause music", "pause song", "stop music"]):
        return {"action": "pause_music", "params": {}}
    if any(w in text for w in ["play music", "resume music"]):
        return {"action": "play_music", "params": {}}
    if any(w in text for w in ["next track", "skip", "next song"]):
        return {"action": "next_track", "params": {}}
    if any(w in text for w in ["previous track", "previous song"]):
        return {"action": "previous_track", "params": {}}

    # Time / Date
    if any(w in text for w in ["what time", "current time", "tell time"]):
        return {"action": "tell_time", "params": {}}
    if any(w in text for w in ["what day", "what date", "today", "current date"]):
        return {"action": "tell_date", "params": {}}

    # Search web
    if any(w in text for w in ["search google", "google search", "search the web", "look up"]):
        query = text.replace("search google", "").replace("google search", "").replace("search the web", "").replace("look up", "").strip()
        return {"action": "search_web", "params": {"query": query or text}}

    # Type text
    if text.startswith("type "):
        content = text.replace("type ", "").strip()
        return {"action": "type_text", "params": {"text": content}}

    # Take note
    if text.startswith("note ") or text.startswith("take note "):
        content = text.replace("note ", "").replace("take note ", "").strip()
        return {"action": "take_note", "params": {"content": content}}

    # Open URL
    if text.startswith("open url ") or text.startswith("go to "):
        url = text.replace("open url ", "").replace("go to ", "").strip()
        return {"action": "open_url", "params": {"url": url}}

    # Press a key
    if text.startswith("press "):
        key = text.replace("press ", "").strip()
        if "+" in key:
            return {"action": "press_combo", "params": {"combo": key}}
        return {"action": "press_key", "params": {"key": key}}

    # Search files
    if text.startswith("search for ") or text.startswith("find file "):
        name = text.replace("search for ", "").replace("find file ", "").strip()
        return {"action": "search_files", "params": {"name": name}}

    # Create file or folder
    if text.startswith("create file "):
        path = text.replace("create file ", "").strip()
        return {"action": "create_file", "params": {"path": path}}
    if text.startswith("create folder "):
        path = text.replace("create folder ", "").strip()
        return {"action": "create_folder", "params": {"path": path}}
    if text.startswith("delete file "):
        path = text.replace("delete file ", "").strip()
        return {"action": "delete_file", "params": {"path": path}}

    # Fall back to AI
    if is_ai_available():
        print(f"No quick match. Sending to AI: '{user_input}'")
        return understand_with_ai(user_input)

    return {"action": "unknown", "params": {}}


# Test
if __name__ == "__main__":
    print("Brain test\n")
    tests = ["open notepad", "volume up", "what time is it", "screenshot", "lock"]
    for cmd in tests:
        result = quick_parse(cmd)
        print(f"  {cmd} -> {result}")