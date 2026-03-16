from __future__ import annotations

import time
from threading import Event, Thread

from PyQt6.QtCore import QObject, pyqtSignal

from config.config import ASSISTANT_NAME, LISTEN_RETRY_DELAY_MS, TTS_ENGINE
from modules.llm_engine import ask_llm
from modules.speech_to_text import SpeechToTextService
from modules.task_router import TaskRouter
from modules.text_to_speech import TextToSpeechService


class AssistantController(QObject):
    transcript_added = pyqtSignal(str, str)
    status_changed = pyqtSignal(str)
    listening_changed = pyqtSignal(bool)
    response_ready = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()
        self._router = TaskRouter()
        self._stt = SpeechToTextService()
        self._tts = TextToSpeechService()
        self._stop_event = Event()
        self._worker: Thread | None = None

    @property
    def tts_available(self) -> bool:
        return self._tts.available

    @property
    def tts_engine_name(self) -> str:
        return TTS_ENGINE

    def start_listening(self) -> None:
        if self._worker and self._worker.is_alive():
            return
        self._stop_event.clear()
        self._worker = Thread(target=self._listen_loop, daemon=True)
        self._worker.start()

    def stop_listening(self) -> None:
        self._stop_event.set()
        self.listening_changed.emit(False)
        self.status_changed.emit("Idle")

    def submit_text(self, text: str) -> None:
        clean = text.strip()
        if not clean:
            self.error_occurred.emit("Type a message before sending.")
            return
        Thread(target=self._handle_command, args=(clean,), daemon=True).start()

    def _listen_loop(self) -> None:
        self.status_changed.emit("Listening")
        self.listening_changed.emit(True)
        while not self._stop_event.is_set():
            try:
                result = self._stt.listen_once()
            except Exception as exc:
                self.error_occurred.emit(f"Listening failed: {exc}")
                break
            if self._stop_event.is_set():
                break
            if result.error:
                self.status_changed.emit(result.error)
                time.sleep(LISTEN_RETRY_DELAY_MS / 1000)
                self.status_changed.emit("Listening")
                continue
            self._handle_command(result.text)
            if self._stop_event.is_set():
                break
            self.status_changed.emit("Listening")
            self.listening_changed.emit(True)
        self.listening_changed.emit(False)
        self.status_changed.emit("Idle")

    def _handle_command(self, command: str) -> None:
        cleaned = command.strip()
        if not cleaned:
            return

        self.listening_changed.emit(False)
        self.transcript_added.emit("user", cleaned)
        self.status_changed.emit("Thinking")

        try:
            lowered = cleaned.lower()
            if lowered in {"stop", "stop listening", "exit", "quit"}:
                reply = f"{ASSISTANT_NAME} is standing by."
                self.transcript_added.emit("assistant", reply)
                self.response_ready.emit(reply)
                self._tts.speak_async(reply)
                self.stop_listening()
                return

            route_result = self._router.route(cleaned)
            reply = route_result.response if route_result.handled else ask_llm(cleaned)
        except Exception as exc:
            reply = f"I hit an internal error while handling that request: {exc}"

        self.transcript_added.emit("assistant", reply)
        self.response_ready.emit(reply)
        self.status_changed.emit("Speaking" if self._tts.available else "Ready")
        if self._tts.available:
            self._tts.speak_async(reply)
        self.status_changed.emit("Ready")
