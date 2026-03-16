from __future__ import annotations

import re
import subprocess
import webbrowser
from datetime import datetime
from pathlib import Path
from urllib.parse import quote_plus

import pyautogui
import requests

from config.config import SCREENSHOT_DIR

APP_ALIASES = {
    "chrome": ["cmd", "/c", "start", "", "chrome"],
    "google chrome": ["cmd", "/c", "start", "", "chrome"],
    "notepad": ["notepad"],
    "calculator": ["calc"],
    "calc": ["calc"],
    "paint": ["mspaint"],
    "vscode": ["code"],
    "visual studio code": ["code"],
    "explorer": ["explorer"],
    "file explorer": ["explorer"],
    "command prompt": ["cmd"],
}

KNOWN_SITES = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "github": "https://www.github.com",
    "wikipedia": "https://www.wikipedia.org",
    "gmail": "https://mail.google.com",
}


def open_application(target: str) -> bool:
    command = APP_ALIASES.get(target.strip().lower())
    if not command:
        return False
    try:
        subprocess.Popen(command)
        return True
    except OSError:
        return False


def open_url(target: str) -> bool:
    cleaned = target.strip().lower()
    if cleaned in KNOWN_SITES:
        webbrowser.open(KNOWN_SITES[cleaned])
        return True
    if "." in cleaned and " " not in cleaned:
        url = cleaned if cleaned.startswith(("http://", "https://")) else f"https://{cleaned}"
        webbrowser.open(url)
        return True
    return False


def open_youtube(query: str = "") -> None:
    if query.strip():
        webbrowser.open(f"https://www.youtube.com/results?search_query={quote_plus(query)}")
        return
    webbrowser.open(KNOWN_SITES["youtube"])


def _find_first_youtube_video(query: str) -> str | None:
    url = f"https://www.youtube.com/results?search_query={quote_plus(query)}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=6)
        response.raise_for_status()
    except requests.RequestException:
        return None

    match = re.search(r'"videoId":"([A-Za-z0-9_-]{11})"', response.text)
    if not match:
        return None
    return f"https://www.youtube.com/watch?v={match.group(1)}"


def play_on_youtube(query: str) -> bool:
    first_video = _find_first_youtube_video(query)
    if first_video:
        webbrowser.open(first_video)
        return True
    open_youtube(query)
    return False


def open_google(query: str = "") -> None:
    if query.strip():
        webbrowser.open(f"https://www.google.com/search?q={quote_plus(query)}")
        return
    webbrowser.open(KNOWN_SITES["google"])


def search_web(query: str) -> None:
    open_google(query)


def take_screenshot() -> str:
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    file_path = SCREENSHOT_DIR / f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    image = pyautogui.screenshot()
    image.save(Path(file_path))
    return str(file_path)
