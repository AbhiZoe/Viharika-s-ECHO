from __future__ import annotations

import os
import subprocess
import sys
from threading import Thread

from config.config import VOICE_RATE

_WORKER_SCRIPT = os.path.join(os.path.dirname(__file__), "tts_worker.py")


class TextToSpeechService:
    def __init__(self) -> None:
        self._proc: subprocess.Popen | None = None
        self._available = True
        try:
            self._start_worker()
        except Exception:
            self._available = False

    def _start_worker(self) -> None:
        self._proc = subprocess.Popen(
            [sys.executable, _WORKER_SCRIPT, str(VOICE_RATE)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
        )
        # Wait for the worker to signal it's ready
        self._proc.stdout.readline()

    @property
    def available(self) -> bool:
        return self._available

    def speak_async(self, text: str, on_done=None) -> bool:
        if not text or not self._available:
            return False
        # Ensure worker is alive
        if self._proc is None or self._proc.poll() is not None:
            try:
                self._start_worker()
            except Exception:
                return False

        def _run():
            try:
                self._proc.stdin.write((text.replace("\n", " ") + "\n").encode())
                self._proc.stdin.flush()
                self._proc.stdout.readline()  # blocks until DONE
            except Exception:
                pass
            finally:
                if on_done:
                    on_done()

        Thread(target=_run, daemon=True).start()
        return True

    def stop(self) -> None:
        if self._proc is not None and self._proc.poll() is None:
            self._proc.terminate()
            try:
                self._proc.wait(timeout=2)
            except Exception:
                self._proc.kill()
            self._proc = None
            # Restart worker so next speech works immediately
            try:
                self._start_worker()
            except Exception:
                pass


_SERVICE = TextToSpeechService()


def speak_async(text: str, on_done=None) -> bool:
    return _SERVICE.speak_async(text, on_done)


def stop_speaking() -> None:
    _SERVICE.stop()
