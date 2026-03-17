# Echo-Mind Voice Assistant

PyQt6 desktop assistant with voice-first control, Groq/OpenAI reasoning, and quick automation for common tasks like YouTube/Google search, screenshots, and app/URL launching.

## Features
- Push-to-talk loop with SpeechRecognition + PyAudio and animated waveform feedback.
- Local TTS (pyttsx3) with optional mute when unavailable.
- Groq (default) or OpenAI chat completions with short-term memory persistence.
- Quick actions: YouTube search/play, Google search, open apps/URLs, capture screenshots, and Wikipedia lookups.
- In-app settings dialog to save API keys to `.env`.
- Mission Control UI with transcript log and preset prompts.

## Requirements
- Python 3.10+ on Windows (tested with PyQt6).
- Microphone access for STT; speakers for TTS.
- PortAudio runtime (PyAudio depends on it).

## Setup
1) Create and activate a virtual environment (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
2) Install dependencies:
```powershell
pip install -r requirements.txt
```
3) Add a `.env` in the project root (values are examples—do not commit real keys):
```bash
ASSISTANT_NAME=Echo-Mind
USER_NAME=User
LLM_PROVIDER=groq          # or openai
GROQ_API_KEY=your_groq_key
GROQ_MODEL=llama-3.3-70b-versatile
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-4o-mini
LISTEN_TIMEOUT=6
LISTEN_PHRASE_LIMIT=8
VOICE_RATE=175
SCREENSHOT_DIR=screenshots
WEATHER_API_KEY=your_weather_api_key   # optional
```
4) Launch the app from the repo root:
```powershell
python main.py
```

## Using the app
- **Start Listening** toggles continuous mic capture; say "stop" to end.
- Type in the composer and click **Send** for text-only queries.
- Quick Actions: open or play on YouTube, Google search, take screenshot, Wikipedia query.
- **Settings** (top right) saves OpenAI/Groq keys to `.env`; restart to reload.
- **Clear Memory** wipes recent chat context used for LLM prompts.

## Troubleshooting
- PyAudio install issues: ensure PortAudio is available or use a prebuilt wheel.
- If TTS is off, check system audio devices; the app will still show text replies.
- Groq/OpenAI errors typically mean missing/invalid API keys or network reachability; confirm keys in `.env`.
