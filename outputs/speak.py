"""
CMD ENGINE - Speech Output (Windows)
Text-to-speech using Windows built-in SAPI voice engine.
No internet needed. Runs in a separate thread so it never blocks.
"""

import threading

try:
    import pyttsx3
    _engine = None
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False


_enabled = True
_rate = 180  # Words per minute (150-250 is natural)
_voice_id = None  # None = default voice


def _get_engine():
    """Get or create the TTS engine (lazy init)."""
    global _engine
    if not TTS_AVAILABLE:
        return None
    if _engine is None:
        _engine = pyttsx3.init()
        _engine.setProperty("rate", _rate)
        if _voice_id:
            _engine.setProperty("voice", _voice_id)
    return _engine


def say(text, voice=None, rate=None):
    """
    Speak text out loud. Runs in a thread so it doesn't block.
    """
    if not _enabled or not TTS_AVAILABLE:
        return

    def _speak():
        try:
            engine = _get_engine()
            if engine is None:
                return

            # Temporarily override voice if specified
            current_voice = engine.getProperty("voice")
            current_rate = engine.getProperty("rate")

            if voice:
                # Find voice by name
                voices = engine.getProperty("voices")
                for v in voices:
                    if voice.lower() in v.name.lower():
                        engine.setProperty("voice", v.id)
                        break

            if rate:
                engine.setProperty("rate", rate)

            # Clean text
            clean_text = text.replace("&", "and").strip()
            engine.say(clean_text)
            engine.runAndWait()

            # Restore previous settings
            if voice:
                engine.setProperty("voice", current_voice)
            if rate:
                engine.setProperty("rate", current_rate)

        except Exception as e:
            print(f"Speech error: {e}")

    thread = threading.Thread(target=_speak, daemon=True)
    thread.start()


def whisper(text):
    """Speak quietly (slower)."""
    say(text, rate=140)


def announce(text):
    """Speak loudly (faster, more urgent)."""
    say(text, rate=220)


def mute():
    """Globally mute speech."""
    global _enabled
    _enabled = False
    return "Speech muted"


def unmute():
    """Globally unmute speech."""
    global _enabled
    _enabled = True
    return "Speech unmuted"


def set_rate(wpm):
    """Set speaking speed in words per minute."""
    global _rate
    _rate = max(80, min(400, wpm))
    engine = _get_engine()
    if engine:
        engine.setProperty("rate", _rate)
    return f"Speech rate: {_rate} WPM"


def list_voices():
    """Return list of installed voices."""
    if not TTS_AVAILABLE:
        return ["TTS not available. Install pyttsx3"]
    engine = _get_engine()
    if engine is None:
        return ["Engine not initialized"]
    voices = engine.getProperty("voices")
    return [v.name for v in voices]


def set_voice(voice_name):
    """Change the speaking voice by name."""
    global _voice_id
    if not TTS_AVAILABLE:
        return "TTS not available"
    engine = _get_engine()
    if engine is None:
        return "Engine not initialized"
    voices = engine.getProperty("voices")
    for v in voices:
        if voice_name.lower() in v.name.lower():
            _voice_id = v.id
            engine.setProperty("voice", v.id)
            return f"Voice: {v.name}"
    available = ", ".join([v.name for v in voices[:5]])
    return f"Voice not found. Available: {available}"


def stop():
    """Stop any currently playing speech."""
    if not TTS_AVAILABLE:
        return
    try:
        engine = _get_engine()
        if engine:
            engine.stop()
    except:
        pass


# Test
if __name__ == "__main__":
    print("Speech test\n")

    if TTS_AVAILABLE:
        voices = list_voices()
        print(f"Voices: {len(voices)} installed")
        for v in voices[:5]:
            print(f"  - {v}")

        say("CMD Engine is online. All systems ready.")
        print("Speaking... (you should hear it now)")
    else:
        print("Install pyttsx3: pip install pyttsx3")