from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"
load_dotenv(ENV_FILE)


def _flag(name: str, default: str = "false") -> bool:
    return os.getenv(name, default).strip().lower() == "true"


ASSISTANT_NAME = os.getenv("ASSISTANT_NAME", "Echo-Mind")
USER_NAME = os.getenv("USER_NAME", "User")
DEBUG_MODE = _flag("DEBUG_MODE")
MAX_MEMORY = int(os.getenv("MAX_MEMORY", "20"))
LLM_TIMEOUT_SECONDS = int(os.getenv("LLM_TIMEOUT_SECONDS", "15"))
LISTEN_TIMEOUT = int(os.getenv("LISTEN_TIMEOUT", "6"))
LISTEN_PHRASE_LIMIT = int(os.getenv("LISTEN_PHRASE_LIMIT", "8"))
VOICE_RATE = int(os.getenv("VOICE_RATE", "175"))
LISTEN_RETRY_DELAY_MS = int(os.getenv("LISTEN_RETRY_DELAY_MS", "600"))
SCREENSHOT_DIR = BASE_DIR / os.getenv("SCREENSHOT_DIR", "screenshots")

STT_ENGINE = os.getenv("STT_ENGINE", "google")
TTS_ENGINE = os.getenv("TTS_ENGINE", "pyttsx3")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq").strip().lower()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
