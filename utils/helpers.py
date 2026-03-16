from __future__ import annotations

import json
import logging
from pathlib import Path
from threading import Lock
from typing import Iterable

from config.config import BASE_DIR, ENV_FILE, MAX_MEMORY

LOGGER = logging.getLogger(__name__)
MEMORY_LOCK = Lock()
MEMORY_FILE = BASE_DIR / "memory" / "conversation_memory.json"


def validate_message(message: object) -> bool:
    if not isinstance(message, dict):
        return False
    role = message.get("role")
    content = message.get("content")
    return role in {"system", "user", "assistant"} and isinstance(content, str) and bool(content.strip())


def ensure_memory_file() -> None:
    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not MEMORY_FILE.exists():
        MEMORY_FILE.write_text("[]\n", encoding="utf-8")


def load_memory() -> list[dict[str, str]]:
    ensure_memory_file()
    with MEMORY_LOCK:
        try:
            raw = json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            LOGGER.warning("Failed to load memory file: %s", exc)
            return []
    if not isinstance(raw, list):
        return []
    return [item for item in raw if validate_message(item)]


def save_memory(data: Iterable[dict[str, str]]) -> None:
    safe_data = [item for item in data if validate_message(item)][-MAX_MEMORY:]
    ensure_memory_file()
    with MEMORY_LOCK:
        MEMORY_FILE.write_text(json.dumps(safe_data, indent=2, ensure_ascii=False), encoding="utf-8")


def append_memory(role: str, content: str) -> None:
    memory = load_memory()
    memory.append({"role": role, "content": content.strip()})
    save_memory(memory)


def clear_memory() -> None:
    save_memory([])


def upsert_env_value(key: str, value: str) -> None:
    ENV_FILE.parent.mkdir(parents=True, exist_ok=True)
    existing_lines: list[str] = []
    if ENV_FILE.exists():
        existing_lines = ENV_FILE.read_text(encoding="utf-8").splitlines()

    rendered = f"{key}={value}"
    updated = False
    output: list[str] = []
    for line in existing_lines:
        if not line or line.lstrip().startswith("#") or "=" not in line:
            output.append(line)
            continue
        current_key = line.split("=", 1)[0].strip()
        if current_key == key:
            output.append(rendered)
            updated = True
        else:
            output.append(line)

    if not updated:
        output.append(rendered)

    ENV_FILE.write_text("\n".join(output).strip() + "\n", encoding="utf-8")
