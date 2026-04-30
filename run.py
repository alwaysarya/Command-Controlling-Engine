"""
CMD ENGINE - Windows
Main entry point. Start with: python run.py
Modes: cli (default), server (phone control), voice (microphone)
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.brain import quick_parse, is_ai_available
from core.executor import run as execute
from core.memory import remember_command, get_recent_commands
from outputs.speak import say


def print_banner():
    banner = r"""
    ╔══════════════════════════════════╗
    ║         CMD ENGINE v1.0         ║
    ║    "Your PC, Your Voice"        ║
    ╚══════════════════════════════════╝
    """
    print(banner)


def process_command(user_input):
    """
    Full pipeline: Brain -> Executor -> Memory -> Response
    """
    user_input = user_input.strip()
    if not user_input:
        return ""

    print(f"\n📢 Command: {user_input}")

    action = quick_parse(user_input)
    print(f"🧠 Action: {action}")

    result = execute(action)
    print(f"⚡ Result: {result}")

    remember_command(user_input, result, action)

    try:
        say(result)
    except:
        pass

    return result


def cli_mode():
    print_banner()
    print("\nCLI MODE - Type commands. 'exit' to quit, 'history' for past commands.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nShutting down...")
            break

        if not user_input:
            continue

        if user_input.lower() in ["exit", "quit", "q"]:
            print("Goodbye!")
            break

        if user_input.lower() == "history":
            commands = get_recent_commands(5)
            if not commands:
                print("No history yet.")
            else:
                print("\nRecent commands:")
                for entry in commands:
                    print(f"  [{entry['timestamp']}] {entry['user']} -> {entry['response']}")
            continue

        if user_input.lower() == "repeat":
            from core.memory import repeat_last_command
            repeated = repeat_last_command()
            if repeated == "No previous command to repeat.":
                print(repeated)
                continue
            print(f"Repeating: {repeated}")
            user_input = repeated

        response = process_command(user_input)
        print(f"CMD ENGINE: {response}")


def server_mode():
    from inputs.phone_server import start_server
    print_banner()
    print("\nSERVER MODE - Waiting for phone connections on port 9999\n")
    start_server()


def voice_mode():
    from inputs.voice_mac import start_listening
    print_banner()
    print("\nVOICE MODE - Listening on microphone\n")
    start_listening()


def main():
    print("Checking AI availability...")
    if is_ai_available():
        print("AI brain is ready.")
    else:
        print("AI not available. Running with basic commands only.")
        print("To enable AI: install Ollama from ollama.com and run 'ollama pull llama3'")

    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
    else:
        mode = "cli"

    if mode == "server":
        server_mode()
    elif mode == "voice":
        voice_mode()
    else:
        cli_mode()


if __name__ == "__main__":
    main()