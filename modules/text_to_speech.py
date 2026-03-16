from __future__ import annotations

from threading import Lock, Thread

import pyttsx3

from config.config import VOICE_RATE


class TextToSpeechService:
    def __init__(self) -> None:
        self._lock = Lock()
        try:
            self._engine = pyttsx3.init()
            self._engine.setProperty("rate", VOICE_RATE)
        except Exception:
            self._engine = None

    @property
    def available(self) -> bool:
        return self._engine is not None

    def speak(self, text: str) -> bool:
        if not text or self._engine is None:
            return False
        with self._lock:
            try:
                self._engine.say(text)
                self._engine.runAndWait()
                return True
            except Exception:
                return False

    def speak_async(self, text: str) -> bool:
        if self._engine is None:
            return False
        Thread(target=self.speak, args=(text,), daemon=True).start()
        return True


_SERVICE = TextToSpeechService()


def speak(text: str) -> bool:
    return _SERVICE.speak(text)


def speak_async(text: str) -> bool:
    return _SERVICE.speak_async(text)
