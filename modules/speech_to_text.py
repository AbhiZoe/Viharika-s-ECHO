from __future__ import annotations

from dataclasses import dataclass

import speech_recognition as sr

from config.config import LISTEN_PHRASE_LIMIT, LISTEN_TIMEOUT, STT_ENGINE


@dataclass(slots=True)
class SpeechResult:
    text: str = ""
    error: str = ""


class SpeechToTextService:
    def __init__(self) -> None:
        self.engine_name = STT_ENGINE
        self.recognizer = sr.Recognizer()

    def listen_once(self, timeout: int = LISTEN_TIMEOUT, phrase_time_limit: int = LISTEN_PHRASE_LIMIT) -> SpeechResult:
        if self.engine_name != "google":
            return SpeechResult(error=f"STT engine '{self.engine_name}' is not configured in this build.")

        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.35)
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except ModuleNotFoundError as exc:
            if exc.name == "distutils":
                return SpeechResult(error="SpeechRecognition needs setuptools on Python 3.12. Install it with: venv\\Scripts\\python.exe -m pip install setuptools")
            return SpeechResult(error=f"Missing Python module: {exc.name}")
        except sr.WaitTimeoutError:
            return SpeechResult(error="No speech detected before timeout.")
        except OSError:
            return SpeechResult(error="Microphone is not available.")
        except Exception as exc:
            return SpeechResult(error=f"Microphone startup failed: {exc}")

        try:
            text = self.recognizer.recognize_google(audio)
            return SpeechResult(text=text.strip())
        except sr.UnknownValueError:
            return SpeechResult(error="I could not understand the audio.")
        except sr.RequestError:
            return SpeechResult(error="Speech recognition service is unavailable.")


def listen(timeout: int = LISTEN_TIMEOUT, phrase_time_limit: int = LISTEN_PHRASE_LIMIT) -> dict[str, str]:
    result = SpeechToTextService().listen_once(timeout=timeout, phrase_time_limit=phrase_time_limit)
    return {"text": result.text, "error": result.error}
