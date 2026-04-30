"""
CMD ENGINE - Executor (Windows)
Takes an action dict and runs it on Windows.
No AI here — just pure automation.
"""

import subprocess
import os
import time
import datetime
import webbrowser
from pathlib import Path


def run(action):
    """
    Execute an action dict like {'action': 'open_app', 'params': {'app_name': 'notepad'}}
    Returns a human-readable result string.
    """

    act = action.get("action", "")
    params = action.get("params", {})

    # --- APP CONTROL ---

    if act == "open_app":
        return _open_app(params.get("app_name", ""))

    elif act == "close_app":
        return _close_app(params.get("app_name", ""))

    # --- VOLUME ---

    elif act == "volume:up":
        return _volume_up()

    elif act == "volume:down":
        return _volume_down()

    elif act == "volume:mute":
        return _volume_mute()

    elif act == "volume:level":
        return _volume_set(params.get("level", 50))

    # --- BRIGHTNESS (laptops only) ---

    elif act == "brightness:up":
        return _brightness_up()

    elif act == "brightness:down":
        return _brightness_down()

    # --- KEYBOARD ---

    elif act == "type_text":
        return _type_text(params.get("text", ""))

    elif act == "press_key":
        return _press_key(params.get("key", ""))

    elif act == "press_combo":
        return _press_combo(params.get("combo", ""))

    # --- SYSTEM ---

    elif act == "screenshot":
        return _screenshot()

    elif act == "lock_screen":
        return _lock_screen()

    elif act == "sleep":
        return _sleep()

    elif act == "shutdown":
        return _shutdown()

    elif act == "restart":
        return _restart()

    # --- WEB ---

    elif act == "open_url":
        return _open_url(params.get("url", ""))

    elif act == "search_web":
        return _search_web(params.get("query", ""))

    # --- FILES ---

    elif act == "search_files":
        return _search_files(params.get("name", ""))

    elif act == "create_file":
        return _create_file(params.get("path", ""))

    elif act == "delete_file":
        return _delete_file(params.get("path", ""))

    elif act == "create_folder":
        return _create_folder(params.get("path", ""))

    # --- MUSIC (basic media keys) ---

    elif act == "play_music":
        return _media_key("playpause")

    elif act == "pause_music":
        return _media_key("playpause")

    elif act == "next_track":
        return _media_key("nexttrack")

    elif act == "previous_track":
        return _media_key("prevtrack")

    # --- INFO ---

    elif act == "tell_time":
        return _tell_time()

    elif act == "tell_date":
        return _tell_date()

    elif act == "take_note":
        return _take_note(params.get("content", ""))

    elif act == "run_shell":
        return _run_shell(params.get("command", ""))

    # --- FALLBACK ---

    elif act == "unknown":
        return "Sorry, I didn't understand that command."

    elif act == "error":
        return f"Something went wrong: {params.get('message', 'Unknown error')}"

    else:
        return f"Action '{act}' is not implemented yet."


# ═══════════════════════════════════
#  APP CONTROL
# ═══════════════════════════════════

def _open_app(app_name):
    """Open an application by name."""
    try:
        # Try common Windows apps first
        common = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "calc": "calc.exe",
            "paint": "mspaint.exe",
            "explorer": "explorer.exe",
            "file explorer": "explorer.exe",
            "cmd": "cmd.exe",
            "command prompt": "cmd.exe",
            "powershell": "powershell.exe",
            "task manager": "taskmgr.exe",
            "control panel": "control.exe",
            "settings": "ms-settings:",
            "chrome": "chrome",
            "google chrome": "chrome",
            "firefox": "firefox",
            "edge": "msedge",
            "microsoft edge": "msedge",
            "spotify": "spotify",
            "vs code": "code",
            "vscode": "code",
            "visual studio code": "code",
        }

        app_lower = app_name.lower()
        if app_lower in common:
            subprocess.Popen(common[app_lower], shell=True)
        else:
            # Try direct
            subprocess.Popen(app_name, shell=True)

        return f"Opened {app_name}"

    except Exception as e:
        return f"Could not open {app_name}: {e}"


def _close_app(app_name):
    """Close an application by name."""
    try:
        subprocess.run(["taskkill", "/IM", f"{app_name}.exe", "/F"],
                       capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        return f"Closed {app_name}"
    except Exception as e:
        return f"Could not close {app_name}: {e}"


# ═══════════════════════════════════
#  VOLUME
# ═══════════════════════════════════

def _volume_up():
    """Increase volume."""
    try:
        import pyautogui
        pyautogui.press("volumeup")
        return "Volume up"
    except:
        return "Volume control requires pyautogui"


def _volume_down():
    """Decrease volume."""
    try:
        import pyautogui
        pyautogui.press("volumedown")
        return "Volume down"
    except:
        return "Volume control requires pyautogui"


def _volume_mute():
    """Toggle mute."""
    try:
        import pyautogui
        pyautogui.press("volumemute")
        return "Muted/Unmuted"
    except:
        return "Volume control requires pyautogui"


def _volume_set(level):
    """Set volume level (0-100). Uses nircmd if available."""
    try:
        subprocess.run(["nircmd", "setsysvolume", str(int(level) * 655)],
                       capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        return f"Volume set to {level}%"
    except:
        return "Install nircmd for precise volume control"


# ═══════════════════════════════════
#  BRIGHTNESS
# ═══════════════════════════════════

def _brightness_up():
    """Increase brightness (laptops)."""
    try:
        import screen_brightness_control as sbc
        current = sbc.get_brightness()
        if isinstance(current, list):
            current = current[0]
        new_val = min(100, current + 10)
        sbc.set_brightness(new_val)
        return f"Brightness up -> {new_val}%"
    except:
        return "Install screen-brightness-control: pip install screen-brightness-control"


def _brightness_down():
    """Decrease brightness (laptops)."""
    try:
        import screen_brightness_control as sbc
        current = sbc.get_brightness()
        if isinstance(current, list):
            current = current[0]
        new_val = max(0, current - 10)
        sbc.set_brightness(new_val)
        return f"Brightness down -> {new_val}%"
    except:
        return "Install screen-brightness-control: pip install screen-brightness-control"


# ═══════════════════════════════════
#  KEYBOARD
# ═══════════════════════════════════

def _type_text(text):
    """Type out text."""
    try:
        import pyautogui
        pyautogui.write(text, interval=0.03)
        return f"Typed: {text}"
    except:
        return "Keyboard control requires pyautogui"


def _press_key(key):
    """Press a single key."""
    try:
        import pyautogui
        pyautogui.press(key.lower())
        return f"Pressed: {key}"
    except:
        return "Keyboard control requires pyautogui"


def _press_combo(combo):
    """Press a key combination like 'ctrl+c'."""
    try:
        import pyautogui
        keys = [k.strip().lower() for k in combo.split("+")]
        # Convert common aliases
        key_map = {"cmd": "win", "command": "win"}
        mapped = [key_map.get(k, k) for k in keys]
        pyautogui.hotkey(*mapped)
        return f"Pressed: {combo}"
    except:
        return "Keyboard control requires pyautogui"


# ═══════════════════════════════════
#  SYSTEM
# ═══════════════════════════════════

def _screenshot():
    """Take a screenshot."""
    try:
        import pyautogui
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(os.path.expanduser("~"), "Desktop", f"screenshot_{timestamp}.png")
        pyautogui.screenshot(path)
        return f"Screenshot saved: {path}"
    except:
        return "Screenshot requires pyautogui"


def _lock_screen():
    """Lock the workstation."""
    subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"],
                   capture_output=True)
    return "Screen locked"


def _sleep():
    """Put PC to sleep."""
    subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"],
                   capture_output=True)
    return "Going to sleep"


def _shutdown():
    """Shutdown PC."""
    subprocess.run(["shutdown", "/s", "/t", "5"], capture_output=True)
    return "Shutting down in 5 seconds"


def _restart():
    """Restart PC."""
    subprocess.run(["shutdown", "/r", "/t", "5"], capture_output=True)
    return "Restarting in 5 seconds"


# ═══════════════════════════════════
#  WEB
# ═══════════════════════════════════

def _open_url(url):
    """Open URL in default browser."""
    if not url.startswith("http"):
        url = "https://" + url
    webbrowser.open(url)
    return f"Opened: {url}"


def _search_web(query):
    """Search Google."""
    webbrowser.open(f"https://www.google.com/search?q={query}")
    return f"Searched: {query}"


# ═══════════════════════════════════
#  FILES
# ═══════════════════════════════════

def _search_files(name):
    """Search for files by name."""
    results = []
    for root, dirs, files in os.walk(os.path.expanduser("~"), topdown=True):
        # Limit depth
        depth = root.replace(os.path.expanduser("~"), "").count(os.sep)
        if depth > 3:
            dirs.clear()
            continue
        for f in files:
            if name.lower() in f.lower():
                results.append(os.path.join(root, f))
                if len(results) >= 10:
                    break
        if len(results) >= 10:
            break

    if results:
        return f"Found {len(results)} file(s). First: {results[0]}"
    return f"No files found for '{name}'"


def _create_file(path):
    """Create an empty file."""
    full_path = os.path.expanduser(path)
    Path(full_path).parent.mkdir(parents=True, exist_ok=True)
    Path(full_path).touch()
    return f"Created file: {full_path}"


def _delete_file(path):
    """Delete a file."""
    full_path = os.path.expanduser(path)
    if os.path.exists(full_path):
        os.remove(full_path)
        return f"Deleted: {full_path}"
    return f"File not found: {full_path}"


def _create_folder(path):
    """Create a folder."""
    full_path = os.path.expanduser(path)
    Path(full_path).mkdir(parents=True, exist_ok=True)
    return f"Created folder: {full_path}"


# ═══════════════════════════════════
#  MUSIC (media keys)
# ═══════════════════════════════════

def _media_key(action):
    """Send media key."""
    try:
        import pyautogui
        pyautogui.press(action)
        return f"Media: {action}"
    except:
        return "Media keys require pyautogui"


# ═══════════════════════════════════
#  INFO
# ═══════════════════════════════════

def _tell_time():
    """Return current time."""
    now = datetime.datetime.now().strftime("%I:%M %p")
    return f"It's {now}"


def _tell_date():
    """Return current date."""
    now = datetime.datetime.now().strftime("%A, %B %d, %Y")
    return f"Today is {now}"


def _take_note(content):
    """Save a note to Desktop."""
    path = os.path.join(os.path.expanduser("~"), "Desktop", "cmd_engine_notes.txt")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {content}\n")
    return f"Note saved: {content}"


def _run_shell(command):
    """Run a shell command."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True,
                                text=True, timeout=30, creationflags=subprocess.CREATE_NO_WINDOW)
        output = result.stdout.strip() or result.stderr.strip() or "Done"
        return output[:500]
    except subprocess.TimeoutExpired:
        return "Command timed out"
    except Exception as e:
        return f"Shell error: {e}"


# Test
if __name__ == "__main__":
    print("Executor test\n")
    print(run({"action": "tell_time", "params": {}}))
    print(run({"action": "tell_date", "params": {}}))
    print(run({"action": "unknown", "params": {}}))