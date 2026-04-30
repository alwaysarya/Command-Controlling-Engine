🚀 CMD ENGINE
Voice-controlled AI automation for Windows.

Control your PC with your voice — from your phone, microphone, or even claps. Open apps, manage files, adjust settings, search the web, play music, and run custom workflows. All in natural language.



✨ Features
🎤 Voice Input
Wake word detection — say "Hey Computer" and your PC listens

Phone control — browser-based interface, tap mic or type commands

Clap detection — 👏👏 for screenshot, 👏👏👏 for lock screen



🧠 Smart Commands
Quick match — instant response for common commands

AI brain — optional Ollama integration for understanding any complex request

Memory — remembers recent commands and preferences



⚡ Actions
Module	What It Does
Apps	Open, close, switch any application
System	Volume, brightness, lock, sleep, shutdown
Keyboard	Type text, press keys, shortcuts
Mouse	Click, scroll, move, drag
Files	Create, delete, search, organize
Web	Open URLs, Google, YouTube, Wikipedia
Screenshots	Full screen, area, timed
Music	Play, pause, skip, Spotify controls
Custom	Multi-step macros (morning routine, work mode, etc.)
📱 Phone Interface
Clean dark UI



Works on any browser (Chrome, Safari, Samsung Internet)

Quick command buttons

No app install needed



🔧 Installation
Prerequisites
Windows 10/11

Python 3.10+

Microphone (for voice/clap features)



One-Command Setup
bash
pip install -r requirements.txt
python run.py
Optional: AI Brain
Install Ollama

Run ollama pull llama3

Restart CMD ENGINE — AI commands now work



🎮 Usage
bash
# Interactive CLI mode
python run.py

# Phone server mode (control from your phone)
python run.py server

# Voice mode (listen on microphone)
python run.py voice
On Your Phone
Start server mode

Open http://YOUR-PC-IP:9999 on your phone browser

Type or tap mic, speak, send

Voice Commands
text
"open notepad"
"search google for weather today"
"volume up"
"take a screenshot"
"what time is it"
"lock screen"
"create file notes.txt"



📁 Project Structure
text
cmd_engine/
├── core/           # Brain, executor, memory
├── inputs/         # Voice, phone server, clap detector
├── outputs/        # Speech, notifications, display
├── actions/        # Apps, system, files, web, music, etc.
├── phone/          # Web interface (HTML/CSS/JS)
├── config/         # Settings and triggers
├── run.py          # Main entry point
└── requirements.txt
🛠 Built With
Python — core engine

Ollama — local AI (optional)

pyautogui — keyboard/mouse automation

pyttsx3 — text-to-speech

SpeechRecognition — voice input

Flask — phone server

📄 License
MIT — see LICENSE



🙌 Author
Arya Ranjan (alwaysarya)